#!/usr/bin/env python3
"""Eval harness for triage. The thing that makes charter tuning measurable.

    eval_triage.py sample --n 150      # Day 5: build a stratified labelled set
    eval_triage.py sample --n 100 --append   # add 100 more without losing existing labels
    eval_triage.py label               # Day 5: score them yourself, before triage runs
    eval_triage.py score               # Days 6-7: run the metrics
    eval_triage.py calibrate           # suggest NEAR/FAR similarity thresholds
    eval_triage.py diff                # what changed since the last run

RECALL MATTERS FAR MORE THAN PRECISION, AND THE DEFAULT INSTINCT GETS THIS
BACKWARDS.

  A wrongly ADMITTED paper costs ~$0.03 for a card nobody uses, and is filtered
  again at every downstream stage.
  A wrongly REJECTED paper is gone. Nothing recovers it and you never learn it
  existed.

So the headline metric is F-beta with beta=3, weighting recall 3:1. If you find
yourself pleased with a high-precision triage, you have optimised the wrong
thing. This script says so on every run.
"""

import argparse, json, random, sqlite3, statistics, sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
EVAL = ROOT / "eval"
LABELS = EVAL / "labels.jsonl"
RUNS = EVAL / "runs"
DB = ROOT / "ingest" / "papers.sqlite"

BETA = 3.0
ADMIT = 4          # baseline threshold; similarity band shifts it


def _infer_domain(categories):
    """papers.sqlite's domain column is null for every harvested row --
    arxiv_pull.py's harvest never sets it, on purpose: domain assignment is
    apply_triage.py's job, and apply_triage.py doesn't exist yet (see
    DAY-5-HANDOFF.md SS4). Without this, canon-similarity scoring in
    sample() and calibrate() silently falls back to comparing a candidate
    against the WHOLE pooled canon instead of just its own domain's slice --
    which dilutes exactly the near/mid/far separation this file exists to
    measure. Rebuild the category-overlap logic arxiv_pull.py's SETS
    already encodes, applied to whatever's in the categories column. A
    paper whose categories span more than one domain's SETS list picks the
    first match in SETS's definition order; good enough for sampling and
    calibration, and no worse than the null it replaces."""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from arxiv_pull import SETS
    except ImportError:
        return None
    cats = set((categories or "").split())
    for domain, wanted in SETS.items():
        if cats & set(wanted):
            return domain
    return None


# ------------------------------------------------------------------ sample

