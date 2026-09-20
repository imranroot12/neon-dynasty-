# Neon Dynasty development simulation

A 500-spin-per-mode smoke run was executed against the supplied Stake Engine
Math SDK codebase with a development-only import shim because this environment
cannot install the pinned `zstandard` dependency.

These numbers are **not production RTP certification** and no optimizer was run.
Stake's documentation recommends 100k+ simulations per mode for production work
and uses optimized lookup-table weights for publication.
