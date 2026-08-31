#!/usr/bin/env python3
"""Harvest arXiv metadata into papers.sqlite.

Two modes:
  --since yesterday        OAI-PMH nightly harvest (daily ingest)
  --query "..."            targeted search API query (math-scout only)

arXiv rate limits: one request per three seconds, single connection.
Both modes respect this. Do not parallelize; 429s have been aggressive
since early 2026 and a ban costs more than a slow harvest.
"""

import argparse, sqlite3, time, sys, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path

DB = Path(__file__).parent / "papers.sqlite"
OAI = "http://export.arxiv.org/oai2"
API = "http://export.arxiv.org/api/query"
DELAY = 3.1                      # seconds between requests; do not lower
UA = "research-net/0.1 (mailto:robinpdanko@gmail.com)"

# Dict order is routing precedence: eval_triage.py's _infer_domain() (and
# run_triage.py, which reuses it) walks SETS and assigns a paper to the FIRST
# domain whose category list intersects its own. So the most specific domain
# has to come first, or a broader list downstream steals its papers before it
# ever gets a look. See EVAL-01-FINDINGS.md sec4A for the eval run that caught
# this -- under the old order (compbio_mechanism last, behind compbio_methods'
# cs.LG), that domain received 2 of 180 labelled papers, essentially every
# protein/sequence paper having been claimed by cs.LG first.
SETS = {
    # Moved to front, was last. A q-bio cross-list is the cheapest available
    # proxy for compbio_methods.md sec1's own routing test -- "would this
    # method still be worth keeping if the word 'biology' were deleted from
    # the abstract? If the biology is load-bearing, it is compbio_mechanism's."
    # q-bio.SC added per charters/compbio_mechanism.md sec 6/8 (matches the
    # pathway/mechanism scope; its earlier omission looked like an oversight).
    # q-bio.PE added -- popgen/phylogenetics theory admitted per that
    # charter's sec 8 decision. Expect q-bio.PE to be noisy: most of its
    # daily volume is phylogenetics tooling and applied popgen results,
    # both still out of scope -- the charter's sec 3/7 criteria and the
    # [popgen-phylo-theory] flag do the filtering, not this category list.
    "compbio_mechanism":  ["q-bio.BM", "q-bio.QM", "q-bio.MN", "q-bio.SC", "q-bio.PE"],
    "stats":            ["stat.ME", "stat.TH", "stat.AP", "stat.CO", "math.ST"],
    # stat.ML kept here deliberately (probability.md sec8's pass-3 addition,
    # re-confirmed after EVAL-01-FINDINGS.md sec4A/ruling on 2 labelled papers
    # -- both real probability-theory content: identifiability, convergence
    # guarantees -- that would otherwise fall through to compbio_methods).
    "probability":      ["math.PR", "math.DS", "math.ST", "stat.ML"],
    # Split from a single "compbio" set -- see charters/compbio_methods.md and
    # charters/compbio_mechanism.md for why. Category lists are a draft, same
    # as the charters; verify against a week of live triage.
    # math.NA added: charters/compbio_methods.md sec2 already claims "numerical
    # methods and matrix algorithms where the contribution is the method", but
    # no domain listed the category, so such papers had no route in at all.
    # cs.NE contributed 0 of 180 labelled papers -- kept anyway, sec3's
    # benchmark-only-metaheuristic rule is written against that literature and
    # a 2-week labelled window is not evidence of its absence.
    "compbio_methods":    ["math.OC", "cs.LG", "cs.NE", "stat.ML", "math.NA"],
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
  arxiv_id   TEXT PRIMARY KEY,
  title      TEXT NOT NULL,
  abstract   TEXT NOT NULL,
  categories TEXT NOT NULL,
  authors    TEXT,
  published  TEXT,
  updated    TEXT,
  status     TEXT NOT NULL DEFAULT 'new',
  domain     TEXT,
  triage_score INTEGER,
  triage_reason TEXT,
  fetched_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_status ON papers(status);
CREATE INDEX IF NOT EXISTS idx_domain ON papers(domain, status);
"""


def db():
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)
    return con


def fetch(url):
    """Single rate-limited request. Retries once on 429 with a long backoff."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                time.sleep(DELAY)
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 1:
                sys.stderr.write("429 from arXiv; backing off 120s\n")
                time.sleep(120)
                continue
            raise
    raise RuntimeError("unreachable")


def upsert(con, rows):
    """Insert only. Existing arxiv_ids are left alone -- never reset status,
    or a paper already carded gets reprocessed and you pay twice."""
    n = 0
    for r in rows:
        cur = con.execute(
            "INSERT OR IGNORE INTO papers "
            "(arxiv_id,title,abstract,categories,authors,published,updated,fetched_at) "
            "VALUES (?,?,?,?,?,?,?,datetime('now'))", r)
        n += cur.rowcount
    con.commit()
    return n


def harvest_oai(con, frm, until):
    """OAI-PMH is the sanctioned bulk path. Resumption-token paginated."""
    ns = {"o": "http://www.openarchives.org/OAI/2.0/",
          "a": "http://arxiv.org/OAI/arXivRaw/"}
    wanted = {c for cats in SETS.values() for c in cats}
    params = {"verb": "ListRecords", "metadataPrefix": "arXivRaw",
              "from": frm, "until": until}
    total = 0
    while True:
        xml = fetch(f"{OAI}?{urllib.parse.urlencode(params)}")
        root = ET.fromstring(xml)
        rows = []
        for rec in root.findall(".//o:record", ns):
            m = rec.find(".//a:arXivRaw", ns)
            if m is None:
                continue
            cats = (m.findtext("a:categories", "", ns) or "").split()
            if not wanted.intersection(cats):
                continue
            rows.append((
                m.findtext("a:id", "", ns),
                " ".join((m.findtext("a:title", "", ns) or "").split()),
                " ".join((m.findtext("a:abstract", "", ns) or "").split()),
                " ".join(cats),
                m.findtext("a:authors", "", ns),
                frm, until,
            ))
        total += upsert(con, rows)
        tok = root.findtext(".//o:resumptionToken", "", ns)
        if not tok:
            break
        params = {"verb": "ListRecords", "resumptionToken": tok}
    return total


def search(con, query, categories, maxr):
    """Targeted search. math-scout only -- never call this in a loop over
    a list of IDs; that is what the OAI harvest is for."""
    ns = {"e": "http://www.w3.org/2005/Atom"}
    cat = " OR ".join(f"cat:{c}" for c in categories.split(","))
    q = f"({query}) AND ({cat})"
    url = f"{API}?{urllib.parse.urlencode({'search_query': q, 'max_results': maxr, 'sortBy': 'relevance'})}"
    root = ET.fromstring(fetch(url))
    rows = []
    for e in root.findall("e:entry", ns):
        aid = (e.findtext("e:id", "", ns) or "").rsplit("/", 1)[-1]
        rows.append((
            aid,
            " ".join((e.findtext("e:title", "", ns) or "").split()),
            " ".join((e.findtext("e:summary", "", ns) or "").split()),
            " ".join(c.get("term") for c in e.findall("e:category", ns)),
            ", ".join(a.findtext("e:name", "", ns) for a in e.findall("e:author", ns)),
            e.findtext("e:published", "", ns),
            e.findtext("e:updated", "", ns),
        ))
    added = upsert(con, rows)
    for r in rows:
        print(f"{r[0]}\t{r[1][:90]}")
    return added


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--since")
    p.add_argument("--query")
    p.add_argument("--categories", default="math.PR,math.OC,math.FA,math.DG,math.NA")
    p.add_argument("--max", type=int, default=8)
    a = p.parse_args()

    # Guard added 2026-08-28. The other three network-facing scripts
    # (canon_harvest.py, citation_overlap.py, verify_citations.py) have always
    # refused to run with a placeholder address; this one did not, and it is the
    # highest-volume caller in the system -- the 5,275-row 2026-08-24 harvest went
    # out through it anonymously. arXiv and OpenAlex both rate-limit anonymous
    # callers harder, and per README.md that matters most for the citation gate: a
    # 429 mid-scan looks exactly like a fabricated citation, which is the one
    # confusion invariant 17 must never make.
    if "YOUR_EMAIL_HERE" in UA:
        sys.exit("Set your email in UA at the top of this file. arXiv rate-limits "
                 "anonymous callers harder, and this script is the bulk harvester.")

    con = db()
    if a.query:
        n = search(con, a.query, a.categories, a.max)
    elif a.since:
        until = date.today().isoformat()
        frm = (date.today() - timedelta(days=1)).isoformat() \
            if a.since == "yesterday" else a.since
        n = harvest_oai(con, frm, until)
    else:
        p.error("need --since or --query")

    print(f"added {n} new papers", file=sys.stderr)
    # Non-zero exit on an empty daily harvest: arXiv publishes every weekday,
    # so zero new papers means something broke silently. The skill halts on this.
    if a.since and n == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
