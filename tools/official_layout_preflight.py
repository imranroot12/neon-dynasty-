#!/usr/bin/env python3
"""Validate Neon Dynasty's handoff into the official Engine SDK workspaces."""
from pathlib import Path
import json, sys

root = Path(__file__).resolve().parents[1]
required = [
    root / "math/neon_dynasty/run.py",
    root / "math/neon_dynasty/game_config.py",
    root / "math/neon_dynasty/gamestate.py",
    root / "math/neon_dynasty/run.py",
    root / "web/neon-dynasty/package.json",
    root / "web/neon-dynasty/vite.config.js",
]
missing = [str(p.relative_to(root)) for p in required if not p.is_file()]
result = {
    "status": "PASS" if not missing else "FAIL",
    "missing": missing,
    "math_source": "math/neon_dynasty",
    "web_source": "web/neon-dynasty",
    "official_math_destination": ".vendor/math-sdk/games/neon_dynasty",
    "official_web_destination": ".vendor/web-sdk/apps/neon-dynasty",
}
print(json.dumps(result, indent=2))
if missing:
    sys.exit(1)
