#!/usr/bin/env python3
"""What `pmd` will put on the dashboard tomorrow, and whether it will parse.

    python3 ingest/pmd_check.py
    python3 ingest/pmd_check.py --json

A DIAGNOSTIC, NOT A PATCH. Run, not applied. Per `patches/README.md` it belongs
in `ingest/`:

    git mv patches/pmd_check.py ingest/pmd_check.py

WHY IT EXISTS

`TODO.md` is read once a day by `pmd`, an external dashboard, and the contract
is a *parse*: a `## Next step` heading, the first unchecked `- [ ]` box beneath
it, indented boxes as subtasks, indented prose as context. Nothing in the repo
checked that parse, so the contract was maintained by eye -- and the repo's own
rule is that a card which does not validate does not exist. A next step that
does not parse does not exist either, and its failure is silent: the dashboard
shows a blank, and a blank is indistinguishable from a project with nothing to
do. `PROJECT-STATUS.md` §5 Tier 0 calls that class the integrity floor.

It caught a real defect on its first run. Patch 7 rewrote two of E1's subtasks
as wrapped two-line entries; the continuation lines parse as *context*
interleaved among the subtasks, and their `~20m` markers land on a line that is
not a box, so pmd would not see them. Patch 9 fixed both and this script is why
they were found.

THE FAILURE MODE WORTH KNOWING

`## Next step` with **zero** unchecked boxes under it is worse than no heading
at all. With no heading, pmd falls back to the first unchecked box anywhere in
the file and still reports something. With the heading present and empty, there
is nothing to fall back to -- so closing the next step without promoting a
backlog item in the same edit blanks the dashboard. That is the single most
likely way this interface breaks, because it is what "finishing a task" looks
like.

EXIT CODES, matching validate_card.py after patch 8

    0   pmd will surface a well-formed next step
    1   the CONTRACT is broken -- pmd will surface nothing, or the wrong thing
    3   this script could not tell (no candidate file, unreadable)

3 rather than 2 because `verify_citations.py` uses 2 for "unreachable" and two
scripts disagreeing about a code is the problem, not the fix.

WHAT IT DELIBERATELY DOES NOT DO

  - It does not judge whether the next step is the *right* next step. That is a
    human ruling and `TODO.md`'s ordering rules are where it is argued.
  - It does not write. Blanking a dashboard by accident is the risk it exists
    to catch; repairing `TODO.md` automatically would be the same risk with the
    author removed.
  - It does not run `.pmd/collect` if one appears. It reports that rung 1 has
    taken over and stops, because executing a repo script to find out what a
    dashboard says is a wider permission than a diagnostic needs.
"""

import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = ["TODO.md", "NOTES.md", "TASKS.md", "NEXT.md", "README.md"]

# "any heading level, case-insensitive, optional trailing colon, optional plural"
HEADING = re.compile(r"^#{1,6}[ \t]*next[ \t]+steps?:?[ \t]*$", re.I)
BOX = re.compile(r"^([ \t]*)- \[([ xX])\][ \t]*(.*)$")
ESTIMATE = re.compile(r"~\d+(?:\.\d+)?[mhdw]\b")
STEP_LINE_MAX = 90


def resolve():
    """pmd's four rungs, in its order. Returns (rung, detail)."""
    if (ROOT / ".pmd" / "collect").exists():
        return 1, ".pmd/collect"
    if (ROOT / ".pmd.conf").exists():
        conf = {}
        for line in (ROOT / ".pmd.conf").read_text().splitlines():
            if ":" in line and not line.strip().startswith("#"):
                k, v = line.split(":", 1)
                conf[k.strip()] = v.strip()
        return 2, conf
    for name in CANDIDATES:
        p = ROOT / name
        if p.is_file() and any(HEADING.match(l) for l in p.read_text().splitlines()):
            return 3, name
    for name in CANDIDATES:
        p = ROOT / name
        if p.is_file() and any(BOX.match(l) and BOX.match(l).group(2) == " "
                               for l in p.read_text().splitlines()):
            return 3, f"{name} (fallback: first unchecked box, no heading)"
    return 4, None


