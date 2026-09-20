# Neon Dynasty — Build 63

Build 63 fixes the production-pipeline handoff introduced in Build 62.

## Changes
- Release gate now reads the **actual vendor Math/Web SDK output trees** used by CI instead of accidentally checking the stale source tree.
- Requires 100,000+ rows in every publication mode.
- Requires optimizer/verification evidence and the Web SDK production output.
- Updated the official pipeline and GitHub Actions workflow to use the Build 63 gate.
- Added SDK provenance documentation.

## Honest status
The official optimizer still cannot be executed in this offline assembly environment. Build 63 therefore remains a production candidate, not a certified release.
