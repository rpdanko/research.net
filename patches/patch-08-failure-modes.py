#!/usr/bin/env python3
"""Patch 8 (2026-09-04): three failures reported as a different failure.

    python3 patches/patch-08-failure-modes.py --dry-run
    python3 patches/patch-08-failure-modes.py

Needs patches 1-7. Code only; patch 7 holds the document half of the same
session, kept separate so a behavioural change to a gate can be reverted
without losing the record of why it was made.

THE THEME, AND WHY IT IS INVARIANT 17 ONE LAYER ALONG

Invariant 17 already rules on this class: *"**Unreachable is not fabricated**
(exit 2 vs exit 1); collapsing those two would make every network outage look
like mass invention."* That is a ruling about a citation checker, and the
reasoning is not specific to citations. It is that a check whose failure mode
is indistinguishable from the thing it checks for is not a check.

Running the eval path on 2026-09-04 turned up three instances, none of them in
`verify_citations.py`.

  1. **`validate_card.py` exits 1 for a missing dependency.** `import yaml,
     jsonschema` fails -> `sys.exit("pip install pyyaml jsonschema")`, which is
     exit 1, which is the same code the script uses for "this card is invalid".
     `card_schema.json` line 4 and the script's own docstring both carry *"A
     card that does not validate does not exist."* Under that convention an
     unprovisioned environment invalidates the entire KB, silently, and the
     caller cannot tell.

     This was found the dull way: all 28 cards "failed" in a sandbox where
     pyyaml was not installed. It reads as catastrophic schema drift and is a
     missing package.

  2. **`validate_card.py` exits 0 for a path that does not exist.** `main()`
     does `if not f.is_file(): continue`, `failed` stays 0, and the script
     prints `all cards valid`. So `validate_card.py kb/*/cards/*.md` in a tree
     with no cards -- an unexpanded glob, a wrong cwd, a domain directory that
     was never created -- reports success. False negatives on a gate are the
     failure `README.md` line 85 calls worse than no gate: *"it discards work
     silently and you never learn what you lost."* Here it admits work silently
     instead, which is the same sentence run backwards.

  3. **`rebuild_index.py` inherits both.** Line 107 imports `check` from
     `validate_card` deliberately -- *"same parser, not a second copy"* -- so
     the dependency exit fires at import time, before argument parsing, on
     every invocation including a plain one that was not going to validate
     anything.

     And `card_eval.py`'s `_ask()` calls bare `input()`. Ctrl-D raises
     `EOFError` and prints a traceback out of the middle of a labelling
     session. `_save()` runs per field so nothing is actually lost, but the
     screen says otherwise at the exact moment a user is deciding whether to
     trust this tool with two hours of judgment. `q` already means "save and
     quit"; EOF should mean it too.

WHAT IT CHANGES

  ingest/validate_card.py    exit 3 for environment/invocation failure, exit 1
                             reserved for a card that failed the schema; a
                             nonexistent path is now reported and counted as
                             invocation failure rather than skipped; docstring
                             gains the exit-code table.
  ingest/rebuild_index.py    the shared import is guarded so the dependency
                             failure surfaces as exit 3 with the same wording,
                             rather than as a traceback or as exit 1.
  ingest/card_eval.py        `_ask()` treats EOF as `q` when `q` is offered,
                             and as a clean abort otherwise.
  ingest/audit_extraction.py its closing note claims the one remaining empty
                             section is "deliberately still open". Patch 2
                             closed it on 2026-09-03. The script now prints 0
                             empty and a footer saying it is open, which is a
                             document quoting a stale metric -- forbidden by
                             `PROJECT-STATUS.md` §6 item 5 -- inside the
                             diagnostic that three documents quote *from*.

WHY 3 AND NOT 2

`verify_citations.py` already uses 2 for "unreachable". Reusing 2 here for a
different meaning in a different script would make the two scripts disagree
about what 2 means, and the whole point of this patch is that a code has to
mean one thing. 3 is free everywhere in `ingest/`, checked.

WHAT IT DELIBERATELY LEAVES UNDONE

  - **Not D6.** The `name` validator belongs in this file and this patch does
    not add it, because patch 7 re-derived it at ten matching names across ten
    cards with false positives among them. That is a retroactivity decision,
    not a five-line fix, and it is filed as such.
  - **Not E4a.** `score` still prints a headline with `unrecorded=2` folded in.
    Making it refuse is option three of a ruling the user has not made.
  - **No other exit codes.** `card_eval.py`, `eval_triage.py` and the audits
    keep theirs. This patch touches the four call sites the run actually
    exercised; a sweep of every script's exit convention is worth doing and is
    not worth doing blind, since each one's 1 currently means something
    specific.
  - **No `sys.exit` in `_ask`'s abort path when `q` is unavailable.** It raises
    `KeyboardInterrupt`, so an outer handler that already saves keeps working.
"""

