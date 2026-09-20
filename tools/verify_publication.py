#!/usr/bin/env python3
"""Verify Math SDK publication books against lookup tables.

Usage:
  python tools/verify_publication.py <publication_dir>

The verifier is deliberately conservative: missing files, malformed rows,
duplicate IDs, or payout mismatches fail the process.
"""

from pathlib import Path
import csv, json, sys, gzip

def read_jsonl(path):
    rows = []
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append((n, json.loads(line)))
            except Exception as e:
                raise RuntimeError(f"{path}:{n}: invalid JSON: {e}")
    return rows

def find_files(pub, mode):
    m = mode.lower()
    books = list(pub.rglob(f"*books*{m}*.jsonl")) + list(pub.rglob(f"*books*{m}*.jsonl.zst"))
    luts = list(pub.rglob(f"*lookUpTable*{m}*.csv"))
    return books, luts

def verify_mode(pub, mode):
    books, luts = find_files(pub, mode)
    if not books:
        raise RuntimeError(f"{mode}: publication book not found")
    if not luts:
        raise RuntimeError(f"{mode}: lookup table not found")

    book = books[0]
    lut = luts[0]

    # zstd is intentionally delegated to the official environment. This verifier
    # accepts plain JSONL/GZip here and tells the caller when zstd support is needed.
    if book.suffix == ".zst":
        raise RuntimeError(f"{mode}: zstd book requires zstd-capable verifier/runtime")

    book_rows = read_jsonl(book)
    seen = set()
    book_payout = {}
    for line_no, row in book_rows:
        if not isinstance(row, dict) or "id" not in row or "payoutMultiplier" not in row:
            raise RuntimeError(f"{mode}: malformed book row at {line_no}")
        rid = str(row["id"])
        if rid in seen:
            raise RuntimeError(f"{mode}: duplicate book id {rid}")
        seen.add(rid)
        book_payout[rid] = row["payoutMultiplier"]

    lut_payout = {}
    with lut.open(newline="", encoding="utf-8") as f:
        for n, row in enumerate(csv.reader(f), 1):
            if not row or row[0].strip().lower() in {"id", "simulationid", "simulation_id"}:
                continue
            if len(row) < 3:
                raise RuntimeError(f"{mode}: malformed LUT row {n}")
            rid = row[0].strip()
            try:
                payout = float(row[2])
            except ValueError:
                raise RuntimeError(f"{mode}: invalid payout in LUT row {n}")
            if rid in lut_payout:
                raise RuntimeError(f"{mode}: duplicate LUT id {rid}")
            lut_payout[rid] = payout

    missing = sorted(set(book_payout) - set(lut_payout))
    extra = sorted(set(lut_payout) - set(book_payout))
    mismatch = []
    for rid in sorted(set(book_payout) & set(lut_payout)):
        if float(book_payout[rid]) != lut_payout[rid]:
            mismatch.append(rid)

    if missing or extra or mismatch:
        raise RuntimeError(
            f"{mode}: integrity failure missing={len(missing)} "
            f"extra={len(extra)} mismatches={len(mismatch)}"
        )

    if len(book_payout) < 100000:
        raise RuntimeError(f"{mode}: only {len(book_payout)} books; require >=100000")

    return {"mode": mode, "books": len(book_payout), "lut_rows": len(lut_payout)}

def main():
    if len(sys.argv) != 2:
        print("usage: verify_publication.py <publication_dir>", file=sys.stderr)
        return 2
    pub = Path(sys.argv[1]).resolve()
    if not pub.is_dir():
        print(f"not a directory: {pub}", file=sys.stderr)
        return 2

    modes = ["BASE", "BASIC", "SUPER", "MYSTERY"]
    results = [verify_mode(pub, m) for m in modes]
    print(json.dumps({"status": "PASS", "modes": results}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
