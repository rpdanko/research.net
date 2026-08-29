# triage batch 3/5 — domain: compbio_methods

Charter: `charters/compbio_methods.md` — read it first, it is authoritative.

## In scope — 25 exemplars from the canon

- **For most large underdetermined systems of linear equations the minimal 𝓁<sub>1</sub>‐norm solution is also the sparsest solution** (2006) — IN SCOPE: add a one-line reason
- **Global Optimization with Polynomials and the Problem of Moments** (2001) — IN SCOPE: add a one-line reason
- **Proximal Algorithms** (2014) — IN SCOPE: add a one-line reason
- **Tensor Rank and the Ill-Posedness of the Best Low-Rank Approximation Problem** (2008) — IN SCOPE: add a one-line reason
- **** (2012) — IN SCOPE: add a one-line reason
- **The Book of Why: The New Science of Cause and Effect** (2018) — IN SCOPE: add a one-line reason
- **Discovering faster matrix multiplication algorithms with reinforcement learning** (2022) — IN SCOPE: add a one-line reason
- **Understanding Machine Learning: From Theory To Algorithms** (2015) — IN SCOPE: add a one-line reason
- **Gradient descent finds global minima of deep neural networks** (2019) — IN SCOPE: add a one-line reason
- **Parameterized Complexity** (2002) — IN SCOPE: add a one-line reason
- **The particle swarm - explosion, stability, and convergence in a multidimensional complex space** (2002) — IN SCOPE: add a one-line reason
- **Computational Complexity: A Modern Approach** (2009) — IN SCOPE: add a one-line reason
- **Sparse Solution of Underdetermined Systems of Linear Equations by Stagewise Orthogonal Matching Pursuit** (2012) — IN SCOPE: add a one-line reason
- **Kolmogorov-Arnold Networks Meet Science** (2025) — IN SCOPE: add a one-line reason
- **Hyperparameter optimization: Foundations, algorithms, best practices, and open challenges** (2023) — IN SCOPE: add a one-line reason
- **A Grassmann manifold handbook: basic geometry and computational aspects** (2024) — IN SCOPE: add a one-line reason
- **Deep Learning with Limited Numerical Precision** (2015) — IN SCOPE: add a one-line reason
- **Guaranteed Matrix Completion via Non-Convex Factorization** (2016) — IN SCOPE: add a one-line reason
- **Thinking Like a Vertex** (2015) — IN SCOPE: add a one-line reason
- **Higher-order organization of complex networks** (2016) — IN SCOPE: add a one-line reason
- **Parallel coordinate descent methods for big data optimization** (2015) — IN SCOPE: add a one-line reason
- **Ecient Sparse Matrix-Vector Multiplication on CUDA** (2008) — IN SCOPE: add a one-line reason
- **On Ideal Lattices and Learning with Errors over Rings** (2013) — IN SCOPE: add a one-line reason
- **Simultaneously Structured Models With Application to Sparse and Low-Rank Matrices** (2015) — IN SCOPE: add a one-line reason
- **iPiano: Inertial Proximal Algorithm for Nonconvex Optimization** (2014) — IN SCOPE: add a one-line reason

## Out of scope — near misses

_Highly cited and topically adjacent. These are the traps._

- **Sequential Optimization and Reliability Assessment Method for Efficient Probabilistic Design** (2004) — OUT: Engineering deisgn paper
- **Hybrid Analysis Method for Reliability-Based Design Optimization** (2003) — OUT: Design optimization
- **A fast and elitist multiobjective genetic algorithm: NSGA-II** (2002) — OUT: I don't work on evolutionary biology
- **Statistical physics of vehicular traffic and some related systems** (2000) — OUT: Seems very specific to vehicle traffic
- **The strong perfect graph theorem** (2006) — OUT: Seems like too specific and theoretical a result
- **Most Tensor Problems Are NP-Hard** (2013) — OUT: Seems like a theoretical paper that doesn't assist practical problem solving too much.


## Abstracts

Each carries a `band` computed before you saw it, the `threshold` that band
implies, and the titles of its nearest canon neighbours. Score on merit first,
then apply the threshold.

