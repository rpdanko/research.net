#!/usr/bin/env python3
"""Verify a probe's pre-registration predates its implementation.

This is the only thing standing between the probe agent and a machine that
confirms whatever it is shown. Models are extremely good at explaining
results after the fact; the pre-registration is worthless unless it is
provably prior.

Two independent checks:
  1. mtime ordering  -- preregistration.md older than probe.py and output
  2. hash match      -- the hash recorded in verdict.md matches the file now

Check 2 is the important one. mtime can be fudged; a hash recorded before
the run and compared after cannot be, without deliberate effort.

    python ingest/verify_prereg.py b-2608-014

Exit 0 clean, 1 if the verdict must be discarded.
"""

import argparse, hashlib, sys, re
from pathlib import Path

ROOT = Path(__file__).parent.parent


def sha(p):
    return "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bridge_id")
    a = ap.parse_args()

    d = ROOT / "probes" / a.bridge_id
    prereg, script, verdict = d / "preregistration.md", d / "probe.py", d / "verdict.md"

    problems = []

    for f in (prereg, verdict):
        if not f.is_file():
            problems.append(f"missing {f.name}")
    if problems:
        print("\n".join(f"FAIL {p}" for p in problems))
        sys.exit(1)

    # 1. Ordering. Equal mtimes are suspicious (a single write pass).
    if script.is_file():
        if prereg.stat().st_mtime >= script.stat().st_mtime:
            problems.append(
                "preregistration.md is not older than probe.py -- the probe was "
                "not pre-registered, or the file was edited after the run")

    if prereg.stat().st_mtime >= verdict.stat().st_mtime:
        problems.append("preregistration.md is not older than verdict.md")

    # 2. Hash. The verdict records the hash it committed to; recompute it.
    m = re.search(r"prereg_hash:\s*[\"']?(sha256:[0-9a-f]{64})", verdict.read_text())
    if not m:
        problems.append("verdict.md records no prereg_hash")
    elif m.group(1) != sha(prereg):
        problems.append(
            "prereg_hash mismatch -- preregistration.md was modified after the "
            "verdict was written. Discard this result.")

    if problems:
        for p in problems:
            print(f"FAIL {a.bridge_id}: {p}")
        print("\nAction: mark this probe 'inconclusive'. Do NOT mark it "
              "'falsified' or 'supported' -- an unverifiable probe is not evidence "
              "in either direction.")
        sys.exit(1)

    print(f"OK {a.bridge_id}: pre-registration verified")


if __name__ == "__main__":
    main()
