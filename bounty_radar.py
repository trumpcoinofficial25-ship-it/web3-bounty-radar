#!/usr/bin/env python3
"""Find practical bounty/grant targets and write a short markdown report."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


GITHUB_QUERIES = [
    'label:bounty web3 state:open -label:in-progress',
    'label:bounty "GitHub Action" state:open',
    'label:bounty "Telegram bot" state:open',
    'label:bounty "dashboard" web3 state:open',
    'label:bounty "analytics" web3 state:open',
]

NOISE_PATTERNS = [
    "star & follow",
    "social media",
    "first impression",
    "hacker news",
    "reddit",
    "share",
    "bug bounty",
    "audit",
    "rcs support",
]

GOOD_PATTERNS = [
    "github action",
    "bot",
    "dashboard",
    "analytics",
    "monitoring",
    "authentication",
    "readme",
    "documentation",
    "frontend",
    "backend",
    "api",
    "integration",
    "tutorial",
]


@dataclass(frozen=True)
class Candidate:
    source: str
    title: str
    url: str
    reward: str
    updated: str
    score: int
    reason: str


def request_json(url: str, headers: dict[str, str] | None = None) -> Any:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "codex-bounty-radar",
            **(headers or {}),
        },
    )
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def money_from_text(text: str) -> str:
    matches = re.findall(r"(?:\$|USDC\s*)\s?[\d,]+(?:\.\d+)?|[\d,]+\s?(?:USDC|USDG|jupUSD|RTC|NIGHT)", text, re.I)
    return ", ".join(dict.fromkeys(matches[:3])) or "unknown"


def score_text(title: str, body: str, labels: list[str], comments: int, updated_at: str = "") -> tuple[int, str]:
    haystack = f"{title}\n{body}\n{' '.join(labels)}".lower()
    score = 0
    reasons: list[str] = []

    for pattern in GOOD_PATTERNS:
        if pattern in haystack:
            score += 8
            reasons.append(pattern)

    for pattern in NOISE_PATTERNS:
        if pattern in haystack:
            score -= 18
            reasons.append(f"avoid:{pattern}")

    if comments > 50:
        score -= 8
        reasons.append("crowded")
    elif comments <= 5:
        score += 4
        reasons.append("low-competition")

    if "acceptance criteria" in haystack or "deliverables" in haystack:
        score += 8
        reasons.append("clear-deliverables")

    if "kyc" in haystack:
        score -= 5
        reasons.append("kyc")

    if updated_at:
        updated = dt.datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        age_days = (dt.datetime.now(dt.timezone.utc) - updated).days
        if age_days > 365:
            score -= 40
            reasons.append("stale-1y+")
        elif age_days > 90:
            score -= 20
            reasons.append("stale-90d+")
        elif age_days <= 7:
            score += 8
            reasons.append("fresh")

    return score, ", ".join(reasons[:6]) or "general match"


def github_candidates(limit: int) -> list[Candidate]:
    seen: set[str] = set()
    candidates: list[Candidate] = []

    for query in GITHUB_QUERIES:
        encoded = urllib.parse.urlencode(
            {
                "q": query,
                "sort": "updated",
                "order": "desc",
                "per_page": "20",
            }
        )
        data = request_json(f"https://api.github.com/search/issues?{encoded}")
        for item in data.get("items", []):
            url = item["html_url"]
            if url in seen or "/pull/" in url:
                continue
            seen.add(url)

            labels = [label["name"] for label in item.get("labels", [])]
            body = item.get("body") or ""
            title = item["title"]
            score, reason = score_text(title, body, labels, item.get("comments", 0), item.get("updated_at", ""))
            candidates.append(
                Candidate(
                    source="GitHub",
                    title=title,
                    url=url,
                    reward=money_from_text(f"{title}\n{body}"),
                    updated=item.get("updated_at", ""),
                    score=score,
                    reason=reason,
                )
            )

    return sorted(candidates, key=lambda c: c.score, reverse=True)[:limit]


def superteam_candidates(limit: int) -> list[Candidate]:
    api_key = os.environ.get("SUPERTEAM_AGENT_API_KEY")
    if not api_key:
        return []

    url = "https://superteam.fun/api/agents/listings/live?take=50"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        listings = request_json(url, headers=headers)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"Superteam scan failed: {exc}", file=sys.stderr)
        return []

    now = dt.datetime.now(dt.timezone.utc)
    candidates: list[Candidate] = []
    for listing in listings:
        deadline_raw = listing.get("deadline")
        deadline = None
        if deadline_raw:
            deadline = dt.datetime.fromisoformat(deadline_raw.replace("Z", "+00:00"))

        score = 10
        reason = [listing.get("agentAccess", "agent")]
        if deadline and deadline < now:
            score -= 30
            reason.append("expired")
        if listing.get("isWinnersAnnounced"):
            score -= 25
            reason.append("winners-announced")
        if listing.get("_count", {}).get("Submission", 0) > 100:
            score -= 8
            reason.append("crowded")

        candidates.append(
            Candidate(
                source="Superteam",
                title=listing.get("title", "Untitled"),
                url=f"https://superteam.fun/earn/listing/{listing.get('slug', '')}",
                reward=f"{listing.get('rewardAmount')} {listing.get('token')}",
                updated=deadline_raw or "",
                score=score,
                reason=", ".join(reason),
            )
        )

    return sorted(candidates, key=lambda c: c.score, reverse=True)[:limit]


def write_report(candidates: list[Candidate], path: str) -> None:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Bounty radar report - {now}",
        "",
        "Scoring favors concrete engineering deliverables and penalizes social, crowded, expired, or security-heavy work.",
        "",
        "| Score | Source | Reward | Title | Why |",
        "|---:|---|---|---|---|",
    ]
    for candidate in candidates:
        title = candidate.title.replace("|", "\\|")
        reason = candidate.reason.replace("|", "\\|")
        lines.append(
            f"| {candidate.score} | {candidate.source} | {candidate.reward} | [{title}]({candidate.url}) | {reason} |"
        )
    lines.append("")
    lines.append("## Immediate playbook")
    lines.append("")
    lines.append("1. Pick the highest-scoring task with a payout in a real currency or a trusted sponsor.")
    lines.append("2. Comment from the human GitHub/Superteam account to confirm the bounty is still active.")
    lines.append("3. Build only a narrow, reviewable deliverable with tests/docs.")
    lines.append("4. Submit with a repo link, concise demo notes, and payout/contact details.")

    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=15)
    parser.add_argument("--out", default="radar-report.md")
    args = parser.parse_args()

    candidates = github_candidates(args.limit)
    candidates.extend(superteam_candidates(args.limit))
    candidates = sorted(candidates, key=lambda c: c.score, reverse=True)[: args.limit]

    write_report(candidates, args.out)
    for candidate in candidates[:8]:
        print(f"{candidate.score:>3} {candidate.source:<10} {candidate.reward:<20} {candidate.title}")
        print(f"    {candidate.url}")
        print(f"    {candidate.reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
