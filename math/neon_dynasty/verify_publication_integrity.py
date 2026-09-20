"""Offline publication integrity gate for Neon Dynasty.
Checks every published lookup-table payout exists in its book and that weighted
RTP/max-win constraints are internally consistent. This is not Stake approval.
"""
import csv, json, subprocess, pathlib, hashlib
ROOT=pathlib.Path(__file__).resolve().parent
PUB=ROOT/'library'/'publish_files'
MODES={'base':1.0,'basic':100.0,'super':200.0,'mystery':500.0}
CAP=20000.0
out={}
for mode,cost in MODES.items():
    raw=subprocess.check_output(['zstd','-q','-d','-c',str(PUB/f'books_{mode}.jsonl.zst')],text=True)
    books=[json.loads(x) for x in raw.splitlines() if x.strip()]
    payouts=[float(x['payoutMultiplier'])/100.0 for x in books]
    lut=[]; weights=[]
    with open(PUB/f'lookUpTable_{mode}_0.csv',newline='') as f:
        for r in csv.reader(f):
            lut.append(float(r[2])/100.0); weights.append(float(r[1]))
    bookset={round(x,9) for x in payouts}
    missing=[x for x in lut if round(x,9) not in bookset]
    weighted=sum(p*w for p,w in zip(lut,weights))/sum(weights)
    out[mode]={
      'book_rows':len(books),'lut_rows':len(lut),'missing_lut_payouts':len(missing),
      'weighted_rtp':weighted/cost,'max_book_multiplier':max(payouts),
      'max_lut_multiplier':max(lut),'under_cap':max(payouts)<=CAP and max(lut)<=CAP,
      'books_sha256':hashlib.sha256((PUB/f'books_{mode}.jsonl.zst').read_bytes()).hexdigest(),
      'lut_sha256':hashlib.sha256((PUB/f'lookUpTable_{mode}_0.csv').read_bytes()).hexdigest(),
    }
print(json.dumps(out,indent=2))
(ROOT/'BUILD_50_INTEGRITY.json').write_text(json.dumps(out,indent=2))
assert all(v['missing_lut_payouts']==0 for v in out.values())
assert all(v['under_cap'] for v in out.values())
