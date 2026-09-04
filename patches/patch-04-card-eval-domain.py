#!/usr/bin/env python3
"""Patch 4 (2026-09-03): `--domain` for `card_eval.py score` and `diff`. TODO.md D4.

    python3 patches/patch-04-card-eval-domain.py --dry-run
    python3 patches/patch-04-card-eval-domain.py

Independent of patches 1 and 2 -- different file, no shared anchors. It needs
patch 3, which repairs a SyntaxError that stops `card_eval.py` loading at all:
the text edits below apply to a broken file perfectly well, but none of the
verification steps can run until it parses, and attribution gets muddled. D4
gates E6, and E6 is what the extractor work was clearing the way for.

THE PROBLEM, IN D4'S OWN WORDS

  "score_run() splits by field, by named_in_paper and by confidence, but never
  by domain -- so a card_labels.jsonl holding both the existing 20 cross-domain
  records and a new stats sample yields one blended figure with no way to
  recover the stats number. sample writes only to the fixed LABELS path, so a
  separate file is not the easy way out."

Current state, re-derived 2026-09-03 rather than read off a listing:
`card_labels.jsonl` holds 20 records -- compbio_methods 7, probability 7,
compbio_mechanism 5, stats 1 -- of which 5 pass `_is_judged`, spread across
three domains and including no stats card at all. E3 will append 15-20 stats
cards against a 30-paper queue (E2, answered 2026-09-03). Without this, the
first card-accuracy number this project has ever had is a pool of two domains
measured for opposite reasons: `stats` because it can be refereed unaided, the
rest because they could not be.

WHAT IT ADDS

  1. `score --domain <d>` filters the judged records and scopes the entire run.
     The scope is printed above every number, in the same position and for the
     same reason as the labeller block: a figure whose population is not stated
     is not a figure.

  2. The run file records `domain` and `n_by_domain`, and its filename carries
     the scope (`20260903-141530-stats.json`). A stored 0.82 already travels
     with `labellers`; it now travels with its population too.

  3. An unfiltered run prints a per-domain summary table. This is the part that
     makes the flag usable rather than a chore -- without it you re-run `score`
     once per domain and produce four run files that `diff` will then try to
     compare against each other. The table is explicitly a diagnostic: it shows
     n, field-correct rate and the object-precision band per domain, and points
     at `--domain` for a number worth storing.

  4. `diff` now compares runs of the SAME scope, and takes `--domain` to say
     which. This is not optional. `diff` picks the last two run files by name,
     so the moment scoped and pooled runs interleave on disk it would compare a
     stats figure against a pooled one and print a confident delta. That is the
     failure `_resolve_labels` exists to prevent one layer down, and the same
     failure `eval_triage.py diff` warns about for sample overlap.

WHAT IT DOES NOT DO

  - No per-domain figures inside the run file beyond `n_by_domain`. The table in
    (3) is computed for display and not stored, deliberately: storing it would
    invent a nested run-file schema, and a domain number worth keeping should be
    produced by `--domain`, where the whole run states its population. One
    number, one scope, one file.
  - No change to `sample`, which already has `--domain`, or to `label`, which
    should walk everything in the file regardless of how it will be scored.
  - No threshold, target or gate. What counts as good enough for `stats` is E7's
    decision and this patch does not encode one.
"""

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- code edits

OLD_SIG = '''def score_run(labels_path=None):
    path = Path(labels_path) if labels_path else LABELS
    if not path.exists():
        sys.exit(f"no {path} -- run `sample` and `label` first")
    recs = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    judged = [r for r in recs if _is_judged(r)]
    if not judged:
        sys.exit("nothing judged yet -- run `card_eval.py label`")

    n = len(judged)
    print(f"=== Card eval, n={n} cards judged ===\\n")'''

