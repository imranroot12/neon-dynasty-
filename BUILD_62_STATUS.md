# Neon Dynasty — Build 62

Build 62 is the official-toolchain execution release.

## What changed
- Added `production/bootstrap_official_sdks.sh` to obtain the public official Engine Math/Web SDK repositories in a network-enabled environment.
- Added `production/run_official_pipeline.sh` that fails closed unless Python, Cargo/Rust, zstd, pnpm, and both official SDK checkouts are present.
- Upgraded the GitHub Actions pipeline to run the official Math SDK's simulation + Rust optimizer, copy the resulting publication files back into the game package, build the Web SDK app, run the release gate, and upload artifacts.
- Removed Python cache/bytecode files from the package.

## Important
The local execution environment used to assemble this archive has no Cargo and no outbound GitHub access, so the official optimizer was not falsely claimed to have run here. Build 62 is prepared so a network-enabled CI runner can execute the real production pipeline.

The current Engine Math SDK documentation states that the official engine generates books, lookup tables and index files, and recommends 100k+ simulations per mode for production-ready diversity; optimization uses Rust/Cargo. See the official documentation and repository.
