# Neon Dynasty — Build 61

Build 61 continues directly from Build 60.

## Changes
- Added a streaming publication-book math contract audit so QA remains memory-bounded as books scale to 100k+ rows.
- Added a dedicated Build 61 release gate that explicitly records candidate vs production-certified status.
- Added SHA-256 file manifest for reproducibility/integrity tracking.
- Removed Python bytecode caches from the release artifact.
- Preserved the official optimizer/100k-per-mode requirement; no synthetic rows were added and no production certification is claimed.

## Current status
The Build 60 candidate books remain unchanged. The next real production milestone is to run the official engineio/math-sdk optimizer with Rust/Cargo and generate/verify 100k+ outcomes for every mode, then build the Web SDK production artifact.