NEW_SIG = '''def _domain_summary(judged):
    """Headline figures per domain, for display only.

    Three formulas duplicated from the body below rather than refactored out of
    it. That is deliberate for a patch: score_run() is 280 lines of interleaved
    computation and printing, and pulling it apart to share code here would
    touch every number in the file to gain a table. The duplication is visible,
    labelled, and the table is explicitly not stored -- see the docstring of
    patches/patch-04-card-eval-domain.py. If a fourth caller ever needs these,
    that is the point to factor properly.
    """
    by_dom = defaultdict(list)
    for r in judged:
        by_dom[r.get("domain") or "(none)"].append(r)

    rows = []
    for dom, rs in sorted(by_dom.items()):
        fy = ft = 0
        listed = correct = unres = 0
        for r in rs:
            for v in r["judgments"].values():
                if v in ("y", "p", "n"):
                    ft += 1
                    fy += v == "y"
            for o in r.get("objects") or []:
                v = o.get("verdict")
                if v == "u":
                    unres += 1
                elif v in ("y", "p", "n"):
                    listed += 1
                    correct += v == "y"
        seen = listed + unres
        rows.append({
            "domain": dom, "cards": len(rs),
            "field_rate": fy / ft if ft else None,
            "prec_hi": correct / listed if listed else None,
            "prec_lo": correct / seen if seen else None,
            "unresolved": unres,
        })
    return rows


def score_run(labels_path=None, domain=None):
    path = Path(labels_path) if labels_path else LABELS
    if not path.exists():
        sys.exit(f"no {path} -- run `sample` and `label` first")
    recs = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    judged = [r for r in recs if _is_judged(r)]
    if not judged:
        sys.exit("nothing judged yet -- run `card_eval.py label`")

    # Scope BEFORE anything is counted. D4's argument: a file holding the
    # existing cross-domain records plus a fresh stats sample yields one blended
    # figure with no way to recover the stats number, and `sample` writes only
    # to the fixed LABELS path so a separate file is not the way out.
    n_by_domain = dict(Counter(r.get("domain") or "(none)" for r in judged))
    if domain:
        judged = [r for r in judged if r.get("domain") == domain]
        if not judged:
            sys.exit(f"no judged cards in domain {domain!r}. Judged so far: "
                     + ", ".join(f"{d}={c}" for d, c in
                                 sorted(n_by_domain.items())))

    n = len(judged)
    scope = domain or "all domains"
    print(f"=== Card eval, n={n} cards judged  [{scope}] ===\\n")
    if domain:
        print(f"  scope: {domain} only, {n} of "
              f"{sum(n_by_domain.values())} judged cards.\\n")
    else:
        # Not a warning when it is the only domain in the file -- only when a
        # single figure is being computed across populations sampled for
        # different reasons.
        if len(n_by_domain) > 1:
            print("  scope: ALL DOMAINS POOLED — "
                  + ", ".join(f"{d}={c}" for d, c in sorted(n_by_domain.items())))
            print("  Every figure below is a blend. `stats` is measured because")
            print("  it can be refereed unaided; the others because they cannot")
            print("  (CARD-EVAL-HANDOFF.md sec4). Pooling those is a number about")
            print("  no domain in particular. Use --domain for one you can quote,")
            print("  and read the per-domain table at the end of this run first.\\n")'''

OLD_RUNFILE = '''    out = {
        "n_cards": n,'''

NEW_RUNFILE = '''    out = {
        "n_cards": n,
        # The population, permanently attached, for the same reason `labellers`
        # is: a stored 0.82 that does not say which cards it covers cannot be
        # compared to anything later, and `diff` would compare it anyway.
        "domain": domain,
        "n_by_domain": n_by_domain,'''

OLD_STAMP = '''    RUNS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")'''

NEW_STAMP = '''    RUNS.mkdir(parents=True, exist_ok=True)
    # Scope in the filename, so a pooled run and a stats run are distinguishable
    # on disk and `diff` can select among them without opening every file.
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S") + (f"-{domain}" if domain else "")'''

