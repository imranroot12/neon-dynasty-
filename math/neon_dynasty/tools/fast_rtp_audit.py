"""Independent high-volume RTP audit.

Runs the actual Neon Dynasty GameState but disables presentation-event
serialization. This is for math analysis only; it does NOT generate publishable
books. Use `run_production.py`/the official SDK for publication books.
"""
import argparse, json, multiprocessing as mp, time
from gamestate import GameState
from game_config import GameConfig

def worker(args):
    mode,start,n=args; c=GameConfig(); g=GameState(c); g.betmode=mode
    total=0.0; mx=0.0
    for sim in range(start,start+n):
        g.run_spin(sim, sim+987654321)
        v=float(g.final_win); total += v; mx=max(mx,v)
    return total,mx,n

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('mode'); ap.add_argument('total',type=int); ap.add_argument('--workers',type=int,default=4); ap.add_argument('--offset',type=int,default=0); args=ap.parse_args()
    chunk=args.total//args.workers; jobs=[]; st=args.offset
    for i in range(args.workers):
        n=chunk+(1 if i < args.total%args.workers else 0); jobs.append((args.mode,st,n)); st+=n
    t=time.time()
    with mp.Pool(args.workers) as pool: results=pool.map(worker,jobs)
    total=sum(x[0] for x in results); mx=max(x[1] for x in results)
    cost={'base':1.0,'basic':100.0,'super':200.0,'mystery':500.0}[args.mode]
    out={'mode':args.mode,'spins':args.total,'cost':cost,'average_payout':total/args.total,'rtp':total/(args.total*cost),'max_observed':mx,'elapsed_seconds':round(time.time()-t,2),'publication_ready':False}
    print(json.dumps(out,indent=2)); return out
if __name__=='__main__': main()
