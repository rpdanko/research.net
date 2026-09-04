#!/usr/bin/env python3
"""Patch 1 (2026-09-03): end-of-body boundary, guarded; widened conclusion
matching; cap raise.

    python3 patches/patch-01-extractor-boundaries.py --dry-run
    python3 patches/patch-01-extractor-boundaries.py

Run from the repo root. Read the diff with --dry-run first; this writes to
`ingest/`, which agents cannot touch (invariant 11), and that constraint is the
whole reason this is a script you execute rather than an edit I applied.

WHAT IT CHANGES, AND WHY EACH ONE

`ingest/pdf_extract.py` has no notion of where the document proper ends. Three
consequences, all measured against the 27 cached e-prints behind the 28 cards
(`ingest/audit_extraction.py` reproduces every figure below):

  1. `_pick` returns `hits[-1]` for the conclusion, on the reasoning that a
     paper saying "Discussion" mid-body and "Conclusion" at the end should give
     the second. Appendices and supplementary material come AFTER the
     conclusion and routinely contain a conclusion-shaped heading, so on those
     papers last-match reliably picks the wrong one:
       - 2506.07459 -> a 23-char supplementary `\\section{Discussion}` stub
         instead of the real 1,262-char `Conclusion`
       - 2605.29508 -> a 563-char `\\subsection*{Conclusion}` sitting INSIDE the
         appendix, about subquantum SDEs, instead of `Concluding Remarks`.
         That card's first `limitations` entry reads "Conclusion is very brief"
         -- the curator noticed and blamed the paper. Its `sections_read` says
         `conclusion`, so the field is not merely under-reporting here (sec5.4),
         it is asserting something false.

  2. The last matched section's body runs to EOF, swallowing acknowledgements,
     bibliography and appendix scaffolding. 2505.00198's conclusion measures
     8,952 chars of which ~7,750 is not conclusion.

  3. The conclusion regex misses three real headings: `conclusion\\b` fails on
     the plural ("Conclusions", 2502.11152); the pattern anchors at line start
     so a leading article defeats it ("The conclusion", 2007.11761); and it
     accepts `summary and <X>` but not a bare "Summary" (2608.16017).

Simulated across all 28 cards before writing: 3 conclusions gained, 2 re-picked
from wrong to right, 0 lost. Nothing else moves except bodies shrinking to
their real extent.

THE GUARD

The cut fires only if trimming leaves a conclusion candidate behind. A paper
whose only conclusion-shaped heading sits after the bibliography is rare and
this corpus has none; if one arrives, the guard keeps today's behaviour rather
than reporting the section missing. That cost is knowingly accepted -- on such
a paper the curator may be handed appendix text -- in exchange for the change
being unable to regress a card that currently gets a real conclusion.

In this corpus the guard declines to cut on exactly the 7 papers with no
conclusion-shaped heading anywhere, which is the intended no-op.

DELIBERATELY NOT IN THIS PATCH

  - Level-aware `SECTION_RE`. It is the right fix for the empty-intro bug
    (2411.02771) and it recovers main-results subsections currently discarded
    on theory papers (2410.16457 intro 3,168 -> 20,285 chars). It also changes
    the window for every paper that uses subsections, which makes it a
    re-curation trigger rather than a bug fix. Re-measure the level-aware
    lengths WITH this patch's boundary in place before deciding; the unbounded
    figures are misleading (2508.08218's conclusion goes to 31,170 without a
    boundary and should not).
  - Any change to the 28 existing cards. Six were built from a defective
    window; whether they are re-curated is E7's decision, not this patch's.
  - `rubrics/`, `charters/`, `.claude/**` -- untouched, per invariant 11 and
    the `.claude` hand-application convention.
"""

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- code edits

OLD_CAP = """DELAY = 3.1                 # matches arxiv_pull.py; do not lower
MAX_SECTION_CHARS = 8000    # per section, after cleaning"""

NEW_CAP = """DELAY = 3.1                 # matches arxiv_pull.py; do not lower
# Raised from 8000 on 2026-09-03. At 8000, eight sections across seven cards
# were clipped and 22,717 characters -- ~11% of the whole intro/conclusion
# corpus -- were discarded with only the truncation notice as a trace. The
# longest real slice in the KB is 14,740 (2007.11761's intro), so 16000 makes
# the cap non-binding on every card currently held, at a cost of roughly 6,000
# tokens across all 28. The end-of-body cut below also removes appendix bloat
# from conclusions, which lowers the pressure rather than raising it.
MAX_SECTION_CHARS = 16000   # per section, after cleaning"""

