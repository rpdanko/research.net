#!/usr/bin/env python3
"""Assign canon tiers and emit vetting worksheets.

    canon_tier.py --stats       # year histogram and museum check -- run this first
    canon_tier.py nominate      # rank within domain, emit Day 2/3 worksheets
    canon_tier.py apply         # read back your marked worksheets

TIERS
  2  shell     ~2000/domain   title-skim only   citation overlap, similarity
  1  core       150/domain    abstracts read    charter derivation, similarity
  0  exemplars   25/domain    hand-picked       the triage PROMPT

Tier 0 is a subset of 1, which is a subset of 2. One file, one flag.

The struck papers matter more than the kept ones. A strike reason is a negative
exemplar and negative exemplars stop the model admitting on topical adjacency,
which is the main triage failure. Write the reason.
"""

import argparse, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
CANON = ROOT / "canon"
FILE = CANON / "canon.jsonl"

# Patterns that flag the papers a citation-count harvest reliably gets wrong.
# Advisory only -- they pre-sort your worksheet, they do not decide anything.
SUSPECT = [
    (re.compile(r"\b(software|package|toolkit|toolbox|pipeline|web server|"
                r"database|resource|platform|suite)\b", re.I), "tool"),
    (re.compile(r"\b(review|survey|perspective|overview|primer|tutorial|"
                r"introduction to)\b", re.I), "review"),
    (re.compile(r"\b(benchmark|comparison of|comparative (study|analysis|"
                r"evaluation)|assessment of)\b", re.I), "benchmark"),
    (re.compile(r"\b(consortium|atlas|catalogue|catalog|compendium)\b", re.I), "resource"),
]


def load():
    return [json.loads(l) for l in FILE.read_text().splitlines() if l.strip()]


def save(recs):
    FILE.write_text("".join(json.dumps(r) + "\n" for r in recs))


def flag(rec):
    hay = f"{rec['title']} {rec.get('abstract','')[:400]}"
    return [lab for pat, lab in SUSPECT if pat.search(hay)]


def stats(recs):
    by_domain = defaultdict(list)
    for r in recs:
        by_domain[r["domain"]].append(r)

    for domain, rs in sorted(by_domain.items()):
        years = Counter(r["year"] for r in rs)
        print(f"\n{domain}  n={len(rs):,}")
        lo, hi = min(years), max(years)
        peak = max(years.values())
        for y in range(lo, hi + 1):
            n = years.get(y, 0)
            print(f"  {y}  {'#' * int(40 * n / peak):<40} {n:>4}")

        # The museum check. A per-year quota should make this flat; if the
        # recent years are thin, the topic filter is missing new work.
        recent = sum(years.get(y, 0) for y in range(hi - 2, hi + 1)) / 3
        older = sum(years.get(y, 0) for y in range(lo, lo + 3)) / 3
        if older and recent < 0.6 * older:
            print(f"  ^ WARNING: last 3 years average {recent:.0f}/yr vs "
                  f"{older:.0f}/yr at the start.")
            print("    The canon is skewing into a museum. Either the topic map")
            print("    misses recent vocabulary, or the year quota is not being")
            print("    filled. Check before vetting -- do not vet a skewed canon.")

        f = Counter(lab for r in rs for lab in flag(r))
        if f:
            print(f"  suspect: {dict(f)}  ({sum(f.values())} of {len(rs)})")


def nominate(core_n):
    recs = load()
    CANON.mkdir(exist_ok=True)
    by_domain = defaultdict(list)
    for r in recs:
        by_domain[r["domain"]].append(r)

    for domain, rs in by_domain.items():
        # Rank on normalized percentile where present, raw count as fallback.
        # Suspects sink so your reading time lands on real methods papers.
        def key(r):
            base = r.get("norm_percentile") or 0
            if not base and r["cited_by_count"]:
                base = 0.5
            return (base, r["cited_by_count"]) if not flag(r) else (base * 0.5, 0)

        rs.sort(key=key, reverse=True)
        for i, r in enumerate(rs):
            r["tier"] = 1 if i < core_n else 2

        core = [r for r in rs if r["tier"] == 1]
        w = CANON / f"vetting-{domain}.md"
        with w.open("w") as f:
            f.write(f"# Vetting worksheet: {domain}\n\n")
            f.write(f"{len(core)} papers. Mark each line: `k` keep, `s` strike.\n")
            f.write("**On a strike, write the reason.** Strike reasons become the\n")
            f.write("negative exemplars in the triage prompt and matter more than\n")
            f.write("the keeps. Mark `*` for Tier 0 exemplars (aim for 25).\n\n")
            f.write("Struck papers stay in Tier 2 -- for citation-overlap purposes\n")
            f.write("a tool paper is still a fine neighbourhood signal.\n\n---\n\n")
            for r in core:
                fl = flag(r)
                f.write(f"- [ ] `{r['openalex_id']}` **{r['title']}**\n")
                f.write(f"      {r['year']} · {r['venue'] or 'n/a'} · "
                        f"{r['cited_by_count']:,} cites")
                if fl:
                    f.write(f" · ⚠ {', '.join(fl)}")
                f.write("\n")
                f.write(f"      {r.get('abstract') or '(no abstract)'}\n")
                f.write("      mark: \n      reason: \n\n")
        print(f"wrote {w}  ({len(core)} to vet)")

    save([r for rs in by_domain.values() for r in rs])
    print("\nDay 3: read the abstracts, mark each line, then `canon_tier.py apply`.")
    print("Do the domain you know LEAST well first, while attention is fresh.")


def apply_marks():
    recs = {r["openalex_id"]: r for r in load()}
    total = Counter()

    for w in CANON.glob("vetting-*.md"):
        oid = None
        for line in w.read_text().splitlines():
            m = re.search(r"`(W\d+)`", line)
            if m:
                oid = m.group(1)
                continue
            if oid and line.strip().startswith("mark:"):
                mark = line.split("mark:", 1)[1].strip().lower()
                r = recs.get(oid)
                if not r:
                    continue
                if mark.startswith("s"):
                    r["tier"], r["vetted"] = 2, "struck"
                    total["struck"] += 1
                elif "*" in mark:
                    r["tier"], r["vetted"] = 0, "exemplar"
                    total["exemplar"] += 1
                elif mark.startswith("k"):
                    r["tier"], r["vetted"] = 1, "kept"
                    total["kept"] += 1
            if oid and line.strip().startswith("reason:"):
                reason = line.split("reason:", 1)[1].strip()
                if reason and oid in recs:
                    recs[oid]["strike_reason"] = reason
                oid = None

    save(list(recs.values()))
    print(dict(total))

    ex = sum(1 for r in recs.values() if r["tier"] == 0)
    if ex < 15:
        print(f"\nOnly {ex} exemplars marked. Aim for ~25 per domain -- these are")
        print("the LLM's entire contact with the canon.")
    if not total["struck"]:
        print("\nNothing struck. A citation-ranked harvest always contains tool")
        print("papers and reviews; if you struck none, the vetting did not happen.")
    print("\nNext: python ingest/canon_index.py build")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", choices=["nominate", "apply"])
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--core", type=int, default=150)
    a = ap.parse_args()

    if a.stats:
        stats(load())
    elif a.cmd == "nominate":
        nominate(a.core)
    elif a.cmd == "apply":
        apply_marks()
    else:
        ap.error("need --stats, nominate, or apply")


if __name__ == "__main__":
    main()
