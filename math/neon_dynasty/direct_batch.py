import sys, os, json, time, subprocess
from game_config import GameConfig
from gamestate import GameState
mode=sys.argv[1]; start=int(sys.argv[2]); n=int(sys.argv[3]); out=sys.argv[4]
c=GameConfig(); g=GameState(c); g.betmode=mode; t=time.time()
raw=out+'.jsonl'
with open(raw,'w',encoding='utf-8') as f:
  for j in range(n):
    sim=start+j; g.run_spin(sim,sim+987654321)
    f.write(json.dumps(g.library[sim+1],separators=(',',':'))+'\n')
subprocess.run(['zstd','-q','-c','-T0',raw],stdout=open(out,'wb'),check=True)
os.remove(raw)
print('DONE',mode,start,n,out,'elapsed',round(time.time()-t,1),flush=True)
