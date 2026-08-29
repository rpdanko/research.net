# triage batch 1/1 — domain: compbio_mechanism

Charter: `charters/compbio_mechanism.md` — read it first, it is authoritative.

## In scope — 21 exemplars from the canon

- **Highly accurate protein structure prediction with AlphaFold** (2021) — IN SCOPE: add a one-line reason
- **Tissue-based map of the human proteome** (2015) — IN SCOPE: add a one-line reason
- **Accurate structure prediction of biomolecular interactions with AlphaFold 3** (2024) — IN SCOPE: add a one-line reason
- **Squeeze-and-Excitation Networks** (2019) — IN SCOPE: add a one-line reason
- **Comprehensive molecular portraits of human breast tumours** (2012) — IN SCOPE: add a one-line reason
- **Epigenetic Regulations of GABAergic Neurotransmission: Relevance for Neurological Disorders and Epigenetic Therapy** (2016) — IN SCOPE: add a one-line reason
- **Alzheimer's Disease: Genes, Proteins, and Therapy** (2001) — IN SCOPE: add a one-line reason
- **Evolutionary-scale prediction of atomic-level protein structure with a language model** (2023) — IN SCOPE: add a one-line reason
- **Natural products in drug discovery: advances and opportunities** (2021) — IN SCOPE: add a one-line reason
- **Genetic effects on gene expression across human tissues** (2017) — IN SCOPE: add a one-line reason
- **Opportunities and obstacles for deep learning in biology and medicine** (2018) — IN SCOPE: add a one-line reason
- **Tensor Decomposition for Signal Processing and Machine Learning** (2017) — IN SCOPE: add a one-line reason
- **Integrated analysis of multimodal single-cell data** (2021) — IN SCOPE: add a one-line reason
- **E(3)-equivariant graph neural networks for data-efficient and accurate interatomic potentials** (2022) — IN SCOPE: add a one-line reason
- **Prisoner’s dilemma game model Based on historical strategy information** (2023) — IN SCOPE: add a one-line reason
- **Gene set enrichment analysis: A knowledge-based approach for interpreting genome-wide expression profiles** (2005) — IN SCOPE: add a one-line reason
- **Macrophages in immunoregulation and therapeutics** (2023) — IN SCOPE: add a one-line reason
- **Targeted Branching for the Maximum Independent Set Problem Using Graph Neural Networks** (2024) — IN SCOPE: add a one-line reason
- **De novo design of protein structure and function with RFdiffusion** (2023) — IN SCOPE: add a one-line reason
- **In silico prediction of protein-protein interactions in human macrophages** (2014) — IN SCOPE: add a one-line reason
- **The Reactome pathway Knowledgebase** (2015) — IN SCOPE: add a one-line reason

## Out of scope — near misses

_Highly cited and topically adjacent. These are the traps._

- **Strengthening the Reporting of Observational Studies in Epidemiology Using Mendelian Randomization** (2021) — OUT: I do not work in epidemiology but this sounds pretty interesting
- **Correlation Coefficients: Appropriate Use and Interpretation** (2018) — OUT: Too rudimentary to be helpful
- **Strengthening the reporting of observational studies in epidemiology using mendelian randomisation (STROBE-MR): explanation and elaboration** (2021) — OUT: Specific to epidemiology
- **Why 90% of clinical drug development fails and how to improve it?** (2022) — OUT: Specific to drug development
- **Tensor-Train Decomposition** (2011) — OUT: Included in the genomics canon
- **RAxML version 8: a tool for phylogenetic analysis and post-analysis of large phylogenies** (2014) — OUT: Methodology paper specific to application. Could be useful if I venture into these waters but it shouldn't be load-bearing.


## Abstracts

Each carries a `band` computed before you saw it, the `threshold` that band
implies, and the titles of its nearest canon neighbours. Score on merit first,
then apply the threshold.

```json
[
  {
    "arxiv_id": "2408.14242",
    "title": "A statistical-mechanical framework for mechanically adaptive cytoskeletal organization",
    "abstract": "Living cells continuously remodel their cytoskeleton in response to mechanical cues. Although these responses have been extensively documented, it remains unclear why continuous changes in the mechanical environment give rise to distinct intracellular architectures rather than gradual structural variation. Here, we introduce a statistical-mechanical framework in which alternative cytoskeletal organizations are represented as ensembles of microscopic configurations, allowing configurational entropy to compete with mechanically dependent interaction energies. Rather than reproducing the full molecular complexity of the cytoskeleton, the model asks which features of mechanically adaptive organization emerge from this minimal physical description. The framework predicts three successive structural transitions corresponding to stress fiber formation, alignment, and lateral aggregation. When these transitions are placed on a common cellular-tension axis that increases with substrate stiffness, the predicted sequence is consistent with our measurements of correlation length and anisotropy in senescent fibroblasts. The preservation of this stiffness-dependent sequence despite altered cellular physiology suggests that the observed ordering reflects a robust physical principle rather than a cell-state-specific phenomenon. Together, these results establish a statistical-mechanical framework for understanding how continuous mechanical cues bias the statistical selection of distinct cytos",
    "categories": "q-bio.CB q-bio.MN q-bio.SC",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "The MARTINI Coarse-Grained Force Field: Extension to Proteins",
      "Calculating Structures and Free Energies of Complex Molecules:\u2009 Combining Molecular Mechanics and Continuum Models",
      "Atomic-Level Characterization of the Structural Dynamics of Proteins"
    ]
  },
  {
    "arxiv_id": "2608.14757",
    "title": "KHiM-Mamba: Injecting Pathology Knowledge into Mamba via Hidden-State Modulation for Whole Slide Image Analysis",
    "abstract": "Whole slide image analysis is commonly formulated as multiple instance learning (MIL), where instance features are contextually updated and aggregated into a slide representation, a process we term slide encoding dynamics. Recently, selective state-space models (SSM) have emerged as promising MIL architectures due to their long-sequence modeling capability and linear complexity. However, existing SSM-based MIL methods rely solely on visual features during MIL. Meanwhile, in large-scale WSIs, where sparse diagnostically decisive regions are surrounded by abundant irrelevant information, such purely vision-driven selective dynamics can misallocate state updates and readouts, causing the evolving SSM state to accumulate task-irrelevant evidence and dilute critical diagnostic cues over long scan trajectories. In this work, we propose the Knowledge-Aware Hidden-State Modulation architecture (KHiM-Mamba), which innovatively regulates Mamba's core selective state-space mechanism with explicit knowledge priors, steering slide encoding dynamics toward diagnostically meaningful evidence accumulation. Specifically, we redesign the original SSM layer to perform knowledge modulation operations during the evolution of hidden states, thereby guiding what visual evidence is accumulated and retrieved from the hidden state at each encoding step. Furthermore, we additionally introduce a local-adaptive vocabulary retrieval module that uses large language models to assign each patch fine-grained,",
    "categories": "eess.IV cs.CV q-bio.QM",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A multimodal generative AI copilot for human pathology",
      "Deep Patient: An Unsupervised Representation to Predict the Future of Patients from the Electronic Health Records",
      "Squeeze-and-Excitation Networks"
    ]
  }
]
```

## Output

One JSON object per abstract, one per line, no prose. Every input `arxiv_id`
appears exactly once. Include `ambiguous` even when false.
