#!/usr/bin/env python3
"""Patch 2 (2026-09-03): level-aware section slicing. Applies on top of patch 1.

    python3 patches/patch-02-level-aware-sections.py --dry-run
    python3 patches/patch-02-level-aware-sections.py

Requires patch 1. It refuses to run otherwise, because level-awareness without
patch 1's END_OF_BODY boundary is actively worse than doing nothing: on
2508.08218 the conclusion absorbs seven `\\subsection{Proof of ...}` blocks and
runs to 31,170 characters. With the boundary in place that same section measures
561 and does not move at all.

WHAT IT CHANGES

`SECTION_RE` matches `\\section` and `\\subsection` with the level discarded, and
`_sections()` ends every body at the next mark of ANY level. So a section's body
is only the prose before its first subsection. Consequences, measured against
the 27 cached e-prints with patch 1 applied (`ingest/audit_extraction.py`):

  - 2411.02771's `\\section{Introduction}` is immediately followed by
    `\\subsection{Motivation}`, so its intro body is two blank lines -- and is
    reported as FOUND, not missing, so nothing warns. The card recorded
    `sections_read: [abstract, conclusion]`; the curator noticed and the
    pipeline did not. Level-aware: 0 -> 17,587 chars, absorbing Motivation,
    Contributions of this work, Related work, Organization.
  - 2410.16457's main results live in §1.2 "Circular law for general models"
    and §1.3 "Weak delocalization estimates" and are discarded. 3,168 -> 20,285.
    This is one of the two cards CARD-EVAL-HANDOFF.md §5.2 cited when it
    concluded that missing objects are out of window by design; on this card
    they were inside the window and thrown away by a slicer bug.
  - 2508.08218 loses "Summary of Main Contributions". 2,535 -> 5,092.

After it, a `\\section` body runs to the next `\\section` and absorbs its
subsections; a `\\subsection` still ends at its sibling. `\\subsubsection` is not
matched by `SECTION_RE` at all and never was, so depth-3 content is already
absorbed into depth 2 -- this makes depths 1-2 consistent with that rather than
introducing a new rule.

SCOPE, MEASURED

Six sections across six cards change. Five absorb contributions lists, main
results or limitations. One does not: 2605.29962's intro goes 11,550 -> 46,176,
absorbing that paper's entire front matter including Methods and Notation.

Nothing else moves. The conclusion side is untouched except 2608.11475 (+905,
absorbing a `Limitations` subsection). No paper gains or loses a conclusion --
the seven with none still have none. No `_pick` outcome changes, because
level-awareness alters body extents and not the marks list.

THE CAP, AND WHY THIS SHIPS WITH IT UNCHANGED

Three sections exceed MAX_SECTION_CHARS (16,000) after this: 2605.29962
(46,176), 2410.16457 (20,285), 2411.02771 (17,587). Ruled 2026-09-03: ship
capped. The reasoning is that the level-aware slice begins where the flat slice
began and continues, so clipping it at 16,000 still delivers strictly more than
today on every card --

    2411.02771   today 0       -> 16,000   (+16,000, loses the Organization tail)
    2410.16457   today 3,168   -> 16,000   (+12,832)
    2605.29962   today 11,550  -> 16,000   (+4,450, loses 30,176)

-- so there is no card on which a curator sees less than it does now. Cost:
+41,351 characters delivered across 27 cards, roughly +425 tokens per card.

The known defect being accepted: truncation cuts at character 16,000, which is a
position and not a boundary, so 2605.29962's intro ends mid-sentence. Making the
cut fall at a subsection edge is a real addition and was deliberately not taken.
What this patch does instead is make the clipping legible -- the notice now
reports the true length, so a curator can see the scale of what it did not get
and set `confidence` accordingly, per the same doctrine as
`## conclusion — NOT FOUND`.

RE-CURATION IS STILL NOT DECIDED

Across patches 1 and 2, these cards were built from a window the extractor no
longer produces:

    2007.11761  2502.11152  2608.16017   -- gained a conclusion (patch 1)
    2506.07459  2605.29508               -- conclusion re-picked (patch 1)
    2411.02771  2410.16457  2508.08218
    2401.16556  2605.29962  2608.11475   -- window widened (patch 2)

Eleven cards, four domains, including two of the three in `stats`. Whether any
are re-curated is E7's decision -- "let that number drive one decision about the
card schema" -- and `PROJECT-STATUS.md` Tier 4 forbids the model spend before
E6 has produced a number. This patch changes the extractor and nothing in `kb/`.
"""

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- code edits

OLD_SECTION_RE = '''SECTION_RE = re.compile(
    r"\\\\(?:sub)?section\\*?\\s*\\{((?:[^{}]|\\{[^{}]*\\})*)\\}", re.S)'''

