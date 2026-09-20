# Neon Dynasty Build 69

**Status:** execution-ready production candidate; not production-certified.

Build 69 fixes the last-mile Web SDK handoff from Build 68. The official Web SDK
build now receives the actual `web/neon-dynasty` application under
`apps/neon-dynasty` before `pnpm run build --filter=neon-dynasty`, matching the
official SDK workspace layout instead of assuming the app already exists there.

It also adds a fail-closed finalizer with:
- official SDK commit provenance;
- required Base/Basic/Super/Mystery publication books;
- >=100,000 rows for uncompressed books when available;
- publication `index.json`;
- official Web SDK production output;
- explicit staging/RGS checks;
- `production_certified: false` until real staging evidence exists.

No official optimizer or Stake Engine staging result is fabricated in this build.
