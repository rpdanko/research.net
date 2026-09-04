#!/usr/bin/env python3
"""Patch 3 (2026-09-03): repair `_is_judged`'s docstring. One edit, nothing else.

    python3 patches/patch-03-card-eval-syntax.py --dry-run
    python3 patches/patch-03-card-eval-syntax.py

`ingest/card_eval.py` does not parse. Every invocation dies before `main()`
runs -- `sample`, `label`, `import`, `score`, `diff`, all of it:

    SyntaxError: leading zeros in decimal integer literals are not permitted
    line 348:  Second fix, 2026-09-01: objects are only required when

`_is_judged`'s docstring closes twice with prose in between, so the second
paragraph is bare code and Python reads `2026-09-01` as a malformed integer:

    def _is_judged(r):
        \"\"\"A card is judged when it is COMPLETE, not merely started.
        ...
        exactly that happened on 2410.16457.
        \"\"\"                                        <- closes
        Second fix, 2026-09-01: objects are only ...  <- now code
        ...
        \"\"\"                                        <- closes again

The fix removes the first closing delimiter, so both paragraphs live in one
docstring. No prose is lost and no behaviour changes.

PROVENANCE, because it dates the blast radius

    git show <commit>:ingest/card_eval.py | python3 -c "import ast,sys; ast.parse(sys.stdin.read())"

    c9ba5e8  2026-08-31        parses
    95923f5  2026-09-01 14:45  parses
    29b4cff  2026-09-01 16:42  SyntaxError line 348   <- introduced here
    2c65a02  2026-09-01 17:08  SyntaxError line 348

So the file has been unloadable since 2026-09-01 16:42, and `2c65a02` -- 26
minutes later -- rewrote `TODO.md` into the E/D gate graph that rests on it.
Nothing noticed because nothing has ever run it: `PROJECT-STATUS.md` §5 item 6
says "written 2026-08-28, not yet run", and `CARD-EVAL-HANDOFF.md` §1 says
"`score` has never been run and `eval/card_runs/` is empty".

It is the same shape as `TODO.md` D5 -- a second paragraph appended without
fixing the delimiter, there in markdown and here in Python -- and both were
applied the same day. Worth a look at anything else touched by `29b4cff`.

DELIBERATELY ONE EDIT

This does not fix anything else, and it is not a smoke test. A file that has
never been parsed has no reason to contain exactly one error, so expect the next
`ast.parse` to find another. That is **E5**'s entire job -- "finding crashes in
code that has never executed, not producing numbers" -- and each defect gets its
own patch so the history stays attributable. Run the verify block below and work
whatever it reports as the next finding.
"""

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD = '''    restart and open the next untouched one instead. Fixed 2026-08-30 after
    exactly that happened on 2410.16457.
    """
    Second fix, 2026-09-01: objects are only required when'''

NEW = '''    restart and open the next untouched one instead. Fixed 2026-08-30 after
    exactly that happened on 2410.16457.

    Second fix, 2026-09-01: objects are only required when'''

EDITS = [
    ("ingest/card_eval.py", "close _is_judged's docstring once, not twice",
     OLD, NEW),
]


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
                    help="skip the .pre-patch3.bak copy")
    a = ap.parse_args()

    target = ROOT / "ingest" / "card_eval.py"
    if not target.exists():
        sys.exit(f"not a research-net checkout: {ROOT}\n"
                 f"  run this from the repo root, as "
                 f"`python3 patches/{Path(__file__).name}`")

    cache = {}
    todo, already, broken = [], [], []
    for rel, label, old, new in EDITS:
        p = ROOT / rel
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
        sys.exit("\n1 edit could not be matched. Nothing written.\n"
                 "  If the docstring has already been repaired by hand, this\n"
                 "  reports `skip` rather than blocking -- so a BLOCKED here\n"
                 "  means the surrounding text changed. Fix it by hand:\n"
                 "  delete the first of the two `\"\"\"` in _is_judged.")
    if not todo:
        _say("\nnothing to do; already applied.")
    elif a.dry_run:
        _say("\n--dry-run: 1 edit would be applied. Nothing written.")
        return
    else:
        staged = {rel: cache[rel].replace(old, new, 1)
                  for rel, _, old, new in todo}
        for rel, text in staged.items():
            p = ROOT / rel
            if not a.no_backup:
                shutil.copy2(p, p.with_suffix(p.suffix + ".pre-patch3.bak"))
            p.write_text(text)
        for rel in staged:
            _say(f"  wrote    {rel}")
        _say("\n1 edit applied to 1 file.")

    # Parse it here, because the whole point of the patch is whether it loads,
    # and because the answer is very likely "not yet".
    import ast
    _say("")
    try:
        ast.parse(target.read_text())
        _say("  ast.parse: OK -- ingest/card_eval.py now loads.")
        _say("\nVerify, then treat E5 as the next item:")
        _say("  python3 ingest/card_eval.py score --help")
        _say("  python3 ingest/card_eval.py score      # 20 records, all judged?")
        _say("  git diff --stat  &&  git commit")
    except SyntaxError as e:
        _say(f"  ast.parse: STILL FAILING at line {e.lineno}: {e.msg}")
        if e.text:
            _say(f"    -> {e.text.strip()[:70]}")
        _say("\n  Expected. This patch fixed one defect deliberately. The next")
        _say("  one is a separate finding and wants its own patch -- commit this")
        _say("  first so the history says which fix addressed what.")


if __name__ == "__main__":
    main()
