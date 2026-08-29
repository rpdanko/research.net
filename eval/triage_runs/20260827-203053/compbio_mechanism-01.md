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
    "arxiv_id": "2608.12090",
    "title": "Task- and dataset-specific information in protein language models",
    "abstract": "Protein language models (PLMs) have transferred the latest advances from natural language processing to computational biology. These models, trained on large corpora of protein sequence data, are widely used to translate amino acid sequences into latent-space embeddings, ready for use in diverse downstream tasks (DTs). By a common consensus, embeddings from the model's last layer are used, and the model's internal behavior remains poorly understood. We analyzed 13 PLMs across 15 DTs from 11 datasets to investigate the informativeness of embeddings created in intermediate PLM layers. We trained probe models on embeddings from each layer, compared their performance, and computed characteristics of the latent spaces they span to estimate the information they contain, and found that the last layers of PLMs rarely contained embeddings that led to the best results on downstream tasks. Furthermore, we identified a connection between DTs and the distribution across PLMs' layers of the relevant information to predict that task. For example, similarity between the pre-training objective and the objective of predicting properties of individual residues leads to a steady increase in understanding of such tasks across the layers of PLMs. On the other hand, for whole-protein tasks, we observe that the dataset, rather than the task itself, defines PLMs' ability to perform well on a DT. Embeddings from shallow layers of PLMs perform better for datasets that contain deep mutational scan (DMS) data, while datasets containing diverse natural proteins find most useful embeddings in the models' deeper layers. Additionally, we discover that the performance of PLMs drops significantly when tasks are introduced for artificial proteins.",
    "categories": "cs.LG q-bio.BM",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences",
      "ProteinBERT: a universal deep-learning model of protein sequence and function",
      "ProtGPT2 is a deep unsupervised language model for protein design"
    ]
  },
  {
    "arxiv_id": "2608.06430",
    "title": "MiGHT-EHR: A Multi-task Graph Transformer for Heterogeneous Temporal Electronic Health Records",
    "abstract": "Learning from Electronic Health Records (EHRs) has gained significant attention due to its potential to improve clinical prediction. However, effective learning remains challenging because EHRs encode heterogeneous, temporally ordered clinical interactions. In particular, EHRs contain: (i) heterogeneous clinical entities, including patients, visits, diagnoses, prescriptions, and procedures, together with their heterogeneous interactions, (ii) longitudinal patient trajectories across hospital visits and (iii) shared statistical dependencies across related clinical prediction tasks. Existing EHR learning methods capture only a subset of these properties. To bridge this gap, we propose Multi-task Graph transformer for Heterogeneous Temporal EHRs (MiGHT-EHR), which jointly models all three within a unified representation learning method. MiGHT-EHR constructs a heterogeneous graph from EHRs in which nodes represent clinical entities and edges connect statistically associated entities identified via normalized point-wise mutual information. Across MIMIC-III and MIMIC-IV datasets, MiGHT-EHR outperforms state-of-the-art methods on average across four tasks: drug recommendation, prediction of length-of-stay, mortality, and readmission, with particularly strong improvements in mortality and readmission prediction. Furthermore, a post-hoc analysis of the learned representations reveals that patient neighborhoods are organized by clinical outcomes, salient medical concepts are recoverable as linear directions in the representation space, and task probabilities are well calibrated. Collectively, these findings demonstrate that MiGHT-EHR representations support diverse prediction tasks while preserving clinically interpretable structure.",
    "categories": "cs.LG q-bio.QM",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Deep EHR: A Survey of Recent Advances in Deep Learning Techniques for Electronic Health Record (EHR) Analysis",
      "Deep Patient: An Unsupervised Representation to Predict the Future of Patients from the Electronic Health Records",
      "Deep learning for healthcare: review, opportunities and challenges"
    ]
  },
  {
    "arxiv_id": "2506.07459",
    "title": "ProteinZero: Self-Improving Protein Generation via Online Reinforcement Learning",
    "abstract": "Protein generative models have shown remarkable promise in protein design, yet their success rates remain constrained by reliance on curated sequence-structure datasets and by misalignment between supervised objectives and real design goals. We present ProteinZero, an online reinforcement learning framework for inverse folding models that enables scalable, automated, and continuous self-improvement with computationally efficient feedback. ProteinZero employs a reward pipeline that combines structural guidance from ESMFold with a novel self-derived ddG predictor, providing stable multi-objective signals while avoiding the prohibitive cost of physics-based methods. To ensure robustness in online RL, we further introduce a novel embedding-level diversity regularizer that mitigates mode collapse and promotes functionally meaningful sequence variation. Within a general RL formulation balancing multi-reward optimization, KL-divergence from a reference model, and diversity regularization, ProteinZero achieves robust improvements across designability, stability, recovery, and diversity. On the CATH-4.3 benchmark, it consistently outperforms state-of-the-art baselines including ProteinMPNN, ESM-IF, and InstructPLM, reducing design failure rates by 36-48% and achieving success rates above 90% across diverse folds. Importantly, a complete RL run can be executed on a single 8 X GPU node within three days, including reward computation and data generation. These results indicate that efficient online RL fine-tuning can complement supervised pretraining by allowing protein generative models to evolve continuously from their own outputs and optimize multiple design objectives without labeled data, opening new possibilities for exploring the vast protein design space. Full source code and model checkpoints will be released upon publication.",
    "categories": "cs.LG q-bio.QM",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Scalable emulation of protein equilibrium ensembles with generative deep learning",
      "OpenFold: retraining AlphaFold2 yields new insights into its learning mechanisms and capacity for generalization",
      "De novo design of protein structure and function with RFdiffusion"
    ]
  },
  {
    "arxiv_id": "2408.14242",
    "title": "A statistical-mechanical framework for mechanically adaptive cytoskeletal organization",
    "abstract": "Living cells continuously remodel their cytoskeleton in response to mechanical cues. Although these responses have been extensively documented, it remains unclear why continuous changes in the mechanical environment give rise to distinct intracellular architectures rather than gradual structural variation. Here, we introduce a statistical-mechanical framework in which alternative cytoskeletal organizations are represented as ensembles of microscopic configurations, allowing configurational entropy to compete with mechanically dependent interaction energies. Rather than reproducing the full molecular complexity of the cytoskeleton, the model asks which features of mechanically adaptive organization emerge from this minimal physical description. The framework predicts three successive structural transitions corresponding to stress fiber formation, alignment, and lateral aggregation. When these transitions are placed on a common cellular-tension axis that increases with substrate stiffness, the predicted sequence is consistent with our measurements of correlation length and anisotropy in senescent fibroblasts. The preservation of this stiffness-dependent sequence despite altered cellular physiology suggests that the observed ordering reflects a robust physical principle rather than a cell-state-specific phenomenon. Together, these results establish a statistical-mechanical framework for understanding how continuous mechanical cues bias the statistical selection of distinct cytoskeletal architectures.",
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
    "arxiv_id": "2608.14245",
    "title": "Body size predicts how long ant workers live - but not how they age or how they die from heat",
    "abstract": "In social insects, mortality risk comprises distinct components that may not share the same predictors: lifespan duration, senescence trajectory, and thermal vulnerability. We tested these three axes in 18 Australian ant species using paired field-laboratory survival assays (2,363 cohort-day observations; 1,148 workers). Body size predicted duration (Cox HR = 0.67, p = 0.002), while colony size (p = 0.60) and the size x temperature interaction (p = 0.72) showed no detectable moderating effect. A weak but significant size x foraging-rate interaction was detected (LRT p = 0.014), suggesting that intrinsic physiology remains the most parsimonious explanation for the main size-longevity pattern, although ecological context may contribute. Senescence trajectory was associated with circadian niche rather than size: it was steepest in matinal species (Kruskal-Wallis p = 0.009; matinal vs. crepuscular p = 0.002) and was uncorrelated with body mass (Spearman p = 0.32). Thermal hazard plateaued above 20 degrees C (Delta AIC = -38; p < 0.001), with elevated thermal sensitivity in Rhytidoponera (Ectatomminae) above the plateau (5% per degree C, p = 0.015). Circadian regime and lineage identity, not body size, therefore emerge as the most climate-relevant axes, although they are strongly collinear (Cramer's V = 0.85). These results show that body size captures only one dimension of mortality risk and that size-based vulnerability indices may misrank taxa when senescence and thermal sensitivity are decoupled from body size.",
    "categories": "q-bio.PE cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "TOWARD A METABOLIC THEORY OF ECOLOGY",
      "Trade\u2010offs in evolutionary immunology: just what is the cost of immunity?",
      "DNA methylation GrimAge strongly predicts lifespan and healthspan"
    ]
  },
  {
    "arxiv_id": "2608.11475",
    "title": "Probing and steering biology across Boltz-1s trunk-diffusion boundary",
    "abstract": "AlphaFold3-class structure predictors pair a representational trunk, which processes sequence and context, with a diffusion module, which generates atomic coordinates. How biological information changes as it crosses this architectural boundary remains poorly understood. We analyze per-residue activations from the Pairformer trunk and diffusion module of Boltz-1 using linear probes, sparse autoencoders (SAEs), and causal interventions. From the trunk, both geometry (secondary structure, disorder) and sequence chemistry (amino-acid identity, signal peptides, disulfide-bond annotations) are linearly decodable. In the diffusion module, the two diverge. Secondary structure transfers essentially unchanged, whereas sequence chemistry is strongly attenuated. We then test whether decodable directions can steer the model, intervening on the final trunk single representation that conditions the diffusion module. Helix and coil directions change predicted structure dose-dependently against matched-norm random controls, but a beta-strand direction that is highly predictive (F1 =0.82) produces no measurable increase in strand content: linear decodability does not imply causal influence at the site we tested. The same probes also score markedly lower against sparse SwissProt annotations than against dense DSSP labels, because unannotated residues that the model gets right are charged as false positives; such scores are therefore lower bounds. Finally, supervised probes outscore single SAE features wherever a label already exists. We release the trained trunk and diffusion SAEs, Boltz-1 per-residue activations, and the analysis code.",
    "categories": "q-bio.QM cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Accurate structure prediction of biomolecular interactions with AlphaFold 3",
      "OpenFold: retraining AlphaFold2 yields new insights into its learning mechanisms and capacity for generalization",
      "Addendum: Accurate structure prediction of biomolecular interactions with AlphaFold 3"
    ]
  },
  {
    "arxiv_id": "2608.17381",
    "title": "Leveraging generative hallucination and biophysics-informed modeling for unified biomolecular sequence-structure co-design",
    "abstract": "Biomolecular design underpins applications from molecular recognition to therapeutics and synthetic biology, yet de novo interaction design remains challenging-especially for DNA/RNA, underexplored non-protein modalities with scarce, heterogeneous complex data and sharper geometric and chemical constraints. We introduce MCTH (Monte Carlo Tree Hallucination), an inference-only framework that casts all-atom sequence-structure co-design as uncertainty-aware planning over hallucinated states from pretrained folding and inverse-folding models, with optional biophysical control within the same decision loop. MCTH treats these models as frozen black-box operators and uses Monte Carlo Tree Search to allocate a fixed inference budget across competing design trajectories, incorporating model confidence and uncertainty, as well as cross-expert consensus/disagreement when multiple predictors are available. Across protein-RNA, protein-DNA, protein-protein, and protein-ligand design, matched-budget experiments show that adaptive search improves over simpler sampling and cycling strategies, while held-out AlphaFold3 and Chai-1 evaluations demonstrate transfer beyond the search-time oracle. MCTH provides a shared planning layer across modalities while allowing task-specific folding, inverse-folding, and biophysical modules, requiring no fine-tuning or backpropagation through component models.",
    "categories": "q-bio.QM cs.AI cs.LG q-bio.BM",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "A hierarchical approach to all\u2010atom protein loop prediction",
      "Modeling of loops in protein structures",
      "Generalized biomolecular modeling and design with RoseTTAFold All-Atom"
    ]
  },
  {
    "arxiv_id": "2506.14488",
    "title": "READ: A Retrieval-Alignment Diffusion Framework for Structure-based Drug Design",
    "abstract": "Structure-based drug design (SBDD) models are central to modern pharmaceutical research, enabling the rational exploration of protein-ligand interactions at atomic resolution. However, most existing approaches frame molecular generation as an isolated optimization or a one-to-one matching task, overlooking the shared binding patterns and intrinsic similarities among protein-ligand complexes. This fragmented perspective constrains their ability to capture the fundamental principles governing molecular recognition and binding specificity. Moreover, the limited availability of high-quality experimental data further hampers model generalization and real-world applicability. To address these challenges, we present READ, a retrieval-alignment molecular generation framework that conditions the generative process on small molecules targeting homologous proteins. Retrieved ligands are aligned with a diffusion model across multiple representational spaces and integrated as conditional guidance throughout successive stages of generation. Under a standardized docking-based evaluation protocol, READ achieves consistently strong performance against state-of-the-art SBDD methods. More importantly, it introduces a retrieval-alignment paradigm for structure-based molecular generation, offering a practical framework for early-stage computational hit generation while leaving prospective experimental validation as future work.",
    "categories": "q-bio.BM cs.LG",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Molecular Docking and Structure-Based Drug Design Strategies",
      "Computational approaches streamlining drug discovery",
      "The Art and Science of Molecular Docking"
    ]
  },
  {
    "arxiv_id": "2608.00697",
    "title": "Evolutionary Curriculum Learning Improves Biological Sequence Modeling",
    "abstract": "Variational autoencoders (VAEs) trained on multiple sequence alignments (MSAs) have emerged as powerful generative models for biological sequences, with applications ranging from disease variant prediction to functional RNA design. However, standard biological VAE training treats all sequences as exchangeable, ignoring the rich evolutionary structure that organizes homologous sequences from evolutionarily close to highly divergent. We propose Evolutionary Curriculum Learning (ECL), a training strategy that exploits this structure by progressively exposing the model to sequences of increasing evolutionary distance from sampled anchors, following a power-law expansion schedule. Applied to two architecturally distinct VAE models and two biological domains--protein variant effect prediction with EVE and RNA family sequence generation with RfamGen--ECL improves downstream task performance across five random seeds per configuration. Mean ClinVar classification AUROC rises from 0.981 to 0.989 for p53; for PTEN, ECL attains 1.000 in every seed whereas the baseline is unstable (mean 0.905, falling as low as 0.54). For RNA, ECL raises mean covariance-model bit scores on all three families tested and exceeds its seed-matched baseline in 12 of 15 training runs, though with only three families the effect cannot be established as significant at the family level. Ablation experiments show that progressively expanding the sampled sequences by evolutionary distance outperforms fixed-size neighborhood sampling in addition to uniform random sampling. Evolutionary distance is therefore a useful inductive bias for ordering the training curriculum in biological sequence modeling.",
    "categories": "cs.AI cs.LG q-bio.BM stat.ML",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Sequence modeling and design from molecular to genome scale with Evo",
      "Nucleotide Transformer: building and evaluating robust foundation models for human genomics",
      "Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences"
    ]
  },
  {
    "arxiv_id": "2608.14757",
    "title": "KHiM-Mamba: Injecting Pathology Knowledge into Mamba via Hidden-State Modulation for Whole Slide Image Analysis",
    "abstract": "Whole slide image analysis is commonly formulated as multiple instance learning (MIL), where instance features are contextually updated and aggregated into a slide representation, a process we term slide encoding dynamics. Recently, selective state-space models (SSM) have emerged as promising MIL architectures due to their long-sequence modeling capability and linear complexity. However, existing SSM-based MIL methods rely solely on visual features during MIL. Meanwhile, in large-scale WSIs, where sparse diagnostically decisive regions are surrounded by abundant irrelevant information, such purely vision-driven selective dynamics can misallocate state updates and readouts, causing the evolving SSM state to accumulate task-irrelevant evidence and dilute critical diagnostic cues over long scan trajectories. In this work, we propose the Knowledge-Aware Hidden-State Modulation architecture (KHiM-Mamba), which innovatively regulates Mamba's core selective state-space mechanism with explicit knowledge priors, steering slide encoding dynamics toward diagnostically meaningful evidence accumulation. Specifically, we redesign the original SSM layer to perform knowledge modulation operations during the evolution of hidden states, thereby guiding what visual evidence is accumulated and retrieved from the hidden state at each encoding step. Furthermore, we additionally introduce a local-adaptive vocabulary retrieval module that uses large language models to assign each patch fine-grained, tissue-specific semantic descriptions, enabling precise modulation across diverse tasks. Experiments on 11 public benchmarks across 4 tasks show that KHiM-Mamba consistently achieves state-of-the-art performance.",
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
