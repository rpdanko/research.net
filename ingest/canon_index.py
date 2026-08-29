#!/usr/bin/env python3
"""Local embedding index over the canon, and similarity scoring for new papers.

    canon_index.py build                    # embed the canon (once, ~1 min)
    canon_index.py score --abstract-file f  # band a new paper
    canon_index.py exemplars --domain stats # render the Tier 0 prompt block

Runs entirely locally on sentence-transformers. Zero API cost, ~6000 abstracts
in under a minute on a laptop.

WHY EMBEDDINGS HERE AND NOT IN BRIDGE-FINDING
The architecture doc argues against a vector store, and that argument stands
where it was made: for INTERSECTION-FINDING, semantic similarity surfaces
exactly the "both papers mention entropy" slop the skeptic exists to kill,
because similarity is not structural identity. For RELEVANCE TRIAGE, semantic
similarity to things we already trust IS the question being asked. Same tool,
different job. Keep it on this side of the line.

WHAT THE MODEL SEES
Not the cosine. A model handed "0.83" anchors on the number; a model shown
"the closest things in our canon are these three papers" reasons about them.
The score becomes a threshold shift, and the titles become context.
"""

import argparse, json, re, sys
from collections import defaultdict
from pathlib import Path

try:
    import numpy as np
except ImportError:
    sys.exit("pip install numpy")

ROOT = Path(__file__).parent.parent
CANON = ROOT / "canon"
INDEX = CANON / "index.npz"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Calibrate these on your own labelled set in week 1 -- the defaults are a
# starting point, not a finding. eval_triage.py --calibrate suggests values.
NEAR, FAR = 0.62, 0.38
TOP_K = 5


def load_model():
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        sys.exit("pip install sentence-transformers")
    return SentenceTransformer(MODEL_NAME)


def canon_records():
    f = CANON / "canon.jsonl"
    if not f.exists():
        sys.exit("no canon.jsonl -- run canon_harvest.py harvest first")
    return [json.loads(l) for l in f.read_text().splitlines() if l.strip()]


def build():
    recs = [r for r in canon_records() if r.get("abstract")]
    if not recs:
        sys.exit("canon has no abstracts")

    model = load_model()
    texts = [f"{r['title']}. {r['abstract'][:1200]}" for r in recs]
    print(f"embedding {len(texts):,} canon abstracts with {MODEL_NAME}...")
    emb = model.encode(texts, batch_size=64, show_progress_bar=True,
                       normalize_embeddings=True)

    np.savez_compressed(
        INDEX,
        emb=emb.astype("float32"),
        ids=np.array([r["openalex_id"] for r in recs]),
        titles=np.array([r["title"][:200] for r in recs]),
        domains=np.array([r["domain"] for r in recs]),
        tiers=np.array([r.get("tier", 2) for r in recs]),
        # Recorded so a model swap cannot silently invalidate every stored score.
        model=np.array([MODEL_NAME]),
        dim=np.array([emb.shape[1]]),
    )
    print(f"wrote {INDEX}  ({emb.shape[0]:,} x {emb.shape[1]})")


def load_index():
    if not INDEX.exists():
        sys.exit("no index -- run canon_index.py build")
    z = np.load(INDEX, allow_pickle=False)
    if str(z["model"][0]) != MODEL_NAME:
        sys.exit(f"index built with {z['model'][0]} but MODEL_NAME is now "
                 f"{MODEL_NAME}. Every stored similarity is invalid. Rebuild.")
    return z


def score(text, domain=None):
    z = load_index()
    model = load_model()
    q = model.encode([text], normalize_embeddings=True)[0]

    emb, mask = z["emb"], np.ones(len(z["ids"]), bool)
    if domain:
        mask = z["domains"] == domain

    sims = emb[mask] @ q
    idx = np.argsort(-sims)[:TOP_K]
    top = [{"id": str(z["ids"][mask][i]),
            "title": str(z["titles"][mask][i]),
            "domain": str(z["domains"][mask][i]),
            "tier": int(z["tiers"][mask][i]),
            "sim": round(float(sims[i]), 4)} for i in idx]

    mean = float(np.mean([t["sim"] for t in top]))
    band = "near" if mean >= NEAR else ("far" if mean < FAR else "mid")

    # The threshold shift IS the fusion rule. Not a weighted model -- a shift
    # you can read in the log and argue with.
    return {
        "band": band,
        "mean_top_k": round(mean, 4),
        "threshold": {"near": 3, "mid": 4, "far": 5}[band],
        "wildcard_eligible": band == "far",
        "neighbours": top,
    }


