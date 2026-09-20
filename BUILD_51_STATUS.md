# Neon Dynasty — Build 51

## Focus
Build 51 is the reproducibility/production-environment pass. It does not fabricate an official optimizer result in an environment without Cargo or npm access.

### Added
- Reproducible production environment instructions.
- Dockerfile with Rust/Cargo, Python, Node and pnpm.
- Math dependency manifest.
- Production check launcher.
- GitHub Actions workflow that checks the Neon Dynasty math against the current public Engine Math SDK and builds the Neon Dynasty Web SDK app using Node 22.16.0 / pnpm 10.5.0.
- Preserved the independent book/LUT integrity gate.

### Upstream facts verified 2026-09-20
- Engine Math SDK: Python >=3.12; Cargo required for the included optimizer.
- Engine Web SDK: Svelte 5 + PixiJS 8 + TurboRepo; Node 22.16.0 and pnpm 10.5.0 in its current README.

### Status
This remains a candidate package until the official optimizer, full 100k+ bonus-mode books, Web SDK production build, and real Stake RGS staging test have all passed.