OLD_SAVE = '''    (RUNS / f"{stamp}.json").write_text(json.dumps(out, indent=2))
    print(f"\\n  saved eval/card_runs/{stamp}.json")'''

NEW_SAVE = '''    # ---- per-domain table: the diagnostic that makes --domain usable
    #
    # Printed only for a pooled run, and only when there is more than one
    # domain in it. Without this you re-run `score` once per domain to see
    # whether one is dragging the pool, which produces several run files that
    # `diff` then tries to compare against each other.
    if not domain and len(n_by_domain) > 1:
        rows = _domain_summary(judged)
        print("\\n  by domain   (diagnostic -- NOT stored; use --domain for a "
              "number worth quoting)\\n")
        print(f"    {'domain':<20}{'cards':>6}{'fields y':>10}"
              f"{'object precision':>19}{'unres':>7}")
        for d in rows:
            fr = f"{d['field_rate']:.2f}" if d["field_rate"] is not None else "  -- "
            if d["prec_hi"] is None:
                pr = "        --     "
            elif d["unresolved"]:
                pr = f"  {d['prec_lo']:.2f} - {d['prec_hi']:.2f}   "
            else:
                pr = f"       {d['prec_hi']:.2f}   "
            print(f"    {d['domain']:<20}{d['cards']:>6}{fr:>10}{pr:>19}"
                  f"{d['unresolved']:>7}")
        thin = [d["domain"] for d in rows if d["cards"] < 5]
        if thin:
            print(f"\\n    Under 5 cards: {', '.join(thin)}. LABEL-USE-PROTOCOL.md")
            print("    R1 sets five as the floor for a pattern and R7 wants ten")
            print("    before proposing text. Those rows are observations.")

    (RUNS / f"{stamp}.json").write_text(json.dumps(out, indent=2))
    print(f"\\n  saved eval/card_runs/{stamp}.json")'''

OLD_DIFF = '''def diff():
    runs = sorted(RUNS.glob("*.json"))
    if len(runs) < 2:
        sys.exit("need at least two runs -- score twice, with a schema or prompt "
                 "change in between, or there is nothing to compare")
    a, b = json.loads(runs[-2].read_text()), json.loads(runs[-1].read_text())
    print(f"{runs[-2].stem}  ->  {runs[-1].stem}\\n")'''

NEW_DIFF = '''def diff(domain=None):
    """Compare the last two runs OF THE SAME SCOPE.

    Scope matching is not a nicety. This picks runs by filename order, so as
    soon as a pooled run and a `--domain stats` run interleave on disk, the
    unguarded version compares a stats figure against a cross-domain one and
    prints a confident delta for a change that never happened. Same class of
    failure as scoring a charter against its own training data, which
    `eval_triage.py._resolve_labels` exists to block one layer down.

    Runs written before patch 3 carry no `domain` key. They are treated as
    pooled, which is what they were.
    """
    runs = sorted(RUNS.glob("*.json"))
    loaded = [(p, json.loads(p.read_text())) for p in runs]
    scoped = [(p, d) for p, d in loaded if (d.get("domain") or None) == domain]

    if len(scoped) < 2:
        have = Counter((d.get("domain") or "all") for _, d in loaded)
        sys.exit(
            f"need at least two runs scoped to {domain or 'all domains'}; "
            f"found {len(scoped)}.\\n"
            f"  runs on disk by scope: "
            + (", ".join(f"{k}={v}" for k, v in sorted(have.items())) or "none")
            + "\\n  score twice at the same scope, with a schema or prompt change\\n"
              "  in between, or there is nothing to compare. Comparing across\\n"
              "  scopes is refused rather than warned about: the delta would be\\n"
              "  a change of population reported as a change in card quality.")

    (pa, a), (pb, b) = scoped[-2], scoped[-1]
    print(f"{pa.stem}  ->  {pb.stem}   [{domain or 'all domains'}]\\n")'''

