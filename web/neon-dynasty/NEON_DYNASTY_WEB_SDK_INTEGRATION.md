# Neon Dynasty — Web SDK integration overlay

Built from Stake Engine's supplied `apps/cluster` Web SDK reference.

## Locked game contract
- 6x5 cluster/tumble
- Target RTP 96.0%
- Target max win 20,000x
- Basic Bonus: 8 FS / 100x
- Super Bonus: 10 FS / 200x
- Hidden Bonus: 15 FS / Mystery Buy only
- Mystery Buy: 500x; vault weights 70/24/6
- ANTE: 3x cost / 5x trigger setting

## Integration
`neonDynastyBookEvents.ts` defines the RGS event contract and `neonDynastyAdapter.ts` maps Neon Dynasty-specific events into the supplied cluster Web SDK handler vocabulary. The adapter performs no RNG or payout calculation.

## Important
Sample Web SDK artwork/audio must not be shipped. Stake approval requires unique visual/audio assets and CDN-loaded assets. Replace the sample asset map with Voltix/Neon Dynasty originals before publication.
