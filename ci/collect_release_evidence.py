#!/usr/bin/env python3
"""Collect release evidence without fabricating any execution result.

Usage:
  python ci/collect_release_evidence.py <artifact-root> <evidence-output>
"""
from pathlib import Path
import hashlib, json, sys, time

def sha256(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    if len(sys.argv) != 3:
        print("usage: collect_release_evidence.py <artifact-root> <evidence-output>")
        return 2

    root = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    if not root.is_dir():
        print(f"artifact root does not exist: {root}")
        return 2

    files = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and ".git" not in p.parts:
            files[p.relative_to(root).as_posix()] = sha256(p)

    evidence = {
        "generated_at_epoch": int(time.time()),
        "artifact_root": str(root),
        "files": files,
        "official_execution_evidence_present": False,
        "certified": False,
        "note": (
            "Hashes prove artifact identity only. They do not prove Math SDK execution, "
            "optimizer execution, Web SDK build success, or RGS staging success."
        )
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "file_count": len(files),
        "evidence": str(out),
        "certified": False
    }, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
