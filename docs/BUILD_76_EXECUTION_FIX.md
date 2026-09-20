# Build 76 — Official SDK Handoff Correction

Build 75 had the game source in the expected project locations, but the CI workflow was invoking the Math SDK from the wrong path and was not copying the frontend into the official Web SDK workspace before building.

Build 76 corrects that execution path:

1. Validate the real source layout before any SDK work.
2. Copy `math/neon_dynasty` into the official Math SDK `games/` workspace.
3. Run the game's `run.py` from inside the official Math SDK checkout.
4. Verify the fresh `library/publish_files` produced by that execution.
5. Copy `web/neon-dynasty` into the official Web SDK `apps/` workspace.
6. Install the official workspace dependencies and build the game through the official workspace.
7. Preserve exact upstream commit hashes and execution evidence.

This build does **not** claim that official Math execution, Rust optimization, Web SDK compilation, or RGS staging has already succeeded. Those remain CI/Engine-environment gates.