import argparse, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUFFIX = ".pre-patch8.bak"

# ---------------------------------------------------------------- 1. deps

VC_DOC_OLD = '''    python3 ingest/validate_card.py kb/stats/cards/2608.01234.md
    python3 ingest/validate_card.py kb/*/cards/*.md --new-only

Exit 0 if all pass, 1 otherwise.
"""
'''

VC_DOC_NEW = '''    python3 ingest/validate_card.py kb/stats/cards/2608.01234.md
    python3 ingest/validate_card.py kb/*/cards/*.md --new-only

EXIT CODES, and they are three rather than two on purpose

    0   every card checked passed the schema
    1   a card failed the schema -- the card is wrong
    3   this script could not run the check -- the ENVIRONMENT is wrong:
        a missing dependency, or a path that is not a file

Invariant 17 rules on exactly this distinction for citations: "Unreachable is
not fabricated (exit 2 vs exit 1); collapsing those two would make every
network outage look like mass invention." The same collapse here is worse,
because `card_schema.json` and this docstring both say "A card that does not
validate does not exist" -- so a missing pyyaml, reported as exit 1, does not
invalidate one card, it invalidates the knowledge base.

3 rather than 2 because `verify_citations.py` already uses 2 for "unreachable".
Two scripts disagreeing about what a code means is the problem, not the fix.
"""
'''

VC_GUARD_OLD = """try:
    import yaml, jsonschema
except ImportError:
    sys.exit("pip install pyyaml jsonschema")
"""

VC_GUARD_NEW = """# Exit 3, not the implicit 1 of sys.exit(str): see the exit-code block above.
# This is an environment failure and must not be legible as an invalid card.
ENV_FAILURE = 3

try:
    import yaml, jsonschema
except ImportError:
    print("pip install pyyaml jsonschema", file=sys.stderr)
    print("  (exit 3 = this script could not run, NOT 'the cards are invalid')",
          file=sys.stderr)
    sys.exit(ENV_FAILURE)
"""

# ------------------------------------------------------- 2. missing paths

VC_MAIN_OLD = """    import time
    cutoff = time.time() - 86400
    failed = 0

    for path in a.paths:
        f = Path(path)
        if not f.is_file():
            continue
        if a.new_only and f.stat().st_mtime < cutoff:
            continue
        problems = check(f)
        if problems:
            failed += 1
            print(f"FAIL {f}")
            for pr in problems:
                print(f"     {pr}")

    print(f"\\n{failed} card(s) failed" if failed else "all cards valid")
    sys.exit(1 if failed else 0)
"""

