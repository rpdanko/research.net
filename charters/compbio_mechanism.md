# Computational biology — structure and mechanism — knowledge base charter

> **DRAFT, third pass.** Renamed from `compbio_genomics.md` to `compbio_mechanism.md` — see §8. The one open decision this charter used to carry — population genetics and phylogenetics theory — has been resolved: **admitted**. See §2, §5, §6, and §8.

## 1. Purpose

This KB covers **computational modelling of biological structure and mechanism**: how molecules fold, how pathways signal, how cell states are inferred. It is where the **unnamed mathematics** lives — computational biology routinely reinvents, under biological vocabulary, objects that probability and statistics have studied properly, and recovering those is the highest-value work in this system. Most bridges are expected to originate here.

Two framing notes before the scope lists.

**The old name was wrong, and it's fixed now.** `compbio_genomics` was inherited from the OpenAlex topic split at harvest time. What belongs here was never genomics in the sequencing sense — quite the opposite; see §3. The domain is now named for what it actually holds.

**This charter is more personal than the other three, deliberately.** Your strike reasons in this domain were first-person statements of research fit — "I do not do sequencing work," "I work at the molecular level," "I work on molecular biological processes and pathways" — rather than judgments about methodological quality. That is legitimate: a charter defines what a KB is *for*, and this one is for your research. But it means the exclusions here are about fit, not merit, and a future reader should not mistake them for claims about the field. §8 flags the one place that distinction has real consequences.

## 2. In scope

Criteria, with vetting-confirmed examples. The criterion admits; the example illustrates.

- **Protein structure and interaction modelling** — structure prediction, protein language models, biomolecular interaction and complex prediction, protein design.
- **Mechanism, pathway, and signalling modelling** — computational accounts of how a biological process actually works. You flagged this repeatedly as the centre of your interest.
- **Cell-state and single-cell inference** — extracting states, trajectories, or structure from per-cell measurements.
- **Machine learning applied to biological processes where the biology is structurally load-bearing** to the method — not a biological dataset fed to a general architecture.
- **Stochastic and dynamical models of biological systems** — reaction networks, parameter identifiability, models where the biological constraint shapes the mathematics.
- **Game-theoretic and economic models of biological cooperation** — you called this a high-value cross-disciplinary intersection. It fits no other criterion cleanly and is admitted by name; see §5.
- **Population-genetics and phylogenetics theory** — coalescent theory, Wright-Fisher and Moran processes, branching processes, Markov models on trees, and similar. Admitted this pass; see §8 for the reasoning and §5 for the flag that still applies to every instance. Distinct from phylogenetics *software*, which stays out of scope under §3 regardless.

## 3. Out of scope

- **Sequence data-processing tooling** — aligners, variant callers, assemblers, QC and preprocessing pipelines, annotation tools, format utilities. The largest struck category in vetting by a wide margin, and struck on research fit rather than quality. Stated as *data-processing tooling* rather than *genomics* so the criterion is about what the paper contributes, not what organism it mentions.
- **Software and package announcements** generally, regardless of biological application. This is what catches phylogenetics tooling (iTOL, RAxML, TNT, MrBayes, jModelTest, PAUP\*, MAFFT, OrthoFinder, and similar) even though popgen/phylogenetics *theory* is admitted per §2 — the theory/tooling line, not the field, is what §2 vs. here turns on. Note how much of the above this criterion already covers on its own — see §8.
- **Disease- or condition-specific findings** (cancer, Alzheimer's, diabetes, depression, COVID) unless the contribution is a general-purpose modelling method rather than a result about that condition.
- **Dataset, cohort, and resource releases** without a methodological contribution.
- **Laboratory and wet-bench protocol papers.**

## 4. Mathematical object normalization — SHARED, identical across all four charters

1. **Name at the level of theory, not notation.**
2. **Use the canonical name; variants go in `aliases`.**
3. **Record the role, not just the presence.**
4. **Include objects the result relies on**, even if unforegrounded.
5. **Exclude objects merely cited** as related work.
6. **Flag unnamed usage** with `named_in_paper: false` plus `evidence`. **In this domain this is the main event, not an edge case.**
7. **Three to seven objects.**

## 5. Ambiguous — flag, don't silently reject

Score normally against §7, and also emit `"ambiguous": true`. Separate axis from `wildcard`; not for ordinary adjacency, which is a 3.

- **`[ml-bio-benchmark-load-bearing]`** — ML/DL evaluated on biological data where it is genuinely unclear whether the biology is load-bearing or incidental. The §2 criterion names the test; plenty of real papers sit on the line rather than either side of it.
- **`[econ-bio-cooperation]`** — game-theoretic and economic models of biological cooperation. Admitted by name rather than by criterion, so flag every instance and keep the exception visible rather than letting it ossify unexamined.
- **`[tooling-buried-methodology]`** — a data-processing tool paper with real algorithmic novelty underneath the tooling framing. The §3 rule is a well-earned prior, but a rule that blunt will occasionally catch a genuine method. If the abstract makes a specific theoretical claim beyond "faster/better," flag before striking.
- **`[popgen-phylo-theory]`** — **population-genetics and phylogenetics theory, as distinct from phylogenetics software.** Admitted per §2/§8. The flag stays — not because the decision is open anymore, but because this is a domain you can't personally evaluate as readily as the rest of the KB (§1's framing note), so every instance should stay visible for your own periodic sanity-check rather than disappearing into the card pile once admitted.

