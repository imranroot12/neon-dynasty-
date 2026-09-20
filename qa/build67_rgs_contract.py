#!/usr/bin/env python3
"""Build 67 RGS/Web integration contract audit.

Static audit only: no fake session is created. A real staging session must
supply URL/session parameters and an actual authenticate/play/end-round run.
"""
from pathlib import Path
import json, re

ROOT=Path(__file__).resolve().parents[1]
files=[p for p in ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
text=""
for p in files:
    if p.suffix.lower() in {".ts",".tsx",".js",".jsx",".svelte",".json",".md"}:
        try: text += p.read_text(encoding="utf-8",errors="ignore")+"\n"
        except: pass

checks={
 "authenticate_request": bool(re.search(r"requestAuthenticate|authenticate",text,re.I)),
 "play_request": bool(re.search(r"requestPlay|play",text,re.I)),
 "end_round": bool(re.search(r"end.?round|requestEnd",text,re.I)),
 "session_id": bool(re.search(r"sessionID|sessionId",text)),
 "rgs_url": bool(re.search(r"rgsUrl|rgsURL",text)),
 "book_event": bool(re.search(r"bookEvent|book_event|event",text,re.I)),
 "balance": bool(re.search(r"\bbalance\b",text,re.I)),
}
result={"build":"67","checks":checks,"static_contract_pass":all(checks.values()),
        "staging_session_executed":False,
        "production_certified":False}
(ROOT/"BUILD_67_RGS_CONTRACT.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
raise SystemExit(0 if result["static_contract_pass"] else 1)
