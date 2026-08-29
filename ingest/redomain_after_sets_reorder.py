#!/usr/bin/env python3
"""One-off: recompute eval/labels.jsonl's domain field against the CURRENT
SETS in arxiv_pull.py, forcibly, ignoring whatever domain is already stored.

Why this exists and fixup_labels_stratum_domain.py doesn't cover it:
that script only backfills domain when the field is empty ("if not
r.get('domain')"). It ran once, correctly, against the SETS order that
existed then. Since then this session reordered SETS -- compbio_mechanism
moved to the front so a q-bio cross-list wins before cs.LG claims the
paper, and math.NA was added to compbio_methods (see arxiv_pull.py's
comment on SETS for the full reasoning). Every row's stored domain is now
whatever the OLD order produced, and a plain re-run of the backfill script
changes nothing, because the field is no longer empty.

This matters concretely: PASS-4-DRAFTS.md's two proposed compbio_methods
changes (the applied-ML-systems exclusion, evidenced by ~90 rejections,
and the property-not-result clause, evidenced by 17 pure-cs.LG admits)
were counted against the stale routing. Before promoting either change,
those counts need to be re-derived against the routing that will actually
be live.

Usage:  python ingest/redomain_after_sets_reorder.py
Writes eval/labels.jsonl in place. Backs up to
eval/labels.jsonl.pre-redomain.bak first (kept separate from the earlier
.bak so both cleanup steps stay individually reversible). Prints every row
whose domain changed, and the before/after per-domain counts.
"""
import json, shutil, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent
LABELS = ROOT / "eval" / "labels.jsonl"

sys.path.insert(0, str(Path(__file__).parent))
from arxiv_pull import SETS


def infer_domain(categories):
    cats = set((categories or "").split())
    for domain, wanted in SETS.items():   # dict order IS precedence
        if cats & set(wanted):
            return domain
    return None


def main():
    if not LABELS.exists():
        sys.exit(f"no {LABELS}")
    recs = [json.loads(l) for l in LABELS.read_text().splitlines() if l.strip()]

    backup = LABELS.parent / "labels.jsonl.pre-redomain.bak"
    shutil.copy(LABELS, backup)
    print(f"backed up to {backup}\n")

    before = Counter(r.get("domain") for r in recs)
    changed = []
    for r in recs:
        old = r.get("domain")
        new = infer_domain(r.get("categories"))
        if new != old:
            changed.append((r["arxiv_id"], old, new, r["title"][:60]))
            r["domain"] = new

    LABELS.write_text("".join(json.dumps(r) + "\n" for r in recs))
    after = Counter(r.get("domain") for r in recs)

    print(f"{len(changed)} row(s) changed domain:\n")
    for aid, old, new, title in changed:
        print(f"  {aid}  {old!r:>18} -> {new!r:<18}  {title}")

    print(f"\nbefore: {dict(before)}")
    print(f"after:  {dict(after)}")

    unresolved = [r["arxiv_id"] for r in recs if not r.get("domain")]
    if unresolved:
        print(f"\n{len(unresolved)} row(s) still have no domain -- their categories "
              f"match nothing in SETS. This is the same gap OPEN-QUESTIONS.md's "
              f"domain-map coverage item flagged; these rows are silently unscoreable "
              f"until SETS or domain_map.yaml is widened: {', '.join(unresolved[:10])}")


if __name__ == "__main__":
    main()
