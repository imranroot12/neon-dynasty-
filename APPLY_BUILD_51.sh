#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
WEB_SDK="${1:-}"
if [ -z "$WEB_SDK" ]; then echo "Usage: APPLY_BUILD_51.sh /path/to/web-sdk"; exit 2; fi
mkdir -p "$WEB_SDK/apps/neon-dynasty"
cp -a "$ROOT/web/neon-dynasty/." "$WEB_SDK/apps/neon-dynasty/"
echo "Neon Dynasty app copied to $WEB_SDK/apps/neon-dynasty"
echo "Then run: cd $WEB_SDK && pnpm install && pnpm run build --filter=neon-dynasty"
