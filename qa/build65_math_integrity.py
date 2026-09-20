#!/usr/bin/env python3
"""Build 65 pre-optimizer integrity checks for publication books/LUTs.

This verifies that each published lookup-table row points to an existing book
row and that the payout stored in the LUT agrees with that book row. It does
NOT certify the official optimizer or replace RGS verification.
"""
from pathlib import Path
import csv, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
PUB=ROOT/'math/neon_dynasty/library/publish_files'
MODES=('base','basic','super','mystery')
errors=[]; report={}
for mode in MODES:
    book=PUB/f'books_{mode}.jsonl.zst'; lut=PUB/f'lookUpTable_{mode}_0.csv'
    if not book.exists() or not lut.exists():
        errors.append(f'{mode}: missing book or LUT'); continue
    # Stream the compressed book into a compact id->payout map.
    proc=subprocess.Popen(['zstd','-dc',str(book)],stdout=subprocess.PIPE,text=True)
    byid={}
    import json as J
    assert proc.stdout
    for line in proc.stdout:
        if line.strip():
            r=J.loads(line); byid[int(r['id'])]=int(r['payoutMultiplier'])
    proc.stdout.close(); rc=proc.wait()
    if rc: errors.append(f'{mode}: zstd decode failed'); continue
    rows=0; mismatches=[]; missing=[]
    with lut.open(newline='') as f:
        for row in csv.reader(f):
            if not row: continue
            rows+=1; idx=int(row[0]); payout=int(float(row[2]))
            if idx not in byid: missing.append(idx)
            elif byid[idx] != payout: mismatches.append((idx,byid[idx],payout))
    if missing: errors.append(f'{mode}: {len(missing)} LUT ids missing from book')
    if mismatches: errors.append(f'{mode}: {len(mismatches)} LUT payout mismatches')
    report[mode]={'book_rows':len(byid),'lut_rows':rows,'missing_ids':len(missing),'payout_mismatches':len(mismatches)}
out={'build':'65','ok':not errors,'errors':errors,'modes':report,
     'optimizer_certified':False,'rgs_verified':False}
(ROOT/'BUILD_65_MATH_INTEGRITY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
sys.exit(1 if errors else 0)
