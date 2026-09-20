#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PUB=ROOT/"math/neon_dynasty/library/publish_files"
MODES={"base":1.0,"basic":100.0,"super":200.0,"mystery":500.0}
errors=[]
for mode,cost in MODES.items():
    p=PUB/f"books_{mode}.jsonl.zst"
    if not p.exists(): errors.append(f"missing {mode} book"); continue
    text=subprocess.check_output(["zstd","-dc",str(p)],text=True)
    rows=[json.loads(x) for x in text.splitlines() if x.strip()]
    if not rows: errors.append(f"empty {mode} book"); continue
    vals=[float(r.get("payoutMultiplier",-1)) for r in rows]
    if min(vals)<0: errors.append(f"negative payout {mode}")
    # Engine publication payoutMultiplier is serialized in hundredths.
    # Normalize it before checking the mode-relative 20,000x cap.
    max_x=max(vals)/100.0
    if max_x>20000+1e-9: errors.append(f"mode max exceeds 20000x: {mode}={max_x}")
    if any("events" not in r for r in rows[:50]): errors.append(f"missing events in {mode}")
    if mode=="mystery":
        counts={"basic":0,"super":0,"hidden":0}
        for r in rows:
            for e in r.get("events",[]):
                if e.get("type")=="mysteryReveal" and e.get("selected") in counts:
                    counts[e["selected"]]+=1
        total=sum(counts.values())
        if total and not (0.60 <= counts["basic"]/total <= 0.80 and 0.15 <= counts["super"]/total <= 0.33 and 0.02 <= counts["hidden"]/total <= 0.12):
            errors.append(f"mystery selection distribution outside broad QA bounds: {counts}")
print(json.dumps({"ok":not errors,"errors":errors},indent=2))
sys.exit(1 if errors else 0)
