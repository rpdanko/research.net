# Runbook — the first measured triage run

Follow in order. Each step says what you should see and when to stop. Run everything
from the repo root.

**One thing to settle first, because it's the question that costs data if you get it
wrong: do NOT prepare one domain at a time.** A single `prepare` covering all four
domains produces one run directory with per-domain batches inside it. Four separate
per-domain prepares produce four run directories, and `collect` writes
`predictions.jsonl` from one run — so you would end up with only the last domain's
predictions and a recall number computed over a quarter of your labels. The
per-domain batching happens automatically inside one run.

The stats-only run you already made (`20260827-133356`) is harmless. Leave it; the
next prepare becomes the latest.

---

## Phase 0 — prerequisites

### 0.1 Register the agents

```bash
mv claude-config .claude
```

Owed to `README.md` line 12 and `HANDOFF.md` line 12 since setup. Until this runs, the
`triage` subagent does not exist as far as Claude Code is concerned, and nothing can
dispatch to it by name.

**Check:** `ls .claude/agents/ | wc -l` → **15 files**, of which 13 are active agents and
2 are superseded (`compbio-curator.md`, `compbio-genomics-curator.md`). `CLAUDE.md` line 78
says 12; that count predates the compbio split turning one curator into two.

Note the asymmetry while you're here: `compbio-genomics-curator.md` has `-SUPERSEDED`
appended to its `name:` field so it cannot be dispatched under the old name, but
`compbio-curator.md` kept its plain `name: compbio-curator` and is still resolvable. The
description warns; the name is the interface. Worth hardening for symmetry.

### 0.2 Fix the label strata

```bash
python3 ingest/fixup_labels_stratum_domain.py
```

Backs up to `eval/labels.jsonl.bak`, normalises `stratum` to
`expect_in`/`expect_out`/`borderline`, backfills `domain` from `categories`.

**Why before scoring, not after:** `score_run()`'s borderline check is
`st.startswith("border")` and is case-sensitive. Three rows currently read
`"Borderline"`, so they are invisible to it — and with only 32 borderline rows in the
whole set, that is ~10% of the one metric `WEEK-1-PLAN.md` §6 calls the number that
actually matters.

**Expect:** exactly one unresolved row reported — `2608.07528`, currently
`stratum: "pit"`.

### 0.3 Hand-fix that one row

Open `eval/labels.jsonl`, find `2608.07528` — *"The Knowing-Saying Gap: When Probes See
Errors that Confidence Misses"*, a probing/LLM-interpretability paper you scored 2 —
and set its `stratum` to `expect_in`, `expect_out` or `borderline` from your own read.
The script won't guess at a typo it can't place.

**Check:** `grep -c '"stratum": "expect_in"\|"stratum": "expect_out"\|"stratum": "borderline"' eval/labels.jsonl` → **180**.

### 0.4 Do NOT rename labels.jsonl yet

`LABEL-USE-PROTOCOL.md` R8's rename only applies once a charter is written *from* the
labels. `stats.pass4.md` has zero label-derived changes, and the `compbio_methods`
drafts in `PASS-4-DRAFTS.md` have not been applied. So nothing is contaminated yet and
the default path is correct.

---

## Phase 1 — the calibration decision

### 1.1 Re-run calibrate

```bash
python3 ingest/eval_triage.py calibrate
```

The earlier NEAR=0.57 / FAR=0.59 result was computed pre-fix against the whole pooled
canon instead of one domain's slice. This run infers domain fresh, so it is the first
honest reading.

### 1.2 Decide — and this gates Phase 2

Your stats prepare banded 40 papers as **near 13 / mid 25 / far 2**. Two papers in the
`far` band means the wildcard channel — which `triage.md` calls the only route open to
work the canon cannot see — will barely be exercised. That is a signal about the
shipped 0.62/0.38 defaults, not about your papers.

- **If calibrate suggests values and the distributions separate:** edit `NEAR`, `FAR` in
  `ingest/canon_index.py` **now**, before Phase 2.
- **If it still reports the distributions overlap almost completely:** change nothing.
  `DAY-5-HANDOFF.md` §3.5 is right — that means similarity is not separating your
  classes, and the honest response is to fix the canon or the domain map, not to ship a
  band that adds noise. Proceed with the defaults and note it when you read the results.

**Critical ordering:** bands are baked into the run's manifest at prepare time and are
what `collect` writes as each paper's `threshold`. If you change `NEAR`/`FAR` after
preparing, the prepared batches are stale — re-run prepare.

---

## Phase 2 — baseline measurement, against the pass-3 charters

Measure what you have before you change it. `eval_triage.py diff` exists precisely to
compare two runs, and it is only meaningful if the first one is a genuine before.

### 2.1 Prepare all domains

```bash
python3 ingest/run_triage.py prepare
```