```json
[
  {
    "arxiv_id": "2406.01756",
    "title": "On the completeness of several fortification-interdiction games in the Polynomial Hierarchy",
    "abstract": "Fortification-interdiction games are tri-level adversarial games where two opponents act in succession to protect, disrupt and simply use an infrastructure for a specific purpose. Many such games have been formulated and tackled in the literature through specific algorithmic methods, however very few investigations exist on the completeness of such fortification problems in order to locate them rigorously in the polynomial hierarchy. We clarify the completeness status of several well-known fortification problems, such as the Tri-level Interdiction Knapsack Problem with unit fortification and attack weights, the Max-flow Interdiction Problem and Shortest Path Interdiction Problem with Fortification, the Multi-level Critical Node Problem with unit weights, as well as a well-studied electric grid defence planning problem. For all of these problems, we prove their completeness either for the $\\Sigma^p_2$ or the $\\Sigma^p_3$ class of the polynomial hierarchy. We also prove that the Multi-level Fortification-Interdiction Knapsack Problem with an arbitrary number of protection and interdiction rounds and unit fortification and attack weights is complete for any level of the polynomial hierarchy, therefore providing a useful basis for further attempts at proving the completeness of protection-interdiction games at any level of said hierarchy.",
    "categories": "cs.CC cs.GT math.OC",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Optimal Inapproximability Results for MAX\u2010CUT and Other 2\u2010Variable CSPs?",
      "Reducibility Among Combinatorial Problems",
      "Submodular Function Maximization via the Multilinear Relaxation and Contention Resolution Schemes"
    ]
  },
  {
    "arxiv_id": "2606.16454",
    "title": "SDS-LoRA: Overcoming Anisotropic Gradient Scaling in Low-Rank Adaptation",
    "abstract": "Low-Rank Adaptation (LoRA) enables efficient adaptation of large pretrained models to downstream tasks by parameterizing weight updates with low-rank matrices. In this paper, we investigate the limitations of the LoRA parameterization from a geometric perspective. Specifically, we show that when a full fine-tuning gradient is backpropagated to the low-rank matrices, it undergoes anisotropic scaling driven by their singular values. We argue that this phenomenon is undesirable because it distorts the full fine-tuning gradient by skewing it toward dominant singular directions while suppressing others. Our analyses demonstrate that anisotropic gradient scaling reduces the effective rank of the low-rank matrices' gradients and fails to provide the best possible alignment between the full fine-tuning gradient and its low-rank approximation in LoRA for arbitrary gradients, thereby exacerbating the gap to full fine-tuning. To address these limitations, we propose a new low-rank parameterization, SDS-LoRA, which Structurally Decouples Singular values from the backward pass. Our method ensures that the full fine-tuning gradient backpropagates only through the orthonormal bases of the low-rank matrices' subspaces, independent of their scales. Convergence analysis demonstrates that while LoRA's convergence rate degrades with the condition number of the low-rank matrices, that of SDS-LoRA remains independent of it. Experimental results across natural language and vision benchmarks show th",
    "categories": "cs.LG cs.AI",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Nonconvex Optimization Meets Low-Rank Matrix Factorization: An Overview",
      "Gradient descent finds global minima of deep neural networks",
      "Subspace Iteration Randomization and Singular Value Problems"
    ]
  },
  {
    "arxiv_id": "2604.16878",
    "title": "OC-Distill: Ontology-aware Contrastive Learning with Cross-Modal Distillation for ICU Risk Prediction",
    "abstract": "Early prediction of severe clinical deterioration and remaining length of stay can enable timely intervention and better resource allocation in high-acuity settings such as the ICU. This has driven the development of machine learning models that leverage continuous streams of vital signs and other physiological signals for real-time risk prediction. Despite their promise, existing methods have important limitations. Contrastive pretraining treats all patients as equally strong negatives, failing to capture clinically meaningful similarity between patients with related diagnoses. Meanwhile, downstream fine-tuning typically ignores complementary modalities such as clinical notes, which provide rich contextual information unavailable in physiological signals alone. To address these challenges, we propose OC-Distill, a two-stage framework that leverages multimodal supervision during training while requiring only vital signs at inference. In the first stage, we introduce an ontology-aware contrastive objective that exploits the ICD hierarchy to quantify patient similarity and learn clinically grounded representations. In the second stage, we fine-tune the pretrained encoder via cross-modal knowledge distillation, transferring complementary information from clinical notes into the model. Across multiple ICU prediction tasks on MIMIC, OC-Distill demonstrates improved label efficiency and achieves state-of-the-art performance among methods that use only vital signs at inference.",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A Topological Loss Function for Deep-Learning Based Image Segmentation Using Persistent Homology",
      "TopologyNet: Topology based deep convolutional and multi-task neural networks for biomolecular property predictions",
      "Topological data analysis for discovery in preclinical spinal cord injury and traumatic brain injury"
    ]
  },
  {
    "arxiv_id": "2608.04180",
    "title": "A Comparative Study of Feature Selection Methods for EHR Diagnosis Codes in Opioid Use Disorder Prediction",
    "abstract": "Feature selection is a critical step in electronic health record (EHR)-based predictive modeling, where input variables are often high-dimensional, sparse, noisy, and redundant. Large feature sets not only increase computational burden and overfitting risk, but also make model interpretation difficult, leading to limited usefulness in clinical settings. In this study, we focus on diagnosis-related features and compare five feature selection paradigms for opioid use disorder (OUD) prediction: recurrence enrichment, NTK-motivated early gradient sensitivity, LightGBM-SHAP, Elastic Net, and large language model (LLM)-guided semantic selection. We use a unified preprocessing and evaluation framework and assess each method by downstream predictive performance, resampling stability, and representation of infrequent diagnosis codes. Our results demonstrate that performance improves with larger feature budgets with diminishing returns beyond a moderate size. NTK sensitivity provides the best overall balance of accuracy and stability, and LLM-guided selection contributes complementary clinically meaningful signals despite lower standalone performance.",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A hybrid multi-objective optimization approach with NSGA-II for feature selection",
      "An Interior-Point Method for Large-Scale l 1 -Regularized Logistic Regression",
      "Differential Evolution-Based Feature Selection: A Niching-Based Multiobjective Approach"
    ]
  },
  {
    "arxiv_id": "2601.03123",
    "title": "Gradient descent reliably finds depth- and gate-optimal circuits for generic unitaries",
    "abstract": "When the gate set has continuous parameters, synthesizing a unitary operator as a quantum circuit is, in principle, always possible using exact methods. However, efficiently finding depth- and gate-minimal circuits remains a major challenge. The landscape is very different for compiled unitaries, which arise from programming and typically have short circuits, as compared with generic unitaries, which use all parameters and typically require circuits of maximal size. Previous approaches based on random combinatorial search indicate a low success rate even when the circuit ansatz is nominally adequately parameterized, motivating the use of heavily overparameterized circuits. In this work, we present a gradient-based optimization framework that enables the synthesis of depth- and gate-optimal circuits for generic unitaries without overparameterization, even under restricted hardware connectivity. We prescribe parameter-optimal circuit skeletons and eliminate the need for random combinatorial search. We further show that the poor performance of earlier random-search approaches can be attributed to the inadvertent selection of parameter-deficient circuit topologies. By systematically avoiding such skeletons, our approach achieves reliable convergence while maintaining parameter efficiency.",
    "categories": "quant-ph cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Simulating Quantum Computation by Contracting Tensor Networks",
      "KANQAS: Kolmogorov-Arnold Network for Quantum Architecture Search",
      "General Framework for Randomized Benchmarking"
    ]
  },
  {
    "arxiv_id": "2608.18008",
    "title": "Policy-Invariant Reward Shaping from LLM Feedback: A Framework for Hybrid RL Agents",
    "abstract": "Combining large language models with reinforcement learning is increasingly explored, yet the theoretical status of LLM-derived reward signals is often left implicit. We formalize the hybrid LLM-planner and RL-controller architecture as a Goal-Augmented Markov Decision Process and show that when the LLM per-state progress score is used as a bounded potential function, the resulting shaping term preserves the optimal policy set even when the LLM scores are inaccurate. This guarantee is stronger than what general LLM-as-reward approaches provide. We verify the result numerically on a small MDP under four potential configurations, including an adversarial one scaled to twenty times the base reward magnitude.",
    "categories": "cs.LG cs.AI",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Distributional Soft Actor-Critic With Three Refinements",
      "DSAC: Distributional Soft Actor-Critic for Risk-Sensitive Reinforcement Learning",
      "Evolutionary Reinforcement Learning: A Survey"
    ]
  },
  {
    "arxiv_id": "2608.16005",
    "title": "Retrieval-guided Twin Fusion with Similarity-aware Contrast for Molecule-Text Alignment",
    "abstract": "This paper studies the problem of molecule-text alignment, which aims to project molecules and their textual descriptions into a joint latent space for downstream tasks including molecule search and molecular property prediction. Previous approaches typically combine graph structure mining with contrastive learning to enhance joint representation learning. However, they typically neglect fine-grained semantic relationships between substructures and texts, leading to suboptimal performance on downstream tasks. Towards this end, we propose a novel approach named Retrieval-guided Twin Fusion with Similarity-aware Contrast (RISEN) for molecule-text alignment. The core idea of RISEN is to construct a latent twin molecule for each substructure with cross-modal retrieval for semantic enhancement. In particular, for each substructure query, we retrieve relevant textual descriptions and sample several molecules that share similar descriptions of substructures. Then, we aggregate their representations via attention pooling for a twin latent representation, which would be further fused with the original substructure for representation enrichment. In addition, we measure the similarity across substructures and texts, which would further guide cross-modal contrastive learning with soft thresholding. Extensive experiments on benchmark datasets validate the superiority of the proposed RISEN in comparison with existing baselines.",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Computer-aided multi-objective optimization in small molecule discovery",
      "TopologyNet: Topology based deep convolutional and multi-task neural networks for biomolecular property predictions",
      "Evolutionary optimization of model merging recipes"
    ]
  },
  {
    "arxiv_id": "2601.19175",
    "title": "A Scalable Inter-edge Correlation Modeling in CopulaGNN for Link Sign Prediction",
    "abstract": "Link sign prediction on a signed graph is a task to determine whether the relationship represented by an edge is positive or negative. Since the presence of negative edges violates the graph homophily assumption that adjacent nodes are similar, regular graph methods have not been applicable without auxiliary structures to handle them. We aim to directly model the latent statistical dependency among edges with the Gaussian copula and its corresponding correlation matrix, extending CopulaGNN (Ma et al., 2021). However, a naive modeling of edge-edge relations is computationally intractable even for a graph with moderate scale. To address this, we propose to 1) represent the correlation matrix as a Gramian of edge embeddings, significantly reducing the number of parameters, and 2) reformulate the conditional probability distribution to dramatically reduce the inference cost. We theoretically verify scalability of our method by proving its linear convergence. Also, our extensive experiments demonstrate that it achieves significantly faster convergence than baselines, maintaining competitive prediction performance to the state-of-the-art models.",
    "categories": "cs.LG cs.AI cs.IR cs.SI",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Random Walks on Simplicial Complexes and the Normalized Hodge 1-Laplacian",
      "Kernel-Based Reconstruction of Graph Signals",
      "Fastest Mixing Markov Chain on a Graph"
    ]
  },
  {
    "arxiv_id": "2608.08440",
    "title": "MGMCL: Multi-Granularity Manifold Contrastive Learning With Neural ODEs for Cross-Subject EEG Emotion Recognition",
    "abstract": "Cross-subject electroencephalogram (EEG)-based emotion recognition remains challenging due to substantial inter-individual variability and discrete formulation that overlooks affective continuity. Existing methods operate in Euclidean space and focus on marginal distribution alignment, failing to preserve the semantic structure of emotions across subjects. This article proposes MGMCL, reconceptualizing emotion recognition as learning continuous representations on symmetric positive definite (SPD) Riemannian manifolds. The frame?work introduces multi-granularity manifold contrastive learning at instance, emotion, and trajectory levels while preserving semantic ordering. Neural ordinary differential equations on manifolds model continuous emotion dynamics. Cross-subject generalization employs Gromov-Wasserstein manifold alignment. Weakly-supervised learning enables continuous valence-arousal-dominance prediction from discrete labels. Extensive experiments on three public datasets demonstrate state-of-the-art performance: 91.23% accuracy on SEED, 73.82% on SEED-IV, and 76.38% on DEAP, achieving consistent improvements of 1.89%, 1.66%, and 1.28% over previous best methods, respectively.",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Vector diffusion maps and the connection Laplacian",
      "Tensor Networks for Dimensionality Reduction and Large-scale Optimization: Part 1 Low-Rank Tensor Decompositions",
      "Laplacian Eigenmaps for Dimensionality Reduction and Data Representation"
    ]
  },
  {
    "arxiv_id": "2510.21805",
    "title": "DiffGRM: Diffusion-based Generative Recommendation Model",
    "abstract": "Generative recommendation (GR) is an emerging paradigm that represents each item via a tokenizer as an n-digit semantic ID (SID) and predicts the next item by autoregressively generating its SID conditioned on the user's history. However, two structural properties of SIDs make ARMs ill-suited. First, intra-item consistency: the n digits jointly specify one item, yet the left-to-right causality trains each digit only under its prefix and blocks bidirectional cross-digit evidence, collapsing supervision to a single causal path. Second, inter-digit heterogeneity: digits differ in semantic granularity and predictability, while the uniform next-token objective assigns equal weight to all digits, overtraining easy digits and undertraining hard digits. To address these two issues, we propose DiffGRM, a diffusion-based GR model that replaces the autoregressive decoder with a masked discrete diffusion model (MDM), thereby enabling bidirectional context and any-order parallel generation of SID digits for recommendation. Specifically, we tailor DiffGRM in three aspects: (1) tokenization with Parallel Semantic Encoding (PSE) to decouple digits and balance per-digit information; (2) training with On-policy Coherent Noising (OCN) that prioritizes uncertain digits via coherent masking to concentrate supervision on high-value signals; and (3) inference with Confidence-guided Parallel Denoising (CPD) that fills higher-confidence digits first and generates diverse Top-K candidates. Experiments",
    "categories": "cs.IR cs.AI cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Opportunities and challenges of diffusion models for generative AI",
      "Generative artificial intelligence: a historical perspective",
      "A Nonnegative Latent Factor Model for Large-Scale Sparse Matrices in Recommender Systems via Alternating Direction Method"
    ]
  },
  {
    "arxiv_id": "2607.19305",
    "title": "Riemannian Deep Learning: Modules, Networks, and Geometries",
    "abstract": "Deep neural networks on manifold-valued representations have attracted growing interest, but many basic components remain tied to specific manifolds, rely on Euclidean approximations, or require costly and numerically fragile geometric operations. This thesis develops a unified framework for Riemannian deep learning from three complementary perspectives: reusable neural modules, manifold-specific network architectures, and the design of underlying geometries. It generalizes batch normalization from Euclidean spaces and individual manifolds to broad classes of Lie groups and gyrogroups, and extends multinomial logistic regression from Euclidean space to SPD manifolds and then to general Riemannian manifolds. It further develops neural networks for several important geometric representations, including an unconstrained model of hyperbolic space, Busemann-based hyperbolic learning, and full-rank correlation matrices. Finally, it introduces adaptive and computationally efficient Riemannian metrics on SPD manifolds, including learnable Log-Euclidean geometries and fast, stable Cholesky-based geometries. The proposed methods are supported by theoretical analysis and validated through numerical experiments and applications in vision, signal processing, graph learning, and genomics.",
    "categories": "cs.LG cs.AI math.DG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A Grassmann manifold handbook: basic geometry and computational aspects",
      "A Brief Introduction to Manifold Optimization",
      "Hessian eigenmaps: Locally linear embedding techniques for high-dimensional data"
    ]
  },
  {
    "arxiv_id": "2602.10576",
    "title": "LLM-Based Scientific Equation Discovery via Physics-Informed Token-Regularized Policy Optimization",
    "abstract": "Symbolic regression aims to distill mathematical equations from observational data. Recent approaches have successfully leveraged Large Language Models (LLMs) to generate equation hypotheses, capitalizing on their vast pre-trained scientific priors. However, existing frameworks predominantly treat the LLM as a static generator, relying on prompt-level guidance to steer exploration. This paradigm fails to update the model's internal representations based on search feedback, often yielding physically inconsistent or mathematically redundant expressions. In this work, we propose PiT-PO (Physics-informed Token-regularized Policy Optimization), a unified framework that evolves the LLM into an adaptive generator via reinforcement learning. Central to PiT-PO is a dual-constraint mechanism that rigorously enforces hierarchical physical validity while simultaneously applying fine-grained, token-level penalties to suppress redundant structures. Consequently, PiT-PO aligns LLM to produce equations that are both scientifically consistent and structurally parsimonious. Empirically, PiT-PO achieves state-of-the-art performance on standard benchmarks and successfully discovers novel turbulence models for challenging fluid dynamics problems. We also demonstrate that PiT-PO empowers small-scale models to outperform closed-source giants, democratizing access to high-performance scientific discovery.",
    "categories": "cs.LG cs.AI",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Reinforcement learning in robotics: A survey",
      "Evolutionary optimization of model merging recipes",
      "Gaussian Processes for Data-Efficient Learning in Robotics and Control"
    ]
  },
  {
    "arxiv_id": "2608.17524",
    "title": "Evaluating RL Explainability Methods by How Much They Help Fix Bugs in Agents",
    "abstract": "This preliminary paper outlines a planned evaluation benchmark for Explainable Reinforcement Learning (XRL) methods. Current evaluations rely on functionally-grounded metrics like faithfulness and compactness, and on human-grounded proxies like subjective ratings or prediction accuracy. We suggest evaluating XRL methods by how effectively their generated explanations help to diagnose and fix malfunctioning reinforcement learning (RL) agents. We propose EvalXRL, a benchmark in which a Large Language Model (LLM) coding agent uses different XRL methods to diagnose a held-out malfunction in an RL agent, and then repair it. Our proposed benchmark iterates across (environment $\\times$ malfunction $\\times$ XRL method) tuples and uses the reward signal of the RL agents to form a final score for each XRL method. The coding agent may use the method interactively: invoke the XRL method, process its output, form new hypotheses on what is broken, and invoke the method again with parameters adjusted for testing these hypotheses. This closed-loop structure may be described as a simplified version of the scientific method. Some XRL methods provide self-evaluations that follow this pattern; we propose the first head-to-head comparison of multiple XRL methods in closed-loop usage.",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Distributional Soft Actor-Critic With Three Refinements",
      "Evolutionary Reinforcement Learning: A Survey",
      "Reinforcement learning in robotics: A survey"
    ]
  },
  {
    "arxiv_id": "2602.05541",
    "title": "Reducing the Complexity of Matrix Multiplication by Quantum Computing",
    "abstract": "Matrix multiplication is a fundamental operation in compute-intensive tasks and a key component of modern quantum acceleration frameworks. Here we present a quantum matrix multiplication algorithm based on quantum kernels (QKMM), achieving an elementary gate complexity of \\(O(N^2\\log_2N)\\), with amplitude encoding overhead explicitly included and without assuming a QRAM oracle. This scaling is asymptotically lower than that of the best-known classical matrix multiplication algorithm \\(O(N^{2.371339})\\). Building upon QKMM, we establish a family of quantum linear algebra operators, including Quantum Vector Inner Product (V${\\scriptstyle 2}$V), Quantum Vector-Matrix Multiplication (V${\\scriptstyle 2}$M), QKMM (M${\\scriptstyle 2}$M), Quantum One-to-Many Matrix Multiplication(O${\\scriptstyle 2}$M) and Quantum Sequential Matrix Multiplication (SMM), providing a unified framework from vector operations to parallel and sequential matrix transformations. Through noiseless simulations, realistic noise modelling and experiments on a superconducting quantum processor, we systematically characterize the numerical accuracy, resource requirements and hardware execution limits of this operator framework. Furthermore, we integrate SMM into deep neural-network inference, enabling intermediate features to propagate coherently across layers without repeated measurement and re-encoding. These results establish a pathway from quantum circuit-level algorithm design to end-to-end coherent computati",
    "categories": "quant-ph cs.CC cs.LG",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Efficient phase-factor evaluation in quantum signal processing",
      "Quantum Circuits That Can Be Simulated Classically in Polynomial Time",
      "Quantum algorithms for algebraic problems"
    ]
  },
  {
    "arxiv_id": "2608.15388",
    "title": "Look Before You Lift: Visual and Quantitative Diagnostics for Topological Deep Learning",
    "abstract": "Topological deep learning (TDL) methods rely on lifting raw data into higher-order discrete domains such as simplicial complexes, cell complexes, and hypergraphs. In practice, this lifting step is often treated as a black box: practitioners select a lifting and then tune architectures, with limited visibility into whether the induced higher-order connectivity is meaningful for the downstream task. To address this missing diagnostic layer, we propose a visualization technique called TopoExplorer that leverages the strictly augmented Hasse graph form of topological datasets for exploratory data analysis. For the first time, practitioners can easily visualize the incidence- and adjacency-based neighborhoods that define the lifted dataset, as well as read off key graph metrics that describe its structural and feature landscape. Via an extensive set of experiments across many datasets and liftings, we show that several of these metrics correlate with downstream model performance, suggesting they can help inform TDL preprocessing design. Our perspective reframes the TDL workflow from lift-train to lift-look-design-train, enabling more principled, interpretable, and efficient model development. TopoExplorer is hosted at https://topoexplorer.pagekite.me, and its source code is available at github.com/geometric-intelligence/topoexplorer.",
    "categories": "cs.LG",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Topological deep learning: a review of an emerging paradigm",
      "Topological Data Analysis in Graph Neural Networks: Surveys and Perspectives",
      "A Survey of Topological Machine Learning Methods"
    ]
  },
  {
    "arxiv_id": "2509.18530",
    "title": "Re-uploading quantum data: a universal function approximator for quantum inputs",
    "abstract": "Quantum data re-uploading has proved powerful for classical inputs, where repeatedly encoding features into a small circuit yields universal function approximation. Extending this idea to quantum inputs remains underexplored, as the information contained in a quantum state is not directly accessible in classical form. We propose and analyze a quantum data re-uploading architecture in which a qubit interacts sequentially with fresh copies of an arbitrary input state. The circuit can approximate any bounded continuous function using only one ancilla qubit and single-qubit measurements. By alternating entangling unitaries with mid-circuit resets of the input register, the architecture realizes a discrete cascade of completely positive and trace-preserving maps, analogous to collision models in open quantum system dynamics. Our framework provides a qubit-efficient and expressive approach to designing quantum machine learning models that operate directly on quantum data.",
    "categories": "quant-ph cs.LG",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Quantum machine learning: A comprehensive review of integrating AI with quantum computing for computational advancements",
      "Prediction by linear regression on a quantum computer",
      "Shadows of quantum machine learning"
    ]
  },
  {
    "arxiv_id": "2608.20315",
    "title": "Explainable Transformer Models for Clinical Prediction Tasks on Structured Electronic Health Records",
    "abstract": "Predictive models over structured electronic health records (EHRs) remain central to machine learning for healthcare, but few have jointly emphasized quantitative laboratory information and interpretability with respect to input medical events. We present BERT-LER, a BERT-style model for coded EHR timelines pretrained and fine-tuned from a de-identified EHR dataset of 75 million patients, that encodes laboratory test results as discrete tokens while retaining graded information through percentile-based binning, paired with Integrated Gradients for token-level attributions grounded in the input EHR sequence. We benchmark our approach on the public EHRShot benchmark suite and on an asthma severity progression study based on real-world data. This addresses a methodological gap in EHR foundation-style modeling by unifying laboratory value representation and explainability in a single framework, while assessing whether both predictive performance and explanations generalize beyond standard clinical prediction tasks. Across EHRShot and asthma tasks, BERT-LER achieves predictive performance that is competitive with, and on laboratory-related tasks often exceeds, publicly available benchmark models, and provides attributions that align with clinically known risk factors. Our architecture and explainability approach can be applied to many therapeutic areas and prediction tasks using language models trained on structured EHRs.",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A Survey on Kolmogorov-Arnold Network",
      "Cellpose 2.0: how to train your own model",
      "An overview of large AI models and their applications"
    ]
  },
  {
    "arxiv_id": "2608.03836",
    "title": "Resume Means Resume: A Machine-Checked Conformance Contract for Checkpoint, Interrupt, and Resume Semantics in Workflow Persistence Layers",
    "abstract": "A framework that persists execution state so a run can be interrupted, survive a crash, and continue must decide what a resume means for effects that already happened. Five widely deployed agent workflow frameworks answer differently, none exposes a machine-checkable contract, and measured behavior violates even the fragments they state. The RESUME CONTRACT states six properties over the persistence API (prefix continuation, effect exactly-once, fork determinism, checkpoint validity, consume-once, recovery determinism), plus fork-intent and liveness obligations. A TLA+ model checks a reference semantics exhaustively, unchanged at scaled bounds (7.4 million states), and the reference conjunction is additionally TLAPS-proved unbounded (196 obligations); a 39-cell fault matrix and two companion modules yield the separating models independence requires. A deterministic, LLM-free harness measures them at pinned releases. LangGraph 1.2.9 durably records a second resume value and never consults it, persists schema-invalid state silently, and re-executes durably recorded work after a real SIGKILL: exactly-once across interrupts, at-least-once across crashes, on one API. CrewAI 1.15.2 re-executes completed effect-bearing methods against its written claim; pydantic-graph 1.x cannot resume after a mid-node crash; no two probed frameworks share a conformance profile. Consume-once holds sequentially and fails under concurrent delivery: k processes resuming one parked interrupt fire the ga",
    "categories": "cs.LG cs.DC cs.LO cs.SE",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Algorithm 799: revolve",
      "1 Zigzag Codes: MDS Array Codes with Optimal Rebuilding",
      "Computer Model Validation with Functional Output"
    ]
  },
  {
    "arxiv_id": "2601.20883",
    "title": "VoxMorph: Scalable Zero-shot Voice Identity Morphing via Disentangled Embeddings",
    "abstract": "Morphing techniques generate artificial biometric samples that combine features from multiple individuals, allowing each contributor to be verified against a single enrolled template. While extensively studied in face recognition, this vulnerability remains largely unexplored in voice biometrics. Prior work on voice morphing is computationally expensive, non-scalable, and limited to acoustically similar identity pairs, constraining practical deployment. Moreover, existing sound-morphing methods target audio textures, music, or environmental sounds and are not transferable to voice identity manipulation. We propose VoxMorph, a zero-shot framework that produces high-fidelity voice morphs from as little as five seconds of audio per subject without model retraining. Our method disentangles vocal traits into prosody and timbre embeddings, enabling fine-grained interpolation of speaking style and identity. These embeddings are fused via Spherical Linear Interpolation (Slerp) and synthesized using an autoregressive language model coupled with a Conditional Flow Matching network. VoxMorph achieves state-of-the-art performance, delivering a 2.6x gain in audio quality, a 73% reduction in intelligibility errors, and a 67.8% morphing attack success rate on automated speaker verification systems under strict security thresholds. This work establishes a practical and scalable paradigm for voice morphing with significant implications for biometric security. The code and dataset are availabl",
    "categories": "cs.SD cs.CR cs.LG eess.AS",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Privacy-Preserving Machine Learning With Fully Homomorphic Encryption for Deep Neural Network",
      "Evolutionary optimization of model merging recipes",
      "Cellpose 2.0: how to train your own model"
    ]
  },
  {
    "arxiv_id": "2608.19861",
    "title": "PolicyGuide: From Guarding One Action to Guiding the Whole Workflow for Policy-Compliant LLM Agents",
    "abstract": "Customer-service LLM agents must follow organizational policy when acting on a user's behalf. Compliance failures arise from either forbidden actions, such as granting an ineligible change, or omitted procedural requirements, such as identification or confirmation. Runtime safeguards can intervene on risky actions, but action-local checks do not guide an agent through a multi-step procedure. Workflow-following systems support prescribed process execution, but primarily target workflow completion rather than safeguarding agent behavior. PolicyGuide instead compiles each domain policy into a workflow graph and invokes a proactive verifier at user-turn boundaries. From persisted graph state, the verifier reconciles open requests and returns step-specific remediation along a policy-compliant path. Across the $\\tau^2$-bench airline, retail, and telecom domains with a GPT-5.4 agent and verifier, PolicyGuide raises mean $\\mathrm{Pass}^4$ from $0.42$ to $0.62$, with the largest gain on telecom ($0.19$ to $0.61$), the most workflow-structured domain. The same workflows transfer to Claude Sonnet 4.6 and Gemini 2.5 Pro agents. Complementary evaluations find the lowest observed attack-success rate under adversarial users and the strongest procedural compliance in an author-designed workflow-level validation.",
    "categories": "cs.AI cs.CL cs.LG",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Eligibility Traces for Off-Policy Policy Evaluation",
      "Trustworthy AI",
      "White-Box Traceable Ciphertext-Policy Attribute-Based Encryption Supporting Any Monotone Access Structures"
    ]
  },
  {
    "arxiv_id": "2608.21075",
    "title": "AudioWorldSim: Realistic Binaural Audio Datasets For World Models",
    "abstract": "This technical report presents AudioWorldSim, an open-source platform designed to generate realistic binaural audio datasets and advance research in audio-based machine learning, particularly world models. Built as a custom extension of Meta's SoundSpaces 2.0 platform, AudioWorldSim leverages their comprehensive acoustics framework, but focuses on the automatic rollout of random agent navigations, as well as implements crucial fixes to how continuous sound is composed. AudioWorldSim is made publicly available to the research community at https://github.com/Luizerko/AudioWorldSim to facilitate reproducibility.",
    "categories": "cs.SD cs.LG",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Human-artificial interaction in the age of agentic AI: a system-theoretical approach",
      "Using machine learning as a surrogate model for agent-based simulations",
      "Gaussian Processes for Machine Learning (GPML) Toolbox"
    ]
  },
  {
    "arxiv_id": "2608.16956",
    "title": "The Price of Thinking: Reasoning Effort as a Model-Specific API Contract",
    "abstract": "API buyers purchase a dated contract, not a model name alone: the contract includes the requested and served model, reasoning-effort term or its omission, output rail, service product, prompt, and price schedule. We study the reasoning-effort term through a registered paired contrast of Sonnet 5 with explicit high effort against the same model with effort omitted, using 30 AIME 2026 items and five calls per item. Every paid attempt was assigned one frozen terminal category, and inference resampled items while retaining their repeated calls. Mean delivered cost was \\$0.01031 per call higher under the explicit-high contract than under the omitted contract [+\\$0.00204, +\\$0.01974]. The corresponding accuracy contrast was +0.0133 [-0.0267, +0.0467]; we did not detect an accuracy difference, and the interval permits a gain of up to 4.67 percentage points that this design cannot rule out. Cost per correct answer was \\$0.08665 under the high-effort contract and \\$0.07662 under the omitted contract, as registered point estimates. A dated contract census, Models-API metadata, and preregistered raw-response probes further documented model-specific omission semantics, including within a provider; claims remained at documentation grade when raw structure was indeterminate. The request registry, parser, terminal taxonomy, statistical plan, and analysis pipeline were frozen before outcomes were examined; the resulting claims are bounded to the model, task, and collection date studied.",
    "categories": "cs.AI cs.CL cs.CY cs.LG",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Generalised free energy and active inference",
      "Issues in Deciding Whether to Use Multifidelity Surrogates",
      "Toward a method of selecting among computational models of cognition."
    ]
  },
  {
    "arxiv_id": "2608.14435",
    "title": "Style or Signature? Artist-Disjoint Evaluation of Style Classification in Frozen Vision Embeddings",
    "abstract": "Frozen image embeddings from models such as CLIP are increasingly used to classify paintings by art-historical style, with high reported accuracy. We ask whether this accuracy reflects an understanding of style or the recognition of individual artists. Standard evaluation uses random splits in which works by the same artist appear on both sides, so a classifier can succeed by recognising the painter rather than the movement. We re-evaluate style classification under an artist-disjoint protocol, holding out every artist in turn so that no work is ever classified using other works by its own painter. On a balanced dataset of 320 paintings across four twentieth-century movements, 5-NN style accuracy falls from 0.87 to 0.77 under this protocol, and the drop is sharply uneven. Impressionism and Cubism barely move, while Surrealism falls twenty points. The pattern holds across four image encoders, including a vision-only self-supervised model, which places the effect in visual structure rather than language. Where an encoder captures genuine shared form, individual artists are barely recognisable yet style is robust, while Surrealism shows the opposite. We argue that artist-disjoint evaluation is necessary to measure stylistic understanding in frozen embeddings.",
    "categories": "cs.CV cs.LG",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "A CATALOG OF VISUAL-LIKE MORPHOLOGIES IN THE 5 CANDELS FIELDS USING DEEP LEARNING",
      "Formal Theory of Creativity, Fun, and Intrinsic Motivation (1990\u20132010)",
      "Generative artificial intelligence: a historical perspective"
    ]
  },
  {
    "arxiv_id": "2608.02829",
    "title": "Wiring Beats Blending: What Transfers Between Transformer Sizes -- and What Doesn't",
    "abstract": "Model families are typically trained size by size, each from scratch. Can a pretrained large model instead be converted into a smaller sibling? We characterize the 1.4B->410M conversion in Pythia end to end. Representations align strongly across sizes (ridge R^2=0.84) while parameters align weakly. Dense weight projection is functionally destructive, and a bit-exact control shows this is not an assembly artifact: basis mixing breaks rotary, per-head, GELU, and LayerNorm structure. After the best-fit linear operator, weight residuals are statistically indistinguishable from noise under shuffle controls. Conversion value therefore lives in initialization. In matched-budget continued pre-training we decompose conversion into two independent levers: least-squares compensation (function lever, best zero-shot) and variance-preserving rescale (dynamics lever, best endpoints). Compensation is a token-efficient, low-budget win rather than a universal one. At 30M tokens it beats the strongest subcloning variant on both a width-reduced pair (84.0 +/- 1.8 vs. 89.7 +/- 3.7, 3/3 seeds) and a held-out depth-reduced pair (109.3 vs. 117.9, 3/3 seeds), reaching a given quality with fewer tokens. At a 33x larger budget the two converge to parity (40.0 vs. 40.0), both far ahead of from-scratch, which transfer initialization always beats: by up to 18x at low budget, with the margin narrowing at convergence and at the largest scale. We also map the method's boundary. At about 5x the donor scale (6",
    "categories": "cs.LG cs.AI cs.CL",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Deep Learning with Limited Numerical Precision",
      "Energy-Efficient Approximate Multiplication for Digital Signal Processing and Classification Applications",
      "Beating Floating Point at its Own Game: Posit Arithmetic"
    ]
  },
  {
    "arxiv_id": "2608.11034",
    "title": "SCOUT: Symmetric Consensus Outlier Detection for Failure Localization in LLM Pre-Training",
    "abstract": "In LLM pre-training, synchronization propagates rank-local stalls, slowdowns, and numerical errors into job-wide symptoms, obscuring their origin. Existing diagnosis often relies on in-process monitors that cannot report after the trainer blocks or terminates, or on post-mortem logs that preserve only synchronized symptoms; offline health tests lose the workload and operating conditions that triggered the failure. We present SCOUT, a unified runtime failure-localization framework built on one design principle: identify outliers through strict-majority consensus among equivalent replicas. SCOUT aligns replica progress, timing, and numerical evidence, then uses its Consensus Collective Communication (C3) abstraction to identify ranks whose compact signatures disagree with their peers. An out-of-band CPU observer remains responsive when training hangs, whereas in-situ replay exercises recurring stragglers and silent data corruption (SDC) beside the live job with its model state, kernels, allocations, communication path, and thermal and memory pressure present. Collective fingerprints expose rank-local protocol divergence. Clean replay coverage certifies checkpoint numerical integrity, preventing recovery from selecting state corrupted by SDC. SCOUT integrates with PyTorch, TorchTitan, Megatron-Core, and DeepSpeed without training-loop or framework-source modifications. SCOUT is open source at https://github.com/LMResiliency/lm-resiliency.",
    "categories": "cs.DC cs.LG",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Algorithm 799: revolve",
      "Solving Multitask Optimization Problems With Adaptive Knowledge Transfer via Anomaly Detection",
      "Early Fault-Tolerant Quantum Computing"
    ]
  }
]
```

## Output

One JSON object per abstract, one per line, no prose. Every input `arxiv_id`
appears exactly once. Include `ambiguous` even when false.
