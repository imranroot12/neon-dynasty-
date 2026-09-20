# Neon Dynasty — Build 48 status

## What was actually completed
- Neon Dynasty Math SDK game runs through the supplied Stake Engine Math SDK codebase.
- System `zstd` compatibility layer was added because the execution environment could not install the pinned PyPI `zstandard` wheel. The SDK's compression/decompression path was exercised successfully.
- Static publication files generated for base/basic/super/mystery.
- `index.json` generated with the four RGS modes.
- Lookup weights tuned to approximately 96.0% RTP on the generated book sets.
- Payout multipliers in books and lookup tables were cross-checked; all checked entries match.
- RGS format verification passed. The SDK reported a volatility-limit warning for Mystery; this is documented rather than hidden.
- Final payout multipliers were quantized to Engine's required 0.1x increment.
- Dragon Meter / Dragon Event book events are present as math events; current Dragon events are presentation/state markers and do not secretly change the payout math.
- Original Neon Dynasty SVG symbol assets are present in the Web app overlay.

## Current generated book sizes
- Base: 100,000 outcomes
- Basic: 10,000 outcomes
- Super: 10,000 outcomes
- Mystery: 10,000 outcomes

Stake's documentation recommends 100k+ simulations per mode for production work. Therefore this is a much stronger math candidate, but the three bonus modes still need 100k+ production simulation sets before calling the math production-certified.

## Current weighted RTP checks
- Base: approximately 96.00002%
- Basic: approximately 96.00000%
- Super: approximately 96.00000%
- Mystery: approximately 96.00000%

These are lookup-weight results on the generated books, not an independent certification.

## Observed maximums
- Base: 314.76x
- Basic: 3,155.29x
- Super: 8,689.01x
- Mystery: 20,000x

## Still required before Stake submission
1. 100k+ production outcomes for Basic, Super and Mystery.
2. Run the official Rust/Cargo optimizer when a Rust toolchain is available, or replace the current development weighting pass with the official optimizer output.
3. Complete the Web SDK production build with the actual installed dependencies.
4. Replace every remaining sample-game Spine/audio asset. Stake explicitly requires unique visual/audio assets and does not approve sample-game assets.
5. Connect and test the live RGS session, bet, bonus-buy, ANTE parameter and replay flows against a real Stake Engine game session.
6. Final mobile/mini-player/approval QA.

Do not upload/publish this package as final until those gates are cleared.
