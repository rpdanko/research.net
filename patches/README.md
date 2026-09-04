# patches/

Scripts that edit files agents cannot write.

`ingest/`, `charters/`, `rubrics/`, `focus.md`, `kb/concordance_user.jsonl` and
`ledger/user_verdicts.jsonl` are denied in `.claude/settings.json` (invariant
11), and `.claude/**` is applied by hand. A patch here is how a change to one of
those arrives with its reasoning attached and without an agent holding the pen:
the text is proposed, you read the diff, you run it.

This is the same arrangement `dev-notes/curator-prompt-edits-pending.md` already
uses for `.claude/**`. The difference is only that these are executable, because
`ingest/` is code and a prose diff of a regex is hard to check by eye.

Nothing permanent lives here. A diagnostic or script that a patch introduces
belongs in `ingest/` with the rest of them; this directory is only the delivery
route, because that is the one place an agent cannot write.

## Naming and order

`patch-NN-short-slug.py`, numbered in the order they are meant to be applied,
zero-padded so lexical sort is application order. **Numbers are never reused**,
including after a patch is deleted — a gap in the sequence is the record that
something was applied and consumed, and the ledger below says what it was.

The number carries order; the docstring and the prose it writes into the
documents carry the date, matching how this repo already marks corrections
(`CLOSED 2026-09-01`, `Corrected 2026-08-30`). Both, because a patch is deleted
eventually and the date has to survive in the documents it edited.

Diagnostics are **not** numbered. They are not applied, they are run, and giving
one a patch number would put it in a sequence it does not belong to.

## Running one

```bash
python3 patches/patch-NN-<slug>.py --dry-run     # always first
python3 patches/patch-NN-<slug>.py
```

Every patch here must:

- **Preflight all or nothing.** Verify each anchor appears exactly once before
  writing anything. A half-applied patch to `ingest/` surfaces as card drift
  weeks later instead of a traceback now.
- **Be idempotent.** Detect already-applied edits and skip them, so a partial
  hand-application followed by a re-run is safe.
- **Back up** to `<file>.pre-patch.bak`, matching the existing convention
  (`OPEN-QUESTIONS.md.pre-prune.bak`, `eval/labels.jsonl.pre-redomain.bak`).
- **Carry its reasoning in the module docstring**, not in a commit message.
  Per `PROJECT-STATUS.md` §1 item 7, the reason has to survive next to the
  change, and a patch that outlives its rationale is the same failure as a
  status document nobody re-derived.
- **Name what it deliberately leaves undone**, so the next session can tell
  "considered and rejected" from "never thought of".

Patches are consumed, not maintained. Once applied and committed, a patch is a
record; delete it when its content has landed in the documents it edited.

## Ledger

Append a row when you write a patch; update its state when you run it. This
table is the order of record — the filenames follow it, not the reverse.

| # | Patch | Applied | Touches | What it did |
|---|---|---|---|---|
| 1 | `patch-01-extractor-boundaries.py` | 2026-09-03 | `ingest/pdf_extract.py`, `TODO.md`, `CARD-EVAL-HANDOFF.md`, `PROJECT-STATUS.md`, `OPEN-QUESTIONS.md` | Bounded the extractor at the end of the document proper, with the candidate guard; widened conclusion heading matching; raised `MAX_SECTION_CHARS` to 16000; fixed the truncated missing-section diagnostic. Docs: `TODO.md` D0 added and D2 rewritten, `CARD-EVAL-HANDOFF.md` §5.2 evidence corrected / §5.3 misattribution / §7.1 ruling propagated. 13 edits, 5 files. |

### Not a patch

`audit_extraction.py` ships in this directory but **belongs in `ingest/`** —
move it there before committing patch 1:

```bash
git mv patches/audit_extraction.py ingest/audit_extraction.py
```

It is a diagnostic, not a patch: it is run, not applied, and it outlives the
patch that introduced it. `TODO.md` D0, `CARD-EVAL-HANDOFF.md` §5.2 and
`PROJECT-STATUS.md` §3 all quote its output, and `PROJECT-STATUS.md` §6 item 5
forbids a document quoting a metric without naming where it came from. If it
ever disagrees with those documents, they are wrong.

It sits here only because `ingest/` is agent-denied (invariant 11) and a patch
directory was the available delivery route. Patch 1's doc edits already point at
`ingest/audit_extraction.py`, and the patch prints a NOTE if the file is not
there yet — so the two steps can be done in either order, but both are needed or
those references dangle.
