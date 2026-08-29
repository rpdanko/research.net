# Pass 4 — proposed charter drafts, with overfitting audit

Written under `LABEL-USE-PROTOCOL.md`. Nothing here is in effect. No live charter has been
edited. R8's rename has **not** happened, so `eval/labels.jsonl` is still at the path
`eval_triage.py score` reads by default — if you adopt any of this, that rename comes first.

---

## 0. Summary: the protocol licensed less than you asked for

| Charter | Label rows | Proposed text changes | Why |
|---|---|---|---|
| `compbio_methods` | ~127 | **2** (one §3 exclusion, one §2 clause) | Only domain where evidence clears R7's n≥10 with room to spare. |
| `stats` | 32 | **0 from labels** | The 10 rejections all fall under §3's existing bullets. Labels *confirm* the charter; they add nothing. Your six §A rulings are still yours — drafted options in §3 below. |
| `probability` | 16 | **0** | 11 admits, all core probability theory already in §2. 5 rejections — R1's absolute floor, R7's question threshold not met. |
| `compbio_mechanism` | **5** | **0 — refused outright** | Fails R7 entirely. The charter with the most speculative decision in it (popgen admitted against your stated preference) is the one the labels cannot speak to at all. |

**Read that last row as the protocol working, not as a gap.** Five papers cannot license a
change to a charter, and the fact that this is the charter I'd most like evidence for is
exactly why the floor has to be mechanical rather than judged case by case.

One further finding is a **code decision, not charter text**, and it is the most consequential
thing in this file — §2.

---

## 1. `compbio_methods` — proposed insertions

### 1.1 New §3 exclusion — applied ML systems work

> - **Applied machine-learning systems work.** Benchmarks and benchmark suites, retrieval
>   and recommendation pipelines, agent frameworks, deployment and serving engineering,
>   fine-tuning recipes, adversarial-robustness demonstrations, and domain applications of
>   existing architectures. The contribution is a system that works or a number on a
>   leaderboard, not a property of a method. This is the largest single genre in `cs.LG`
>   and the charter was previously silent on it — §3's existing bullets were written for
>   metaheuristics and narrow engineering and do not obviously reach it.

**Evidence:** ~90 rejections in this bucket, overwhelmingly of this shape. Well clear of R7.

**Why this is silence-filling and not boundary-moving (R3):** §3 currently names benchmark-only
metaheuristics, narrow single-application engineering, software announcements, and reviews.
A paper titled *"AI4AI-Bench: Benchmarking LLM Agents in Algorithmic Design"* is caught by
none of those without stretching "narrow single-application engineering" past what it was
written to mean. The charter isn't drawing this boundary in the wrong place — it isn't
drawing it at all, and triage is currently improvising.

### 1.2 New §2 lead clause — the property, not the result

> **The unifying test across every criterion below: is the contribution an analyzable
> property of a method — convergence, complexity, coverage, identifiability, approximation
> quality, sample complexity — or is it an empirical result?** The property is what
> transfers and what a concordance entry can be written against. This holds regardless of
> the applied wrapper: a paper about language models, molecules, or images is in scope when
> the claim is a property, and out when the claim is performance.

**Evidence:** the 17 admitted papers whose categories are pure `cs.*` with no `math.*`,
`stat.*` or `q-bio.*` cross-list — conformal prediction under label shift, Koopman operators
for coupled systems, gradient-descent convergence via generalized Lipschitz structure,
length-squared sampling for PSD matrices, quantum matrix-multiplication complexity,
topological deep-learning diagnostics, generalized convexity for DNN optimization.