OLD_HEADINGS = '''# Deliberately generous on the conclusion side. A theory paper may close with
# "Discussion", "Concluding remarks", "Summary and outlook" or nothing at all,
# and a curator reading a missing conclusion writes a worse card than one
# reading a section called Discussion.
HEADINGS = {
    "intro": re.compile(r"^\\s*(\\d+[.\\s]*)?introduction\\b", re.I),
    "conclusion": re.compile(
        r"^\\s*(\\d+[.\\s]*)?(conclusion|concluding\\s+remarks|discussion"
        r"|summary\\s+and\\s+(outlook|discussion|conclusion)|outlook)\\b", re.I),
}'''

NEW_HEADINGS = '''# Deliberately generous on the conclusion side. A theory paper may close with
# "Discussion", "Concluding remarks", "Summary and outlook" or nothing at all,
# and a curator reading a missing conclusion writes a worse card than one
# reading a section called Discussion.
#
# Widened 2026-09-03 after three real headings in the KB were found unmatched:
# "Conclusions" (2502.11152) -- `conclusion\\b` fails on the plural, since `s`
# is a word character; "The conclusion" (2007.11761) -- the pattern anchors at
# line start, so any leading article defeats it; and "Summary" (2608.16017) --
# only `summary and <X>` was accepted.
#
# Note what the two branches buy. The first requires the closing word to be the
# WHOLE heading (`\\s*$`), the second allows `<word> and ...`. That is tighter
# than the old `\\b`, not looser: it drops two false positives the old pattern
# had -- "Discussion of related work" and "Conclusion of the proof", either of
# which could steal the pick as the last match. Tested against every heading in
# all 27 cached sources: exactly the three cards above change, no new matches.
HEADINGS = {
    "intro": re.compile(r"^\\s*(\\d+[.\\s]*)?introduction\\b", re.I),
    "conclusion": re.compile(
        r"^\\s*(?:\\d+[.\\s]*)?(?:the\\s+)?"
        r"(?:conclusions?|concluding\\s+remarks?|closing\\s+remarks?"
        r"|discussions?|summary|final\\s+remarks?|outlook)\\s*$"
        r"|^\\s*(?:\\d+[.\\s]*)?(?:the\\s+)?"
        r"(?:conclusions?|discussions?|summary|summaries)\\s+and\\s+", re.I),
}'''

OLD_SECTION_RE = '''SECTION_RE = re.compile(
    r"\\\\(?:sub)?section\\*?\\s*\\{((?:[^{}]|\\{[^{}]*\\})*)\\}", re.S)'''

NEW_SECTION_RE = '''SECTION_RE = re.compile(
    r"\\\\(?:sub)?section\\*?\\s*\\{((?:[^{}]|\\{[^{}]*\\})*)\\}", re.S)

# Where the document PROPER ends. Everything past the first of these is
# appendix, supplementary material or back matter, and nothing after it should
# be eligible to be returned as a conclusion or absorbed into one.
#
# Coverage in the KB's 27 LaTeX sources: a bibliography marker in 27/27, an
# appendix-family marker in 13/27. Acknowledgements and "Supplementary" headings
# were considered and dropped -- redundant given full bibliography coverage, and
# acknowledgements is the one marker that can legitimately precede a conclusion,
# so including it would add the only real failure mode for no gain.
END_OF_BODY = re.compile(
    r"\\\\appendix\\b|\\\\begin\\{appendi(?:x|ces)\\}|\\\\appendices\\b"
    r"|\\\\begin\\{thebibliography\\}|\\\\bibliography\\s*\\{|\\\\printbibliography")'''

OLD_SECTIONS = '''def _sections(tex):
    """[(heading, body)] in document order, from \\\\begin{document} onward."""
    start = tex.find("\\\\begin{document}")
    body = tex[start:] if start >= 0 else tex
    marks = [(m.start(), m.end(), m.group(1)) for m in SECTION_RE.finditer(body)]
    out = []
    for i, (s, e, head) in enumerate(marks):
        stop = marks[i + 1][0] if i + 1 < len(marks) else len(body)
        out.append((re.sub(r"\\\\[a-zA-Z]+", "", head).strip(), body[e:stop]))
    return out'''

