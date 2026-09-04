#!/usr/bin/env python3
"""Patch 6 (2026-09-04): the correction pass from the cold-start orientation session.

    python3 patches/patch-06-orientation-corrections.py --dry-run
    python3 patches/patch-06-orientation-corrections.py

Needs patches 1-5 applied. Every claim below was re-derived from an artifact
rather than read out of a document, per `PROJECT-STATUS.md` §6 item 5 and the
`_load_cards` warning that a number written once and never re-derived is the
repo's characteristic failure.

WHAT IT CORRECTS

  1. `PROJECT-STATUS.md` §2 says "`card_eval.py` does not exist." The
     orientation skill flags this sentence in `CLAUDE.md` line 13 and files it
     as D1, but the same false sentence is also in §2 -- the top of the
     supersession chain -- where nothing had noticed it. `ingest/card_eval.py`
     is 64,177 bytes, parses, and answers `--help` with all five subcommands.
     D1's scope was CLAUDE.md alone, so applying D1 as filed would have left
     the phase document asserting it.

  2. `CLAUDE.md` lines 5 and 13, using the text staged in
     `dev-notes/curator-prompt-edits-pending.md` §10 verbatim. That item has
     read "pending - do this one first" since 2026-09-01 and is Tier 0 item 4.
     CLAUDE.md is not in `settings.json`'s deny list, so it needs no hand
     application; it was waiting only because the staged text sat in the
     `.claude/**` queue by filing convention rather than by necessity. §10 is
     marked applied in the same run so the queue does not keep offering it.

  3. `CARD-EVAL-HANDOFF.md` §6 still reads "six of twenty-one judged". §1
     corrected those figures to five of twenty on 2026-09-03 and patch 5
     rewrote §3's table to match, but §6 was missed -- and §6 is the section
     the orientation skill sends a cold reader to for the actual program, so
     the stale pair sat in the operative list while the corrected pair sat two
     screens above it. Re-derived here: `card_labels.jsonl` holds 20 records
     and `_is_judged` passes 5.

  4. `TODO.md` D8 is already implemented and is closed. `exemplars()` in
     `ingest/canon_index.py` excludes `strike_superseded` records from
     `neg_pool` directly, with the reasoning in its docstring.
     `PROJECT-STATUS.md` §3 has recorded this as landed "at some point"; D8 did
     not know. Closed with the caveat that matters: exactly one canon record
     sets the field and it is a `stats` record, so the code path has never been
     exercised on `compbio_mechanism`, which is the domain D7 touches.

  5. `TODO.md` D7 and `PROJECT-STATUS.md` Tier 0 item 5 both describe the
     pending canon work as "two strike reversals and ten rewritten reasons" in
     `compbio_mechanism`. Replicating `apply_marks()` read-only against
     `canon.jsonl` gives a different and wider delta:

         compbio_mechanism   1 mark  (W1993482030 struck -> exemplar)   1 reason
         compbio_methods     2 marks (W2178011284 struck -> kept,
                                      W2050834445 exemplar -> kept)     3 reasons
         stats               0 marks                                    1 reason
         probability         0 marks                                    0 reasons

     Two things follow. The `compbio_mechanism` figure is one change, not two.
     And `apply_marks()` globs every `vetting-*.md`, so running it also applies
     five changes in two domains that no to-do list mentions -- including
     demoting W2050834445 (Donoho, minimal L1 = sparsest) out of tier 0.

     That demotion is the consequential one. Exemplars are the model's entire
     contact with the canon, triage is the only measured component in the
     project (recall 0.903 / precision 0.699, `eval/runs/20260827-214656`), and
     §4.6 already records part of that precision gain tracing to a prompt edit
     nobody wrote down. A second unrecorded change to the triage prompt would
     compound exactly that. So D7 stops being a chore and becomes a decision,
     and it is paired here with the `triage.md` reconstruction it now shares a
     cause with. Headroom is not the risk: 26 -> 25 exemplars for
     `compbio_methods` and 18 -> 19 for `compbio_mechanism`, both above the
     15 floor `apply_marks()` warns at.

  6. `TODO.md` E6 is gated by `E1`, and no E1 exists -- not in TODO.md, not in
     any `.bak` of it, not in any document in the repo. The item under
     `## Next step` is the prerequisite E6 would need and carries no code, so
     this patch gives it the code `E1` and resolves the reference.
     **This is an inference, not a recovered fact.** If E1 was meant to be
     something else, the graph is still wrong and only the dangling pointer has
     been hidden. Flagged in the summary for that reason.

  7. The `## Next step` procedure. Its intent is right and unchanged -- the
     stats cards first, because they are where a standard is formed rather than
     inherited, and the draft reports second because `label` will offer their
     verdicts as press-enter defaults. Two of its five subtasks are unsafe as
     written:

     - "against its abstract" points at the `papers.sqlite` abstract, and §5.1
       records that abstract diverging materially from arXiv's v1 on three of
       four cards checked. There is also no network in the sandbox, so arXiv is
       not the fallback. `show_eprint.py` reads
       `ingest/cache/eprint/<id>.bin`, which is what the curator actually
       parsed, and all three stats cards have one (88KB, 151KB, 692KB).
     - Two of the three stats cards -- 2411.02771 and 2608.16017 -- are in D0's
       set of six built from a defective extraction window. On those two a
       card/source discrepancy may be an extractor artifact rather than a
       curator error, and a reader who does not know that will file the wrong
       finding. Named per card so the distinction survives.

     `show_eprint.py 2506.07459 --list` was run on 2026-09-04 and works, so
     §6 step 0 and E5's first subtask are marked done rather than left as
     never-run. It needs no network and mutates nothing.

WHAT IT DELIBERATELY DOES NOT DO

  It does not run `canon_tier.py apply`, `import`, `label` or `score`. All four
  mutate state, a sandbox holds a copy, and `label` is the user's handwriting
  under invariant 14 besides. The derivation in item 5 is read-only and
  transfers; the run does not.

  It does not touch `CARD-EVAL-HANDOFF.md` §5.3's KL-divergence
  misattribution. The orientation skill lists it as a known-false statement and
  it re-derives as false -- `trust region` is an alias on 2506.07459 line 49
  and 2608.17381 has no KL object -- but patch 1's ledger row says it already
  corrected §5.3, so a second correction needs a look at what patch 1 actually
  wrote before it is layered on. Left for the next pass rather than guessed at.

  It does not consolidate anything. That is D9, gated behind the first `score`
  run on purpose, and `dev-notes/notes-consolidation-plan.md` is explicit that
  consolidating against a state about to move is the wrong order.
"""

