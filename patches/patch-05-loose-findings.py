#!/usr/bin/env python3
"""Patch 5 (2026-09-03): file the loose findings; install the orientation skill.

    python3 patches/patch-05-loose-findings.py --dry-run
    python3 patches/patch-05-loose-findings.py

Needs patches 1-4 applied. Housekeeping rather than machinery: everything here
was established during the 2026-09-03 session and existed only in conversation,
which is the failure mode `PROJECT-STATUS.md` §1 item 7 is about -- write the
reasoning down so a later reader can check it.

WHAT IT FILES

  1. `CARD-EVAL-HANDOFF.md` §1 and §3 disagree with `eval/card_labels.jsonl`.
     §3 says two cards are judged and four are "drafted, unimported". Five pass
     `_is_judged`; `drafted` is False on all five; and three that §3 lists as
     drafted-only -- 2606.07914, 2506.07459, 2601.03123 -- carry
     `labeller: user`. §1's claim that 2601.03123's marks were reset to null
     does not hold either. §3 is the table that says what is left to judge, so
     E6 reads it.

  2. Two of those five records have no `labeller` field at all, so they enter
     the headline figures unattributed while `score_run`'s own docstring says
     provenance travels with the number. That is a decision, not a correction,
     and it becomes TODO.md **E4a** -- a sibling of E4 under §7's heading,
     "settle these before the numbers mean anything".

  3. `RUNBOOK-first-measurement.md` Phase 0 is stale, and stale in the
     easy-to-miss direction: it is stale because the work is DONE, not because
     it needs repointing. Verified against `eval/labels.dev.jsonl` --
     `expect_in` 62, `expect_out` 86, `borderline` 32 = 180, `2608.07528` set
     to `expect_out`, zero `domain` nulls. So 0.2 and 0.3 are complete, and
     0.4's "do NOT rename labels.jsonl yet" was superseded when R8 was adopted
     on 2026-08-28 (`charters/compbio_methods.md` line 3). Anyone following it
     literally would run `fixup_labels_stratum_domain.py`, which hardcodes
     `eval/labels.jsonl`, against a path that no longer exists.

  4. Installs `.claude/skills/orientation/SKILL.md` from the staged copy in this
     directory, creating the directory and backing up any existing file. That
     tree is not writable from the assistant side, which is the whole reason
     this is a script you run.

  5. Removes `patches/patch-03-card-eval-domain.py` if it is still present. That
     file was renumbered to `patch-04` mid-session; keeping both leaves two
     scripts that apply the same `--domain` edits, one of which writes "APPLIED
     by patch 3" into TODO.md D4 and collides on `.pre-patch3.bak`.

WHAT IT DOES NOT FILE, AND WHY

  The `29b4cff` loose thread is closed rather than filed. That commit's
  two-paragraph-docstring defect looked like it might be a pattern -- TODO.md D5
  is the same mistake in markdown, applied the same day. It is not: all 26
  scripts under `ingest/` were parsed on 2026-09-03 and `card_eval.py` was the
  only failure. Nothing to check, so no task.

  `patches/README.md` is a drop-in replacement at its own path and needs no
  install step. This patch checks whether the ledger mentions patch 5 and says
  so if it does not.
"""

import argparse
import ast
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- doc edits

OLD_S1 = """`card_eval.py` is written and instrumented. **No cards have been scored yet** —
`score` has never been run and `eval/card_runs/` is empty. Two cards were judged
by hand before this session (2407.01051, 2410.16457); four more have **drafted**
verdicts sitting in `eval/drafts/`, unimported. Fifteen of the twenty-one sampled
cards have neither. The immediate next action is §6."""

