#!/usr/bin/env python3
"""Patch 7 (2026-09-04): what the first execution of the eval path changed.

    python3 patches/patch-07-eval-path-executed.py --dry-run
    python3 patches/patch-07-eval-path-executed.py

Needs patches 1-6 applied. Documents only -- every code change the same session
found is in patch 8, kept separate because a document correction and a
behavioural change to a gate should be revertible independently.

WHY THIS EXISTS

`TODO.md` E5 asked for the eval path to be smoke-tested "as pure debugging",
ungated, and it had sat in the backlog because `PROJECT-STATUS.md`'s
environment note says the sandbox does not start on the assistant side. That
note is no longer true for anything local. E5 was run on 2026-09-04 and the
path works end to end -- `import` on all four drafts, `label` walked far enough
to render a drafted verdict, `score` pooled and per-domain, exit 0 throughout.

So this patch closes E5, and then corrects the five places where documents
describe a state the run disproved. Each edit below replaces a sentence that
was true when written.

WHAT IT CORRECTS

  1. `TODO.md` E5 -- closed, with the results, and the two defects it found
     forwarded to patch 8 rather than left as prose.

  2. `TODO.md` E1's `show_eprint.py` sentence. It says the tool "reads what the
     curator actually parsed". It reads the raw tarball. What the curator
     parsed is the *window* `pdf_extract.py` cut from that tarball, and patches
     1 and 2 moved that window on eleven of the 28 cards. On those eleven,
     E1's own procedure shows the reader a source the curator never had.

  3. `TODO.md` E1's two named subtasks and its defective-window paragraph.
     Re-derived by reconstructing the pre-patch-1 extractor from
     `ingest/pdf_extract.py.pre-patch.bak` and diffing its output against the
     current one -- `patches/window_diff.py`, shipped with this patch. The
     paragraph said a discrepancy on 2411.02771 or 2608.16017 "may be the
     extractor's, not the curator's" and gave no way to tell. There is now a
     way, and the answer differs per card:

       2512.16061  window UNCHANGED -- `n` for absence is safe as it stands
       2608.16017  conclusion 0 -> 1,451 chars
       2411.02771  intro 0 -> 16,053 chars, conclusion -726

     2411.02771 is also the case worth having in writing. The old extractor
     reported `missing: {}` -- nothing missing -- while handing the curator an
     empty intro, and the card's `sections_read` omits the intro anyway. The
     curator caught the extractor lying to it. E1's line described that card
     as one whose "intro came back empty", which is true of the extractor and
     reads as a mark against the card.

  4. `TODO.md` D6's count. It names three offending object names and says "all
     three are real". A scan of all 28 cards finds ten, across ten cards, and
     some are defensible as single concepts. That moves D6 from a five-line
     validator to a retroactivity decision over 36% of the KB, which is §7.1
     item 1's shape and belongs next to it.

  5. `CARD-EVAL-HANDOFF.md` §6's "has never been executed end to end" and
     `PROJECT-STATUS.md`'s environment note.

  6. `patches/README.md`'s ledger, which stops at row 5 while patch 6 is on
     disk and marked applied in two documents. The README calls that table the
     order of record.

WHAT IT DELIBERATELY LEAVES UNDONE

  - **It does not close E1.** The reading is calibration and only the user can
    do it. `score_run()` warns that a run with zero overrides is
    uninterpretable and §4 says why: if a draft is written and accepted, the
    number measures two model instances agreeing.
  - **It does not touch E3, E6 or the gate graph.** The run surfaced that E6 is
    gated by E3, E3 wants curator spend, and Tier 4 forbids that spend before
    E6 produces a number -- a cycle. Writing a resolution into `TODO.md` would
    be this patch ruling on a live decision. It is filed as OQ material in the
    E5 text and left there.
  - **It does not reconcile `PROJECT-STATUS.md` Tier 1 with `TODO.md` E3** on
    which domain to measure. They disagree; D9 is the item for it and D9 is
    gated by E6, correctly.
  - **It does not run `git commit`.** Patch 6 is applied and uncommitted. The
    ledger row this adds says so, and committing is the user's.
"""

import argparse, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUFFIX = ".pre-patch7.bak"

E5_OLD = """- [ ] **E5.** Smoke-test the eval path as pure debugging

  - [x] `python3 ingest/show_eprint.py 2506.07459 --list` — run 2026-09-04, works
  - [ ] `card_eval.py import` each of the four files in `eval/drafts/`
  - [ ] Walk one card through `label`
  - [ ] `card_eval.py score`

  Needs no calibration — the point is finding crashes in code that has never
  executed, not producing numbers.
  **Gates:** E6
"""

