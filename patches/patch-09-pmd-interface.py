#!/usr/bin/env python3
"""Patch 9 (2026-09-04): the pmd interface, written down, plus a pickup state.

    python3 patches/patch-09-pmd-interface.py --dry-run
    python3 patches/patch-09-pmd-interface.py

**Requires patches 1-8 and refuses to run without patch 7**, whose text two of
the edits below anchor on.

WHAT PMD IS, AND WHAT THIS PATCH IS NOT

`pmd` is an external dashboard. Once a day it reads this repo and extracts one
thing -- the next step -- by trying four rungs in order: `.pmd/collect`, then
`.pmd.conf`, then a `## Next step` heading (or the first unchecked box) in
`TODO.md`/`NOTES.md`/`TASKS.md`/`NEXT.md`/`README.md`, then nothing.

**This repo already sits on rung 3 and already parses.** Verified before
writing anything: `TODO.md` line 27 carries the heading, pmd resolves E1 as the
step, six subtasks and 23 context lines beneath it, 30 open items, and a
`## Backlog` heading it counts from. So this patch adds **no `.pmd.conf` and no
`.pmd/collect`** -- rung 3 is the lowest-effort rung and it fits, `research-net`
is a stable directory name so `id` buys nothing, and a collect script is a thing
the user then has to maintain.

What was actually wrong is narrower and worse: **the contract was maintained by
eye.** One sentence in `TODO.md`'s header described it, nothing checked it, and
patch 7 broke it four hours after being written -- two of E1's subtasks became
wrapped two-line entries, so their continuation lines parse as *context* and
their `~20m` markers sit on lines that are not boxes. Neither the author nor
the reviewer saw it. `patches/pmd_check.py`, shipped with this patch, saw it
immediately.

That is the shape of the whole problem. A dashboard parse fails silently and
its failure mode is a blank, which is indistinguishable from a project with
nothing to do.

WHAT IT DOES

  1. `TODO.md` header: replaces the one-sentence description with the contract
     -- the four rungs, the shape rules, the character limit, where estimates
     must sit, and the one failure mode that blanks the dashboard. Closing the
     next step without promoting a backlog item in the same edit leaves the
     heading present and empty, and an empty heading is worse than no heading:
     with no heading pmd falls back to the first unchecked box anywhere and
     still reports something; with an empty one there is nothing to fall back
     to. That is what "finishing a task" looks like from the inside, which is
     why it needs writing down rather than remembering.

  2. `TODO.md` E1: the two wrapped subtasks, rewritten to one line each with
     the estimate back on the box line.

  3. `TODO.md` E1: an actor line. E1 is a task no session may perform --
     `.claude/skills/orientation/SKILL.md` forbids drafting verdicts for stats
     cards, because a drafted verdict is an inherited standard and E1 exists to
     form one. A session reading `TODO.md` step 2 of the orientation order gets
     "read the three stats cards" as the live task with nothing saying it is not
     theirs. The line goes in the *prose*, not the step line: sessions read the
     whole file, pmd hides everything under the step, and the step line has 12
     characters of headroom that are not worth spending on a marker the
     dashboard's only reader does not need.

  4. `TODO.md` D10: consume the patch queue. Nine patch files sit in
     `patches/` and none has been deleted; `patches/README.md` says patches are
     consumed, not maintained, and that a gap in the numbering is the record.
     Real pending work with a documented rule behind it, and the queue is also
     the thing a next session most needs to see before it starts.

  5. `PROJECT-STATUS.md` §3: three rows -- the pmd interface, the patch queue,
     and git. §3 is the verified-state table and orientation's own rule is that
     a fact belongs there rather than in the router.

  6. `patches/README.md`: ledger rows 8 and 9, and `pmd_check.py` under
     "Not a patch".

  7. `dev-notes/curator-prompt-edits-pending.md`: the inventory row for item 10
     still reads "pending -- **highest value on this list**" while §10's body
     says "APPLIED by patch 6". Patch 6 updated the body and not the table it is
     indexed from -- the same one-place fix the D1 lesson is about, committed by
     the patch that recorded the lesson. Fixed, and item 11 filed with the
     orientation-skill edits this session needs, since `.claude/**` is applied
     by hand.

WHAT IT DELIBERATELY LEAVES UNDONE

  - **It does not change which item is `## Next step`.** There is an argument
    that it should: patch 7 rewrites E1's own subtasks, so applying 7 gates E1,
    and the patch queue is a ten-minute job where E1 is two hours. But by the
    time this patch runs 7 and 8 are applied, so the gate is discharged, and
    which item the dashboard surfaces is the user's ruling. pmd's own
    instruction is not to invent a next step. D10 sits in the backlog where it
    can be promoted with a one-line edit.
  - **No `.pmd.conf`, no `.pmd/collect`.** Reasoning above. If `TODO.md` ever
    stops being the file where work is tracked, rung 2 is the answer and it is
    four lines.
  - **It does not edit `.claude/skills/orientation/SKILL.md`.** That tree is
    hand-applied. The text is staged as item 11.
  - **It does not commit.** Patch 6 is still uncommitted; D10 covers it.
  - **It does not touch the three stale sandbox claims** in `WEEK-2-PLAN.md`,
    `WEEK-3-PLAN.md` and `WEEK-3-HANDOFF.md`. Grepped for deliberately, after
    patch 7 corrected the live one in `PROJECT-STATUS.md`: those three are
    superseded records, `CLAUDE.md` now says so in as many words, and
    `ESCALATION-REVIEW.md` §118's version is a true statement about a past
    session's conditions. `OPEN-QUESTIONS.md`'s note was already correct before
    this session. So there is no ungrepped live duplicate -- which is the check
    D1 failed to do, run here and recorded as having been run.
"""