NEW_SECTION_RE = '''# Group 1 is the level ("sub" or None), group 2 the heading. The level used to
# be matched and discarded, which is what made `_sections` end a section at its
# own first subsection -- see that function.
#
# `\\subsubsection` is deliberately still unmatched: `\\` + optional `sub` +
# `section` cannot consume it. Depth-3 content has therefore always been
# absorbed into its depth-2 parent, and level-awareness below makes depths 1-2
# behave the same way rather than adding a third rule.
SECTION_RE = re.compile(
    r"\\\\(sub)?section\\*?\\s*\\{((?:[^{}]|\\{[^{}]*\\})*)\\}", re.S)'''

OLD_HEADING_TEXTS = '''def _heading_texts(chunk):
    """Cleaned heading strings inside a slice of the document."""
    return [re.sub(r"\\\\[a-zA-Z]+", "", m.group(1)).strip()
            for m in SECTION_RE.finditer(chunk)]'''

NEW_HEADING_TEXTS = '''def _heading_texts(chunk):
    """Cleaned heading strings inside a slice of the document."""
    return [re.sub(r"\\\\[a-zA-Z]+", "", m.group(2)).strip()
            for m in SECTION_RE.finditer(chunk)]'''

OLD_SLICE = '''    marks = [(m.start(), m.end(), m.group(1)) for m in SECTION_RE.finditer(body)]
    out = []
    for i, (s, e, head) in enumerate(marks):
        stop = marks[i + 1][0] if i + 1 < len(marks) else len(body)
        out.append((re.sub(r"\\\\[a-zA-Z]+", "", head).strip(), body[e:stop]))
    return out, {"cut_at": cut_at, "cut_applied": cut_applied,
                 "full_len": full_len}'''

NEW_SLICE = '''    # Level-aware since 2026-09-03. A body runs to the next mark of the SAME OR
    # HIGHER level, so a section absorbs its subsections and a subsection still
    # ends at its sibling. Before this, every body ended at the next mark of any
    # level, which made a section whose prose is entirely in subsections come
    # back EMPTY while being reported as found (2411.02771), and discarded
    # main-results subsections on theory papers (2410.16457 §1.2, §1.3).
    marks = [(m.start(), m.end(), 2 if m.group(1) else 1, m.group(2))
             for m in SECTION_RE.finditer(body)]
    out = []
    for i, (s, e, lvl, head) in enumerate(marks):
        stop = len(body)
        for j in range(i + 1, len(marks)):
            if marks[j][2] <= lvl:
                stop = marks[j][0]
                break
        out.append((re.sub(r"\\\\[a-zA-Z]+", "", head).strip(), body[e:stop]))
    return out, {"cut_at": cut_at, "cut_applied": cut_applied,
                 "full_len": full_len}'''

OLD_TRUNC = '''        if len(text) > MAX_SECTION_CHARS:
            text = text[:MAX_SECTION_CHARS] + \\
                f"\\n\\n[truncated at {MAX_SECTION_CHARS} chars]"'''

NEW_TRUNC = '''        if len(text) > MAX_SECTION_CHARS:
            # Report the TRUE length, not just the limit. Level-aware slicing
            # clips three sections in the current KB, and a notice that says
            # only "truncated at 16000" tells the curator nothing about whether
            # it lost a paragraph or thirty thousand characters. Same doctrine
            # as `## conclusion — NOT FOUND (<why>)`: a shortfall the curator
            # can size is one it can put in `confidence` and `card_notes`.
            text = text[:MAX_SECTION_CHARS] + (
                f"\\n\\n[truncated at {MAX_SECTION_CHARS} of {len(text)} chars; "
                f"{len(text) - MAX_SECTION_CHARS} not shown]")'''

# ---------------------------------------------------------------- doc edits

OLD_D0_TAIL = """  **Still open, and deliberately not in that patch:** level-aware `SECTION_RE`.
  It fixes the empty intro and recovers main-results subsections currently
  discarded on theory papers, but it changes the window for every paper using
  subsections, so it is a re-curation trigger rather than a bug fix. Re-measure
  with D0's boundary in place first — the unbounded figures overstate it.
  **Gates:** E3, and any decision about re-curating the six affected cards (E7)."""

NEW_D0_TAIL = """  **Second half closed by patch 2, 2026-09-03**
  (`patches/patch-02-level-aware-sections.py`): level-aware `SECTION_RE`. It was
  held back for one measurement, and the measurement mattered — unbounded, it
  made 2508.08218's conclusion absorb seven proof subsections and run to 31,170
  chars. With patch 1's boundary in place that section does not move at all, and
  only six sections across six cards change, five of them absorbing
  contributions lists, main results or limitations.

  Shipped with `MAX_SECTION_CHARS` unchanged at 16,000. Three sections clip, but
  a level-aware slice starts where the flat one did and continues, so every card
  still receives strictly more than before — 2411.02771's intro goes 0 → 16,000.
  Cost ~+425 tokens per card. Accepted defect: the cut falls at a character
  position rather than a subsection edge, so 2605.29962's intro ends
  mid-sentence; the notice now reports the true length so the curator can size
  what it did not get.

  **Still open — and it is a decision, not a fix.** Eleven cards across four
  domains were built from a window the extractor no longer produces: gained a
  conclusion — 2007.11761, 2502.11152, 2608.16017; re-picked — 2506.07459,
  2605.29508; widened — 2411.02771, 2410.16457, 2508.08218, 2401.16556,
  2605.29962, 2608.11475. Two of the three `stats` cards are in that set.
  Whether any are re-curated belongs to E7, and Tier 4 forbids the spend before
  E6 has produced a number.
  **Gates:** E3, and the re-curation decision (E7)."""