E5_NEW = """- [x] **E5.** Smoke-test the eval path as pure debugging —
  **RUN 2026-09-04. `import` → `label` → `score` completes end to end.**

  - [x] `python3 ingest/show_eprint.py 2506.07459 --list` — run 2026-09-04, works
  - [x] `card_eval.py import` each of the four files in `eval/drafts/`
  - [x] Walk one card through `label`
  - [x] `card_eval.py score`, pooled and `--domain`

  Run in a scratch copy of the repo, deliberately: a `score` here writes
  `eval/card_runs/<ts>.json`, and `CLAUDE.md` line 13 designates *"check
  whether `eval/card_runs/` is empty"* as the test of whether the measurement
  has happened. A debugging run that answers that test in the affirmative
  destroys the one signal the line exists to carry. **`eval/card_runs/` is
  still absent on disk and should stay that way until E6.**

  What it found, in the order a reader needs it:

  - **Three of §6's four `import` commands are no-ops.** 2606.07914,
    2506.07459 and 2601.03123 skip as already-judged; only 2608.17381 loads.
    §3 predicted exactly this and §6 lists four commands without saying so.
  - **`import` is clean.** Diffed `card_labels.jsonl` before and after: only
    `drafted` and `labeller` moved, `judgments` byte-identical on all twenty
    records. The guarantee in §2's table holds.
  - **`score --domain stats` exits 1** — no judged stats cards — with a message,
    not a traceback. Correct behaviour, and it means E6 as filed cannot produce
    a stats number today.
  - **The pooled run flags `mathematical_objects` at 0.20** as weakest field
    and prints `unrecorded=2`, then folds those two into every headline anyway.
    That is E4a observed rather than predicted; option three there — have
    `score` refuse a headline while any record is unattributed — is the one the
    run argues for.
  - Two code defects, both forwarded to **patch 8** rather than described here:
    `_ask()` has no `EOFError` guard, and `validate_card.py` reports a missing
    dependency, an invalid card and a nonexistent path with the same exit code.

  **One finding this item cannot close.** E6 is gated by E3; E3 wants curator
  spend; Tier 4 forbids that spend before E6 produces a number. That is a cycle,
  and the cheap way out is that `sample --domain stats --append` draws the other
  two stats cards for zero model calls — verified working, 2 new records, 22
  total. It yields three stats cards, below `LABEL-USE-PROTOCOL.md` R1's floor
  of five, and `sample` says so itself. `probability` reaches seven sampled with
  five left to label and no curation at all. **Which of those E6 runs on is a
  decision, not a scheduling detail** — `PROJECT-STATUS.md` Tier 1 item 7 says
  pool or draw probability, E3 says stats, and D9 is gated by E6.
  **Gates:** E6
"""

E1_SUBTASKS_OLD = """  - [ ] Read `kb/stats/cards/2411.02771.md` — D0: its intro came back empty ~20m
  - [ ] Read `kb/stats/cards/2608.16017.md` — D0: its "Summary" was missed ~20m
"""

E1_SUBTASKS_NEW = """  - [ ] Read `kb/stats/cards/2411.02771.md` — window changed most; read the
        window note below before scoring anything `n` ~20m
  - [ ] Read `kb/stats/cards/2608.16017.md` — gained a 1,451-char conclusion
        the curator never saw ~20m
"""

E1_EPRINT_OLD = """  Read each card against the **cached e-print**, not the `papers.sqlite`
  abstract. §5.1 found that abstract diverging materially from arXiv's v1 on
  three of four cards checked, and there is no network here, so arXiv is not the
  fallback either. `show_eprint.py` reads what the curator actually parsed; all
  three stats cards have a `.bin` and the tool was verified working 2026-09-04.
"""

E1_EPRINT_NEW = """  Read each card against the **cached e-print**, not the `papers.sqlite`
  abstract. §5.1 found that abstract diverging materially from arXiv's v1 on
  three of four cards checked, and there is no network here, so arXiv is not the
  fallback either. All three stats cards have a `.bin` and `show_eprint.py` was
  verified working on all three, 2026-09-04.

  *Corrected 2026-09-04: this paragraph said `show_eprint.py` "reads what the
  curator actually parsed". It reads the raw tarball. What the curator parsed is
  the window `pdf_extract.py` cut out of that tarball, and patches 1 and 2 moved
  that window on eleven of the 28 cards. On those eleven the sentence as written
  sends you to compare a card against a source it was not built from.*
"""