import argparse
import ast
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- doc edits

OLD_PS2 = """**Actual.** Four curators have run. 28 validated cards: `probability` 10,
`compbio_methods` 9, `compbio_mechanism` 6, `stats` 3. `card_eval.py` does not exist. See
§4.1 — this is the most consequential deviation in the project."""

NEW_PS2 = """**Actual.** Four curators have run. 28 validated cards: `probability` 10,
`compbio_methods` 9, `compbio_mechanism` 6, `stats` 3, re-derived from
`kb/*/cards/*.md` on 2026-09-04. `ingest/card_eval.py` is written and has never
been run — **check `ls eval/card_runs/` rather than trusting this sentence.** See
§4.1 — this is the most consequential deviation in the project.

*Corrected 2026-09-04: this paragraph said `card_eval.py` did not exist. It is
64,177 bytes and answers `--help`. The orientation skill filed the same sentence
in `CLAUDE.md` line 13 as D1 and did not know it was here too.*"""

OLD_PS_GIT = """1. **`git init && git add -A && git commit`** **[shell]**. Thirty seconds. It has already
   cost the project two unrecoverable changes (§4.3). Do this before any further edits, so
   today's work is the first commit rather than part of an untracked pile."""

NEW_PS_GIT = """1. ~~**`git init && git add -A && git commit`**~~ — **done.** `git log` shows ten
   commits through `d8e8602` "patch 5", and `git status` is clean. The two
   unrecoverable changes in §4.3 are still lost; everything since is recoverable."""