NEW_SECTIONS = '''def _heading_texts(chunk):
    """Cleaned heading strings inside a slice of the document."""
    return [re.sub(r"\\\\[a-zA-Z]+", "", m.group(1)).strip()
            for m in SECTION_RE.finditer(chunk)]


def _sections(tex):
    """([(heading, body)], info) in document order, from \\\\begin{document} to the
    end of the document proper.

    `info` carries `cut_at` -- the offset of the first END_OF_BODY marker, or
    None -- and `cut_applied`, which is False when the guard declined. Both feed
    the missing-section diagnostic, which previously could not tell "this paper
    has no closing section" from "its closing section is inside the appendix".

    THE GUARD. Trim only if trimming leaves a conclusion candidate behind. A
    paper whose only conclusion-shaped heading sits after the bibliography is
    rare and this corpus has none; if one arrives, keeping today's behaviour is
    the conservative choice, at the known cost that the curator may be handed
    appendix text on such a paper. What it buys is that this change cannot
    regress a card that currently receives a real conclusion.
    """
    start = tex.find("\\\\begin{document}")
    body = tex[start:] if start >= 0 else tex
    full_len = len(body)

    cut = END_OF_BODY.search(body)
    cut_at = cut.start() if cut else None
    cut_applied = False
    if cut_at is not None:
        head = body[:cut_at]
        if any(HEADINGS["conclusion"].match(h) for h in _heading_texts(head)):
            body, cut_applied = head, True

    marks = [(m.start(), m.end(), m.group(1)) for m in SECTION_RE.finditer(body)]
    out = []
    for i, (s, e, head) in enumerate(marks):
        stop = marks[i + 1][0] if i + 1 < len(marks) else len(body)
        out.append((re.sub(r"\\\\[a-zA-Z]+", "", head).strip(), body[e:stop]))
    return out, {"cut_at": cut_at, "cut_applied": cut_applied,
                 "full_len": full_len}'''

OLD_CALL = '''    sections = _sections(tex)
    if not sections:'''

NEW_CALL = '''    sections, docinfo = _sections(tex)
    if not sections:'''

OLD_DIAG = '''            out["missing"][w] = (
                f"no section heading matched; document has: "
                f"{', '.join(h for h, _ in sections[:8])}")
            continue'''

NEW_DIAG = '''            # Report the END of the heading list, not the start. The old
            # message printed the first eight marks -- which include
            # subsections, so on a paper of any depth it never reached the
            # closing section and read as "this paper has no conclusion". That
            # is how 2608.16017's `\\section{Summary}` stayed invisible from
            # Week 2 to 2026-09-03, and why WEEK-2-PLAN.md's open item on it
            # could not be resolved by reading the output.
            heads = [h for h, _ in sections]
            note = (f"no section heading matched; {len(heads)} headings, "
                    f"ending: {', '.join(heads[-6:]) or '(none)'}")
            if docinfo["cut_at"] is not None:
                pct = 100.0 * docinfo["cut_at"] / max(1, docinfo["full_len"])
                note += (f"; back matter begins at {pct:.0f}% and was "
                         f"{'trimmed' if docinfo['cut_applied'] else 'NOT trimmed'} "
                         f"before matching")
            out["missing"][w] = note
            continue'''

# ---------------------------------------------------------------- doc edits

OLD_D2 = """- [ ] **D2.** Correct the card count wherever it appears

  The KB holds **30** cards — probability 11, compbio_methods 10,
  compbio_mechanism 6, stats 3 — not the 28 in `CLAUDE.md` line 10 and the
  handoffs. `CARD-EVAL-HANDOFF.md` §3 likewise tabulates 21 sampled cards where
  `card_labels.jsonl` holds 20. Both are the failure `_load_cards` warns about:
  a number written down once and never re-derived."""

NEW_D2 = """- [ ] **D2.** Correct the sampled-card count in `CARD-EVAL-HANDOFF.md` §3

  **Rewritten 2026-09-03; the previous version of this item was wrong and
  executing it would have introduced the error it was filed to remove.** It
  claimed the KB holds 30 cards — probability 11, compbio_methods 10 — and that
  the 28 in `CLAUDE.md` line 10 was the mistake. **28 is correct**: probability
  10, compbio_methods 9, compbio_mechanism 6, stats 3, and all four
  `index.jsonl` files agree, as does `PROJECT-STATUS.md` §2. No card count needs
  changing anywhere.

  What survives: `CARD-EVAL-HANDOFF.md` §3 tabulates 21 sampled cards where
  `card_labels.jsonl` holds 20. That one is real.

  The item is left here rather than deleted because it is the sharpest instance
  of the failure `_load_cards` warns about — a number written down once and
  never re-derived — and this time the correction was the thing that went
  unchecked. Re-derive before quoting; never trust a document that counts."""

