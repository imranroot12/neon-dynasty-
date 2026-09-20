# Neon Dynasty — Build 65

## Completed in this build
- Corrected the Build 64 asset audit false-positive: `reelhouse.svg` is a real Neon Dynasty animation asset and is referenced by `src/game/assets.ts`.
- Asset/UI/audio audit now passes: 61 packaged assets, 5 audio files, no missing explicit asset references, and all major game-feature hooks detected.
- Added `qa/build65_math_integrity.py` to verify publication-book ↔ lookup-table ID and payout consistency before optimizer certification.
- Added `production/run_build65_official.sh`, a fail-closed runner for the official Engine Math SDK pipeline.

## Math result
The current packaged books are still:
- base: 100,000
- basic: 10,000
- super: 10,000
- mystery: 10,000

Build 65 does **not** duplicate rows to pretend that the bonus modes have 100k simulations. The official optimizer remains uncertified until it is actually executed in the official SDK environment.

## Official production requirement
Stake's Math SDK requires Python >=3.12 and Rust/Cargo when its optimization algorithm is used. The official quick-start says the publication files are generated under `library/publish_files/`. The current official repository also has an open issue concerning optimizer-generated payout values and book/LUT integrity, so Build 65 explicitly performs a book↔LUT integrity check before any production claim.

## Next gate
Run `production/run_build65_official.sh` in a network-enabled environment containing the official Math SDK and Cargo. It must generate and verify 100k+ outcomes for every required mode, run the official optimizer/analysis, and then pass the SDK's RGS verification suite.
