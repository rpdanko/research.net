#!/usr/bin/env python3
"""One-off cleanup for eval/labels.jsonl. Run once, after the session that
found two problems with the file as it stood at 180 labelled rows:

1. Every row has "domain": null. arxiv_pull.py's harvest never sets domain
   -- that's apply_triage.py's job, and apply_triage.py doesn't exist yet
   (see DAY-5-HANDOFF.md SS4). Left uncorrected, sample()'s canon-similarity
   banding and calibrate()'s NEAR/FAR suggestion were both silently
   comparing every candidate against the WHOLE pooled canon (~8,300 papers
   across all four domains) instead of just its own domain's slice
   (~2,000), which dilutes exactly the separation calibrate() exists to
   measure. eval_triage.py now infers domain from categories at read time
   (see _infer_domain there), which fixes calibrate() going forward without
   needing this file changed -- but the stored null is still worth
   backfilling so the file is self-describing and any other tool reading it
   later doesn't hit the same trap.

2. label()'s stratum prompt has always said "[in/out/borderline]", but
   every other place in the codebase (sample(), score_run(), this
   project's own docs) uses "expect_in"/"expect_out"/"borderline". Every
   row in the file was typed by hand against that prompt, so `stratum` is a
   mix of "in", "out", "In", "Borderline", a typo ("borderlinne"), and one
   value ("pit") that doesn't map to anything. This normalizes what it can
   and prints what it can't for manual review -- it does not guess at "pit".

Usage:  python ingest/fixup_labels_stratum_domain.py
Writes eval/labels.jsonl in place. eval/labels.jsonl.bak keeps the
pre-fix copy -- diff against it if anything looks wrong afterward.
"""
import json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
LABELS = ROOT / "eval" / "labels.jsonl"

sys.path.insert(0, str(Path(__file__).parent))
from arxiv_pull import SETS


def infer_domain(categories):
    cats = set((categories or "").split())
    for domain, wanted in SETS.items():
        if cats & set(wanted):
            return domain
    return None


def normalize_stratum(raw):
    s = (raw or "").strip().lower()
    if s.startswith("in"):
        return "expect_in"
    if s.startswith("out"):
        return "expect_out"
    if s.startswith("bord"):
        return "borderline"
    return None   # unrecognized -- caller leaves it alone and flags it


def main():
    if not LABELS.exists():
        sys.exit(f"no {LABELS}")
    recs = [json.loads(l) for l in LABELS.read_text().splitlines() if l.strip()]

    backup = LABELS.with_suffix(".jsonl.bak")
    shutil.copy(LABELS, backup)
    print(f"backed up to {backup}")

    domain_fixed = stratum_fixed = 0
    unresolved = []
    for r in recs:
        if not r.get("domain"):
            inferred = infer_domain(r.get("categories"))
            if inferred:
                r["domain"] = inferred
                domain_fixed += 1

        new_stratum = normalize_stratum(r["stratum"])
        if new_stratum and new_stratum != r["stratum"]:
            r["stratum"] = new_stratum
            stratum_fixed += 1
        elif not new_stratum:
            unresolved.append((r["arxiv_id"], r["stratum"], r["title"][:70]))

    LABELS.write_text("".join(json.dumps(r) + "\n" for r in recs))

    print(f"domain backfilled:   {domain_fixed}/{len(recs)}")
    print(f"stratum normalized:  {stratum_fixed}/{len(recs)}")
    if unresolved:
        print(f"\n{len(unresolved)} row(s) with an unrecognized stratum -- fix these by hand "
              f"in eval/labels.jsonl (the file is JSON-lines; open in any editor):")
        for aid, strat, title in unresolved:
            print(f"  {aid}  stratum={strat!r}  {title}")
    else:
        print("\nno unresolved rows.")


if __name__ == "__main__":
    main()
