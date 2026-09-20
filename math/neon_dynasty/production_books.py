import sys, os, json, time, csv, shutil, subprocess
from game_config import GameConfig
from gamestate import GameState

MODE=sys.argv[1]; TOTAL=int(sys.argv[2]); BATCH=int(sys.argv[3]) if len(sys.argv)>3 else 10000
c=GameConfig(); pub=c.publish_path; os.makedirs(pub,exist_ok=True)
out_json=os.path.join(pub,f'books_{MODE}.jsonl')
start=time.time(); count=0
with open(out_json,'w',encoding='utf-8') as out:
    for batch_start in range(0,TOTAL,BATCH):
        n=min(BATCH,TOTAL-batch_start)
        g=GameState(c); g.betmode=MODE
        for j in range(n):
            sim=batch_start+j
            g.run_spin(sim, sim+987654321)
            out.write(json.dumps(g.library[sim+1],separators=(',',':'))+'\n')
        out.flush()
        print(f'{MODE}: {batch_start+n}/{TOTAL} elapsed={time.time()-start:.1f}s',flush=True)
# compress using system zstd
zst=out_json+'.zst'
with open(out_json,'rb') as src, open(zst,'wb') as dst:
    subprocess.run(['zstd','-q','-c','-T0','-'],stdin=src,stdout=dst,check=True)
os.remove(out_json)
print('DONE',MODE,zst,os.path.getsize(zst))
