# Web3 Bounty Radar

Small command-line scanner for finding practical Web3 bounty targets.

It currently scans GitHub issues for bounty-like tasks, scores them, and writes a markdown report. The scoring favors concrete engineering deliverables and penalizes stale, crowded, social, expired, or security-heavy work.

## Usage

```bash
python3 bounty_radar.py --limit 20 --out radar-report.md
```

Optional Superteam Earn agent scan:

```bash
SUPERTEAM_AGENT_API_KEY=sk_... python3 bounty_radar.py --limit 20 --out radar-report.md
```

## What It Optimizes For

- real engineering deliverables,
- clear acceptance criteria,
- recent activity,
- fewer existing attempts,
- payout signal in the issue text,
- practical implementation scope.

## Current Playbook

1. Run the scanner.
2. Inspect only recent, low-competition candidates.
3. Confirm payout and assignment rules before coding.
4. Build narrow PRs with tests/docs.
5. Submit concise proof and payout/contact details.

This repo is also intended as proof-of-work for grant and bounty applications.
