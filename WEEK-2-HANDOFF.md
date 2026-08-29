# Week 2 handoff

## Purpose reminder

research-net is a continuous multi-agent system that maintains knowledge
bases in statistics, probability, and computational biology (methods +
mechanism), sources the mathematics underneath them, and proposes research
at their intersections — put through peer review and cheap numerical
falsification before reaching you. Week 1 built the piece that decides what
gets into the knowledge bases at all: canon, charters, and a measured triage
step. Week 2 is where the downstream half — cards, concordance, bridges —
starts running for the first time.

## Where Week 1 landed

All four `WEEK-1-PLAN.md` §6 done-criteria met on run `20260827-203053`:
recall 0.901, precision 0.688, borderline agreement 0.78, qualitative
reason-check 9/10. Four charters promoted (`stats.md`, `probability.md`,
`compbio_methods.md`, `compbio_mechanism.md` — the last untouched by labels,
n=5 stayed below the protocol floor). `run_triage.py` built and working
end-to-end. Full writeup: `QUALITATIVE-CHECK.md`.

`apply_triage.py` does not exist yet. Nothing past triage — cards, KB
writes, concordance, bridges — has ever run.

---

## To do, in order

### 1. Apply `.claude/settings.json`

Sitting in the outputs folder from last session, not yet copied over. Fixes
13 silently-broken `Write(path)` → `Edit(path)` permission rules — until
this is applied, the guardrails protecting `charters/`, `rubrics/`,
`ingest/`, and `focus.md` from agent writes are not actually enforced.
Five-second fix, do it before anything else touches those directories.

### 2. Build `apply_triage.py`

The real Week 2 blocker (`OPEN-QUESTIONS.md` §0.2). Needs to: write
`domain` into `papers.sqlite` (currently null on every row — `eval_triage.py`
only works around this, doesn't fix it), dispatch curator agents on
triage-admitted papers, write cards to `kb/`, and apply the ambiguous-tier
logic that's been sitting inert since it was built (charters' §5, `triage.md`,
`coalition_audit.py`'s 40% warning — none of it has ever run).

### 3. Rule on the `compbio_methods` firehose

`OPEN-QUESTIONS.md` §1.1. Your own 180 labels now make the choice
measurable: option 3 (ranked queue, cap = top 10 by score) retains 76 of 76
admits; options 1 and 2 discard 85%+. This also gates re-harvesting — decide
before pulling more data, not after. My recommendation stands: option 3,
plus an explicit edit to `daily-ingest.md` since it currently says the cap
is a throughput control, not a ranking cutoff.

### 4. Two loose threads from today's qualitative check

- **`stats` exemplar set may be thin on forecasting/time-series cases.**
  Triage admitted `2608.20406` (an Ontario COVID case-study paper) without
  applying the A4 single-dataset exclusion `stats.md` §3 was rewritten to
  catch. Worth checking whether the negative exemplars skew toward the
  psych/poli-sci pattern §A3 flags and don't cover this shape at all.
- **Recheck `2509.18530`'s label.** `my_score: 2` in `labels.dev.jsonl`,
  but `compbio_methods.md` §2's own "approximation quality" clause reads it
  as in-scope, and triage's score-5 call looks charter-faithful. Your call,
  not mine — I didn't touch the label.

### 5. Label hygiene and calibration re-run

Both cheap, both stale (`OPEN-QUESTIONS.md` §1.2–1.3):
- Three borderline rows still read `"Borderline"` (capitalized) — invisible
  to `score_run()`'s case-sensitive check. One row (`2608.07528`) still has
  the malformed stratum `"pit"` and needs your call on what it should be.
- `calibrate()`'s NEAR/FAR thresholds (0.57/0.59, "distributions overlap
  almost completely") were computed against the pooled pre-fix canon. Worth
  a clean re-run now that domain-scoping is fixed — may turn out to be a
  real canon/domain-map signal rather than noise.

### 6. Decide on a fresh, held-out eval set

`OPEN-QUESTIONS.md` §1.6. `labels.dev.jsonl` trained `compbio_methods.md`'s
two label-derived clauses; measuring that charter against the same labels
again would be circular. If you want a real (non-dev) measurement later,
draw 60–80 fresh papers — and shuffle `sample()`'s output after banding
first, since the existing set arrived in same-band streaks that invite
anchoring.

### 7. `compbio_mechanism` — still the least-measured charter

Only 5 labelled papers, below the protocol floor for any label-derived
text (`OPEN-QUESTIONS.md` §1.5). Carries the popgen/phylogenetics admission
decision made on bridge-finding grounds against your own stated scope
preference — the charter most worth a closer look and the one with the
least evidence. A targeted `sample --append` restricted to `q-bio.*` would
fix the labelling gap; no rewrite-prep doc exists for it yet either
(§2.2), unlike `stats`.

### 8. Small and easy to lose (`OPEN-QUESTIONS.md` Tier 3)

- Domain-map coverage gap: 7 labelled papers (`math.NA`/`NT`/`CO`/`GT`)
  match no `SETS` entry at all and all scored ≥4 — a harvest gap, not a
  scope question.
- `vetting-stats.md` line 334: reason text landed in the wrong field, lost.
- `vetting-compbio_methods.md` line 148 (`W4408399347`): never marked.
- Stray empty file `research-net/To` — shell redirect typo, safe to delete.
- Confirm the superseded files (`compbio.md`, `compbio_genomics.md`, two
  old curator agent files) should stay in place rather than be removed.
