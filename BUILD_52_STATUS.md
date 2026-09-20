# Neon Dynasty — Build 52

## Focus
Production pipeline hardening and blocker elimination.

## Added
- A system-zstd compatibility module for restricted environments where PyPI cannot be reached. It is explicitly marked as a build-environment fallback, not an official replacement for the Python `zstandard` package.
- `production/run_sdk_with_system_zstd.sh` to run SDK commands with the compatibility module.
- Replaced the old smoke-only `math/neon_dynasty/run.py` with an official-SDK-shaped production entrypoint that requests 100k books for each locked mode and invokes the official optimizer/analysis/RGS verification modules.
- The production entrypoint now hard-fails when Cargo/Rust is unavailable instead of pretending optimization succeeded.
- Independent high-volume RTP audit tool that executes the actual Neon Dynasty GameState without presentation-event serialization. It is explicitly non-publication math analysis.
- Original Neon Dynasty UI/audio development assets and an asset-audit report.

## Current verified environment
- Python: available
- system zstd: available
- Node 22.16.0: available
- pnpm: unavailable in this execution environment
- Cargo/Rust: unavailable in this execution environment
- PyPI network: unavailable

## Production status
NOT YET SUBMISSION-READY. The official optimizer cannot execute here until Cargo/Rust is present. Bonus publication books also require the official 100k-per-mode production pipeline, not the independent fast audit.