OLD_PS_CANON = """5. **`python3 ingest/canon_tier.py apply`** **[shell]**, then re-render exemplars. Today's
   `compbio_mechanism` worksheet edits — two strike reversals and ten rewritten reasons —
   are inert until this runs. The two reversed papers are still eligible for the negative
   block, which is the exact contradiction the ruling removed."""

NEW_PS_CANON = """5. **`python3 ingest/canon_tier.py apply`** **[shell]**, then re-render exemplars.
   Worksheet edits are inert until this runs. **Delta re-derived 2026-09-04 by
   replicating `apply_marks()` read-only against `canon.jsonl`, and it is wider
   than this item said** — `apply_marks()` globs every `vetting-*.md`:

   | Worksheet | Marks | Reasons |
   |---|---|---|
   | `compbio_mechanism` | 1 — W1993482030 struck → **exemplar** | 1 |
   | `compbio_methods` | 2 — W2178011284 struck → kept; **W2050834445 exemplar → kept** | 3 |
   | `stats` | 0 | 1 |
   | `probability` | 0 | 0 |

   Read `TODO.md` D7 before running it. The `compbio_methods` exemplar demotion
   changes the triage positive block, and triage is the one measured component
   here — so this is now paired with Tier 3 item 10 rather than standing alone.

   *Corrected 2026-09-04: this item said two strike reversals and ten rewritten
   reasons in `compbio_mechanism`. It is one mark and one reason there; the
   second reversal is in `compbio_methods`, alongside a demotion and three
   reasons that no list mentioned.*"""

OLD_CLAUDE_L5 = """Read `PROJECT-STATUS.md` for current state and next actions. `research-network-architecture.md` has the full design and cost model. `WEEK-1-PLAN.md` is the active phase. `HYBRID-SYSTEM-REVIEW.md` is why invariants 13–16 exist and `DISTORTION-REVIEW.md` is why 17–19 do; read the relevant one before touching either group."""

NEW_CLAUDE_L5 = """Read `TODO.md` for the next action and `PROJECT-STATUS.md` for current state. `OPEN-QUESTIONS.md` is the decision register — check it before re-opening a settled question. `research-network-architecture.md` has the full design and cost model. `HYBRID-SYSTEM-REVIEW.md` is why invariants 13–16 exist and `DISTORTION-REVIEW.md` is why 17–19 do; read the relevant one before touching either group. **The week plans and the handoffs are superseded records, not current state — do not take a next action from one.**"""

OLD_CLAUDE_L13 = """Before enabling anything further: card extraction has never been measured — card_eval.py does not exist, so the phasing gate "the schema stops moving" has not been passed. Each gate goes live only after the user has personally audited its judgment for two weeks."""

NEW_CLAUDE_L13 = """Before enabling anything further: card extraction has never been measured. `ingest/card_eval.py` is written but has never been run — **check whether `eval/card_runs/` is empty rather than trusting this sentence**, which is exactly the kind of claim that goes stale. Until a run exists, the phasing gate "the schema stops moving" has not been passed. Each gate goes live only after the user has personally audited its judgment for two weeks."""

OLD_CE6 = """With six of twenty-one judged, `score` will be thin — but running it now surfaces
crashes and shows whether the provenance and error-type blocks read usefully,
which is worth more at this stage than the numbers."""

NEW_CE6 = """With five of twenty judged, `score` will be thin — but running it now surfaces
crashes and shows whether the provenance and error-type blocks read usefully,
which is worth more at this stage than the numbers.

*Corrected 2026-09-04: read "six of twenty-one". §1 corrected those figures on
2026-09-03 and patch 5 rewrote §3's table to match; this sentence was missed, so
the stale pair sat in the action list while the corrected pair sat above it.
Re-derived: 20 records in `card_labels.jsonl`, 5 passing `_is_judged`.*"""

OLD_CE6_STEP0 = """# 0. smoke-test the new tool (never run)
python3 ingest/show_eprint.py 2506.07459 --list"""

NEW_CE6_STEP0 = """# 0. smoke-test the new tool — DONE 2026-09-04, works. No network needed.
python3 ingest/show_eprint.py 2506.07459 --list"""

