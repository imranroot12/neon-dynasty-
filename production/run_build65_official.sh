#!/usr/bin/env bash
set -euo pipefail
# Run only inside the official Stake Engine Math SDK environment.
# No synthetic rows or client-side replacement optimizer is permitted.
: "${NEON_GAME_DIR:=games/neon_dynasty}"
cd "$NEON_GAME_DIR"
command -v cargo >/dev/null || { echo 'BLOCKED: Rust/Cargo required'; exit 20; }
command -v python3 >/dev/null || { echo 'BLOCKED: Python required'; exit 21; }
python3 run.py
