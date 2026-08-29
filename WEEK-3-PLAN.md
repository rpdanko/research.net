# Week 3 plan — to-do list

> **SUPERSEDED 2026-08-28 by `PROJECT-STATUS.md`.** Most of what follows was worked
> through in the session that produced it; the live to-do is there. This file is kept
> as the record of what Week 3 opened with and what the rulings were, not as a task list.

Derived from `WEEK-3-HANDOFF.md` and `OPEN-QUESTIONS.md`, then checked against
the actual repo state today (2026-08-28) rather than trusted forward. Several
carryover items turned out to be **already done** — those are listed in §0 and
struck, so they stop being rediscovered every session. `OPEN-QUESTIONS.md` is
now the stalest document in the repo; §1.1 is the first item below for that
reason.

Order is as requested: everything that should already have been addressed
comes first (§0–§2), then Week 3's actual program (§3).

**Environment.** The Linux sandbox does not start on the assistant side.
Everything marked **[shell]** runs on your machine. Every script runs with
`python3`, not `python`.

---

## §0 — Carryover items that are already closed (verified, no action)

Checked directly against the files, not against any document's claim about
them. Nothing here needs doing; it is here so the next handoff can drop it.

- ~~`run_triage.py` missing (OQ 0.1)~~ — exists at `ingest/run_triage.py`.
- ~~`apply_triage.py` missing (OQ 0.2)~~ — exists, along with `pdf_extract.py`
  and `rebuild_index.py`.
- ~~`kb/` contains no cards (OQ 0.2)~~ — 28 cards on disk: `stats` 3,
  `probability` 10, `compbio_methods` 9, `compbio_mechanism` 6. Matches the
  handoff's count exactly.
- ~~Label strata unnormalized (OQ 1.2)~~ — all 180 rows in
  `eval/labels.dev.jsonl` now carry `expect_in` / `expect_out` / `borderline`.
  No `In`, no `Borderline`, no `borderlinne`, no `pit`. The
  case-sensitive `startswith("border")` blind spot is gone.
- ~~`domain` null throughout the label set (OQ 1.2)~~ — zero nulls remain; all
  180 rows carry a domain.
- ~~`stats.pass4.md` awaiting promotion (OQ 2.1)~~ — no `.pass4.md` files
  remain in `charters/`; `charters/stats.md` is live.
- ~~Superseded files still on disk (OQ 3, WEEK-3-HANDOFF §3)~~ — all gone:
  `charters/compbio.md`, `charters/compbio_genomics.md`,
  `.claude/agents/compbio-curator.md`,
  `.claude/agents/compbio-genomics-curator.md`,
  `canon/vetting-compbio_genomics.md`. **This item can be deleted from
  `OPEN-QUESTIONS.md` §3 and from the handoff.**
- ~~Stray empty file `research-net/To` (OQ 3)~~ — gone.
- ~~`vetting-stats.md` line 334 mark/reason mixup (OQ 3)~~ — fixed; line 334
  reads `mark: s` with a full `reason:` on 335.
- ~~`vetting-compbio_methods.md` line 148 unmarked (OQ 3)~~ — `W4408399347`
  now carries `mark: S`.

---

## §1 — Overdue, still open, cheap (do these first)

### 1.1 Prune `OPEN-QUESTIONS.md` — **DONE 2026-08-28**

It had become a decision register that no longer described the decisions:
Tier 0 entirely resolved, 1.1 and 1.4 marked decided but still carrying their
full "as it stood when this was open" bodies, five of six Tier 3 bullets done.

Now pruned. Resolved items are one-liners under a new §Closed; decided items
keep the decision and its live consequence, not the deliberation. Section
numbers were deliberately **not** renumbered — this plan and
`WEEK-3-HANDOFF.md` both cite §1.3/§1.5/§1.6/§2.2/§2.3 by number. Pre-prune
copy at `OPEN-QUESTIONS.md.pre-prune.bak` (no git in this repo, so the backup
is the only history).

### 1.2 `compbio_mechanism`'s counts (OQ 1.5) — label side done, sqlite side **[shell]**

**Done:** all four per-domain counts re-derived from the now-backfilled
`domain` field in `eval/labels.dev.jsonl`. Every number in §1.5's old table
was wrong — it predated the routing fix and counted by primary category:

| Domain | Rows | Admits (`my_score ≥4`) | Was |
|---|---|---|---|
| `compbio_methods` | 101 | 26 | ~127 / 35 |
| `stats` | 40 | 26 | 32 / 22 |
| `probability` | 29 | 17 | 16 / 11 |
| `compbio_mechanism` | 10 | 3 | 5 / 1 |

