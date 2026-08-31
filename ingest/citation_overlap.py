#!/usr/bin/env python3
"""Citation overlap against the canon -- the LAGGED corrector.

    citation_overlap.py --audit --lag-days 14

READ THIS BEFORE WIRING IT INTO ANYTHING LIVE

Citing two or more canon papers is a strong in-scope signal and nearly free.
But OpenAlex needs days to weeks to index a new arXiv preprint and extract its
reference list. On the day a paper appears the signal is usually ABSENT -- and
absence is not evidence of no overlap.

A prefilter that reads missing reference data as zero overlap would silently
penalise the newest papers, which are the entire point of a streaming system.
So this does NOT gate the live decision. It runs on a lag and reports where the
citation signal DISAGREES with what triage decided a fortnight ago.

Those disagreements are the best charter-tuning material you will get. A paper
triage rejected that turns out to cite five canon works is a charter gap with a
name on it.
"""

import argparse, json, sqlite3, sys, time, urllib.parse, urllib.request
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
CANON = ROOT / "canon"
DB = ROOT / "ingest" / "papers.sqlite"
API = "https://api.openalex.org"
MAILTO = "robinpdanko@gmail.com"

STRONG = 2      # canon references at or above this = strong in-scope signal


def get(path, **params):
    params["mailto"] = MAILTO
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            time.sleep(0.15)
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        if e.code == 429:
            sys.exit("429: OpenAlex daily limit exhausted")
        raise


def canon_ids_by_domain():
    f = CANON / "canon.jsonl"
    out = {}
    for line in f.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        out.setdefault(r["domain"], set()).add(r["openalex_id"])
    return out


def refs_for(arxiv_id):
    """Returns a set of OpenAlex IDs, or None if the work is not indexed yet.

    None and empty-set are DIFFERENT and must not be collapsed. None means we
    do not know; empty means we know there is no overlap.
    """
    data = get("works", filter=f"ids.openalex:null,doi:10.48550/arxiv.{arxiv_id}",
               select="id,referenced_works", per_page=1)
    if not data or not data.get("results"):
        data = get("works", search=arxiv_id, select="id,referenced_works", per_page=1)
    if not data or not data.get("results"):
        return None
    w = data["results"][0]
    if "referenced_works" not in w:
        return None
    return {r.rsplit("/", 1)[-1] for r in (w.get("referenced_works") or [])}


def audit(lag_days, limit):
    canon = canon_ids_by_domain()
    con = sqlite3.connect(DB)
    cutoff = (date.today() - timedelta(days=lag_days)).isoformat()

    rows = con.execute(
        "SELECT arxiv_id, domain, status, triage_score, triage_reason, title "
        "FROM papers WHERE fetched_at <= ? AND triage_score IS NOT NULL "
        "ORDER BY fetched_at DESC LIMIT ?", (cutoff, limit)).fetchall()

    if not rows:
        sys.exit(f"no triaged papers older than {lag_days} days yet")

    tally = Counter()
    disagreements = []

    for aid, domain, status, score, reason, title in rows:
        refs = refs_for(aid)
        if refs is None:
            tally["not-indexed"] += 1
            continue

        overlap = refs & canon.get(domain, set())
        n = len(overlap)
        tally["checked"] += 1

        admitted = status in ("admitted", "carded")

        if n >= STRONG and not admitted:
            tally["missed"] += 1
            disagreements.append(("MISSED", aid, domain, score, n, title, reason))
        elif n == 0 and admitted and score is not None and score >= 4:
            tally["loose"] += 1
            disagreements.append(("LOOSE", aid, domain, score, n, title, reason))
        else:
            tally["agree"] += 1

    print(f"=== Citation-overlap audit, {lag_days}-day lag ===\n")
    print(f"  checked      {tally['checked']}")
    print(f"  not indexed  {tally['not-indexed']}  (no signal -- NOT a zero)")
    print(f"  agree        {tally['agree']}")
    print(f"  MISSED       {tally['missed']}  rejected but cites >= {STRONG} canon works")
    print(f"  loose        {tally['loose']}  admitted but cites no canon work\n")

    if tally["not-indexed"] > tally["checked"]:
        print("  ^ More than half not indexed. Raise --lag-days; OpenAlex has not")
        print("    caught up. Do NOT read this as a coverage failure.\n")

    for kind, aid, domain, score, n, title, reason in disagreements[:40]:
        print(f"[{kind}] {aid} {domain} score={score} canon_refs={n}")
        print(f"        {title[:88]}")
        print(f"        triage said: {reason}\n")

    if tally["missed"]:
        print("MISSED papers are your charter gaps. Read the triage reasons above:")
        print("they will cluster, and the cluster names the thing your charter")
        print("does not describe. Fix the charter, not the individual verdicts.")
    if tally["loose"] and not tally["missed"]:
        print("Only LOOSE disagreements. That is the cheap error -- a wrongly")
        print("admitted paper costs ~$0.03 and gets filtered downstream. Do not")
        print("tighten the charter to fix it; you will buy precision with recall.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true", required=True)
    ap.add_argument("--lag-days", type=int, default=14)
    ap.add_argument("--limit", type=int, default=200)
    a = ap.parse_args()
    if MAILTO == "YOUR_EMAIL_HERE":
        sys.exit("Set MAILTO to your email first.")
    audit(a.lag_days, a.limit)


if __name__ == "__main__":
    main()
