#!/usr/bin/env python3
"""Applies triage predictions to papers.sqlite. Database only -- no dispatch.

    apply_triage.py apply                  # predictions.jsonl -> papers.sqlite
    apply_triage.py apply --dry-run        # print the transitions, write nothing
    apply_triage.py status                 # what the database currently holds

The second half of the missing link. `run_triage.py collect` writes
eval/predictions.jsonl; nothing read it. Until this file existed, the `domain`
column was null on every row, the ambiguous tier was inert, and
coalition_audit.py sections 3 and 6 printed "not measurable" rather than a number.

WHY THIS DOES NOT DISPATCH CURATORS
daily-ingest.md already splits triage (section 2, ending in this script) from
curation (section 3, dispatched by the skill). Keeping that split is not
tidiness. run_triage.py's docstring gives the reason at length: no script in
this repo shells out to an agent, the invocation for dispatching a named
subagent non-interactively cannot be verified from inside a sandbox, and a
plausible-looking command that fails on first contact is worse than none. The
deterministic part belongs in Python where it can be tested; the model-facing
part belongs in the skill where a human is watching. A version of this script
that dispatched curators would be untestable in exactly the half that matters.

THREE LITERAL-STRING CONTRACTS, ALL LOAD-BEARING
Downstream tooling reads triage_reason as text, so the exact bytes matter:

1. `wildcard` -- coalition_audit.wildcard_return() selects
   `triage_reason LIKE '%wildcard%'`. That is its only handle on the quota.
   Written as the suffix ` [wildcard]`, at the END of the reason.

2. `[tag]` at the START -- coalition_audit.ambiguous_backlog() selects
   `triage_reason LIKE '[%]%'` and then applies `TAG_RE.match()`, which anchors
   at position 0. SQLite's LIKE has no character classes, so that pattern means
   a literal `[` in the first position. The bracketed tag triage.md emits at the
   head of `reason` therefore has to stay at the head: the reason is copied
   VERBATIM and the wildcard suffix goes on the end, never the front. Getting
   these two backwards makes every ambiguous flag invisible and is silent.

3. Both at once is legal and common. `[shared-sparse-estimation] ... [wildcard]`
   satisfies both queries; the tag regex stops at the first match, and the
   trailing marker cannot be mistaken for a tag because it is not at position 0.

WHY ONLY QUOTA-ADMITTED PAPERS GET THE WILDCARD MARKER
triage.md makes every far-band paper scoring >=4 emit `wildcard: true`, which is
more papers than the quota admits. coalition_audit.py prints its wildcard number
as "share of admissions ... (target ~15%)". If the marker went on every flagged
paper rather than every admitted one, that percentage would measure something
other than its own label and would sail past 15% with nothing wrong. So: flagged
is a model output, marked is an admission decision, and only the second is
written to the database.

(One imprecision inherited from the reader, worth knowing and not worth patching
from this side: wildcard_return()'s denominator is `COUNT(*) WHERE triage_score
>= 4`, which also counts far-band 4s that the quota did not admit. It will read
slightly low. Fixing it means changing that query to count `status='admitted'`,
which is coalition_audit.py's call to make, not this script's.)

DOMAIN COMES FROM THE CATEGORIES, NOT FROM THE MODEL
triage.md's output carries a `domain` field. It is ignored here, the same way
run_triage.py's collect() ignores the model's `threshold` and substitutes
prepare()'s. Domain assignment is a routing decision made by SETS in
arxiv_pull.py before the model saw the paper; letting the model's echo of it
win would mean a batch could quietly re-route itself, and the ordering
precedence in SETS -- which EVAL-01-FINDINGS.md section 4A shows is easy to get
wrong and hard to notice -- would stop being the thing that decides.

STATUS TRANSITIONS ARE ONE-WAY BY DEFAULT
Only rows at `status='new'` are transitioned. arxiv_pull.py's upsert() carries
the same rule and the same comment: never reset the status of a paper that has
already moved, or a paper already carded gets reprocessed and you pay twice.
Re-running this script over the same predictions is therefore free and safe.
--restate lifts the restriction deliberately, for the case where you have
re-run triage against a revised charter and *want* the old verdicts replaced.
"""

import argparse, json, sqlite3, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
EVAL = ROOT / "eval"
PRED = EVAL / "predictions.jsonl"
DB = ROOT / "ingest" / "papers.sqlite"

# CLAUDE.md invariant 7. Proportional, not a flat count: on a daily run of ~10
# admissions this lands at 1-2, which is what triage.md promises the model.
# Over a 180-paper eval set it scales with the set, which is the point -- a
# fixed "two per run" would silently become 1% of a large run.
WILDCARD_SHARE = 0.15

MARKER = " [wildcard]"


# ------------------------------------------------------------------ loading

def _load_predictions(path):
    if not path.exists():
        sys.exit(f"no {path} -- run `run_triage.py collect` first")
    recs, bad = [], 0
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            bad += 1
            continue
        if isinstance(o, dict) and "arxiv_id" in o:
            recs.append(o)
        else:
            bad += 1
    if bad:
        print(f"warning: {bad} unparseable lines in {path.name}")
    if not recs:
        sys.exit(f"{path} has no usable predictions")
    return recs