import argparse, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUFFIX = ".pre-patch9.bak"

# ------------------------------------------------- 1. the contract, written

HEADER_OLD = """Read by `pmd` once a day, which surfaces the item under `## Next step` and hides
its subtasks and context behind a click. Keep exactly one unchecked top-level box
there: a short imperative title, the procedure in indented subtasks, the
reasoning in indented prose beneath. Backlog items are counted but never
surfaced — promote one up when it becomes the next thing.
"""

HEADER_NEW = """Read by `pmd` once a day, which surfaces the item under `## Next step` and hides
its subtasks and context behind a click. Keep exactly one unchecked top-level box
there: a short imperative title, the procedure in indented subtasks, the
reasoning in indented prose beneath. Backlog items are counted but never
surfaced — promote one up when it becomes the next thing.

### The pmd contract — it is a parse, so treat it like one

`pmd` resolves a next step by trying four rungs and taking the first hit:
`.pmd/collect`, then `.pmd.conf`, then a `## Next step` heading — or failing
that the first unchecked box — in `TODO.md`, `NOTES.md`, `TASKS.md`, `NEXT.md`
or `README.md`, then nothing. **This repo is on rung 3 and deliberately has no
`.pmd.conf`**: rung 3 is the lowest-effort rung that fits, and a config file
would be one more thing to keep true. Verify with `python3
ingest/pmd_check.py`, which implements the resolution and exits non-zero if
this file no longer parses.

The rules, and each one is a way the parse fails rather than a style
preference:

- **Exactly one unchecked top-level box under `## Next step`.** pmd takes the
  first; a second is invisible rather than queued.
- **Never leave the heading with zero unchecked boxes.** This is the failure
  that blanks the dashboard, and it is what finishing a task looks like from
  the inside. With *no* heading pmd falls back to the first unchecked box
  anywhere in the file and still reports something; with the heading present
  and empty there is nothing to fall back to. **Close the next step and promote
  a backlog item in the same edit, never in two.**
- **The step line is a title, under 90 characters**, one imperative clause, no
  colon introducing a procedure and no rationale. It is the only line the
  dashboard shows.
- **One subtask per line.** A wrapped continuation line is not a box, so it
  parses as context and any `~estimate` on it is lost. Patch 7 broke this on
  two of E1's subtasks and patch 9 repaired it; `pmd_check.py` exists because
  neither the author nor the reviewer noticed.
- **Estimates go on the box line** — `~30m`, `~6h`, `~3d`, `~2w`; days are 8h,
  weeks 40. The top-level one is the one that matters; subtask estimates only
  where there is a basis.
- **Actor.** Some items only the user can do — labelling, anything under
  `[shell]` that needs the network, `.claude/**` edits. Say so in the prose
  beneath, not in the step line: a session reads the whole file and pmd hides
  everything under the step, so the step line should not spend characters on a
  marker its only reader does not need.
"""

