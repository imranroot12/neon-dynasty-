# Build 78 — Official Runtime Alignment

Build 78 removes two remaining execution-path ambiguities:

- The Web SDK CI runtime now follows the current official getting-started documentation: Node 18.18.0 and pnpm 10.5.0.
- The CI job now packages the fresh Math publication directory and the Web SDK `dist` output as execution artifacts, rather than retaining only metadata/evidence.

The Math job continues to require Rust/Cargo and the official optimizer, and the workflow remains fail-closed. No certification is claimed until the workflow completes successfully.
