#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
checks = []

def check(name, ok, detail):
    checks.append({"name": name, "status": "PASS" if ok else "FAIL", "detail": detail})

check("math_source",
      (ROOT/"math/neon_dynasty/run.py").is_file(),
      "math/neon_dynasty/run.py")

check("web_source",
      (ROOT/"web/neon-dynasty/package.json").is_file(),
      "web/neon-dynasty/package.json")

wf = ROOT/".github/workflows/neon-dynasty-official-execution.yml"
check("official_workflow", wf.is_file(), str(wf.relative_to(ROOT)) if wf.is_file() else "missing")

if wf.is_file():
    s = wf.read_text()
    check("official_math_sdk_checkout", "engineio/math-sdk" in s, "workflow must checkout official Math SDK")
    check("official_web_sdk_checkout", "engineio/web-sdk" in s, "workflow must checkout official Web SDK")
    check("optimizer_gate", "optimization_required_guard" in s and "run_optimization" in s, "workflow must require optimization")
    check("publication_gate", "verify_publication.py" in s, "workflow must verify publication output")

# Search for accidental credentials/secrets in text-like project files.
secret_rx = re.compile(r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})")
hits = []
for p in ROOT.rglob("*"):
    if not p.is_file() or ".git" in p.parts:
        continue
    if p.suffix.lower() in {".py",".js",".ts",".json",".yml",".yaml",".md",".txt",".toml",".sh"}:
        try:
            if secret_rx.search(p.read_text(errors="ignore")):
                hits.append(str(p.relative_to(ROOT)))
        except Exception:
            pass
check("credential_scan", not hits, "potential credential files: " + ", ".join(hits) if hits else "no common credential patterns found")

result = {
    "build": 79,
    "status": "PASS" if all(x["status"]=="PASS" for x in checks) else "FAIL",
    "official_execution_verified_here": False,
    "official_optimizer_verified_here": False,
    "rgs_staging_verified_here": False,
    "checks": checks,
}
print(json.dumps(result, indent=2))
sys.exit(0 if result["status"]=="PASS" else 1)
