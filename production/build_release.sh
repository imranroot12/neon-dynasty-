#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENGINE_MATH_SDK="${ENGINE_MATH_SDK:-$ROOT/../../math-sdk-main}"
ENGINE_WEB_SDK="${ENGINE_WEB_SDK:-$ROOT/../../web-sdk-main}"
: "${ENGINE_MATH_SDK:?ENGINE_MATH_SDK must point to an official engineio/math-sdk checkout}"
: "${ENGINE_WEB_SDK:?ENGINE_WEB_SDK must point to an official engineio/web-sdk checkout}"
command -v cargo >/dev/null || { echo 'FAIL: Cargo/Rust missing'; exit 2; }
command -v pnpm >/dev/null || { echo 'FAIL: pnpm missing'; exit 2; }
command -v python3 >/dev/null || exit 2
command -v zstd >/dev/null || exit 2
cd "$ENGINE_MATH_SDK"
python3 -m pip install -r requirements.txt
make run GAME=neon_dynasty
cd "$ENGINE_WEB_SDK"
pnpm install --frozen-lockfile
pnpm --filter neon-dynasty build
cd "$ROOT"
python3 production/release_gate.py
