#!/usr/bin/env python3
"""Build 61 streaming publication-book contract audit.

Reads each zstd JSONL publication book line-by-line so QA remains bounded in
memory as production books grow from 10k to 100k+ rows.
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "math/neon_dynasty/library/publish_files"
MODES = ("base", "basic", "super", "mystery")
errors = []
summary = {}

for mode in MODES:
    path = PUB / f"books_{mode}.jsonl.zst"
    if not path.exists():
        errors.append(f"missing {mode} book")
        continue

    count = 0
    max_x = 0.0
    min_payout = None
    events_missing = 0
    mystery_counts = {"basic": 0, "super": 0, "hidden": 0}

    proc = subprocess.Popen(
        ["zstd", "-dc", str(path)],
        stdout=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="strict",
    )
    assert proc.stdout is not None
    try:
        for line in proc.stdout:
            if not line.strip():
                continue
            row = json.loads(line)
            count += 1
            payout = float(row.get("payoutMultiplier", -1))
            min_payout = payout if min_payout is None else min(min_payout, payout)
            max_x = max(max_x, payout / 100.0)
            if "events" not in row:
                events_missing += 1
            if mode == "mystery":
                for event in row.get("events", []):
                    if event.get("type") == "mysteryReveal":
                        selected = event.get("selected")
                        if selected in mystery_counts:
                            mystery_counts[selected] += 1
    finally:
        proc.stdout.close()
    rc = proc.wait()
    if rc != 0:
        errors.append(f"zstd decode failed: {mode} rc={rc}")
        continue

    if count == 0:
        errors.append(f"empty {mode} book")
    if min_payout is not None and min_payout < 0:
        errors.append(f"negative payout {mode}")
    if max_x > 20000.0 + 1e-9:
        errors.append(f"mode max exceeds 20000x: {mode}={max_x}")
    if events_missing:
        errors.append(f"missing events in {mode}: {events_missing} rows")

    if mode == "mystery":
        total = sum(mystery_counts.values())
        if total:
            b = mystery_counts["basic"]/total
            s = mystery_counts["super"]/total
            h = mystery_counts["hidden"]/total
            if not (0.60 <= b <= 0.80 and 0.15 <= s <= 0.33 and 0.02 <= h <= 0.12):
                errors.append(f"mystery selection distribution outside broad QA bounds: {mystery_counts}")

    summary[mode] = {
        "rows": count,
        "max_win_x": round(max_x, 6),
        "min_payout_serialized": min_payout,
        "events_missing": events_missing,
        "mystery_selection": mystery_counts if mode == "mystery" else None,
    }

result = {"ok": not errors, "errors": errors, "summary": summary}
print(json.dumps(result, indent=2))
sys.exit(1 if errors else 0)
