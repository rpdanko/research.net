---
bridge: b-2608-001
verdict: assumption-blocked
error_type: conceptual-math
confidence: high
searched:
  - "doubly robust estimation probe accuracy under missing labels interpretability evaluation"
  - "positive-unlabeled evaluation linear probes SwissProt sparse annotations lower bound precision"
  - "Neyman orthogonal doubly robust estimator positive-unlabeled learning MNAR label bias identification"
  - "calibrated debiased machine learning isotonic Riesz representer semi-supervised missing outcome"
prior_work: []
---

## The object in each source

### stats 2411.02771 (card + search)
Object: a **doubly robust / debiased-ML estimator of a linear functional of the outcome
regression** E[Y | X] (ATE-class / mixed-bias parameters). Two nuisances: the outcome
regression and the Riesz representer. The paper's contribution is narrowly about the
**second-order / inferential** behaviour: isotonic calibration of the two cross-fitted
nuisances upgrades "double robustness of consistency" to "double robustness of
asymptotic normality" under an *asymptotic partial-orthogonality* condition, so a
root-n CI survives when only one nuisance converges fast.

Crucially — the functional is assumed **identified**. Nothing in the abstract, the
conclusion, the card `problem`/`setting`/`method`, or the calibratedDML literature
found in search addresses non-ignorable missingness. Identification (ignorable
missingness / unconfoundedness + overlap) is a *precondition*, not something the
method delivers. The card's `limitations` say the estimand class is "linear
functionals of the outcome regression" and the load-bearing assumption is partial
orthogonality, which is stated for that identified setting.

### compbio 2608.11475 (card + search)
Object: **probe precision / F1 scored against sparse SwissProt annotations**, which the
paper calls a *lower bound* because a model-correct prediction on an unannotated
residue is charged as a false positive. The card's `mathematical_objects` entry names
the mechanism directly: aliases "missing-not-at-random annotations",
"positive-unlabeled evaluation", "censored labels". `cross_domain_note`: "a
positive-unlabeled / censored-data problem". `open_questions`: formalize the
correction "e.g. as positive-unlabeled learning".

## Q1 — same object?
Partially. "A linear functional of a regression function estimated by an
influence-function correction" is genuinely shared machinery, and probe precision can
be written as E[m(X) 1{g(X)=1}] / E[1{g(X)=1}] with m(X) = P(true label | activation),
a linear functional of m. So this is not a pure name collision. The divergence is in
which property is load-bearing (Q4).

## Q2 — comparable work?
Weak. The stats result operates *downstream of identification*: it protects the CI
when a nuisance is ML-estimated at a slow rate. The compbio bias is *upstream* — a
first-order, systematic downward bias from the label being unobserved in a way
correlated with the label itself. Calibrated DML's "double robustness" is robustness
to nuisance-estimation error, not robustness to a non-ignorable observation process.
A theorem that "calibration upgrades DR-consistency to DR-normality" says nothing
about de-biasing an unidentified estimand.

## Q3 — already done?
No single paper does this specific application (DR/Neyman-orthogonal correction of
probe-decodability metrics against sparse protein annotations). But the general
combination — doubly-robust / Neyman-orthogonal estimation for MNAR and
positive-unlabeled label bias — is an established, active area. Search surfaced
(titles only, not opened, not relied on for this kill): "Positive-Unlabeled Learning
in Implicit Feedback from a Missing-Not-At-Random Perspective" (Entropy 2025);
"On Non-Random Missing Labels in Semi-Supervised Learning" (arXiv, 2022); "A Doubly
Robust Framework for Addressing Outcome-Dependent Selection Bias in Multi-Cohort EHR
Studies" (arXiv). These matter for the novelty referee: the hard part (identification
under MNAR/PU) is a literature of its own that the stats source paper is not part of.
This did not drive the verdict; the verdict is Q4.

## Q4 — transfer blocked by an assumption?  YES.
Calibrated DML works because the functional is identified: ignorable (MAR)
missingness given observed covariates, plus overlap. The compbio card states its
missingness is **not** that — "missing-not-at-random annotations", "positive-unlabeled",
"censored". SwissProt feature annotation (signal peptides, disulfide bonds) is present
only for experimentally characterised regions; annotation status is correlated with
the very biology being probed, i.e. non-ignorable. The stats paper supplies nothing
for that regime.

The bridge is aware of the gap and papers over it in `must_be_true`:
- #2 concedes overlap may fail and vaguely substitutes "a sensitivity/bounds model" —
  which is a different method, not this paper's.
- #3 needs partial orthogonality "in the annotation-missingness model" — asserted, and
  precisely the object the stats paper does not establish outside the identified
  setting.
- #4 proposes a "dense gold label (DSSP-style)" subset to fit the annotation-propensity
  nuisance. This is a category error: DSSP labels secondary structure; the sparsely
  annotated SwissProt features are signal peptides / disulfides / AA identity. There is
  no dense gold-label subset for the features that are actually MNAR, so the propensity
  nuisance cannot be fit and the "doubly robust" claim collapses to single robustness
  at best.

## Verdict
`assumption-blocked`, `conceptual-math`, confidence high. The bridge misreads what the
stats paper's "double robustness" delivers — robustness to nuisance-estimation error
for an *identified* linear functional — and treats it as a solution to a
non-ignorable-missingness (PU) *identification* problem that the paper never touches.
The compbio paper's own card labels the mechanism MNAR / positive-unlabeled, and there
is no dense-label subset for the affected features to fit the required propensity
nuisance. The connection is not real as stated.
