#!/usr/bin/env python3
"""Monthly audit of the COALITION, as opposed to the machine.

Every failure mode in research-network-architecture.md section 6 is a way the
machine goes wrong: semantic slop, schema drift, grade inflation, probe theater,
loop runaway. None of them is a way the human-plus-machine system goes wrong,
and those failures are slower, quieter, and not recoverable by re-running
anything.

Six of them are measurable from files you already have.

    python3 ingest/coalition_audit.py --month
    python3 ingest/coalition_audit.py --month --snapshot   # append to the trend

1. NARROWING. Messeri & Crockett's monoculture, operationalised. A canon-anchored
   pipeline that feeds its own output back into bridge-finder will converge on a
   shrinking set of mathematical objects, and every individual week will look
   fine while it happens. Two numbers: concentration of the concordance, and how
   much of this month's output is built from objects the system already had.

2. COUPLING. Whether anything flows from you into the machine, or only out of
   it. Measured as the share of promoted proposals traceable to an object you
   planted in kb/concordance_user.jsonl.

3. WILDCARD RETURN. 15% of admissions are reserved for papers the canon does not
   recognise (invariant 7). HANDOFF.md section 3 predicts they will be
   OVER-represented in bridges. Nothing has ever checked.

4. ENGAGEMENT. Whether the digest is being read at all. This is the deskilling
   tripwire; see HYBRID-SYSTEM-REVIEW.md 3.3.

5. FLATTERY. Whether proposals converge on objects you have already pursued --
   Sun et al.'s overfitting-to-audience-expectations failure, made countable.

6. AMBIGUOUS BACKLOG. Every charter now names specific scope patterns triage
   should flag rather than silently call (see charters/*.md section 5, added
   alongside the compbio domain split). A pattern flagged once is triage doing
   its job; the same pattern flagged every week is a charter decision you keep
   deferring instead of making.

None of these has a threshold that means "broken". They have TRENDS that mean
"look". Run with --snapshot monthly and read the last six rows, not the last one.
"""

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
LEDGER = ROOT / "ledger" / "bridges.jsonl"
VERDICTS = ROOT / "ledger" / "user_verdicts.jsonl"
CONCORDANCE = ROOT / "kb" / "concordance.jsonl"
USER_CONCORDANCE = ROOT / "kb" / "concordance_user.jsonl"
HISTORY = ROOT / "eval" / "coalition_history.jsonl"
DB = ROOT / "ingest" / "papers.sqlite"


def read_jsonl(path):
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def bridges_since(cutoff):
    latest = {}
    for row in read_jsonl(LEDGER):
        if "id" in row:
            latest[row["id"]] = {**latest.get(row["id"], {}), **row}
    return [b for b in latest.values() if b.get("created", "") >= cutoff]


# --- 1. narrowing ----------------------------------------------------------

def concentration(concordance):
    """Effective number of objects, via inverse Simpson on paper counts.

    HHI is the standard measure but it is unreadable at these magnitudes -- 0.031
    tells you nothing on its own. Its reciprocal is the number of objects the
    concordance behaves as if it had, if they were all equally weighted, and that
    is a number you can compare month to month without a reference table.

    A concordance of 200 objects with an effective count of 12 is a system that
    has quietly decided everything is optimal transport.
    """
    counts = []
    for row in concordance:
        n = sum(len(v or []) for v in (row.get("papers") or {}).values())
        if n:
            counts.append(n)
    total = sum(counts)
    if not total:
        return None, 0, 0
    hhi = sum((c / total) ** 2 for c in counts)
    return (1 / hhi if hhi else None), len(counts), total


def recycling_rate(bridges, concordance, weeks=8):
    """Share of this month's bridges built on objects the system already had."""
    cutoff = (date.today() - timedelta(weeks=weeks)).isoformat()
    old = {
        r.get("object") for r in concordance
        if r.get("first_seen", "9999") < cutoff
    }
    old |= {
        alias for r in concordance if r.get("first_seen", "9999") < cutoff
        for alias in (r.get("aliases") or [])
    }
    if not bridges:
        return None, 0
    recycled = sum(1 for b in bridges if b.get("object") in old)
    return recycled / len(bridges), recycled


# --- 2. coupling -----------------------------------------------------------

def coupling(bridges):
    planted = {r.get("object") for r in read_jsonl(USER_CONCORDANCE)}
    planted |= {
        alias for r in read_jsonl(USER_CONCORDANCE)
        for alias in (r.get("aliases") or [])
    }
    if not planted:
        return None, 0, 0
    hits = [b for b in bridges if b.get("object") in planted]
    promoted = [b for b in hits if b.get("state") == "promoted"]
    return len(planted), len(hits), len(promoted)


