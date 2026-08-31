#!/usr/bin/env python3
"""Five raw abstracts for the weekly digest. Unranked, uncarded, unsummarised.

This is not an information channel. It is calibration maintenance, and it is the
only defence in the repo against the human half of the loop degrading.

The argument, in full, because it is the least obvious thing here: the capacity
this system offloads is *noticing a cross-domain connection in raw abstracts*.
That same capacity is what you draw on to maintain charters/ and rubrics/ -- the
two files that must be in your handwriting and that everything downstream
inherits. If the pipeline works, you stop reading abstracts; if you stop reading
abstracts, your ability to maintain the two files it depends on decays quietly
and nothing in review_audit.py would ever show it. Clark's GPS case is benign
because wayfinding is not a prerequisite for maintaining GPS. Here it is.

So: five abstracts a week, raw, no card, no score, no agent between you and the
text. Two minutes.

    python3 ingest/raw_sample.py --n 5                  # for the digest
    python3 ingest/raw_sample.py --band nearmiss        # live triage audit
    python3 ingest/raw_sample.py --band mixed --n 6     # both, unlabelled

BANDS

  unused    (default) Admitted by triage, carded, and then used by nothing --
            no bridge cites the paper, no concordance object lists it. These are
            the system's own blind spot: it thought they mattered and then did
            nothing with them.
  nearmiss  Scored 3 by triage and therefore rejected, one point under the bar.
            Reading these is the cheapest standing audit of the charter that
            exists. A good paper here is a charter gap with an ID attached.
  mixed     Both, shuffled, and deliberately NOT labelled with which is which.
            Use this one once you have been reading the other two for a month:
            if you cannot tell an admitted paper from a rejected one, that is
            information about the triage bar and it is worth more than a
            comfortable week.

Deterministically seeded on the ISO week, so re-running the digest gives the
same five papers rather than letting you reroll until the sample looks boring.
"""

import argparse
import json
import random
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
DB = ROOT / "ingest" / "papers.sqlite"
LEDGER = ROOT / "ledger" / "bridges.jsonl"
CONCORDANCE = ROOT / "kb" / "concordance.jsonl"


def used_ids():
    """Every arxiv_id that anything downstream actually touched."""
    used = set()
    for path in (LEDGER,):
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            for v in (row.get("source_papers") or {}).values():
                if isinstance(v, str):
                    used.add(v)
                elif isinstance(v, list):
                    used.update(v)
    if CONCORDANCE.exists():
        for line in CONCORDANCE.read_text().splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            for ids in (row.get("papers") or {}).values():
                used.update(ids or [])
    return used


def query(con, band, days):
    cur = con.cursor()
    if band == "nearmiss":
        cur.execute(
            """SELECT arxiv_id, title, abstract, categories, domain, triage_score,
                      triage_reason
               FROM papers
               WHERE triage_score = 3
                 AND julianday('now') - julianday(fetched_at) <= ?""",
            (days,),
        )
        return [dict(zip([c[0] for c in cur.description], r)) for r in cur.fetchall()]

    cur.execute(
        """SELECT arxiv_id, title, abstract, categories, domain, triage_score,
                  triage_reason
           FROM papers
           WHERE triage_score >= 4
             AND julianday('now') - julianday(fetched_at) <= ?""",
        (days,),
    )
    rows = [dict(zip([c[0] for c in cur.description], r)) for r in cur.fetchall()]
    used = used_ids()
    return [r for r in rows if r["arxiv_id"] not in used]


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--band", choices=("unused", "nearmiss", "mixed"), default="unused")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if not DB.exists():
        sys.exit(f"no database at {DB}")
    con = sqlite3.connect(DB)

    if a.band == "mixed":
        pool = query(con, "unused", a.days) + query(con, "nearmiss", a.days)
    else:
        pool = query(con, a.band, a.days)

    if not pool:
        print(f"(no papers in the '{a.band}' band this week)")
        if a.band == "unused":
            print("# Nothing admitted went unused. Either a very tight week or the")
            print("# 'used' join is broken -- check that ledger source_papers ids")
            print("# match the arxiv_id format in the database.")
        return

    iso = date.today().isocalendar()
    rng = random.Random(f"{iso[0]}-W{iso[1]}-{a.band}")
    pick = rng.sample(pool, min(a.n, len(pool)))

    if a.json:
        print(json.dumps(pick, indent=2))
        return

    label = {
        "unused": "Admitted, carded, and used by nothing",
        "nearmiss": "Scored 3 -- rejected, one point under the bar",
        "mixed": "Mixed admitted and rejected, unlabelled on purpose",
    }[a.band]
    print(f"## Raw abstracts -- {label}\n")
    print("_No card, no score shown, no agent in between. Read them. If one is")
    print("obviously good or obviously wrong for this system, that is a charter")
    print("edit, and it is the cheapest one you will ever get._\n")

    for p in pick:
        print(f"### {p['title'].strip()}")
        print(f"`{p['arxiv_id']}` · {p['categories']}"
              + (f" · {p['domain']}" if p.get("domain") and a.band != "mixed" else ""))
        print()
        print(" ".join((p["abstract"] or "").split()))
        print()

    if a.band != "mixed":
        print(f"<!-- pool: {len(pool)} papers in band '{a.band}' over {a.days} days -->")


if __name__ == "__main__":
    main()