# ---------------------------------------------- 2. the wrapped subtask fix

WRAPPED_OLD = """  - [ ] Read `kb/stats/cards/2411.02771.md` — window changed most; read the
        window note below before scoring anything `n` ~20m
  - [ ] Read `kb/stats/cards/2608.16017.md` — gained a 1,451-char conclusion
        the curator never saw ~20m
"""

WRAPPED_NEW = """  - [ ] Read `kb/stats/cards/2411.02771.md` — window note below first ~20m
  - [ ] Read `kb/stats/cards/2608.16017.md` — window note below first ~20m
"""

# --------------------------------------------------------- 3. actor line

ACTOR_OLD = """  - [ ] Read the other three reports in `eval/drafts/` ~30m

  Statistics is the domain you can referee unaided, so the stats cards come
"""

ACTOR_NEW = """  - [ ] Read the other three reports in `eval/drafts/` ~30m

  **Yours, and not delegable.** A session may pull quotes, run
  `ingest/window_diff.py`, and say where a claim sits in the source. It may not
  supply verdicts for stats cards — `.claude/skills/orientation/SKILL.md`
  forbids it, because `import` turns a drafted verdict into a press-enter
  default and E1 exists to form a standard rather than inherit one. A session
  that reads this item as its own task is about to manufacture the zero-override
  run `score_run()` reports as uninterpretable.

  Statistics is the domain you can referee unaided, so the stats cards come
"""

# ------------------------------------------------------------ 4. D10

D10_OLD = """- [ ] **D9.** Consolidate the status documents ~3h

  Per `dev-notes/notes-consolidation-plan.md`. Fifteen carry an action or
  decision list, three define "done", and a live blocking decision sits outside
  `OPEN-QUESTIONS.md`.
  **Gated by:** E6 — deliberately, since that run is expected to produce a bug
  list which is itself content for these files.
"""

D10_NEW = """- [ ] **D9.** Consolidate the status documents ~3h

  Per `dev-notes/notes-consolidation-plan.md`. Fifteen carry an action or
  decision list, three define "done", and a live blocking decision sits outside
  `OPEN-QUESTIONS.md`.
  **Gated by:** E6 — deliberately, since that run is expected to produce a bug
  list which is itself content for these files.

- [ ] **D10.** Consume the patch queue and commit ~30m **[shell]**

  - [ ] `git mv patches/window_diff.py ingest/window_diff.py`
  - [ ] `git mv patches/pmd_check.py ingest/pmd_check.py`
  - [ ] `git add -A && git commit` — patch 6 has been applied and uncommitted
        since 2026-09-04
  - [ ] Delete patches 1–9 once committed, leaving the ledger rows

  Ungated, and the first thing a session should look at before anything else:
  `patches/README.md`'s ledger is the authority on what is applied and what is
  merely written, and `Applied: pending` there means the code on disk is not
  what the documents describe.

  Nine patch files are in `patches/` and none has been deleted, against that
  file's own rule — *"Patches are consumed, not maintained. Once applied and
  committed, a patch is a record; delete it when its content has landed in the
  documents it edited"* — with the numbering gap as the surviving record. The
  two diagnostics are the exception and must be moved rather than deleted:
  they are run, not applied, and they outlive the patches that delivered them.

  The commit is `PROJECT-STATUS.md` §5 Tier 0 item 1, which reads as done
  because `git log` shows ten commits. It was done, and then five files were
  modified without one.
"""

