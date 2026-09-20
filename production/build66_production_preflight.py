#!/usr/bin/env python3
"""Build 66 production execution preflight.

This script prepares and validates the real official SDK execution contract.
It never fabricates simulations or marks certification passed when the
official optimizer/build did not actually execute.
"""
from pathlib import Path
import json, os, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
MATH=Path(os.environ.get("NEON_MATH_GAME", ROOT/"math/neon_dynasty"))
WEB=Path(os.environ.get("NEON_WEB_GAME", ROOT/"web/neon-dynasty"))
SDK=Path(os.environ.get("ENGINE_MATH_SDK", ROOT/"vendor/math-sdk"))
WSDK=Path(os.environ.get("ENGINE_WEB_SDK", ROOT/"vendor/web-sdk"))

requirements={
    "python_3_12_plus": sys.version_info >= (3,12),
    "cargo": shutil.which("cargo") is not None,
    "zstd": shutil.which("zstd") is not None,
    "node": shutil.which("node") is not None,
    "pnpm": shutil.which("pnpm") is not None,
    "official_math_sdk_present": (SDK/"README.md").is_file(),
    "official_web_sdk_present": (WSDK/"README.md").is_file(),
    "math_game_present": MATH.is_dir(),
    "web_game_present": WEB.is_dir(),
}
report={
    "build":"66",
    "requirements":requirements,
    "ready_to_execute":all(requirements.values()),
    "production_certified":False,
    "required_simulations":{
        "base":100000,
        "basic":100000,
        "super":100000,
        "mystery":100000
    },
    "commands":{
        "math":"make setup && make run GAME=neon_dynasty",
        "web":"pnpm install && pnpm run build --filter=neon-dynasty",
        "rgs":"run a real Stake Engine staging session and test authenticate/play/end-round"
    }
}
(ROOT/"BUILD_66_PRODUCTION_PREFLIGHT.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
sys.exit(0 if report["ready_to_execute"] else 2)
