# triage batch 1/5 — domain: compbio_methods

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
    "arxiv_id": "2608.16609",
    "title": "A Splitting Framework for Composite Semimonotone Inclusions",
    "abstract": "We introduce a general framework for composite inclusion problems with affine constraints, covering both monotone and semimonotone regimes. The central idea is a new interpretation of the constrained inclusion through an operator-vector pair that separates the implicit inclusion from the affine constraint: the former is handled through possibly preconditioned resolvent evaluations, while the latter is handled through an explicit forward step in an auxiliary variable. This yields a single abstract iteration applicable to multioperator inclusions, linearly coupled inclusions, and block-separable inclusions with affine constraints. The freedom in choosing the operator-vector pair enables the systematic construction of problem-adapted splitting algorithms, including new schemes for several important problem classes. Exploiting the orthogonal decomposition induced by the constraint subspace, we develop a unified and streamlined convergence analysis and establish weak and strong convergence guarantees under semimonotonicity assumptions. When specialized to multioperator inclusions, the framework permits general bounded linear operator coefficients, rather than only scalar coefficients, and therefore accommodates preconditioned resolvents. The resulting schemes recover several existing methods while extending them to previously uncovered regimes, and in several important cases, require weaker assumptions and admit provably larger admissible parameter ranges.",
    "categories": "math.OC",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "A Monotone+Skew Splitting Model for Composite Monotone Inclusions in Duality",
      "A Forward-Backward Splitting Method for Monotone Inclusions Without Cocoercivity",
      "Solving the split feasibility problem without prior knowledge of matrix norms"
    ]
  },
  {
    "arxiv_id": "2608.09523",
    "title": "Generalized Convexity and Smoothness via Conjugate Duality: Optimization Theory for Deep Neural Networks",
    "abstract": "Deep neural network (DNN) training with stochastic gradient descent (SGD) and its variants achieves strong empirical performance, yet classical optimization theory does not fully explain this success. This limitation arises because conventional analyses rely on assumptions such as differentiability, convexity, or smoothness, which are often violated by DNN objectives. In this paper, we establish a unified optimization framework for DNN training by generalizing classical convexity and smoothness through Legendre functions and convex conjugation. Specifically, we introduce $\\mathcal{H}(\\psi)$-convexity and $\\mathcal{H}(\\Psi)$-smoothness, which unify convex and non-convex as well as smooth and non-smooth objectives within a single formalism and reveal a natural duality between generalized smoothness and convexity. Building on these generalized properties, we introduce generalized gradient descent (GD) and generalized SGD through convex conjugation. We theoretically prove that generalized GD admits an optimal learning rate of exactly $1$, and derive rigorous gradient-energy-based convergence rates for both proposed optimizers. We further reformulate DNN training as a composite optimization problem, demonstrating that its convergence relies on jointly reducing the gradient energy and controlling the induced norm of the network Jacobian. To characterize the practical influences of network architectures and training configurations, we introduce the gradient correlation factor and mo",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Gradient descent finds global minima of deep neural networks",
      "A Descent Lemma Beyond Lipschitz Gradient Continuity: First-Order Methods Revisited and Applications",
      "Basic Enhancement Strategies When Using Bayesian Optimization for Hyperparameter Tuning of Deep Neural Networks"
    ]
  },
  {
    "arxiv_id": "2603.14700",
    "title": "Design Space of Self--Consistent Electrostatic Machine Learning Interatomic Potentials",
    "abstract": "Machine learning interatomic potentials (MLIPs) have become widely used tools in atomistic simulations. For much of the history of this field, the most commonly employed architectures were based on short-ranged atomic energy contributions, and the assumption of locality still persists in many modern foundation models. While this approach has enabled efficient and accurate modelling for many use cases, it poses intrinsic limitations for systems where long-range electrostatics, charge transfer, or induced polarization play a central role. A growing body of work has proposed extensions that incorporate electrostatic effects, ranging from locally predicted atomic charges to self-consistent models. While these models have demonstrated success for specific examples, their underlying assumptions, and fundamental limitations are not yet well understood. In this work, we present a framework for treating electrostatics in MLIPs by viewing existing models as coarse-grained approximations to density functional theory (DFT). This perspective makes explicit the approximations involved, clarifies the physical meaning of the learned quantities, and reveals connections and equivalences between several previously proposed models. Using this formalism, we identify key design choices that define a broader design space of self-consistent electrostatic MLIPs. We implement salient points in this space using the MACE architecture and a shared representation of the charge density, enabling controlled",
    "categories": "physics.chem-ph cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Active phase discovery in heterogeneous catalysis via topology-guided sampling and machine learning",
      "Representability of algebraic topology for biomolecules in machine learning based scoring and virtual screening",
      "Machine learning-based inverse design methods considering data characteristics and design space size in materials design and manufacturing: a review"
    ]
  },
  {
    "arxiv_id": "2608.07828",
    "title": "The Rank-Collapse Principle for Quadratic Optimization",
    "abstract": "Quadratic optimization becomes hard as soon as either the matrix in the quadratic form has an unfavorable curvature or the feasible set is discrete, combinatorial, or otherwise nonconvex. A complementary phenomenon is also well known in the signal-processing and optimization communities: when the matrix in the quadratic form has small rank, some hard-looking quadratic programs admit exact polynomial-time algorithms for fixed rank. We study the common positive-semidefinite geometry behind this phenomenon. If $Q=BB^\\top$ is positive semidefinite, the objective depends on $x$ only through the rank-space shadow $y=B^\\top x$. Every optimal shadow $y^*$ uniquely maximizes the linear functional defined by its own direction and satisfies a quantitative quadratic margin. Thus nonlinear optimality collapses to a low-dimensional, self-generated linear exposure direction. We call this the rank-collapse principle. The principle alone does not imply a finite candidate set: efficient exact optimization additionally depends on the projected or active geometry of the feasible family. We organize this distinction through projected-shadow scattering and active-structure collapse, relate it explicitly to established zonotope, convex-combinatorial, edge-skeleton, projected-normal-fan, and fixed-rank sparse-PCA methods, and derive tie-safe consequences for binary and finite-phase vectors, cardinality constraints, matroid bases, and sparse PCA. We also give directional-stability and approximately l",
    "categories": "math.OC",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Low-Rank Optimization on the Cone of Positive Semidefinite Matrices",
      "A Spectral Bundle Method for Semidefinite Programming",
      "Semidefinite optimization"
    ]
  },
  {
    "arxiv_id": "2007.11761",
    "title": "Strong convergence of an inertial Tseng's extragradient algorithm for pseudomonotone variational inequalities with applications to optimal control problems",
    "abstract": "We investigate an inertial viscosity-type Tseng's extragradient algorithm with a new step size to solve pseudomonotone variational inequality problems in real Hilbert spaces. A strong convergence theorem of the algorithm is obtained without the prior information of the Lipschitz constant of the operator and also without any requirement of additional projections. Finally, several computational tests are carried out to demonstrate the reliability and benefits of the algorithm and compare it with the existing ones. Moreover, our algorithm is also applied to solve the variational inequality problem that appears in optimal control problems. The algorithm presented in this paper improves some known results in the literature.",
    "categories": "math.OC cs.NA math.NA",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Strong convergence of subgradient extragradient methods for the variational inequality problem in Hilbert space",
      "Extensions of Korpelevich's extragradient method for the variational inequality problem in Euclidean space",
      "A Hybrid Extragradient-Viscosity Method for Monotone Operators and Fixed Point Problems"
    ]
  },
  {
    "arxiv_id": "2410.05777",
    "title": "Integrated Encoding and Quantization to Enhance Quanvolutional Neural Networks",
    "abstract": "Image processing is one of the most promising applications for quantum machine learning (QML). Quanvolutional Neural Networks with non-trainable parameters are the preferred solution to run on current and near future quantum devices. The typical input preprocessing pipeline for quanvolutional layers comprises of four steps: optional input binary quantization, encoding classical data into quantum states, processing the data to obtain the final quantum states, decoding quantum states back to classical outputs. In this paper we propose two ways to enhance the efficiency of quanvolutional models. First, we propose a flexible data quantization approach with memoization, applicable to any encoding method. This allows us to increase the number of quantization levels to retain more information or lower them to reduce the amount of circuit executions. Second, we introduce a new integrated encoding strategy, which combines the encoding and processing steps in a single circuit. This method allows great flexibility on several architectural parameters (e.g., number of qubits, filter size, and circuit depth) making them adjustable to quantum hardware requirements. We compare our proposed integrated model with a classical convolutional neural network and the well-known rotational encoding method, on two different classification tasks. The results demonstrate that our proposed model encoding exhibits a comparable or superior performance to the other models while requiring fewer quantum resou",
    "categories": "quant-ph cs.AI cs.LG",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "KANQAS: Kolmogorov-Arnold Network for Quantum Architecture Search",
      "Quantum machine learning: A comprehensive review of integrating AI with quantum computing for computational advancements",
      "Shadows of quantum machine learning"
    ]
  },
  {
    "arxiv_id": "2608.12090",
    "title": "Task- and dataset-specific information in protein language models",
    "abstract": "Protein language models (PLMs) have transferred the latest advances from natural language processing to computational biology. These models, trained on large corpora of protein sequence data, are widely used to translate amino acid sequences into latent-space embeddings, ready for use in diverse downstream tasks (DTs). By a common consensus, embeddings from the model's last layer are used, and the model's internal behavior remains poorly understood. We analyzed 13 PLMs across 15 DTs from 11 datasets to investigate the informativeness of embeddings created in intermediate PLM layers. We trained probe models on embeddings from each layer, compared their performance, and computed characteristics of the latent spaces they span to estimate the information they contain, and found that the last layers of PLMs rarely contained embeddings that led to the best results on downstream tasks. Furthermore, we identified a connection between DTs and the distribution across PLMs' layers of the relevant information to predict that task. For example, similarity between the pre-training objective and the objective of predicting properties of individual residues leads to a steady increase in understanding of such tasks across the layers of PLMs. On the other hand, for whole-protein tasks, we observe that the dataset, rather than the task itself, defines PLMs' ability to perform well on a DT. Embeddings from shallow layers of PLMs perform better for datasets that contain deep mutational scan (DMS)",
    "categories": "cs.LG q-bio.BM",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Evolutionary optimization of model merging recipes",
      "Navigating the protein fitness landscape with Gaussian processes",
      "TopologyNet: Topology based deep convolutional and multi-task neural networks for biomolecular property predictions"
    ]
  },
  {
    "arxiv_id": "2606.02507",
    "title": "Towards Automated Discovery: A Review of Generative Models, Multimodal Learning and Closed-Loop Workflows in Inverse Materials Design",
    "abstract": "Inverse materials design is shifting materials discovery from forward prediction toward targeted proposal of candidates that satisfy objectives under physical constraints. Here, we review advances in generative crystal structure modeling, multimodal learning, and closed-loop design pipelines for crystalline solids. We survey how generators learn chemical-structural priors from databases to enable controllable sampling of periodic structures, comparing variational autoencoders, normalizing flows, autoregressive models, and diffusion models. Across these families, we examine where feasibility constraints and physical priors enter, from representations and training objectives to sampling-time guidance, screening, and relaxation. We also discuss multimodal learning combining crystal structures, thermodynamic and electronic information, microscopy, spectroscopy, processing context, and scientific text to construct materials representations. Inverse-design strategies integrating conditional generation with latent optimization, Bayesian optimization, reinforcement learning, and active learning are also examined. We highlight recurring failure modes, including surrogate exploitation, diversity collapse, distribution shift, and the stability-synthesizability gap, and outline evaluation based on validity, novelty, uniqueness, stability, and cost. To support credible claims, we define a nine-rung discovery-credibility ladder and propose a minimum reporting standard: declared matching to",
    "categories": "cond-mat.mtrl-sci cs.ET cs.LG physics.app-ph physics.comp-ph",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Machine learning-based inverse design methods considering data characteristics and design space size in materials design and manufacturing: a review",
      "Deep learning framework for material design space exploration using active transfer learning and data augmentation",
      "Bias free multiobjective active learning for materials design and discovery"
    ]
  },
  {
    "arxiv_id": "2412.17228",
    "title": "MatchMiner-AI: Open-source, Privacy-preserving Cancer Clinical Trial Matching using Artificial Intelligence",
    "abstract": "Background: Clinical trials are essential to advancing cancer treatments, but fewer than 10% of adults with cancer enroll in therapeutic trials. Open-source AI trial matching tools could democratize access to trial options. Methods: We created MatchMiner-AI, co-developed with practicing clinical oncologists and trained on synthetic electronic health record (EHR) data. It uses open-weight LLMs to summarize patient histories from unstructured EHR text and extract target populations from trial eligibility documents. Embedding and re-ranking models were distilled to retrieve and rank trial and patient suggestions. Multifaceted evaluation was performed, including retrospective quantification of distillation fidelity; applying a closed-source LLM as judge of patient summarization and matching; and evaluation of candidate matches by oncologists. Results: Across retrospective evaluations of distillation fidelity, the pipeline outperformed a baseline text-embedding model, improving mean average precision (MAP) at 20 from 0.44 (95% CI 0.44-0.45) to 0.95 (95% CI 0.95-0.96) for trial-enrolled patients and from 0.38 (95% CI 0.37-0.38) to 0.94 (95% CI 0.93-0.94) for patients who received standard of care therapies. In a 50-patient sample selected for comparison between MatchMiner-AI and a rules-based tumor genomic trial matching algorithm, MatchMiner-AI retrieved trials for all patients, as opposed to 19 patients (38%) who had tumor genomic data available. Among those 19 patients, 80% of 2",
    "categories": "cs.AI cs.LG",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Homomorphic Encryption for Machine Learning in Medicine and Bioinformatics",
      "An overview of large AI models and their applications",
      "Quantitative Toxicity Prediction Using Topology Based Multitask Deep Neural Networks"
    ]
  },
  {
    "arxiv_id": "2410.19208",
    "title": "Approximate Projections onto the Positive Semidefinite Cone Using Randomization",
    "abstract": "This paper presents two algorithms that compute approximate Positive Semidefinite (PSD) projections of real symmetric matrices using Randomized Numerical Linear Algebra (RNLA). Classical PSD projection of an $n\\times n$ matrix relies on a deterministic eigen-decomposition with computation that scales as $\\mathcal{O}(n^3)$. Our approach leverages RNLA to construct low-rank matrix approximations before projection, significantly reducing the required numerical resources to $\\mathcal{O}(k n^2)$, for some user defined fixed parameter $k$. The first algorithm utilizes random sampling to generate a low-rank approximation, followed by a standard eigen-decomposition on this smaller matrix. The second algorithm enhances this process by introducing a scaling approach that aligns the leading-order singular values with the positive eigenvalues, biasing the low-rank approximation to focus on capturing the essential information about the positive eigenvalues for PSD projection. Both methods offer a trade-off between accuracy and computational speed, supported by probabilistic error bounds. Numerical experiments on large-scale matrices ( $n\\approx 20K$) demonstrate that the proposed randomized algorithms effectively approximate PSD projections.",
    "categories": "math.OC cs.NA math.NA",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Randomized numerical linear algebra: Foundations and algorithms",
      "Subspace Iteration Randomization and Singular Value Problems",
      "Literature survey on low rank approximation of matrices"
    ]
  },
  {
    "arxiv_id": "2608.17678",
    "title": "Conformal Prediction for Molecular Properties under Label Shift",
    "abstract": "Drug discovery and development underpins healthcare but remains costly and failure-prone. A critical bottleneck lies in predicting molecular properties such as solubility, potency, and toxicity, which directly determine whether a candidate can advance from preclinical to clinical trials. Artificial Intelligence (AI) has accelerated this process, yet its reliability is often undermined by distribution shift, as experimental conditions frequently diverge from training data. In addition, conventional point predictions provide only single-value estimates, offering limited guidance for high-stakes experimental design. We address these challenges with a conformal prediction framework tailored to label shift. By weighting conformal scores using marginal label probability ratios, our method produces statistically rigorous prediction intervals without retraining. This enables robust uncertainty quantification even when property distributions drift, directly tackling one of the most pervasive obstacles to applying AI in real-world drug development. By moving beyond accuracy alone to provide actionable confidence measures, our approach enhances the trustworthiness of AI-driven predictions. This further aligns predictive modeling with regulatory demands for transparency and uncertainty reporting and ultimately supports more reliable decision-making in billion-dollar development pipelines.",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Navigating the protein fitness landscape with Gaussian processes",
      "Integration of element specific persistent homology and machine learning for protein\u2010ligand binding affinity prediction",
      "Computer-aided multi-objective optimization in small molecule discovery"
    ]
  },
  {
    "arxiv_id": "2608.06430",
    "title": "MiGHT-EHR: A Multi-task Graph Transformer for Heterogeneous Temporal Electronic Health Records",
    "abstract": "Learning from Electronic Health Records (EHRs) has gained significant attention due to its potential to improve clinical prediction. However, effective learning remains challenging because EHRs encode heterogeneous, temporally ordered clinical interactions. In particular, EHRs contain: (i) heterogeneous clinical entities, including patients, visits, diagnoses, prescriptions, and procedures, together with their heterogeneous interactions, (ii) longitudinal patient trajectories across hospital visits and (iii) shared statistical dependencies across related clinical prediction tasks. Existing EHR learning methods capture only a subset of these properties. To bridge this gap, we propose Multi-task Graph transformer for Heterogeneous Temporal EHRs (MiGHT-EHR), which jointly models all three within a unified representation learning method. MiGHT-EHR constructs a heterogeneous graph from EHRs in which nodes represent clinical entities and edges connect statistically associated entities identified via normalized point-wise mutual information. Across MIMIC-III and MIMIC-IV datasets, MiGHT-EHR outperforms state-of-the-art methods on average across four tasks: drug recommendation, prediction of length-of-stay, mortality, and readmission, with particularly strong improvements in mortality and readmission prediction. Furthermore, a post-hoc analysis of the learned representations reveals that patient neighborhoods are organized by clinical outcomes, salient medical concepts are recoverabl",
    "categories": "cs.LG q-bio.QM",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A Survey on Kolmogorov-Arnold Network",
      "Nonlinear information fusion algorithms for data-efficient multi-fidelity modelling",
      "Topological data analysis for discovery in preclinical spinal cord injury and traumatic brain injury"
    ]
  },
  {
    "arxiv_id": "2608.16475",
    "title": "A Two-Stage Learning PINN Approach for Solving the Inverse Problem of the 1D Porous Medium Equation",
    "abstract": "The Porous Medium Equation (PME), given by $u_t = \\Delta(u^m)$ for $m > 1$, is a degenerate nonlinear parabolic partial differential equation that arises in various physical applications such as fluid flow in porous media, heat transfer in plasmas, and population dynamics. It is known for its nonlinear diffusion and finite propagation speed. In this paper, we study numerical solutions of the one-dimensional direct and inverse PME using Physics-Informed Neural Networks (PINNs), and compare them with classical numerical methods and available analytical and manufactured solutions. While PINNs provide a flexible framework for solving both forward and inverse problems, we show that the standard inverse formulation suffers from a strong sensitivity to the initial guess, leading to only local convergence. To address this issue, we propose a novel two-stage PINN training framework for the inverse problem, which significantly improves convergence stability and allows reliable recovery of the unknown parameter even for poor initial guesses. Overall, the proposed approach demonstrates that PINNs are a flexible and accurate alternative to classical methods for the 1D PME, and the introduced two-stage training strategy substantially improves their robustness in inverse problems, providing a solid basis for extensions to more complex geometries and higher-dimensional cases.",
    "categories": "math.OC cs.AI",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A Proof that Artificial Neural Networks Overcome the Curse of Dimensionality in the Numerical Approximation of Black\u2013Scholes Partial Differential Equations",
      "A complete Physics-Informed Neural Network-based framework for structural topology optimization",
      "Subgrid modelling for two-dimensional turbulence using neural networks"
    ]
  },
  {
    "arxiv_id": "2608.19043",
    "title": "Bernstein-Vazirani Networks: Quantum Machine Learning by Interference",
    "abstract": "We introduce Bernstein-Vazirani Networks (BVNs), a non-variational quantum machine learning framework that leverages quantum interference for supervised learning, demonstrated on vision and representation learning tasks. In their standard form, BVNs follow the principle of quantum Fourier sampling: labelled data are placed in superposition and interfered in the Fourier basis to extract globally informative features. We then define generalised BVNs that enable interference in problem-adapted bases, yielding more expressive models under the same measurement budget as in the standard setting. BVNs achieve universal function approximation through (over)complete interference bases, while training of BVNs is gradient-free. Experiments on synthetic and real-world classification tasks, as well as implicit image representation, show strong generalisation capabilities and competitive performance with classical and quantum baselines.",
    "categories": "quant-ph cs.AI cs.CV cs.LG",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Shadows of quantum machine learning",
      "Universal expressiveness of variational quantum classifiers and quantum kernels for support vector machines",
      "Quantum machine learning: A comprehensive review of integrating AI with quantum computing for computational advancements"
    ]
  },
  {
    "arxiv_id": "2502.11152",
    "title": "Error Bound Analysis for the Regularized Loss of Deep Linear Neural Networks",
    "abstract": "The optimization foundations of deep linear networks have recently received significant attention. However, due to their inherent non-convexity and hierarchical structure, analyzing the loss functions of deep linear networks remains a challenging task. In this work, we study the local geometry of the regularized squared loss of deep linear networks around each critical point. Specifically, we obtain a closed-form characterization of the critical point set building on existing results and establish an error bound for the regularized loss under mild conditions on network width and regularization parameters. Notably, this error bound quantifies the distance from a point to the critical point set in terms of the current gradient norm, which can be used to derive linear convergence of first-order methods. To support our theoretical findings, we conduct numerical experiments and demonstrate that gradient descent converges linearly to a critical point when optimizing the regularized loss of deep linear networks.",
    "categories": "math.OC cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Gradient descent finds global minima of deep neural networks",
      "A Descent Lemma Beyond Lipschitz Gradient Continuity: First-Order Methods Revisited and Applications",
      "Fixed-Point Continuation for $\\ell_1$-Minimization: Methodology and Convergence"
    ]
  },
  {
    "arxiv_id": "2506.07459",
    "title": "ProteinZero: Self-Improving Protein Generation via Online Reinforcement Learning",
    "abstract": "Protein generative models have shown remarkable promise in protein design, yet their success rates remain constrained by reliance on curated sequence-structure datasets and by misalignment between supervised objectives and real design goals. We present ProteinZero, an online reinforcement learning framework for inverse folding models that enables scalable, automated, and continuous self-improvement with computationally efficient feedback. ProteinZero employs a reward pipeline that combines structural guidance from ESMFold with a novel self-derived ddG predictor, providing stable multi-objective signals while avoiding the prohibitive cost of physics-based methods. To ensure robustness in online RL, we further introduce a novel embedding-level diversity regularizer that mitigates mode collapse and promotes functionally meaningful sequence variation. Within a general RL formulation balancing multi-reward optimization, KL-divergence from a reference model, and diversity regularization, ProteinZero achieves robust improvements across designability, stability, recovery, and diversity. On the CATH-4.3 benchmark, it consistently outperforms state-of-the-art baselines including ProteinMPNN, ESM-IF, and InstructPLM, reducing design failure rates by 36-48% and achieving success rates above 90% across diverse folds. Importantly, a complete RL run can be executed on a single 8 X GPU node within three days, including reward computation and data generation. These results indicate that effic",
    "categories": "cs.LG q-bio.QM",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Computer-aided multi-objective optimization in small molecule discovery",
      "TopologyNet: Topology based deep convolutional and multi-task neural networks for biomolecular property predictions",
      "Navigating the protein fitness landscape with Gaussian processes"
    ]
  },
  {
    "arxiv_id": "2512.07847",
    "title": "CarBench: A Comprehensive Benchmark for Neural Surrogates on High-Fidelity 3D Car Aerodynamics",
    "abstract": "Benchmarking has been the cornerstone of progress in computer vision, natural language processing, and the broader deep learning domain, driving algorithmic innovation through standardized datasets and reproducible evaluation protocols. The growing availability of large-scale Computational Fluid Dynamics (CFD) datasets has opened new opportunities for applying machine learning to aerodynamic and engineering design. Yet, despite this progress, there exists no standardized benchmark for large-scale numerical simulations in engineering design. In this work, we introduce CarBench, the first comprehensive benchmark dedicated to large-scale 3D car aerodynamics, performing a large-scale evaluation of state-of-the-art models on DrivAerNet++, the largest public dataset for automotive aerodynamics, containing over 8,000 high-fidelity car simulations. We assess eleven architectures spanning neural operator methods (e.g., Fourier Neural Operator), geometric deep learning (PointNet, RegDGCNN, PointMAE, PointTransformer), transformer-based neural solvers (Transolver, Transolver++, AB-UPT), and implicit field networks (TripNet). Beyond standard interpolation tasks, we perform cross-category experiments in which transformer-based solvers trained on a single car archetype are evaluated on unseen categories. Our analysis covers predictive accuracy, physical consistency, computational efficiency, and statistical uncertainty. To accelerate progress in data-driven engineering, we open-source the ",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Efficient Aerodynamic Shape Optimization with Deep-Learning-Based Geometric Filtering",
      "A point-cloud deep learning framework for prediction of fluid flow fields on irregular geometries",
      "Meta-heuristics and deep learning for energy applications: Review and open research challenges (2018\u20132023)"
    ]
  },
  {
    "arxiv_id": "2608.21234",
    "title": "Advanced Linear Algebra with Applications - Part I (Numerical linear algebra for PDEs, machine learning, and data assimilation)",
    "abstract": "These lecture notes form the first part of a master's-level course on advanced numerical linear algebra. Their aim is not only to present the classical algorithms, but to show why the subject has become considerably more central than it was a generation ago. Numerical linear algebra grew up alongside the numerical solution of partial differential equations, and for a long time that is where its large sparse systems came from. Ranking the nodes of a network, assimilating observations into a weather forecast, and fitting a model to a large noisy data set now lead to problems of the same kind: too large to factorise, structured, and accessible only through matrix-vector products. Strikingly few ideas are needed for all of them. Each chapter therefore develops a standard topic and then puts it to work outside its original setting. We treat norms, factorisations, conditioning and floating-point arithmetic; sparse matrices arising from finite differences, from graphs and from machine learning; stationary iterations and the smoothing property; the conjugate gradient and Lanczos methods, with spectral clustering and regularisation by early stopping; Arnoldi and GMRES, with PageRank and large least squares; and finally preconditioning, Schwarz domain decomposition and multigrid. We assume a first course in linear algebra. Every section closes with a summary of what should be retained and every chapter with exercises, several drawn from past examinations. Accompanying Python code repro",
    "categories": "math.NA cs.LG cs.NA",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Randomized numerical linear algebra: Foundations and algorithms",
      "Matrix Algorithms, Volume II: Eigensystems",
      "Minimizing Communication in Numerical Linear Algebra"
    ]
  },
  {
    "arxiv_id": "2407.01051",
    "title": "On Some Versions of Subspace Optimization Methods with Inexact Gradient Information",
    "abstract": "It is well-known that accelerated gradient methods possess optimal complexity estimates for the class of convex smooth minimization problems. In many practical situations, it makes sense to work with inexact gradients. However, this can lead to the accumulation of corresponding inexactness in the theoretical estimates of the rate of convergence. We propose some modifications of first-order methods for convex optimization with an inexact gradient based on subspace optimization, such as Nemirovski's Conjugate Gradient method and the Sequential Subspace Optimization method. We study their convergence under different conditions on the inexactness both in the gradient value and in the accuracy of the solution of the subspace optimization subproblems. Besides this, we investigate a generalization of these results to the class of quasar-convex (weakly-quasi-convex) functions.",
    "categories": "math.OC",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Gradient methods for minimizing composite objective function",
      "Interior Gradient and Proximal Methods for Convex and Conic Optimization",
      "A Descent Lemma Beyond Lipschitz Gradient Continuity: First-Order Methods Revisited and Applications"
    ]
  },
  {
    "arxiv_id": "2608.11479",
    "title": "Convergence Guarantees of Gradient Descent for Neural Networks via Generalized Lipschitz Smoothness",
    "abstract": "We establish convergence guarantees of gradient descent for general feedforward neural networks of arbitrary width or depth, with no special requirements on the initialization or dataset. We only assume that the activation functions are Lipschitz smooth, Lipschitz continuous, and linearly bounded--- properties that hold for linear, tanh, softplus, and sigmoid activation functions. For the loss function, we require that it is Lipschitz smooth in the model outputs, which is true for mean-squared error. The key theoretical insight is that the Lipschitz properties of the activation functions are partially preserved even through repeated compositions, leading to a novel generalized Lipschitz smoothness condition where the change in gradient is upper bounded by the change in the parameter space, multiplied by polynomial terms of the parameter norms at both endpoints. This type of condition holds for both the model function and the loss function, enabling a descent lemma where the loss decreases as long as the learning rate is small enough with respect to the parameter norms. By ensuring that the parameter norms do not grow too quickly to infinity, we prove that the minimum squared gradient norm converges to zero in $T$ iterations at rate $O(1/T^{1/L})$ for an $L$-layer neural network.",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Gradient descent finds global minima of deep neural networks",
      "A Descent Lemma Beyond Lipschitz Gradient Continuity: First-Order Methods Revisited and Applications",
      "Gradient Convergence in Gradient methods with Errors"
    ]
  },
  {
    "arxiv_id": "2608.12503",
    "title": "Fast Length-Squared Sampling for Positive-Semidefinite Matrices",
    "abstract": "We describe a simple rejection-sampling-based algorithm to perform length-squared sampling on an $n \\times n$ positive-semidefinite (psd) matrix: that is, to sample a column with probability proportional to its squared $\\ell_2$-norm. The algorithm runs in just $O(n)$ expected time, which is significantly sublinear in the input matrix size. The runtime is optimal, even when the input is assumed to be diagonal. Our result has several applications. Length-squared sampling is used by a number of sublinear time algorithms for matrix problems, like low-rank approximation and eigenvalue approximation. Often, it is assumed that the algorithm is given access to the matrix column norms, and thus can perform length-squared sampling efficiently. Our result shows that, at least for psd matrices, we can remove this assumption. We also discuss an application to an asymptotically optimal algorithm for estimating the Frobenius norm of a psd matrix to relative error. Finally, we show that our sampling algorithm yields a very simple sublinear time algorithm for the robust psd low-rank approximation problem introduced by Bakshi et al. (FOCS, 2020), which nearly matches the more complex method developed there.",
    "categories": "cs.DS cs.LG",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Sampling from large matrices",
      "Randomized numerical linear algebra: Foundations and algorithms",
      "Subspace Iteration Randomization and Singular Value Problems"
    ]
  },
  {
    "arxiv_id": "2605.01835",
    "title": "Learning Koopman operators for coupled systems via information on governing equations of subsystems",
    "abstract": "Nonlinear coupled systems are ubiquitous in science and engineering. The analysis and modeling of such systems are challenging due to their high dimensionality and complex interactions among subsystems. In recent years, operator-theoretic methods based on the Koopman operator have attracted attention as a powerful tool for analyzing and modeling nonlinear dynamical systems. Extended dynamic mode decomposition (EDMD) is one of the most popular methods for approximating the Koopman operator. However, EDMD is a purely data-driven method, and it may be unstable and inaccurate for coupled systems under limited data availability. In this paper, we propose a method to construct a finite-dimensional Koopman approximation for coupled systems using the differential equations governing each subsystem. The proposed method aims to improve data efficiency by using the known subsystem dynamics as prior information and learning the coupling-induced correction from a limited number of snapshots. We also demonstrate its effectiveness through numerical experiments on coupled oscillator systems.",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Numerical solution of large\u2010scale Lyapunov equations, Riccati equations, and linear\u2010quadratic optimal control problems",
      "Dynamical Low\u2010Rank Approximation",
      "Discretization schemes for fractional-order differentiators and integrators"
    ]
  },
  {
    "arxiv_id": "2608.16009",
    "title": "On the Complexity of BFGS Method for Smooth Convex Optimization",
    "abstract": "We study the BFGS method with an Armijo-Wolfe line search for minimizing convex functions with Lipschitz-continuous gradients, without assuming strong convexity. We establish a global iteration complexity bound of $\\mathcal{O}(k^{-1/2})$ for the smallest gradient norm among the first $k$ iterates. Moreover, when the initial sublevel set is bounded, we show that the function value gap converges at a rate of $\\mathcal{O}(k^{-1})$. Our analysis leverages the classical trace-log-determinant potential function and reveals that a key inequality underlying this potential function remains valid without strong convexity.",
    "categories": "math.OC",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Gradient methods for minimizing composite objective function",
      "A Descent Lemma Beyond Lipschitz Gradient Continuity: First-Order Methods Revisited and Applications",
      "A Nonmonotone Line Search Technique and Its Application to Unconstrained Optimization"
    ]
  },
  {
    "arxiv_id": "2608.13797",
    "title": "Recent Advances in Deep Learning-Based Drug-Target Binding Affinity Prediction",
    "abstract": "Computational approaches to drug discovery involve multiple sub-problems, and among them, drug-target binding affinity prediction plays an important role. Despite recent advances, accurately predicting binding affinity remains an open research area. The major objective of our paper is to perform a comprehensive review and comparative analysis of recent machine learning methods for drug-target binding affinity prediction, with a focus on identifying strengths, limitations, and research gaps. We review representative recent deep learning approaches that use common benchmark datasets and evaluation metrics, covering a range of neural network architectures and representation strategies. In addition, we analyze seven widely used benchmark datasets and commonly adopted evaluation metrics for drug-target binding affinity prediction. Our analysis indicates that although many methods report strong performance on standard benchmarks, their effectiveness is often influenced by dataset bias and limited evaluation settings. Furthermore, most methods exhibit reduced performance in cold-start scenarios, highlighting challenges in generalization. We identify several limitations of current approaches, including dataset imbalance, the lack of standardized evaluation, limited real-world applicability, and challenges in cold-start scenarios. We also discuss future research directions, including better dataset design, more robust evaluation methods, improved handling of cold-start problems, and t",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Integration of element specific persistent homology and machine learning for protein\u2010ligand binding affinity prediction",
      "TopologyNet: Topology based deep convolutional and multi-task neural networks for biomolecular property predictions",
      "Meta-heuristics and deep learning for energy applications: Review and open research challenges (2018\u20132023)"
    ]
  },
  {
    "arxiv_id": "2608.12805",
    "title": "CoMedBench: A Multi-Source Benchmark of Synthetic Medical Data Fidelity and Downstream Utility",
    "abstract": "Access to clinical data is essential for developing reliable healthcare machine learning systems, but direct use of electronic health records is constrained by privacy regulation, institutional review, data-use agreements, and the risk of re-identification. Synthetic data promises a practical alternative: it can preserve useful statistical and clinical structure while reducing exposure of sensitive patient records. Prior studies often evaluate a single generator, one dataset, or a narrow downstream task, making it difficult to know when synthetic data can support model development and when it fails to preserve task-critical signal. We introduce CoMedBench, a reproducible benchmark that evaluates a family of generators under a common clinical-validity framework and one shared training and evaluation engine, spanning static tabular and temporal downstream tasks on established critical-care datasets. In total the benchmark spans 37 dataset-task pairs across two modalities consists of 20 static tabular and 17 temporal ICU time-series-drawn from seven public data sources: three intensive-care databases (MIMIC-III, MIMIC-IV, and eICU) together with the UCI Machine Learning Repository, the CDC BRFSS diabetes cohort (2015), NHANES (1999-2014), and the pycox survival datasets (GBSG and METABRIC). The benchmark evaluates both statistical fidelity and task utility by comparing models trained and tested across real and synthetic data. In these settings, synthetic training data preserves ",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "An overview of large AI models and their applications",
      "Using machine learning as a surrogate model for agent-based simulations",
      "A Survey on Kolmogorov-Arnold Network"
    ]
  }
]
```

## Output

One JSON object per abstract, one per line, no prose. Every input `arxiv_id`
appears exactly once. Include `ambiguous` even when false.