Two findings worth carrying into §3: **`stats` is now the strongest usable
eval target**, not the marginal one — it roughly doubled and is the only
domain both large enough and uncontaminated by §1.4's dev-set problem. And
`compbio_mechanism` is still unusable for tuning, but for a new reason: 10
rows, only 3 admits.

**Still open [shell]** — the "8 admitted" figure quoted elsewhere for
`compbio_mechanism` matches neither number above:

```bash
sqlite3 ingest/papers.sqlite \
  "select status, count(*) from papers where domain='compbio_mechanism' group by status"
```

Settle it, then decide whether the targeted `q-bio.*` labelling sitting is
needed at all. It may show the draw is unnecessary.

### 1.3 Fix `sample()`'s output ordering (OQ 1.6) — **DONE 2026-08-28**

`random.shuffle(picks)` now runs after the quota loop in `sample()`, before
`new_recs` is built, with a comment recording the reasoning.

The loop already shuffled *within* each band, which randomized which rows got
drawn — but it extended `picks` stratum by stratum, so the written order was
an `expect_in` block, then `expect_out`, then `borderline`. That is what
produced rows 105–133 (24 admits of 29) and 134–147 (fourteen consecutive
rejections).

Confirmed it is the order that matters: `label()` iterates the file top to
bottom, so file order *is* scoring order. `--append` is unaffected — existing
rows are written ahead of the new draw and never move — and nothing downstream
groups by stratum position (`score_run()` buckets on the field).

The sampler is now safe to draw the §4 fresh set with.

### 1.4 The domain-map coverage gap (OQ Tier 3) — **CLOSED 2026-08-28: not a gap**

Investigated and dismissed. The original bullet was wrong three ways, and my
own restatement of it above inherited the first error — recorded here so the
correction sticks:

- **Wrong file.** `canon/domain_map.yaml` holds OpenAlex topic IDs (`T13500`,
  `T11871`, …) for slicing the canon. It contains no arXiv categories at all,
  so "contains no `math.NA` entry" was never a meaningful claim about it.
  Harvest coverage lives in `arxiv_pull.py`'s `SETS`.
- **Wrong test.** `harvest_oai()` filters on `wanted.intersection(cats)` —
  **any** category on the paper, not the primary one. All seven papers are
  harvested today via cross-lists (`math.PR`, `math.ST`, `stat.ME`, `cs.LG`).
  Separately, `math.NA` was since added to `compbio_methods`' set explicitly,
  with a comment giving precisely the "no route in at all" reasoning.
- **Wrong count.** Six of seven scored ≥4, not all seven — line 36
  (`math.NA cs.LG cs.NA`) scored 2.

Nothing was ever unreachable, so there is nothing to decide.

**One real thing did surface**, logged to OQ Tier 3 rather than actioned:
`_infer_domain()` takes the *first* `SETS` domain whose categories intersect,
and `probability` precedes `compbio_methods`. Line 117
(`math.NA cs.LG cs.NA math.AP math.PR`) therefore routes to `probability` on
its `math.PR` cross-list despite `math.NA`/`cs.LG` pointing elsewhere. Harmless
here — it scored 5, probability is defensible — but precedence is doing real
work on numerical papers and nobody has checked it lands right in general.

### 1.5 Numbering hazard — fix when convenient

This plan's §1.4 and `OPEN-QUESTIONS.md` §1.4 are **different items** (the
coverage gap vs. the `LABEL-USE-PROTOCOL` adoption), and this plan cites OQ
sections as "OQ 1.x" throughout. That collision has already caused one
mix-up. When touching either file, prefer "OQ §1.4" / "plan §1.4" explicitly
over a bare "§1.4".

---

## §2 — Overdue, still open, larger (schedule, don't squeeze in)

### 2.1 `calibrate()` re-run + `EVAL-01-FINDINGS.md` — **doc corrected 2026-08-28; re-run still [shell]**

**Done: the document is corrected.** And it was wrong in a bigger way than
this plan assumed. It analyses run `20260827-144416`, but **two later score
runs existed and it never mentions either**:

| Run | recall | precision | F-beta(3) | misses |
|---|---|---|---|---|
| `144416` (what the doc reports) | 0.803 | 0.570 | 0.771 | 15 |
| `201651` | 0.915 | 0.607 | 0.871 | 6 |
| `214656` (latest) | **0.901** | **0.688** | **0.874** | 7 |
| latest, corrected for the `2509.18530` flip | **0.903** | **0.699** | **0.877** | 7 |

