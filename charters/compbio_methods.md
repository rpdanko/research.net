# Computational biology — methods — knowledge base charter

> **Promoted, fourth pass — adopted 2026-08-28.** Both label-derived changes below (the §2 property-not-result clause, the §3 applied-ML-systems exclusion) are live, per §8's audit. `eval/labels.jsonl` is renamed `eval/labels.dev.jsonl` (R8) — those 180 rows partly drafted this charter, so they are now a development set for `compbio_methods` specifically, not a valid measurement of it. A fresh held-out set is needed before trusting any recall/precision number for this domain (`OPEN-QUESTIONS.md` §1.6). §8's firehose question is resolved separately (option 3, 2026-08-28).

## 1. Purpose

Despite the name inherited from the topic split, this KB is **not** biology-specific. It tracks general optimization, learning, and computational methodology — the algorithmic toolkit computational biology work draws on — as distinct from `compbio_mechanism` (renamed from `compbio_genomics`), which covers biological structure and mechanism.

The routing test: **would this method still be worth keeping if the word "biology" were deleted from the abstract?** If yes, it is here. If the biology is load-bearing, it is `compbio_mechanism`'s.

**Provenance caveat.** Vetting for this domain ran on a canon of citation-ranked journal articles in computational-theory and optimization topics. Its clearest finding — the metaheuristic pattern in §3 — transfers to arXiv well, because `cs.NE` is thick with exactly that literature. Its silences transfer less well; as elsewhere, absence from the canon is not evidence of exclusion.

## 2. In scope

**The unifying test across every criterion below: is the contribution an analyzable property of a method — convergence, complexity, coverage, identifiability, approximation quality, sample complexity — or is it an empirical result?** The property is what transfers and what a concordance entry can be written against. This holds regardless of the applied wrapper: a paper about language models, molecules, or images is in scope when the claim is a property, and out when the claim is performance. *[Label-derived, `LABEL-USE-PROTOCOL.md` R4 — restates `stats.md` §2's opening criterion for a literature the OpenAlex canon did not contain, rather than inventing a new one. Evidence: 15 labelled papers, pure `cs.*` categories with no `math.*`/`stat.*`/`q-bio.*` cross-list, scored ≥4 — conformal prediction under label shift, Koopman operators for coupled systems, GD convergence via generalized Lipschitz structure, quantum matrix-multiplication complexity, among others. (Originally counted at 17 before two were independently relabeled down as container errors in a separate correction — see `EVAL-01-FINDINGS.md`; unrelated to this clause's evidence, which stayed intact under the domain-routing fix since none of the affected papers carried a `q-bio.*` tag.)]*

Criteria, with canon-confirmed examples. The criterion admits; the example illustrates.

- **Optimization methodology with algorithmic or theoretical content** — convergence results, complexity results, a genuine structural idea. Vetting kept particle swarm optimization, differential evolution and its adaptive variants, gradient and proximal methods, mixed-integer nonlinear optimization.
- **Learning theory and neural-network methodology**, including hyperparameter optimization and theoretical treatments of deep networks.
- **Sparse, low-rank, and tensor methods** — sparse PCA, matrix completion, tensor decomposition.
- **General causal-inference frameworks** — Pearl-style causal modelling, flagged in vetting as foundational to how you think about this work rather than as a narrow application.
- **Graph, network, and combinatorial algorithms** with real algorithmic content.
- **Numerical methods and matrix algorithms** where the contribution is the method.
- **Control theory when connected to modelling biological or cellular systems.** Selective, not blanket — see §5.

## 3. Out of scope