**Why this is R4-compliant (labels adjudicate, don't originate):** this is not a new rule.
It is `stats.md` §2's opening criterion — "estimators and tests with analyzable properties" —
restated for a literature the OpenAlex canon did not contain. The labels chose between two
pre-existing readings of how far that principle extends; they did not invent it. If it read
as a rule true only of this sample, it would come out under R4.

### 1.3 Refused: an AI-for-science flag

Lines 86 and 108 (research-problem discovery with local LMs; LLM-based equation discovery)
scored 4, while 17 and 46 (reviews of automated discovery and DL drug-target prediction)
scored 2 and 3. That looks like a coherent contribution-vs-review boundary in a genre worth
flagging in §5.

**n = 4. Below R1's floor of 5. Refused.** Noted here so it can be re-examined against the
fresh set rather than quietly acted on.

---

## 2. The firehose decision — `arxiv_pull.py` `SETS`, not charter text

`compbio_methods.md` §8 offers three options and assumes narrowing is close to free because
"`cs.LG` and `stat.ML` are where general ML lives and most of it fails §1's routing test
anyway." The proportion is right — 28% admit rate in this bucket. **The absolute cost is not.**

| Option | Admits retained (of 76 total) | Cost |
|---|---|---|
| **1.** Narrow to `math.OC` + `cs.NE` | **11** | Drops 65 of your 76 admitted papers. `cs.NE` appears **zero times** in 180 labelled papers — it is contributing nothing but is assumed load-bearing in §8. |
| **2.** Require `cs.LG`/`stat.ML` to cross-list to `math.OC` or `q-bio.*` | **4** of ~30 `cs.LG`/`stat.ML` admits | Essentially none of the 17 pure-`cs.LG` admits carry any such cross-list. Loosening the proxy to any `math.*`/`stat.*` cross-list still drops about half. |
| **3.** Ranked queue; cap becomes "top 10 by score today" | **76** | No recall cost. Requires `daily-ingest.md` to say the cap is a ranking cutoff, not throughput control. |

**Recommendation: option 3.** Invariant 9 prices recall over precision roughly 3:1, and
options 1 and 2 spend 85% and ~87% of your admissions respectively to buy throughput. The
firehose is a cost-and-attention problem, and options 1–2 solve it by discarding the papers
you actually want.

**Overfitting reading:** this is calibration against a category filter, explicitly permitted
by the protocol's applied table. It sets no charter text and no scoring rule. The residual
risk is that the labelled sample's category mix is not the steady-state arXiv mix — worth
re-checking once a fortnight of live harvest exists, but the `cs.NE`-is-empty finding is
robust regardless of mix.

---

## 3. `stats` — your six rulings, drafted both ways

No label-derived changes. These are the §A questions from `stats.rewrite-prep.md`, with text
drafted for each position so you can pick rather than compose. **Picking is the ruling; the
wording is yours to overwrite.**

**A1 Meta-analysis** *(canon: 3 strikes, "I don't do metaanalysis". Labels: 1 admit, n=1, no weight)*

- *Ban:* add to §3 — "Meta-analysis and evidence synthesis, including methodological work on them."
- *Split:* add to §2 — "Meta-analytic methodology where the contribution is an estimator or its properties"; to §3 — "Meta-analyses and evidence syntheses reporting pooled effects."
- *Flag:* add to §5 — "`[meta-analysis-methodology]` — a methods contribution inside the evidence-synthesis literature. Flag rather than deciding."

**A2 "Too rudimentary"** *(11 canon uses, currently expressed nowhere)*

- *Restore as depth criterion:* add to §7 — "Score 1–2 where the statistical content is below the level at which a methods paper is useful, even when the genre is right."
- *Leave dropped:* no change; §8's redundancy argument stands.

**A3 Psychology / political science** *(5 + 2 identical canon statements)*

- *Reinstate hard:* add to §3 — "Psychology and political-science papers, regardless of methodological content."
- *Keep as flag:* no change; `[applied-field-methodology]` stands.

**A4 "Specific to X"** *(~45 strikes — the reading that governs all of §3)*

- *Reading 1 (current):* no change. "Application with no transferable machinery"; the field is incidental.
- *Reading 2:* replace §3 bullet 1 with — "Work tied to a single setting, population, or dataset such that the method would not be recognisable outside it, whether or not it contains a methodological contribution."

**A5 Experimental design** — confirm §2 keeps it. I checked the five strikes; all are
reporting-guidance documents, so the restoration looks safe. Your call to confirm.

**A6 The PRISMA keep** — line 13 of `vetting-stats.md` keeps a PRISMA paper that §3 excludes
by name. Slip, or does "benchmarking paper" mean something here?

---

## 4. Overfitting audit

| # | Change | n | Type | Risk | Residual concern |
|---|---|---|---|---|---|
| 1.1 | §3 applied-ML exclusion | ~90 | Silence-filling | **Low** | Genre boundaries blur at the edges — "adversarial robustness" spans systems work and theory. Wording leans on *property vs. performance* to carry that, which is 1.2's job. |
| 1.2 | §2 property-not-result clause | 17 | Silence-filling + R4 restatement | **Low–moderate** | The 17 are the sample's most distinctive cluster, which is exactly what an overfitted rule would latch onto. Mitigated by it being `stats.md` §2's existing principle rather than a new one — but if you would not have written this sentence before seeing the labels, cut it. |
| 2 | `SETS` option 3 | 76 / 11 / 4 | Calibration, no text | **Low** | Sample category mix vs. steady-state mix. |
| 1.3 | AI-for-science flag | 4 | — | **Refused** | Below floor. |
| — | `compbio_mechanism` anything | 5 | — | **Refused** | Below floor. |
| — | `stats`, `probability` text | 32 / 16 | — | **None proposed** | Labels confirm existing criteria; nothing to add. |

**R5 compliance:** this is one pass. Patterns were extracted once, before any text was
drafted. I have not re-scored the drafts against the labels and will not.

**R6 compliance:** if adopted, 1.1 and 1.2 each carry a §8 marker naming the pattern and its
n, so both are identifiable and revertible when the fresh eval disagrees.

**The honest residual.** Even under every rule, two things stay unfixable. First, I chose
which aggregates to compute, and that choice was made after reading the papers. Second, 1.2's
17-paper cluster is the most salient pattern in the file, and salience is what overfitting
feeds on. The pre-registration below is the check on both.

---

## 5. Pre-registered predictions

Recorded before the fresh 60–80 labelled set exists, so these can be scored honestly rather
than rationalised afterwards. (`ingest/verify_prereg.py` already exists for this pattern.)

1. **If 1.1 is right:** applied-ML-systems papers in the fresh set are rejected by triage at
   ≥85% agreement with your labels. **If it is overfitted:** agreement is high on papers
   resembling the 90 but drops sharply on genres absent from them.
2. **If 1.2 is right:** pure-`cs.LG` papers with a property claim are admitted at a rate
   within ±10pp of the current 21% pure-CS admit rate. **If it is overfitted:** the fresh
   admit rate on this class runs well above 21%, meaning the clause was written wide enough
   to readmit the specific 17 rather than the class.
3. **If option 3 is right:** the ranked queue's top 10 per day contains ≥6 papers you would
   score ≥4. **If wrong:** the cap is a ranking cutoff over mostly-noise and narrowing was
   the correct call after all.
4. **Null prediction, worth holding to:** `stats` and `probability` borderline-stratum
   agreement should be **unchanged** by this pass, because nothing in either charter moved.
   If they improve, something leaked that this document does not account for.