E1_WINDOW_OLD = """  separately above: on 2411.02771 and 2608.16017 a discrepancy between card and
  source may be the extractor's, not the curator's. Scoring either `n` for
  absence without checking the window first files a curator defect against an
  extraction bug — and 2411.02771's intro was reported as found while coming
  back empty, so the card was built without it.
"""

E1_WINDOW_NEW = """  separately above: on 2411.02771 and 2608.16017 a discrepancy between card and
  source may be the extractor's, not the curator's. Scoring either `n` for
  absence without checking the window first files a curator defect against an
  extraction bug.

  **Which it is, per card, re-derived 2026-09-04** by reconstructing the
  pre-patch-1 extractor from `ingest/pdf_extract.py.pre-patch.bak` and diffing
  it against the current one — `python3 ingest/window_diff.py --domain stats`,
  and `--all-affected` for D0's eleven:

  | Card | `sections_read` | Was | Now | Read it how |
  |---|---|---|---|---|
  | 2512.16061 | abstract, intro | — | unchanged | comparable as it stands; an `n` for absence is safe |
  | 2608.16017 | abstract, intro | conclusion 0 | 1,451 | the conclusion is new text; `u`/`out-of-window`, not `n` |
  | 2411.02771 | abstract, conclusion | intro 0 | 16,053 | see below; conclusion also lost 726 chars to patch 1's boundary |

  So 2512.16061 first, not just because E1 already lists it first: it is the one
  stats card where card and source are the same pair the curator saw, and the
  only one where a disagreement is unambiguously the curator's.

  **2411.02771 is a curator win, and it is recorded nowhere else.** The old
  extractor returned `missing: {}` — nothing missing — while handing over a
  0-char intro. The card's `sections_read` is `["abstract", "conclusion"]`. The
  curator was told it had the introduction, was given nothing, and said so.
  Read the card against `sections_read`, not against today's 16,053 chars;
  anything living only in that delta is `u` with reason `out-of-window`
  (`CARD-EVAL-HANDOFF.md` §7.5), which keeps the defect countable instead of
  filing an extraction bug against a curator that behaved correctly.

  *Corrected 2026-09-04: this paragraph described 2411.02771 as the card whose
  "intro was reported as found while coming back empty, so the card was built
  without it". Both halves are true of the extractor and the second reads as a
  mark against the card. Patch 2 has since closed the empty intro; the live
  defect on that card is now truncation at `MAX_SECTION_CHARS`.*
"""

D6_OLD = """  Reject `(`, `/` and ` and ` in a `mathematical_objects` name. Catches
  `Hermitization (Girko's method)`, `Subset-rank and no-cancellation conditions`
  and `Circuit skeleton / ansatz topology` at write time — all three are real and
  all three currently score `y`.
"""

D6_NEW = """  Reject `(`, `/` and ` and ` in a `mathematical_objects` name. Catches
  `Hermitization (Girko's method)`, `Subset-rank and no-cancellation conditions`
  and `Circuit skeleton / ansatz topology` at write time — all three are real and
  all three currently score `y`.

  **Re-derived 2026-09-04 across all 28 cards: the rule matches ten names, not
  three, and this is no longer a five-line fix.**

  | Domain | Card | Name |
  |---|---|---|
  | compbio_methods | 2406.01756 | Multilevel / tri-level optimization |
  | compbio_methods | 2410.19208 | Spectral scaling / preconditioning |
  | compbio_methods | 2502.11152 | Balancedness / approximate balancedness of weights |
  | compbio_methods | 2509.18530 | Mid-circuit measurement and reset |
  | compbio_methods | 2601.03123 | Circuit skeleton / ansatz topology |
  | probability | 2109.02644 | Leave-one-out / resolvent perturbation identities |
  | probability | 2401.16556 | Convex conjugate / Fenchel duality |
  | probability | 2410.16457 | Hermitization (Girko's method) |
  | probability | 2505.00198 | Positive recurrence / stationary distribution |
  | probability | 2606.07914 | Subset-rank and no-cancellation conditions |

  Two things follow. **The rule has false positives**: `Mid-circuit measurement
  and reset` is one standard operation in quantum circuits, not two objects
  welded together, and `Convex conjugate / Fenchel duality` is a single notion
  under two names — which is `aliases` doing its job, badly placed. A validator
  that rejects those teaches curators to rename real objects to get past it,
  which is the failure invariant 11 exists to prevent, arriving through the card
  instead of the validator.

  **And retroactivity is now a decision.** Ten of 28 cards is 36% of the KB, so
  the choice is the §7.1 item 1 choice — forward-only with re-curation handed to
  E7, or a pass over the existing cards that Tier 4 forbids before E6. A
  validator that rejects at write time and a KB that would not pass it are
  consistent only if the second is deliberate and written down.

  Cheapest shape that keeps the finding without either cost: **warn, do not
  reject**, and tally. The three genuine cases are then countable and the seven
  arguable ones are visible for E7 to rule on, which is what §5.6 item 2 wanted
  the letter for.
"""