def _infer(categories):
    """Reuse eval_triage's inference. A third copy of SETS-walking logic would
    drift from the first two, and the ordering precedence is the whole game."""
    sys.path.insert(0, str(Path(__file__).parent))
    from eval_triage import _infer_domain
    return _infer_domain(categories)


def _fetch_rows(con, ids):
    """Everything the decision needs, in one query rather than N."""
    out = {}
    cur = con.cursor()
    for i in range(0, len(ids), 500):
        chunk = ids[i:i + 500]
        q = ",".join("?" * len(chunk))
        cur.execute(f"SELECT arxiv_id, categories, status, triage_score "
                    f"FROM papers WHERE arxiv_id IN ({q})", chunk)
        for aid, cats, status, score in cur.fetchall():
            out[aid] = {"categories": cats, "status": status, "score": score}
    return out


# ------------------------------------------------------------------ decision

def _decide(recs, rows, restate):
    """Pure. Returns (transitions, skipped, warnings) and touches no database.

    Split out so the interesting half can be reasoned about without a sqlite
    file in the way -- the same reason run_triage.py separates prepare from run.
    """
    warnings, skipped = Counter(), []
    by_domain = defaultdict(list)

    for r in recs:
        aid = r["arxiv_id"]
        row = rows.get(aid)
        if row is None:
            # Not skipped silently. The labelled set was drawn FROM this
            # database by eval_triage.sample(), so a prediction with no row is
            # a sign the two have diverged -- a re-harvest, a hand-edited
            # labels file, or the wrong run collected. Any of those changes
            # what the numbers mean.
            skipped.append((aid, "not in papers.sqlite"))
            continue
        if row["status"] != "new" and not restate:
            skipped.append((aid, f"status={row['status']!r}, not 'new'"))
            continue

        domain = _infer(row["categories"])
        if not domain:
            skipped.append((aid, f"no domain for categories {row['categories']!r}"))
            continue

        score = r.get("score")
        if not isinstance(score, int) or not 0 <= score <= 5:
            skipped.append((aid, f"score {score!r} is not an int 0-5"))
            continue

        thr = r.get("threshold")
        if not isinstance(thr, int):
            # eval_triage.ADMIT. collect() normally stamps the banded value from
            # the manifest, so reaching this means a hand-assembled predictions
            # file; say so rather than quietly applying a different rule.
            warnings["threshold missing, fell back to 4"] += 1
            thr = 4

        reason = (r.get("reason") or "").strip()
        # Substring, not the bracketed form: the audit's query is
        # LIKE '%wildcard%', so a bare "wildcard" in prose trips it too.
        if "wildcard" in reason.lower() and not r.get("wildcard"):
            # The audit's query is a substring match on 'wildcard'. A reason
            # that uses the word in prose would be counted as a quota admission
            # forever, and nothing downstream would ever say so.
            warnings["reason contains 'wildcard' but paper is not flagged"] += 1

        by_domain[domain].append({
            "arxiv_id": aid, "domain": domain, "score": score,
            "threshold": thr, "reason": reason,
            "flagged": bool(r.get("wildcard")),
            "ambiguous": bool(r.get("ambiguous")),
        })

    transitions = []
    for domain, items in sorted(by_domain.items()):
        regular = [d for d in items if d["score"] >= d["threshold"]]
        # Eligible for the quota: flagged, and would NOT get in on merit.
        # A far-band 5 is already admitted and does not consume a reserved slot.
        eligible = [d for d in items
                    if d["flagged"] and d["score"] < d["threshold"]]
        quota = max(1, round(WILDCARD_SHARE * len(regular))) if eligible else 0
        # Deterministic: score descending, then arxiv_id. The tie-break is
        # arbitrary but it is not random, so two runs over one predictions file
        # admit the same papers and a diff of the database means something.
        eligible.sort(key=lambda d: (-d["score"], d["arxiv_id"]))
        admitted_wild = {d["arxiv_id"] for d in eligible[:quota]}

        for d in items:
            wild = d["arxiv_id"] in admitted_wild
            admit = d["score"] >= d["threshold"] or wild
            # Verbatim, so a leading [tag] stays at position 0 for TAG_RE.
            # Marker appended, never prepended. See the docstring.
            d["triage_reason"] = d["reason"] + (MARKER if wild else "")
            d["status"] = "admitted" if admit else "rejected"
            d["wildcard_admitted"] = wild
            transitions.append(d)

    return transitions, skipped, warnings


# ------------------------------------------------------------------ writing