# ------------------------------------------- 5. PROJECT-STATUS §3 rows

PS_OLD = """| `strike_superseded` | Implemented in `canon_index.py` (EVAL-01 §4B/B2 landed at some point) |
"""

PS_NEW = """| `strike_superseded` | Implemented in `canon_index.py` (EVAL-01 §4B/B2 landed at some point) |
| `pmd` interface | Rung 3, live and parsing. `TODO.md` line 27 heading; pmd resolves E1, 6 subtasks, 30 open items, `## Backlog` counted. No `.pmd.conf` by decision — rung 3 fits and a config file is one more thing to keep true. Contract written into `TODO.md`'s header 2026-09-04 and checkable with `python3 ingest/pmd_check.py`, which exits 1 if the parse breaks. It broke once, four hours after being documented — patch 7's wrapped subtasks, repaired by patch 9 |
| Patch queue | **The authority is `patches/README.md`'s ledger, not this row.** `Applied: pending` there means the code on disk is not what the documents describe. As of 2026-09-04: 1–6 applied, 7–9 written and verified against a scratch copy, 6 applied-but-uncommitted. Two diagnostics staged in `patches/` awaiting `git mv` into `ingest/`: `window_diff.py`, `pmd_check.py` |
| Git | Ten commits through `d8e8602` "patch 5". **Working tree dirty since 2026-09-04** — patch 6's five modified files and its `.pre-patch6.bak` set, uncommitted. Tier 0 item 1 reads as done and is no longer. `TODO.md` D10 |
"""

# ------------------------------------------------- 6. patches ledger

LEDGER_OLD = """### Not a patch

`window_diff.py` is a **diagnostic** — run, not applied — and per the rule above
it is unnumbered and belongs in `ingest/`, moved as part of patch 7:
"""

LEDGER_NEW = """| 8 | `patch-08-failure-modes.py` | pending | `ingest/validate_card.py`, `ingest/rebuild_index.py`, `ingest/card_eval.py`, `ingest/audit_extraction.py` | Separates three failures that reported identically. `validate_card.py` gains exit 3 for environment/invocation failure so a missing `pyyaml` no longer reads as 28 invalid cards, and a path that is not a file is reported instead of skipped — an unexpanded glob used to print `all cards valid` and exit 0. `rebuild_index.py`'s shared import re-raises as the same 3. `_ask()` treats EOF as `q` rather than a traceback mid-labelling. `audit_extraction.py`'s footer no longer claims an empty section that patch 2 closed is still open. Invariant 17's exit-2-vs-1 ruling, applied where it was not written. 6 edits, 4 files. |
| 9 | `patch-09-pmd-interface.py` | pending | `TODO.md`, `PROJECT-STATUS.md`, `patches/README.md`, `dev-notes/curator-prompt-edits-pending.md` | Writes the `pmd` dashboard contract into `TODO.md`'s header as a parse with named failure modes, repairs the two wrapped subtasks patch 7 introduced, adds an actor statement to E1, files D10 for the patch queue and the commit, adds three verified-state rows to `PROJECT-STATUS.md` §3, and corrects the inventory row for dev-note item 10 which patch 6 left contradicting its own body. Ships `pmd_check.py`. Adds no `.pmd.conf`: rung 3 fits. 7 edits, 4 files. |

### Not a patch

`pmd_check.py` is a **diagnostic** and belongs in `ingest/`, moved as part of
patch 9:

```bash
git mv patches/pmd_check.py ingest/pmd_check.py
```

It implements `pmd`'s documented resolution and validates `TODO.md` against the
contract now recorded in that file's header — one unchecked top-level box, a
step line under 90 characters, one subtask per line, estimates on the box line
— exiting 1 when the dashboard would show nothing or the wrong thing and 3 when
it cannot tell. The exit codes match `validate_card.py`'s after patch 8, for
the same reason. It earned its place before it was committed: patch 7 broke the
subtask rule and this script found it, where two readings by eye had not.

`window_diff.py` is a **diagnostic** — run, not applied — and per the rule above
it is unnumbered and belongs in `ingest/`, moved as part of patch 7:
"""

