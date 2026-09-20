# Neon Dynasty Build 56

Build 56 is a production-pipeline hardening release.

## Changes
- Corrected the GitHub Actions math workflow to apply the current `math/neon_dynasty` tree instead of an obsolete `build50_final` path.
- Corrected the Web SDK workflow to checkout the official `engineio/web-sdk` repository directly instead of relying on an archived local ZIP.
- Kept Node 22.16.0, pnpm 10.5.0, Python 3.13 and Rust/Cargo setup in CI.
- Corrected the release gate to inspect Neon Dynasty's actual `math/neon_dynasty/library/publish_files` directory.
- Renamed the generated gate report to `RELEASE_GATE_BUILD_56.json`.
- Kept the gate fail-closed when Cargo, pnpm, publication books, or clean assets are missing.

## Current official-engine alignment
The current Engine Math SDK documents Python >=3.12 and Cargo/Rust for its optimizer. The current Web SDK is a separate official repository and the current project has active work around deriving bet modes from RGS.

## Status
This build is **not** claimed Stake-approved. CI is now correctly capable of testing against fresh official Engine repositories rather than stale local copies.
