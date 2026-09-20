# Neon Dynasty Build 57 — production run

This package now follows the current Engine repositories' documented flow.

## Local production environment
- Python >= 3.12
- Node 22.16.0
- pnpm 10.5.0
- Rust/Cargo
- zstd

## Official Math SDK
1. Checkout `engineio/math-sdk`.
2. Copy `math/neon_dynasty` into `games/neon_dynasty`.
3. Install `requirements.txt`.
4. Run `python games/neon_dynasty/run.py`.
5. This generates 100,000 outcomes per mode, runs the official optimizer, writes configs, analysis, and RGS verification.

## Official Web SDK
1. Checkout `engineio/web-sdk`.
2. Copy `web/neon-dynasty` into `apps/neon-dynasty`.
3. `pnpm install --frozen-lockfile`.
4. `pnpm --filter neon-dynasty build`.

The GitHub Actions workflow performs these steps automatically on Ubuntu 24.04.

**No local result is labeled final unless the Cargo optimizer, 100k-per-mode books, Web SDK build, and release gate all pass.**
