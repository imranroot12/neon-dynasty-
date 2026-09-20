#!/usr/bin/env python3
"""Strict preflight for Stake Engine static math publication files.

Validates index.json references, CSV columns, JSONL(.zst) presence, and
cross-file IDs/payouts when readable. It never generates or modifies math.
"""

from pathlib import Path
import csv, json, sys, gzip

def read_jsonl(path):
    op = gzip.open if path.suffix == ".gz" else open
    with op(path, "rt", encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                yield n, json.loads(line)
            except Exception as e:
                raise RuntimeError(f"{path.name}:{n}: invalid JSON: {e}")

def main():
    if len(sys.argv) != 2:
        print("usage: engine_publication_preflight.py <publication_dir>", file=sys.stderr)
        return 2

    pub = Path(sys.argv[1]).resolve()
    index = pub / "index.json"
    if not index.is_file():
        raise SystemExit("FAIL: index.json missing")

    data = json.loads(index.read_text(encoding="utf-8"))
    modes = data.get("modes")
    if not isinstance(modes, list) or not modes:
        raise SystemExit("FAIL: index.json must contain a non-empty modes array")

    results = []
    for mode in modes:
        for key in ("name", "cost", "events", "weights"):
            if key not in mode:
                raise SystemExit(f"FAIL: mode missing {key}: {mode}")

        events = pub / mode["events"]
        weights = pub / mode["weights"]
        if not events.is_file():
            raise SystemExit(f"FAIL: missing events file for {mode['name']}: {events.name}")
        if not weights.is_file():
            raise SystemExit(f"FAIL: missing weights file for {mode['name']}: {weights.name}")

        # CSV must have ID, probability/weight, payout.
        rows = []
        with weights.open(newline="", encoding="utf-8") as f:
            for n, row in enumerate(csv.reader(f), 1):
                if not row:
                    continue
                if n == 1 and row[0].strip().lower() in {"id", "simulationid", "simulation_id"}:
                    continue
                if len(row) < 3:
                    raise SystemExit(f"FAIL: {weights.name}:{n}: expected ID, probability, payout")
                try:
                    int(row[0])
                    float(row[1])
                    payout = float(row[2])
                except ValueError:
                    raise SystemExit(f"FAIL: {weights.name}:{n}: invalid numeric field")
                rows.append((str(int(row[0])), payout))

        ids = [x[0] for x in rows]
        if len(ids) != len(set(ids)):
            raise SystemExit(f"FAIL: duplicate simulation ID in {weights.name}")

        result = {
            "mode": mode["name"],
            "cost": mode["cost"],
            "events": events.name,
            "weights": weights.name,
            "lookup_rows": len(rows),
        }

        # JSONL can be inspected directly; zstd requires the Engine runtime's zstd tool.
        if events.suffix == ".zst":
            result["event_crosscheck"] = "deferred_to_zstd_capable_engine_runtime"
        else:
            event_ids = {}
            for line_no, book in read_jsonl(events):
                if not isinstance(book, dict) or "id" not in book or "payoutMultiplier" not in book:
                    raise SystemExit(f"FAIL: {events.name}:{line_no}: missing id/payoutMultiplier")
                event_ids[str(book["id"])] = float(book["payoutMultiplier"])
            if set(event_ids) != set(ids):
                raise SystemExit(f"FAIL: ID set mismatch for {mode['name']}")
            for sid, payout in rows:
                if event_ids[sid] != payout:
                    raise SystemExit(f"FAIL: payout mismatch for simulation {sid} in {mode['name']}")
            result["event_crosscheck"] = "PASS"

        results.append(result)

    print(json.dumps({"status": "PASS", "modes": results}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