OLD_DEV_HEADER = "### Development — build or fix the machinery"

NEW_DEV_HEADER = """### Development — build or fix the machinery

- [ ] **D0.** Bound `pdf_extract.py` at the end of the document proper —
  **APPLIED by patch 1, 2026-09-03** (`patches/patch-01-extractor-boundaries.py`;
  see `patches/README.md` for the ledger)

  Ungated, and it sat above E3 because E3 spends curator calls to build the
  sample E6 scores, and every card E3 writes inherits the extractor's window.
  Reproduce with `python3 ingest/audit_extraction.py`.

  Six of 28 cards were built from a defective window: three whose real closing
  section was missed by the heading regex (2007.11761 "The conclusion",
  2502.11152 "Conclusions", 2608.16017 "Summary"), two handed a conclusion-shaped
  heading from inside the appendix instead of the real one (2506.07459,
  2605.29508), and one whose intro came back empty while being reported as found
  (2411.02771). Two of the three stats cards are in that set, which is the domain
  the project chose to measure on.

  **Still open, and deliberately not in that patch:** level-aware `SECTION_RE`.
  It fixes the empty intro and recovers main-results subsections currently
  discarded on theory papers, but it changes the window for every paper using
  subsections, so it is a re-curation trigger rather than a bug fix. Re-measure
  with D0's boundary in place first — the unbounded figures overstate it.
  **Gates:** E3, and any decision about re-curating the six affected cards (E7)."""

OLD_52 = """2. **\"Conclusion section was not matched by the extractor\" — a real bug.**
   2410.16457 and 2309.12441 both say this. There the curator *asked* for the
   conclusion and did not get it. That is a genuine `pdf_extract.py` section-matching
   failure, and it is worth fixing: 2606.07914 is the one card where the conclusion
   *was* matched, and its `limitations` are visibly sharper — two bullets sourced
   near-verbatim to the conclusion instead of inferred."""

NEW_52 = """2. **\"Conclusion section was not matched by the extractor\" — a real bug, but
   not on the cards named here. Corrected 2026-09-03.**

   The original text cited 2410.16457 and 2309.12441 as the evidence. Both are
   wrong: reproduced from the cached e-prints, **neither paper has a closing
   section of any kind**, so both cards are correct and there is no bug on
   either. Seven of the twelve cards without a delivered conclusion are in that
   position — 2109.02644, 2307.13826, 2309.12441, 2401.16556, 2410.16457,
   2605.29962, 2512.16061 — and 2408.14242 is a PDF-only submission with no
   LaTeX source at all.

   The bug is real and lands on a disjoint set of six cards, all now fixed by
   patch 1, 2026-09-03 (`patches/patch-01-extractor-boundaries.py`; see
   `TODO.md` D0):
   three missed by the heading regex, two handed an appendix heading by
   `_pick`'s last-match rule, one whose intro came back empty while reported as
   found. `ingest/audit_extraction.py` reproduces the classification.

   Two consequences for the rest of this file. **§5.2's policy question was
   argued against the wrong data**: on 2410.16457, "Circular law for general
   models" and "Weak delocalization estimates" are §1.2 and §1.3 — inside the
   curator's requested window, discarded by a boundary bug rather than excluded
   by design. And **§5.4's reading of `sections_read` is too kind**: on
   2605.29508 it claims `conclusion` while the delivered text was an appendix
   subsection, so the field can mis-report, not merely under-report.

   The corroboration in the other direction still stands unchanged: 2606.07914
   is a card where the conclusion *was* matched, and its `limitations` are
   visibly sharper — two bullets sourced near-verbatim to the conclusion instead
   of inferred."""

OLD_KL = '| 2608.17381 | `KL divergence` → "trust region" |'
NEW_KL = ('| 2506.07459 | `KL divergence` → "trust region" — **attributed to '
          '2608.17381 until 2026-09-03; that card has no KL object.** '
          'So these defects span four cards, not five, and 2506.07459 carries two |')