OLD_CLI = '''    sc = sub.add_parser("score")
    sc.add_argument("--labels", help="defaults to eval/card_labels.jsonl")
    sub.add_parser("diff")
    a = ap.parse_args()'''

NEW_CLI = '''    sc = sub.add_parser("score")
    sc.add_argument("--labels", help="defaults to eval/card_labels.jsonl")
    sc.add_argument("--domain", choices=DOMAINS,
                     help="score one domain only, and say so in the run file. "
                          "Without it every figure is pooled across whatever "
                          "domains the file holds -- see TODO.md D4")
    df = sub.add_parser("diff")
    df.add_argument("--domain", choices=DOMAINS,
                     help="compare the last two runs scoped to this domain; "
                          "default compares the last two POOLED runs. Runs of "
                          "different scope are never compared")
    a = ap.parse_args()'''

OLD_DISPATCH = '''     "score": lambda: score_run(a.labels),
     "diff": diff}[a.cmd]()'''

NEW_DISPATCH = '''     "score": lambda: score_run(a.labels, a.domain),
     "diff": lambda: diff(a.domain)}[a.cmd]()'''

OLD_DOCSTRING = '''    card_eval.py label                         # your judgment, per field
    card_eval.py score                         # curator vs. you
    card_eval.py diff                          # did the last schema/prompt edit help'''

NEW_DOCSTRING = '''    card_eval.py label                         # your judgment, per field
    card_eval.py score                         # curator vs. you, pooled
    card_eval.py score --domain stats          # ...or one domain, on the record
    card_eval.py diff                          # did the last schema/prompt edit help
    card_eval.py diff --domain stats           # same scope only; never across'''

# ---------------------------------------------------------------- doc edits

OLD_D4 = """- [ ] **D4.** Add a `--domain` filter to `card_eval.py score`

  `score_run()` splits by field, by `named_in_paper` and by confidence, but never
  by domain — so a `card_labels.jsonl` holding both the existing 20 cross-domain
  records and a new stats sample yields one blended figure with no way to recover
  the stats number. `sample` writes only to the fixed `LABELS` path, so a
  separate file is not the easy way out. Small change; it is what makes E6
  answerable.
  **Gates:** E6"""

NEW_D4 = """- [ ] **D4.** Add a `--domain` filter to `card_eval.py score` —
  **APPLIED by patch 4, 2026-09-03** (`patches/patch-04-card-eval-domain.py`)

  `score_run()` split by field, by `named_in_paper` and by confidence, but never
  by domain — so a `card_labels.jsonl` holding both the existing 20 cross-domain
  records and a new stats sample yielded one blended figure with no way to
  recover the stats number. `sample` writes only to the fixed `LABELS` path, so a
  separate file was not the easy way out.

  What landed: `score --domain <d>` scopes the whole run and records the scope in
  the run file and its filename; a pooled run prints a per-domain diagnostic
  table; and `diff` now compares only runs of the same scope and **refuses**
  across scopes rather than warning, because it selects by filename order and
  would otherwise report a change of population as a change in card quality.

  Not encoded, deliberately: any threshold for what counts as good enough per
  domain. That is E7's.
  **Gates:** E6"""

OLD_STATUS_ROW = ("| Scripts | `run_triage`, `apply_triage`, `pdf_extract`, "
                  "`rebuild_index` all written and exercised. `pdf_extract` was "
                  "exercised *and defective*: six of 28 cards were built from a "
                  "short window, fixed 2026-09-03 (`TODO.md` D0). Exercised is not "
                  "measured |")
