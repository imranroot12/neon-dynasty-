# Official SDK provenance — Build 63

Build 63 uses the public `engineio/math-sdk` and `engineio/web-sdk` repositories.
The CI job records the exact checked-out commit automatically in the workflow logs.
Do not claim production certification from this archive alone: the official optimizer and Web SDK build must execute successfully in CI.

The current public Math SDK requires Python >= 3.12 and Rust/Cargo when its optimizer is used. The current public Web SDK documents Node 22.16.0 and pnpm 10.5.0 and emits a SvelteKit production output for built games.
