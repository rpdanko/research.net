# Eval 01 — findings and proposed fixes

> ## ⚠ Status, updated 2026-08-28 — the headline numbers below are SUPERSEDED
>
> This document analyses run `20260827-144416`. **Two later score runs exist**
> and neither is mentioned anywhere below. The §4 drafts were evidently applied
> and they worked; §5's "nothing here is applied" is no longer true.
>
> | Run | recall | precision | F-beta(3) | within±1 | misses |
> |---|---|---|---|---|---|
> | `20260827-144416` (this doc) | 0.803 | 0.570 | 0.771 | 0.650 | 15 |
> | `20260827-201651` | 0.915 | 0.607 | 0.871 | 0.717 | 6 |
> | `20260827-214656` (latest scored) | **0.901** | **0.688** | **0.874** | 0.767 | 7 |
> | latest, corrected for the `2509.18530` flip | **0.903** | **0.699** | **0.877** | 0.772 | 7 |
>
> **Recall and precision are both at or above target** (0.90 / 0.60) — they were
> both below when this document was written. Read §1–§6 as the diagnosis that
> produced the fixes, not as a description of current performance.
>
> **The correction in the last row** is arithmetic, not a re-run: `2509.18530`'s
> label was corrected on 2026-08-28 (`my_score` 2→5), after every run above. It
> was a false positive in the latest run and becomes a true positive, so
> tp 64→65, fp 29→28, true_in 71→72, and it also moves inside ±1. Derived from
> the stored run JSON plus `predictions.jsonl`, which was confirmed to be the
> file run `214656` scored — all 7 of its misses score below their own threshold
> in that file.
>
> **Two things below cannot be reproduced and should not be re-derived:**
>
> - The per-stratum line (`borderline 0.75 / expect_in 0.83 / expect_out 0.46`)
>   was computed when strata still held raw un-normalized values (`in`, `In`,
>   `Borderline`, `borderlinne`, `pit`). Those were rewritten during the
>   `OPEN-QUESTIONS.md` §1.2 hygiene pass, so the buckets no longer partition the
>   set the way they did at run time. The cells do not reconcile with the overall
>   within±1 figure and are best treated as lost.
> - The "You" column in §2 predates both the 5 relabels §5 recommended and the
>   `2509.18530` flip. Your admits went 76 → 71 → 72.
>
> **Still genuinely open:** the per-domain `calibrate()` re-run
> (`OPEN-QUESTIONS.md` §1.3). Every number in this table is pooled across all
> four domains. Separately, one of §6's own pre-registered checks has fired and
> was never followed up — see §7.

Run `eval/runs/20260827-144416.json`, pass-3 charters, 180 labelled papers.
Nothing here is applied. Drafts in §4 need your approval.

```
recall 0.803  precision 0.570  F-beta(3) 0.771  within±1 0.650
borderline 0.75   expect_in 0.83   expect_out 0.46
15 missed in-scope · 5 wildcard admissions
```

---

## 1. The two raters were not asked the same question

`eval_triage.py label()` displays `arxiv_id`, `categories`, `stratum`, title and
abstract. It does **not** display the domain, and it does not put a charter in front of
you. So you scored each paper against your own sense of what this project should hold.

`triage.md` asks something else entirely: *"A paper may score 5 for one domain and 1 for
another. Score each domain independently"* — against one charter, the one its router
picked.

**Good news first:** because your labels are domain-agnostic, changing `SETS` re-routes
papers without invalidating a single label. The `SETS` fix in §4 costs no re-labelling.

**The reframe:** part of the 0.803 is not triage failing to find what you wanted. It is
two raters answering different questions. The Selmer-groups paper is the clean case —
you scored it 4 because you want it; probability's charter does not claim number theory;
triage said *"keyword collision on math.PR"* and was right on the question it was asked.
Recorded as a miss, it is a category mismatch.

This also explains `expect_out` at 0.46, the worst cell in the table. You score a
rejection 2 ("same vocabulary, different concern"); triage scores 3–4 against a charter
that half-claims it. Both reject. The ±1 metric counts it as disagreement.

---

## 2. Triage over-admits — the low precision is not a broad charter

| Score | You | Triage |
|---|---|---|
| 0–2 | 86 | 47 |
| 3 | 18 | 26 |
| 4–5 | **76** | **107** |

46 false positives. Triage's mass sits at 4, yours at 2. `triage.md` tells it to take the
higher score when torn and prices recall 3:1, with nothing pulling the other way — so it
rounds up systematically. Recall *and* precision both under target means the charter is
not discriminating: admitting the wrong papers while missing right ones. That is a
different disease from "too narrow," and the usual reflex — widen the charter — makes it
worse.

---

## 3. The 15 misses, classified

Only **three** are genuine charter holes.