# -------------------------------------- 7. dev-note inventory + item 11

DEVNOTE_OLD = """| 10 | Two false statements about current state | `CLAUDE.md` lines 5, 13 | PROJECT-STATUS Tier 0 item 4; ESCALATION-REVIEW #3 | pending — **highest value on this list** |
"""

DEVNOTE_NEW = """| 10 | Two false statements about current state | `CLAUDE.md` lines 5, 13 | PROJECT-STATUS Tier 0 item 4; ESCALATION-REVIEW #3 | **applied by patch 6, 2026-09-04** |
| 11 | Router edits: pmd contract, patch ledger, trap-list corrections | `.claude/skills/orientation/SKILL.md` | this session | pending — see §11 |

*Row 10 corrected 2026-09-04. It read "pending — **highest value on this
list**" while §10's own body had said "APPLIED by patch 6" since that patch ran.
Patch 6 updated the body and not the table the body is indexed from, which is
the D1 lesson — a fact fixed in the one place it was noticed — committed by the
patch that recorded the lesson.*
"""

ITEM11_ANCHOR = """## Context: the §7.1 ruling that item 4 implements"""

ITEM11_TEXT = """## 11. `orientation/SKILL.md` — the router, after the 2026-09-04 session

Three edits. The skill is the first thing a cold session reads, and two of its
trap entries have become folklore: the tasks behind them have landed, so the
entries now warn about sentences that no longer exist. Its own maintenance rule
says to **delete rather than update** an entry when its task lands, and that an
entry with no task behind it is not a trap but a fact.

### Edit A — delete two entries from "Statements known to be false"

Both are `D1`, applied by patch 6 on 2026-09-04. Delete these two bullets:

- the `CLAUDE.md` line 5 bullet — names `WEEK-1-PLAN.md` as the active phase
- the `CLAUDE.md` line 13 bullet — says `card_eval.py` does not exist

Line 5 now points at `TODO.md` and `PROJECT-STATUS.md` and says the week plans
are records; line 13 now says `card_eval.py` is written-but-never-run and tells
the reader to check `eval/card_runs/` instead of believing the sentence.

### Edit B — replace the `OPEN-QUESTIONS.md` environment bullet

It quotes *"the Linux sandbox will not start on this machine, so anything marked
**[shell]** has to run on your side."* That sentence is not in
`OPEN-QUESTIONS.md`; the note there already reads "test this rather than
believing it" and carries both caveats. The trap is now in the router only.
Replace the bullet with:

> - **Any "the sandbox does not start" claim.** Test it. It has been false in
>   at least two sessions (2026-09-03 read-only; 2026-09-04 the whole eval
>   path). `PROJECT-STATUS.md`'s copy was corrected by patch 7 and
>   `OPEN-QUESTIONS.md`'s was already right; the three surviving copies are in
>   `WEEK-2-PLAN.md`, `WEEK-3-PLAN.md` and `WEEK-3-HANDOFF.md`, which are
>   superseded records. Two constraints hold even when it starts: **no network**
>   — arXiv and OpenAlex work is the user's — and **no `pyyaml`/`jsonschema`
>   with `pip install` denied**, so `validate_card.py` and `rebuild_index.py`
>   cannot complete there and no card-validation claim made from that sandbox
>   means anything. A sandbox also holds a *copy*: state-mutating runs do not
>   transfer.

### Edit C — two lines into "Session-start checks"

The first because the ledger is the authority on whether the code on disk
matches the documents, and a session that starts without reading it can act on
a document a pending patch has not yet corrected. The second because the pmd
parse fails silently and its failure looks like a project with nothing to do.

```bash
grep -n 'pending' patches/README.md                       # patches written but not applied
python3 ingest/pmd_check.py                               # will the dashboard show anything
```

And in the reading order, after step 2 (`TODO.md`), add: *its header states the
`pmd` contract, which is a parse — `pmd_check.py` checks it, and closing the
next step without promoting a backlog item in the same edit blanks the
dashboard.*

### Not proposed

Nothing about the patch queue's *contents* goes in this file. The skill holds
reading order, supersession and traps, and a queue is state — it belongs in
`PROJECT-STATUS.md` §3, which patch 9 gives it. Adding it here would make the
router the seventeenth stale document, which is the thing it exists to prevent.

---

## Context: the §7.1 ruling that item 4 implements"""