## 6. arXiv categories

`q-bio.BM`, `q-bio.QM`, `q-bio.MN`, `q-bio.SC`, and `q-bio.PE`.

`q-bio.PE` (populations and evolution) is **restored this pass** — see §8. Expect it to be the noisiest category here: most of its daily volume is phylogenetics tooling and applied population-genetics results with no theoretical contribution, both out of scope under §3. The §7 bar and the `[popgen-phylo-theory]` flag have to do real filtering work on this one category specifically. `q-bio.GN` remains omitted: it is where sequence-processing work lives, which §3 excludes on content grounds independent of this decision.

## 7. Triage guidance

Score 5 for a method with identifiable mathematical structure applied to protein structure, mechanism, or cell-state inference — **especially unnamed structure recovered from biological vocabulary**, which is what this KB exists for. Score 4 for solid methodological contributions in those areas using conventional machinery. Score 3 for good biology with standard tools.

Score 1–2 for work whose contribution is producing, aligning, annotating, or storing sequence data, however well executed.

## 8. What changed in this pass, and the decision that's now resolved

**Reframed around what you do, not what you reject.** The second pass opened with the sequencing exclusion and derived scope from it; the domain's most-cited candidates were nearly all tooling, so the negative rule was the loudest thing in the vetting data. But a charter that leads with an exclusion specifies a hole rather than a subject. §1 and §2 now lead with molecular mechanism, structure, and pathway modelling — the things your keep-reasons actually describe — and the sequencing rule sits in §3 where an exclusion belongs.

**The sequencing exclusion is now about tooling, not topic.** Most papers struck under "I do not do sequencing work" were software announcements: SAMtools, BWA, Trimmomatic, minimap2, Kraken2, HTSeq, fastp, TopHat2, and so on. Those are caught by the software-announcement criterion on their own. Restating the rule as *data-processing tooling* keeps the same practical effect while no longer excluding, by accident, a paper that happens to mention sequence data while contributing something else.

*Corrected 2026-08-28 (was "nearly every paper"; see `compbio_mechanism.rewrite-prep.md` §A1).* Not all of them are software. The sequencing cluster also holds genome-result and resource papers — *Initial sequencing and analysis of the human genome*, *A global reference for human genetic variation*, *The Draft Genome of Ciona intestinalis* — which the software-announcement criterion does **not** reach. Those are caught by §3's *dataset, cohort, and resource releases* bullet instead. The reframe still holds; it is just carried by two §3 criteria rather than one, and both have to stay for the effect to survive.

**Resolved: population genetics and phylogenetics theory is admitted.** The second pass excluded these outright, citing your "I do not work on evolutionary biology" and "I do not work on phylogenetics" strikes. The third pass held it as a flag rather than deciding, because the evidence pointed both ways:

*For excluding:* you said it plainly, more than once, and this charter is explicitly about research fit.

*For admitting:* almost every phylogenetics paper you struck was a package paper — iTOL v3 through v6, RAxML, TNT, MrBayes, jModelTest, PAUP\*, MAFFT, OrthoFinder — struck by the software criterion regardless of field. The number of *theory* papers in that literature you rejected on evolutionary-biology grounds is small. Meanwhile the first-draft `compbio.md` charter called population genetics and phylogenetics "the most mathematically structured subfield, prioritize it," and this KB's stated purpose is recovering unnamed mathematics. Coalescent theory, Wright-Fisher and Moran processes, branching processes, and Markov models on trees are the richest vein of exactly that in all of computational biology, and they connect directly to `probability`'s stochastic-processes scope. If bridges mostly originate here, this is the seam most likely to produce them.

The sharpest way to put the tension: the charters exist to serve **intersection-finding**, and bridge-finder reads the concordance, not your reading list. A domain can hold objects you would never read a paper about and still be the reason a bridge exists.

**Your call: admit, keeping tooling struck.** `q-bio.PE` restored (§6), the theory criterion added to §2, the `[popgen-phylo-theory]` flag in §5 kept (now as an ongoing visibility mechanism rather than an open question — this is a subfield you can't evaluate as readily as the rest of the KB, per §1, so keep the flag active going forward rather than letting admitted instances disappear into the card pile unreviewed). Phylogenetics and popgen *tooling* stays excluded exactly as before, via §3's software-announcement rule — admitting the theory did not touch that.

**Also:** `q-bio.SC` (subcellular processes) added — it directly matches the pathway and mechanism scope and its omission looked like an oversight rather than a decision.

**Renamed this pass:** `compbio_genomics` → `compbio_mechanism`, per this section's earlier recommendation (the other candidate was `compbio_structure`). Propagated through `domain_map.yaml`, `card_schema.json`, `arxiv_pull.py` (which also picked up the `q-bio.SC` addition above, previously undone in code), both curator agents, `daily-ingest.md`, and the vetting worksheet.
