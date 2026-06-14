# Web3 bounty/grant scan - 2026-06-14

## What was checked

- Superteam Earn public listings.
- Superteam Earn official agent API.
- GitHub open issues with `bounty` + `web3`.
- Always-on grant programs: Solana Foundation, Solana Mobile, Base, Circle, Ethereum ESP.

## Superteam Earn status

An agent profile was created successfully for Superteam Earn:

- Agent name: `codex-grants-builder`
- Agent username: `codex-grants-builder-hot-21`

The agent API returned several `AGENT_ALLOWED` / `AGENT_ONLY` listings, but the useful developer listings were mostly past deadline or already in review as of 2026-06-14.

Examples checked:

- Jupiter `Not Your Regular Bounty`: good technical fit, but deadline was 2026-05-12.
- OOBE x Ace Data Cloud autonomous agent bounty: good technical fit, but deadline was 2026-06-03 and listing is in review.
- BENTO beta bounty: relevant agent/security feedback task, but already effectively closed based on fresh reports.

Conclusion: do not spend build time on these unless a sponsor explicitly confirms late submissions are accepted.

## GitHub bounty candidates

### Best engineering candidates

1. Spectral Finance Lux - Smart Contract Event Monitoring System
   - URL: https://github.com/Spectral-Finance/lux/issues/75
   - Listed budget: $1,500
   - Why it fits: backend/data monitoring, event indexing, alerting, docs/tests.
   - Risk: need inspect repo quality and bounty legitimacy before coding.

2. Spectral Finance Lux - Web3 Authentication and Authorization Framework
   - URL: https://github.com/Spectral-Finance/lux/issues/77
   - Listed budget: $1,000
   - Why it fits: SIWE, sessions, RBAC, docs/tests.
   - Risk: wider scope than it looks; likely needs staged implementation.

3. Spectral Finance Lux - NFT Marketplace Data Aggregation
   - URL: https://github.com/Spectral-Finance/lux/issues/87
   - Listed budget: $750
   - Why it fits: API integration, indexing, analytics.
   - Risk: need confirm target chains/marketplaces.

4. Midnight contributor hub - Unshielded Token dApp tutorial with UI
   - URL: https://github.com/midnightntwrk/contributor-hub/issues/328
   - Listed range: bounty, high priority
   - Why it fits: working repo + tutorial.
   - Risk: content is checked for AI generation; must be genuinely tested and written from verified build notes.

5. Rustchain bounties - Bounty Verification Bot
   - URL: https://github.com/Scottcjn/rustchain-bounties/issues/747
   - Listed reward: 50-75 RTC
   - Why it fits: GitHub Action bot, API checks, deterministic deliverable.
   - Risk: payout is not USDC/cash; ecosystem looks experimental.

### Avoid for now

- Star/follow/social bounties: low value and poor signal.
- Large security/bridge/wallet infrastructure bounties unless sponsor confirms scope and payout first.
- Superteam content contests with hundreds of submissions and already-in-review status.

## Best next move

Start with a small, reviewable engineering bounty:

1. Inspect `Spectral-Finance/lux`.
2. Verify it builds locally.
3. Pick the narrowest issue with clear tests.
4. Ask/confirm in the issue if bounty is still active and whether partial PRs are accepted.
5. Implement a scoped PR.

### Spectral Lux repo check

The repo was cloned into `spectral-lux`.

Findings:

- Real codebase, not just a placeholder.
- Stack: Elixir/Phoenix, plus Node assets.
- Required local versions from `.tool-versions`:
  - Elixir `1.18.1-otp-27`
  - Erlang `27.2`
  - Node.js `22.13.0`
  - Python `3.12.3`
- Local blocker: `mix` is not installed on this machine, so the project cannot be built/tested immediately without installing the Elixir/Erlang toolchain or using the repo's devcontainer/Codespaces setup.

Recommendation: treat Spectral as a medium-effort candidate, not the fastest first submission.

Parallel grant path:

Build a small open-source "Web3 bounty/grant radar" tool:

- pulls Superteam/GitHub opportunities,
- filters stale or in-review listings,
- scores by fit, payout, deadline, and competition,
- exports a Telegram digest or markdown report.

This is useful as proof-of-work for Solana/Base/Circle-style grant applications and helps find the next paid task faster.
