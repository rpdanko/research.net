# Statistics — knowledge base charter

> **DRAFT, fourth pass.** Promote with `mv charters/stats.pass4.md charters/stats.md` once
> you've read §8. Unlike passes 1–3, every judgment call in this file is yours — six rulings,
> recorded in §8. The prose is still mine; see §8's closing note on what that does and does
> not discharge.

## 1. Purpose

This KB exists to support intersection-finding, not to be a complete record of statistics. Admit papers whose **methodological machinery** might transfer or be transferred to. A perfectly good applied paper with no reusable machinery is correctly rejected.

**Provenance caveat, and it matters for everything below.** The vetting that informs this charter ran on the OpenAlex canon: journal articles, 2000–2025, citation-ranked. Triage runs on arXiv preprints in `stat.*` and `math.ST`. These are different populations. The canon was dominated by clinical and biomedical journal statistics; arXiv is dominated by theory and methodology. So canon evidence is strong evidence about what you value and weak evidence about what triage will actually see. Where this charter cites vetting, it says so — treat those as calibration, not as the specification itself.

## 2. In scope

Criteria, with canon-confirmed examples. **The criterion admits; the example only illustrates.** A paper doing something not on this list is admissible if it meets a criterion — that is the point of writing them as criteria. **All criteria here are subject to §3's first exclusion; see the precedence note there.**

- **Estimators and tests with analyzable properties** — consistency, convergence rates, efficiency, robustness, minimaxity.
- **Nonparametric and semiparametric methods**, especially function-space ones (RKHS, sieves, shape constraints).
- **High-dimensional inference** — regularization, selection, post-selection validity. Vetting confirmed this hard: Lasso, adaptive Lasso, Dantzig selector, LARS, L1-regularization paths all kept.
- **Causal inference where the contribution is identification or estimation**, not application. The single most consistent keep-pattern in vetting: difference-in-differences, two-way fixed effects, regression discontinuity, weak-instrument IV, propensity-score theory, confounder selection. You repeatedly flagged these as active areas worth prioritizing.
- **Assumption-lean inference, misspecification, and sensitivity analysis** — results that survive their assumptions failing.
- **Statistical computation where the algorithm has provable properties** — MCMC theory, variational methods with guarantees, INLA-style approximations. Note the distinction vetting drew sharply: the *algorithm* paper is in scope, the *implementation announcement* is not (INLA and stochastic variational inference kept; the Stan software paper struck).
- **Experimental design with mathematical structure.**
- **Meta-analytic methodology where the contribution is an estimator or its properties** — heterogeneity measures, network meta-analysis models, pooling estimators and their behaviour under misspecification. The methodology is in scope; the synthesis itself is not, per §3.
- **Evaluation methodology where the contribution is statistical** — calibration, proper scoring, the theory of what ROC/AUC and R² do and do not measure. Distinct from the reporting-guideline genre in §3, which covers similar ground with no statistical content.

## 3. Out of scope

Content criteria, not field labels. See §8 on why that distinction is explicit.

- **Work tied to a single setting, population, or dataset** such that the method would not be recognisable outside it — **whether or not it contains a methodological contribution.**

  *Precedence.* This exclusion overrides §2. A paper may present a genuinely novel estimator with analyzable properties and still be rejected here if the estimator is inseparable from the one cohort, registry, instrument, or population it was built for. That is the intended effect and not a contradiction to be resolved case by case: transferability is the thing this KB is for, and a method that cannot be lifted out of its setting cannot participate in a bridge no matter how sound it is. The cost is real — see §8's pre-registered check.
- **Meta-analyses and evidence syntheses reporting pooled effects.** The estimand is a summary of a literature, not a property of a method. Methodological work *on* meta-analysis is §2's.
- **Software and package announcements.** The paper exists to announce an implementation, not to establish a property of the method.
- **Reviews, tutorials, expository guides, position pieces, and consensus statements.** Includes the "how to choose/interpret/report X" genre, which is teaching, not contributing.
- **Reporting and checklist guidelines** — CONSORT, PRISMA, ARRIVE, STROBE, TRIPOD, ROBINS, GRADE and their variants. *Canon-derived and probably rare on arXiv* — this was the largest struck category by volume in the journal canon and will likely be near-absent in `stat.*`. Kept here as a short entry because it costs little and stat.AP occasionally carries reporting-adjacent work; do not let its length in this file suggest its frequency.

  *Not a verdict on their worth.* Research-practice standards — reporting checklists, preregistration, reproducibility programmes — are load-bearing for this project; `ingest/verify_prereg.py`, `rubrics/`, and the `review-loop` skill all rest on them. They are excluded here because the KB is the wrong container, not because they are unimportant: `card_schema.json` requires at least one `mathematical_object` and a reporting checklist has none, so such a paper cannot produce a card that validates. Their home is `rubrics/`. Triage rejects them; nobody should re-litigate this on the grounds that the papers are valuable, because that was never the disagreement.
- **Reproductions and errata.**

## 4. Mathematical object normalization — SHARED, identical across all four charters

These rules must be applied identically by every curator or the concordance fragments and every bridge is lost.

1. **Name at the level of theory, not notation.** "Reproducing kernel Hilbert space", not "the space defined in section 3".
2. **Use the canonical name; put variants in `aliases`.** "Sinkhorn divergence" → object `optimal transport`, alias `Sinkhorn`. When in doubt, the canonical name is the one a mathematician would use, not the one this subfield uses.
3. **Record the role, not just the presence.** What work is the object doing in this paper?
4. **Include objects the result relies on**, even if unforegrounded — machinery in the proof counts.
5. **Exclude objects merely cited** as related work.
6. **Flag unnamed usage** with `named_in_paper: false` plus an `evidence` quote. These are the highest-value entries in the system.
7. **Three to seven objects.** More than ten means you are listing notation.

