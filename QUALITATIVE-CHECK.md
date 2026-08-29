# WEEK-1-PLAN §6 qualitative check — run 20260827-203053

The plan's literal test: read ten triage `reason` strings and agree with eight
**for the stated reason**, not merely the verdict. Never performed before this
pass. Ten picked by even line spacing through `predictions.jsonl` (offsets 5,
20, 40, 60, 80, 100, 120, 140, 160, 175) — not cherry-picked.

Each reviewed against its `labels.dev.jsonl` abstract and the relevant
charter section, independently of `my_score` — the test is whether *I* agree
with the stated reasoning, not whether it matches an old label.

| arxiv_id | domain | score | reason (as given) | verdict |
|---|---|---|---|---|
| 2109.02644 | probability | 4 | Heterogeneous random matrix theory weakens i.i.d. assumptions. | Agree. Abstract is exactly this — non-identical column profiles, no i.i.d. assumption. |
| 2411.02771 | stats | 5 | Calibrated DML for asymptotic normality; §2 causal inference. | Agree. Doubly robust estimation, calibration for asymptotic normality — core §2 territory. |
| 2509.18530 | compbio_methods | 5 | Universal function approximator for quantum inputs; §2 learning theory property. | Agree with the reasoning, but flag: my_score was 2 (expect_out). §2's unifying test names "approximation quality" as an in-scope property outright, and that's the paper's whole claim. Triage is reading the charter correctly as written — this looks like the old label is the one worth rechecking, not the triage call. |
| 2605.01835 | compbio_methods | 5 | Theory-informed Koopman operator learning improves sample efficiency; §2 methodology. | Agree. Matches abstract and §2 exactly. |
| 2608.03836 | compbio_methods | 1 | Formal verification of workflow persistence semantics; wrong field (software engineering). | Agree. TLA+/Verus conformance-checking paper, cs.SE/cs.DC/cs.LO — correctly identified as out of field. |
| 2608.09856 | probability | 4 | Random tree mass erasure and Lévy forests; charter §2 lists branching. | Agree. R-tree mass erasure converging to Lévy/GW branching forests — squarely branching-process territory. |
| 2608.12974 | compbio_methods | 0 | Malformed: Comment on another paper; no original contribution. | Agree — exactly. This is the "Comment on..." paper Robin himself relabeled 4→0 earlier, agreeing triage was right. Clean confirmatory case. |
| 2608.15616 | probability | 4 | Super-Brownian motion compact support irregular drift; charter §2 lists branching. | Agree. Compact-support SPDE result for super-Brownian motion — branching diffusion. |
| 2608.17678 | compbio_methods | 5 | Conformal prediction for label-shift robustness with formal guarantees; §2 learning theory. | Agree. Statistically rigorous UQ under distribution shift — a property claim, not a benchmark result. |
| 2608.20406 | stats | 4 | MLAMA adaptive ensemble for time-series forecasting; methodological framework for model selection weighting. | **Disagree.** Title is literally "...an Ontario COVID-19 Case Study"; the entire evaluation is one jurisdiction's 190-week case-count series with no out-of-setting validation. This is the exact shape `stats.md` §3's A4 exclusion ("tied to a single setting, population, or dataset... whether or not it contains a methodological contribution") was rewritten to catch. The reason string focuses on the ensembling idea and never engages with the single-dataset container. |

## Result

9 of 10 agreed with, for the stated reason — clears the ≥8/10 bar.

One real miss (2608.20406): triage didn't apply the A4 single-dataset
exclusion to an applied forecasting case study. Worth a look at whether the
`stats` exemplar set has enough of this *forecasting/time-series* shape to
make A4 salient — the existing negative exemplars may skew toward the
psych/poli-sci pattern A3 already flags, not this one.

One flagged relabel candidate (2509.18530): `my_score: 2` in
`labels.dev.jsonl` looks like it predates a careful read against §2's
"approximation quality" clause. Not changed here — flagging for Robin's own
call, per `LABEL-USE-PROTOCOL.md`'s spirit (labels are data Robin owns, not
something I silently edit).

## WEEK-1-PLAN §6 status

All four done-criteria now met on the same trustworthy run (20260827-203053 /
score summary 20260827-214656):

- recall 0.901 (≥0.90)
- precision 0.688 (≥0.60)
- borderline-stratum agreement 0.78 (≥0.70)
- qualitative reason-check: 9/10 (≥8/10)

No systematic-miss pattern found beyond the two items above, both of which
are narrow and named, not a class of papers falling through a gap.
