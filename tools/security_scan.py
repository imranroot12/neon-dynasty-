#!/usr/bin/env python3
"""Lightweight release guard: reject obvious RGS/session secrets in tracked text."""

from pathlib import Path
import re
import sys

PATTERNS = [
    re.compile(r"(?i)(session[_-]?id|authorization|bearer|api[_-]?key)\s*[:=]\s*['\"][^'\"]{16,}"),
    re.compile(r"(?i)https?://[^\s\"']*(?:token|session|auth)[^\s\"']*"),
]

SKIP = {".git", "node_modules", ".svelte-kit", "dist", "build", "__pycache__"}

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
hits = []

for p in root.rglob("*"):
    if not p.is_file() or any(part in SKIP for part in p.parts):
        continue
    if p.stat().st_size > 2_000_000:
        continue
    try:
        text = p.read_text(errors="ignore")
    except Exception:
        continue
    for pattern in PATTERNS:
        if pattern.search(text):
            hits.append(str(p.relative_to(root)))
            break

if hits:
    print("SECURITY GUARD FAILED:")
    for h in sorted(set(hits)):
        print(" -", h)
    sys.exit(1)

print("SECURITY GUARD PASS: no obvious embedded RGS/session secrets found.")
