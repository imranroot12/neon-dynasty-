import sys, json, os, time
from game_config import GameConfig
from gamestate import GameState
mode=sys.argv[1]; n=int(sys.argv[2])
c=GameConfig(); gs=GameState(c); gs.betmode=mode
out=[]; t=time.time()
for i in range(n):
    gs.run_spin(i, i+1234567)
    out.append(gs.library[i+1])
    if (i+1)%1000==0: print(i+1, 'elapsed', round(time.time()-t,1), flush=True)
os.makedirs(c.publish_path,exist_ok=True)
with open(os.path.join(c.publish_path,f'direct_{mode}_{n}.jsonl'),'w') as f:
    for x in out: f.write(json.dumps(x)+'\n')
print('DONE')
