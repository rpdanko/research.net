# Handoff — end of Day 4, into Day 5

State at the end of the session that split the compbio domain, rewrote the charters, and built the canon index. Read `HANDOFF.md` for the standing project state; this file covers what moved, what you owe, and how Day 5 should run.

---

## 1. The thing you owe before Day 5: rewrite the charters yourself

**All four charters are still agent-written. That is not the intended end state and Day 5 is measuring them.**

`README.md` §"The two files that must be in your handwriting" is explicit that `charters/*.md` encode judgment no agent can supply, and `WEEK-1-PLAN.md` Day 4 says the model's version "is a first draft that has read 150 papers; the judgment has to be yours." Three passes have now happened and every one was mine:

- **Pass 1** — generic scaffolding, written before any canon existed.
- **Pass 2** — derived from your vetting marks. Over-fitted the canon badly; described the 150 papers you read rather than specifying the domain.
- **Pass 3** — corrected the over-fit, restored scope dropped by omission, converted instance-lists to criteria. Each charter's §8 records what changed.

Pass 3 is a better draft. It is still a draft, and it is still mine. Everything downstream inherits these files, and the Day 5 labelled set exists specifically to measure them — so if the charters are not yours before you label, you will be measuring how well triage reproduces my reading of your strike reasons, which is one inference removed from the thing you actually want measured.

**Minimum viable version of this obligation, if time is short:** read each charter's §2 and §3 and rewrite in your own words anything you would not have written. You do not need to restructure the files. The sections that most need your hand are the ones where I inferred a rule from strike reasons rather than being told it.

### Four decisions I did not make for you

| Decision | Where | Status |
|---|---|---|
| Psychology / political-science field bans | `stats.md` §8 | I softened your standing rules to content criteria. Three reasons given; one of them is that the coauthor rule contradicts `triage.md`'s "do not infer authorship." Reinstate the hard bans if you disagree. |
| Popgen / phylogenetics theory | `compbio_mechanism.md` §8 (formerly `compbio_genomics.md`) | Flagged `[popgen-phylo-theory]`, `q-bio.PE` held out. A flag nobody rules on is a slower rejection — decide before Day 5, because it changes what the labelled set should contain. **Still open** — the rename below is done, this is not. |
| `compbio_methods` category firehose | `compbio_methods.md` §8 | `cs.LG` + `stat.ML` + `math.OC` is several hundred submissions a day against a cap of 10. Three options given. **This one blocks Day 5** — see §3 below. |
| ~~Rename `compbio_genomics`~~ | `compbio_mechanism.md` §8 | **Done.** Renamed to `compbio_mechanism`. Propagated through `domain_map.yaml`, `card_schema.json`, `arxiv_pull.py`, both curator agents, `daily-ingest.md`, and the remaining docs/charters that referenced the old name. |

---

## 2. What else moved this session

**Domain split.** `compbio` → `compbio_methods` + `compbio_genomics`, propagated through `domain_map.yaml`, `card_schema.json`, `arxiv_pull.py` (`SETS`), `daily-ingest.md`, `math-scout.md`'s `kb/` path list, `README.md`, `HANDOFF.md`. Two new curator agents; the old `compbio-curator.md` and `charters/compbio.md` marked superseded rather than deleted. (`compbio_genomics` later renamed to `compbio_mechanism` — see the table above.)

**Canon complete.** ~~8,320 records, 2,080 per domain, 26 years × 80/year, no gaps.~~ **Corrected:** 8,102 records. 2,080 per domain × 4 = 8,320 was the *target*; the harvest fell 218 short and only `compbio_mechanism` filled it — `compbio_methods` 2,077, `stats` 2,010, `probability` **1,935**. Probability's shortfall is diffuse rather than era-skewed (2000s −65, 2010s −59, 2020s −21), so the slice is thin but not biased toward recent work. Worth reading alongside `probability.md` §8, which already argues the canon under-represents that domain on topic mix — this is a second, independent 7% shortfall on top of it. Vetting figures are all correct as stated: 111 kept, 102 exemplars, 382 struck with reasons. `canon/index.npz` built, verified post-rename (its `domains` array carries `compbio_mechanism`, so per-domain banding is scoped correctly).