HANDOFF_OLD = """**The `import` → `label` → `score` path has never been executed end to end.**
Expect to fix something on the first pass.

With five of twenty judged, `score` will be thin — but running it now surfaces
crashes and shows whether the provenance and error-type blocks read usefully,
which is worth more at this stage than the numbers.
"""

HANDOFF_NEW = """**The `import` → `label` → `score` path was executed end to end on 2026-09-04
and works.** Exit 0 throughout, in a scratch copy of the repo so that
`eval/card_runs/` stays empty until E6 — `CLAUDE.md` line 13 makes that
directory's emptiness the test of whether this measurement has happened, and a
debugging run must not answer it. Results and the two defects found are in
`TODO.md` E5; the fixes are patch 8.

**Three of the four `import` commands above are no-ops.** 2606.07914,
2506.07459 and 2601.03123 skip as already-judged — which §3 predicts and this
list did not say — so only 2608.17381 actually loads a draft. Run them anyway:
the skip message is the confirmation that your five hand judgments are not
about to be overwritten.

With five of twenty judged, `score` is thin — but the run surfaced that the
provenance block reads usefully and that `unrecorded=2` reaches every headline
figure unremarked, which is E4a as an observation rather than a prediction.
"""

ENV_OLD = """**Environment.** The Linux sandbox does not start on the assistant side — **[shell]** items
run on your machine. Every script runs with `python3`, not `python` (see §3.5).
"""

ENV_NEW = """**Environment.** Every script runs with `python3`, not `python` (see §3.5).

*Corrected 2026-09-04: this note said the Linux sandbox does not start on the
assistant side, so all **[shell]** items run on your machine. It does start, and
most of E5's path ran there — `card_eval.py import`/`label`/`score`,
`audit_extraction.py`, `pdf_extract.py`, `show_eprint.py`, `window_diff.py`.*

*Two constraints survive, and they are different from each other. **No
network:** `backfill_source_pins.py` (D3), E8's version check and
`verify_citations.py` still have to be yours. **No `pyyaml` or `jsonschema`,
and `pip install` is denied:** `validate_card.py` and `rebuild_index.py` cannot
complete there at all, so the convention "a card that does not validate does
not exist" is unenforceable in that sandbox and every card-validation claim
made from it is worthless. That is what patch 8's exit 3 makes legible instead
of leaving it to look like 28 failing cards. And two things are yours by design
rather than by environment: `.claude/**` edits, and any labelling.*
"""

LEDGER_ANCHOR = """### Not a patch

`orientation-SKILL.md` is staged here only so patch 5 can install it to"""

LEDGER_INSERT = """| 6 | `patch-06-orientation-corrections.py` | 2026-09-04 | `PROJECT-STATUS.md`, `CLAUDE.md`, `TODO.md`, `CARD-EVAL-HANDOFF.md`, `dev-notes/curator-prompt-edits-pending.md` | The cold-start orientation correction pass. `TODO.md` D1: `CLAUDE.md` lines 5 and 13 rewritten from §10's staged text, plus the third instance of "`card_eval.py` does not exist" in `PROJECT-STATUS.md` §2, which D1's stated scope did not cover. **Applied but not committed** — `git status` shows five modified files and six untracked `.pre-patch6.bak` at the time row 7 was written. Row added retrospectively 2026-09-04: the patch was written and run without one, and this table is the order of record. |
| 7 | `patch-07-eval-path-executed.py` | pending | `TODO.md`, `CARD-EVAL-HANDOFF.md`, `PROJECT-STATUS.md`, `patches/README.md` | Documents only, from the first end-to-end run of the card-eval path. Closes E5 with its results; corrects E1's `show_eprint.py` claim and its two named subtasks against a reconstructed pre-patch window; re-derives D6 at ten offending names rather than three and reframes it as a retroactivity decision; retires `PROJECT-STATUS.md`'s environment note; adds ledger rows 6 and 7. Ships `window_diff.py`. 8 edits, 4 files. |

### Not a patch

`window_diff.py` is a **diagnostic** — run, not applied — and per the rule above
it is unnumbered and belongs in `ingest/`, moved as part of patch 7:

```bash
git mv patches/window_diff.py ingest/window_diff.py
```

It reconstructs the extractor a card was actually written under from
`ingest/pdf_extract.py.pre-patch.bak` and diffs its window against the current
one, so a card/source discrepancy can be attributed to the extractor or to the
curator instead of guessed at. `TODO.md` E1 and D0 both quote its output;
patch 7's doc edits point at `ingest/window_diff.py`, so those references dangle
until the move happens.

`orientation-SKILL.md` is staged here only so patch 5 can install it to"""