OLD_71 = """### 7.1 Does `aliases` mean synonyms, or related terms worth matching on?

Determines whether roughly **half** the object defects across five cards are
defects. Under \"synonyms\", `GRPO → DPO` and `Unitary synthesis → unitary
compilation` are false identities that merge concordance nodes. Under \"related
terms\", both are fine. `card_schema.json` does not say."""

NEW_71 = """### 7.1 Does `aliases` mean synonyms, or related terms worth matching on? — **RULED 2026-09-01; propagated here 2026-09-03**

**Synonyms.** The ruling and its reasoning live in
`dev-notes/curator-prompt-edits-pending.md` under \"Context: the §7.1 ruling that
item 4 implements\" — *\"`aliases` means synonyms. Settled 2026-09-01\"* — with
five corroborating files, a rejected `related:` field, and the asymmetry caveat.
`card_schema.json`'s `aliases` description carries it, and
`compbio-mechanism-curator.md` carries it in prose with a worked example.

The version of this section that stood until 2026-09-03 said
\"`card_schema.json` does not say\", which had been false for two days, and
predicted the ruling would dissolve roughly half the alias defects. **It does the
opposite: five of six stand.** The corrected table is in the dev-note.

Three things the ruling does not settle, and they are the live part:

1. **Retroactivity.** The 28 existing cards were written under prose compatible
   with either reading. `source_version`'s precedent — \"make it required after a
   re-curation pass, not before\" — and Tier 4's rule against spending model
   calls before the schema is known stable both point at forward-only, with the
   re-curation question handed to E7.
2. **Enforcement.** `card_eval.py` contains no occurrence of \"alias\": no
   prompt, no letter, no tally. §5.6 item 1 names \"object right, alias wrong\" as
   a gap and §7.5 declines to give it a letter, so the defects the ruling makes
   real are invisible to `score`. False merges are already countable as
   `conceptual-math`; **under-population has no tag at all**, and the dev-note
   calls it the more expensive failure. `score_run` has `objects_missed` and no
   `aliases_missed`.
3. **One of the user's own files is in violation.** The worked example states
   that `factor graph inference` fails the rule as a broader family. That pair is
   an alias on `belief propagation` in `kb/concordance_user.jsonl`, which is
   agent-denied, and `math-scout` — the component invariant 15 designates to
   arbitrate identity — has never run."""

OLD_PS_SCRIPTS = ("| Scripts | `run_triage`, `apply_triage`, `pdf_extract`, "
                  "`rebuild_index` all written and exercised |")
NEW_PS_SCRIPTS = ("| Scripts | `run_triage`, `apply_triage`, `pdf_extract`, "
                  "`rebuild_index` all written and exercised. `pdf_extract` was "
                  "exercised *and defective*: six of 28 cards were built from a "
                  "short window, fixed 2026-09-03 (`TODO.md` D0). Exercised is not "
                  "measured |")

OLD_OQ_ENV = """**Environment note:** the Linux sandbox will not start on this machine, so anything marked
**[shell]** has to run on your side. I can write and edit files, not execute them."""

NEW_OQ_ENV = """**Environment note:** **test this rather than believing it** — it has been false in at
least one session (2026-09-03), where read-only diagnostics ran locally and produced
`TODO.md` D0. Two caveats survive even when the sandbox does start: there is no network,
so anything resolving against arXiv or OpenAlex is still your side; and a sandbox holds a
*copy* of the repo, so state-mutating runs do not transfer. Read-only diagnostics against
`ingest/cache/` and `papers.sqlite` are the useful class. Items marked **[shell]** that
need the network, or that write state you intend to keep, remain yours."""

# ------------------------------------------------------------------- driver

def _say(*args):
    """print() that survives a closed stdout.

    `| head`, or quitting `less`, raises BrokenPipeError on the next write. In a
    script that mutates files that must not cancel the run, and must not abort
    it midway either -- so every message goes through here and the writes happen
    before any of them.
    """
    try:
        print(*args)
    except BrokenPipeError:
        pass


