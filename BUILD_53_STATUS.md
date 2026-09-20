# Neon Dynasty — Build 53

Build 53 converts the remaining production environment blocker into a reproducible CI release gate.

## Added
- `production/release_gate.py`: hard release gate for Python, Node, pnpm, Cargo, zstd, publication books and sample-asset quarantine.
- `production/build_release.sh`: runs the official Math SDK and Web SDK production pipeline when the required toolchains are available.
- `.github/workflows/neon-dynasty-release.yml`: CI workflow that installs Rust/Cargo, pnpm 10.5, Node 22.16, zstd, checks out the official Engine Math/Web SDK repositories, applies Neon Dynasty, and runs the release gate.
- Sample-asset quarantine: known sample-game asset families now block release rather than being silently carried into a submission package.

## Current local environment
- Python 3.13: available
- Node 22.16: available
- zstd: available
- Cargo/Rust: unavailable locally
- pnpm: unavailable locally because the registry is unreachable

Therefore Build 53 does **not** claim a successful production release build locally. The CI workflow is the intended path for the official Cargo optimizer and full Web SDK dependency installation.

## Official resources
- https://github.com/engineio
- https://github.com/engineio/math-sdk
- https://github.com/engineio/web-sdk
- https://stake-engine.com/docs