def apply(pred_path, dry_run, restate, only_domain):
    if not DB.exists():
        sys.exit(f"no {DB} -- run arxiv_pull.py first")

    recs = _load_predictions(pred_path)
    con = sqlite3.connect(DB)
    rows = _fetch_rows(con, [r["arxiv_id"] for r in recs])

    transitions, skipped, warnings = _decide(recs, rows, restate)
    if only_domain:
        transitions = [t for t in transitions if t["domain"] == only_domain]
        if not transitions:
            sys.exit(f"no transitions in domain {only_domain!r}")

    # ---- report before writing, always, dry-run or not
    print(f"predictions: {pred_path}   rows matched: {len(rows)}/{len(recs)}\n")

    per_domain = defaultdict(Counter)
    for t in transitions:
        c = per_domain[t["domain"]]
        c[t["status"]] += 1
        c["wildcard"] += t["wildcard_admitted"]
        c["ambiguous"] += t["ambiguous"]

    print(f"  {'domain':<20} {'admit':>6} {'reject':>7} {'wild':>5} {'ambig':>6}")
    for domain, c in sorted(per_domain.items()):
        print(f"  {domain:<20} {c['admitted']:>6} {c['rejected']:>7} "
              f"{c['wildcard']:>5} {c['ambiguous']:>6}")
    tot = Counter()
    for c in per_domain.values():
        tot.update(c)
    print(f"  {'TOTAL':<20} {tot['admitted']:>6} {tot['rejected']:>7} "
          f"{tot['wildcard']:>5} {tot['ambiguous']:>6}")

    if tot["admitted"]:
        share = tot["wildcard"] / tot["admitted"]
        print(f"\n  wildcard share of admissions: {share:.0%}  "
              f"(invariant 7 target ~{WILDCARD_SHARE:.0%})")

    if warnings:
        print("\n  warnings:")
        for k, v in warnings.most_common():
            print(f"    {v:>4}  {k}")

    if skipped:
        print(f"\n  {len(skipped)} predictions not applied:")
        seen = Counter(why for _, why in skipped)
        for why, n in seen.most_common(8):
            print(f"    {n:>4}  {why}")
        notin = [a for a, w in skipped if "not in papers.sqlite" in w]
        if notin:
            print(f"\n  ^ {len(notin)} predictions have no row in the database, "
                  f"e.g. {', '.join(notin[:4])}.")
            print("    The labelled set was drawn from this database, so this "
                  "means the two\n    have diverged. Check you collected the "
                  "run you think you did before\n    trusting any number above.")

    if dry_run:
        print("\n--dry-run: nothing written.")
        return

    with con:
        con.executemany(
            "UPDATE papers SET domain=?, status=?, triage_score=?, "
            "triage_reason=? WHERE arxiv_id=?",
            [(t["domain"], t["status"], t["score"], t["triage_reason"],
              t["arxiv_id"]) for t in transitions])

    print(f"\nwrote {len(transitions)} rows to {DB.relative_to(ROOT)}")
    print("\nNext: `coalition_audit.py --month` should now print numbers for "
          "sections 3 and 6\ninstead of 'not measurable'. That is the test that "
          "this worked.")


# ------------------------------------------------------------------- status

def status():
    if not DB.exists():
        sys.exit(f"no {DB}")
    con = sqlite3.connect(DB)
    cur = con.cursor()

    print("by status:")
    for st, n in cur.execute(
            "SELECT status, COUNT(*) FROM papers GROUP BY status ORDER BY 2 DESC"):
        print(f"  {st or '(null)':<16} {n:>6}")

    print("\nby domain:")
    for dom, n in cur.execute(
            "SELECT domain, COUNT(*) FROM papers GROUP BY domain ORDER BY 2 DESC"):
        print(f"  {dom or '(null)':<16} {n:>6}")

    nulls = cur.execute(
        "SELECT COUNT(*) FROM papers WHERE domain IS NULL").fetchone()[0]
    wild = cur.execute(
        "SELECT COUNT(*) FROM papers "
        "WHERE triage_reason LIKE '%wildcard%'").fetchone()[0]
    amb = cur.execute(
        "SELECT COUNT(*) FROM papers "
        "WHERE triage_reason LIKE '[%]%'").fetchone()[0]

    print(f"\n  domain null        {nulls:>6}")
    print(f"  wildcard-marked    {wild:>6}   (coalition_audit section 3 reads this)")
    print(f"  ambiguous-tagged   {amb:>6}   (section 6 reads this)")
    if not wild and not amb:
        print("\n  Both are zero. If you have run `apply` already, that is a "
              "finding, not a\n  formatting problem -- check that predictions "
              "carried `wildcard` and\n  `ambiguous` keys at all.")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        epilog="Start with: apply_triage.py apply --dry-run",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="action", required=True, metavar="{apply,status}")

    a = sub.add_parser("apply")
    a.add_argument("--predictions", default=str(PRED))
    a.add_argument("--dry-run", action="store_true")
    a.add_argument("--domain", help="restrict writes to one domain")
    a.add_argument("--restate", action="store_true",
                   help="also transition rows that have already moved off "
                        "'new'. For re-running triage against a revised "
                        "charter, when replacing the old verdicts is the point.")

    sub.add_parser("status")
    args = ap.parse_args()

    if args.action == "apply":
        apply(Path(args.predictions), args.dry_run, args.restate, args.domain)
    else:
        status()


if __name__ == "__main__":
    main()