EDITS = [
    ("TODO.md", E5_OLD, E5_NEW, "close E5 with its results"),
    ("TODO.md", E1_SUBTASKS_OLD, E1_SUBTASKS_NEW, "E1 subtasks: correct both window descriptions"),
    ("TODO.md", E1_EPRINT_OLD, E1_EPRINT_NEW, "E1: show_eprint.py reads the tarball, not the window"),
    ("TODO.md", E1_WINDOW_OLD, E1_WINDOW_NEW, "E1: per-card window classification"),
    ("TODO.md", D6_OLD, D6_NEW, "D6: ten names, not three"),
    ("CARD-EVAL-HANDOFF.md", HANDOFF_OLD, HANDOFF_NEW, "§6: the path has been executed"),
    ("PROJECT-STATUS.md", ENV_OLD, ENV_NEW, "environment note: the sandbox starts"),
    ("patches/README.md", LEDGER_ANCHOR, LEDGER_INSERT, "ledger rows 6 and 7 + window_diff.py"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report only, touch nothing")
    a = ap.parse_args()

    # ---- preflight: all or nothing -------------------------------------
    texts, plan, already, problems = {}, [], [], []
    for fname, old, new, label in EDITS:
        p = ROOT / fname
        if not p.is_file():
            problems.append(f"{fname}: not found")
            continue
        if fname not in texts:
            texts[fname] = p.read_text()
        t = texts[fname]
        n_old, n_new = t.count(old), t.count(new)
        # `n_new` first and without reference to `n_old`: where the new text
        # extends the old rather than replacing it -- an appended correction,
        # which is this repo's usual shape -- the old anchor is still present
        # afterwards, and testing `n_old` first would re-apply the edit and
        # duplicate its tail. Presence of the new text is the applied test.
        if n_new >= 1:
            already.append(f"{fname}: {label}")
        elif n_old == 1:
            plan.append((fname, old, new, label))
        elif n_old == 0:
            problems.append(f"{fname}: anchor not found — {label}")
        else:
            problems.append(f"{fname}: anchor appears {n_old}x, must be 1 — {label}")

    for line in already:
        print(f"  SKIP    {line}  (already applied)")
    for fname, _, _, label in plan:
        print(f"  APPLY   {fname}: {label}")
    for line in problems:
        print(f"  PROBLEM {line}")

    if problems:
        sys.exit("\nrefusing to write: preflight failed. A half-applied patch to "
                 "these documents is worse than none — it leaves two versions of "
                 "the same correction in the repo, which is the failure the "
                 "supersession chain in PROJECT-STATUS.md §2 already records.")

    if not plan:
        print("\nnothing to do — patch 7 is fully applied.")
        return

    if a.dry_run:
        print(f"\ndry run: {len(plan)} edit(s) across "
              f"{len(set(f for f, *_ in plan))} file(s), nothing written.")
        return

    # ---- write ---------------------------------------------------------
    touched = {}
    for fname, old, new, _ in plan:
        touched[fname] = touched.get(fname, texts[fname]).replace(old, new, 1)

    for fname, out in touched.items():
        p = ROOT / fname
        bak = p.with_name(p.name + SUFFIX)
        if not bak.exists():
            shutil.copy2(p, bak)
        p.write_text(out)
        print(f"  wrote   {fname}   (backup: {bak.name})")

    print(f"\n{len(plan)} edit(s) applied across {len(touched)} file(s).")
    print("\nStill yours, and this patch does not do them:")
    print("  git mv patches/window_diff.py ingest/window_diff.py")
    print("  git add -A && git commit    # patch 6 is still uncommitted")
    print("  python3 patches/patch-08-failure-modes.py --dry-run")


if __name__ == "__main__":
    main()
