#!/usr/bin/env python3
from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]
TEXT_EXT={".ts",".tsx",".js",".jsx",".svelte",".css",".scss",".json",".html",".md"}
ASSET_EXT={".png",".jpg",".jpeg",".webp",".avif",".svg",".mp3",".ogg",".wav",".m4a",".woff",".woff2",".ttf"}
files=[p for p in ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
assets=[p for p in files if p.suffix.lower() in ASSET_EXT or p.name.endswith(".atlas")]
source=[p for p in files if p.suffix.lower() in TEXT_EXT]
refs=set()
pat=re.compile(r'''["'`]([^"'`\\n]+\.(?:png|jpe?g|webp|avif|svg|mp3|ogg|wav|m4a|atlas|woff2?|ttf))["'`]''',re.I)
for p in source:
    try: txt=p.read_text(encoding="utf-8",errors="ignore")
    except: continue
    refs.update(x for x in pat.findall(txt) if not x.startswith(("http://","https://","data:")))
asset_names={p.name for p in assets}
missing=sorted(r for r in refs if Path(r).name not in asset_names)
sample_terms=("sample_","placeholder","miningfont","storybook")
suspicious=[str(p.relative_to(ROOT)) for p in files if any(t in p.name.lower() for t in sample_terms)]
audio=[str(p.relative_to(ROOT)) for p in assets if p.suffix.lower() in {".mp3",".ogg",".wav",".m4a"}]
all_text=""
for p in source:
    try: all_text += p.read_text(encoding="utf-8",errors="ignore")+"\n"
    except: pass
features={k:bool(re.search(v,all_text,re.I)) for k,v in {
 "cluster":r"\bcluster\b","tumble":r"\btumble\b","wild":r"\bwild\b",
 "mystery":r"\bmystery\b","multiplier":r"\bmultipli","freespin":r"free.?spin",
 "buy":r"\bbonus.?buy\b|\bmystery.?buy\b","dragon":r"\bdragon\b"}.items()}
result={"build":"64","asset_count":len(assets),"audio_count":len(audio),
"explicit_missing_asset_references":missing,
"suspicious_sample_or_placeholder_files":suspicious,
"feature_presence":features,"ok":not missing and not suspicious}
(ROOT/"BUILD_64_ASSET_UI_AUDIT.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
raise SystemExit(0 if result["ok"] else 2)
