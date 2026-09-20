# Neon Dynasty Build 43

## Added
- Official Math SDK-derived `games/neon_dynasty` implementation.
- 6x5 cluster/tumble math configuration.
- RGS buy modes: `base`, `basic` (100x), `super` (200x), `mystery` (500x).
- Hidden Bonus is an outcome of Mystery Buy and is not a standalone mode.
- Basic = 8 spins, Super = 10 spins, Hidden = 15 spins.
- Neon-specific `bonusStart`, `mysteryReveal`, `dragonMeter`, `dragonEvent`, and `bonusComplete` book events.
- Frontend handlers and a Dragon/Mystery feature overlay.
- Symbol rendering no longer depends on the supplied sample symbol Spine art; symbols use an original Neon Dynasty text treatment.
- Local 2,000-spin smoke run per mode, producing `BUILD43_SMOKE_RTP.json`.

## Local smoke result
The current 2,000-spin development sample was:
- Base: 95.917%
- Basic Buy: 95.290%
- Super Buy: 95.962%
- Mystery Buy: 96.144%

These are **development sample estimates, not certified RTP values**. Stake's production math workflow requires substantially larger simulations and the normal optimization/verification pipeline before submission.

## Remaining production gates
1. Run the official SDK optimizer and 100k+ simulations per mode in an environment with the required dependencies/toolchain.
2. Replace remaining sample background/animation/audio assets with original production assets.
3. Complete RGS live-session testing, bet-level handling, replay, mobile/desktop QA, and approval checks.
4. Do not publish until all gates pass.
