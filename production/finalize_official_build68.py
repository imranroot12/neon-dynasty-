#!/usr/bin/env python3
"""Final fail-closed handoff manifest for Neon Dynasty Build 68.

Run this only after the official Math SDK and Web SDK have executed. It records
SDK commit hashes, verifies the publication set exists, checks 100k+ rows per
mode, and confirms the web production output exists. It never labels a build
production-certified; real Stake Engine staging remains required.
"""
import csv, hashlib, json, os, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATH = Path(os.environ.get("NEON_MATH_GAME") or ROOT / "math/neon_dynasty")
WEB = Path(os.environ.get("NEON_WEB_GAME") or ROOT / "web/neon-dynasty")
MATH_SDK = Path(os.environ.get("ENGINE_MATH_SDK") or ROOT / "../../math-sdk-main")
WEB_SDK = Path(os.environ.get("ENGINE_WEB_SDK") or ROOT / "../../web-sdk-main")
started = os.environ.get("NEON_OFFICIAL_RUN_STARTED_AT")
checks = []

def add(name, ok, detail):
    checks.append({"name": name, "ok": bool(ok), "detail": str(detail)})

def git_head(path):
    try:
        return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unavailable"

def zstd_rows(path):
    if not shutil.which("zstd") or not path.is_file():
        return None
    p = subprocess.Popen(["zstd", "-dc", str(path)], stdout=subprocess.PIPE, text=True)
    rows = sum(1 for line in p.stdout if line.strip()) if p.stdout else 0
    rc = p.wait()
    return rows if rc == 0 else None

for mode in ("base", "basic", "super", "mystery"):
    book = MATH / "library/publish_files" / f"books_{mode}.jsonl.zst"
    lut = MATH / "library/publish_files" / f"lookUpTable_{mode}_0.csv"
    add(f"book_{mode}", book.is_file(), book)
    rows = zstd_rows(book)
    add(f"100k_rows_{mode}", rows is not None and rows >= 100000, rows if rows is not None else "unreadable/missing")
    add(f"lookup_{mode}", lut.is_file(), lut)
    if lut.is_file():
        try:
            with lut.open(newline="") as fh:
                count = sum(1 for r in csv.reader(fh) if r and r[0].strip().isdigit())
            add(f"lookup_rows_{mode}", count >= 100000, count)
        except Exception as exc:
            add(f"lookup_rows_{mode}", False, exc)

index = MATH / "library/publish_files/index.json"
add("publication_index", index.is_file(), index)
web_candidates = [WEB / ".svelte-kit/output", WEB / "build", WEB / "dist"]
existing = [p for p in web_candidates if p.exists()]
add("web_production_output", bool(existing), "; ".join(map(str, existing)) if existing else "missing")

if started:
    try:
        start_ts = float(started)
        stale = []
        for p in [MATH / "library/publish_files", WEB / ".svelte-kit/output"]:
            if p.exists():
                for f in p.rglob("*"):
                    if f.is_file() and f.stat().st_mtime < start_ts:
                        continue
        # Publication freshness is checked on the required book files specifically.
        for mode in ("base", "basic", "super", "mystery"):
            p = MATH / "library/publish_files" / f"books_{mode}.jsonl.zst"
            if p.exists() and p.stat().st_mtime < start_ts:
                stale.append(str(p.relative_to(MATH)))
        add("official_output_freshness", not stale, "; ".join(stale) if stale else "fresh")
    except ValueError:
        add("official_output_freshness", False, "invalid NEON_OFFICIAL_RUN_STARTED_AT")
else:
    add("official_output_freshness", False, "missing NEON_OFFICIAL_RUN_STARTED_AT")

manifest = {
    "build": 68,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "candidate_status": "production_candidate" if all(c["ok"] for c in checks) else "blocked",
    "production_certified": False,
    "sdk_commits": {"math_sdk": git_head(MATH_SDK), "web_sdk": git_head(WEB_SDK)},
    "math_game": str(MATH),
    "web_game": str(WEB),
    "checks": checks,
    "ready_for_staging": all(c["ok"] for c in checks),
    "note": "This manifest does not certify production. Stake Engine staging/RGS validation is still required."
}
path = ROOT / "BUILD_68_OFFICIAL_HANDOFF.json"
path.write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps(manifest, indent=2))
sys.exit(0 if manifest["ready_for_staging"] else 2)
