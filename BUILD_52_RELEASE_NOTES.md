# Build 52 release notes

Build 52 is a production-hardening build, not an approval claim.

### Real improvements
- The old math entrypoint that only ran a smoke simulation is replaced with an official-SDK-shaped pipeline that requests 100,000 outcomes for each locked mode and invokes the official optimizer, analysis and RGS verification modules when Cargo is present.
- The environment now has a system-zstd compatibility path for restricted build environments. It does not claim to replace the official Python package for a real production deployment.
- Added a high-volume RTP audit tool against the actual Neon Dynasty GameState.
- Added original Neon Dynasty SVG UI assets and original development sound effects.
- Added an automated asset audit that explicitly identifies remaining sample/unverified assets.

### Still blocked
- Cargo/Rust is not installed in this execution environment, so the official optimizer has not been executed here.
- pnpm is not installed here, so the Web SDK production build has not been executed here.
- The current Web app still contains sample cluster assets in its runtime graph; they must be replaced/removed before Stake approval.
- The official 100k-per-mode publication run still needs to be executed in a full Engine SDK environment.
