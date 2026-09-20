# Neon Dynasty — Build 58 status

## Improvements in this build
- Hardened the release gate so local builds use `math/neon_dynasty` and `web/neon-dynasty`, while CI uses `ENGINE_MATH_SDK` / `ENGINE_WEB_SDK` official checkout paths.
- Removed false-positive sample-asset quarantine matching for the generic `tumble_win` filename; retained known sample identifiers such as `sample_provider`, `sample_lines`, `transition.atlas`, etc.
- Added Storybook event stories for the Neon-specific bonus events: `bonusStart`, `mysteryReveal`, `dragonMeter`, `dragonEvent`, and `bonusComplete`.
- Fixed duplicated `nd_nd_*` sound identifiers to canonical `nd_*` identifiers and validated `sounds.json` as JSON.
- Made the Menu controls functional: music mute, sound-effects mute, and Turbo Spins now affect the game state/audio layer.
- Expanded Rules & Paytable UI with the complete 5–30 cluster payout table and special-value disclosures.
- Synchronized the frontend symbol paytables with the Neon Dynasty math paytable values.

## Verified locally
- Python source compilation: PASS.
- Audio JSON validation: PASS.
- No known sample-provider/sample-game identifiers in Neon source tree: PASS.
- Local release gate now correctly detects the publication books.
- Base publication book: 100,000 rows.
- Basic/Super/Mystery publication books: 10,000 rows each in the current local candidate package.

## Remaining production blockers
- Official optimizer has not been executed locally because Cargo/Rust is unavailable in the current environment.
- Full Web SDK production build has not been executed locally; the networked dependency installation required by the official Web SDK is not available here.
- Basic/Super/Mystery still need 100,000-row production books before the release gate can pass.
- ANTE remains an explicit RGS integration point: the UI displays the locked 3×/5× setting but refuses to charge it until the deployed RGS exposes a supported ANTE parameter. This avoids inventing a client-side transaction field.
- Stake Engine approval/publish has NOT been performed.

## CI completion path
The repository workflow checks out the current official Engine Math/Web SDK repositories, runs the official math optimizer, builds the Web SDK app, then runs the release gate. Stake Engine requires static compressed outcome files and frontend handling for all book events; Bet Replay is mandatory for new games.
