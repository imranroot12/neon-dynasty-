#!/usr/bin/env python3
import json, sys
from pathlib import Path

p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("release/build75_release_gate.json")
data = json.loads(p.read_text())
for key in (
    "official_math_execution_verified_here",
    "official_optimizer_verified_here",
    "official_web_build_verified_here",
    "stake_engine_rgs_staging_verified_here",
):
    if data.get(key) is True:
        raise SystemExit(f"FAIL: {key} must not be true without real execution evidence")
if data.get("status", "").lower().find("certif") >= 0 and "pending" not in data.get("status", "").lower():
    raise SystemExit("FAIL: package status must remain non-certified")
print("PASS: Build 75 is explicitly non-certified pending official execution.")