## 5. Ambiguous — flag, don't silently reject

Score these normally against the scale in §7, but also emit `"ambiguous": true`. This is a separate axis from `wildcard` — it flags a **known charter blind spot**, not a similarity-band judgment. Do not use it for ordinary adjacency; that is what a score of 3 is for.

Named patterns. The bracketed slug is the tag to use in triage output (see `triage.md`):

- **`[shared-sparse-estimation]`** — Lasso variants, sparse PCA, precision-matrix estimation, matrix completion, shared with `probability`. Vetting kept these in *both* domains' worksheets. When the contribution is the estimation procedure it is yours; when it is the concentration or spectral structure it is `probability`'s — and the same paper can legitimately be both. Flag either way.
- **`[applied-field-methodology]`** — a genuine methodological contribution arriving in the clothing of an applied field (psychometrics, econometrics, epidemiology, political methodology). §8 explains why this is a flag rather than a rejection. If the method would be recognisable as statistics with the application stripped out, flag it rather than rejecting on the field. **Note the interaction with §3's first exclusion:** "recognisable with the application stripped out" is precisely the test §3 now applies. If the method survives that stripping it is in scope and this flag applies; if it does not, §3 rejects it and this flag does not rescue it.
- **`[econometrics-methodology-vs-application]`** — the DiD/TWFE/RDD cluster is this charter's strongest keep-signal, but not every paper in that literature is equally methodological. If the methodological contribution reads as secondary to a specific empirical application, flag it instead of scoring 5 on vocabulary alone.

## 6. arXiv categories

`stat.ME`, `stat.TH`, `stat.AP`, `stat.CO`, `math.ST`

Cross-lists are normal and not penalized.

## 7. Triage guidance

Score 5 for methodological work with explicit mathematical structure — most likely to participate in a bridge, and especially the causal-inference and high-dimensional clusters above. Score 4 for solid methodology without unusual structure. Score 3 (rejected) for competent applications. Being adjacent to scope is a 3, not a generous 4.

Two traps specific to this domain:

**Citation count is not scope evidence.** A reporting guideline or expository guide can be among the most-cited work in the field; that reflects everyone citing the checklist they followed, not methodological influence. Score on content.

**Field of application is not scope evidence either, in either direction.** A paper is not out of scope because it is motivated by psychology, and not in scope because it says "econometrics". The question is always whether there is transferable machinery. See §5's `[applied-field-methodology]`.

## 8. What changed in this pass

**Six rulings, all yours.** Passes 1–3 were agent-written throughout, which `README.md` and `WEEK-1-PLAN.md` both name as the wrong end state. This pass changes nothing on my own judgment. Each item below records what you decided and what moved.

| # | Question | Your ruling | Effect |
|---|---|---|---|
| A1 | Meta-analysis — you struck it three times in vetting ("I don't do metaanalysis"), the charter didn't mention it | **Split** | §2 gains a meta-analytic-methodology criterion; §3 gains an exclusion for syntheses reporting pooled effects. |
| A2 | "Too rudimentary" — stated 11 times in vetting, expressed nowhere in the charter | **Keep silent** | No change. Pass 3's redundancy argument stands: every such strike is caught by the tutorial/expository or no-contribution criteria. |
| A3 | Psychology / political-science field bans, which pass 3 softened to content criteria | **Keep as flag** | No change. `[applied-field-methodology]` stands; the hard bans stay out. |
| A4 | "Specific to X" — ~45 strikes, the reading that governs all of §3 | **Reading 2** | §3's first bullet replaced. Now excludes work tied to a single setting *even when methodologically novel*, with an explicit precedence note. |
| A5 | Experimental design — struck 5 times in vetting, restored to §2 by pass 3 | **Confirm** | No change. The five strikes are all reporting-guidance documents; the restoration holds. |
| A6 | A PRISMA paper kept at vetting line 13, against a §3 that excludes PRISMA by name | **Genuine, wrong container** | §3's guideline bullet gains a note: these are valued by the project and belong in `rubrics/`, not the KB, because they cannot produce a card with a `mathematical_object`. |

**No label-derived changes in this pass.** `eval/labels.jsonl` licensed nothing here: of 32 stats-domain rows, the 10 rejections all fall under §3's pre-existing bullets, so the labels confirmed the charter rather than adding to it. Per `LABEL-USE-PROTOCOL.md` R6, any label-derived text would carry a marker naming the pattern and its n. There is none, so this charter remains entirely canon-and-judgment derived and stays valid as an eval target.

**The one thing to watch, pre-registered.** A4 reading 2 is the largest scope change in this pass and it buys precision with recall — exactly the trade invariant 9 prices at 3:1 against. I deliberately have **not** estimated its cost against the 180 labelled papers: `LABEL-USE-PROTOCOL.md` R5 forbids re-scoring a draft against the labels, and a reassuring answer would not make the loop safe. So it is recorded as a prediction instead:

> On the fresh labelled set, false negatives attributable to §3's first exclusion should be
> **sparse and non-systematic**. If they cluster in one subfield — most likely biostatistics or
> psychometrics, where methods and settings are hardest to separate — reading 2 is cutting
> into scope rather than trimming applications, and the bullet should revert toward reading 1.

Per `WEEK-1-PLAN.md` §6, "no systematic miss" is already a done-criterion. This is that criterion pointed at a specific bullet.

**What this does not discharge.** The judgment in this file is now yours; the prose is still mine. `README.md`'s requirement is handwriting, not just decisions, and picking from drafted options is not the same as writing the thing. §2 and §3 are where that gap matters most — if any sentence there is one you would not have written, it should be overwritten before this is promoted.
