import csv, os, math, json
ROOT=os.path.dirname(__file__); LIB=os.path.join(ROOT,'library'); PUB=os.path.join(LIB,'publish_files'); LUT=os.path.join(LIB,'lookup_tables')
os.makedirs(PUB,exist_ok=True)
MODES=[('base',1.0),('basic',100.0),('super',200.0),('mystery',500.0)]
report={}
for mode,cost in MODES:
    src=os.path.join(LUT,f'lookUpTable_{mode}.csv')
    rows=[list(map(int,r)) for r in csv.reader(open(src))]
    target_int=0.96*cost*10
    nz=[r for r in rows if r[2]>0]; z=[r for r in rows if r[2]==0]
    if not z:
        # If no zero-payout outcomes exist, solve with all weights=1 only when already exact.
        weight=1_000_000
    else:
        num=sum(r[2] for r in nz)*1_000_000 - target_int*len(nz)*1_000_000
        den=target_int*len(z)
        weight=max(1,round(num/den)) if den else 1_000_000
    for r in rows: r[1]=weight if r[2]==0 else 1_000_000
    out=os.path.join(PUB,f'lookUpTable_{mode}_0.csv')
    with open(out,'w',newline='') as f: csv.writer(f).writerows(rows)
    sw=sum(r[1]*r[2] for r in rows); ww=sum(r[1] for r in rows)
    avg_int=sw/ww
    rtp=(avg_int/10)/cost
    report[mode]={'rows':len(rows),'zero_rows':len(z),'zero_weight':weight,'weighted_average_multiplier':avg_int/10,'weighted_rtp':rtp}
index={'modes':[{'name':m,'cost':c,'events':f'books_{m}.jsonl.zst','weights':f'lookUpTable_{m}_0.csv'} for m,c in MODES]}
with open(os.path.join(PUB,'index.json'),'w') as f: json.dump(index,f,indent=2)
with open(os.path.join(ROOT,'CORRECTED_WEIGHT_REPORT.json'),'w') as f: json.dump(report,f,indent=2)
print(json.dumps(report,indent=2))
