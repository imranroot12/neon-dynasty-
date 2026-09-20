#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SDK_ROOT="${SDK_ROOT:-$ROOT/../../math-sdk-main}"
GAME_DIR="$ROOT/math/neon_dynasty"
if [[ ! -d "$SDK_ROOT/src" ]]; then echo "Missing SDK source: $SDK_ROOT" >&2; exit 2; fi
export PYTHONPATH="$ROOT/production:$SDK_ROOT:$GAME_DIR${PYTHONPATH:+:$PYTHONPATH}"
exec python3 "$SDK_ROOT/run.py" "$@"