def sample(n, append=False):
    """Stratified sample. The borderline stratum is the only one that teaches
    you anything -- a labelled set of easy cases measures nothing.

    Strata come from canon similarity, not draw order. The original version
    of this function drew rows at random and then assigned strata by their
    INDEX in that draw -- the first n//3 called `expect_in`, the next n//3
    `expect_out`, for no reason but position. A random arXiv draw is
    overwhelmingly out-of-scope for any given domain, so that scheme produced
    150 easy rejections and called a third of them "borderline" by fiat. See
    DAY-5-HANDOFF.md sec 3.2 for the original diagnosis.

    Fix: pull a larger pool, score every candidate against the canon with
    canon_index.py's index (same NEAR/FAR bands triage itself uses), and
    build each stratum from the band that actually matches its name --
    `near` -> expect_in, `far` -> expect_out, `mid` -> borderline. The
    stratum you type during `label` still overwrites this; that part of the
    original design was fine and is unchanged.

    --append (n = how many NEW papers to add, not a new total): rerunning
    plain `sample` overwrites labels.jsonl and destroys any labelling
    you've already done. Append mode instead (a) keeps every already-written
    row -- labelled or not -- untouched, (b) excludes those arxiv_ids from
    the new draw so you can't get a duplicate, and (c) appends only the
    newly picked rows with my_score: null. `label` already only shows rows
    where my_score is null, so your old labels stay exactly as you left them
    and you just pick up where you stopped.
    """
    EVAL.mkdir(exist_ok=True)

    existing, seen_ids = [], set()
    if append and LABELS.exists():
        existing = [json.loads(l) for l in LABELS.read_text().splitlines() if l.strip()]
        seen_ids = {r["arxiv_id"] for r in existing}
        print(f"append mode: keeping {len(existing)} existing rows "
              f"({sum(1 for r in existing if r['my_score'] is not None)} already labelled), "
              f"excluding their arxiv_ids from the new draw.")
    elif append:
        print("append mode: no existing labels.jsonl found, behaving like a fresh sample.")

    con = sqlite3.connect(DB)
    pool_n = n * 4
    # Over-fetch to cover exclusions, since a NOT IN filter in Python (below)
    # can otherwise leave the pool short after already-seen ids are dropped.
    fetch_n = pool_n + len(seen_ids)
    rows_raw = con.execute(
        "SELECT arxiv_id, title, abstract, categories, domain FROM papers "
        "ORDER BY RANDOM() LIMIT ?", (fetch_n,)).fetchall()
    rows = [r for r in rows_raw if r[0] not in seen_ids][:pool_n]
    if len(rows) < n:
        sys.exit(f"only {len(rows)} unseen papers available; harvest a wider "
                  f"window first{' (everything else is already in labels.jsonl)' if append else ''}")

    # papers.sqlite's domain column is null pre-triage -- see _infer_domain's
    # docstring. Backfill from categories so the banding below is scoped to
    # each paper's own domain, not the whole pooled canon.
    rows = [(aid, title, abstract, cats, domain or _infer_domain(cats))
            for aid, title, abstract, cats, domain in rows]

    try:
        sys.path.insert(0, str(Path(__file__).parent))
        import numpy as np
        from canon_index import load_model, load_index, NEAR, FAR, TOP_K
    except ImportError as e:
        sys.exit(f"can't score against the canon ({e}). Need numpy, "
                  f"sentence-transformers, and canon/index.npz (canon_index.py "
                  f"build). Run from a repo checkout with those in place -- "
                  f"there is no fallback to the old index-position scheme, "
                  f"because that scheme doesn't actually stratify anything.")

    print(f"scoring {len(rows)} candidates against the canon "
          f"(one-time embedding pass, not per-paper reload)...")
    model = load_model()
    z = load_index()
    emb, dom_z = z["emb"], z["domains"]

    texts = [f"{title}. {(abstract or '')[:1200]}" for _, title, abstract, _, _ in rows]
    q = model.encode(texts, batch_size=64, normalize_embeddings=True,
                      show_progress_bar=True)

    banded = {"near": [], "mid": [], "far": []}
    for row, qi in zip(rows, q):
        _, _, _, _, domain = row
        mask = (dom_z == domain) if domain else np.ones(len(dom_z), bool)
        sims = emb[mask] @ qi
        top = np.sort(sims)[-TOP_K:] if len(sims) else np.array([0.0])
        mean = float(np.mean(top))
        band = "near" if mean >= NEAR else ("far" if mean < FAR else "mid")
        banded[band].append(row)

    per = n // 3
    remainder = n - per * 3   # goes to borderline -- the stratum that matters most
    quotas = {"expect_in": ("near", per), "expect_out": ("far", per),
              "borderline": ("mid", per + remainder)}

    picks, shortfalls = [], []
    for stratum, (band, want) in quotas.items():
        pool = banded[band]
        random.shuffle(pool)
        take = pool[:want]
        if len(take) < want:
            shortfalls.append(f"  {stratum} (band={band}): wanted {want}, "
                               f"canon only put {len(take)} candidates there")
        picks.extend((stratum, row) for row in take)

    # Shuffle ACROSS strata, not just within bands. The loop above shuffles
    # each band's pool before taking from it, which randomizes *which* rows are
    # drawn -- but it extends `picks` one stratum at a time, so the written
    # order is an expect_in block, then an expect_out block, then a borderline
    # block. That is what produced rows 105-133 (24 admits out of 29) and rows
    # 134-147 (fourteen consecutive rejections) in the existing 180-row set.
    # Scoring in same-band streaks invites anchoring against your neighbours
    # instead of against the scale, which is exactly the drift the stratified
    # design is meant to avoid. See OPEN-QUESTIONS.md sec 1.6.
    #
    # Only the new draw is shuffled. In --append mode `existing` is written
    # ahead of new_recs untouched, so already-labelled rows never move.
    random.shuffle(picks)

    new_recs = [{
        "arxiv_id": aid, "title": title,
        # 8000, not a real cap for any legitimate abstract (arXiv abstracts run
        # a few hundred to ~2500 chars; this is a pathological-input guard,
        # not truncation). The old 1500 cap sliced a real paper's abstract off
        # mid-sentence -- W2602.05541's quantum-matrix-multiplication paper
        # lost its last clause, which reads as truncated/corrupted input and
        # triage.md correctly scores that "malformed" per its own rules. The
        # agent wasn't wrong; the stored data was incomplete. See
        # ingest/backfill_full_abstracts.py for recovering rows already cut
        # under the old cap -- papers.sqlite never truncates at harvest, so
        # nothing already truncated here is actually lost.
        "abstract": (abstract or "")[:8000],
        "categories": cats, "domain": domain,
        "stratum": stratum, "my_score": None,
    } for stratum, (aid, title, abstract, cats, domain) in picks]

    all_recs = existing + new_recs
    with LABELS.open("w") as f:
        for r in all_recs:
            f.write(json.dumps(r) + "\n")

    if append:
        print(f"wrote {LABELS} ({len(existing)} existing + {len(new_recs)} new = "
              f"{len(all_recs)} total, band counts this draw: "
              f"near={len(banded['near'])} mid={len(banded['mid'])} far={len(banded['far'])} "
              f"in a pool of {len(rows)} unseen candidates)")
    else:
        print(f"wrote {LABELS} ({len(new_recs)} papers, band counts: "
              f"near={len(banded['near'])} mid={len(banded['mid'])} far={len(banded['far'])} "
              f"in a pool of {len(rows)})")
    if shortfalls:
        print("\nWARNING -- one or more strata came up short of the requested size:")
        print("\n".join(shortfalls))
        print("  Widen the harvest window or raise --n to pull a bigger pool; "
              "there is no padding from other bands, because that would just "
              "reintroduce the original bug under a different name.")

    print("""
Day 5: run `eval_triage.py label` and score every one YOURSELF, 0-5, using the
same scale triage uses. Do this BEFORE running triage on them even once -- once
you have seen a machine score, you cannot unsee it, and your labels stop being
an independent standard.

Re-assign the stratum as you go if your own read disagrees with the canon's
band -- the canon's `mid` band is a good proxy for borderline, not a promise.
The stratum you type during labelling is the one `score` actually uses.
""")


