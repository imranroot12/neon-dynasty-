#!/usr/bin/env python3
import json, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATH = Path(os.environ.get("NEON_MATH_GAME", ROOT/"math/neon_dynasty"))
WEB = Path(os.environ.get("NEON_WEB_GAME", ROOT/"web/neon-dynasty"))
checks=[]

def add(name, ok, detail):
    checks.append({"name":name, "ok":bool(ok), "detail":str(detail)})

add("python", sys.version_info >= (3,12), sys.version.split()[0])
add("node", shutil.which("node") is not None, shutil.which("node") or "missing")
add("pnpm", shutil.which("pnpm") is not None, shutil.which("pnpm") or "missing")
add("zstd", shutil.which("zstd") is not None, shutil.which("zstd") or "missing")
add("cargo", shutil.which("cargo") is not None, shutil.which("cargo") or "missing")

for mode in ("base","basic","super","mystery"):
    p=MATH/"library/publish_files"/f"books_{mode}.jsonl.zst"
    add(f"publication_book_{mode}", p.is_file(), p)

# Count rows with the system zstd decoder. This gate intentionally does not
# manufacture rows to satisfy the 100k production requirement.
for mode in ("base","basic","super","mystery"):
    p=MATH/"library/publish_files"/f"books_{mode}.jsonl.zst"
    if not p.is_file() or not shutil.which("zstd"):
        add(f"100k_rows_{mode}", False, "book unavailable or zstd missing")
        continue
    proc=subprocess.Popen(["zstd","-dc",str(p)], stdout=subprocess.PIPE, text=True)
    rows=0
    if proc.stdout:
        for line in proc.stdout:
            if line.strip():
                rows += 1
        proc.stdout.close()
    rc=proc.wait()
    add(f"100k_rows_{mode}", rc == 0 and rows >= 100000, f"{rows} rows")

web_candidates=[WEB/".svelte-kit/output", WEB/"build", WEB/"dist"]
existing=[str(p) for p in web_candidates if p.exists()]
add("web_build_artifact", bool(existing), "; ".join(existing) if existing else "missing")

sample_tokens=("mm_", "miningfont_", "clusterpay", "reelhouse_glow", "transition.atlas",
               "symbols3", "sample_provider", "sample_lines")
sample=[]
for p in (ROOT/"web").rglob("*"):
    if p.is_file() and any(t in p.name.lower() for t in sample_tokens):
        sample.append(str(p.relative_to(ROOT)))
add("sample_asset_quarantine", not sample, "; ".join(sample[:12]) if sample else "clean")

report={
    "build":"61",
    "candidate_status": "development_candidate",
    "production_certified": False,
    "checks":checks,
    "ready":all(x["ok"] for x in checks),
    "note":"Production certification requires the official engineio/math-sdk optimizer and 100k+ verified outcomes per mode plus a successful Web SDK production build."
}
path=ROOT/"RELEASE_GATE_BUILD_61.json"
path.write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(report, indent=2))
sys.exit(0 if report["ready"] else 2)
