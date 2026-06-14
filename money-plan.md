# Money plan for Web3 bounties

Date: 2026-06-14

## Goal

Fastest realistic path to first money:

1. Avoid crowded/expired contests.
2. Avoid security bug bounty unless we intentionally do security.
3. Target tasks with:
   - clear deliverables,
   - real payout in USDC/USD/ETH,
   - low number of existing attempts,
   - code/docs/tests we can build locally,
   - sponsor confirmation before we spend real time.

## What we can do here

Codex can:

- scan opportunities,
- inspect repos/issues,
- implement code,
- write docs/tests,
- prepare PR text/submission text,
- draft sponsor messages.

Human must:

- post GitHub/Superteam comments,
- create accounts,
- connect wallet,
- receive payout,
- reply to sponsors.

## Current state

### Superteam

Not the fastest path today.

The agent API works, but the useful dev/agent listings currently surfaced are mostly expired, in review, or heavily crowded.

### GitHub/Spectral Finance Lux

Possible money, but not instant.

Pros:

- real repo,
- multiple issues list budgets from `$750` to `$2,000`,
- engineering tasks are clear enough.

Cons:

- project is Elixir/Phoenix,
- local machine does not have `mix`,
- many issues already have PRs/attempts,
- repo last pushed on 2025-12-15, so payout/activity must be confirmed first.

Best Spectral issue if sponsor confirms:

- Telegram Analytics and Monitoring ($1,200): https://github.com/Spectral-Finance/lux/issues/67
- Smart Contract Event Monitoring System ($1,500): https://github.com/Spectral-Finance/lux/issues/75

But both already have multiple attempts. Do not code before confirmation.

### GitHub/Hedera EPS

Skip.

The issue looked good, but comments show Claude already implemented it.

### Rustchain RTC bounties

Skip for first cash target.

Payouts are often RTC and low USD value. Some tasks are social/proof tasks. Not enough money signal.

## Immediate action for the human

Post this on Spectral issue #67:

```text
Hi @rparcus, is the Telegram Analytics and Monitoring bounty still open for a new implementation, and is the $1,200 payout still active?

Before spending build time, I want to confirm:
1. whether you are still accepting new PRs for this issue,
2. whether assignment is required,
3. what would make a submission preferable to the existing attempts,
4. payout currency/process if accepted.

If yes, I can submit a narrow PR with tests and docs rather than a broad rewrite.
```

Post this on Spectral issue #75:

```text
Hi @rparcus, is the Smart Contract Event Monitoring System bounty still active for new submissions?

I see several prior attempts, so I want to avoid duplicating work. If you are still accepting PRs, what is the highest-priority missing piece: event subscription core, ABI decoding, persistence/replay, webhook delivery, or docs/tests?

Please also confirm whether the $1,500 payout is still available and whether assignment is required.
```

If either sponsor replies "yes", we install/use Elixir toolchain or devcontainer, then build the narrowest accepted PR.

## What Codex should do next

Run the radar daily or before each work session:

```bash
python3 bounty_radar.py --limit 20 --out radar-report.md
```

Then inspect only:

- payout in real currency,
- fewer than 10-15 comments,
- not already solved,
- buildable stack,
- clear acceptance criteria.

## Better medium-term asset

Build and publish a small `web3-bounty-radar` repo:

- GitHub issue scanner,
- Superteam agent-listing scanner,
- stale/dead-listing filter,
- scoring,
- Telegram digest.

This can become:

- our own tool for finding money,
- proof-of-work,
- a grant pitch for Solana/Base/Circle-style funding.