def label():
    recs = [json.loads(l) for l in LABELS.read_text().splitlines() if l.strip()]
    todo = [r for r in recs if r["my_score"] is None]
    if not todo:
        print("all labelled.")
        return

    print(f"{len(todo)} to label. 0-5, 's' skip, 'q' save and quit.")
    print("Reminder: 4-5 admits. 3 is a rejection with a note, not a hedge.\n")
    for r in todo:
        print("=" * 74)
        # domain shown deliberately: EVAL-01-FINDINGS.md sec1 found the first
        # 180 labels were scored domain-blind -- you were judging "would I
        # want this for the project" while triage.md judges "does this
        # domain's charter claim it", a different question. A miss where you
        # score 4 and triage says 1 because it landed in the wrong domain
        # looks identical to a real charter gap unless you can see, while
        # labelling, which charter the paper will actually be judged against.
        print(f"{r['arxiv_id']}  [{r['categories']}]  domain={r.get('domain') or '?'}  stratum={r['stratum']}")
        print(f"\n{r['title']}\n")
        print(r["abstract"][:900])
        while True:
            v = input("\nscore [0-5/s/q]: ").strip().lower()
            if v == "q":
                _save(recs)
                return
            if v == "s":
                break
            if v.isdigit() and 0 <= int(v) <= 5:
                r["my_score"] = int(v)
                raw = input(f"stratum [in/out/borderline, enter=keep {r['stratum']}]: ").strip()
                if raw:
                    r["stratum"] = _normalize_stratum(raw)
                break
        print()
    _save(recs)
    print("labelled.")


def _normalize_stratum(raw):
    """Every stratum this file writes or expects elsewhere is expect_in /
    expect_out / borderline, but the label() prompt above has always said
    "[in/out/borderline]" -- so anyone typing the shorthand it displays gets
    a value ("in", "out", "In", "Borderline", a typo...) that doesn't match
    what sample() and score_run() actually use, and score's per-stratum
    breakdown silently fragments into extra buckets. Map the recognizable
    shorthand to canonical form; leave anything unrecognizable (a typo bad
    enough that startswith can't place it) exactly as typed rather than
    guessing -- that's a signal to go fix it by hand, not swallow it."""
    s = raw.strip().lower()
    if s.startswith("in"):
        return "expect_in"
    if s.startswith("out"):
        return "expect_out"
    if s.startswith("bord"):
        return "borderline"
    return raw.strip()


def _save(recs):
    LABELS.write_text("".join(json.dumps(r) + "\n" for r in recs))


# ------------------------------------------------------------------- score

