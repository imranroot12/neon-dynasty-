#!/usr/bin/env bash
set -euo pipefail
# Network-enabled developer/CI helper. It uses the public official repositories.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MATH_DEST="${ENGINE_MATH_SDK:-$ROOT/../../math-sdk-main}"
WEB_DEST="${ENGINE_WEB_SDK:-$ROOT/../../web-sdk-main}"

if ! command -v git >/dev/null; then echo 'FAIL: git missing'; exit 2; fi
if [ ! -d "$MATH_DEST/.git" ]; then
  git clone https://github.com/engineio/math-sdk.git "$MATH_DEST"
else
  git -C "$MATH_DEST" fetch --prune origin
  git -C "$MATH_DEST" checkout main
  git -C "$MATH_DEST" pull --ff-only origin main
fi
if [ ! -d "$WEB_DEST/.git" ]; then
  git clone https://github.com/engineio/web-sdk.git "$WEB_DEST"
else
  git -C "$WEB_DEST" fetch --prune origin
  git -C "$WEB_DEST" checkout main
  git -C "$WEB_DEST" pull --ff-only origin main
fi

echo "MATH_SDK=$MATH_DEST"
echo "WEB_SDK=$WEB_DEST"
git -C "$MATH_DEST" rev-parse HEAD
git -C "$WEB_DEST" rev-parse HEAD
