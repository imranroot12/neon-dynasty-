# Neon Dynasty — Build 49

## Major correction in this build
Build 48 contained an incorrect development weighting formula for buy modes: it treated 96% as `96` rather than `0.96` when converting target RTP to an average payout multiplier. Build 49 corrects this. The correct target average payout is:

- Base: 0.96x
- Basic Buy (100x cost): 96x
- Super Buy (200x cost): 192x
- Mystery Buy (500x cost): 480x

The corrected lookup tables are generated from the supplied Stake Engine Math SDK lookup tables and the weighted RTP is calculated as weighted payout / mode cost.

## Current math status
- Base book: 100,000 outcomes.
- Basic/Super/Mystery books: 10,000 outcomes each in the current verified publication set.
- Corrected weighted RTP checks are included in `math/neon_dynasty/CORRECTED_WEIGHT_REPORT.json`.
- Payout values remain quantized to 0.1x.
- Mystery max-win remains capped at 20,000x in the current candidate set.

## Important production gate
Stake Engine's current quick-start documentation recommends 100k+ outcomes per mode for production work and describes the official optimization process as modifying lookup-table weights. Build 49 therefore fixes the RTP math but does **not** claim that the bonus modes are production-certified yet.

The official Math SDK also requires Rust/Cargo for its optimization algorithm. This environment does not contain Cargo and cannot download packages from PyPI, so the official optimizer has not been falsely represented as run.

## Frontend status
The Web SDK overlay, Neon event contract, RGS bet contract, replay contract, original SVG symbol set, menu and bonus-buy UI from Build 48 are retained.

## Next real gates
1. Generate 100k+ bonus outcomes per mode on a machine with the official SDK environment.
2. Run the official Rust/Cargo optimizer and analysis/PAR sheet.
3. Complete the full Web SDK dependency install/build.
4. Replace remaining sample Spine/audio assets.
5. Test the live RGS session, bonus buys, ANTE, replay and mobile/mini-player flows.
