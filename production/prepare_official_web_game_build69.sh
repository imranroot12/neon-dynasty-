#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WEB_SDK="${ENGINE_WEB_SDK:-$ROOT/../../web-sdk-main}"
APP_SRC="$ROOT/web/neon-dynasty"
APP_DST="$WEB_SDK/apps/neon-dynasty"

[ -d "$WEB_SDK/apps" ] || { echo "FAIL: official Web SDK apps directory missing: $WEB_SDK/apps"; exit 2; }
[ -f "$APP_SRC/package.json" ] || { echo "FAIL: Neon Dynasty web app package.json missing"; exit 2; }
[ -f "$APP_SRC/src/routes/+page.svelte" ] || { echo "FAIL: Neon Dynasty route missing"; exit 2; }

rm -rf "$APP_DST"
mkdir -p "$APP_DST"
cp -a "$APP_SRC/." "$APP_DST/"

# The official SDK is the source of shared packages and its workspace lockfile.
# This step deliberately does not mutate the SDK's root configuration.
for required in \
  "$WEB_SDK/packages/components-shared" \
  "$WEB_SDK/packages/components-pixi" \
  "$WEB_SDK/packages/utils-book" \
  "$WEB_SDK/packages/rgs-requests"; do
  [ -e "$required" ] || { echo "FAIL: expected official Web SDK package missing: $required"; exit 2; }
done

echo "Prepared Neon Dynasty at: $APP_DST"