def _resolve_labels(explicit):
    """LABELS is a module constant, but LABEL-USE-PROTOCOL.md R8 expects it to
    stop existing at that path once a charter gets written from it -- the
    rename to eval/labels.dev.jsonl is deliberate, so a future run can't
    silently score a charter against its own training data. score and
    calibrate hit that FileNotFoundError first and need a way past it; sample
    and label are unaffected since this is a read-only path for both of them.
    """
    if explicit:
        p = Path(explicit)
        if not p.exists():
            sys.exit(f"no {p}")
        return p
    if LABELS.exists():
        return LABELS
    candidates = sorted(EVAL.glob("labels*.jsonl"))
    if len(candidates) == 1:
        sys.exit(f"{LABELS} doesn't exist, but {candidates[0]} does -- "
                 f"pass --labels {candidates[0]} (likely the R8 rename; "
                 f"see LABEL-USE-PROTOCOL.md)")
    if candidates:
        sys.exit(f"{LABELS} doesn't exist. Found instead: "
                 f"{', '.join(str(c) for c in candidates)} -- pass --labels <path>.")
    sys.exit(f"no {LABELS} and nothing matching eval/labels*.jsonl -- "
             f"run `sample` first")


def fbeta(p, r, beta=BETA):
    if p + r == 0:
        return 0.0
    b2 = beta * beta
    return (1 + b2) * p * r / (b2 * p + r)


def score_run(pred_file, labels_path=None):
    labels_path = _resolve_labels(labels_path)
    labels = {r["arxiv_id"]: r for r in
              (json.loads(l) for l in labels_path.read_text().splitlines() if l.strip())
              if r["my_score"] is not None}
    if not labels:
        sys.exit("no labels yet -- run `eval_triage.py label` first")

    preds = {r["arxiv_id"]: r for r in
             (json.loads(l) for l in Path(pred_file).read_text().splitlines() if l.strip())}

    tp = fp = fn = tn = 0
    within1 = 0
    n = 0
    misses, band_hits = [], defaultdict(lambda: [0, 0])
    wildcards = 0

    for aid, lab in labels.items():
        pred = preds.get(aid)
        if not pred:
            continue
        n += 1
        thr = pred.get("threshold", ADMIT)
        got, want = pred["score"], lab["my_score"]
        pred_in, true_in = got >= thr, want >= ADMIT

        if pred.get("wildcard"):
            wildcards += 1

        if abs(got - want) <= 1:
            within1 += 1
        st = lab.get("stratum", "?")
        band_hits[st][1] += 1
        if abs(got - want) <= 1:
            band_hits[st][0] += 1

        if pred_in and true_in:
            tp += 1
        elif pred_in:
            fp += 1
        elif true_in:
            fn += 1
            misses.append((aid, want, got, lab["title"], pred.get("reason", "")))
        else:
            tn += 1

    if not n:
        sys.exit("no overlap between labels and predictions")

    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0

    print(f"=== Triage eval, n={n} ===\n")
    print(f"  recall      {rec:.3f}   {'OK' if rec >= 0.90 else 'BELOW TARGET (0.90)'}")
    print(f"  precision   {prec:.3f}   {'OK' if prec >= 0.60 else 'below target (0.60)'}")
    print(f"  F-beta(3)   {fbeta(prec, rec):.3f}   <- the headline number")
    print(f"  within +-1  {within1/n:.3f}\n")

    print("  by stratum (agreement within +-1):")
    for st, (hit, tot) in sorted(band_hits.items()):
        flag = ""
        if st.startswith("border") and tot and hit / tot < 0.70:
            flag = "  <- BELOW TARGET (0.70). This is the number that matters."
        print(f"    {st:<12} {hit}/{tot} = {hit/max(tot,1):.2f}{flag}")

    print(f"\n  wildcard admissions: {wildcards}")
    if wildcards == 0:
        print("    ^ Zero. The far-band quota is decorative. Lower FAR in")
        print("      canon_index.py rather than removing the quota -- it is the")
        print("      only channel open to work the canon cannot recognise.")

    if rec < 0.90:
        print(f"\n  {len(misses)} MISSED in-scope papers -- read these before")
        print("  touching anything else. If they share a theme, the charter has")
        print("  a hole with a name; if they look random, the threshold is high.\n")
        for aid, want, got, title, reason in misses[:15]:
            print(f"    {aid} you={want} triage={got}  {title[:66]}")
            print(f"        said: {reason[:100]}")

    if prec > 0.85 and rec < 0.95:
        print("\n  NOTE: precision is high and recall is not. You are buying")
        print("  precision with recall, which is the wrong trade here -- a missed")
        print("  paper is gone forever, a false admit costs three cents.")

    RUNS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    (RUNS / f"{stamp}.json").write_text(json.dumps({
        "n": n, "recall": rec, "precision": prec, "fbeta": fbeta(prec, rec),
        "within1": within1 / n, "wildcards": wildcards,
        "misses": [m[0] for m in misses],
    }, indent=2))
    print(f"\n  saved eval/runs/{stamp}.json")