NEW_STATUS_ROW = ("| Scripts | `run_triage`, `apply_triage`, `pdf_extract`, "
                  "`rebuild_index` all written and exercised. `pdf_extract` was "
                  "exercised *and defective*: six of 28 cards were built from a "
                  "short window, fixed 2026-09-03 (`TODO.md` D0). Exercised is not "
                  "measured |\n"
                  "| Admitted queues | Derived 2026-09-03 from `papers.sqlite` "
                  "`status='admitted'` minus cards on disk, the same method behind "
                  "`WEEK-3-PLAN.md`'s figures: **stats 30** (33 admitted, 3 "
                  "curated) · compbio_methods 26 · probability 8 · "
                  "compbio_mechanism 2. E2's worry that the `stats` queue might be "
                  "thin is answered — it is the deepest reserve relative to what "
                  "has been curated, so E3 is not size-constrained |")

OLD_LABELS_ROW = ("| Per-domain labels | `compbio_methods` 101/26 admits · `stats` "
                  "40/26 · `probability` 29/17 · `compbio_mechanism` 10/3 |")
NEW_LABELS_ROW = ("| Per-domain labels | 180 rows in `eval/labels.dev.jsonl` "
                  "(R8-renamed): `compbio_methods` 101 · `stats` 40 · `probability` "
                  "29 · `compbio_mechanism` 10. **The admit counts previously in "
                  "this cell — 26/26/17/3 — were wrong in all four and are removed, "
                  "2026-09-03.** `papers.sqlite` `status='admitted'` gives "
                  "35/33/18/8; `stratum: expect_in` gives 21/25/13/3; `my_score>=4` "
                  "gives 26/26/17/3. The old cell was the third of those, labelled "
                  "as the first — and `compbio_methods` reading 26 is the *queue* "
                  "depth in an admit-count column. See the Admitted queues row |")

OLD_E2 = """- [ ] **E2.** Check how deep the `stats` admitted queue is"""
NEW_E2 = """- [x] **E2.** Check how deep the `stats` admitted queue is — **ANSWERED 2026-09-03: 30**

  33 admitted in `papers.sqlite`, 3 curated. Same method as `WEEK-3-PLAN.md`'s
  figures for the other domains (`status='admitted'` minus cards on disk),
  verified against its `probability`: 8 queued (18 admitted, 10 curated). So the
  premise below is wrong in the good direction — the queue is the deepest
  per-domain reserve in the project relative to what has been curated, and E3 is
  not size-constrained. At `MAX_CARDS_PER_DOMAIN_PER_DAY=10`, a target of 15–20
  is two days of curation. Nothing here is a finding about triage or the charter.

  Original text, kept because its reasoning about *why* stats still stands:"""

# ------------------------------------------------------------------- driver


def _say(*args):
    """print() that survives a closed stdout, so `| head` cannot cancel a run."""
    try:
        print(*args)
    except BrokenPipeError:
        pass


