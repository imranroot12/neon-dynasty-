#!/usr/bin/env python3
"""Static contract checks for Neon Dynasty's locked product specification."""
from pathlib import Path
import json, re
root=Path(__file__).resolve().parents[1]
math=root/'math'/'neon_dynasty'
web=root/'web'/'neon-dynasty'/'src'
errors=[]

def need(cond,msg):
    if not cond: errors.append(msg)

cfg=(math/'game_config.py').read_text()
gs=(math/'gamestate.py').read_text()
buy=(web/'components'/'NeonBuyPanel.svelte').read_text()
rules='\n'.join(p.read_text(errors='ignore') for p in (web/'components').glob('*Rules*'))
need('self.num_reels = 6' in cfg and 'self.num_rows = [5] * 6' in cfg, 'grid must be 6x5')
need('self.rtp = 0.96' in cfg, 'RTP target must be 0.96')
need('self.wincap = 20000.0' in cfg, 'win cap must be 20000x')
need('"base", 1.0' in cfg and '"basic", 100.0' in cfg and '"super", 200.0' in cfg and '"mystery", 500.0' in cfg, 'mode costs missing')
need('self.tot_fs = 8' in gs and 'self.tot_fs = 10' in gs and 'self.tot_fs = 15' in gs, 'bonus spin counts missing')
need('"hidden"' in gs and '"mystery"' in gs, 'hidden/mystery flow missing')
need('"basic"] * 70 + ["super"] * 24 + ["hidden"] * 6' in gs, 'mystery vault weights missing')
need('3× BET' in buy and '5×' not in buy, 'ANTE UI must show locked 3x pricing; trigger ratio belongs in rules/RGS contract')
need('MYSTERY BUY' in buy and '500' in buy, 'mystery buy UI missing')
need('100' in buy and '200' in buy, 'bonus buy costs missing')
need('requestBet' in buy, 'bonus purchase must go through RGS')
# Ensure no direct hidden buy mode appears in the UI mode table.
need('id: \'hidden\'' not in buy and 'id: "hidden"' not in buy, 'hidden bonus must not be directly purchasable')
# Ensure replay hooks remain present.
allsrc='\n'.join(p.read_text(errors='ignore') for p in web.rglob('*.ts'))
need('requestReplay' in allsrc or 'replay' in allsrc, 'replay integration missing')
report={'ok':not errors,'errors':errors}
(root/'qa'/'BUILD_59_LOCKED_CONTRACT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(0 if not errors else 1)
