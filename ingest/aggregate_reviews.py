#!/usr/bin/env python3
"""Aggregate referee verdicts into a gate decision.

The gate runs on the BINARY reject verdicts. The 1-5 scores are advisory --
used for ranking survivors and for detecting drift, never for deciding.
Binary judgments from LLM judges track human agreement more reliably than
five-point ones; fine-grained scales invite distinctions the judge cannot
defend.

Deliberately not an agent. Asking a model to "weigh the reviews" reintroduces
exactly the anchoring the split-axis referees exist to prevent.

    python ingest/aggregate_reviews.py b-2608-014
"""

import argparse, json, sys, statistics
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml")

ROOT = Path(__file__).parent.parent
PROCEED_MEAN = 3.5
AXES = {"feasibility", "relevance", "novelty"}


def load_reviews(bid):
    d = ROOT / "reviews" / bid
    if not d.is_dir():
        sys.exit(f"no reviews directory for {bid}")
    out = []
    for f in sorted(d.glob("*.md")):
        if f.stem == "skeptic":
            continue
        m = f.read_text().split("---")
        raw = m[1] if f.read_text().startswith("---") and len(m) > 2 else f.read_text()
        try:
            r = yaml.safe_load(raw)
        except yaml.YAMLError as e:
            sys.exit(f"{f}: unparseable ({e})")
        if not isinstance(r, dict) or "reject" not in r or "axis" not in r:
            sys.exit(f"{f}: missing required 'axis' or 'reject' field")
        r["_file"] = f.name
        out.append(r)
    return out


def normalize(v):
    """Accept yes/no, true/false, y/n. Anything else is an error, not a guess."""
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    if s in ("yes", "true", "y"):
        return True
    if s in ("no", "false", "n"):
        return False
    sys.exit(f"uninterpretable reject value: {v!r}")


def decide(reviews):
    covered = {r["axis"] for r in reviews}
    missing = AXES - covered
    if missing:
        return {"decision": "error",
                "reason": f"missing axes: {', '.join(sorted(missing))}"}

    vetoes = [r for r in reviews if normalize(r["reject"])]
    if vetoes:
        return {
            "decision": "kill",
            "reason": "referee veto",
            "vetoed_by": [f"{r['axis']}/{r.get('domain', '-')}" for r in vetoes],
            "objections": [r.get("strongest_objection", "").strip() for r in vetoes],
        }

    scores = [float(r["score"]) for r in reviews if r.get("score") is not None]
    mean = statistics.mean(scores) if scores else 0.0

    return {
        "decision": "probe" if mean >= PROCEED_MEAN else "revise",
        "reason": f"no vetoes; mean {mean:.2f} {'>=' if mean >= PROCEED_MEAN else '<'} {PROCEED_MEAN}",
        "mean_score": round(mean, 2),
        "by_axis": {r["axis"]: r.get("score") for r in reviews},
        # Weakest axis drives a revision, so name it for the architect.
        "weakest_axis": min((r for r in reviews if r.get("score") is not None),
                            key=lambda r: float(r["score"]), default={}).get("axis"),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("bridge_id")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    result = decide(load_reviews(a.bridge_id))
    result["bridge_id"] = a.bridge_id

    if a.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{a.bridge_id}: {result['decision'].upper()} -- {result['reason']}")
        for k in ("vetoed_by", "by_axis", "weakest_axis"):
            if k in result:
                print(f"  {k}: {result[k]}")

    sys.exit(2 if result["decision"] == "error" else 0)


if __name__ == "__main__":
    main()
