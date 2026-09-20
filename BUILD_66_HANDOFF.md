# Build 66 — Production Handoff

This build is the production-execution handoff, not a claim of certification.

Official Stake Engine documentation says the Math SDK generates the backend/configuration files, lookup tables and simulation results, and that publication requires books, lookup tables and an index. The official Web SDK is Svelte 5 + PixiJS 8 + TurboRepo and its documented build creates a static bundle for upload.

## Required real execution
1. Run the official Math SDK against Neon Dynasty.
2. Generate >=100,000 outcomes for Base, Basic, Super and Mystery.
3. Run the official Rust/Cargo optimizer and analysis.
4. Verify book/lookup/index consistency.
5. Build the Web SDK production artifact.
6. Start a real Stake Engine staging session.
7. Test authenticate -> play -> event rendering -> end-round -> balance.
8. Only after those pass, create the release candidate.

No synthetic expansion of the existing 10k bonus books is permitted.