Both metrics moved from below target to at or above it (0.90 / 0.60). The §4
drafts were applied and worked; the doc's "nothing here is applied" was false.
It now carries a status block with the run history, the flip arithmetic, and a
note that its per-stratum cells are unreproducible — strata were rewritten by
the §1.2 hygiene pass, and they no longer reconcile with the overall within±1.

**A new open question fell out of it — logged as OQ §1.7.** The doc's own §6
pre-registered: precision "should stay near 0.57. If it rises without a
`triage.md` scoring change, find out why before believing it." It rose 0.12,
and nobody found out why. Either an unrecorded scoring change landed, or §2's
round-up diagnosis — which shaped the pass-4 charters — is wrong. Don't bank
the 0.688 until that resolves.

Also settled while there: §6's routing prediction (`compbio_mechanism` should
receive 10–14 papers, not 2) **passed** at 10.

**Still open [shell]:** the per-domain `calibrate()` re-run itself. Every
figure above is pooled across all four domains, and the NEAR/FAR group means
(0.57 vs 0.59 — inverted) were computed against the pooled 8,320-paper canon
rather than the ~2,080 of one domain, the comparison most likely to wash out
separation. Note the live band constants in `canon_index.py` are
`NEAR, FAR = 0.62, 0.38`; the 0.57/0.59 pair are measured group means, not
thresholds — don't confuse them. If separation is still inverted per-domain,
treat that as a signal about the canon or the domain map, not a reason to ship
a noisy band.

### 2.2 Rewrite-prep — `compbio_mechanism` **DONE 2026-08-28**; two remain

`charters/compbio_mechanism.rewrite-prep.md`, in `stats.rewrite-prep.md`'s
shape. 150 papers, ~128 strikes, ~22 keeps. Four `RULING:` lines await you;
the two substantial ones:

- **§8's popgen/phylogenetics case rests on an unverified claim.** It asserts
  the theory papers rejected on evolutionary-biology grounds are "small" in
  number. Of the nine strikes in that cluster, exactly one names tooling; the
  other eight are bare field rejections that cannot tell theory from software.
  That sentence carries the charter's largest scope decision, in the domain
  §1.5 shows has the least label evidence. Either read the eight titles or
  soften the claim.
- **The domain is bounded on both sides; §3 encodes neither.** Six strikes
  reject work above the molecular level (epidemiology, oceanography,
  marsupials, "higher-order organisms"), two below it (force fields, atomic
  modelling). Nothing in §3 stops either today, and both would pass §2's
  stochastic-and-dynamical-models bullet.

Also flagged: §8's "nearly every sequencing strike was a software
announcement" is overstated — the Human Genome and 1000 Genomes papers are
resource releases, caught by a different §3 bullet. And ~10 strike reasons
("Not relevant", "Really interesting but not relevant to what I do") are
eligible for the negative-exemplar block while teaching an agent nothing.

**Still open:** `probability.md` and `compbio_methods.md`.

### 2.2b Prompt-pipeline defect found while doing the above — worth a look

`compbio_mechanism`'s negative-exemplar block in
`eval/triage_runs/20260827-203053/compbio_mechanism-01.md` has six entries.
**Three carry strike reasons written in other domains' worksheets** —
"Too rudimentary to be helpful" and "Specific to drug development" from
`vetting-stats.md`, "Included in the genomics canon" from
`vetting-compbio_methods.md`. Two more are the same STROBE-MR paper twice,
leaving RAxML as the only distinct negative drawn from this domain's own
judgments. The largest strike genre here — package papers, ~47 of 128 — was
not represented at all.

Week 2's bucketed round-robin fix should address the selection half. It does
not obviously address reason *provenance*: `exemplars()` picks records by the
domain's canon slice while `strike_reason` comes from whichever worksheet
marked the record. Check a freshly rendered prompt; if it persists it is a
`canon_index.py` fix.

### 2.3 The three deferred-by-floor re-reads (OQ 2.3)

Small, individually cheap, easy to lose:

- **AI-for-science flag** (`PASS-4-DRAFTS.md` §1.3) — n=4, below R1's floor
  of 5. Re-examine against a fresh set, not the dev set.
- **Line 80** — cytoskeletal statistical-mechanical framework, `q-bio.CB/MN/SC`,
  scored 2 despite sitting in the centre of `compbio_mechanism.md` §2. n=1.
- **Line 109** — *"Evaluating RL Explainability Methods…"*, stratum `in`,
  score 2. The only internal contradiction in 180 rows; likely a keying slip.
  Confirm or correct it.

Add to this list: **`2307.13826`** (probability — expository monograph, real
proofs, no new theorems) was left in against `probability.md` §3's
"reviews… without a result" exclusion. Seen, not missed, but flag it if the
pattern recurs.

