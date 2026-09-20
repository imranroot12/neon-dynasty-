#!/usr/bin/env python3
"""Fail-closed checks for the upstream Engine SDK interfaces Neon Dynasty uses."""
from pathlib import Path
import json, sys

root = Path(__file__).resolve().parents[1]
math = root / ".vendor" / "math-sdk"
web = root / ".vendor" / "web-sdk"
required_math = [
    "src/state/run_sims.py",
    "src/write_data/write_configs.py",
    "optimization_program/run_script.py",
    "utils/rgs_verification.py",
]
required_web = ["package.json", "pnpm-workspace.yaml"]
missing_math = [p for p in required_math if not (math / p).is_file()]
missing_web = [p for p in required_web if not (web / p).is_file()]
result = {
    "status": "PASS" if not missing_math and not missing_web else "FAIL",
    "math_sdk_head": "unknown",
    "web_sdk_head": "unknown",
    "missing_math": missing_math,
    "missing_web": missing_web,
    "required_math_interfaces": required_math,
    "required_web_interfaces": required_web,
}
print(json.dumps(result, indent=2))
if missing_math or missing_web:
    sys.exit(1)