NEW_S1 = """`card_eval.py` is written and instrumented. **Corrected 2026-09-03: the counts
that stood here were wrong, and so was §3's table.** Re-derived from
`eval/card_labels.jsonl` with `_is_judged`, the file holds **20** records of
which **5** are fully judged — 2407.01051, 2410.16457, 2606.07914, 2506.07459,
2601.03123 — and `drafted` is False on every one, so nothing was ever imported.
Three of those five were described here as drafted-only. Fifteen records are
untouched. See §3 for the table and E4a for the one open question it leaves.

Whether `score` has been run is answered by `ls eval/card_runs/`, not by this
paragraph; it was empty until 2026-09-03. The immediate next action is §6."""

OLD_S3 = """| # | arXiv ID | Domain | State |
|---|---|---|---|
| 1 | 2407.01051 | compbio_methods | **judged** (hand, pre-session) |
| 2 | 2410.16457 | probability | **judged** (hand, pre-session) — see §5.4, one ruling may need revisiting |
| 3 | 2606.07914 | probability | **drafted**, unimported |
| 4 | 2506.07459 | compbio_mechanism | **drafted**, unimported |
| 5 | 2601.03123 | compbio_methods | **drafted**, unimported; marks cleared |
| 6 | 2608.17381 | compbio_mechanism | **drafted**, unimported |
| 7–21 | — | — | **not drafted** (15 cards) |"""

NEW_S3 = """**Re-derived 2026-09-03 against `eval/card_labels.jsonl` and `_is_judged`.** The
table that stood here was wrong on three rows and on the total; what follows is
what the file contains.

| # | arXiv ID | Domain | `_is_judged` | `labeller` | `drafted` |
|---|---|---|---|---|---|
| 1 | 2407.01051 | compbio_methods | **yes** | *absent* | no |
| 2 | 2410.16457 | probability | **yes** | *absent* | no — see §5.4 |
| 3 | 2606.07914 | probability | **yes** | `user` | no |
| 4 | 2506.07459 | compbio_mechanism | **yes** | `user` | no |
| 5 | 2601.03123 | compbio_methods | **yes** | `user` | no |
| 6 | 2608.17381 | compbio_mechanism | no | — | no |
| 7–20 | — | — | no | — | no |

Four corrections, each of which mattered:

- **Five records are judged, not two.** Rows 3–5 were listed as "drafted,
  unimported" and are hand judgments. `drafted` is False on all twenty records,
  so `import` has never run on anything.
- **Row 5's marks were not cleared.** §1 recorded them reset to null at your
  request; it passes the all-fields test, so either the clearing did not happen
  or it was undone.
- **Twenty records, not twenty-one.** `sample` drew 20. D2 already flagged this
  half and it is the half that was right.
- **Rows 1 and 2 carry no `labeller`.** They predate the field and enter every
  figure unattributed. That is E4a, not a correction — it needs a ruling.

The four `<id>.json` / `<id>-report.md` pairs in `eval/drafts/` are still
unimported, and rows 3–5 having been judged by hand means importing them now
would land on cards you have already ruled on. `import` skips judged cards
unless `--force`, so the default is safe."""

OLD_RB = """### 0.2 Fix the label strata

```bash
python3 ingest/fixup_labels_stratum_domain.py
```"""

NEW_RB = """> **Phase 0 is COMPLETE. Verified 2026-09-03 — do not re-run 0.2 or 0.3.**
> `eval/labels.dev.jsonl` holds `expect_in` 62, `expect_out` 86, `borderline` 32
> = 180, `2608.07528` is `expect_out`, and no row has a null `domain`. So the
> script below has run and the hand-fix in 0.3 was made.
>
> Re-running it would fail rather than no-op: `fixup_labels_stratum_domain.py`
> hardcodes `eval/labels.jsonl`, and R8 renamed that file to
> `eval/labels.dev.jsonl` on 2026-08-28 — recorded in
> `charters/compbio_methods.md` line 3, handled in code by
> `eval_triage.py._resolve_labels`, and **not** reflected in 0.3 or 0.4 below.
> Read the rest of Phase 0 as a record of what was done, not as instructions.

### 0.2 Fix the label strata — DONE

```bash
python3 ingest/fixup_labels_stratum_domain.py
```"""