- **Benchmark-only metaheuristics.** A new search heuristic whose entire evidence is "we ran it on standard test functions and it did well," with no convergence analysis, no complexity claim, and no structural insight. **The animal name is the tell, not the criterion**: bat, grey wolf, hippopotamus, pelican, vulture, firefly, cuckoo, osprey, lemming, salp, gorilla, rabbit, tornado, hiking. Vetting struck this pattern with near-perfect consistency across dozens of papers, and `cs.NE` produces it continuously. Stated as content rather than nomenclature so that a genuinely theoretical paper with an unfortunate name is not lost — see §5's `[animal-name-exception]`.
- **Narrow single-application engineering** — antenna design, aircraft conflict resolution, circuit layout — where an existing optimizer is applied and nothing methodological is added.
- **Software and package announcements** with no methodological content of their own.
- **Reviews, surveys, and historical overviews** without a result.
- **Applied machine-learning systems work.** Benchmarks and benchmark suites, retrieval and recommendation pipelines, agent frameworks, deployment and serving engineering, fine-tuning recipes, adversarial-robustness demonstrations, and domain applications of existing architectures. The contribution is a system that works or a number on a leaderboard, not a property of a method. *[Label-derived, `LABEL-USE-PROTOCOL.md` R3 silence-filling — the charter previously said nothing about this genre; the bullets above were written for metaheuristics and narrow engineering and don't obviously reach it. Evidence: this domain's largest rejected genre by volume, well clear of R7's floor. A paper titled "AI4AI-Bench: Benchmarking LLM Agents in Algorithmic Design" is caught by none of the existing bullets without stretching "narrow single-application engineering" past what it was written to mean.]*

## 4. Mathematical object normalization — SHARED, identical across all four charters

1. **Name at the level of theory, not notation.**
2. **Use the canonical name; variants go in `aliases`.**
3. **Record the role, not just the presence.**
4. **Include objects the result relies on**, even if unforegrounded.
5. **Exclude objects merely cited** as related work.
6. **Flag unnamed usage** with `named_in_paper: false` plus `evidence`.
7. **Three to seven objects.** More than ten means you are listing notation.

## 5. Ambiguous — flag, don't silently reject

Score normally against §7, and also emit `"ambiguous": true`. Separate axis from `wildcard`; not for ordinary adjacency, which is a 3.

- **`[bio-connection-not-load-bearing]`** — the §1 routing test has a real gray zone: papers gesturing at biological motivation without the method depending on biological structure. If applying the test yields a close call rather than a clean answer, flag rather than forcing a yes/no.
- **`[control-theory-bio-modeling]`** — same tag as `probability.md` §5. Could belong to either, or to `compbio_mechanism` if the biological system itself is the point rather than the control method.
- **`[animal-name-exception]`** — an animal-named optimizer that nonetheless makes a substantive theoretical claim: a real convergence proof, a complexity result, a structural insight. The §3 rule is a strong heuristic about a genuine literature-wide pattern, not a certainty, and this is the channel that keeps it from becoming one.
- **`[theory-without-route-to-practice]`** — replaces the second pass's flat "too theoretical" exclusion. This charter does want applicable methodology, and `probability` is the home for portable theory without current contact. But the boundary is not crisp, and a permanent exclusion buys precision with recall that invariant 9 says we should not spend. Score it 3 and flag it.

## 6. arXiv categories

`q-bio.BM`, `q-bio.QM`, `q-bio.MN`, `q-bio.SC`, `q-bio.PE` route to `compbio_mechanism` **before** this domain is checked — see `arxiv_pull.py`'s `SETS` comment. This domain's own list: `math.OC`, `cs.LG`, `cs.NE`, `stat.ML`, `math.NA` — `math.NA` added this pass, closing the gap where §2's numerical-methods criterion had no category route in at all (`EVAL-01-FINDINGS.md` §4A). **Still draft. §8's firehose question is resolved (2026-08-28, option 3) — `SETS` itself does not change; verify the category list against a week of live triage regardless.**

## 7. Triage guidance

Score 5 for methodology with real algorithmic or theoretical content and a plausible route to application — the causal-framework and sparse/low-rank clusters are the clearest cases. Score 4 for solid conventional methodological contributions. Score 3 for competent engineering applications with no reusable core.

Score 1–2 for benchmark-only metaheuristics per §3. This is the one place in this charter where a fast surface heuristic is licensed, because the pattern was near-universal in vetting and the `[animal-name-exception]` flag exists to catch the rare miss.

## 8. What changed in this pass

**Two label-derived changes, both marked in place** per `LABEL-USE-PROTOCOL.md` R6: the §2 property-not-result clause and the §3 applied-ML-systems exclusion. Both cleared R7's evidence floor with room to spare, both survived a re-check after this session's `SETS` routing fix moved 7 papers out of this domain's evidence pool — none of the 7 touched either clause's supporting evidence, since all seven carried a `q-bio.*` tag that the property clause's definition already excluded, and none were part of either clause's counted set. Full audit in `EVAL-01-FINDINGS.md` §4A and `PASS-4-DRAFTS.md` §4.

**Everything from pass 3 otherwise stands unchanged:** in-scope as criteria rather than canon instances, the metaheuristic rule as content rather than nomenclature, "too theoretical" as a flag rather than an exclusion.

**§6's category list changed in code, not by ruling.** `compbio_mechanism` now routes first in `SETS` (a q-bio cross-list beats `cs.LG`), and `math.NA` was added here. Both are routing corrections, not scope decisions — see `arxiv_pull.py`'s `SETS` comment and `EVAL-01-FINDINGS.md` §4A for why the old order was silently misrouting protein and sequence papers to this charter instead of `compbio_mechanism`'s.

**The firehose question from pass 3 is still open and this pass does not touch it.** `cs.LG` alone still runs to several hundred submissions a day against a cap of 10, and the three options below are unchanged:

1. **Narrow the categories.** `math.OC` plus `cs.NE` is much closer to what this charter actually describes; `cs.LG` and `stat.ML` are where general ML lives and most of it fails §1's routing test anyway. *Costed against the labelled set in `EVAL-01-FINDINGS.md`'s companion analysis: this retains only 11 of 76 admitted papers, and `cs.NE` contributed 0 of 180 labelled papers despite being assumed load-bearing here.*
2. **Require a cross-list.** Admit `cs.LG`/`stat.ML` only when cross-listed to `math.OC`, `q-bio.*`, or each other. *Retains roughly 4 of ~30 `cs.LG`/`stat.ML` admits — essentially none of the pure-`cs.LG` admits evidenced in §2 above carry any such cross-list, which is exactly what this option would discard.*
3. **Accept the backlog as a ranked queue** and reinterpret the cap as "top 10 by score today." *Retains all admissions; costs a reinterpretation of what the cap means, which `daily-ingest.md` would need to say explicitly.*

Still your call — this is a volume-and-cost decision about your time and the daily spend, not a scope judgment. Option 3 is the one I'd take, given invariant 9 prices recall over precision roughly 3:1 and options 1–2 spend 85%+ of current admissions to buy throughput control.

**Decided 2026-08-28: option 3.** `SETS` stays as listed above, unchanged. `daily-ingest.md` §3 now carries an explicit exception documenting that this domain's cap is a permanent ranked cutoff, not a temporary throughput control, so a standing backlog here is not itself a signal to tighten the charter.
