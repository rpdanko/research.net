#!/usr/bin/env python3
"""Harvest a canon of influential papers from OpenAlex.

Two subcommands:

    canon_harvest.py resolve      # discover subfield/topic IDs, write a starter map
    canon_harvest.py harvest      # pull the canon using canon/domain_map.yaml

WHY A FIXED QUOTA PER YEAR
Raw citation counts across a 25-year window are useless -- a 2003 paper beats a
2023 paper on volume alone and the canon becomes a museum. Two defences, both
used here:
  1. Sort on citation_normalized_percentile, which OpenAlex normalizes by work
     type, publication year AND subfield.
  2. Take a fixed quota PER YEAR, so recent work cannot be crowded out.

WHY TOPIC-LEVEL DOMAIN ASSIGNMENT
OpenAlex puts statistics and probability in ONE subfield. This system needs them
apart, so domains are assigned from a topic map you edit. Run `resolve` first.
"""

import argparse, json, sys, time, urllib.parse, urllib.request
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml")

ROOT = Path(__file__).parent.parent
CANON = ROOT / "canon"
API = "https://api.openalex.org"

# OpenAlex asks for a contact address and service is more reliable with it.
MAILTO = "robinpdanko@gmail.com"

DELAY = 0.15
PER_YEAR = 80
YEAR_FROM, YEAR_TO = 2000, 2025

# Seed names for `resolve`. Edit freely -- these are search terms, not IDs.
SUBFIELD_HINTS = {
    "stats":       ["Statistics and Probability", "Statistics, Probability and Uncertainty"],
    "probability": ["Statistics and Probability"],
    "compbio":     ["Computational Theory and Mathematics", "Molecular Biology",
                    "Genetics", "Computational Mathematics", "Bioengineering"],
}


def get(path, **params):
    params["mailto"] = MAILTO
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                time.sleep(DELAY)
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            # 403 = slow down. 429 = daily limit exhausted; no point retrying.
            if e.code == 403:
                wait = 10 * (attempt + 1)
                sys.stderr.write(f"403 from OpenAlex, backing off {wait}s\n")
                time.sleep(wait)
                continue
            if e.code == 429:
                sys.exit("429: OpenAlex daily limit exhausted. Resume tomorrow; "
                         "the harvest is idempotent and will skip what it has.")
            raise
    sys.exit("repeated 403s from OpenAlex; stopping")


# ---------------------------------------------------------------- resolve

def resolve():
    """Print candidate subfields and their busiest topics, and write a starter map.

    This is the first real decision of Week 1. The generated map is a guess;
    editing it is a charter expressed in numbers and is worth an hour.
    """
    CANON.mkdir(exist_ok=True)
    out, seen = {}, set()

    for domain, hints in SUBFIELD_HINTS.items():
        print(f"\n{'='*70}\n{domain.upper()}\n{'='*70}")
        topics = []
        for hint in hints:
            data = get("subfields", search=hint, per_page=5)
            for sf in data.get("results", []):
                sid = sf["id"].rsplit("/", 1)[-1]
                if (domain, sid) in seen:
                    continue
                seen.add((domain, sid))
                print(f"\n  subfield {sid}  {sf['display_name']}  "
                      f"({sf.get('works_count', 0):,} works)")

                t = get("topics", filter=f"subfield.id:{sid}",
                        per_page=25, sort="works_count:desc")
                for topic in t.get("results", []):
                    tid = topic["id"].rsplit("/", 1)[-1]
                    print(f"      {tid:<10} {topic['display_name'][:55]:<55} "
                          f"{topic.get('works_count', 0):>9,}")
                    topics.append(tid)
        out[domain] = {"topics": topics, "subfields": []}

    p = CANON / "domain_map.generated.yaml"
    p.write_text(yaml.safe_dump(out, sort_keys=False))
    print(f"\n\nWrote {p}")
    print("""
NEXT STEP -- do not skip this:

  1. Copy it:  cp canon/domain_map.generated.yaml canon/domain_map.yaml
  2. Edit it. The generated map is over-broad by design.

     - Statistics and Probability is ONE OpenAlex subfield. Split it yourself:
       inference/estimation/design topics -> stats
       stochastic processes/random matrices/limit theorems -> probability
     - Strike topics that are adjacent but not yours. A topic with millions of
       works is almost certainly too broad to be useful.
     - 8-20 topics per domain is a healthy map. Sixty is not a map, it is a net.
""")


