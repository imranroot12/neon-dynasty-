# Neon Dynasty — Build 71 Final Execution

Build 71 moves the project from static integration hardening to **fresh publication
verification**.

## Official execution sequence

1. Run the official Math SDK against Neon Dynasty.
2. Generate fresh books, lookup tables, and index under `library/publish_files/`.
3. Run the official optimizer when configured.
4. Run the publication verifier:
   `python tools/verify_publication.py <publication_dir>`
5. Require at least 100,000 published outcomes in each supported mode:
   BASE, BASIC, SUPER, MYSTERY.
6. Run the official Web SDK production build.
7. Upload the resulting frontend to a Stake Engine staging game.
8. Start a real staging session and verify authentication.
9. Verify at least one play and event sequence in each mode.
10. Verify replay and active-round resume.
11. Capture final artifact hashes and retain the actual logs.

## Hard rule

Static checks do not equal certification. A production status may only be changed
after the real official SDK and staging/RGS execution succeeds.

## Why the book/LUT gate exists

The official Math SDK documentation states that the publication set includes books,
lookup tables and an index, and that a book's `payoutMultiplier` corresponds to the
lookup-table payout for that simulation. The same documentation recommends 100k+
simulations per mode for production-ready games.