def exemplars(domain, limit=25, neg_limit=10):
    """Render the Tier 0 prompt block: positives, then the negative exemplars.

    The struck papers do more work than the kept ones. They are what stops the
    model admitting on topical adjacency, which is the main way triage fails.

    STRIKE REASONS OUTLIVE THE CHARTER THAT PRODUCED THEM
    Exemplars are frozen at the moment of vetting; charters get revised. When a
    later pass overturns a strike reason -- e.g. pass 4 of stats.md admitting
    meta-analytic methodology against an earlier "I don't do metaanalysis"
    strike -- the frozen reason keeps getting rendered into the triage prompt
    and keeps winning, because triage.md tells the model the negative block
    "matters more" than the positives. EVAL-01-FINDINGS.md sec4B caught this
    live: a network meta-analysis paper you scored 4 was rejected by triage
    citing that exact exemplar by name, after the charter had already been
    revised to admit it.
    triage.md now carries a precedence rule (charter beats a contradicting
    exemplar) as the primary fix. This is the belt-and-braces backup: a canon
    record marked strike_superseded=true is dropped from the negative block
    entirely, so an overruled judgment can stop appearing in the prompt at all
    rather than relying on the model correctly resolving the contradiction
    every time. The vetting record itself is untouched -- strike_reason stays
    exactly as originally written; this only changes what gets rendered here.

    NEGATIVE SELECTION USED TO BE THE FIRST 6 IN FILE ORDER -- FIXED HERE
    canon.jsonl is written sorted by cited_by_count descending (canon_harvest.py).
    A flat `[:6]` slice over that order does not sample "highly cited and
    topically adjacent" strikes, it samples the single most-cited strikes,
    unconditionally -- and for stats those are CONSORT 2010, TIDieR, an ICC
    reporting guide, the Cochrane risk-of-bias tool, a discussion paper, and
    "False-Positive Psychology". Every one of them is a reporting-guideline or
    meta-science strike. None is the "tied to a single setting/dataset" (A4)
    pattern, despite ~45 such strikes existing in canon/vetting-stats.md --
    none of them are cited highly enough to survive a top-6-by-citation cut.
    stats.md sec7 tells the MODEL "citation count is not scope evidence"; the
    old version of this function let citation count decide which traps the
    model ever saw, silently, on every run, for every domain that shares this
    function. Confirmed live: 2608.20406 and 2504.09854 both cleared triage
    for exactly the pattern the negative block had zero examples of.

    Fix: bucket struck records by a coarse reason pattern first, then take the
    highest-cited record from each bucket in turn (round-robin) before any
    bucket gets a second pick. This guarantees pattern diversity -- in
    particular, a setting-specific strike is no longer structurally
    impossible to select -- while still preferring the most-cited record
    within whatever it does select, so the "highly cited" framing stays true
    of the output rather than just the input it was drawn from.
    """
    recs = canon_records()
    pos = [r for r in recs if r["domain"] == domain and r.get("tier") == 0][:limit]
    neg_pool = [r for r in recs if r["domain"] == domain
                and r.get("vetted") == "struck" and r.get("strike_reason")
                and not r.get("strike_superseded")]
    neg = _diversify(neg_pool, neg_limit)

    if not pos:
        sys.exit(f"no tier-0 exemplars for {domain} -- mark some with `*` in "
                 f"canon/vetting-{domain}.md, then run canon_tier.py apply")

    out = [f"## In scope — {len(pos)} exemplars from the canon\n"]
    for r in pos:
        out.append(f"- **{r['title']}** ({r['year']}) — {r.get('why', 'IN SCOPE: add a one-line reason')}")

    if neg:
        out.append(f"\n## Out of scope — near misses\n")
        out.append("_Highly cited and topically adjacent. These are the traps._\n")
        for r in neg:
            out.append(f"- **{r['title']}** ({r['year']}) — OUT: {r['strike_reason']}")
    else:
        out.append("\n_No negative exemplars recorded. Add strike reasons in the "
                   "vetting worksheets — they matter more than the positives._")

    print("\n".join(out))