# --------------------------------------------------------------- TODO.md: next step

OLD_NEXT = """- [ ] Read the stats cards and draft reports before labelling anything ~2h
  - [ ] Read `kb/stats/cards/2512.16061.md` against its abstract ~20m
  - [ ] Read `kb/stats/cards/2411.02771.md` against its abstract ~20m
  - [ ] Read `kb/stats/cards/2608.16017.md` against its abstract ~20m
  - [ ] Audit the quote inventory in `eval/drafts/2606.07914-report.md` ~30m
  - [ ] Read the other three reports in `eval/drafts/` ~30m

  Statistics is the domain you can referee unaided, so the stats cards come
  first — they are where you form a standard rather than inherit one. The draft
  reports come second because `label` will offer their verdicts as press-enter
  defaults. Take 2606.07914 first of those: `CARD-EVAL-HANDOFF.md` §4 records
  four of its citations pointing at sentences that did not establish the claim,
  and its report predates the quote-inventory fix, so the handoff says treat
  them as leads. The goal is not a verdict but the capacity to disagree with
  one — `score_run()` warns that a run with zero overrides is uninterpretable,
  and that is the likely outcome of labelling cold."""

NEW_NEXT = """- [ ] **E1.** Read the three stats cards and four draft reports before labelling ~2h
  - [x] Smoke-test `python3 ingest/show_eprint.py 2506.07459 --list` ~5m
  - [ ] Read `kb/stats/cards/2512.16061.md` against `show_eprint.py 2512.16061` ~20m
  - [ ] Read `kb/stats/cards/2411.02771.md` — D0: its intro came back empty ~20m
  - [ ] Read `kb/stats/cards/2608.16017.md` — D0: its "Summary" was missed ~20m
  - [ ] Audit the quote inventory in `eval/drafts/2606.07914-report.md` ~30m
  - [ ] Read the other three reports in `eval/drafts/` ~30m

  Statistics is the domain you can referee unaided, so the stats cards come
  first — they are where you form a standard rather than inherit one. The draft
  reports come second because `label` will offer their verdicts as press-enter
  defaults. Take 2606.07914 first of those: `CARD-EVAL-HANDOFF.md` §4 records
  four of its citations pointing at sentences that did not establish the claim,
  and its report predates the quote-inventory fix, so the handoff says treat
  them as leads. The goal is not a verdict but the capacity to disagree with
  one — `score_run()` warns that a run with zero overrides is uninterpretable,
  and that is the likely outcome of labelling cold.

  Read each card against the **cached e-print**, not the `papers.sqlite`
  abstract. §5.1 found that abstract diverging materially from arXiv's v1 on
  three of four cards checked, and there is no network here, so arXiv is not the
  fallback either. `show_eprint.py` reads what the curator actually parsed; all
  three stats cards have a `.bin` and the tool was verified working 2026-09-04.

  Two of the three are in D0's defective-window set, which is why they are named
  separately above: on 2411.02771 and 2608.16017 a discrepancy between card and
  source may be the extractor's, not the curator's. Scoring either `n` for
  absence without checking the window first files a curator defect against an
  extraction bug — and 2411.02771's intro was reported as found while coming
  back empty, so the card was built without it.

  Numbered `E1` on 2026-09-04 because E6 is gated by an `E1` that exists nowhere
  in the repo and this is the prerequisite it needs. **Confirm that reading** —
  if E1 meant something else, the gate graph is still wrong."""

# --------------------------------------------------------------- TODO.md: backlog

OLD_D1 = """- [ ] **D1.** Fix the two false statements in `CLAUDE.md`

  Line 5 names `WEEK-1-PLAN.md` as the active phase when `PROJECT-STATUS.md`
  supersedes `WEEK-3-PLAN.md`; line 13 says `card_eval.py` does not exist. It is
  the file every agent reads first, so both misinform every agent at boot.
  Replacement text in `dev-notes/curator-prompt-edits-pending.md` §10. Five
  minutes, and already Tier 0 item 4."""