OLD_RB4 = """### 0.4 Do NOT rename labels.jsonl yet

`LABEL-USE-PROTOCOL.md` R8's rename only applies once a charter is written *from* the
labels. `stats.pass4.md` has zero label-derived changes, and the `compbio_methods`
drafts in `PASS-4-DRAFTS.md` have not been applied. So nothing is contaminated yet and
the default path is correct."""

NEW_RB4 = """### 0.4 Do NOT rename labels.jsonl yet — **SUPERSEDED 2026-08-28**

The rename happened, correctly. `charters/compbio_methods.md` line 3 records
adopting R8 when that charter took its two label-derived changes, which makes the
180 rows a development set for `compbio_methods` specifically. `stats` is
unaffected and its charter still carries zero label-derived changes, so it
remains a valid eval target — which is the whole reason E2/E3/E6 point at it.

The original reasoning, true when written:

`LABEL-USE-PROTOCOL.md` R8's rename only applies once a charter is written *from* the
labels. `stats.pass4.md` has zero label-derived changes, and the `compbio_methods`
drafts in `PASS-4-DRAFTS.md` have not been applied. So nothing is contaminated yet and
the default path is correct."""

OLD_E4 = """- [ ] **E4.** Settle `CARD-EVAL-HANDOFF.md` §7.2 and §7.3"""

NEW_E4 = """- [ ] **E4a.** Rule on the two unattributed label records

  2407.01051 and 2410.16457 pass `_is_judged` and carry no `labeller` field —
  they predate it. `score` reports them as `unrecorded=2` and then folds them
  into every headline figure without further comment, against `card_eval.py`'s
  own statement that provenance travels with the number and that a stored 0.82
  which does not say who produced the labels is the same artifact as
  `EVAL-01-FINDINGS.md`'s stale figures.

  Three options, and the choice is a judgment about your own past work rather
  than a code question: stamp them `user` retrospectively if you are confident
  they were yours; exclude them from scored runs; or leave them and have `score`
  refuse to print a headline while any record is unattributed. With five judged
  cards, two of them is 40% of the sample.
  **Gates:** E6

- [ ] **E4.** Settle `CARD-EVAL-HANDOFF.md` §7.2 and §7.3"""

TEXT_EDITS = [
    ("CARD-EVAL-HANDOFF.md", "correct §1's judged/drafted counts", OLD_S1, NEW_S1),
    ("CARD-EVAL-HANDOFF.md", "re-derive §3's card-status table", OLD_S3, NEW_S3),
    ("RUNBOOK-first-measurement.md", "mark Phase 0 complete", OLD_RB, NEW_RB),
    ("RUNBOOK-first-measurement.md", "mark 0.4 superseded by R8", OLD_RB4, NEW_RB4),
    ("TODO.md", "file E4a, the unattributed labellers", OLD_E4, NEW_E4),
]

# ------------------------------------------------------- file installs/removals

INSTALL = [("orientation-SKILL.md", ".claude/skills/orientation/SKILL.md")]
REMOVE = ["patches/patch-03-card-eval-domain.py"]