# --- 5. flattery -----------------------------------------------------------

def flattery(bridges):
    """Are proposals converging on the objects you have already pursued?

    Sun et al. (2024) categorise "flattery" as an overfitting failure: content
    generated to please or cater to the audience's expectations. The user-verdict
    channel gives project-architect and bridge-finder a direct signal of what the
    user valued, which is exactly the material that failure needs.

    Deliberately measured on object-name overlap rather than embeddings. Invariant
    8 bars semantic similarity from bridge-finding because similarity is not
    structural identity; the same objection does not apply to measurement, but a
    fuzzy match here would flag convergence that is really shared vocabulary, and
    that is the error this repo spends most effort avoiding elsewhere.
    """
    verdicts = read_jsonl(VERDICTS)
    pursued = {v.get("object") for v in verdicts if v.get("verdict") == "pursued"}
    pursued.discard(None)
    if not pursued or not bridges:
        return None, 0, len(pursued)
    hits = sum(1 for b in bridges if b.get("object") in pursued)
    return hits / len(bridges), hits, len(pursued)


# --- 3. wildcard -----------------------------------------------------------

def wildcard_return(bridges):
    """Requires apply_triage.py to mark wildcard admissions in the database.

    The marker is a triage_reason containing the literal string 'wildcard'. If
    nothing is marked, this returns None rather than 0 -- an unmeasured quota and
    a quota with no return are different findings and must not print the same.
    """
    if not DB.exists():
        return None, None, None
    import sqlite3

    con = sqlite3.connect(DB)
    cur = con.cursor()
    try:
        cur.execute(
            "SELECT arxiv_id FROM papers WHERE triage_reason LIKE '%wildcard%'"
        )
    except sqlite3.OperationalError:
        return None, None, None
    wild = {r[0] for r in cur.fetchall()}
    if not wild:
        return None, None, None

    cur.execute("SELECT COUNT(*) FROM papers WHERE triage_score >= 4")
    admitted = cur.fetchone()[0] or 1

    hits = 0
    for b in bridges:
        ids = set()
        for v in (b.get("source_papers") or {}).values():
            ids.update([v] if isinstance(v, str) else (v or []))
        if ids & wild:
            hits += 1
    share_admitted = len(wild) / admitted
    share_bridges = hits / len(bridges) if bridges else None
    return share_admitted, share_bridges, hits


# --- 6. ambiguous backlog ---------------------------------------------------

TAG_RE = re.compile(r"\[([a-z][a-z0-9-]*)\]")


def ambiguous_backlog():
    """Requires apply_triage.py to write '[tag]' into triage_reason whenever
    triage set ambiguous: true, per triage.md's tagging instruction.

    Unlike wildcard, there is no target rate here. The question is not "is this
    the right share" -- it is "is one named pattern recurring often enough that
    the charter should resolve it outright instead of flagging it every time".
    """
    if not DB.exists():
        return None
    import sqlite3

    con = sqlite3.connect(DB)
    cur = con.cursor()
    try:
        cur.execute("SELECT domain, triage_reason, status FROM papers "
                    "WHERE triage_reason LIKE '[%]%'")
    except sqlite3.OperationalError:
        return None
    rows = cur.fetchall()
    if not rows:
        return None

    by_tag, by_domain = Counter(), Counter()
    admitted = 0
    for domain, reason, status in rows:
        m = TAG_RE.match((reason or "").strip())
        by_tag[m.group(1) if m else "untagged"] += 1
        by_domain[domain] += 1
        if status == "admitted":
            admitted += 1
    return by_tag, by_domain, len(rows), admitted