| Type | n | Papers |
|---|---|---|
| **Routing** — charter judged a paper that should never have reached it | 4 | Surrogate modeling · protein language models · Safe Start · Evolutionary Curriculum Learning |
| **Triage was right** | 3 | Comment on… (scale: 0 = comment) · GenAI review · Integrating RCTs/RWD |
| **Container error — your ruling** | 2 | SGHA · Advanced Linear Algebra |
| **Question mismatch** (§1) | 2 | Selmer groups · Multidimensional Sorting |
| **Exemplar override** (§4B) | 1 | Network Meta-Analysis |
| **Genuine charter question** | 3 | Quantum Markovian · Forking Fast · Backward through Time |

**Routing detail.** Three distinct `SETS` pathologies, all first-match-wins artifacts:

- `cs.LG` (compbio_methods, 3rd) beats `q-bio.*` (mechanism, 4th) → every protein and
  sequence paper goes to methods. Mechanism got **2 of 180**.
- `stat.ML` sits in *probability's* list at position 2 → a biological-sequence VAE paper
  was scored against the probability charter, which correctly said "not probabilistic."
- `math.OC stat.ME` → `stats` wins on `stat.ME`, so an optimization paper was judged by
  the statistics charter, which correctly said "optimization theory not charter statistics."

**Your numerical-methods point needs no charter edit.** `compbio_methods.md` §2 already
reads *"Numerical methods and matrix algorithms where the contribution is the method."*
The criterion exists; `math.NA` never reaches it. This is routing, not scope.

**Good news buried in the list:** `[theory-without-current-contact]` **fired correctly**
on Quantum Markovian Dynamics — the first evidence the ambiguous tier works. It found the
right paper; §7's guidance then scored it 3 where you said 4. That is a scoring-guidance
question, not a blind spot.

**Projected effect of fixes.** Relabelling the 5 papers in "triage was right" and
"container error" gives recall ≈ 0.86 with no code change. Fixing the 4 routing cases
could reach ≈ 0.92, above target. Estimates, not results — they need a re-run to confirm.

---

## 4. Drafts

### A. `arxiv_pull.py` — `SETS` order and membership

```python
# Order matters: _infer_domain takes the FIRST domain whose category list
# intersects the paper's, so the most specific domain must come first.
SETS = {
    # Moved to front. A q-bio cross-list is the cheapest available proxy for
    # compbio_methods.md §1's "the biology is load-bearing" test. Last in the
    # old order, cs.LG claimed every protein and sequence paper and this
    # domain received 2 of 180 labelled papers.
    "compbio_mechanism": ["q-bio.BM", "q-bio.QM", "q-bio.MN", "q-bio.SC", "q-bio.PE"],
    "stats":             ["stat.ME", "stat.TH", "stat.AP", "stat.CO", "math.ST"],
    # stat.ML removed -- see the note below, this one is a decision, not a fix.
    "probability":       ["math.PR", "math.DS", "math.ST"],
    # math.NA added: §2 already claims "numerical methods and matrix algorithms
    # where the contribution is the method", but no domain listed the category.
    # cs.NE contributed 0 papers in 180 -- kept anyway, because §3's
    # benchmark-only metaheuristic rule is written against that literature and
    # a 2-week window is not evidence of its absence.
    "compbio_methods":   ["math.OC", "cs.LG", "cs.NE", "stat.ML", "math.NA"],
}
```

**`stat.ML` is a decision, not a repair.** `probability.md` §6/§8 added it deliberately
in pass 3, with a volume caveat. Removing it sends ML-theory papers to
`compbio_methods` — which matches where they were admitted from — but it reverses a
pass-3 judgment, so it is yours to make. Leaving it costs the Evolutionary Curriculum
Learning class of miss.

### B. Exemplars override charters — the architectural one

