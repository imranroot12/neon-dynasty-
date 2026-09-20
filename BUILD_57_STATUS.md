# Build 57 — Production Pipeline Hardening

## Completed
- Added missing `game_optimization.py` required by the official Math SDK run path.
- Replaced the placeholder production `run.py` with the official SDK orchestration pattern.
- Production math target is now 100,000 outcomes for each of base/basic/super/mystery before optimization.
- Added candidate-only 100k runner for diversity testing without falsely calling it optimized.
- Fixed the GitHub Actions workflow's invalid nested checkout command.
- CI now checks out current `engineio/math-sdk` and `engineio/web-sdk` and applies Neon Dynasty.
- Release gate now validates the actual official SDK workspace, 100k rows per mode, and a real Web SDK build artifact.
- Added explicit production-run instructions.

## Current local environment
- Node 22.16.0: available
- npm: available
- Python 3.13.5: available
- zstd: available
- pnpm: unavailable because registry access is blocked
- Cargo/Rust: unavailable in this execution environment

Therefore the official optimizer and Web SDK dependency build are intentionally delegated to the reproducible CI workflow and are not represented as locally completed.

## Executed evidence in this environment
- Official Math SDK `create_books()` successfully ran across all four modes at 1,000 outcomes/mode after fixing the local zstd compatibility layer (`compress()`/`decompress()` support).
- A 100,000-outcome official SDK candidate book was successfully generated for **Base** and verified as exactly 100,000 JSONL rows with the system `zstd` CLI.
- The attempt to generate 100,000 outcomes for all four modes exceeded the execution-time limit; the three bonus modes therefore remain below the production diversity gate here.
- The official optimizer was not run locally because Cargo/Rust is absent. The CI workflow is configured to install Rust and execute the official optimizer.
- The Web SDK production build was not run locally because pnpm cannot be fetched from the npm registry in this environment.
- A sound-registry hardening pass renamed inherited/sample-style sound identifiers to `nd_*` identifiers throughout the Neon Dynasty source and audio registry.
- Fixed stale `SUPERSPIN` frontend vocabulary to the actual `super` math/RGS mode.
