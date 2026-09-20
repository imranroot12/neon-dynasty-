from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]/'web/neon-dynasty/static'
patterns=('mm_','MM_','miningfont','symbols3','reelhouse','clusterpay','big_wins','fs_screen','buy_button','tumble_win','multiframe','anticipation','transition','SD2_','sounds.')
found=[]
for p in root.rglob('*'):
    if p.is_file() and any(x.lower() in p.name.lower() for x in patterns): found.append(str(p.relative_to(root)))
report={'sample_or_unverified_candidates':sorted(found),'approval_ready':len(found)==0}
print(json.dumps(report,indent=2))
