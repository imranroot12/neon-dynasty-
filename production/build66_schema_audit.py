#!/usr/bin/env python3
"""Build 66 static publication schema audit."""
from pathlib import Path
import json, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
PUB=ROOT/"math/neon_dynasty/library/publish_files"
MODES=("base","basic","super","mystery")
required=("simulationNumber","probability","payoutMultiplier")
results={}
errors=[]

for mode in MODES:
    p=PUB/f"books_{mode}.jsonl.zst"
    if not p.exists():
        errors.append(f"missing {p}")
        continue
    proc=subprocess.Popen(["zstd","-dc",str(p)],stdout=subprocess.PIPE,text=True)
    seen=0; bad=0
    if proc.stdout:
        for line in proc.stdout:
            if not line.strip(): continue
            seen+=1
            try: row=json.loads(line)
            except Exception:
                bad+=1; continue
            if any(k not in row for k in required): bad+=1
            if not isinstance(row.get("events"),list): bad+=1
            if not isinstance(row.get("payoutMultiplier"),(int,float)): bad+=1
        proc.stdout.close()
    rc=proc.wait()
    if rc: errors.append(f"decode failure {mode}")
    if bad: errors.append(f"{mode}: {bad} schema-invalid rows")
    results[mode]={"rows":seen,"schema_invalid":bad}
(ROOT/"BUILD_66_SCHEMA_AUDIT.json").write_text(json.dumps({"build":"66","ok":not errors,"errors":errors,"modes":results},indent=2)+"\n")
print(json.dumps({"build":"66","ok":not errors,"errors":errors,"modes":results},indent=2))
sys.exit(0 if not errors else 1)
