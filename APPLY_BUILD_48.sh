#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
WEB_SDK_ROOT="${1:-../web-sdk}"
mkdir -p "$WEB_SDK_ROOT/apps/neon-dynasty"
rm -rf "$WEB_SDK_ROOT/apps/neon-dynasty"/*
cp -a "$ROOT/web/neon-dynasty/." "$WEB_SDK_ROOT/apps/neon-dynasty/"
echo "Neon Dynasty Web SDK app copied to $WEB_SDK_ROOT/apps/neon-dynasty"
echo "Run the current Web SDK install/build commands from the Web SDK README before launch."