# Coarse, deliberately generic pattern buckets -- these are English keyword
# groups over free-text strike reasons and titles, not a domain-specific
# taxonomy. They exist to break the citation-count monopoly above, not to
# model any one charter's section numbering.
#
# REPORTING-GUIDELINE IS CHECKED FIRST, AGAINST TITLE AS WELL AS REASON --
# and that ordering is itself a fix, found by reading the actual output of
# the first version of this function. GRADE ("Specific to recommendations")
# and ROBINS-I ("Specific to experimental design") both landed in
# setting-specific under reason-only matching, because a "Specific to X"
# one-liner is what this project's vetting habit produces for almost any
# strike, guideline tools included -- and both are so highly cited they then
# won that bucket's top slots outright, crowding out the low/mid-citation
# genuine single-population strikes (Danish registry, migration, cohort
# studies, sepsis...) the bucket exists to surface. Their TITLES say what
# they actually are ("GRADE: ... rating quality of evidence", "ROBINS-I: a
# tool for assessing risk of bias") even where the reason field doesn't.
# Checking title first, and checking it before setting-specific gets a turn,
# is what keeps a guideline tool from masquerading as an A4 exemplar just
# because its one-line strike reason happened to start with "Specific to".
GUIDELINE_ACRONYMS = re.compile(
    r"\b(CONSORT|PRISMA|ARRIVE|STROBE|TRIPOD|ROBINS|GRADE|SPIRIT|TIDieR|MMAT)\b")
GUIDELINE_TITLE_PHRASES = ("checklist", "guideline", "tool for assessing",
                           "reporting guideline", "consensus statement")

_REASON_BUCKETS = [
    ("review-or-rudimentary", ("rudimentary", "tutorial", "review", "guide",
                               "expository", "not a methods paper")),
    ("meta-analysis", ("meta-analysis", "metaanalysis", "meta analysis")),
    ("software", ("software", "package", "implementation", "announcement")),
    ("setting-specific", ("specific to", "tied to", "particular to")),
]


def _bucket(record):
    title = record.get("title") or ""
    title_l = title.lower()
    reason = (record.get("strike_reason") or "").strip().lower()

    if (GUIDELINE_ACRONYMS.search(title)
            or any(p in title_l for p in GUIDELINE_TITLE_PHRASES)
            or any(k in reason for k in
                   ("report", "checklist", "guideline", "consensus"))):
        return "reporting-guideline"

    # Generic software-tool title pattern, checked after the guideline check
    # above (so "a tool for assessing risk of bias" -- an appraisal
    # instrument -- still resolves to reporting-guideline first) and before
    # the reason-text loop below. Found via RAxML: title "a tool for
    # phylogenetic analysis...", reason "specific to application" -- the
    # reason alone put it in setting-specific, crowding out a genuine
    # disease-specific near-miss, even though compbio_mechanism.md sec3 names
    # RAxML by name as tooling in the same breath as SAMtools and BWA. Manual
    # vetting reasons default to "specific to X" for almost any strike, tool
    # papers included, so title is the only reliable signal for this pattern.
    if "tool for" in title_l or "toolkit" in title_l:
        return "software"

    for name, keywords in _REASON_BUCKETS:
        if any(k in reason for k in keywords):
            return name
    return "other"


def _diversify(pool, n):
    """Round-robin across reason buckets, highest cited_by_count first within
    each bucket, so no single bucket can crowd out the rest the way citation
    order alone did. Deterministic: ties broken by openalex_id."""
    buckets = defaultdict(list)
    for r in pool:
        buckets[_bucket(r)].append(r)
    for recs in buckets.values():
        recs.sort(key=lambda r: (-r.get("cited_by_count", 0), r.get("openalex_id", "")))

    order = sorted(buckets, key=lambda b: (b == "other", -len(buckets[b])))
    out, i = [], 0
    while len(out) < n and any(buckets[b] for b in order):
        b = order[i % len(order)]
        if buckets[b]:
            out.append(buckets[b].pop(0))
        i += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    s = sub.add_parser("score")
    s.add_argument("--abstract-file")
    s.add_argument("--text")
    s.add_argument("--domain")
    e = sub.add_parser("exemplars")
    e.add_argument("--domain", required=True)
    a = ap.parse_args()

    if a.cmd == "build":
        build()
    elif a.cmd == "score":
        text = Path(a.abstract_file).read_text() if a.abstract_file else a.text
        if not text:
            sys.exit("need --abstract-file or --text")
        print(json.dumps(score(text, a.domain), indent=2))
    else:
        exemplars(a.domain)


if __name__ == "__main__":
    main()
