# Build 79 — Launch Execution Runbook

Build 79 freezes the project-side work and makes the remaining gates explicit.

## Official execution

Run the repository workflow:

`.github/workflows/neon-dynasty-official-execution.yml`

The workflow must:
1. check out the official Math SDK and Web SDK;
2. record exact revisions;
3. execute Neon Dynasty through the Math SDK;
4. generate compressed publication books and lookup tables;
5. run the official optimizer;
6. verify IDs and exact payoutMultiplier ↔ lookup-table matches;
7. build the frontend through the official Web SDK;
8. retain publication and frontend artifacts.

## Engine publication requirements

The publication directory must contain the Engine-required `index.json`,
lookup CSV files, and `.jsonl.zst` game logic. Every simulation must carry
`id`, `events`, and `payoutMultiplier`, and the CSV payout must exactly match
the corresponding game-logic payout.

## What this build does NOT claim

This package does not claim that the official SDK, optimizer, or RGS staging
has already run. Those are external execution gates and must be evidenced by
the CI artifacts.

## Final external gate

After successful CI execution, upload the generated Math and FrontEnd files
to the user's own Engine account, launch a staging session, and test base,
bonus, mystery, free-spin, wild/multiplier, replay/resume, balance and error
paths before submission.