NEW_D1 = """- [ ] **D1.** Fix the false statements about `card_eval.py` and the phase —
  **APPLIED by patch 6, 2026-09-04**

  Both `CLAUDE.md` lines are corrected with §10's staged text verbatim: line 5
  now points at `TODO.md` and `PROJECT-STATUS.md` and says the week plans are
  records, line 13 now says `card_eval.py` is written-but-never-run and tells
  the reader to check `eval/card_runs/` instead of believing the sentence.

  **A third instance was found and fixed in the same run.** `PROJECT-STATUS.md`
  §2 carried "`card_eval.py` does not exist" as well — the top of the
  supersession chain, and outside this item's stated scope, so applying D1 as
  filed would have left the phase document asserting it. The lesson is the
  filing one: a false sentence was located once, in the file where it was first
  noticed, and never grepped for elsewhere."""

OLD_D7 = """- [ ] **D7.** Run `python3 ingest/canon_tier.py apply`, then re-render exemplars

  The `compbio_mechanism` worksheet edits — two strike reversals and ten
  rewritten reasons — are inert until this runs, and the two reversed papers are
  still eligible for the negative block (`PROJECT-STATUS.md` Tier 0 item 5)."""

NEW_D7 = """- [ ] **D7.** Apply the canon worksheet marks, and record what moves in the
  triage prompt

  **Delta re-derived 2026-09-04** by replicating `apply_marks()` read-only
  against `canon.jsonl`. This item said two strike reversals and ten rewritten
  reasons in `compbio_mechanism`. That is not what is pending:

  | Worksheet | Marks | Reasons |
  |---|---|---|
  | `compbio_mechanism` | 1 — W1993482030 *Tensor-Train Decomposition*, struck → **exemplar** | 1 |
  | `compbio_methods` | 2 — W2178011284 struck → kept; **W2050834445 exemplar → kept** | 3 |
  | `stats` | 0 | 1 |
  | `probability` | 0 | 0 |

  `apply_marks()` globs every `vetting-*.md`, so one run applies all of it —
  including five changes across two domains that no list here mentioned.

  **The decision, and it is why this is no longer a chore.** W2050834445
  (Donoho, minimal L1 = sparsest) is a live tier-0 exemplar for
  `compbio_methods` and the worksheet demotes it. Exemplars are the model's
  entire contact with the canon; triage is the only measured component in this
  project (recall 0.903 / precision 0.699, `eval/runs/20260827-214656`); and
  §4.6 already records part of that precision gain tracing to a prompt edit
  nobody wrote down. Applying this silently makes the next triage run
  non-comparable to that baseline for the same reason, one layer along. So
  either accept the demotion and record it, or leave the mark alone — but decide
  rather than discover it later.

  Cron is off, so nothing is being contaminated while this waits. That is what
  keeps it off `## Next step`.

  Headroom is not the risk: `compbio_methods` 26 → 25 exemplars,
  `compbio_mechanism` 18 → 19, both above the 15 floor `apply_marks()` warns at.

  - [ ] `python3 ingest/canon_tier.py apply` **[shell]**, then re-render exemplars
  - [ ] Record the `compbio_methods` exemplar change with Tier 3 item 10's
        `triage.md` reconstruction — same cause, same sitting
  **Gates:** Tier 3 item 10 (`OPEN-QUESTIONS.md` §1.7)"""

OLD_D8 = """- [ ] **D8.** Add an optional `strike_superseded` field to `ingest/canon_index.py`

  So `exemplars()` skips overruled strike reasons, keeping the vetting record
  intact while keeping a reversed judgment out of the triage prompt
  (`EVAL-01-FINDINGS.md` B2, ~5 lines)."""

NEW_D8 = """- [x] **D8.** Add an optional `strike_superseded` field to `ingest/canon_index.py`
  — **ALREADY IMPLEMENTED; closed 2026-09-04**

  `exemplars()` excludes `strike_superseded` records from `neg_pool` directly,
  and its docstring carries the EVAL-01 §4B reasoning. `PROJECT-STATUS.md` §3
  recorded this as landed "at some point"; this item did not know, so it sat
  open next to a status row saying it was done.

  **One caveat survives the close.** Exactly one record in `canon.jsonl` sets
  the field, and it is a `stats` record. The code path has never been exercised
  on `compbio_mechanism` — the domain D7 touches — and a reversal there is
  expressed by changing `mark:` in the worksheet, not by setting this field.
  The two mechanisms are independent; do not assume D7 exercises this one."""

