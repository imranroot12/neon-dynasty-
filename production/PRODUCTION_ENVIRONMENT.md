# Neon Dynasty — reproducible production environment

Stake Engine's current Math SDK requires Python >=3.12; its official optimizer additionally requires Rust/Cargo. The current Web SDK requires Node 22.16.0 and pnpm 10.5.0.

## Math
1. Extract the official Engine Math SDK.
2. Install its `requirements.txt` (including `zstandard`).
3. Put `math/neon_dynasty` under `games/neon_dynasty`.
4. Run `make run GAME=neon_dynasty` for the official SDK pipeline.
5. Run the official optimizer from `optimization_program` with the generated optimization configuration.
6. Run the independent publication-integrity verifier after optimization.

## Web
1. Use Node 22.16.0 and pnpm 10.5.0.
2. Copy the Neon Dynasty app into `apps/neon-dynasty` in the supplied Web SDK checkout.
3. Run `pnpm install`.
4. Run `pnpm run build --filter=neon-dynasty`.
5. Upload the resulting static build to Stake Engine Files and test it through a staging game session.

The package intentionally does not claim Stake approval until the real RGS staging session and approval process succeed.