def diff():
    runs = sorted(RUNS.glob("*.json"))
    if len(runs) < 2:
        sys.exit("need at least two runs")
    a, b = json.loads(runs[-2].read_text()), json.loads(runs[-1].read_text())
    print(f"{runs[-2].stem}  ->  {runs[-1].stem}\n")
    for k in ("recall", "precision", "fbeta", "within1"):
        d = b[k] - a[k]
        print(f"  {k:<10} {a[k]:.3f} -> {b[k]:.3f}  ({d:+.3f})")

    fixed = set(a["misses"]) - set(b["misses"])
    broke = set(b["misses"]) - set(a["misses"])
    print(f"\n  newly caught: {len(fixed)}   newly missed: {len(broke)}")
    if broke:
        print("  regressions:", ", ".join(sorted(broke)[:10]))
        print("\n  A charter edit that fixes some and breaks others is usually a")
        print("  narrowing, not an improvement. Check F-beta, not the miss count.")


def calibrate(labels_path=None):
    """Suggest NEAR/FAR from the labelled set rather than the shipped guesses."""
    try:
        from canon_index import score as sim_score
    except ImportError:
        sys.exit("run from the repo root so canon_index is importable")

    labels_path = _resolve_labels(labels_path)
    recs = [json.loads(l) for l in labels_path.read_text().splitlines() if l.strip()]
    recs = [r for r in recs if r["my_score"] is not None]
    if len(recs) < 30:
        sys.exit("need at least 30 labelled papers to calibrate")

    no_domain = sum(1 for r in recs if not r.get("domain"))
    if no_domain:
        print(f"note: {no_domain}/{len(recs)} rows have no stored domain "
              f"(papers.sqlite's domain column is null pre-triage) -- "
              f"inferring from categories per row instead of comparing "
              f"against the whole pooled canon. See _infer_domain's "
              f"docstring.\n")

    ins, outs = [], []
    for r in recs:
        dom = r.get("domain") or _infer_domain(r.get("categories"))
        s = sim_score(f"{r['title']}. {r['abstract']}", dom)
        (ins if r["my_score"] >= 4 else outs).append(s["mean_top_k"])

    print(f"in-scope  n={len(ins):<4} median {statistics.median(ins):.3f}")
    print(f"out       n={len(outs):<4} median {statistics.median(outs):.3f}\n")
    near = statistics.quantiles(ins, n=4)[0] if len(ins) > 3 else 0.62
    far = statistics.quantiles(outs, n=4)[2] if len(outs) > 3 else 0.38
    print(f"suggested NEAR = {near:.2f}   (lower quartile of in-scope)")
    print(f"suggested FAR  = {far:.2f}   (upper quartile of out-of-scope)")
    if near <= far:
        print("\nWARNING: the distributions overlap almost completely. Similarity")
        print("is not separating your classes -- do not wire the band into the")
        print("threshold until the canon or the domain map improves.")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample"); s.add_argument("--n", type=int, default=150)
    s.add_argument("--append", action="store_true",
                    help="add --n new papers to the existing labels.jsonl instead of "
                         "overwriting it; excludes arxiv_ids already in the file so "
                         "there's no overlap with what you've already labelled")
    sub.add_parser("label")
    sc = sub.add_parser("score"); sc.add_argument("--pred", default="eval/predictions.jsonl")
    sc.add_argument("--labels", help="defaults to eval/labels.jsonl; pass explicitly "
                     "once that path no longer exists (see LABEL-USE-PROTOCOL.md R8)")
    sub.add_parser("diff")
    cb = sub.add_parser("calibrate")
    cb.add_argument("--labels", help="same as score's --labels")
    a = ap.parse_args()

    {"sample": lambda: sample(a.n, a.append), "label": label,
     "score": lambda: score_run(a.pred, a.labels), "diff": diff,
     "calibrate": lambda: calibrate(a.labels)}[a.cmd]()


if __name__ == "__main__":
    main()