OLD_E6_GATE = """  **Gated by:** E1, E3, E4, E5, D4. **Gates:** E7, D9, and everything in the
  phasing table from Week 4 on."""

NEW_E6_GATE = """  **Gated by:** E1 (the `## Next step` item), E3, E4, E5, D4. **Gates:** E7, D9,
  and everything in the phasing table from Week 4 on.

  *E1 had no referent anywhere in the repo until 2026-09-04, when the next-step
  item was given that code. Confirm the reading — if E1 meant something else,
  this gate is still wrong.*"""

OLD_E5_SMOKE = """  - [ ] `python3 ingest/show_eprint.py 2506.07459 --list`"""

NEW_E5_SMOKE = """  - [x] `python3 ingest/show_eprint.py 2506.07459 --list` — run 2026-09-04, works"""

OLD_DN10 = """## 10. `CLAUDE.md` — two false statements in the file every agent reads first

**Status:** pending · **do this one first.** It is the cheapest item here and the
only one that misinforms every agent at boot."""

NEW_DN10 = """## 10. `CLAUDE.md` — two false statements in the file every agent reads first

**Status: APPLIED by patch 6, 2026-09-04.** Both edits below went in verbatim.
A third instance of Edit B's false sentence was found in `PROJECT-STATUS.md` §2
and corrected in the same run — it was outside this item's scope, which is why
nothing had caught it.

`CLAUDE.md` is not in `settings.json`'s deny list, so this never actually needed
hand application. It sat in the `.claude/**` queue by filing convention. Worth
remembering for the next item filed here: check the deny list before assuming a
path needs the slow route."""

TEXT_EDITS = [
    ("PROJECT-STATUS.md", "§2: drop the card_eval.py falsehood", OLD_PS2, NEW_PS2),
    ("PROJECT-STATUS.md", "Tier 0 item 1: git is done", OLD_PS_GIT, NEW_PS_GIT),
    ("PROJECT-STATUS.md", "Tier 0 item 5: real canon delta", OLD_PS_CANON, NEW_PS_CANON),
    ("CLAUDE.md", "line 5: phase pointer (§10 Edit A)", OLD_CLAUDE_L5, NEW_CLAUDE_L5),
    ("CLAUDE.md", "line 13: card_eval.py (§10 Edit B)", OLD_CLAUDE_L13, NEW_CLAUDE_L13),
    ("CARD-EVAL-HANDOFF.md", "§6: five of twenty, not six of 21", OLD_CE6, NEW_CE6),
    ("CARD-EVAL-HANDOFF.md", "§6 step 0: smoke test done", OLD_CE6_STEP0, NEW_CE6_STEP0),
    ("TODO.md", "Next step: e-print reads, D0 flags, E1", OLD_NEXT, NEW_NEXT),
    ("TODO.md", "D1: applied, plus the third instance", OLD_D1, NEW_D1),
    ("TODO.md", "D7: real delta and the exemplar decision", OLD_D7, NEW_D7),
    ("TODO.md", "D8: close, already implemented", OLD_D8, NEW_D8),
    ("TODO.md", "E6: resolve the dangling E1 gate", OLD_E6_GATE, NEW_E6_GATE),
    ("TODO.md", "E5: smoke test done", OLD_E5_SMOKE, NEW_E5_SMOKE),
    ("dev-notes/curator-prompt-edits-pending.md", "§10: mark applied",
     OLD_DN10, NEW_DN10),
]


def _say(*args):
    """print() that survives a closed stdout, so `| head` cannot cancel a run."""
    try:
        print(*args)
    except BrokenPipeError:
        pass


