# triage batch 2/5 — domain: compbio_methods

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
    "arxiv_id": "2608.10401",
    "title": "Automatic Field-of-View Adjustment for a View-Expansive Microscope via LSTM-Based Gaze and Pipette Motion Interpretation",
    "abstract": "Intracytoplasmic sperm injection (ICSI) operators frequently adjust the field-of-view (FOV) during procedures, which interrupts workflow and increases procedure time. Conventional microscopes require manual objective lens switching and illumination adjustments to achieve different FOV sizes. We propose an AI-based automatic FOV adjustment method integrated with a view-expansive microscope. This microscope enables the simultaneous acquisition of a large FOV and high-resolution images using a single objective lens through multiview imaging with galvanometer mirrors and high-speed vision, thereby eliminating the need for physical lens exchanges. Our method utilizes a long short-term memory (LSTM) model to predict the appropriate FOV size based on real-time analysis of the pipette's position and velocity, combined with the operator's gaze position. The AI model is trained using ICSI procedure data from an expert with over five years of micromanipulation experience. Experimental evaluation with novice operators reveals that the proposed automatic FOV adjustment system significantly improves the ICSI procedure speed, reducing the average task completion time from 60.5 to 48.0 s (p < 0.001). The experiments also demonstrate that this improvement enables novice operators to achieve ICSI working speeds equivalent to those of expert operators.",
    "categories": "cs.HC cs.LG cs.RO eess.IV",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Cellpose 2.0: how to train your own model",
      "Evolution-guided Bayesian optimization for constrained multi-objective optimization in self-driving labs",
      "Combining radial basis function surrogates and dynamic coordinate search in high-dimensional expensive black-box optimization"
    ]
  },
  {
    "arxiv_id": "2608.09887",
    "title": "Space-Creating versus Dead Possession: An Off-Ball Possession-Quality Index for Broadcast Football",
    "abstract": "Ball possession is the most-cited and most-misleading number in football: 60% recycled in one's own half is not 60% spent pinning the opponent back. Existing event-based possession-value frameworks (expected threat, VAEP, on-ball value) price on-ball actions but ignore the off-ball question a sterile possession poses: did holding the ball create space, or was the circulation dead? We answer this in two layers. First, an event-side junk-possession index prices each possession sequence by its peak threat gain under an expected-threat grid and -- after reconstructing the live scoreline to exclude lead-protecting circulation -- flags low-threat sequences in tied-or-losing states. On the 2026 FIFA World Cup (103 matches, 206 team-matches) the flag correlates negatively with points (r=-0.37) and xG difference (r=-0.51, partly index-coupled). It is not a repackaging of on-ball value: with team offensive VAEP and field tilt held fixed, the junk flag stays strongly negatively associated with points (p<0.0001, also match-clustered) while VAEP is not significant -- in this same-match (descriptive) regression it adds information beyond this on-ball action-value model. Second, for a flagged window we resolve whether it was spatially dead or space-creating by projecting broadcast video to pitch coordinates and measuring a Space-Creation Index (SCI): a net pitch-control change capturing whether the possession seized space or pushed the opponent's block back. Across 31 of 35 flagged windows ",
    "categories": "cs.CV cs.CY cs.LG",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Shapley Effects for Global Sensitivity Analysis: Theory and Computation",
      "How Hard Is Bribery in Elections?",
      "Compressed full-text indexes"
    ]
  },
  {
    "arxiv_id": "2608.14650",
    "title": "Paired Exact-Reset Evaluation of a Prediction-Derived Medium-to-Full World-Model Cascade",
    "abstract": "Existing adaptive-inference and world-action-model systems use cheap-stage outputs or predicted futures to allocate additional computation. We study a narrower question: under paired exact-reset physical outcomes, can a Medium-derived interface predict when switching to a separately frozen Full predictor improves task-specific decision loss enough to justify sequential overhead? Our contribution is a paired evaluation and audit protocol, not a new generic routing rule: all candidate actions are executed from the same reset state, Medium and Full act on the same candidate set and task, and their paired physical-loss difference defines the routing target. On a fresh PushT bank (V106; 1,600 states, 39 tasks, three checkpoint pairs), a frozen prediction-interface router lowers overhead-inclusive decision cost relative to standalone Medium, standalone Full, and a latency-advantaged task-only router. We then prospectively seal a second 1,600-state PushT confirmation (V107) against a stronger current-state control using the task, a dimension-matched projection of current DINO features, and all five candidate actions, with no DINO encoder latency charged. The prediction interface lowers priced physical decision cost by 0.002549 (state-clustered 95% interval [-0.002867, -0.002238]; one-sided 95% upper bound -0.002286), with negative effects for all three checkpoint pairs. A controlled-PyBullet audit independently supports a composite task-prediction-regime router. The sequential route",
    "categories": "cs.LG cs.RO",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Eligibility Traces for Off-Policy Policy Evaluation",
      "Distributional Soft Actor-Critic With Three Refinements",
      "Explicit Evolutionary Multitasking for Combinatorial Optimization: A Case Study on Capacitated Vehicle Routing Problem"
    ]
  },
  {
    "arxiv_id": "2608.10553",
    "title": "Retrieval-Corrected Conformal Prediction for Time Series",
    "abstract": "Conformal prediction (CP) provides distribution-free prediction intervals for fixed forecasters, but its standard calibration procedure is often inefficient for time series data, where forecast errors are temporally dependent and change across time and operating conditions. Recent time series CP methods improve local calibration using recent, weighted, or localized residuals. Yet local calibration can remain indirect, since broad residual weighting or additional adaptation procedures may dilute the evidence most relevant to the current prediction. This motivates a simple retrieval and correction strategy that selects similar past residuals as local evidence and then corrects the coverage error left by retrieval. In this paper, we propose Retrieval--Corrected Conformal Prediction (RCCP), a retrieval-augmented calibration method for time series prediction intervals. RCCP builds an asymmetric interval from retrieved one-sided residuals and calibrates its normalized retrieval error with a scalar conformal correction. Thus, retrieval provides local residual evidence, while conformal correction determines the final scale needed for coverage. We provide a coverage-gap bound based on the stability of the normalized retrieval error distribution. Across standard benchmarks and backbone forecasters, RCCP attains the target coverage in every setting and achieves the lowest Winkler scores, with fewer severe misses. RCCP also achieves low calibration and inference overhead, showing that re",
    "categories": "cs.LG cs.AI",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Enhancing financial time series forecasting through topological data analysis",
      "Learning about physical parameters: the importance of model discrepancy",
      "Heterogeneous Ensemble-Based Infill Criterion for Evolutionary Multiobjective Optimization of Expensive Problems"
    ]
  },
  {
    "arxiv_id": "2608.06956",
    "title": "How Molecular Generative Models Organize Molecular Identity",
    "abstract": "Generative models for matter are often evaluated as samplers over output representations, and their latent spaces are commonly used as proxies for navigating chemical space. Much less is known about how these models internally arrange discrete chemical identities within those representations. We study this arrangement by making molecular identity explicit and pulling it back through the generative process. Through these pullbacks we probe the regions that generate the same object, exposing the trained model's internal repertoire: a fixed partition that determines which objects (novel or not) the model can produce. Across three molecular generative architectures, we find that this repertoire is arranged into piecewise-constant regions separated by recurring coarse-to-fine boundaries. Its organization depends on the representation probed, the identity convention, decoder stochasticity, and the metric used to compare coordinates. During training, local chemical organization stabilizes while the number of distinct molecular identities represented within each neighborhood continues to change. Internal organization must therefore be characterized, rather than assumed, before a generative space can be treated as chemically navigable.",
    "categories": "cs.LG physics.chem-ph",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Active phase discovery in heterogeneous catalysis via topology-guided sampling and machine learning",
      "Representability of algebraic topology for biomolecules in machine learning based scoring and virtual screening",
      "A Review of Topological Data Analysis and Topological Deep Learning in Molecular Sciences"
    ]
  },
  {
    "arxiv_id": "2601.21628",
    "title": "Noise as a Probe: Membership Inference Attacks on Diffusion Models Leveraging Initial Noise",
    "abstract": "Diffusion models have achieved remarkable progress in image generation, but their increasing deployment raises serious concerns about privacy and copyright. In particular, fine-tuned models are highly vulnerable, as they are often fine-tuned on small and private datasets. Membership inference attacks (MIAs) are used to assess privacy risks by determining whether a specific sample was part of a model's training data. Existing MIAs against diffusion models either assume obtaining the intermediate results or require training the shadow model on auxiliary datasets. In this work, we utilized a critical yet overlooked vulnerability: the widely used noise schedules fail to fully eliminate semantic information in the images, resulting in residual semantic signals even at the maximum noise step. We empirically demonstrate that the fine-tuned diffusion model captures hidden correlations between the residual semantics in initial noise and the original images. Building on this insight, we propose a simple yet effective membership inference attack, which injects semantic information into the initial noise and infers membership by analyzing the model's generation result. Extensive experiments demonstrate that the semantic initial noise can strongly reveal membership information, highlighting the vulnerability of diffusion models to MIAs. Code is available at https://github.com/S3IC-Lab/NoiseMIA.",
    "categories": "cs.CR cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Opportunities and challenges of diffusion models for generative AI",
      "Privacy-Preserving Machine Learning With Fully Homomorphic Encryption for Deep Neural Network",
      "Cognition-Driven Structural Prior for Instance-Dependent Label Transition Matrix Estimation"
    ]
  },
  {
    "arxiv_id": "2608.12974",
    "title": "Comment on \"Modeling rapid language learning by distilling Bayesian priors into artificial neural networks\"",
    "abstract": "McCoy & Griffiths (2025, henceforth M&G) suggest that a Bayesian prior can be distilled into Artificial Neural Networks (ANNs) through Model-Agnostic Meta-Learning (MAML, Finn et al., 2017). They support this empirically by showing that meta-trained networks demonstrate formal language learning abilities comparable to Yang & Piantadosi (2023)'s Bayesian learner, significantly outperforming standard ANNs. We point out that under the standard interpretation of a prior, M&G's procedure does not actually instill one; it merely initializes network weights favorably, leaving the objective function unchanged. We then consider a more permissive interpretation, where the system as a whole can be seen as implementing a Bayesian learner even without an explicit prior in the objective. We show that this interpretation faces nontrivial challenges. Finally, we assess how well MAML approximates the empirical results of Bayesian learning, showing that unlike genuine Bayesian learners, M&G's model overfits and generalizes poorly to unseen data.",
    "categories": "cs.LG cs.CL",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Basic Enhancement Strategies When Using Bayesian Optimization for Hyperparameter Tuning of Deep Neural Networks",
      "Evolutionary optimization of model merging recipes",
      "GPT-3: Its Nature, Scope, Limits, and Consequences"
    ]
  },
  {
    "arxiv_id": "2501.17400",
    "title": "A Model-Free Data-Driven Algorithm for Continuous-Time Control",
    "abstract": "Presented is an algorithm to synthesize an infinite-horizon LQR optimal feedback controller for continuous-time systems. The algorithm does not require knowledge of the system dynamics, but instead uses only a finite-length sampling of (possibly suboptimal) input-output data. The algorithm is based on a constrained optimization problem that enforces a necessary condition on the dynamics of the optimal value function along an arbitrary trajectory. This paper presents the derivation as well as shows examples applied to both linear and nonlinear systems inspired by air vehicles.",
    "categories": "math.OC cs.SY eess.SY",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Value and Policy Iterations in Optimal Control and Adaptive Dynamic Programming",
      "A Survey of Linear Parameter-Varying Control Applications Validated by Experiments or High-Fidelity Simulations",
      "Continuous-time analysis, eigenstructure assignment, and H/sub 2/ synthesis with enhanced linear matrix inequalities (LMI) characterizations"
    ]
  },
  {
    "arxiv_id": "2608.16031",
    "title": "AdROD: HyperNetwork-based Adversarially Robust Object Detection for Autonomous Driving",
    "abstract": "Camera-based object detectors are vulnerable to physical adversarial attacks designed to suppress detections. While adversarial training and input purification offer some protection, they often overfit to specific attack distributions and fail on adaptive adversaries. This paper presents AdROD, an embedded, stochastic ensemble defense software designed for autonomous driving. AdROD employs {\\em low-rank HyperNetworks}, which require only 1.6\\% of the parameter footprint of standard HyperNetworks, to generate diverse detectors at a per-frame rate, making it impractical for attackers to obtain the deployed detectors in time. To further improve adversarial robustness, AdROD incorporates a novel \\emph{functional diversity} mechanism, which couples stochastic weight updates with unique input-space transformations. We design two serving modes of AdROD that strike different trade-offs between robustness and runtime overhead: AdROD-I, a continuous protection mode for maximum resilience that leverages inter-detector disagreement to recover compromised detections, and AdROD-II, an on-demand mode triggered by kinematic discontinuities in object tracking. Through comprehensive evaluation with synthetic benchmarks, physically deployed adversarial patches, and end-to-end safety tests in the OpenCDA co-simulator, AdROD outperforms five baseline defenses and exhibits superior generalizability compared with the evaluated adversarial-training baselines, while maintaining real-time performance ",
    "categories": "cs.LG cs.CV",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Neural Architecture Search as Multiobjective Optimization Benchmarks: Problem Formulation and Performance Assessment",
      "Adaptive Submodularity: Theory and Applications in Active Learning and Stochastic Optimization",
      "Physical Layer Authentication and Security Design in the Machine Learning Era"
    ]
  },
  {
    "arxiv_id": "2502.05375",
    "title": "Properties of Turnpike Functions for Discounted Finite Markov Decision Processes",
    "abstract": "This paper studies convergence times of the Value Iteration Algorithm (VIA) for discounted discrete-time Markov Decision Processes (MDPs) with finite state and action sets. For each discount factor, starting from a finite number of iterations, which is called the turnpike integer, the VIA generates deterministic optimal policies for infinite-horizon problems. Turnpike integers are viewed as functions of discount factors called turnpike functions. We design an algorithm to detect in strongly polynomial time whether a discount factor is irregular - at which the sets of optimal policies change. We then prove that a turnpike function is upper-semicontinuous and finitely-piecewise constant on any closed subinterval of [0,1) that does not contain irregular points. In particular, we prove that for small discount factors a turnpike function is bounded by the number of states and design an algorithm based on the VIA to solve an MDP for all small discount factors in strongly polynomial time.",
    "categories": "math.OC",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Value and Policy Iterations in Optimal Control and Adaptive Dynamic Programming",
      "Online convex programming and generalized infinitesimal gradient ascent",
      "Optimal Inapproximability Results for MAX\u2010CUT and Other 2\u2010Variable CSPs?"
    ]
  },
  {
    "arxiv_id": "2608.14823",
    "title": "Disentangling Homophily and Rarity: Explaining Failure in Graph Neural Networks",
    "abstract": "Are heterophilic nodes in a graph harder to classify because they are heterophilic or because they are rare? Some existing work frames classification of such nodes as a subgroup generalisation problem, where a model performs well on the majority group at the expense of the rare group. Others explain this as a problem of neighbourhood aggregation in graph neural networks (GNNs). We assess these two viewpoints through a detailed evaluation of six GNNs on five datasets of varying homophily, and find that homophilic nodes tend to be easier to classify, even when they are rare---challenging the subgroup framing. However, our findings also nuance existing beliefs about how GNNs misrepresent heterophilic nodes. We demonstrate that the information needed to classify heterophilic nodes correctly is often recoverable by retraining the classification head of a model, or even just the final linear classification layer.",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Topological Data Analysis in Graph Neural Networks: Surveys and Perspectives",
      "Two\u2019s company, three (or more) is a simplex",
      "Finding and evaluating community structure in networks"
    ]
  },
  {
    "arxiv_id": "2508.08218",
    "title": "A Distributed Asynchronous Generalized Momentum Algorithm Without Delay Bounds",
    "abstract": "Asynchronous optimization algorithms often require delay bounds to prove their convergence, though these bounds can be difficult to obtain in practice. Therefore, we introduce a novel distributed generalized momentum algorithm that provides fast convergence and allows arbitrary finite delays. It subsumes Nesterov's accelerated gradient algorithm and the heavy ball algorithm, among others. We first develop conditions on the parameters of the algorithm that ensure asymptotic convergence. Then we show its convergence rate is linear in a function of the number of computations and communications that processors perform (in a way that we make precise). Simulations compare this algorithm to gradient descent, heavy ball, and Nesterov's accelerated gradient algorithm with a text classification problem on the 20 newsgroups dataset. Across a range of scenarios with unbounded delays, the generalized momentum algorithm converges with at least 36% fewer iterations than gradient descent, 28% fewer iterations than the heavy ball algorithm, and 16% fewer iterations than Nesterov's accelerated gradient algorithm.",
    "categories": "math.OC",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Convex Optimization for Big Data: Scalable, randomized, and parallel algorithms for big data analytics",
      "Gradient descent finds global minima of deep neural networks",
      "Parallel coordinate descent methods for big data optimization"
    ]
  },
  {
    "arxiv_id": "2608.19098",
    "title": "Open-MOPD: Diagnosing and Fixing Capability Imbalance in Multi-Teacher On-Policy Distillation",
    "abstract": "Multi-teacher on-policy distillation (M-OPD) has emerged as a promising paradigm for consolidating domain-specialized reinforcement learning (RL) experts into a single generalist student via dense, token-level reward supervision. Despite its practical success, the optimization dynamics governing multi-teacher capability integration remain poorly understood, and open, rigorously reproducible recipes are conspicuously lacking. In this work, we establish a controlled M-OPD benchmark on SmolLM3-3B-Base with oracle routing, isolating capability integration from routing ambiguity. Our investigation reveals a pronounced capability integration gap: standard M-OPD captures only 35.6% of the available headroom relative to a domain-routed oracle ensemble, with concise tasks such as instruction following suffering severe degradation and premature stagnation. Crucially, we show that this failure stems not from gradient conflict, but from a severe misallocation of the token-level optimization budget. This pathology is driven by three orthogonal factors: structural sequence-length disparities across domains, dynamic convergence drift due to non-uniform learning rates, and multi-step reward staleness from asynchronous policy updates. To resolve these imbalances, we introduce Open-MOPD, a principled framework incorporating token-share balancing, gap-aware dynamic budget allocation, and student reward refresh. Together, these mechanisms systematically restore cross-domain balance, elevating he",
    "categories": "cs.LG cs.AI cs.CL",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Insights on Transfer Optimization: Because Experience is the Best Teacher",
      "A Survey on Learnable Evolutionary Algorithms for Scalable Multiobjective Optimization",
      "A Level-Based Learning Swarm Optimizer for Large-Scale Optimization"
    ]
  },
  {
    "arxiv_id": "2608.18825",
    "title": "Understanding Multilingual Medical ASR Adaptation Through Layer-Wise Analysis",
    "abstract": "Medical automatic speech recognition (MedASR) requires adaptation to specialised terminology, limited annotated clinical data, and multilingual use cases. Although large-scale pretrained ASR models such as Whisper achieve strong generalisation, their behaviour after medical and multilingual adaptation remains insufficiently understood beyond word error rate (WER). This paper investigates how multilingual medical adaptation reshapes the internal representations of Whisper models through layer-wise encoder analysis. We compare zero-shot decoding, English-only fine-tuning, German-only diagnostic fine-tuning, two-stage EN->EN+DE continuation, and direct EN+DE fine-tuning across Whisper model sizes. Fine-tuning substantially improves MedASR performance, but the best model depends on the adaptation setting: Whisper-Medium gives the lowest English WER (7.72%) and the lowest combined EN+DE WER under direct EN+DE training (26.30%); German-only Whisper-Large-v3 gives the lowest German WER (44.96%), but as a within-corpus diagnostic on 86 single-speaker training utterances rather than robust generalisation. Layer-wise analysis of the two-stage Whisper-Small trajectory shows that English medical fine-tuning produces the dominant encoder shift, whereas multilingual continuation largely preserves the adapted representation space. Domain and language information remain highly recoverable across layers, while linearly recoverable error-predictive cues weaken as WER improves.",
    "categories": "cs.CL cs.AI cs.LG cs.SD",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Basic Enhancement Strategies When Using Bayesian Optimization for Hyperparameter Tuning of Deep Neural Networks",
      "The unreasonable effectiveness of deep learning in artificial intelligence",
      "Cellpose 2.0: how to train your own model"
    ]
  },
  {
    "arxiv_id": "2608.11261",
    "title": "Temperature-Driven Sequential Modeling for the Prediction of Annual Power Conversion Efficiency Profiles of Organic Photovoltaic Materials: Douala Case Study",
    "abstract": "Organic photovoltaic (OPV) materials are promising candidates for distributed solar energy in tropical regions, yet existing virtual screening tools report static power conversion efficiency (PCE) values at standard testing conditions (STC) that fail to capture the temperature-driven performance degradation experienced under real deployment conditions. Here we introduce a Climate-Native computational framework that forecasts the annual PCE profile of OPV donor molecules under geographically realistic operating conditions. The framework combines GFN2-xTB molecular dynamics with an equivariant graph neural network surrogate ($268$ Neyman-stratified CEP molecules; $120,600$ training geometries; $\\sim 1050\\times$ speedup over explicit quantum chemistry) and sequential deep learning models trained on annual time series anchored in NASA POWER climate data for Douala, Cameroon, and validated by zero-shot transfer to Yaound\\'e and Maroua. Applied to $\\sim 30,000$ molecules from the Harvard Clean Energy Project (CEP) and validated against $350$ HOPV15 experimental device measurements, the framework demonstrates that sequential models trained on full molecular dynamics trajectories outperform time-averaged baselines ($35\\%$-$48\\%$ relative MAE improvement over static baselines), confirming that thermal conformational dynamics carry information beyond mean geometry. We further introduce a seasonal stability score that reranks OPV candidates by performance consistency under tropical cond",
    "categories": "cond-mat.mtrl-sci cs.LG physics.chem-ph",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Meta-heuristics and deep learning for energy applications: Review and open research challenges (2018\u20132023)",
      "Efficient Global Structure Optimization with a Machine-Learned Surrogate Model",
      "Neural network-based surrogate modeling and optimization of a multigeneration system"
    ]
  },
  {
    "arxiv_id": "2608.17290",
    "title": "Universal Approximation of Maximal Lyapunov Functions with Anchored Neural Networks",
    "abstract": "Maximal Lyapunov functions encode the entire domain of attraction of an asymptotically stable equilibrium, but preserving strict decrease under neural approximation is difficult because its margin vanishes at the equilibrium. For systems locally dominated by an asymptotically stable homogeneous vector field, we construct a continuously differentiable maximal target and an anchored, positivity-preserving neural family. We prove semiglobal universal approximation: strict neural Lyapunov functions and their first derivatives can approximate the target on nested invariant sublevel sets that exhaust the domain of attraction. We also provide directly verifiable conditions under which a candidate neural Lyapunov function can be formally certified, and illustrate the effectiveness of the proposed neural architecture through numerical examples.",
    "categories": "eess.SY cs.SY math.OC",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A Proof that Artificial Neural Networks Overcome the Curse of Dimensionality in the Numerical Approximation of Black\u2013Scholes Partial Differential Equations",
      "Antiwindup design with guaranteed regions of stability: an LMI-based approach",
      "Li\u2013Yorke sensitivity"
    ]
  },
  {
    "arxiv_id": "2608.10529",
    "title": "Robust Multi-Agent Bandits with Heavy-Tailed Rewards and Information Asymmetry",
    "abstract": "The multi-armed bandit problem is a central framework in sequential decision-making, extensively studied under sub-Gaussian reward assumptions. However, real-world applications often involve heavy-tailed reward distributions and decentralized, information-asymmetric interactions. We study multi-agent multi-armed bandits with heavy-tailed rewards under three information-asymmetry regimes: unobserved actions with common rewards, observed actions with independent rewards, and unobserved actions with independent rewards. We develop robust decentralized algorithms for each setting and derive regret guarantees that nearly match centralized heavy-tailed rates. Experiments on a Pareto-distributed reward environment validate our theoretical findings and illustrate the trade-offs between synchronization, coordination, and exploration across the three regimes.",
    "categories": "cs.LG cs.AI",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Information-Theoretic Regret Bounds for Gaussian Process Optimization in the Bandit Setting",
      "Contextual Gaussian Process Bandit Optimization",
      "Multi-objective reinforcement learning using sets of pareto dominating policies"
    ]
  },
  {
    "arxiv_id": "2602.22647",
    "title": "Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators",
    "abstract": "Generative retrieval has emerged as a powerful paradigm for LLM-based recommendation. However, industrial recommender systems often benefit from restricting the output space to a constrained subset of items based on business logic (e.g. enforcing content freshness or product category), which standard autoregressive decoding cannot natively support. Moreover, existing constrained decoding methods that make use of prefix trees (Tries) incur severe latency penalties on hardware accelerators (TPUs/GPUs). In this work, we introduce STATIC (Sparse Transition Matrix-Accelerated Trie Index for Constrained Decoding), an efficient and scalable constrained decoding technique designed specifically for high-throughput LLM-based generative retrieval on TPUs/GPUs. By flattening the prefix tree into a static Compressed Sparse Row (CSR) matrix, we transform irregular tree traversals into fully vectorized sparse matrix operations, unlocking massive efficiency gains on hardware accelerators. We deploy STATIC on a large-scale industrial video recommendation platform serving billions of users. STATIC produces significant product metric impact with minimal latency overhead (0.033 ms per step and 0.25% of inference time), achieving a 948x speedup over a CPU trie implementation and a 47-1033x speedup over a hardware-accelerated binary-search baseline. Furthermore, the runtime overhead of STATIC remains extremely low across a wide range of practical configurations. To the best of our knowledge, STATI",
    "categories": "cs.IR cs.CL cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Ecient Sparse Matrix-Vector Multiplication on CUDA",
      "Thinking Like a Vertex",
      "Fixed-Rate Compressed Floating-Point Arrays"
    ]
  },
  {
    "arxiv_id": "2608.16932",
    "title": "DOW-KE: Anchor-Free Multi-Layer Knowledge Editing via Direct End-to-End Weight Optimization",
    "abstract": "Multi-layer locate-then-edit methods for knowledge editing first optimize target residual-stream activations (anchors) at selected layers, then realize them layer by layer as weight updates. This pipeline optimizes an intermediate representation but deploys multi-layer weight updates whose joint effect through the true forward pass is never itself optimized: regardless of how anchors are set or propagated, each update comes from a local solve, so propagation-induced attenuation and distortion go uncorrected, leaving a closure gap between anchor targets and realized edits. We propose DOW-KE, an anchor-free method built on a single principle: what is optimized must be exactly what is deployed. DOW-KE backpropagates the final editing objective through the complete model, jointly optimizing the updates of all edited layers so cross-layer propagation and coupling enter every gradient step. The same principle dictates where preservation resides: embedding the preservation projection in the update parameterization, inside the computation graph, makes every gradient act on the deployed update; post-hoc constraints would reopen the gap, and the constrained search keeps edits clear of protected knowledge. In large-scale sequential editing on two datasets and three models, DOW-KE achieves the highest overall Score and neighborhood Specificity in five of six model-dataset settings among the evaluated baselines.",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Insights on Transfer Optimization: Because Experience is the Best Teacher",
      "Block-Level Knowledge Transfer for Evolutionary Multitask Optimization",
      "Performance and Scalability of the Block Low-Rank Multifrontal Factorization on Multicore Architectures"
    ]
  },
  {
    "arxiv_id": "2608.18118",
    "title": "Formal Safety Verification for Nonlinear Systems with Generative Barrier Certificate",
    "abstract": "Safety verification is a fundamental problem in control theory. Barrier certificates (BCs) provide a powerful formal mechanism, yet deriving BCs is computationally intensive. This paper introduces a generative framework that leverages large language models (LLMs) to synthesize BCs through reasoning. Based on the classical Sum-of-Squares (SOS) approach, we train a domain-specific LLM capable of generating high-quality BC candidates for nonlinear systems. Then, the LLM-generated BCs transform the intractable Bilinear Matrix Inequality (BMI) solving problems into convex Linear Matrix Inequality (LMI) feasibility test, significantly improving efficiency while preserving correctness. Experimental results show that our generative method achieves several orders of magnitude speedup over traditional numerical BC approaches and, perhaps surprisingly, surpasses the state-of-the-art dedicated neural BC model. These findings mark a substantive step toward integrating generative AI with formal safety verification for dynamical systems.",
    "categories": "math.OC cs.SY eess.SY",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Combining Convex\u2013Concave Decompositions and Linearization Approaches for Solving BMIs, With Application to Static Output Feedback",
      "Evolutionary optimization of model merging recipes",
      "Evolutionary Optimization of Computationally Expensive Problems via Surrogate Modeling"
    ]
  },
  {
    "arxiv_id": "2608.17501",
    "title": "SGHA: Evidence-Grounded Research Problem Discovery with Local Language Models",
    "abstract": "Recent efforts toward fully automated AI scientists have demonstrated that language-model agents can generate hypotheses, execute experiments, and draft scientific manuscripts. However, during the early stages of research, when research problems are formulated, these AI scientists often rely heavily on proprietary frontier models. Their proposals are shaped by opaque parametric knowledge and by literature searches conditioned on the proposals themselves. Such knowledge is effectively a black box, and this dependence makes the evidential basis and validity of generated research problems difficult to audit and leaves the process vulnerable to model-specific hallucinations and biases. Furthermore, if proprietary research materials are transmitted to external APIs, the use of these models creates confidentiality, privacy, and data-governance concerns. We introduce the Structural Gap Hypothesis Agent (SGHA), a fully automated, corpus-first research-problem discovery system that runs entirely on a local LLM. SGHA structures a scientific literature corpus into evidence-linked paper objects and a typed evidence graph, detects unresolved structural patterns across papers, screens candidate gaps before formulation, and produces traceable research-problem families. In particular, it is able to output assumptions, objectives, success criteria, and remaining ambiguities. All LLM-based components of SGHA are executed using a locally served open-weight 9B language model, without requiring p",
    "categories": "cs.AI cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Mathematical discoveries from program search with large language models",
      "GPT-3: Its Nature, Scope, Limits, and Consequences",
      "Foundation models are platform models: Prompting and the political economy of AI"
    ]
  },
  {
    "arxiv_id": "2608.08027",
    "title": "BASIS: Breach-Aware Selective Prompt Injection Shielding with Prefill Attention Probes",
    "abstract": "Prompt injection is a critical security threat in large language model (LLM) applications, where attackers hijack model behavior by embedding malicious instructions in user or external data. Existing detection methods only detect the presence of injection and refuse to respond upon detection, overlooking the fact that for many modern aligned models, well-crafted instructions can resist most injection attacks. This means that the injection robustness varies significantly across instructions and models. This leads to widespread unnecessary over-refusal: inputs containing injections that the model could have handled correctly are rejected incorrectly. To deal with this over-refusal issue, we propose BASIS (Robustness-Aware Prompt Injection Defense). This defense method uses the Attention Competition Ratio ($\\rho$) as features to train two sparse linear probes: an existence probe and a breach probe. Both probes make defense decisions through cascaded gating, which does not require additional LLM inference. BASIS comprises three stages: injection existence detection, per-sample breach prediction, and instruction robustness assessment; the online cascade refuses only when the model would actually be compromised and thus avoids over-refusal on robust instructions. Experiments across four tasks and six open-source LLMs show that BASIS maintains near-perfect injection detection while substantially reducing over-refusal on safe attack samples, especially under robust instruction templa",
    "categories": "cs.CR cs.LG",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Physical Layer Authentication and Security Design in the Machine Learning Era",
      "On the (im)possibility of obfuscating programs",
      "Preventing undesirable behavior of intelligent machines"
    ]
  },
  {
    "arxiv_id": "2608.10957",
    "title": "DD-suite: A cross-platform package to build Decision Diagrams for optimization purposes",
    "abstract": "Decision diagrams (DDs) have become a powerful tool for discrete optimization, supporting a wide range of algorithms that span cut-generation procedures, decomposition methods, and specialized branch-and-bound searches. Despite this growth, their adoption remains limited, partly because most existing DD code is tailored to a specific algorithm or application and is therefore hard to reuse. We introduce DD-suite, a cross-platform, open-source software package for building and manipulating DDs for discrete optimization. DD-suite is available in both Python and C++ through a shared modeling interface, and lets users construct exact, restricted, and relaxed DDs for any discrete optimization problem expressed in recursive form. The package implements the DD reduction procedure, shortest-path routines for obtaining primal and dual bounds, a visualization tool, and an extensive automated test suite. Furthermore, it includes extensive documentation, a support webpage, and ready-to-use examples for four combinatorial problems. Rather than a closed solver, DD-suite is designed as an extensible building block: users can add new construction mechanisms or run custom algorithms on top of the resulting diagram, as we illustrate with a DD-based cutting plane procedure embedded in a state-of-the-art mixed-integer programming solver. Our numerical experiments show that the C++ implementation is 5-6 times faster than the Python one while producing identical diagrams, and remains within a small",
    "categories": "math.OC",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Using Branch-and-Price-and-Cut to Solve Origin-Destination Integer Multicommodity Flow Problems",
      "A parallel global multiobjective framework for optimization: pagmo",
      "Pymoo: Multi-Objective Optimization in Python"
    ]
  },
  {
    "arxiv_id": "2608.10386",
    "title": "Dreamer-SAC: Off-Policy Learning in Latent World Models for Sample-Efficient Autonomous Driving",
    "abstract": "Sample-efficient reinforcement learning for autonomous driving is often limited by the trade-off between data efficiency and model bias. While world models reduce the reliance on costly environment interactions, policy optimization over learned dynamics remains sensitive to prediction errors. This paper proposes the Dreamer-SAC framework, which integrates a recurrent state-space world model with an off-policy soft actor-critic algorithm trained directly in latent space. The framework uses a combination of real interactions and short-horizon generated trajectories with n-step target estimation and multi-objective supervision. Evaluated in autonomous driving scenarios with objectives encompassing driving efficiency and safety, the proposed framework consistently outperforms representative reinforcement learning baselines, including DreamerV3, SAC, and PPO, while achieving improved performance with substantially fewer real environment interactions. Experiments reveal an inverted-U relationship between rollout horizon and policy performance, where short-horizon latent rollouts achieve the best trade-off between additional training signals and accumulated model bias. Furthermore, n-step target estimation demonstrates more effectiveness over one-step temporal-difference targets in exploiting predicted experience for value learning.",
    "categories": "cs.LG cs.RO",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Gaussian Processes for Data-Efficient Learning in Robotics and Control",
      "Distributional Soft Actor-Critic With Three Refinements",
      "Eligibility Traces for Off-Policy Policy Evaluation"
    ]
  },
  {
    "arxiv_id": "2602.18662",
    "title": "Large Causal Models for Temporal Causal Discovery",
    "abstract": "Causal discovery for both cross-sectional and temporal data has traditionally followed a dataset-specific paradigm, where a new model is fitted for each individual dataset. Such an approach limits the potential of multi-dataset pretraining. The concept of large causal models (LCMs) envisions a class of pre-trained neural architectures specifically designed for temporal causal discovery. Prior approaches are constrained to small variable counts, degrade with larger inputs, and rely heavily on synthetic data, limiting generalization. We propose a principled framework for LCMs, combining diverse synthetic generators with realistic time-series datasets, allowing learning at scale. Extensive experiments on synthetic, semi-synthetic and realistic benchmarks show that LCMs scale effectively to higher variable counts and deeper architectures while maintaining strong performance. Trained models achieve competitive or superior accuracy compared to classical and neural baselines, particularly in out-of-distribution settings, while enabling fast, single-pass inference. Results demonstrate LCMs as a promising foundation-model paradigm for temporal causal discovery. Experiments and model weights are available at https://github.com/kougioulis/LCM/.",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "An overview of large AI models and their applications",
      "Opportunities and challenges of diffusion models for generative AI",
      "Using machine learning as a surrogate model for agent-based simulations"
    ]
  }
]
```

## Output

One JSON object per abstract, one per line, no prose. Every input `arxiv_id`
appears exactly once. Include `ambiguous` even when false.
