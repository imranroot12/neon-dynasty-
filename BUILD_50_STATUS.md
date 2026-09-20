# Neon Dynasty — Build 50

## What changed
- Added a strict offline publication-integrity gate.
- Verified every current lookup-table payout is present in its corresponding book.
- Verified all current book/LUT payouts are <= 20,000x using Engine's 100-unit payoutMultiplier encoding.
- Added an explicit production-run procedure using the official Engine Math SDK.
- Added official Engine GitHub/Stake documentation resources.
- Preserved the locked game design: 6x5 cluster/tumble, 96.0% target RTP,
  20,000x cap, Basic/Super/Hidden bonuses, 100x/200x/500x buys, Mystery Buy,
  and ANTE 3x cost / 5x trigger setting.

## Current integrity result
- Base: 100,000 book rows; weighted RTP 96.0000033%; max 3,148.0x.
- Basic: 10,000 book rows; weighted RTP 96.0000000%; max 3,155.3x.
- Super: 10,000 book rows; weighted RTP 96.0000000%; max 8,689.0x.
- Mystery: 10,000 book rows; weighted RTP 96.0000000%; max 20,000.0x.
- All four modes have zero LUT payouts missing from their corresponding books.

## Current production gate
The package remains **candidate / not Stake-approved**.
Base has 100,000 book rows. Basic, Super, and Mystery currently have 10,000
rows and therefore do not yet meet the recommended 100k+ production diversity
threshold. The official Rust/Cargo optimizer has not been run in this
execution environment because Cargo is unavailable.

## Upstream integrity note
The public Engine Math SDK currently has an open issue concerning optimizer
outputs that may synthesize payout values not present in simulations. Neon
Dynasty therefore keeps an independent book-to-LUT payout-integrity gate.
