#!/usr/bin/env python3
"""Enforce the revision round cap and the per-bridge spend ceiling.

The review loop is the only cycle in an otherwise acyclic pipeline, and
cycles are where token budgets die. The cap lives here, in code, because an
instruction in an agent prompt saying "revise at most twice" is not a cap.

    python ingest/check_round_cap.py b-2608-014

Exit 0 -> may revise (prints the incremented round)
Exit 3 -> shelve; caller must not dispatch project-architect
"""

import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
LEDGER = ROOT / "ledger" / "bridges.jsonl"

MAX_ROUND = 2
MAX_SPEND_USD = 2.00


def read_entry(bid):
    """Last line wins -- the ledger is append-only, so later entries supersede."""
    entry = None
    for line in LEDGER.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("id") == bid:
            entry = rec
    if entry is None:
        sys.exit(f"no ledger entry for {bid}")
    return entry


def append(rec):
    with LEDGER.open("a") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bridge_id")
    ap.add_argument("--commit", action="store_true",
                    help="write the state transition, not just report it")
    a = ap.parse_args()

    e = read_entry(a.bridge_id)
    rnd = int(e.get("round", 0))
    spend = float(e.get("cumulative_usd", 0.0))

    if rnd >= MAX_ROUND:
        print(f"SHELVE {a.bridge_id}: round {rnd} >= cap {MAX_ROUND}")
        print("  No exceptions. If the idea is genuinely good it will resurface")
        print("  from bridge-finder when new papers change the picture.")
        if a.commit:
            append({**e, "state": "shelved", "shelve_reason": "round-cap"})
        sys.exit(3)

    if spend >= MAX_SPEND_USD:
        print(f"SHELVE {a.bridge_id}: spend ${spend:.2f} >= cap ${MAX_SPEND_USD:.2f}")
        if a.commit:
            append({**e, "state": "shelved", "shelve_reason": "spend-cap"})
        sys.exit(3)

    nxt = rnd + 1
    print(f"OK {a.bridge_id}: round {rnd} -> {nxt} (spend ${spend:.2f})")
    if a.commit:
        append({**e, "state": "revising", "round": nxt})


if __name__ == "__main__":
    main()
