#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SDK="${ENGINE_MATH_SDK:-$ROOT/../../math-sdk-main}"
if [ ! -f "$SDK/Makefile" ]; then echo "ENGINE_MATH_SDK must point to the official engineio/math-sdk checkout"; exit 2; fi
command -v cargo >/dev/null || { echo "Cargo is required for the official optimizer"; exit 2; }
command -v python3 >/dev/null || exit 2
command -v zstd >/dev/null || { echo "zstd CLI is required by the local book exporter"; exit 2; }
cd "$SDK"
PYTHONPATH=. python3 -m pip install -r requirements.txt
make run GAME=neon_dynasty