# ---------------------------------------------------------------- harvest

def harvest(resume):
    mapping = yaml.safe_load((CANON / "domain_map.yaml").read_text())
    outfile = CANON / "canon.jsonl"

    done = set()
    if resume and outfile.exists():
        for line in outfile.read_text().splitlines():
            if line.strip():
                rec = json.loads(line)
                done.add((rec["domain"], rec["year"]))
        print(f"resuming: {len(done)} domain-years already harvested")

    fh = outfile.open("a" if resume else "w")
    counts = Counter()

    for domain, spec in mapping.items():
        clauses = []
        if spec.get("topics"):
            clauses.append("topics.id:" + "|".join(spec["topics"]))
        if spec.get("subfields"):
            clauses.append("topics.subfield.id:" + "|".join(str(s) for s in spec["subfields"]))
        if not clauses:
            sys.exit(f"{domain}: domain_map.yaml has neither topics nor subfields")

        for year in range(YEAR_FROM, YEAR_TO + 1):
            if (domain, year) in done:
                continue

            filt = ",".join(clauses + [
                f"publication_year:{year}",
                "type:article",
                "has_abstract:true",
            ])
            # Sort on raw counts WITHIN a single year -- the year is already
            # fixed, so age bias cannot operate, and raw counts are less noisy
            # than percentile at the top of the distribution.
            data = get("works", filter=filt, per_page=PER_YEAR,
                       sort="cited_by_count:desc",
                       select="id,doi,title,publication_year,cited_by_count,"
                              "citation_normalized_percentile,authorships,"
                              "primary_location,abstract_inverted_index,"
                              "referenced_works,topics,type")

            for w in data.get("results", []):
                rec = {
                    "openalex_id": w["id"].rsplit("/", 1)[-1],
                    "doi": w.get("doi"),
                    "arxiv_id": _arxiv_id(w),
                    "title": w.get("title") or "",
                    "abstract": _abstract(w.get("abstract_inverted_index")),
                    "year": year,
                    "domain": domain,
                    "cited_by_count": w.get("cited_by_count", 0),
                    "norm_percentile": (w.get("citation_normalized_percentile") or {}).get("value"),
                    "authors": [a["author"]["display_name"]
                                for a in (w.get("authorships") or [])[:12]],
                    "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                    "topics": [t["id"].rsplit("/", 1)[-1] for t in (w.get("topics") or [])],
                    "referenced_works": [r.rsplit("/", 1)[-1]
                                         for r in (w.get("referenced_works") or [])],
                    "tier": 2,
                    "vetted": None,
                }
                fh.write(json.dumps(rec) + "\n")
                counts[domain] += 1

            fh.flush()
            print(f"  {domain:<12} {year}  {len(data.get('results', [])):>3} works", flush=True)

    fh.close()
    print("\n" + "=" * 50)
    for d, n in counts.items():
        print(f"{d:<14} {n:>6,}")
    print(f"{'TOTAL':<14} {sum(counts.values()):>6,}")
    print(f"\nWrote {outfile}\nNext: python3 ingest/canon_tier.py --stats")


def _abstract(inv):
    """OpenAlex stores abstracts as an inverted index. Reconstruct."""
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def _arxiv_id(w):
    loc = w.get("primary_location") or {}
    url = (loc.get("landing_page_url") or "") + " " + (loc.get("pdf_url") or "")
    if "arxiv.org" in url:
        for part in url.replace("/", " ").split():
            if part.replace(".", "").replace("v", "").isdigit() and "." in part:
                return part
    return None


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("resolve")
    h = sub.add_parser("harvest")
    h.add_argument("--resume", action="store_true",
                   help="skip domain-years already in canon.jsonl")
    a = ap.parse_args()

    if MAILTO == "YOUR_EMAIL_HERE":
        sys.exit("Set MAILTO at the top of this file to your email address first.")

    resolve() if a.cmd == "resolve" else harvest(a.resume)


if __name__ == "__main__":
    main()
