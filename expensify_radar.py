#!/usr/bin/env python3
"""Find likely actionable Expensify paid OSS issues."""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request


QUERY = 'repo:Expensify/App "$250" "Help Wanted" state:open'

BAD_LABELS = {
    "Reviewing",
    "PR Author Review",
    "Awaiting payment",
    "Awaiting Payment",
    "Paid",
    "Hold",
    "Internal",
}


def gh_json(url: str):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "expensify-radar",
        },
    )
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    encoded = urllib.parse.urlencode(
        {
            "q": QUERY,
            "sort": "updated",
            "order": "desc",
            "per_page": "50",
        }
    )
    data = gh_json(f"https://api.github.com/search/issues?{encoded}")
    rows = []
    for item in data["items"]:
        labels = {label["name"] for label in item.get("labels", [])}
        if labels & BAD_LABELS:
            continue
        if "External" not in labels and "Help Wanted" not in labels:
            continue
        if "due for payment" in item["title"].lower():
            continue
        body = item.get("body") or ""
        comments = item.get("comments", 0)
        has_upwork = "upwork.com/jobs" in body.lower()
        score = 20
        if comments <= 10:
            score += 20
        elif comments <= 25:
            score += 10
        else:
            score -= 10
        if has_upwork:
            score += 10
        if "needs reproduction" in body.lower():
            score -= 5
        if re.search(r"\[\$[0-9,]+\]", item["title"]):
            score += 5

        rows.append((score, item["title"], item["html_url"], comments, ",".join(sorted(labels))))

    rows.sort(reverse=True)
    for score, title, url, comments, labels in rows[:15]:
        print(f"{score:>3} comments={comments:<3} {title}")
        print(f"    {url}")
        print(f"    labels: {labels}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