# --- main ------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--month", action="store_true")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--snapshot", action="store_true",
                    help="append this month's row to eval/coalition_history.jsonl")
    a = ap.parse_args()

    cutoff = (date.today() - timedelta(days=a.days)).isoformat()
    concordance = read_jsonl(CONCORDANCE)
    bridges = bridges_since(cutoff)

    print(f"=== Coalition audit, trailing {a.days} days ===\n")

    if not concordance:
        print("Concordance is empty. Nothing to measure yet -- this audit becomes")
        print("meaningful around Week 6, once bridge-finder has run a few times.")
        return

    # 1
    eff, n_obj, n_links = concentration(concordance)
    rec_rate, rec_n = recycling_rate(bridges, concordance)
    print("1. NARROWING\n")
    print(f"   concordance objects        {n_obj}")
    print(f"   object->paper links        {n_links}")
    print(f"   effective objects          {eff:.1f}" if eff else "   effective objects   n/a")
    if eff and n_obj:
        print(f"   concentration ratio        {eff/n_obj:.2f}  (1.0 = perfectly even)")
        if eff / n_obj < 0.25:
            print("\n   ^ LOOK: the concordance behaves as if it had a quarter of the")
            print("     objects it lists. A few objects carry everything. That is not")
            print("     automatically wrong -- optimal transport really is everywhere --")
            print("     but check the trend. If the ratio is falling month over month,")
            print("     the system is narrowing and the wildcard quota is not enough.")
    if rec_rate is not None:
        print(f"\n   bridges this period        {len(bridges)}")
        print(f"   built on objects >8wk old  {rec_n} ({rec_rate:.0%})")
        if rec_rate > 0.8:
            print("\n   ^ LOOK: over 80% of bridges recycle objects the system already")
            print("     had. Rising recycling means it is eating its own tail: the KB")
            print("     feeds bridge-finder, bridge-finder's survivors shape what you")
            print("     read, what you read shapes the charters, and the charters")
            print("     decide what enters the KB. Check the wildcard number below.")
    print()

    # 2
    print("2. COUPLING\n")
    planted, hits, promoted = coupling(bridges)
    if planted is None:
        print("   kb/concordance_user.jsonl is empty.")
        print("   Nothing has ever flowed from you into the machine's central data")
        print("   structure. That is the definition of a tool rather than an")
        print("   extension, and it is fine for now -- but if it is still empty in")
        print("   three months, either you have nothing to add (unlikely) or the")
        print("   file is not in your way at the moment you would use it.")
    else:
        print(f"   objects you planted        {planted}")
        print(f"   bridges using one          {hits}")
        print(f"   of those, promoted         {promoted}")
        if hits == 0:
            print("\n   ^ You have planted objects and none produced a bridge. Worth")
            print("     knowing which: either math-scout would have found them anyway")
            print("     (check first_seen in the main concordance) or bridge-finder is")
            print("     not reading the merged view. The second is a bug.")
    print()

    # 3
    print("3. WILDCARD RETURN\n")
    sa, sb, hits_w = wildcard_return(bridges)
    if sa is None:
        print("   Not measurable: no admissions are marked as wildcard in the")
        print("   database. apply_triage.py must write 'wildcard' into")
        print("   triage_reason for quota admissions. Until it does, invariant 7")
        print("   is an unverified belief -- the quota may be costing $0.02/day and")
        print("   returning nothing, and there is currently no way to tell.")
    else:
        print(f"   share of admissions        {sa:.0%}   (target ~15%)")
        print(f"   share of bridges           {sb:.0%}   ({hits_w} bridges)"
              if sb is not None else "   share of bridges           n/a")
        if sb is not None and sb < sa:
            print("\n   ^ LOOK: wildcards are UNDER-represented in bridges. HANDOFF.md")
            print("     section 3 predicts the opposite. Either the prediction was")
            print("     wrong -- worth writing down -- or wildcard papers are being")
            print("     admitted and then not carded, which is a pipeline bug rather")
            print("     than a finding.")
    print()

    # 4
    print("4. ENGAGEMENT\n")
    verdicts = [v for v in read_jsonl(VERDICTS) if v.get("date", "") >= cutoff]
    promoted_ct = sum(1 for b in bridges if b.get("state") == "promoted")
    if not verdicts:
        print(f"   {promoted_ct} proposals promoted, 0 verdicts logged.")
        print("   The loop is open. Nothing this system produced has been judged by")
        print("   the only judge that matters, which means the referee gate's")
        print("   agreement rate is unmeasurable and its credibility is frozen at")
        print("   whatever you concluded in Week 9.")
        print("\n   python3 ingest/log_verdict.py pending")
    else:
        unread = sum(1 for v in verdicts if not v.get("read"))
        vc = Counter(v.get("verdict") for v in verdicts)
        print(f"   promoted                   {promoted_ct}")
        print(f"   verdicts logged            {len(verdicts)}")
        print(f"   unread                     {unread} ({unread/len(verdicts):.0%})")
        print("   " + "  ".join(f"{k}={n}" for k, n in vc.most_common()))
        if unread > len(verdicts) / 2:
            print("\n   ^ LOOK: most promoted proposals go unread. Raise the promote")
            print("     bar to mean >= 4.0 (costs nothing, cuts to ~1/week) before")
            print("     concluding the proposals are bad. An unread digest is the")
            print("     failure this whole layer exists to catch.")

    # 5
    print("5. FLATTERY\n")
    flat_share, flat_n, pursued_n = flattery(bridges)
    if flat_share is None:
        print("   Not measurable yet: nothing logged as 'pursued'.")
        print("   Becomes meaningful once you have pursued 3-4 proposals.")
    else:
        print(f"   objects you have pursued    {pursued_n}")
        print(f"   this period's bridges on one of them   {flat_n} ({flat_share:.0%})")
        if flat_share > 0.5:
            print("\n   ^ LOOK: over half of this period's bridges are built on objects")
            print("     you have already pursued. `flattery` in rubrics/ERROR-TYPES.md")
            print("     -- generating content that caters to the audience's expectations.")
            print("     The verdict file exists so project-architect learns what you")
            print("     valued; read one way that closes a loop, read another it is a")
            print("     training signal for telling you what you want to hear. Both")
            print("     agent prompts forbid optimising against it, and a prompt is")
            print("     not an enforcement mechanism. Check the near-misses in the")
            print("     digest: if the kills are also concentrated on your objects,")
            print("     the narrowing is upstream in bridge-finder, not here.")
    print()

    # 6
    print("6. AMBIGUOUS BACKLOG\n")
    amb = ambiguous_backlog()
    top_tag = top_n = amb_total = amb_admitted = None
    if amb is None:
        print("   Not measurable: no records marked with a bracketed tag in")
        print("   triage_reason. apply_triage.py must write it -- see the Known")
        print("   gaps table in HANDOFF.md. Until it does, the charters' Ambiguous")
        print("   sections are unread signal.")
    else:
        by_tag, by_domain, amb_total, amb_admitted = amb
        print(f"   total flagged              {amb_total}   (admitted: {amb_admitted})")
        print("   by domain: " + "  ".join(f"{d}={n}" for d, n in by_domain.most_common()))
        print("   by pattern:")
        for tag, n in by_tag.most_common():
            print(f"     {tag:<32} {n:>3}")
        top_tag, top_n = by_tag.most_common(1)[0]
        if top_n / amb_total > 0.4:
            print(f"\n   ^ LOOK: '{top_tag}' is {top_n}/{amb_total} of all ambiguous flags.")
            print("     A pattern this concentrated isn't ambiguous anymore -- it's a")
            print("     charter decision you keep deferring. Resolve it explicitly in")
            print("     the charter (in scope, out of scope, or its own line item)")
            print("     rather than flagging the same call every day.")
    print()

    if a.snapshot:
        HISTORY.parent.mkdir(parents=True, exist_ok=True)
        row = {
            "flattery_share": round(flat_share, 3) if flat_share is not None else None,
            "date": date.today().isoformat(),
            "objects": n_obj,
            "effective_objects": round(eff, 2) if eff else None,
            "concentration_ratio": round(eff / n_obj, 3) if eff and n_obj else None,
            "bridges": len(bridges),
            "recycling_rate": round(rec_rate, 3) if rec_rate is not None else None,
            "planted_objects": planted,
            "planted_bridges": hits,
            "wildcard_share_admitted": round(sa, 3) if sa is not None else None,
            "wildcard_share_bridges": round(sb, 3) if sb is not None else None,
            "promoted": promoted_ct,
            "verdicts": len(verdicts),
            "ambiguous_total": amb_total,
            "ambiguous_top_tag": top_tag,
            "ambiguous_top_share": round(top_n / amb_total, 3) if top_n and amb_total else None,
        }
        with HISTORY.open("a") as f:
            f.write(json.dumps(row) + "\n")
        print(f"\nsnapshot appended -> {HISTORY.relative_to(ROOT)}")
        hist = read_jsonl(HISTORY)
        if len(hist) >= 3:
            # `x or '-'` would print a dash for a legitimate 0.0, which is exactly
            # the value you most want to see in the recycling and wildcard columns.
            def cell(v, w):
                return f"{'-' if v is None else v:>{w}}"

            print("\nTREND (read this, not the single month above)\n")
            print(f"   {'date':<12} {'eff.obj':>8} {'ratio':>7} {'recycl':>7} "
                  f"{'wild':>6} {'ambig':>6} {'top tag':<28}")
            for h in hist[-6:]:
                print(f"   {h['date']:<12} "
                      f"{cell(h.get('effective_objects'), 8)} "
                      f"{cell(h.get('concentration_ratio'), 7)} "
                      f"{cell(h.get('recycling_rate'), 7)} "
                      f"{cell(h.get('wildcard_share_bridges'), 6)} "
                      f"{cell(h.get('ambiguous_total'), 6)} "
                      f"{cell(h.get('ambiguous_top_tag'), 28)}")


if __name__ == "__main__":
    main()
