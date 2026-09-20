#!/usr/bin/env bash
set -euo pipefail

# Build 63: execute against the official Engine SDKs. This script deliberately
# fails closed when the official optimizer toolchain is unavailable.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MATH_SDK="${ENGINE_MATH_SDK:-$ROOT/../../math-sdk-main}"
WEB_SDK="${ENGINE_WEB_SDK:-$ROOT/../../web-sdk-main}"

command -v python3 >/dev/null || { echo 'FAIL: python3 missing'; exit 2; }
command -v cargo >/dev/null || { echo 'FAIL: Cargo/Rust missing — official optimizer cannot run'; exit 2; }
command -v zstd >/dev/null || { echo 'FAIL: zstd missing'; exit 2; }
command -v pnpm >/dev/null || { echo 'FAIL: pnpm missing'; exit 2; }
[ -d "$MATH_SDK" ] || { echo "FAIL: official math SDK not found: $MATH_SDK"; exit 2; }
[ -d "$WEB_SDK" ] || { echo "FAIL: official web SDK not found: $WEB_SDK"; exit 2; }

rm -rf "$MATH_SDK/games/neon_dynasty"
cp -a "$ROOT/math/neon_dynasty" "$MATH_SDK/games/neon_dynasty"

cd "$MATH_SDK"
python3 -m pip install -r requirements.txt
python3 games/neon_dynasty/run.py

cd "$WEB_SDK"
pnpm install --frozen-lockfile
pnpm --filter neon-dynasty build

cd "$ROOT"
NEON_MATH_GAME="$MATH_SDK/games/neon_dynasty" NEON_WEB_GAME="$WEB_SDK/apps/neon-dynasty" python3 production/release_gate_build63.py || {
  echo 'FAIL: release gate did not pass; see RELEASE_GATE_BUILD_63.json'
  exit 3
}

echo 'BUILD_63_OFFICIAL_PIPELINE_COMPLETE'
