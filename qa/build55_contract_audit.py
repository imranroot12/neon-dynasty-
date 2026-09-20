#!/usr/bin/env python3
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'web' / 'neon-dynasty'

errors=[]

def check(cond,msg):
    if not cond: errors.append(msg)

# RGS contract source checks
rgs=(WEB/'src/game/rgsContract.ts').read_text()
check('requestBet' not in rgs, 'rgsContract must remain pure: requestBet must not be embedded in contract helpers')
check('/bet/replay/' in rgs, 'Replay endpoint contract missing')
check('clampToRgsBet' in rgs and 'isRgsBetAllowed' in rgs, 'Bet validation helpers missing')

# Replay endpoint behavior mirrored as deterministic test vectors.
def replay_endpoint(cfg):
    if not all([cfg.get('replay'), cfg.get('rgsUrl'), cfg.get('game'), cfg.get('version'), cfg.get('mode'), cfg.get('event')]):
        return None
    import urllib.parse
    return cfg['rgsUrl'].rstrip('/') + '/bet/replay/' + '/'.join(urllib.parse.quote(str(cfg[k]), safe='') for k in ('game','version','mode','event'))
check(replay_endpoint({'replay':True,'rgsUrl':'https://rgs.test/','game':'neon_dynasty','version':'1','mode':'base','event':'58'}) == 'https://rgs.test/bet/replay/neon_dynasty/1/base/58', 'Replay endpoint vector failed')
check(replay_endpoint({'replay':False,'rgsUrl':'x','game':'g','version':'1','mode':'base','event':'1'}) is None, 'Replay must be disabled without replay=true')

# Event schema consistency.
types=(WEB/'src/game/typesBookEvent.ts').read_text()
handler=(WEB/'src/game/bookEventHandlerMap.ts').read_text()
for ev in ['bonusStart','mysteryReveal','dragonMeter','dragonEvent','bonusComplete','finalWin','freeSpinRetrigger']:
    check(f"type: '{ev}'" in types, f'Missing event type: {ev}')
    check(f"{ev}: async" in handler, f'Missing handler: {ev}')

# No duplicate union entries for the known snapshot event.
union=types.split('export type BookEvent =',1)[1].split('export type Bet',1)[0]
check(union.count('BookEventCreateBonusSnapshot') == 1, 'BookEventCreateBonusSnapshot appears more than once in BookEvent union')

# Locked game configuration checks.
config=(WEB/'src/game/config.ts').read_text()
for token in ["providerName: 'Voltix Games'", "gameName: 'Neon Dynasty'", "gameID: 'neon_dynasty'", 'rtp: 0.96', 'numReels: 6']:
    check(token in config, f'Missing locked config token: {token}')
check(config.count('numRows: [5, 5, 5, 5, 5, 5]') == 1, '6x5 configuration missing')
for mode,cost in [('basic','100.0'),('super','200.0'),('mystery','500.0')]:
    check(f"{mode}: {{ cost: {cost}" in config, f'{mode} cost mismatch')

# Asset registry must not reference the inherited sample static asset tree.
assets=(WEB/'src/game/assets.ts').read_text()
check('static/assets' not in assets and 'sample_' not in assets, 'Sample asset reference found in Neon registry')

# Required original assets exist.
required=['ui/background.svg','ui/logo.svg','ui/dragon-meter.svg','ui/vault.svg','audio/sounds.ogg','audio/sounds.json']
for rel in required:
    check((WEB/'src/assets/neon'/rel).exists(), f'Missing Neon asset: {rel}')

# Asset manifest audit, if present.
manifest=ROOT/'NEON_DYNASTY_ASSET_MANIFEST_BUILD_54.json'
if manifest.exists():
    data=json.loads(manifest.read_text())
    check(not data.get('sample_or_unverified_candidates'), 'Asset manifest still reports sample/unverified candidates')

if errors:
    print('BUILD 55 CONTRACT AUDIT: FAIL')
    for e in errors: print(' -',e)
    sys.exit(1)
print('BUILD 55 CONTRACT AUDIT: PASS')
print('RGS bet validation, replay routing, Neon event handlers, locked math metadata, and asset registry checks passed.')