OLD_52_FRAGMENT = """   Two consequences for the rest of this file. **§5.2's policy question was
   argued against the wrong data**: on 2410.16457, \"Circular law for general
   models\" and \"Weak delocalization estimates\" are §1.2 and §1.3 — inside the
   curator's requested window, discarded by a boundary bug rather than excluded
   by design. And **§5.4's reading of `sections_read` is too kind**: on
   2605.29508 it claims `conclusion` while the delivered text was an appendix
   subsection, so the field can mis-report, not merely under-report."""

NEW_52_FRAGMENT = """   Two consequences for the rest of this file. **§5.2's policy question was
   argued against the wrong data**: on 2410.16457, \"Circular law for general
   models\" and \"Weak delocalization estimates\" are §1.2 and §1.3 — inside the
   curator's requested window, discarded by a slicer bug rather than excluded by
   design. Patch 2 (2026-09-03) delivers them: that intro goes from 3,168 to
   20,285 characters, capped at 16,000. So the window policy is a narrower
   question than this section framed it — the abstract/intro/conclusion choice
   is still a decision for you, but a measurable part of what looked like its
   cost was a defect, and it is fixed. Re-read §5.2's re-audit table with that
   in mind before treating any of its `objects_missed` numbers as settled.

   And **§5.4's reading of `sections_read` is too kind**: on 2605.29508 it claims
   `conclusion` while the delivered text was an appendix subsection, so the field
   can mis-report, not merely under-report."""

# ------------------------------------------------------------------- driver


def _say(*args):
    """print() that survives a closed stdout, so `| head` cannot cancel a run."""
    try:
        print(*args)
    except BrokenPipeError:
        pass


EDITS = [
    ("ingest/pdf_extract.py", "capture the section level in SECTION_RE",
     OLD_SECTION_RE, NEW_SECTION_RE),
    ("ingest/pdf_extract.py", "follow the group shift in _heading_texts",
     OLD_HEADING_TEXTS, NEW_HEADING_TEXTS),
    ("ingest/pdf_extract.py", "slice to the next same-or-higher level mark",
     OLD_SLICE, NEW_SLICE),
    ("ingest/pdf_extract.py", "report the true length when truncating",
     OLD_TRUNC, NEW_TRUNC),
    ("TODO.md", "close D0's second half", OLD_D0_TAIL, NEW_D0_TAIL),
    ("CARD-EVAL-HANDOFF.md", "narrow §5.2's policy question", OLD_52_FRAGMENT,
     NEW_52_FRAGMENT),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change and exit without writing")
    ap.add_argument("--no-backup", action="store_true",
                    help="skip the .pre-patch2.bak copies")
    a = ap.parse_args()

    px = ROOT / "ingest" / "pdf_extract.py"
    if not px.exists():
        sys.exit(f"not a research-net checkout: {ROOT}\n"
                 f"  run this from the repo root, as "
                 f"`python3 patches/{Path(__file__).name}`")

    # Hard prerequisite, not a warning. Level-awareness without the boundary
    # lets a conclusion swallow the appendix -- 2508.08218 goes to 31,170 chars.
    if "END_OF_BODY" not in px.read_text():
        sys.exit("patch 1 is not applied: ingest/pdf_extract.py has no "
                 "END_OF_BODY.\n"
                 "  Run patches/patch-01-extractor-boundaries.py first. This\n"
                 "  patch is worse than nothing without it -- see the docstring.")

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
                 f"  Anchors are exact text from the post-patch-1 state.\n"
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
            shutil.copy2(p, p.with_suffix(p.suffix + ".pre-patch2.bak"))
        p.write_text(staged[rel])

    for rel in touched:
        _say(f"  wrote    {rel}")
    _say(f"\n{len(todo)} edit(s) applied to {len(touched)} file(s).")
    _say("\nVerify, in this order:")
    _say("  python3 -c \"import ast,pathlib;"
         "ast.parse(pathlib.Path('ingest/pdf_extract.py').read_text())\"")
    _say("  python3 ingest/audit_extraction.py")
    _say("     -> expect: 0 unmatched, 0 EMPTY (2411.02771's intro is fixed),")
    _say("        3 truncated at 16000, 7 with no closing section")
    _say("  python3 ingest/pdf_extract.py 2411.02771 --sections intro | head -20")
    _say("     -> expect its Motivation / Contributions text, not a bare heading")
    _say("  git diff --stat")
    _say("\nThen commit. The .pre-patch2.bak files are redundant once you have.")


if __name__ == "__main__":
    main()