Verified: `stats`' first negative exemplar is `OUT: I don't do metaanalysis`, and triage
cited it by name to reject the NMA paper. `canon_index.exemplars()` renders
`strike_reason` straight from the vetting worksheet, and `triage.md` says the negative
block *"matters more"* than the positives.

**So promoting `stats.pass4.md` will not fix that miss.** Your A1 split says admit;
exemplar #1 says strike; the exemplar wins. Charters are revisable, exemplars are frozen
at pass-1 judgments, and every future ruling that contradicts a strike reason is silently
reversed at triage time. A4 and A6 are exposed to the same mechanism.

**B1 — precedence, one line in `.claude/agents/triage.md`** (I cannot write to `.claude/`;
paste this into the "What the exemplars are for" section):

> **Where an exemplar's strike reason contradicts the charter, the charter governs.**
> Exemplars are frozen at the time of vetting and predate charter revisions; the charter
> is the current specification. If you reject a paper on a near-miss resemblance, check
> that the charter still excludes it.

**B2 — suppression, ~5 lines in `canon_index.py`.** Add an optional `strike_superseded`
field to canon records; `exemplars()` skips any record carrying it. Preserves the vetting
record intact — the strike reason stays exactly as you wrote it — while keeping an
overruled judgment out of the prompt. Set it on the meta-analysis record once A1 lands.

**B3 — separate defect, worth naming.** `exemplars()` takes `[:6]` of the struck records:
the first six in file order, which is citation-rank order. The six *most-cited* strikes,
not the six most instructive. For a block `triage.md` says matters more than the
positives, that selection is arbitrary.

### C. `eval_triage.py label()` — show the domain

One line, and it closes §1's gap for the next labelled set:

```python
print(f"{r['arxiv_id']}  [{r['categories']}]  domain={r['domain']}  stratum={r['stratum']}")
```

Does not fix the existing 180 — those were scored domain-blind and stay that way. But a
fresh set labelled with the domain visible would be answering triage's question, and the
agreement number would mean what the plan assumes it means.

---

## 5. Recommended order

1. **Relabel the 5** in "triage was right" and "container error." Your judgment; no code.
2. **Decide the metatool shelf.** SGHA and the linear-algebra notes are the A6 pattern
   again — valuable to the project, not KB material. A6 sent research-practice standards
   to `rubrics/`; this needs its own home, or those papers keep reappearing as misses.
3. **Apply A** (and rule on `stat.ML`).
4. **Apply B1**, then promote `stats.pass4.md`. In that order — promoting first measures a
   charter the exemplars are still overriding.
5. **Re-run** prepare → dispatch → collect → score → `diff`.

## 6. Pre-registration for the re-run

Carried forward from `PASS-4-DRAFTS.md` §5, plus:

- **Routing fix:** `compbio_mechanism` should receive roughly 10–14 papers, not 2. If it
  stays under 5, the q-bio proxy is not doing what §1's routing test assumes.
- **B1:** the NMA paper should move from 2 to ≥4. If it does not, the precedence line is
  too weak and B2's suppression is required rather than optional.
- **Unchanged:** the null prediction stands — `probability` agreement should not improve,
  since its charter has not moved. If it does, something leaked.
- **Over-admission:** watch whether precision moves. None of these fixes address the
  round-up bias in §2, so precision should stay near 0.57. If it rises without a
  `triage.md` scoring change, find out why before believing it.

---

## 7. §6's pre-registered checks, scored against the later runs

Added 2026-08-28. §6 was written as a pre-registration and then never settled
against the runs that followed. Doing that now, because a pre-registration you
don't return to is just a note.

**PASSED — routing fix.** Predicted `compbio_mechanism` should receive roughly
10–14 papers, not 2, or "the q-bio proxy is not doing what §1's routing test
assumes." It now holds **10** labelled rows (`OPEN-QUESTIONS.md` §1.5, re-derived
from the backfilled `domain` field). Bottom of the predicted range, but inside it.
The proxy works.

**FIRED, AND NEVER FOLLOWED UP — over-admission.** This is the one that matters.
§6 predicted precision "should stay near 0.57" and said explicitly: *"If it rises
without a `triage.md` scoring change, find out why before believing it."*

Precision went **0.570 → 0.607 → 0.688**, a rise of 0.12. That is exactly the
condition §6 named, and the investigation it calls for has not happened. Either:

- a `triage.md` scoring change *did* land, in which case the round-up bias in §2
  was addressed by something not recorded here and the mechanism should be named; or
- it did not, and a 0.12 precision gain arrived from routing and exemplar fixes
  alone — which §2's diagnosis says should not happen, and would mean §2 has the
  disease wrong.

**Do not treat the 0.688 as banked until this is resolved.** It is the single
largest unexplained number in the repo, and it is load-bearing: it is the
difference between precision being below target and above it.

**UNTESTABLE AS WRITTEN — the `probability` null prediction.** §6 predicted
`probability` agreement "should not improve, since its charter has not moved."
`score_run()` only reports pooled figures and a per-*stratum* breakdown; it never
breaks down by domain, so this prediction cannot be checked against the stored run
JSON, which keeps only pooled metrics plus a miss list. Checking it needs either a
per-domain scoring mode or a manual pass over `predictions.jsonl` joined to the
labels. Worth having — it is the same per-domain gap `OPEN-QUESTIONS.md` §1.3
raises for `calibrate()`.

**PARTIALLY CHECKABLE — B1 and the NMA paper.** Predicted to move from 2 to ≥4.
Resolvable by hand from `predictions.jsonl`; not done here because the paper is
identified in §3 only by the name "Network Meta-Analysis" and matching it to an
arXiv id needs the labels file. One lookup, worth doing alongside the precision
question above since both bear on whether the exemplar-override fix did the work
it was credited with.
