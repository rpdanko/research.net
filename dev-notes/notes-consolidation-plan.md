# Consolidating the status documents

Written 2026-09-01, from a header pass over every root `*.md` plus targeted
reads. **Execute after the first `card_eval.py score` run, not before** — see
Sequencing. Delete this file once executed; it is a plan, not a record, and a
plan that outlives its execution becomes another stale document, which is the
problem it exists to fix.

Yes, this is a sixteenth document. It is meant to be consumed and removed.

---

## The evidence

### 1. The entry point is wrong in two places

`CLAUDE.md` is what every agent reads first.

- **Line 5** — "`WEEK-1-PLAN.md` is the active phase." `WEEK-3-PLAN.md` exists,
  and `PROJECT-STATUS.md` supersedes *that*. Agents are pointed two phases back.
- **Line 13** — "`card_eval.py` does not exist." It is roughly a thousand lines
  and was edited on 2026-09-01.

Both are already recorded as needing fixing — `PROJECT-STATUS.md` Tier 0 item 4,
`ESCALATION-REVIEW.md` §6 item 3 — and neither has been applied. Exact proposed
text is in `dev-notes/curator-prompt-edits-pending.md` §10.

### 2. Fifteen documents carry an action or decision list

`HANDOFF` §5 · `DAY-5-HANDOFF` §3, §4, §6 · `WEEK-2-HANDOFF` "To do, in order" ·
`WEEK-1-PLAN` · `WEEK-2-PLAN` · `WEEK-3-PLAN` §1–§3 · `PROJECT-STATUS` §5 ·
`CARD-EVAL-HANDOFF` §6 · `RUNBOOK-first-measurement` phases ·
`EVAL-01-FINDINGS` §5 · `ESCALATION-REVIEW` §6 · `DISTORTION-REVIEW` §6 ·
`HYBRID-SYSTEM-REVIEW` §4 · `dev-notes/curator-prompt-edits-pending` · `TODO.md`.

At least three separate "Done means" definitions: `DAY-5-HANDOFF` §5,
`WEEK-3-PLAN`, `PROJECT-STATUS` §6.

Measured cost, 2026-09-01: assembling the pending `.claude/` work required a grep
across five documents, and of the items found, one was already applied, one
described a problem already solved, and one pointed at a corrected file that had
been lost when a scratchpad cleared.

### 3. A live blocking decision sits outside the decision register

`LABEL-USE-PROTOCOL.md` "Outstanding decision" closes:

> "I won't propose charter revisions from the labels until this is settled either way."

That blocks charter work and is not in `OPEN-QUESTIONS.md`.

### 4. There is an unnamed genre, and it is load-bearing

`HYBRID-SYSTEM-REVIEW`, `DISTORTION-REVIEW` and `ESCALATION-REVIEW` are the same
artifact three times: an external source read against the repo, with changes
proposed or built. Invariants 13–16 and 17–19 trace to two of them, and
`CLAUDE.md` instructs the reader to consult the relevant one before touching
either group. **These are reference, not status.** They must be grouped and
explicitly exempted from archiving.

### 5. The convention already exists — it was used once

`PROJECT-STATUS.md` lines 3–4:

> "Written 2026-08-28. Supersedes `WEEK-3-PLAN.md` as the live to-do; that file
> stays as the record of what Week 3 opened with."

That is the correct pattern in full: declare supersession, keep the superseded
file as record. It appears in one file of fifteen. **Most of this plan is
propagating a convention the repo already chose, not importing a new one.**

---

## Target structure

**Entry — `CLAUDE.md`.** Corrected, pointing only at the live layer.

**Live layer — these three, and nothing else, carry current state:**

| File | Holds | Rule |
|---|---|---|
| `TODO.md` | the next action, and the backlog | the only action list in the repo |
| `PROJECT-STATUS.md` | what is true now | the only "current state" document |
| `OPEN-QUESTIONS.md` | decisions, open and settled | the only decision register |

`focus.md` stays outside this. It is a user-owned input channel under invariant
13, not a status document, and `settings.json` denies agents write access to it.

