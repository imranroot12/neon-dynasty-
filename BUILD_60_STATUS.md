# Neon Dynasty — Build 60

Build 60 is a hardening pass on Build 59. It does not claim Stake approval or production certification.

## Changes
- Hardened CI setup ordering around pnpm/Node.
- Corrected the presentation adapter so `bonusComplete` remains a Neon book event instead of being incorrectly converted to `freeSpinEnd`.
- Added a focused compressed-book math integrity QA script.
- Corrected cap QA to account for Engine publication `payoutMultiplier` being serialized in hundredths.
- Added the same normalized max-win check to the production release gate.
- Retained the official optimizer and 100k-per-mode production gate.

## Current local evidence
- Base book: 100,000 rows.
- Basic/Super/Mystery books: 10,000 rows each.
- Local compressed-book QA: PASS on the current candidate books.
- Current 10k Mystery selection sample is approximately 70.36% Basic / 23.32% Super / 6.32% Hidden, consistent with the locked 70/24/6 design at this sample size.
- Local official optimizer: blocked by missing Cargo/Rust.
- Local Web SDK production build: blocked by unavailable npm/GitHub network access.

## Important
The current candidate books are still development candidates. The 96.0% RTP target is not certified until the official production optimizer and verification pipeline completes with 100k+ production outcomes per mode.