EDITS = [
    ("TODO.md", HEADER_OLD, HEADER_NEW, "header: the pmd contract as a parse"),
    ("TODO.md", WRAPPED_OLD, WRAPPED_NEW, "E1: unwrap the two subtasks patch 7 broke"),
    ("TODO.md", ACTOR_OLD, ACTOR_NEW, "E1: actor statement"),
    ("TODO.md", D10_OLD, D10_NEW, "D10: consume the patch queue and commit"),
    ("PROJECT-STATUS.md", PS_OLD, PS_NEW, "§3: pmd interface, patch queue, git"),
    ("patches/README.md", LEDGER_OLD, LEDGER_NEW, "ledger rows 8-9 + pmd_check.py"),
    ("dev-notes/curator-prompt-edits-pending.md", DEVNOTE_OLD, DEVNOTE_NEW,
     "inventory row 10 -> applied; row 11 filed"),
    ("dev-notes/curator-prompt-edits-pending.md", ITEM11_ANCHOR, ITEM11_TEXT,
     "item 11: staged orientation-skill edits"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report only, touch nothing")
    a = ap.parse_args()

    # Patch 7 is a hard prerequisite: two anchors are its output.
    todo = (ROOT / "TODO.md")
    if todo.is_file() and "RUN 2026-09-04" not in todo.read_text():
        sys.exit("patch 7 has not been applied — TODO.md E5 is still open, and "
                 "two of this patch's anchors are patch 7's text.\n"
                 "  python3 patches/patch-07-eval-path-executed.py --dry-run")

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
        # afterwards, and testing `n_old` first would re-apply and duplicate.
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
        sys.exit("\nrefusing to write: preflight failed. Half-applying an edit to "
                 "TODO.md can leave `## Next step` with no unchecked box, which "
                 "blanks the dashboard silently — the exact failure this patch "
                 "documents.")

    if not plan:
        print("\nnothing to do — patch 9 is fully applied.")
        return

    if a.dry_run:
        print(f"\ndry run: {len(plan)} edit(s) across "
              f"{len(set(f for f, *_ in plan))} file(s), nothing written.")
        print("\nRun `python3 patches/pmd_check.py` before and after — it should "
              "go from exit 1 to exit 0.")
        return

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
    print("\nVerify:")
    print("  python3 patches/pmd_check.py        # expect exit 0, E1 as the line")
    print("\nThen D10, which this patch does not do:")
    print("  git mv patches/window_diff.py ingest/window_diff.py")
    print("  git mv patches/pmd_check.py ingest/pmd_check.py")
    print("  git add -A && git commit")
    print("\nAnd by hand, since .claude/ is not writable from a session:")
    print("  dev-notes/curator-prompt-edits-pending.md item 11")


if __name__ == "__main__":
    main()