EDITS = [
    ("ingest/pdf_extract.py", "raise MAX_SECTION_CHARS to 16000", OLD_CAP, NEW_CAP),
    ("ingest/pdf_extract.py", "widen the conclusion heading regex", OLD_HEADINGS, NEW_HEADINGS),
    ("ingest/pdf_extract.py", "add END_OF_BODY", OLD_SECTION_RE, NEW_SECTION_RE),
    ("ingest/pdf_extract.py", "trim to the document proper, guarded", OLD_SECTIONS, NEW_SECTIONS),
    ("ingest/pdf_extract.py", "unpack the new _sections return", OLD_CALL, NEW_CALL),
    ("ingest/pdf_extract.py", "report the heading tail and the cut", OLD_DIAG, NEW_DIAG),
    ("TODO.md", "rewrite D2 (28 is correct, not 30)", OLD_D2, NEW_D2),
    ("TODO.md", "insert D0 above the Development backlog", OLD_DEV_HEADER, NEW_DEV_HEADER),
    ("CARD-EVAL-HANDOFF.md", "correct §5.2's evidence base", OLD_52, NEW_52),
    ("CARD-EVAL-HANDOFF.md", "fix the §5.3 KL misattribution", OLD_KL, NEW_KL),
    ("CARD-EVAL-HANDOFF.md", "propagate the §7.1 ruling", OLD_71, NEW_71),
    ("PROJECT-STATUS.md", "note pdf_extract was exercised and defective", OLD_PS_SCRIPTS, NEW_PS_SCRIPTS),
    ("OPEN-QUESTIONS.md", "amend the stale environment note", OLD_OQ_ENV, NEW_OQ_ENV),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change and exit without writing")
    ap.add_argument("--no-backup", action="store_true",
                    help="skip the .pre-patch.bak copies")
    a = ap.parse_args()

    if not (ROOT / "ingest" / "pdf_extract.py").exists():
        sys.exit(f"not a research-net checkout: {ROOT}\n"
                 f"  run this from the repo root, as "
                 f"`python3 patches/{Path(__file__).name}`")

    # Not fatal, but say it loudly: the doc edits below name
    # ingest/audit_extraction.py as the reproducer for their figures, per
    # PROJECT-STATUS.md sec6 item 5. If it is not there, this patch creates
    # exactly the dangling reference it spends four edits correcting elsewhere.
    if not (ROOT / "ingest" / "audit_extraction.py").exists():
        _say("  NOTE     ingest/audit_extraction.py is not present. The doc\n"
              "           edits reference it as the reproducer for their\n"
              "           numbers. Move it there (it ships in patches/) before\n"
              "           you commit, or those references dangle.\n")

    # ---- preflight. All or nothing: a half-applied patch to the extractor is
    # worse than an unapplied one, because the failure would show up as card
    # drift weeks later rather than as a traceback now.
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
                 f"  If a file has changed since, apply those edits by hand and\n"
                 f"  re-run -- applied edits are detected and skipped.")
    if not todo:
        _say("\nnothing to do; all edits already present.")
        return
    if a.dry_run:
        _say(f"\n--dry-run: {len(todo)} edit(s) would be applied across "
              f"{len({r for r, _, _, _ in todo})} file(s). Nothing written.")
        return

    # ---- stage the edits in memory, per file
    staged = dict(cache)
    for rel, label, old, new in todo:
        staged[rel] = staged[rel].replace(old, new, 1)

    # ---- apply. Every write completes BEFORE anything is reported, so that a
    # closed stdout -- `| head`, quitting `less` -- cannot kill the process
    # midway through the write loop and leave the half-applied state the
    # preflight above exists to prevent. Found the hard way.
    touched = sorted({rel for rel, _, _, _ in todo})
    for rel in touched:
        p = ROOT / rel
        if not a.no_backup:
            # Same convention as OPEN-QUESTIONS.md.pre-prune.bak and
            # eval/labels.jsonl.pre-redomain.bak.
            shutil.copy2(p, p.with_suffix(p.suffix + ".pre-patch.bak"))
        p.write_text(staged[rel])

    for rel in touched:
        _say(f"  wrote    {rel}")

    _say(f"\n{len(todo)} edit(s) applied to {len(touched)} file(s).")
    _say("\nVerify, in this order:")
    _say("  python3 -c \"import ast,pathlib;"
         "ast.parse(pathlib.Path('ingest/pdf_extract.py').read_text())\"")
    _say("  python3 ingest/audit_extraction.py")
    _say("     -> expect: 0 truncated, 0 unmatched closing sections,")
    _say("        1 empty (2411.02771's intro, still open), 7 with none")
    _say("  git diff --stat")
    _say("\nThen commit. The .pre-patch.bak files are redundant once you have.")


if __name__ == "__main__":
    main()