---

## §3 — Week 3's actual program: `card_eval.py`

Confirmed missing from `ingest/` today. This is the thing the project has
never measured, and `recode.py`'s `cards` judgment source is blocked on it
existing.

### 3.1 Write `ingest/card_eval.py`

Mirror `eval_triage.py`'s real file shape — `_infer_domain`, `sample`,
`label`, the `_save`/`_resolve` pair, a `score_run` equivalent, `diff`,
`main()`/argparse. The assistant can write it without shell access, the same
way `apply_triage.py`, `pdf_extract.py` and `rebuild_index.py` were written
last session, and hand it over to run.

```bash
python3 ingest/card_eval.py sample --n 20 --domain stats   # pull cards for hand-checking
python3 ingest/card_eval.py label                          # your judgment, per field
python3 ingest/card_eval.py score                          # curator vs. you
python3 ingest/card_eval.py diff                           # did the last schema/prompt edit help
```

**Score on field equivalence, not exact string match.** A curator writing
"optimal transport" for a paper that says "Sinkhorn divergence" is correct.
`README.md`'s "Card accuracy" section cites the LLM-NERRE manual-scoring table
for why: exact match badly undercounts correct-but-reworded extraction, and
`mathematical_objects` is the field it bites hardest.

**Carry §1.3's lesson across.** Whatever sampling `card_eval.py` does, shuffle
the final output before writing — don't reproduce `eval_triage.py`'s streaking
bug in a second tool.

### 3.2 Run it: `sample` → `label` → `score`

Against the current 28-card KB. Per-domain rather than pooled if 20 from one
domain is more useful — note `stats` only has 3 cards, so a `--domain stats`
draw is capped at 3 and `probability` (10) or `compbio_methods` (9) are the
only domains that can carry a real per-domain number today.

**Note the inversion this creates.** §1.2 makes `stats` the best *charter*
eval target — largest uncontaminated label set — while it is simultaneously
the worst *card* eval target, at 3 cards. The two measurements want different
domains. Don't let a `--domain stats` habit carry over from triage work; pool
across all 28, or draw from `probability`.

Output: **the first curator-vs-you accuracy number this project has ever had.**

### 3.3 Decide, with that number in hand

Whether the card schema or the curator prompts need revising — before curating
further into the backlogs. Not another round of manual spot-checks.

If a field comes back weak and *stays* weak after one schema/prompt revision,
`README.md` names `mathematical_objects` as the strongest fine-tuning
candidate. Not a Week 3 decision, but on the table if prompting plateaus.

---

## §4 — Deliberately deferred (don't start these in Week 3)

Listed so they aren't rediscovered, not so they get done.

- **`compbio_methods`: 26 admitted papers still queued, all pre-clause
  admissions.** More DiffGRM-shaped papers are plausible in there. Worth a
  pass *before* pulling anything new from that pool — but after §3.3.
- **`probability`: 8 admitted papers still queued** (18 admitted, 10 curated).
- **The 5,275-row untriaged harvest from 2026-08-24** in `papers.sqlite`;
  ~1,049 rows infer to `probability` alone. Model-call spend should be a
  deliberate decision, not a reflex — same reasoning as `WEEK-2-PLAN.md`'s
  Step-7 writeup.
- **Fresh held-out eval set for `compbio_methods` (OQ 1.6).** No longer
  hypothetical: its charter was partly drafted from the 180 dev rows, so any
  recall/precision claim against those same rows is circular. Needs §1.3's
  fix first. `stats` is unaffected — zero label-derived changes — and remains
  a valid target as-is.
- **`math-scout` has never run**, so the base `kb/concordance.jsonl` is still
  absent and `concordance.merged.jsonl`'s 3 rows all come from
  `concordance_user.jsonl`. Not blocking; worth knowing before the next
  `bridge-finder` run.
- **Expectation for the next `bridge-finder` run:** none of the three planted
  concordance objects (`belief propagation`, `Dirichlet process`, `Kingman's
  coalescent`) appear by name or alias anywhere in the 28 cards. Expect it to
  find structure on its own, as it did with `b-2608-001`/`002` — not the
  planted bridges.

---

## Done means

1. `OPEN-QUESTIONS.md` describes the project as it is today, not as it was on
   Day 5.
2. `compbio_mechanism`'s labelled/admitted counts are derived, not quoted.
3. `random.shuffle(picks)` is in `eval_triage.py` and the domain-map gap has a
   recorded decision either way.
4. `ingest/card_eval.py` exists, runs, and has produced a real number.
5. That number has been used to make one decision about the schema or the
   curator prompts — including the decision to change nothing.
