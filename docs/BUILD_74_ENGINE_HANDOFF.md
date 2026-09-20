# Build 74 — Engine Publication Handoff

The current Engine documentation specifies that published static math consists of an
`index.json`, lookup-table CSVs, and compressed JSON-lines game-logic files. The index
maps each mode to its cost, events file and weights file. The payout multiplier in the
CSV must exactly match the corresponding game-logic payout.

Build 74 adds `tools/engine_publication_preflight.py` to check this structure before
upload. Compressed `.jsonl.zst` event books are intentionally left to the official
Engine/zstd-capable runtime for final cross-checking.

## Final external step

After the official Math SDK creates fresh publication files:

1. Run the Engine publication preflight.
2. Upload the math files to the game's Engine Files page.
3. Publish the Front End after the official Web SDK build.
4. Start a Developer staging game session.
5. Exercise Base/Basic/Super/Mystery and replay/resume.
6. Keep the resulting staging evidence with the exact SDK commit hashes.

This build does not contain or request account credentials.
