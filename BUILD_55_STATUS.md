# Neon Dynasty — Build 55

## Focus: RGS/event contract hardening

Build 55 fixes and verifies the frontend contract layer before the final workspace build.

### Completed
- Fixed duplicate `BookEventCreateBonusSnapshot` union entry.
- Corrected `freeSpinRetrigger` handler typing to use its actual event type.
- Added deterministic RGS/replay/event contract audit under `qa/build55_contract_audit.py`.
- Verified replay endpoint construction against the documented `/bet/replay/{game}/{version}/{mode}/{event}` path.
- Verified RGS bet clamp/step validation helpers remain isolated from client-side payout logic.
- Verified locked 6x5 / 96% / 20,000x configuration metadata.
- Verified Basic 100x, Super 200x and Mystery 500x mode costs in frontend config.
- Verified the Neon runtime asset registry contains no inherited sample asset path.
- Verified required Neon background/logo/Dragon Meter/vault/audio assets exist.

### Production gates still external
- Official Engine Rust/Cargo optimizer must run in an environment with Cargo installed.
- Full Web SDK workspace dependency installation/build must run with the official package-manager environment.
- Production math still requires 100k+ diverse simulations per mode and official optimization/analysis. Stake documents 100k+ per mode as the typical production recommendation.
- Final RGS session/replay behavior must be exercised against the user's deployed Stake Engine game.
