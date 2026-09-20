import os, json, csv, hashlib, shutil, subprocess
ROOT=os.path.dirname(__file__); LIB=os.path.join(ROOT,'library'); PUB=os.path.join(LIB,'publish_files'); CFG=os.path.join(LIB,'configs'); FORCE=os.path.join(LIB,'forces')
os.makedirs(PUB,exist_ok=True)
# Remove development clutter from publish dir.
for name in os.listdir(PUB):
    if name in {'books_base.jsonl.zst','books_basic.jsonl.zst','books_super.jsonl.zst','books_mystery.jsonl.zst'} or name.startswith('lookUpTable_') or name=='index.json':
        continue
    os.remove(os.path.join(PUB,name))
# Recreate optimized lookup files from current base tables.
def rows(path): return [list(map(int,r)) for r in csv.reader(open(path))]
# base/basic/super zero weighting tuned to 96% on current sampled book sets
for mode,cost in [('base',1),('basic',100),('super',200)]:
    rs=rows(os.path.join(LIB,'lookup_tables',f'lookUpTable_{mode}.csv'))
    vals=[r[2] for r in rs]; z=sum(v==0 for v in vals); nz=len(vals)-z; s=sum(vals); target=96*cost
    wz=round(((s/target-nz)/z)*1_000_000); wn=1_000_000
    for r in rs:r[1]=wz if r[2]==0 else wn
    with open(os.path.join(PUB,f'lookUpTable_{mode}_0.csv'),'w',newline='') as f:csv.writer(f).writerows(rs)
# mystery: zero weight 0.5x and high-tail (>=374.69x) 1.067341x, tuned to 96%.
rs=rows(os.path.join(LIB,'lookup_tables','lookUpTable_mystery.csv'))
for r in rs:
    if r[2]==0:r[1]=500000
    elif r[2]>=37469:r[1]=1067341
    else:r[1]=1000000
with open(os.path.join(PUB,'lookUpTable_mystery_0.csv'),'w',newline='') as f:csv.writer(f).writerows(rs)
# Ensure index references exact optimized filenames.
index={'modes':[]}
for mode,cost in [('base',1.0),('basic',100.0),('super',200.0),('mystery',500.0)]:
    index['modes'].append({'name':mode,'cost':cost,'events':f'books_{mode}.jsonl.zst','weights':f'lookUpTable_{mode}_0.csv'})
with open(os.path.join(PUB,'index.json'),'w') as f:json.dump(index,f,indent=4)
# Copy config/force files needed for operator handoff.
# Build backend config with hashes of current publication files.
def sha(path):
    h=hashlib.sha256();
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
config_path=os.path.join(CFG,'config.json')
config=json.load(open(config_path))
for bm in config['bookShelfConfig']:
    mode=bm['name']; lut=os.path.join(PUB,f'lookUpTable_{mode}_0.csv'); book=os.path.join(PUB,f'books_{mode}.jsonl.zst'); force=os.path.join(FORCE,f'force_record_{mode}.json')
    bm['tables'][0]['file']=os.path.basename(lut); bm['tables'][0]['sha256']=sha(lut)
    bm['bookLength']=sum(1 for _ in open(lut))
    bm['booksFile']['file']=os.path.basename(book); bm['booksFile']['sha256']=sha(book)
    bm['forceFile']['file']=os.path.basename(force); bm['forceFile']['sha256']=sha(force)
with open(config_path,'w') as f:json.dump(config,f,indent=4)
print('FINALIZED')