def _preflight():
    """Re-derive every count this patch writes. Refuse if the repo disagrees."""
    problems = []

    ce = ROOT / "ingest" / "card_eval.py"
    if not ce.exists():
        problems.append("ingest/card_eval.py is missing -- this patch asserts it exists")
    else:
        try:
            ast.parse(ce.read_text())
        except SyntaxError as e:
            problems.append(f"ingest/card_eval.py does not parse (line {e.lineno}); "
                            "apply patch 3 first")

    cards = list((ROOT / "kb").glob("*/cards/*.md"))
    if len(cards) != 28:
        problems.append(f"expected 28 cards on disk, found {len(cards)}; "
                        "§2's re-derived count would be wrong")

    labels = ROOT / "eval" / "card_labels.jsonl"
    if labels.exists():
        n = sum(1 for line in labels.read_text().splitlines() if line.strip())
        if n != 20:
            problems.append(f"expected 20 label records, found {n}; "
                            "§6's corrected figure would be wrong")
    else:
        problems.append("eval/card_labels.jsonl is missing")

    ci = ROOT / "ingest" / "canon_index.py"
    if ci.exists() and "strike_superseded" not in ci.read_text():
        problems.append("canon_index.py has no strike_superseded; "
                        "this patch closes D8 on the grounds that it does")

    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change and exit without writing")
    ap.add_argument("--no-backup", action="store_true",
                    help="skip the .pre-patch6.bak copies")
    a = ap.parse_args()

    if not (ROOT / "ingest" / "card_eval.py").exists() and not (ROOT / "TODO.md").exists():
        sys.exit(f"not a research-net checkout: {ROOT}\n"
                 f"  run this from the repo root, as "
                 f"`python3 patches/{Path(__file__).name}`")

    problems = _preflight()
    if problems:
        _say("preflight failed -- this patch writes claims it cannot verify:")
        for p in problems:
            _say(f"  {p}")
        sys.exit("\nNothing written. Re-derive, then adjust the patch text to match\n"
                 "the artifact rather than adjusting the artifact to match the patch.")

    cache = {}
    todo, already, broken = [], [], []
    for rel, label, old, new in TEXT_EDITS:
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
        _say(f"  skip     {rel:<42} {label} (already applied)")
    for rel, label, why in broken:
        _say(f"  BLOCKED  {rel:<42} {label} -- {why}")
    for rel, label, _, _ in todo:
        _say(f"  apply    {rel:<42} {label}")

    if broken:
        sys.exit(f"\n{len(broken)} item(s) could not be matched. Nothing written.\n"
                 f"  Anchors are exact text from the post-patch-5 state.\n"
                 f"  Applied edits are detected and skipped, so a partial\n"
                 f"  hand-application followed by a re-run is safe.")
    if not todo:
        _say("\nnothing to do.")
        return
    if a.dry_run:
        _say(f"\n--dry-run: {len(todo)} edit(s) across "
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
            shutil.copy2(p, p.with_suffix(p.suffix + ".pre-patch6.bak"))
        p.write_text(staged[rel])

    for rel in touched:
        _say(f"  wrote    {rel}")
    _say(f"\n{len(todo)} edit(s) across {len(touched)} file(s).")

    readme = ROOT / "patches" / "README.md"
    if readme.exists() and "patch-06" not in readme.read_text():
        _say("\n  NOTE  patches/README.md's ledger has no patch 6 row. The ledger")
        _say("        is the order of record -- add it before committing.")

    _say("\nVerify:")
    _say("  sed -n '/^## Next step/,/^## Backlog/p' TODO.md   # what pmd will surface")
    _say("  grep -n 'card_eval.py does not exist' CLAUDE.md PROJECT-STATUS.md  # expect none")
    _say("  grep -n 'six of twenty-one' CARD-EVAL-HANDOFF.md                   # expect none")
    _say("  grep -n 'D7\\|D8\\|E1' TODO.md | head -20")
    _say("  git status --short && git diff --stat")
    _say("\nStill yours, and unchanged by this patch:")
    _say("  canon_tier.py apply  -- decide the W2050834445 demotion first (D7)")
    _say("  import / label / score -- state-mutating, and label is your handwriting")
    _say("\nThen commit. The .pre-patch6.bak files are redundant once you have.")


if __name__ == "__main__":
    main()