**Archive.** Every plan and handoff takes the `PROJECT-STATUS` supersession
header and stops being consulted for current state. The chain is already
chronological: `HANDOFF` → `DAY-5-HANDOFF` → `WEEK-1/2/3-PLAN` and
`WEEK-2/3-HANDOFF` → `CARD-EVAL-HANDOFF`. Also archival: `QUALITATIVE-CHECK`
(a one-off verification tied to `WEEK-1-PLAN` §6), and the `charters/*.rewrite-prep`
and `PASS-4-DRAFTS` working documents.

**Reference — never archived, never rewritten.** The three source reviews, moved
to `dev-notes/source-reviews/`; `README.md`; `research-network-architecture.md`;
`RUNBOOK-first-measurement.md`; the protocol half of `LABEL-USE-PROTOCOL.md`.

---

## Migrations

1. **`CARD-EVAL-HANDOFF` §7 → `OPEN-QUESTIONS`.** The §7.1, §7.4 and §7.5
   rulings made on 2026-09-01 are decisions, and they currently live in a
   document whose entire genre is going stale. §7.2 and §7.3 are still open and
   belong in the register for that reason too.
2. **`LABEL-USE-PROTOCOL` "Outstanding decision" → `OPEN-QUESTIONS`.** See
   evidence 3.
3. **Remaining action lists → `TODO.md` backlog.** `ESCALATION-REVIEW` §6,
   `EVAL-01-FINDINGS` §5, `CARD-EVAL-HANDOFF` §6, `PROJECT-STATUS` §5. Each
   source section becomes a pointer to `TODO.md` rather than a list.
4. **`PROJECT-STATUS` §5 Tier 0/Tier 1 → `TODO.md`.** This is the one that will
   feel wrong, because Tier 0/1 is good. But two action lists is the disease, and
   `TODO.md` is what `pmd` reads. `PROJECT-STATUS` keeps §1–§4 and §6.

---

## What not to touch

**Anything containing a retraction.** These are the reason the repo's
conclusions are worth anything, and a consolidation that flattens them removes
the evidence that the conclusions were tested:

- `CARD-EVAL-HANDOFF` §5.2 — "Corrected 2026-08-30 after checking the curator prompts"
- `CARD-EVAL-HANDOFF` §5.1 — two recorded instances of scoring a card against the wrong version
- `CARD-EVAL-HANDOFF` §4 — the mid-session citation-discipline correction
- `ESCALATION-REVIEW` §5 — "A correction, recorded because the first version of this review got it wrong"
- `DISTORTION-REVIEW` §1 and `ESCALATION-REVIEW` §1 — "how much of it to believe"

Archive them. Never rewrite them.

**`charters/`, `rubrics/`, `focus.md`** — user's handwriting, agent-denied by
`settings.json`, invariant 11.

**The three source reviews' content** — reference, per evidence 4.

---

## Sequencing

**Now, independent of everything else:** the `CLAUDE.md` fix. Two false
sentences in the file every agent boots from, five minutes, already Tier 0.

**After the first `score` run:** everything else. The argument is not that the
consolidation is unimportant but that the first run will change what the notes
need to say — it is expected to produce a bug list rather than numbers, and that
bug list is itself content for `TODO.md` and `OPEN-QUESTIONS`. Consolidating
first means consolidating against a state that is about to move.

The wedge is already in: `TODO.md` has been the single action list since
2026-09-01, so no *new* duplication is accumulating while this waits.

---

## Limits of this plan

The read pass covered headers across every root document and full text on
roughly a third. That is enough to **classify** every document with confidence
and enough to justify the structure above. It is **not** enough to execute
migrations 1 and 2 safely — both `CARD-EVAL-HANDOFF` §7 and `OPEN-QUESTIONS`
need a full read before content moves between them, and `LABEL-USE-PROTOCOL`
needs one before its decision is lifted out of context.

Not read in full: `WEEK-1-PLAN`, `WEEK-3-HANDOFF`, `HANDOFF`, `DAY-5-HANDOFF`,
`research-network-architecture.md`, `RUNBOOK-first-measurement`, and the bodies
of the three source reviews.
