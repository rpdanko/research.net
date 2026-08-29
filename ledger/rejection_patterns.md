# Rejection patterns

Accumulated skeptic kills, grouped by category. Read by `bridge-finder` at the
start of every run. Each entry: `error_type` tag + one prose sentence naming the
fault. Tags are from `rubrics/ERROR-TYPES.md`; counted by `review_audit.py --errors`.

---

## Assumption mismatch (technique needs a property the target data lacks)

- **b-2608-001** — `conceptual-math` — Bridged calibrated debiased-ML (2411.02771)
  onto the sparse-SwissProt probe-precision "lower bound" problem (2608.11475),
  but the stats paper's "double robustness" is robustness to nuisance-estimation
  *rate/misspecification* for an *identified* linear functional, whereas the
  compbio problem is an *identification* failure under non-ignorable (MNAR /
  positive-unlabeled) label missingness — a regime the stats paper never
  addresses — and there is no dense gold-label subset for the affected SwissProt
  features (signal peptides, disulfides; DSSP labels a different concept) to fit
  the required annotation-propensity nuisance.

---

## Shared object misidentified (same name, two different mathematical things)

- **b-2608-002** — `conceptual-math` — Bridged calibrated DML / Neyman-orthogonal
  estimation (2411.02771) onto the "confounded" null steering result in
  2608.11475 (adding a strand direction to the trunk single representation `s`
  moves nothing; strand info may live in the pair representation `z`), calling
  both "estimating an intervention effect while partialling out a high-dimensional
  nuisance control." Not the same object: the stats paper's nuisance is an
  *unknown confounding-adjustment function estimated from an i.i.d. sample with
  controlled error*, and orthogonality exists to neutralize that estimation error
  for an *identified* functional — whereas in the deterministic Boltz-1 forward
  pass the treatment `delta` is exogenous and analyst-set (no confounding, the
  bridge itself concedes no overlap problem), `z` is *computed not estimated* (no
  nuisance function, no sampling distribution, nothing for root-n or orthogonality
  to act on), and the real question is a *path-specific / mediation-locus* one —
  does the concept's causal effect route through `s` or `z` — which the compbio
  paper's own open_questions say is answered by *intervening on* `z`, not
  *adjusting for* it. "Causal effect estimation" in both is the false positive:
  statistical inference of an identified parameter from a noisy sample vs. asking
  which internal node of a known deterministic function carries a computation.