EDITS = [
    ("ingest/card_eval.py", "document the flag in the module docstring",
     OLD_DOCSTRING, NEW_DOCSTRING),
    ("ingest/card_eval.py", "scope score_run, add the per-domain helper",
     OLD_SIG, NEW_SIG),
    ("ingest/card_eval.py", "record the scope in the run file",
     OLD_RUNFILE, NEW_RUNFILE),
    ("ingest/card_eval.py", "put the scope in the run filename",
     OLD_STAMP, NEW_STAMP),
    ("ingest/card_eval.py", "print the per-domain diagnostic table",
     OLD_SAVE, NEW_SAVE),
    ("ingest/card_eval.py", "make diff refuse to compare across scopes",
     OLD_DIFF, NEW_DIFF),
    ("ingest/card_eval.py", "wire --domain into score and diff", OLD_CLI, NEW_CLI),
    ("ingest/card_eval.py", "pass it through the dispatch table",
     OLD_DISPATCH, NEW_DISPATCH),
    ("TODO.md", "mark D4 applied and record what landed", OLD_D4, NEW_D4),
    ("TODO.md", "close E2 with the derived queue depth", OLD_E2, NEW_E2),
    ("PROJECT-STATUS.md", "add the admitted-queue row", OLD_STATUS_ROW,
     NEW_STATUS_ROW),
    ("PROJECT-STATUS.md", "remove the four wrong admit counts", OLD_LABELS_ROW,
     NEW_LABELS_ROW),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change and exit without writing")
    ap.add_argument("--no-backup", action="store_true",
                    help="skip the .pre-patch4.bak copies")
    a = ap.parse_args()

    if not (ROOT / "ingest" / "card_eval.py").exists():
        sys.exit(f"not a research-net checkout: {ROOT}\n"
                 f"  run this from the repo root, as "
                 f"`python3 patches/{Path(__file__).name}`")

    # Soft, not fatal: these are text edits and they apply either way. But the
    # verify block at the end cannot run on a file that will not parse, and
    # patch 3 is the fix for that.
    import ast
    try:
        ast.parse((ROOT / "ingest" / "card_eval.py").read_text())
    except SyntaxError as e:
        _say(f"  NOTE     ingest/card_eval.py does not parse (line {e.lineno}).\n"
             f"           These edits will apply, but nothing below can be\n"
             f"           verified until it loads. Apply patch 3 first.\n")

    cache = {}
    todo, already, broken = [], [], []
    for rel, label, old, new in EDITS:
        p = ROOT / rel
        if not p.exists():
            broken.append((rel, label, "file not found"))
            continue
        text = cache.setdefault(rel, p.read_text())
        n_old, n_new = text.count(old), text.count(new)
        if n_new:
            already.append((rel, label))
        elif n_old == 1:
            todo.append((rel, label, old, new))
        elif n_old == 0:
            broken.append((rel, label, "anchor not found -- file has moved on"))
        else:
            broken.append((rel, label, f"anchor appears {n_old} times, expected 1"))

    for rel, label in already:
        _say(f"  skip     {rel:<24} {label} (already applied)")
    for rel, label, why in broken:
        _say(f"  BLOCKED  {rel:<24} {label} -- {why}")
    for rel, label, _, _ in todo:
        _say(f"  apply    {rel:<24} {label}")

    if broken:
        sys.exit(f"\n{len(broken)} edit(s) could not be matched. Nothing written.\n"
                 f"  Anchors are exact text from the 2026-09-03 state of the repo.\n"
                 f"  Applied edits are detected and skipped, so a partial\n"
                 f"  hand-application followed by a re-run is safe.")
    if not todo:
        _say("\nnothing to do; all edits already present.")
        return
    if a.dry_run:
        _say(f"\n--dry-run: {len(todo)} edit(s) would be applied across "
             f"{len({r for r, _, _, _ in todo})} file(s). Nothing written.")
        return

    staged = dict(cache)
    for rel, label, old, new in todo:
        staged[rel] = staged[rel].replace(old, new, 1)

    # Writes complete before anything is reported, so a closed stdout cannot
    # kill the process midway and leave a half-applied tree.
    touched = sorted({rel for rel, _, _, _ in todo})
    for rel in touched:
        p = ROOT / rel
        if not a.no_backup:
            shutil.copy2(p, p.with_suffix(p.suffix + ".pre-patch4.bak"))
        p.write_text(staged[rel])

    for rel in touched:
        _say(f"  wrote    {rel}")
    _say(f"\n{len(todo)} edit(s) applied to {len(touched)} file(s).")
    _say("\nVerify, in this order:")
    _say("  python3 -c \"import ast,pathlib;"
         "ast.parse(pathlib.Path('ingest/card_eval.py').read_text())\"")
    _say("  python3 ingest/card_eval.py score --help      # --domain present")
    _say("  python3 ingest/card_eval.py score             # pooled + domain table")
    _say("  python3 ingest/card_eval.py score --domain stats")
    _say("     -> n=1, and it says so; one card is not a measurement")
    _say("  python3 ingest/card_eval.py diff --domain stats")
    _say("     -> refuses, naming the scopes on disk")
    _say("  git diff --stat")
    _say("\nThen commit. The .pre-patch4.bak files are redundant once you have.")


if __name__ == "__main__":
    main()
