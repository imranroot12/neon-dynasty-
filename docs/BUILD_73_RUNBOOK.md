# Build 73 — Official Execution Runbook

Build 73 contains the final automated handoff for the real official Engine execution.

## What can be done in this chat environment

- inspect and modify the project
- validate source/configuration
- package reproducible builds
- prepare fail-closed CI
- verify that no certification is claimed without evidence

## What requires the network-enabled Engine environment

The official Math SDK must actually run the Neon Dynasty game simulation and produce
fresh publication files. The official Web SDK must actually build the frontend.
Finally, Stake Engine staging must execute real RGS authentication/play/replay flows.

The workflow `.github/workflows/neon-dynasty-official-execution.yml` is designed for
that network-enabled execution.

## Required final evidence

The release is only eligible for certification when the CI artifact contains:

- exact Math SDK commit
- exact Web SDK commit
- Python version
- Rust/Cargo version when optimizer is used
- fresh publication output
- 100k+ rows in BASE/BASIC/SUPER/MYSTERY
- successful book/LUT verification
- successful Web SDK production build
- real Stake Engine staging evidence

No pre-existing book is accepted as proof of a fresh Math SDK run.
