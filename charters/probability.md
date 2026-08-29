# Probability theory — knowledge base charter

> **DRAFT, third pass.** Second pass leaned on canon evidence that this domain, specifically, does not have. See §8 — the probability canon is the least representative of the four and should carry the least weight here.

## 1. Purpose

This KB is the **theory reservoir**. Its job is less to track probability as a field than to hold the machinery the applied domains are using — often at less than full strength. Prioritize results that *transfer*.

**Provenance caveat, and it is sharper here than in any other charter.** `canon/domain_map.yaml` gives this domain five topics: random matrices, Markov chains and Monte Carlo, Benford's law, risk and safety analysis, and probabilistic engineering design. Two of those five are engineering-risk topics, and *none* covers stochastic processes, limit theorems, concentration, or measure-theoretic probability — those either sat in the merged stats topics or have no OpenAlex topic at this granularity. So the vetting pool was substantially reliability engineering and never contained most of what this KB is actually for. **Canon silence about a category here is evidence about the topic map, not about the domain.** This pass therefore restores the first-draft scope and uses vetting only where it genuinely spoke.

## 2. In scope

Criteria, with examples where vetting or the first draft supports them. The criterion admits; the example illustrates.

- **Concentration inequalities and their assumption structure.** The highest-value category in this KB — a concentration result that weakens an assumption is the raw material of a theory-gap bridge. Vetting confirms: Hanson-Wright, user-friendly tail bounds for random matrices, and Vershynin's high-dimensional probability were all kept.
- **Limit theorems**, especially variants that relax standard conditions.
- **Random matrices and random graphs**, particularly spectral results. Strongly canon-confirmed.
- **High-dimensional probability and measure concentration.**
- **Optimal transport and metric-measure geometry.** Restored — see §8. This is the running example object throughout the repo's own documentation, and vetting kept unbalanced-OT scaling algorithms and Wasserstein distributionally-robust optimization.
- **Sparse and structured high-dimensional estimation where the contribution is the probabilistic structure** — sparse PCA, precision-matrix and covariance estimation, matrix completion. May also belong in `stats`; see §5.
- **Monte Carlo and MCMC methodology** — adaptive MCMC, particle MCMC, Riemannian-manifold samplers, convergence diagnostics with theory behind them.
- **Stochastic processes** — SPDEs, rough paths, branching, random walks, interacting particle systems.
- **Coupling, mixing times, Markov chain convergence.**
- **Stochastic optimization theory** where the probabilistic structure carries the result — proximal and coordinate-descent methods with convergence analysis.

## 3. Out of scope

- **Domain-specific engineering applications**, however probabilistic the machinery: combustion and detonation, wind-turbine and structural reliability, infrastructure and terrorism risk, maintenance scheduling. Canon-confirmed and by far the largest struck category — though see §8 on why it was so large.
- **Reliability and degradation modelling** tied to a specific equipment class rather than to the process theory.
- **Pure measure theory** with no probabilistic content.
- **Financial mathematics** unless the process theory is the contribution.
- **Statistical physics** unless the probabilistic structure is explicit and portable.
- **Software and package announcements**; **reviews and surveys** without a result.

Note what is deliberately *not* here: "too abstract to be currently useful." That is a score of 3 under §7, not an exclusion. See §8.

## 4. Mathematical object normalization — SHARED, identical across all four charters

1. **Name at the level of theory, not notation.**
2. **Use the canonical name; variants go in `aliases`.**
3. **Record the role, not just the presence.**
4. **Include objects the result relies on**, even if unforegrounded.
5. **Exclude objects merely cited** as related work.
6. **Flag unnamed usage** with `named_in_paper: false` plus `evidence`.
7. **Three to seven objects.** More than ten means you are listing notation.

Domain-specific warning: probability papers are *made* of mathematical objects, so the list can balloon. Record only the machinery the result turns on. Sigma-algebras are not informative.

## 5. Ambiguous — flag, don't silently reject

Score normally against §7, and also emit `"ambiguous": true`. A separate axis from `wildcard`: this flags a **known charter blind spot**, not a similarity-band judgment. Not for ordinary adjacency — that is a 3.

