# Neon Dynasty production math run

This is the real production gate. Run this from a clean checkout of the official
Engine Math SDK with Python >=3.12, the `zstandard` package, and Rust/Cargo.
The official SDK documents `make setup`, `make run GAME=<game>`, and Cargo for
its optimizer.

1. Copy `games/neon_dynasty` into the SDK `games/` directory.
2. Install the official dependencies with `make setup`.
3. Set production simulation counts to **>=100,000 per mode**.
4. Enable simulation, optimization, and analysis.
5. Run `make run GAME=neon_dynasty`.
6. Run `verify_publication_integrity.py` against the resulting publish files.
7. Do not publish if any LUT payout is absent from the book, any payout exceeds
   20,000x, or any mode's optimized RTP is outside the approved tolerance.

Do not substitute the local zstd compatibility shim for the official Python
`zstandard` dependency in a final production run.
