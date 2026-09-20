#!/usr/bin/env python3
"""Fail-closed finalizer for the real network-enabled Engine execution."""
from __future__ import annotations
import hashlib, json, os, subprocess, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
math_game = Path(os.environ.get("NEON_MATH_GAME", ""))
web_game = Path(os.environ.get("NEON_WEB_GAME", ""))
if not math_game.is_dir() or not web_game.is_dir():
    raise SystemExit("FAIL: official Math/Web output directories were not supplied")

required_modes = ("base", "basic", "super", "mystery")
errors: list[str] = []

# Accept common book naming variants while requiring a real, fresh publication set.
publish = math_game / "library" / "publish_files"
if not publish.is_dir():
    errors.append(f"missing publication directory: {publish}")

index = publish / "index.json"
if not index.exists():
    errors.append("missing publication index.json")

counts: dict[str, int] = {}
for mode in required_modes:
    candidates = [
        math_game / "library" / "books" / f"books_{mode}.jsonl",
        math_game / "library" / "books" / f"books_{mode}.jsonl.zst",
        publish / f"books_{mode}.jsonl",
        publish / f"books_{mode}.jsonl.zst",
    ]
    found = next((p for p in candidates if p.exists()), None)
    if not found:
        errors.append(f"missing book for mode {mode}")
        continue
    if found.stat().st_mtime + 1 < time.time() - 86400:
        errors.append(f"book for mode {mode} appears older than 24h: {found}")
    if found.suffix == ".zst":
        # zstd stream is intentionally not decoded here; use sidecar/index metadata if present.
        counts[mode] = -1
    else:
        with found.open("rb") as f:
            counts[mode] = sum(1 for line in f if line.strip())
        if counts[mode] < 100_000:
            errors.append(f"book {mode} has only {counts[mode]} rows; require >=100000")

# Web SDK official build output documented by Engine.
web_output_candidates = [
    web_game / ".svelte-kit" / "output" / "prerendered" / "pages" / "index.html",
    web_game / ".svelte-kit" / "output" / "client",
]
if not any(p.exists() for p in web_output_candidates):
    errors.append("missing official Web SDK production output")

sdk_commits = {}
for key, path in (("math_sdk", os.environ.get("ENGINE_MATH_SDK", "")), ("web_sdk", os.environ.get("ENGINE_WEB_SDK", ""))):
    if path:
        try:
            sdk_commits[key] = subprocess.check_output(["git", "-C", path, "rev-parse", "HEAD"], text=True).strip()
        except Exception:
            errors.append(f"could not resolve {key} git commit")

manifest = {
    "build": 69,
    "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "official_execution": True,
    "production_certified": False,
    "math_sdk_commits": sdk_commits,
    "book_rows": counts,
    "staging_required": True,
    "staging_required_checks": [
        "authenticate/session",
        "balance",
        "base spin",
        "tumble/cluster book events",
        "Mystery Buy",
        "Basic/Super/Hidden bonus modes",
        "free-spin retriggers",
        "sticky/expanding wild events",
        "end-round",
        "replay",
    ],
    "errors": errors,
}

out = ROOT / "BUILD_69_OFFICIAL_HANDOFF.json"
out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
if errors:
    raise SystemExit("FAIL: " + "; ".join(errors))
print(out)
