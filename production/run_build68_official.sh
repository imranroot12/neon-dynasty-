#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MATH_SDK="${ENGINE_MATH_SDK:-$ROOT/../../math-sdk-main}"
WEB_SDK="${ENGINE_WEB_SDK:-$ROOT/../../web-sdk-main}"
export ENGINE_MATH_SDK="$MATH_SDK" ENGINE_WEB_SDK="$WEB_SDK"
command -v python3 >/dev/null || { echo 'FAIL: python3 missing'; exit 2; }
command -v cargo >/dev/null || { echo 'FAIL: Cargo/Rust missing'; exit 2; }
command -v zstd >/dev/null || { echo 'FAIL: zstd missing'; exit 2; }
command -v pnpm >/dev/null || { echo 'FAIL: pnpm missing'; exit 2; }
[ -d "$MATH_SDK" ] || { echo "FAIL: official Math SDK missing: $MATH_SDK"; exit 2; }
[ -d "$WEB_SDK" ] || { echo "FAIL: official Web SDK missing: $WEB_SDK"; exit 2; }
STARTED="$(python3 -c 'import time; print(time.time())')"
export NEON_OFFICIAL_RUN_STARTED_AT="$STARTED"
rm -rf "$MATH_SDK/games/neon_dynasty"
cp -a "$ROOT/math/neon_dynasty" "$MATH_SDK/games/neon_dynasty"
cd "$MATH_SDK"
python3 -m pip install -r requirements.txt
python3 games/neon_dynasty/run.py
cd "$WEB_SDK"
pnpm install --frozen-lockfile
pnpm run build --filter=neon-dynasty
cd "$ROOT"
NEON_MATH_GAME="$MATH_SDK/games/neon_dynasty" NEON_WEB_GAME="$WEB_SDK/apps/neon-dynasty" \
  python3 production/finalize_official_build68.py