VC_MAIN_NEW = """    import time
    cutoff = time.time() - 86400
    failed = 0
    checked = 0
    unreadable = []

    for path in a.paths:
        f = Path(path)
        if not f.is_file():
            # NOT `continue`. A path that is not a file used to be skipped, so
            # an unexpanded glob or a wrong cwd printed "all cards valid" and
            # exited 0 -- a gate reporting success for having checked nothing.
            unreadable.append(path)
            continue
        if a.new_only and f.stat().st_mtime < cutoff:
            continue
        checked += 1
        problems = check(f)
        if problems:
            failed += 1
            print(f"FAIL {f}")
            for pr in problems:
                print(f"     {pr}")

    if unreadable:
        print(f"\\nCANNOT READ {len(unreadable)} path(s) -- not files:",
              file=sys.stderr)
        for path in unreadable:
            print(f"     {path}", file=sys.stderr)
        print("  An unexpanded glob looks exactly like this. Nothing was\\n"
              "  checked for these, and 'nothing checked' is not 'all valid'.",
              file=sys.stderr)

    if failed:
        print(f"\\n{failed} card(s) failed")
    elif checked:
        print(f"all {checked} card(s) valid")
    else:
        print("\\nNO CARDS CHECKED.", file=sys.stderr)

    if unreadable or not checked:
        sys.exit(ENV_FAILURE)
    sys.exit(1 if failed else 0)
"""

# -------------------------------------------------------- 3. rebuild_index

RI_OLD = """sys.path.insert(0, str(Path(__file__).parent))
from validate_card import check as full_check, FM  # noqa: E402  same parser, not a second copy
"""

RI_NEW = """sys.path.insert(0, str(Path(__file__).parent))
# Deliberately the same parser, not a second copy -- but the import carries
# validate_card.py's dependency failure with it, and used to fire as a bare
# exit before argparse ran, on every invocation including ones that validate
# nothing. Re-raised as its exit 3 so a caller can still tell "the environment
# is wrong" from "a card is wrong". See patch 8 and invariant 17.
try:
    from validate_card import check as full_check, FM  # noqa: E402
except SystemExit:
    print("rebuild_index.py needs validate_card.py's dependencies: "
          "pip install pyyaml jsonschema", file=sys.stderr)
    print("  (exit 3 = could not run, NOT 'the index is wrong')", file=sys.stderr)
    sys.exit(3)
"""

# --------------------------------------------------------------- 4. EOF

ASK_OLD = """def _ask(prompt, valid, default=None):
    while True:
        v = input(prompt).strip().lower()
        if not v and default is not None:
            return default
        if v in valid:
            return v
"""

ASK_NEW = """def _ask(prompt, valid, default=None):
    while True:
        try:
            v = input(prompt).strip().lower()
        except EOFError:
            # Ctrl-D used to raise out of the middle of a labelling session as
            # a traceback. `_save()` runs per field so nothing was ever lost,
            # but the screen said otherwise at the moment the user is deciding
            # whether to trust this tool with two hours of judgment. `q`
            # already means save-and-quit; EOF means the same thing.
            if "q" in valid:
                print("\\n  (EOF -- treating as `q`: saving and quitting)")
                return "q"
            print("\\n  (EOF with no quit option here -- aborting)")
            raise KeyboardInterrupt
        if not v and default is not None:
            return default
        if v in valid:
            return v
"""

# ------------------------------------------------- 5. stale audit footer

AUDIT_OLD = '''    print("\\nBefore patch 1 (2026-09-03) this read: 8 truncated, 1 empty,\\n"
          "3 unmatched closing sections, plus 2 cards silently handed an\\n"
          "appendix heading as their conclusion (2506.07459, 2605.29508) --\\n"
          "six defective windows in total. After it: 0, 1, 0, 0. The one\\n"
          "remaining EMPTY is 2411.02771's intro, which needs level-aware\\n"
          "SECTION_RE and is deliberately still open -- see TODO.md D0.")
'''

