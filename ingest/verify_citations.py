#!/usr/bin/env python3
"""Resolve every citation this system emits. A fabricated one invalidates the artifact.

Sun et al. (2024), Humanit Soc Sci Commun 11:1278, name the failure mode
"false academic information": fictitious papers, apparently irrelevant fictitious
references, and non-existent links. Walters & Wilder (2023), which they cite,
found it throughout ChatGPT bibliographies.

This pipeline is unusually exposed to it. Two of its most consequential outputs
are citation-shaped:

    skeptic.prior_work    "arXiv:2401.xxxxx does X, which is most of this"  -> kills a bridge
    referee-novelty       "the closest work is Y, which does Z instead"     -> kills a proposal
    spec.prior_art        carried forward from the skeptic, not re-derived
    math-scout.theory_gap "math.OC has adaptive schedules with better rates since 2024"

A fabricated citation in any of them does not produce a visible error. It
produces a confident, well-reasoned, wrong judgment with a reference attached --
and a reference reads as evidence. A novelty review resting on a fabricated
"closest prior work" is worse than no novelty review, which is why a
non-resolving citation invalidates the artifact rather than being logged.

    python ingest/verify_citations.py scan                 # everything, cached
    python ingest/verify_citations.py gate reviews/b-2608-014/novelty.md
    python ingest/verify_citations.py sample --n 3         # the part scripts can't do
    python ingest/verify_citations.py report --month

WHAT THIS DOES NOT CATCH, and it is half the problem: resolution proves a paper
EXISTS. It does not prove the paper says what it was cited for. Sun et al.'s
phrase is "apparently irrelevant fictitious references" -- a real citation
attached to a claim it does not support. No script can check that. `sample`
pulls three resolved citations a week and shows you the claim beside the actual
abstract; three minutes, and it is the only coverage available.

Set MAILTO below. arXiv and OpenAlex both rate-limit anonymous callers harder,
and this script refuses to run without it -- same convention as arxiv_pull.py,
canon_harvest.py and citation_overlap.py.
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

MAILTO = ""  # <- your email. Required.

ROOT = Path(__file__).parent.parent
CACHE = ROOT / "ingest" / "citation_cache.json"
LOG = ROOT / "ledger" / "citation_failures.jsonl"
RELEVANCE = ROOT / "eval" / "citation_relevance.jsonl"

ARXIV_API = "http://export.arxiv.org/api/query?id_list="
OPENALEX_API = "https://api.openalex.org/works/"

# 2007-and-later ids (2401.01234v2) and the pre-2007 scheme (math.PR/0601001).
ARXIV_RE = re.compile(
    r"(?:arXiv:|arxiv\.org/abs/)?\b(\d{4}\.\d{4,5}(?:v\d+)?|[a-z-]+(?:\.[A-Z]{2})?/\d{7})\b",
    re.IGNORECASE,
)
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+?)(?=[\s,;\)\]\"']|$)")

# Where citations live. Each entry: glob, and the fields whose text to scan.
SOURCES = [
    ("reviews/*/skeptic.md", "skeptic"),
    ("reviews/*/novelty*.md", "referee-novelty"),
    ("reviews/*/feasibility*.md", "referee-feasibility"),
    ("reviews/*/relevance*.md", "referee-relevance"),
    ("proposals/*/spec.md", "project-architect"),
    ("proposals/*/pitch.md", "project-architect"),
]


def load_cache():
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text())
        except json.JSONDecodeError:
            print("  ! cache corrupt, starting fresh", file=sys.stderr)
    return {}


def save_cache(c):
    CACHE.write_text(json.dumps(c, indent=1, sort_keys=True))


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": f"research-net ({MAILTO})"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return None if e.code == 404 else f"__HTTP_{e.code}__"
    except Exception as e:
        return f"__ERR_{type(e).__name__}__"


def resolve_arxiv(aid):
    """Returns {'ok': bool, 'title': str} or {'transient': True}.

    arXiv asks for one request per three seconds. Respect it; a 429 here would
    look exactly like a fabricated citation, which is the one confusion this
    script must never make.
    """
    time.sleep(3)
    body = fetch(ARXIV_API + urllib.parse.quote(aid))
    if body is None:
        return {"ok": False, "reason": "404"}
    if body.startswith("__"):
        return {"transient": True, "reason": body.strip("_")}
    # A query for a nonexistent id returns a feed with zero <entry> elements.
    if "<entry>" not in body:
        return {"ok": False, "reason": "no-entry"}
    m = re.search(r"<title>(.*?)</title>", body.split("<entry>", 1)[1], re.S)
    summ = re.search(r"<summary>(.*?)</summary>", body.split("<entry>", 1)[1], re.S)
    return {
        "ok": True,
        "title": " ".join(m.group(1).split()) if m else "",
        "abstract": " ".join(summ.group(1).split())[:1200] if summ else "",
    }


def resolve_doi(doi):
    time.sleep(0.2)
    url = OPENALEX_API + "doi:" + urllib.parse.quote(doi) + f"?mailto={MAILTO}"
    body = fetch(url)
    if body is None:
        return {"ok": False, "reason": "404"}
    if body.startswith("__"):
        return {"transient": True, "reason": body.strip("_")}
    try:
        w = json.loads(body)
    except json.JSONDecodeError:
        return {"transient": True, "reason": "unparseable"}
    return {"ok": True, "title": w.get("title") or "", "abstract": ""}


def extract(text):
    """(kind, identifier, the line it appeared on) for every citation in text."""
    out = []
    for i, line in enumerate(text.splitlines()):
        for m in ARXIV_RE.finditer(line):
            out.append(("arxiv", m.group(1).lower(), line.strip()))
        for m in DOI_RE.finditer(line):
            out.append(("doi", m.group(1).rstrip(".").lower(), line.strip()))
    # De-duplicate on identifier, keeping the first context we saw it in.
    seen, uniq = set(), []
    for kind, ident, ctx in out:
        if ident not in seen:
            seen.add(ident)
            uniq.append((kind, ident, ctx))
    return uniq


def verify(items, cache, recheck_transient=True):
    """Resolve, using the cache. Transient failures are never cached as failures."""
    results = []
    for kind, ident, ctx in items:
        key = f"{kind}:{ident}"
        hit = cache.get(key)
        if hit and not (hit.get("transient") and recheck_transient):
            results.append((kind, ident, ctx, hit))
            continue
        r = resolve_arxiv(ident) if kind == "arxiv" else resolve_doi(ident)
        if not r.get("transient"):
            cache[key] = r
        results.append((kind, ident, ctx, r))
    return results


def check_file(path, agent, cache):
    text = path.read_text(errors="replace")
    items = extract(text)
    if not items:
        return []
    rows = []
    for kind, ident, ctx, r in verify(items, cache):
        rows.append({
            "file": str(path.relative_to(ROOT)),
            "agent": agent,
            "kind": kind,
            "id": ident,
            "context": ctx[:300],
            "status": "transient" if r.get("transient") else ("ok" if r.get("ok") else "MISSING"),
            "title": r.get("title", ""),
            "reason": r.get("reason", ""),
        })
    return rows


def cmd_scan(a):
    cache = load_cache()
    all_rows = []
    for glob, agent in SOURCES:
        for path in sorted(ROOT.glob(glob)):
            all_rows.extend(check_file(path, agent, cache))
    # theory_gap is free text inside the concordance and is scanned separately.
    conc = ROOT / "kb" / "concordance.jsonl"
    if conc.exists():
        for line in conc.read_text().splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            gap = row.get("theory_gap") or ""
            if not gap:
                continue
            for kind, ident, ctx, r in verify(extract(gap), cache):
                all_rows.append({
                    "file": "kb/concordance.jsonl",
                    "agent": "math-scout",
                    "object": row.get("object"),
                    "kind": kind, "id": ident, "context": ctx[:300],
                    "status": "transient" if r.get("transient") else ("ok" if r.get("ok") else "MISSING"),
                    "title": r.get("title", ""), "reason": r.get("reason", ""),
                })
    save_cache(cache)

    ok = [r for r in all_rows if r["status"] == "ok"]
    missing = [r for r in all_rows if r["status"] == "MISSING"]
    trans = [r for r in all_rows if r["status"] == "transient"]

    print(f"=== Citation scan ===\n")
    print(f"  resolved   {len(ok)}")
    print(f"  MISSING    {len(missing)}")
    print(f"  unreachable {len(trans)}  (network, not fabrication -- rerun)")

    if missing:
        print("\nFABRICATED OR WRONG -- these identifiers do not resolve:\n")
        for r in missing:
            print(f"  {r['file']}")
            print(f"    {r['kind']}:{r['id']}  ({r['reason']})")
            print(f"    context: {r['context']}")
            print()
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a") as f:
            for r in missing:
                f.write(json.dumps({**r, "date": date.today().isoformat(),
                                    "error_type": "fabricated-citation"}) + "\n")
        print(f"  logged -> {LOG.relative_to(ROOT)}")
        print("\n  Each of these invalidates its artifact. A novelty review resting")
        print("  on a citation that does not exist is worse than no novelty review:")
        print("  it is a kill decision with a reference attached, and the reference")
        print("  is what made it persuasive. Re-run the agent; do not hand-patch")
        print("  the file, or you will never see the rate.")

    if trans:
        print(f"\n  {len(trans)} unreachable. NOT counted as fabricated -- the two")
        print("  must never be confused. Re-run when the network is back.")

    return 1 if missing else 0


def cmd_gate(a):
    """Blocking check on one artifact. Non-zero exit means do not proceed."""
    path = Path(a.path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        sys.exit(f"no such file: {path}")
    cache = load_cache()
    rows = check_file(path, "gate", cache)
    save_cache(cache)
    missing = [r for r in rows if r["status"] == "MISSING"]
    trans = [r for r in rows if r["status"] == "transient"]
    print(f"{len(rows)} citation(s), {len(missing)} missing, {len(trans)} unreachable")
    for r in missing:
        print(f"  MISSING {r['kind']}:{r['id']} -- {r['context']}")
    if trans:
        print("  ! unreachable citations: gate is INCONCLUSIVE, not passed.")
        return 2
    return 1 if missing else 0


def cmd_sample(a):
    """The half no script can do: does the real paper support the claim?

    Resolution proves existence. Sun et al.'s category is 'apparently irrelevant
    fictitious references' -- a real paper cited for something it does not say.
    Three a week is not coverage. It is enough to notice a rate.
    """
    cache = load_cache()
    resolved = [(k, v) for k, v in cache.items() if v.get("ok") and v.get("title")]
    if not resolved:
        print("Nothing resolved yet. Run `scan` first.")
        return 0

    done = set()
    if RELEVANCE.exists():
        for line in RELEVANCE.read_text().splitlines():
            if line.strip():
                try:
                    done.add(json.loads(line)["id"])
                except Exception:
                    pass

    # Re-scan for context so the claim and the citation are shown together.
    contexts = {}
    for glob, agent in SOURCES:
        for path in sorted(ROOT.glob(glob)):
            for kind, ident, ctx in extract(path.read_text(errors="replace")):
                contexts.setdefault(f"{kind}:{ident}", (str(path.relative_to(ROOT)), ctx))

    pool = [(k, v) for k, v in resolved if k not in done and k in contexts]
    if not pool:
        print("No unchecked resolved citations with context. Nothing to sample.")
        return 0

    import random
    iso = date.today().isocalendar()
    pick = random.Random(f"{iso[0]}-W{iso[1]}-cite").sample(pool, min(a.n, len(pool)))

    RELEVANCE.parent.mkdir(parents=True, exist_ok=True)
    for key, meta in pick:
        src, ctx = contexts[key]
        print("\n" + "=" * 70)
        print(f"CLAIM   ({src})")
        print(f"  {ctx}")
        print(f"\nCITED   {key}")
        print(f"  {meta['title']}")
        if meta.get("abstract"):
            print(f"\n  {meta['abstract'][:700]}")
        print("=" * 70)
        print("\nDoes the cited paper support the claim it is attached to?")
        try:
            v = input("  [s]upports / [n]o / [u]nclear / [q]uit > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nstopped")
            return 0
        if v.startswith("q"):
            return 0
        verdict = {"s": "supports", "n": "does-not-support", "u": "unclear"}.get(v[:1], "unclear")
        note = ""
        if verdict == "does-not-support":
            note = input("  what does it actually say? > ").strip()
            print("\n  ^ That is a `fabricated-citation` in the second sense --")
            print("    real paper, wrong claim. It is the harder half and the")
            print("    reason this sampling exists. Consider whether the verdict")
            print("    that citation supported should be revisited.")
        with RELEVANCE.open("a") as f:
            f.write(json.dumps({
                "id": key, "date": date.today().isoformat(), "source": src,
                "claim": ctx[:300], "title": meta["title"],
                "verdict": verdict, "note": note,
            }) + "\n")
    print("\nlogged -> " + str(RELEVANCE.relative_to(ROOT)))
    return 0


def cmd_report(a):
    cutoff = (date.today() - timedelta(days=a.days)).isoformat()
    fails = []
    if LOG.exists():
        for line in LOG.read_text().splitlines():
            if line.strip():
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if r.get("date", "") >= cutoff:
                    fails.append(r)
    rel = []
    if RELEVANCE.exists():
        for line in RELEVANCE.read_text().splitlines():
            if line.strip():
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if r.get("date", "") >= cutoff:
                    rel.append(r)

    print(f"=== Citations, trailing {a.days} days ===\n")
    print(f"1. NON-RESOLVING: {len(fails)}")
    if fails:
        by_agent = {}
        for r in fails:
            by_agent[r.get("agent", "?")] = by_agent.get(r.get("agent", "?"), 0) + 1
        for k, n in sorted(by_agent.items(), key=lambda x: -x[1]):
            print(f"   {k:<20} {n}")
        print("\n   ^ Concentrated in one agent means a prompt problem, not a model")
        print("     problem. The agent citing most is usually referee-novelty,")
        print("     because it is the one under most pressure to produce a name.")
    else:
        print("   none. Note this is also what an unrun scan looks like --")
        print("   check ingest/citation_cache.json has entries.")

    print(f"\n2. RELEVANCE SPOT-CHECKS: {len(rel)}")
    if rel:
        bad = [r for r in rel if r["verdict"] == "does-not-support"]
        unclear = [r for r in rel if r["verdict"] == "unclear"]
        print(f"   supports          {len(rel) - len(bad) - len(unclear)}")
        print(f"   does not support  {len(bad)}")
        print(f"   unclear           {len(unclear)}")
        if bad:
            print("\n   Real papers cited for claims they do not make:\n")
            for r in bad:
                print(f"     {r['id']}  ({r['source']})")
                print(f"       claim: {r['claim'][:150]}")
                if r.get("note"):
                    print(f"       says:  {r['note'][:150]}")
            print("\n   ^ This rate matters more than the non-resolving rate.")
            print("     Non-resolution is caught automatically forever. This is")
            print("     caught only by you, only three a week, and it is the")
            print("     category the source paper says is most common.")
    else:
        print("   none run. `python ingest/verify_citations.py sample --n 3`")
    return 0


def main():
    if not MAILTO:
        sys.exit("Set MAILTO at the top of this file. arXiv and OpenAlex both "
                 "rate-limit anonymous callers harder, and a 429 mid-scan looks "
                 "exactly like a fabricated citation.")
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("scan").set_defaults(fn=cmd_scan)

    p = sub.add_parser("gate")
    p.add_argument("path")
    p.set_defaults(fn=cmd_gate)

    p = sub.add_parser("sample")
    p.add_argument("--n", type=int, default=3)
    p.set_defaults(fn=cmd_sample)

    p = sub.add_parser("report")
    p.add_argument("--month", action="store_true")
    p.add_argument("--days", type=int, default=30)
    p.set_defaults(fn=cmd_report)

    a = ap.parse_args()
    sys.exit(a.fn(a) or 0)


if __name__ == "__main__":
    main()