**Ambiguous tier.** New §5 in each charter naming domain-specific blind-spot patterns with bracketed tags; `triage.md` emits `"ambiguous": true` plus the tag; `coalition_audit.py` §6 counts them and warns when one tag exceeds 40% of flags. Dark until `apply_triage.py` exists.

**Two loose ends worth two minutes.** `vetting-stats.md` line 334 has `mark: Surgical guidelines` — struck correctly (leading "s") but the reason landed in the mark field and was lost. `vetting-compbio_methods.md` line 148 (`W4408399347`) was never marked, so it sits in Tier 1 by default rather than by review.

**Concordance draft.** `kb/concordance_user.draft.jsonl` — three entries (belief propagation, Dirichlet process, Kingman's coalescent), deliberately **not** at the live path because `papers` is empty on all three and the spec's bar is "could you write the object down in both papers." Promote with `mv` once cards exist.

---

## 3. Day 5 — build the labelled eval set

Goal per `WEEK-1-PLAN.md`: 150 papers from a recent arXiv window, stratified into expect-in / expect-out / genuinely-borderline, **scored by you before triage sees them even once**.

### 3.1 Prerequisite: `papers.sqlite` does not exist yet

`eval_triage.py sample` reads from the arXiv database, and nothing has ever written it. Before anything else:

```bash
python ingest/arxiv_pull.py --since 2026-08-09      # ~2 weeks; --since takes a date or "yesterday"
```

`--since` accepts a literal date. You want a window wide enough to yield several hundred papers across four domains — `sample` fetches `n*4` rows and errors out if the DB holds fewer than `n`. Respect the 3.1s rate limit already coded in; do not parallelise.

**Decide the `compbio_methods` category question first** (§1 table). The harvest reads `SETS` in `arxiv_pull.py`, so if `cs.LG` and `stat.ML` stay in, a two-week window pulls several thousand `compbio_methods` papers and that domain will swamp the sample. Narrowing the categories before harvesting is much cheaper than filtering afterwards.

### 3.2 Fixed: `sample` used to not actually stratify

**Fixed.** `sample()` in `ingest/eval_triage.py` now takes fix #1 below — pre-score against the canon index, band by `near`/`mid`/`far`, assign strata from the band. Kept the original bug report here so the reasoning stays visible.

The original code drew rows at random and then assigned strata **by index position**:

```python
picked = random.sample(rows, n)
for i, (...) in enumerate(picked):
    stratum = ("expect_in" if i < per else "expect_out" if i < 2*per else "borderline")
```

The first 50 were labelled `expect_in` for no reason other than being first. The docstring said "Stratified sample" and the printed note said "your `expect_in` guesses will be wrong for maybe a fifth of them" — but they were not guesses, they were arbitrary.

Consequence: the borderline stratum, which the plan calls "the only one that will teach you anything," was not borderline. It was a random third of a random draw — and a random arXiv draw is overwhelmingly out-of-scope for any given domain, so a 150-paper sample would have been 150 easy rejections and taught almost nothing.

**Two ways to fix it were on the table; the first is what's implemented:**

1. **Pre-score with the canon index and pick the middle.** ✅ Implemented. `sample()` pulls a `n*4` pool, scores every candidate against the canon with `canon_index.py`'s embedding index directly (batched, not a per-paper `score()` call — reloading the model per candidate would make a 600-paper pool impractically slow), and buckets by the same `near`/`mid`/`far` bands triage itself uses. `expect_in` comes from `near`, `expect_out` from `far`, `borderline` from `mid`. If a band comes up short of its quota, `sample` warns rather than padding from another band — padding would just reintroduce the original bug under a different name.
2. **Over-sample and re-assign as you go.** Not implemented, but still available as a manual fallback: `label` prompts for a stratum on every paper and overwrites whatever `sample` assigned, so if the canon-based bands still look wrong for a given paper, retyping the stratum during labelling is always the final word.

Either way: **the stratum you type during labelling is the one that counts.** `score` reports per-stratum agreement and the borderline row is the target number (≥0.70).

### 3.3 Labelling

```bash
python ingest/eval_triage.py sample --n 150      # or 300, per above
python ingest/eval_triage.py label
```

Non-negotiable, and the script says so: **score every paper yourself before running triage on them even once.** Once you have seen a machine score you cannot unsee it and your labels stop being an independent standard. There is no undo for this.

Use the same 0–5 scale as `triage.md`. Hold the line that 3 is a rejection with a note, not a hedge — if you find yourself giving 3s to avoid deciding, the labelled set loses exactly the resolution it exists to provide.

`label` saves on `q`, so this can be done in sittings. Do the domain you know least well first, while attention is fresh — same advice as Day 3, same reason.

### 3.4 A sizing problem the plan predates

`WEEK-1-PLAN.md` was written for three domains. There are now four, and `sample` does not filter by domain — so 150 papers is ~37 per domain, and the borderline stratum within a domain is ~12. That is too thin to tune a single charter on.

Options, none free:

- **Accept aggregate resolution.** The eval measures triage overall, not each charter. Fine for a first pass; weak for the per-charter tuning Days 6–7 are supposed to do.
- **150 per domain.** Statistically right, 600 abstracts of your reading time, will not happen this week.
- **Two domains now, two later.** Label 150 across `stats` and `compbio_mechanism` (formerly `compbio_genomics`) only — the two that changed most in pass 3 and where my inference from your strike reasons is thinnest. Defer the others to a second labelled set. This is what I would do.

### 3.5 Optional, once ≥30 are labelled

```bash
python ingest/eval_triage.py calibrate    # run from repo root; needs canon_index importable
```

Suggests `NEAR`/`FAR` from your labels instead of the shipped 0.62/0.38 guesses. If it reports that the distributions overlap almost completely, **do not wire the band into the threshold** — that is the script telling you similarity is not separating your classes, and the honest response is to fix the canon or the domain map rather than to ship a band that adds noise.

---

## 4. What blocks Day 6

**`run_triage.py` does not exist.** `eval_triage.py score` reads `eval/predictions.jsonl` and nothing writes it. You need a runner that pulls the labelled set, attaches each paper's similarity band from `canon_index.py score`, dispatches the `triage` subagent in batches of 25 with the charter path and exemplar block, and collects the JSON lines. `HANDOFF.md` §6 estimates ~60 lines; that is about right.

Write it on Day 6, not now. It is the only thing between a labelled set and a measured charter.

---

## 5. Done means

From `WEEK-1-PLAN.md` §6, unchanged:

- Recall ≥ 0.90 on labelled in-scope papers. Below this the charter is too narrow — read the misses before touching anything.
- Precision ≥ 0.60. Much higher probably means recall is being bought away.
- Borderline-stratum agreement ≥ 0.70 within ±1. The number that actually matters and the one that will be worst.
- No systematic miss — false negatives should look random, not like a subfield you forgot to describe.

And the qualitative one, which is the real test: you should be able to read ten triage `reason` strings and agree with eight **for the stated reason**, not merely with the verdict.

---

## 6. Session handoff — mid-labelling state, resume here

Written at the end of a chat that picked up Day 5 in progress. Read this before doing anything else if you're continuing this in a new chat.

### 6.1 What's settled since the top of this file

- **`compbio_genomics` → `compbio_mechanism`.** Renamed everywhere — charter, `domain_map.yaml`, `card_schema.json`, `arxiv_pull.py`, both curator agents, `daily-ingest.md`, remaining docs. §1's table above is stale on this point; treat it as done.
- **Popgen/phylogenetics theory: admitted.** `q-bio.PE` restored in the charter and in `arxiv_pull.py`'s `SETS`, the `[popgen-phylo-theory]` flag kept as an ongoing visibility check rather than an open question, tooling still excluded exactly as before. `charters/compbio_mechanism.md` §§2/5/6/8 all carry this. §1's table above is stale on this point too.
- **`compbio_methods` category firehose: still open.** Not touched this session. Still blocks a full-scale Day 5 run — see §3 above.

### 6.2 Labelling status

`eval/labels.jsonl` has **180 rows, all fully labelled** (no `my_score: null` remaining) — the original 109 plus a `--append` run of ~71 more. By `calibrate`'s own count: 76 scored ≥4 ("in-scope"), 104 scored <4 ("out-of-scope").

### 6.3 Two more bugs found this session, one needs a one-time script run before you trust `calibrate` again

**`sample` not stratifying (§3.2 above): already fixed, nothing further needed.**

**`papers.sqlite`'s `domain` column is null for every harvested row, and it was silently corrupting the canon-similarity scoring `sample`/`calibrate` depend on.** Root cause: `arxiv_pull.py`'s harvest never sets `domain` — that's `apply_triage.py`'s job by design (§4: it doesn't exist yet), so domain assignment was always meant to happen post-triage, not at harvest. But `sample()`'s near/mid/far banding and `calibrate()`'s `NEAR`/`FAR` suggestion both read the stored `domain` column to scope the canon comparison to one domain's ~2,000 papers — with it null, both were silently comparing every candidate against the **whole pooled canon** (~8,300 papers across all four domains) instead. That dilutes exactly the separation `calibrate` exists to measure.

Fixed in code: `eval_triage.py` now has `_infer_domain(categories)`, which rebuilds the domain from a row's stored `categories` using `arxiv_pull.py`'s own `SETS` mapping. `sample()` and `calibrate()` both use it as a fallback whenever the stored `domain` is empty. `calibrate()` infers fresh every run, so it's fixed without touching the data file — **but the calibration numbers reported earlier in this session (NEAR=0.57 / FAR=0.59, "distributions overlap almost completely") were computed pre-fix, against the undifferentiated canon. Re-run `calibrate` before drawing any further conclusion from that result** — the fix should tighten the separation, possibly enough to clear the warning. If it's still inverted after this, that's a much cleaner signal about the canon/domain map than what you had before, and worth taking seriously.

**`label`'s stratum prompt says `[in/out/borderline]`, but every other place in the codebase uses `expect_in`/`expect_out`/`borderline`.** All 180 rows were hand-typed against that mismatched prompt, so the stored `stratum` values are currently a mix of `"in"`, `"out"`, `"In"`, `"Borderline"`, a typo (`"borderlinne"`), and one unrecognizable value, `"pit"`, on `2608.07528` ("The Knowing-Saying Gap: When Probes See Errors that Confidence Misses"). This matters beyond cosmetics: `score_run()`'s borderline-agreement check is `st.startswith("border")`, case-sensitive — so the capitalized `"Borderline"` rows are currently invisible to that check. Fixed going forward: `label()` now normalizes what you type (`_normalize_stratum`, case-insensitive, prefix-matched). The 180 existing rows need a one-time cleanup pass:

```bash
python ingest/fixup_labels_stratum_domain.py
```

Backs up to `eval/labels.jsonl.bak` first, then backfills `domain` from `categories` and normalizes `stratum` in place. It will print exactly one unresolved row — `2608.07528`, currently `stratum: "pit"` — because it won't guess at a typo it can't confidently place. Open `eval/labels.jsonl`, find that line, and set `stratum` to `expect_in`, `expect_out`, or `borderline` based on your own memory of that paper (or re-read the abstract; it's a probing/LLM-interpretability paper, `my_score: 2`) before running `score` later.

### 6.4 Resume here

```bash
python ingest/fixup_labels_stratum_domain.py     # one-time; see 6.3
# then hand-fix the one flagged row's stratum in eval/labels.jsonl
python ingest/eval_triage.py calibrate           # re-run now that domain scoping is fixed
```

After that, pick back up at §3.3/§3.4 above: keep labelling (`sample --n <k> --append`, then `label`) toward whatever target you land on given the four-domain sizing problem, and remember §4's `run_triage.py` still doesn't exist — that, not the labelled-set size, is the actual blocker before Day 6's scoring can run at all.