- **`[shared-sparse-estimation]`** — mirror of the entry in `stats.md` §5, same tag deliberately, because it is the same underlying pattern. Sparse PCA, precision-matrix estimation and matrix completion were kept in both domains' worksheets. Flag rather than force a single home.
- **`[control-theory-bio-modeling]`** — control theory and filtering connected to biological or cellular modelling. Several control and jump-system papers were kept specifically because they might model cell architecture. Overlaps `compbio_methods` (same tag there). Flag; do not silently pick a domain.
- **`[theory-without-current-contact]`** — a serious result with no visible applied contact today. Replaces the second pass's `[too-theoretical-inconsistency]`, which was incoherent: it told the agent a rule was firm in §3 and unreliable in §5 simultaneously. The rule is now simply that these score 3 and get flagged, so the pattern stays visible without being an exclusion.

## 6. arXiv categories

`math.PR`; `math.DS` selectively (only where the dynamics are stochastic); `math.ST`; `stat.ML`.

`math.ST` and `stat.ML` added this pass. Much of what §2 says this KB wants most — concentration inequalities, high-dimensional probability, sparse/structured estimation — is primary-listed or cross-listed in `math.ST` rather than `math.PR`; a random-matrix or concentration paper is about as likely to sit in one as the other, and restricting to `math.PR` alone was quietly starving this domain of exactly the work it claims to prioritize. `math.ST` already appears in `stats.md`'s category list too — that overlap is fine and expected, per the same reasoning as `[shared-sparse-estimation]` in §5: the two charters score the same paper independently, and cross-listing is normal, not a conflict to resolve.

**Watch `stat.ML` for the firehose problem `compbio_methods.md` §8 flags** for `cs.LG`/`stat.ML`/`math.OC`: it is a high-volume category and most of its daily traffic is generic machine learning with no probabilistic structure. The §7 bar — does the result weaken an assumption, not just apply one — has to do real filtering work here. If the daily backlog does not clear, narrow to `stat.ML` cross-listed with `math.PR`/`math.ST` rather than raising the cap.

## 7. Triage guidance

Score 5 for results that **weaken an assumption** other fields currently impose — independence, Gaussianity, bounded degree, stationarity. These are what theory-gap bridges are built from and they are worth more here than technical depth.

Score 4 for solid theory of portable machinery.

Score 3 for deep results in areas with no current applied contact. Excellent mathematics, but this KB is not a library — and per §5, flag these rather than discarding the observation. A 3 is a rejection with a note, not a verdict on the mathematics.

## 8. What changed in this pass

**The canon under-represents this domain badly, and the second pass did not account for it.** With two of five topics being engineering-risk, the vetting pool was full of wind turbines and detonation engines — so "domain-specific engineering was the largest struck category" is mostly a fact about `domain_map.yaml`, not a discovery about probability. The second pass treated that volume as signal and let the canon's shape drive the charter's shape.

**Restored from the first draft:** concentration inequalities as the top category, limit theorems that relax conditions, optimal transport and metric-measure geometry, rough paths. The second pass dropped all of these. Optimal transport is the clearest error of the four — it is the canonical worked example in `math-scout.md`, `bridge-finder.md`, `ERROR-TYPES.md` and `concordance_user.spec.md`, and the second pass removed it from scope because a five-topic canon happened not to surface much of it.

**Fixed an internal contradiction.** The second pass listed "results judged too abstract with no current applied contact" under Out of scope while §7 simultaneously scored them 3 — an exclusion and a rejection-with-a-note are different things, and the file asserted both. §7's treatment is correct and §3's bullet is gone.

**Dropped the psychology field ban**, for the reasons set out in `stats.md` §8: it is a precision move paid for in recall, and every paper you struck under it is independently caught by a content criterion. Reinstate if you disagree — see that section for the full argument, which applies identically here.

**Category list widened this pass:** added `math.ST` and `stat.ML` — the §6 flag from the last pass has now been acted on. See §6 for the reasoning and the `stat.ML` volume caveat.