AUDIT_NEW = '''    print("\\nBefore patch 1 (2026-09-03) this read: 8 truncated, 1 empty,\\n"
          "3 unmatched closing sections, plus 2 cards silently handed an\\n"
          "appendix heading as their conclusion (2506.07459, 2605.29508) --\\n"
          "six defective windows in total. After patch 1: 0, 1, 0, 0. Patch 2\\n"
          "closed the last empty section the same day -- 2411.02771's intro,\\n"
          "0 -> 16,053 chars via level-aware SECTION_RE -- so the empty column\\n"
          "now reads 0 and the truncated column reads 3 because that intro\\n"
          "clips at MAX_SECTION_CHARS. Nothing in TODO.md D0's FIRST half is\\n"
          "still open.\\n"
          "\\nWhat IS still open is D0's second half, and it is a decision\\n"
          "rather than a fix: eleven cards were built from a window this\\n"
          "extractor no longer produces, so a card/source discrepancy on one\\n"
          "of them may be an artifact of the repair. This script cannot see\\n"
          "that -- it reports today's window only. `window_diff.py\\n"
          "--all-affected` reconstructs the window each card was actually\\n"
          "written under and is the tool for that question.")
'''

EDITS = [
    ("ingest/validate_card.py", VC_DOC_OLD, VC_DOC_NEW, "exit-code table in the docstring"),
    ("ingest/validate_card.py", VC_GUARD_OLD, VC_GUARD_NEW, "missing dependency -> exit 3"),
    ("ingest/validate_card.py", VC_MAIN_OLD, VC_MAIN_NEW, "unreadable path is reported, not skipped"),
    ("ingest/rebuild_index.py", RI_OLD, RI_NEW, "guard the shared import"),
    ("ingest/card_eval.py", ASK_OLD, ASK_NEW, "_ask(): EOF means `q`"),
    ("ingest/audit_extraction.py", AUDIT_OLD, AUDIT_NEW, "footer: patch 2 closed the empty section"),
]


def compiles(path, text):
    """A syntax check before writing, because these four files are the ones a
    curator cannot repair: ingest/ is agent-denied, so a patch that leaves a
    file unparseable is only fixable by hand. Patch 3 exists because
    card_eval.py sat unparseable for two days and nothing had run it."""
    try:
        compile(text, str(path), "exec")
        return None
    except SyntaxError as e:
        return f"{e.msg} at line {e.lineno}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report only, touch nothing")
    a = ap.parse_args()

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
                 "ingest/ surfaces as card drift weeks later instead of a "
                 "traceback now.")

    if not plan:
        print("\nnothing to do — patch 8 is fully applied.")
        return

    touched = {}
    for fname, old, new, _ in plan:
        touched[fname] = touched.get(fname, texts[fname]).replace(old, new, 1)

    syntax = [(f, e) for f, out in touched.items()
              if (e := compiles(ROOT / f, out))]
    if syntax:
        for f, e in syntax:
            print(f"  PROBLEM {f}: result would not parse — {e}")
        sys.exit("\nrefusing to write: the patched text does not compile.")

    if a.dry_run:
        print(f"\ndry run: {len(plan)} edit(s) across {len(touched)} file(s), "
              f"all compile, nothing written.")
        return

    for fname, out in touched.items():
        p = ROOT / fname
        bak = p.with_name(p.name + SUFFIX)
        if not bak.exists():
            shutil.copy2(p, bak)
        p.write_text(out)
        print(f"  wrote   {fname}   (backup: {bak.name})")

    print(f"\n{len(plan)} edit(s) applied across {len(touched)} file(s).")
    print("\nVerify, in this order:")
    print("  python3 ingest/validate_card.py kb/*/cards/*.md   # expect: all 28 valid, exit 0")
    print("  python3 ingest/validate_card.py kb/nope/*.md      # expect: CANNOT READ, exit 3")
    print("  python3 ingest/audit_extraction.py                # expect: 3 truncated, 0 empty")
    print("\nThe second one is the whole patch. If it prints 'all cards valid'")
    print("and exits 0, the edit did not take.")


if __name__ == "__main__":
    main()