def _say(*args):
    """print() that survives a closed stdout, so `| head` cannot cancel a run."""
    try:
        print(*args)
    except BrokenPipeError:
        pass


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change and exit without writing")
    ap.add_argument("--no-backup", action="store_true",
                    help="skip the .pre-patch5.bak copies")
    a = ap.parse_args()

    if not (ROOT / "ingest" / "card_eval.py").exists():
        sys.exit(f"not a research-net checkout: {ROOT}\n"
                 f"  run this from the repo root, as "
                 f"`python3 patches/{Path(__file__).name}`")
    try:
        ast.parse((ROOT / "ingest" / "card_eval.py").read_text())
    except SyntaxError as e:
        sys.exit(f"ingest/card_eval.py does not parse (line {e.lineno}).\n"
                 "  Apply patch 3 first. This patch corrects documents that\n"
                 "  describe that file's state, and correcting them against a\n"
                 "  version nobody can run is how the last set got stale.")

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

    installs = []
    for src, dest in INSTALL:
        s, d = HERE / src, ROOT / dest
        if s.exists():
            installs.append((s, d))
        elif d.exists():
            # The staged copy is consumed on install, so its absence plus a
            # present destination is the already-applied state, not a failure.
            # Reporting it as BLOCKED made a second run exit non-zero with
            # "nothing written" while every edit was in fact already applied,
            # which contradicts this directory's own idempotency rule.
            already.append((dest, "install (already installed)"))
        else:
            broken.append((src, "install " + dest,
                           f"staged file missing -- drop {src} into patches/"))

    removals = [ROOT / r for r in REMOVE if (ROOT / r).exists()]

    for rel, label in already:
        _say(f"  skip     {rel:<30} {label} (already applied)")
    for rel, label, why in broken:
        _say(f"  BLOCKED  {rel:<30} {label} -- {why}")
    for rel, label, _, _ in todo:
        _say(f"  apply    {rel:<30} {label}")
    for s, d in installs:
        _say(f"  install  {d.relative_to(ROOT)!s:<30} from patches/{s.name}"
             + ("" if d.exists() else "  (new)"))
    for r in removals:
        _say(f"  DELETE   {r.relative_to(ROOT)!s:<30} superseded by patch 4")

    if broken:
        sys.exit(f"\n{len(broken)} item(s) could not be matched. Nothing written.\n"
                 f"  Anchors are exact text from the post-patch-4 state.\n"
                 f"  Applied edits are detected and skipped, so a partial\n"
                 f"  hand-application followed by a re-run is safe.")
    if not (todo or installs or removals):
        _say("\nnothing to do.")
        return
    if a.dry_run:
        _say(f"\n--dry-run: {len(todo)} edit(s), {len(installs)} install(s), "
             f"{len(removals)} removal(s). Nothing written.")
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
            shutil.copy2(p, p.with_suffix(p.suffix + ".pre-patch5.bak"))
        p.write_text(staged[rel])

    for s, d in installs:
        d.parent.mkdir(parents=True, exist_ok=True)
        if d.exists() and not a.no_backup:
            shutil.copy2(d, d.with_suffix(d.suffix + ".pre-patch5.bak"))
        shutil.copy2(s, d)
        s.unlink()          # staged copy consumed; the installed one is the file

    for r in removals:
        r.unlink()

    for rel in touched:
        _say(f"  wrote    {rel}")
    for _, d in installs:
        _say(f"  wrote    {d.relative_to(ROOT)}")
    for r in removals:
        _say(f"  removed  {r.relative_to(ROOT)}")

    _say(f"\n{len(todo)} edit(s), {len(installs)} install(s), "
         f"{len(removals)} removal(s).")

    readme = ROOT / "patches" / "README.md"
    if readme.exists() and "patch-05" not in readme.read_text():
        _say("\n  NOTE  patches/README.md's ledger has no patch 5 row. It is a")
        _say("        drop-in replacement at its own path -- copy the updated")
        _say("        one over it. The ledger is the order of record.")

    _say("\nVerify:")
    _say("  sed -n '/## 3. Card status/,/^## 4/p' CARD-EVAL-HANDOFF.md")
    _say("  grep -n 'E4a' TODO.md")
    _say("  head -8 RUNBOOK-first-measurement.md")
    _say("  ls .claude/skills/orientation/SKILL.md")
    _say("  ls patches/*.py        # four patches, no *-card-eval-domain on 03")
    _say("  git status --short && git diff --stat")
    _say("\nThen commit. The .pre-patch5.bak files are redundant once you have.")


if __name__ == "__main__":
    main()