def parse(path):
    lines = (ROOT / path).read_text().splitlines()
    h = next((i for i, l in enumerate(lines) if HEADING.match(l)), None)
    if h is None:
        return None, lines, None
    level = len(lines[h]) - len(lines[h].lstrip("#"))
    end = len(lines)
    for j in range(h + 1, len(lines)):
        m = re.match(r"^(#{1,6})[ \t]", lines[j])
        if m and len(m.group(1)) <= level:
            end = j
            break
    return (h, end), lines, level


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="machine-readable")
    a = ap.parse_args()

    rung, detail = resolve()
    problems, notes = [], []

    if rung == 1:
        print("rung 1: .pmd/collect exists and overrides everything below.")
        print("  This script does not execute it. Nothing here applies.")
        sys.exit(0)
    if rung == 2:
        print(f"rung 2: .pmd.conf -> {detail}")
        notes.append("a .pmd.conf is present; TODO.md may not be what pmd reads")
    if rung == 4:
        print("rung 4: NOTHING FOUND. pmd will report no next step.", file=sys.stderr)
        sys.exit(3)

    fname = (detail if isinstance(detail, str) else
             detail.get("next_step_file", "TODO.md")).split(" (")[0]
    if not (ROOT / fname).is_file():
        print(f"cannot read {fname}", file=sys.stderr)
        sys.exit(3)

    span, lines, _ = parse(fname)
    if span is None:
        problems.append(f"no '## Next step' heading in {fname}; pmd is on its "
                        f"fallback path and will surface the first unchecked box "
                        f"anywhere in the file")
        h, end = -1, len(lines)
    else:
        h, end = span

    # --- the step line ------------------------------------------------
    tops = [(j, m) for j in range(h + 1, end)
            if (m := BOX.match(lines[j])) and not m.group(1)]
    unchecked = [(j, m) for j, m in tops if m.group(2) == " "]

    if not tops:
        problems.append("no top-level box under the heading at all")
    elif not unchecked:
        problems.append(f"{len(tops)} top-level box(es) under the heading and ALL "
                        f"ARE CHECKED. pmd will surface nothing and cannot fall "
                        f"back, because the heading exists. Promote a backlog item.")
    elif len(unchecked) > 1:
        problems.append(f"{len(unchecked)} unchecked top-level boxes; pmd takes the "
                        f"first and the rest are invisible: "
                        + ", ".join(repr(m.group(3)[:40]) for _, m in unchecked))

    step = unchecked[0] if unchecked else None
    subs, ctx = [], []
    if step:
        j, m = step
        text = m.group(3)
        print(f"file: {fname}   heading: line {h + 1}")
        print(f"\nDASHBOARD LINE (line {j + 1}):\n  {text}\n")
        if len(text) > STEP_LINE_MAX:
            problems.append(f"step line is {len(text)} chars, over {STEP_LINE_MAX}; "
                            f"the dashboard shows this line only")
        if not ESTIMATE.search(text):
            notes.append("no ~estimate marker on the step line")
        if ":" in text.split("`")[0]:
            notes.append("step line contains a colon before any code span -- pmd's "
                         "guidance says no colons introducing a procedure")

        # subtasks and wrapped-line detection
        seen_sub = False
        for k in range(j + 1, end):
            mm = BOX.match(lines[k])
            if mm and not mm.group(1):
                break
            if mm:
                subs.append({"text": mm.group(3), "done": mm.group(2) != " "})
                seen_sub = True
            elif lines[k].strip():
                if seen_sub and not ctx and lines[k].startswith("        "):
                    problems.append(
                        f"line {k + 1} is a WRAPPED SUBTASK, not context: "
                        f"{lines[k].strip()[:50]!r}. A continuation line is not a "
                        f"box, so pmd reads it as context and any ~estimate on it "
                        f"is lost. Keep each subtask on one line.")
                ctx.append(lines[k].strip())

        print(f"SUBTASKS ({sum(1 for s in subs if s['done'])}/{len(subs)} done):")
        for s in subs:
            print(f"  [{'x' if s['done'] else ' '}] {s['text'][:74]}")
        print(f"\nCONTEXT: {len(ctx)} line(s), first: {ctx[0][:70] if ctx else '(none)'}")

    # --- open items ---------------------------------------------------
    open_items = sum(1 for l in lines if (m := BOX.match(l)) and m.group(2) == " ")
    has_backlog = any(re.match(r"^#{1,6}[ \t]*backlog", l, re.I) for l in lines)
    print(f"\nopen_items (unchecked boxes in file): {open_items}"
          f"   ## Backlog heading: {'yes' if has_backlog else 'no'}")

    if a.json:
        print(json.dumps({"rung": rung, "file": fname,
                          "next_step": {"text": step[1].group(3) if step else None,
                                        "subtasks": subs, "context": ctx},
                          "open_items": open_items, "problems": problems}, indent=2))

    for n in notes:
        print(f"\n  note     {n}")
    for p in problems:
        print(f"\n  BROKEN   {p}", file=sys.stderr)

    if problems:
        print("\nThe contract is broken. `TODO.md`'s header states it; fix there.",
              file=sys.stderr)
        sys.exit(1)
    print("\ncontract holds — pmd will surface the line above.")
    sys.exit(0)


if __name__ == "__main__":
    main()
