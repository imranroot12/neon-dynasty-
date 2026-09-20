# Neon Dynasty — Build 68 Official Execution Handoff

Build 68 is the **execution-ready** handoff. It does not claim that the official
Math SDK optimizer, Web SDK build, or Stake Engine staging has run in this chat.

## What changed
- Added `production/run_build68_official.sh` as the single fail-closed official runner.
- Added `production/finalize_official_build68.py` to record the exact Math/Web SDK
  commit hashes used by the execution environment.
- The finalizer requires fresh official output and checks:
  - Base / Basic / Super / Mystery books: 100,000+ rows each.
  - Matching publication lookup tables with 100,000+ numeric rows each.
  - Publication `index.json`.
  - Web SDK production output.
- The handoff manifest always keeps `production_certified: false` until real staging/RGS testing is completed.

## Official environment
The current official repositories document Math SDK Python >=3.12 and Cargo/Rust
for the included optimizer. The current Web SDK documents Node 22.16.0 and pnpm
10.5.0, and uses Svelte 5 + PixiJS 8.

## Execution
From a network-enabled build machine or GitHub Actions runner:

```bash
./production/bootstrap_official_sdks.sh
./production/run_build68_official.sh
```

Or use the Build 68 GitHub Actions workflow, which clones the official SDKs and
records their commit hashes before running the game.

## Staging gate
After the official build passes, start a Stake Engine staging session and verify
authentication, balance, normal spins, Mystery Buy, Free Spins/retriggers, bonus
modes, book-event ordering, wins, and end-round handling. Save the session/build
identifier and logs. Only after those checks should this be treated as ready for
an actual Stake Engine deployment.