**Expect:** ~8 batches over 4 domains, ~180 papers, a printed band histogram and a
per-domain count. Note the run stamp it prints.

The per-domain counts will not match the table in `OPEN-QUESTIONS.md` §1.5 — that used
primary category as a proxy, and `_infer_domain` matches *any* category against `SETS`
in definition order. `prepare`'s numbers are the real ones. Expect `stats` to be larger
than 32 and `compbio_mechanism` to stay very small.

### 2.2 Verify the leak guard by eye, once

```bash
grep -c "my_score\|stratum" eval/triage_runs/<stamp>/stats-01.md
```

**Must be 0.** The assertion in `prepare` already checks this and refuses to write —
but confirm it yourself the first time. If either field ever reaches the model, the eval
is not degraded, it is void.

Also open the file and read the top: you should see the charter path, the in-scope
exemplar block, the out-of-scope near-miss block, then the JSON abstracts each carrying
`band`, `threshold` and neighbour titles.

### 2.3 Dispatch

In a Claude Code session in this repo:

> Dispatch each batch file in `eval/triage_runs/<stamp>/` to the `triage` subagent, one
> invocation per batch. Write each reply's JSON lines verbatim to
> `eval/triage_runs/<stamp>/out/<batch>.jsonl`. No commentary, no edits to the JSON.

One invocation per batch, not per paper — same rule as `daily-ingest.md`.

### 2.4 Check coverage before collecting

```bash
python3 ingest/run_triage.py status
```

**Expect** every batch showing `ok` with counts matching. `part` means the agent dropped
papers, which `triage.md` forbids ("Never skip"). Re-dispatch that batch rather than
proceeding.

### 2.5 Collect

```bash
python3 ingest/run_triage.py collect
```

Validates hard: every ID present exactly once, scores are ints 0–5, thresholds forced
back to the banded values, `ambiguous` present, far-band ≥4 forced to `wildcard`.

- **Contract warnings** are repaired and counted — read them, they tell you where the
  agent is drifting from `triage.md`.
- **Structural errors** refuse to write. That is deliberate: missing predictions shrink
  the denominator of every metric silently. Re-dispatch the affected batch. `--force`
  exists, and if you use it, say so when you report the number.

### 2.6 Score

```bash
python3 ingest/eval_triage.py score
```

**This is the baseline.** Read against `WEEK-1-PLAN.md` §6: recall ≥0.90, precision
≥0.60, borderline agreement ≥0.70 within ±1, no systematic miss. Expect the borderline
row to be the worst — the handoff has said so from the start.

Then do the qualitative test, which matters more than any of the four numbers: read ten
`reason` strings and check whether you agree with eight **for the stated reason**, not
merely with the verdict.

---

## Phase 3 — measure the change

### 3.1 Promote pass 4

Only after you've read `charters/stats.pass4.md` §8 and overwritten anything in §2/§3
you would not have written yourself.

```bash
mv charters/stats.pass4.md charters/stats.md
```

The path stays `charters/stats.md`, so nothing downstream needs touching.

### 3.2 Re-run and compare

```bash
python3 ingest/run_triage.py prepare
# dispatch as in 2.3, then:
python3 ingest/run_triage.py collect
python3 ingest/eval_triage.py score
python3 ingest/eval_triage.py diff
```

`diff` compares the last two runs and will tell you what your six rulings actually did.
Watch for its own warning: *"A charter edit that fixes some and breaks others is usually
a narrowing, not an improvement. Check F-beta, not the miss count."*

### 3.3 Check the pre-registration

`PASS-4-DRAFTS.md` §5 recorded predictions before any of this ran. Two apply here:

- **A4 reading 2** should produce false negatives that are sparse and non-systematic. If
  they cluster in one subfield — most likely biostatistics or psychometrics, where method
  and setting are hardest to separate — reading 2 is cutting into scope rather than
  trimming applications, and §3's first bullet should revert toward reading 1.
- **The null prediction:** `probability` should be **unchanged** between the two runs,
  because its charter did not move. If it improves, something leaked that these documents
  do not account for, and that is worth finding before trusting anything else.

---

## If something breaks

| Symptom | Cause | Fix |
|---|---|---|
| `no exemplars for <domain>` | Tier 0 never applied for that domain | `canon_tier.py apply` — but all four had exemplars at last check (102 total) |
| `canon has no papers for domain X` | Index built before a rename | `canon_index.py build` — verified clean as of this run |
| `N papers have no inferable domain` | Their categories match no `SETS` entry | Widen `SETS`, or remove those rows deliberately and note why. Do not skip them silently |
| Every band comes out `far` | Domain mask matched nothing | Rebuild the index; check the domain names line up |
| `collect` refuses to write | Missing or duplicated predictions | Re-dispatch the named batch |
