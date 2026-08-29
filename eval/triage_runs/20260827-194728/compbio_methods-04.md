# triage batch 4/5 — domain: compbio_methods

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
    "arxiv_id": "2608.14031",
    "title": "Demonstration of Space Robot Teleoperation over a Lossy and Delayed Network using ATMOS",
    "abstract": "We present a demonstration showcasing the Autonomy Testbed for Multi-purpose Orbiting Systems (ATMOS), a planar spacecraft-analog robot designed for hardware-in-the-loop evaluation of guidance and control strategies in microgravity-like conditions. Using ATMOS as the physical test platform, we investigate the design, analysis, and performance evaluation of control architectures for remotely operated spacecraft under round-trip communication delays. In this work, we develop and experimentally validate a control strategy that combines state prediction and trajectory tracking control to perform a docking maneuver, accounting for time-varying random communication latency between ground operators and the ATMOS system. The demonstration includes a long-distance remote control experiment between Seoul and Stockholm, introducing realistic intercontinental delays and variability. The results highlight the capability of ATMOS to support rapid, reliable, and cost-effective testing of spacecraft teleoperation concepts, establishing a first step toward robust validation of on-orbit operations in microgravity-like environments.",
    "categories": "cs.RO cs.SY eess.SY math.OC",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Gaussian Processes for Data-Efficient Learning in Robotics and Control",
      "Human-artificial interaction in the age of agentic AI: a system-theoretical approach",
      "Reinforcement learning in robotics: A survey"
    ]
  },
  {
    "arxiv_id": "2608.19134",
    "title": "SCORE: Subject Coordinate Recovery for Label-Free Cross-Subject EEG-to-Image Retrieval",
    "abstract": "Accurate visual decoding can reveal how the brain represents visual information and recover perceived content from neural signals such as electroencephalography (EEG), with potential for neural communication. However, current EEG-to-image retrieval methods perform far below their within-subject counterparts for new users without labeled calibration, limiting real-world deployment. To understand this gap, we analyze EEG features across subjects and find that different subjects preserve similar relationships among concepts but express them along different coordinate directions. We therefore propose Subject Coordinate Recovery (SCORE), a target label-free framework combining recovery-aware source training with coordinate alignment at deployment. During training, SCORE aligns source subject EEG with a common image space and simulates unseen-subject recovery through source-only episodes. At deployment, with both encoders frozen, SCORE selects reliable EEG-image landmarks through hubness-corrected matching and estimates an orthogonal transformation to recover target EEG coordinates without source data or target labels. In 200-way retrieval on two public benchmarks, SCORE outperforms the unadapted baseline for every target subject and achieves the best overall accuracy. It reaches 53.23%/83.55% and 12.01%/32.16% Top-1/Top-5 on THINGS-EEG2 and Alljoined-1.6M, respectively, surpassing the strongest baselines by 17.45/15.70 and 3.08/4.62 percentage points. Without target labels or enco",
    "categories": "cs.LG",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Cognition-Driven Structural Prior for Instance-Dependent Label Transition Matrix Estimation",
      "Towards a new approach to reveal dynamical organization of the brain using topological data analysis",
      "Cellpose 2.0: how to train your own model"
    ]
  },
  {
    "arxiv_id": "2608.15861",
    "title": "TransfHAR: Self-Supervised Wrist Representations for On-Demand Activity Recognition",
    "abstract": "Fine-grained wrist activity recognition can support applications such as procedural step guidance and context-aware assistance, yet acquiring labeled data for every new task, user, and activity granularity remains a bottleneck. We present TransfHAR, a self-supervised wrist IMU framework for on-demand, fine-grained activity recognition by learning transferable motion priors from global, unlabeled activities. We show that self-supervised pretraining on coarse wrist IMU activities (e.g., sitting, walking, exercise) learns motion structure rich enough to transfer to fine-grained manipulative, gestural, and procedural activities (e.g., snapping, stirring, waving) that are absent from pretraining. We implement TransfHAR as a real-time smartwatch application that lets users define and expand their own activity set for personalized recognition from only a few demonstrations. Across three offline cross-dataset evaluations, TransfHAR matches or exceeds fully supervised baselines that use complete label sets with equal or additional sensor channels, by 6.2 balanced-accuracy points on average. In an in-lab study with 10 participants each performing seven novel wrist activities, TransfHAR reaches 86.7% balanced accuracy across participants with five examples per class and 90.4% when updated from a single one-minute recording per class. These results indicate that broad self-supervised wrist pretraining provides an effective foundation for on-demand fine-grained activity recognition.",
    "categories": "cs.LG",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Cellpose 2.0: how to train your own model",
      "Knee Point-Based Imbalanced Transfer Learning for Dynamic Multiobjective Optimization",
      "Gaussian Processes for Data-Efficient Learning in Robotics and Control"
    ]
  },
  {
    "arxiv_id": "2608.17556",
    "title": "Reflex-Guard: A Low-Latency Guardrail for LLM Prompt Safety Using Dense Semantic Embeddings",
    "abstract": "Large Language Models (LLMs) in real-world applications often face the risks of specially crafted prompts designed to bypass the safety controls. Existing guardrail methods, such as LLM-as-a-judge and cloud-based safety APIs are able to detect unsafe content. However, they often add a delay of about 250-900 ms to each request. This delay is too high for real-time applications, when the system usually needs to respond in less than 100 ms. Furthermore, routing user prompts through external moderation endpoints raises significant data privacy concerns. This paper introduces Reflex-Guard, a lightweight guardrail that runs locally. It uses jailbreak-aware preprocessing, compact sentence-transformer embeddings, and seven fast binary classifiers. Together, these components enable high-accuracy prompt safety filtering with much lower latency than existing solutions. Through systematic evaluation on a strategically balanced dataset of 30,568 samples drawn from five complementary sources, we demonstrate that Reflex-Guard achieves 95.9% recall on harmful prompts at 37.6 ms end-to-end latency. It is faster than existing baselines, including Llama Guard 2 at 255 ms and SafeDecoding at 723 ms. It can detect 100% of GCG suffix attacks and Base64-encoded prompts using the default threshold. However, DrAttack structured prompts required lowering the threshold to 0.03 for optimal detection, as they produced a distinct probability distribution. Reflex-Guard achieves Reflex Efficiency Score (RES",
    "categories": "cs.CR cs.CL cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Privacy-Preserving Machine Learning With Fully Homomorphic Encryption for Deep Neural Network",
      "Generating Private Recommendations Efficiently Using Homomorphic Encryption and Data Packing",
      "Physical Layer Authentication and Security Design in the Machine Learning Era"
    ]
  },
  {
    "arxiv_id": "2608.19611",
    "title": "Forking Fast: Efficiently Estimating Uncertainty Dynamics in Text Generation",
    "abstract": "LLM reasoning is stochastic, and so understanding a model requires grappling with the distribution of reasoning chains that it might produce for a given question, i.e., its uncertainty. Resampling-based analyses characterize this distribution, revealing which steps of a rollout determine how the model arrives at its answer. However, a major limitation of these approaches is that resampling text sequences at every token or sentence in a reasoning chain is very costly. Our work strives to make resampling analysis more computationally efficient, while also shedding light on an important scientific question: what is the right statistical model for explaining uncertainty dynamics in text generation? We show that when resampling many reasoning chains, uncertainty dynamics converge to stable patterns, and noise is largely an artifact of sampling rather than an LLM's sensitivity to each individual token or reasoning step. We develop a statistical model for smoothing noisy low-sample rollout data to better approximate high-sample data, allowing us to significantly cut sampling costs.",
    "categories": "cs.CL cs.AI cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Evolutionary optimization of model merging recipes",
      "Mathematical discoveries from program search with large language models",
      "Generating Scenario Trees for Multistage Decision Problems"
    ]
  },
  {
    "arxiv_id": "2608.10240",
    "title": "Sequential Modality Dropout for Robust Multi-Modal Sequential Recommendation",
    "abstract": "Multi-modal sequential recommenders assume every item carries every modality, but real product catalogs often miss images or text, and a model trained on complete data loses much of its recommendation accuracy when a modality is unavailable at serving time. We propose Sequential Modality Dropout (SMD): during training, each modality stream (image and text) is independently erased with probability p for an entire user interaction history, so the model learns to predict the next item without relying on any single modality. We measure robustness by retention, the fraction of a model's full-modality accuracy (HR@10) that survives when a modality is removed at test time. Across four backbones (MM-SASRec, IISAN, MISSRec, and fMRLRec) on four Amazon domains, SMD raises text retention by 1.0 to 3.2x at essentially no cost to full-modality accuracy; under an extreme 95% per-item missing rate, it retains 61% of HR@10 versus 22% without (a 2.8x improvement). An optional cross-modal reconstruction loss further lifts retention from 90% to 98% on a simple additive backbone under severe text missingness. SMD is a four-line, architecture-agnostic change that makes multi-modal sequential recommenders robust to the missing modalities they actually encounter in deployment.",
    "categories": "cs.IR cs.LG cs.MM",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A Nonnegative Latent Factor Model for Large-Scale Sparse Matrices in Recommender Systems via Alternating Direction Method",
      "Smooth PARAFAC Decomposition for Tensor Completion",
      "An Efficient Approach for Assessing Hyperparameter Importance"
    ]
  },
  {
    "arxiv_id": "2608.08963",
    "title": "Fourier Self-Supervision for Fine-Grained Generalized Category Discovery",
    "abstract": "Generalized Category Discovery aims to recognize known categories while identifying novel ones within unlabeled data. Existing methods, typically based on self-supervision and contrastive learning, often struggle to capture fine-grained distinctions, relying on superficial visual cues rather than the intrinsic attributes humans use for categorization. We introduce Fourier Self-Supervision, that leverages the Fourier transform of images to enhance the discrimination of subtle differences and support the discovery of new categories. Our method employs a dual frequency filtering strategy: a low-pass filter first extracts broad, abstract attributes that capture high-level category information, while a high-pass filter emphasizes fine details such as edges and textures that are essential for fine-grained recognition. Each operates on a dedicated latent space, and their overlapping representations together yield a richer, more complete feature space. This dual-frequency approach not only refines feature extraction to identify novel categories, but also strengthens the model's discriminative power in fine-grained category discovery. Experiments on multiple fine-grained datasets show that incorporating Fourier Self-Supervision outperforms state-of-the-art methods, even when the number of classes is unknown, demonstrating its effectiveness for Generalized Category Discovery. Our code is available at: https://github.com/SarahRastegar/FourEx.",
    "categories": "cs.CV cs.AI cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Cellpose 2.0: how to train your own model",
      "Feature Learning for Image Classification Via Multiobjective Genetic Programming",
      "Topological deep learning: a review of an emerging paradigm"
    ]
  },
  {
    "arxiv_id": "2507.01354",
    "title": "Efficient Kilometer-Scale Precipitation Downscaling with Conditional Wavelet Diffusion",
    "abstract": "Effective hydrological modeling and extreme weather analysis demand precipitation data at a kilometer-scale resolution, which is significantly finer than the 10 km scale offered by standard global products like IMERG. To address this, we propose the Wavelet Diffusion Model (WDM), a generative framework that achieves 10x spatial super-resolution (downscaling to 1 km) and delivers a 9x inference speedup over pixel-based diffusion models. WDM is a conditional diffusion model that learns the learns the complex structure of precipitation from MRMS radar data directly in the wavelet domain. By focusing on high-frequency wavelet coefficients, it generates exceptionally realistic and detailed 1-km precipitation fields. This wavelet-based approach produces visually superior results with fewer artifacts than pixel-space models, and delivers a significant gains in sampling efficiency. Our results demonstrate that WDM provides a robust solution to the dual challenges of accuracy and speed in geoscience super-resolution, paving the way for more reliable hydrological forecasts.",
    "categories": "cs.LG physics.ao-ph",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Optimal Mass Transport: Signal processing and machine-learning applications",
      "Diffusion maps and coarse-graining: a unified framework for dimensionality reduction, graph partitioning, and data set parameterization",
      "Vector diffusion maps and the connection Laplacian"
    ]
  },
  {
    "arxiv_id": "2608.09350",
    "title": "A Machine Learning Based Search for Lunar Anomalies",
    "abstract": "The Lunar Reconnaissance Orbiter (LRO) has been collecting high-resolution images (at around 0.5-2 meters per pixel linearly with its Narrow Angle Camera) of the Moon since 2009, amassing a large dataset of images and offering researchers the opportunity to study the surface of the Moon at unprecedented scale. Here, we aim to test the abilities of the Beta-Variational Autoencoder (VAE) created by Lesnikowski et al. (2024), an unsupervised learning model which identifies anomalous features across the Moon's surface, locating not only scientifically useful geologic formations such as rockfall deposits, fresh impact craters, irregular mare patches, or volcanic pits/collapsed lava tubes, but also artificial objects such as landed spacecraft. This investigation further gauged the model's ability to locate anomalous surface features, successfully recovering two places of interest (Plaskett Crater and Paracelsus C Crater) and numerous landed technological assets at a statistically significant rate.",
    "categories": "astro-ph.EP cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Galaxy Zoo: reproducing galaxy morphologies via machine learning\u2605",
      "Feature Learning for Image Classification Via Multiobjective Genetic Programming",
      "Geometry of nonlinear least squares with applications to sloppy models and optimization"
    ]
  },
  {
    "arxiv_id": "2608.07528",
    "title": "The Knowing-Saying Gap: When Probes See Errors that Confidence Misses",
    "abstract": "Linear probes detect corrupted context in language models with near-perfect accuracy, yet this does not translate into reliable failure prediction. The result is a dissociation with direct implications for deployment monitoring. Across multi-hop arithmetic chains, probes that detect corruption turn out to be uninformative about final answer correctness; models forced into structured confidence formats collapse to two values with indistinguishable error rates; and probe persistence across hops fails to separate correct from incorrect outcomes, refuting our pre-registered \"persistence beats peak\" hypothesis. This pattern of knowing but not saying generalises across model families including reasoning models. As a real-time monitor, probe-based interventions are sharply model and error-type dependent: branch-and-pick is net-positive across models and uniquely non-breaking on Llama-3.1-8B (4 rescued, 0 broken), while reprompt and replace-prior break correct traces at roughly the rate they rescue wrong ones. Probe-based monitoring is a necessary complement to verbalised confidence, but no single intervention dominates, and the deployable answer is model-aware, error-type-aware routing.",
    "categories": "cs.AI cs.CL cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A Framework for Validation of Computer Models",
      "Quantification of Model Uncertainty: Calibration, Model Discrepancy, and Identifiability",
      "The Exploratory Modeling Workbench: An open source toolkit for exploratory modeling, scenario discovery, and (multi-objective) robust decision making"
    ]
  },
  {
    "arxiv_id": "2605.00062",
    "title": "RETO: A Rotary-Enhanced Transformer Operator for High-Fidelity Prediction of Automotive Aerodynamics",
    "abstract": "Rapid aerodynamic evaluation is crucial for modern vehicle design, yet existing neural operators struggle to capture intricate spatial correlations. We propose the rotary-enhanced transformer operator (RETO), a novel neural solver featuring a dual-stage spatial awareness mechanism: sinusoidal-cosine encodings for global referencing and rotary positional encodings (RoPE) for relative displacements. RoPE encodes spatial relations via unitary rotations, enforcing translation invariance and enhancing local gradient resolution. RETO is validated on ShapeNet and the high-fidelity DrivAerML benchmark. On ShapeNet, RETO achieves a relative $L_2$ error of 0.063, outperforming RegDGCNN at 0.125 and representing a 16\\% improvement over the Transolver baseline, which yields an error of 0.075. These performance gains are further amplified on the DrivAerML dataset, where RETO achieves relative $L_2$ errors of 0.089 for surface pressure and 0.097 for velocity. In comparison, Transolver results in errors of 0.116 and 0.121 for the same metrics, indicating that RETO achieves precision enhancements of 23\\% and 19\\%, respectively. For comprehensive comparison, the surface pressure and velocity errors for AB-UBT are 0.102 and 0.124, while RegDGCNN yields 0.235 and 0.312, respectively. Information-theoretical analysis shows that the entropy peak of RETO at 0.35 is significantly lower than that of Transolver at 0.75 under $10^4$ resolution, indicating a focused attentional mechanism capable of pre",
    "categories": "eess.IV cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Efficient Aerodynamic Shape Optimization with Deep-Learning-Based Geometric Filtering",
      "A point-cloud deep learning framework for prediction of fluid flow fields on irregular geometries",
      "Stress Field Prediction in Cantilevered Structures Using Convolutional Neural Networks"
    ]
  },
  {
    "arxiv_id": "2608.20360",
    "title": "TriPLU: Bypassing the Gate with Direct Trilinear Product FFNs in Tiny Language Models",
    "abstract": "We study whether tiny decoder-only language models benefit from feed-forward layers that directly multiply learned feature projections. TriPLU, a Trilinear Product Linear Unit, replaces the usual gated FFN branch with a product-only degree-3 branch that multiplies three projected streams coordinatewise. In a character-level TinyStories 1M-byte prefix study, TriPLU reaches a mean best validation loss of 1.0637, compared with 1.1017 for closely matched SwiGLU, 1.0780 for a degree-4 product control, and 1.1026 for a degree-2 control. In train-only Byte-BPE experiments, TriPLU also lowers validation and heldout bits per byte on TinyStories and WikiText-2 raw under low-learning-rate settings, with PMI-slice evidence suggesting gains on seen middle- and high-PMI adjacent-token pairs. Constant-learning-rate diagnostics show that product-branch normalization can reduce the high-learning-rate best-checkpoint gap, although final BPB still degrades under hot schedules. The resulting claim is deliberately narrow: direct product FFNs can improve fixed-budget small-model loss in specific low-compute regimes, but the branch is optimization-sensitive and does not establish FLOP-normalized efficiency, scaling behavior, or broad LLM performance.",
    "categories": "cs.CL cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Deep Learning with Limited Numerical Precision",
      "Channel Polarization: A Method for Constructing Capacity-Achieving Codes for Symmetric Binary-Input Memoryless Channels",
      "Branching and bounds tighteningtechniques for non-convex MINLP"
    ]
  },
  {
    "arxiv_id": "2608.06520",
    "title": "Online Security Learning in Cooperative Multi-Agent Systems under Hidden Byzantine Attacks",
    "abstract": "We study online cooperative control of a multi-agent system under Byzantine attacks. Namely, an unknown, fixed subset of agents are Byzantine comprised and can stealthily overwrite its own coordinates of the team's planned joint action after observing that plan. The learner observes planned actions, public rewards, and public states, but neither the overwrite nor the executed joint action. Our objective is security: to optimize the team performance against the worst overwrites and achieve the optimal security value. We first show that the attacker's information determines the geometry. An attacker that observes the planned action induces an exact $(s,a)$-rectangular robust Markov decision process (MDP) whose rows are convex hulls of overwrite-induced public-outcome laws, whereas a blind attacker induces an $s$-rectangular model. We then identify the information-theoretic limit of security learning, showing that the security regret decomposes exactly into return regret against the response generating the data and a cumulative response gap $D_K$. Two indistinguishable horizon-one instances force $\\Omega(K)$ expected security regret while return regret is zero, showing that dependence on $D_K$ is unavoidable. Finally, we develop a stage-tied robust estimation-to-decisions learner and prove a regret bound of $\\widetilde{\\mathcal O}\\!\\left(H^2S\\sqrt{AK}\\right)+\\mathbb E[D_K]$. Our studies thus provide comprehensive theoretical and algorithmic foundations of reliable multi-agent sy",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Information-Theoretic Regret Bounds for Gaussian Process Optimization in the Bandit Setting",
      "Multi-objective reinforcement learning using sets of pareto dominating policies",
      "The Operational Meaning of Min- and Max-Entropy"
    ]
  },
  {
    "arxiv_id": "2608.15602",
    "title": "FluxBin: Flexible LUT-based Ultra-low-bit LLM Inference by Algorithm-Kernel Synergy",
    "abstract": "While binary quantization theoretically promises extreme compression and acceleration for Large Language Models (LLMs), existing research often overlooks the necessity of specialized hardware kernels, thus failing to unleash the full acceleration potential due to persistent reliance on expensive floating-point arithmetic or runtime dequantization overheads. To bridge this gap, we propose FluxBin (\\textbf{F}lexible \\textbf{L}UT-based \\textbf{U}ltra-low-bit e\\textbf{X}ecution with \\textbf{Bin}ary bases), an algorithm-kernel co-design that synergizes post-training quantization with a highly optimized CUDA kernel. Algorithmically, we introduce Decoupled Row-Column Binary Decomposition to enhance representational capacity while maintaining hardware efficiency, complemented by a Hessian-guided saliency-aware hybrid bases that preserve critical information. At the kernel level, we implement a Lookup Table Building Approach with Scale Fusion to reduce floating-point arithmetic, featuring a Virtual Columnar Mapping that transforms irregular, sparse, and salient matrices into dense execution. Extensive evaluations demonstrate FluxBin achieves up to $5.92\\times$ speedup and $10.19\\times$ energy savings across diverse model architectures, delivering comparable accuracy to heavily fine-tuned methods. This effectively enables the deployment of 70B-scale models on one single A100 GPU with a $4\\times$ memory reduction. Code is available at https://github.com/nicyyyy/FluxBin.",
    "categories": "cs.LG cs.AI",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Deep Learning with Limited Numerical Precision",
      "Fixed-Rate Compressed Floating-Point Arrays",
      "Ecient Sparse Matrix-Vector Multiplication on CUDA"
    ]
  },
  {
    "arxiv_id": "2606.28455",
    "title": "Event-Conditioned Diagnostics of Kinematic, Contact, and Object-Permanence Fields in Passive Object-State World Models",
    "abstract": "World models can predict future physical states, but prediction accuracy alone does not explain how physical information is organized and used inside their latent dynamics. We introduce a controlled diagnostic protocol for studying event-conditioned latent physical structure in passive object-state world models. The protocol tests whether hidden representations encode event-regime information, whether event contexts reweight non-exclusive physical field readouts, and whether field-aligned representational components have functional consequences for prediction. Using a balanced controlled-generator dataset with free-motion, collision, and occlusion events, we evaluate recurrent, attention-based, and latent state-space transition models under a fixed-horizon forecasting setup. The models learn useful predictive dynamics and their hidden states support reliable event-regime readout. Event contexts systematically reweight kinematic, contact, and object-permanence field readouts: free motion is kinematic-dominant, collision combines kinematic and contact structure, and occlusion combines motion-related and object-permanence structure. Time-aligned and directional-consistency analyses further show phase-related shifts in field emphasis. Finally, fixed-horizon projection causal field effect (CFE) shows that suppressing field-aligned directions can degrade event-relevant prediction, with strongest evidence for contact-aligned structure in collision-contact windows and more qualified ",
    "categories": "cs.RO cs.AI cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A point-cloud deep learning framework for prediction of fluid flow fields on irregular geometries",
      "Computer Model Calibration Using High-Dimensional Output",
      "Learning about physical parameters: the importance of model discrepancy"
    ]
  },
  {
    "arxiv_id": "2608.21209",
    "title": "Personalized Privacy Control in LLMs via Attention Head Intervention",
    "abstract": "The rise of agentic AI enables LLMs to access diverse user data, raising critical privacy concerns. Prior work on contextual privacy studies whether LLMs regulate information disclosure according to context-dependent norms. However, acceptable disclosure boundaries may vary across users even within the same context. To address this limitation, we introduce \\textit{personalized privacy}, which incorporates user-specific disclosure preferences into privacy control. We further present P3Bench~(\\textbf{P}ersonalized \\textbf{P}rivacy \\textbf{P}reservation \\textbf{Bench}mark), a novel benchmark extending contextual privacy policies with personalized disclosure policies. Experiments show that prompt-based policies fail to reliably enforce personalized privacy policies, with Qwen2.5-7B and Gemma3-4B showing average policy ignorance ratios of 51.25\\% and 74.28\\%, respectively. Finally, to address this problem, we propose \\textsc{Repair}, a robust inference-time attention head intervention method that adjusts disclosure behavior toward policy-consistent responses. Our method significantly improves adherence to user-specific privacy preferences by reducing cases where the model fails to follow the given policy.",
    "categories": "cs.AI cs.CL cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "An overview of large AI models and their applications",
      "Combining fragmentation and encryption to protect privacy in data storage",
      "Searchable Symmetric Encryption with Forward Search Privacy"
    ]
  },
  {
    "arxiv_id": "2606.30528",
    "title": "$\\mu$Flow: Leveraging Average Images for Improving Generalisation of Deepfake Faces Detectors",
    "abstract": "Current generative models, including GANs and diffusion models, have reached an outstanding level of photorealism, posing significant risks to privacy and security. To ensure real-world applicability, deepfake detectors must generalise effectively to unseen generators. However, most existing approaches rely on supervised training with both real and fake images, which limits their generalisation especially across generators categories (e.g. GANs vs DMs). In this work, we introduce $\\mu$Flow, a one-class deepfake detector trained only on real images without relying on pseudo-deepfakes or synthetic artifacts. Our approach builds on the observation that averaging multiple images amplifies consistent generative traces, producing highly discriminative feature representations. We leverage this property by modelling the distribution of features extracted from averaged images and training a normalizing flow to align the feature space of individual images with this distribution. This alignment yields a likelihood-based criterion that separates real and fake samples while promoting strong generalisation. We evaluate $\\mu$Flow on a fully out-of-distribution setting, where both real and fake datasets are unseen during training. Experimental results show that our method significantly outperforms SOTA detectors. Project page: https://opontorno.github.io/MuFlow.",
    "categories": "cs.CV cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Evolutionary Multiobjective Optimization Driven by Generative Adversarial Networks (GANs)",
      "Generative artificial intelligence: a historical perspective",
      "Cellpose 2.0: how to train your own model"
    ]
  },
  {
    "arxiv_id": "2608.14747",
    "title": "WANDR: A Benchmark for Wide and Deep Research",
    "abstract": "WANDR (Wide ANd Deep Research) is a benchmark of 500 realistic, challenging data-collection tasks for research agents. Each task requires a system to discover a large set of entities that satisfy specified criteria (breadth), investigate each entity through multiple coordinated web searches (depth), and return independently verifiable records with supporting sources and excerpts. Tasks are represented as qualification key hierarchies that specify the entities, relationships, evidence, and required count at each level; a hierarchy with n companies, m employees per company, and k sources per employee requires n x m x k records. This structure supports diverse workflows such as market mapping, due diligence, literature review, product comparison, and talent sourcing, with targets ranging from dozens to thousands of records. WANDR replaces static gold answer sets with task-specific judges that refetch cited pages and verify each record against its evidence, allowing evaluation of current and changing facts. Record verdicts are aggregated into soft and hard precision, recall, and F1 scores that distinguish factual quality, coverage, and hierarchical completeness. The tasks are derived from de-identified product-usage logs and produced through a semi-automated pipeline with automated checks, empirical audits, and human review where needed. We evaluate six production research systems and find that the benchmark is far from saturated: at high effort, the strongest system reaches only",
    "categories": "cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Hyperparameter Tuning in Machine Learning: A Comprehensive Review",
      "An Efficient Approach for Assessing Hyperparameter Importance",
      "An Adaptive Archive-Based Evolutionary Framework for Many-Task Optimization"
    ]
  },
  {
    "arxiv_id": "2608.20572",
    "title": "Faults That Fortify: CNN Adversarial Robustness via GPU Undervolting",
    "abstract": "Convolutional Neural Networks (CNNs) face a dual challenge: vulnerability to adversarial attacks and prohibitive training cost. Adversarial training is effective but expensive, a burden that grows as learning shifts to the energy-constrained edge. This paper addresses both through GPU undervolting during training. Reducing supply voltage introduces stochastic perturbations that act as implicit regularization, improving robustness while lowering power. We characterize undervolting-induced faults at the bit level, then train LeNet, VGG-6, and MobileNetV3 on MNIST and CIFAR-10 under two training regimes, standard and adversarial, each at nominal and undervolted voltage, and evaluate all models against adversarial attacks. In both regimes, the undervolted model consistently achieves higher adversarial accuracy than its nominal-voltage counterpart, showing that hardware-induced faults strengthen even adversarial training. Because dynamic power scales quadratically with supply voltage, these robustness gains arrive with substantial energy savings. GPU undervolting is therefore a readily deployable hardware-level defense requiring no algorithmic change, and opens a promising direction in which robustness and energy efficiency move together.",
    "categories": "cs.LG cs.AR cs.CR",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Deep Learning with Limited Numerical Precision",
      "Meta-heuristics and deep learning for energy applications: Review and open research challenges (2018\u20132023)",
      "Gradient descent finds global minima of deep neural networks"
    ]
  },
  {
    "arxiv_id": "2607.17417",
    "title": "Grounded verification of chemical and materials reasoning: detection is the bottleneck",
    "abstract": "Language models are moving into chemistry and materials discovery workflows, where a wrong molecular formula, space group, or formation energy can silently propagate into downstream decisions. These confabulations hide inside fluent reasoning traces and concentrate on rare, long-tail entities, where model confidence is least trustworthy. Retrieving reference data for every prompt would catch them, but at a heavy coverage and abstention cost. We show that deterministic, database-grounded verification catches and repairs these errors selectively, and that the binding constraint is detection rather than repair. Our tiered verifier extracts each checkable claim, tests it against authoritative databases and physical law, and retrieves a reference value only when a check fails. Across four models and over five hundred prompts with pinned conditions, gated correction cuts the error rate of committed formulas from 22% to 4% with 3.2 times fewer retrievals than blanket augmentation, and it outperforms a conversational retrieval oracle when every answer, corrected or not, is scored. When a flag fires, repair almost always succeeds; the benefit reaches the final answer only where the verifier's scope covers it and where long-tail error exists. Checkable claims, checked cheaply, are a practical lever for trustworthy machine reasoning in chemistry.",
    "categories": "cs.LG physics.chem-ph physics.comp-ph quant-ph",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Mathematical discoveries from program search with large language models",
      "Evolutionary optimization of model merging recipes",
      "Delegating Computation"
    ]
  },
  {
    "arxiv_id": "2607.28633",
    "title": "Topology-Aware Data Movement for Disaggregated GPU Inference",
    "abstract": "Disaggregated LLM inference creates a datacenter networking problem that no existing system solves correctly. When prefill and decode run on separate GPU pools, the KV cache must be transferred between them. For a 70B model this is 1.3 GB per request, exceeding 100 GB/s aggregate at production scale. Yet DistServe, Splitwise, and Mooncake all use uniform RDMA, ignoring that bandwidth between two GPUs varies by 72x depending on their physical relationship: 900 GB/s via NVLink 4.0 within a domain (1.8 TB/s on NVLink 5, widening the gap to 144x), 50 GB/s via InfiniBand across nodes, 12.5 GB/s via TCP across data centers. We design a topology-aware transfer orchestrator that discovers interconnect hierarchy at startup and selects optimal transport per transfer. Three mechanisms work together: (1) pipelined layer-by-layer transfer that overlaps transmission with ongoing prefill, hiding 76 to 100 percent of transfer latency behind computation depending on transport, with NVLink and PCIe transfers hidden entirely; (2) NVLink domain-aware placement for Mixture-of-Experts models that co-optimizes expert dispatch with KV cache locality; and (3) CXL 3.0 memory expanders as a shared overflow tier providing 6x capacity at 86x lower latency than NVMe. Full evaluation requires multi-node clusters with heterogeneous interconnects and CXL 3.0 hardware that is beyond academic resources and not yet available in GPU clouds. We present analytical bandwidth models, component implementations, and p",
    "categories": "cs.LG cs.AI cs.PF",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A unified approach to approximating resource allocation and scheduling",
      "Ecient Sparse Matrix-Vector Multiplication on CUDA",
      "Parallel metaheuristics: recent advances and new trends"
    ]
  },
  {
    "arxiv_id": "2605.20254",
    "title": "Efficient Table QA via TableGrid Navigation and Progressive Inference Prompting",
    "abstract": "Large Language Models (LLMs) have shown promising results on NLP tasks, however, their performance on tabular data still needs research attention, because Table Question-Answering (TQA) requires precise cell retrieval and multi-step structured reasoning. Existing work improves TQA either by fine-tuning or training LLMs on task-specific tabular data, but often lacks verifiable control over how the model navigates tables and derives answers. In this work, we propose a training-free TQA approach with two structured prompting frameworks: TableGrid Navigation (TGN), which iteratively navigates rows and columns via a three-module loop to locate evidence and refine answers, and Progressive Inference Prompting (PIP), which enforces columns identification for explicit progressive row selection constraint according to the query. We evaluate 17 LLMs against 6 baselines on TableBench and FeTaQa dataset. On TableBench, TGN improves over the strongest baseline by 3.8 points, and on FeTaQa, PIP achieves SOTA performance over ReAct and Chain-of-Thought. Beyond inference-time gains, PIP and TGN can also serve as supervision templates to fine-tune small models, narrowing the performance gap to much larger architectures in resource-constrained settings, offering versatile and cost-efficient solution for TQA.",
    "categories": "cs.IR cs.AI cs.CV cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Evolutionary optimization of model merging recipes",
      "Generative AI and Prompt Engineering: The Art of Whispering to Let the Genie Out of the Algorithmic World",
      "Mathematical discoveries from program search with large language models"
    ]
  },
  {
    "arxiv_id": "2508.17092",
    "title": "Enhancing Knowledge Tracing through Leakage-Free and Recency-Aware Embeddings",
    "abstract": "Knowledge Tracing (KT) aims to predict a student's future performance based on their sequence of interactions with learning content. Many KT models rely on knowledge concepts (KCs), which represent the skills required for each item. However, some of these models are vulnerable to label leakage, a phenomenon in which the input data inadvertently reveal the correct answer, particularly in datasets with multiple KCs per question. We propose a straightforward yet effective solution to prevent label leakage by masking ground-truth labels during input embedding construction whenever such leakage could occur. To accomplish this, we introduce a dedicated \\texttt{MASK} label, inspired by masked language modeling (e.g., BERT), to replace ground-truth labels. In addition, we introduce Recency Encoding, which encodes the step-wise distance between the current item and its most recent previous occurrence. This distance is important for modeling learning dynamics such as forgetting, which is a fundamental aspect of human learning, yet it is often overlooked in existing models. Recency Encoding demonstrates improved performance over traditional positional encodings on multiple KT benchmarks. We show that incorporating our embeddings into KT models such as DKT, DKT+, AKT, and SAKT consistently improves prediction accuracy across multiple benchmarks. The approach is both efficient and widely applicable.",
    "categories": "cs.CY cs.AI cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Evolutionary optimization of model merging recipes",
      "Cognition-Driven Structural Prior for Instance-Dependent Label Transition Matrix Estimation",
      "GPT-3: Its Nature, Scope, Limits, and Consequences"
    ]
  },
  {
    "arxiv_id": "2512.10853",
    "title": "Multidimensional Sorting: Comparative Statics",
    "abstract": "Characterizing multidimensional sorting problems is notoriously difficult - solutions are known only for a small number of examples. Our main results completely characterize the comparative statics of sorting and earnings with respect to technological change for a general class of multidimensional assignment models. We show that symmetric technological change passes fully into worker earnings, while antisymmetric change results only in reallocation. In general, both margins adjust, with relative importance governed by the complementarity between workers and jobs and their distributions. To quantitatively illustrate our theory, we quantify responses in sorting and earnings to cognitive skill-biased technological change for U.S. data.",
    "categories": "econ.GN math.OC q-fin.EC",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Designing Random Allocation Mechanisms: Theory and Applications",
      "Statistical ranking and combinatorial Hodge theory",
      "An Efficient Approach to Nondominated Sorting for Evolutionary Multiobjective Optimization"
    ]
  },
  {
    "arxiv_id": "2608.17087",
    "title": "Backward through Time, Algebraically",
    "abstract": "Linear temporal logic is a modal extension of propositional logic that allows one to state how a system should behave over time. Its canonical domain is the booleans, but discretely-valued judgements are of little use in steering softly-valued systems (neural policies, adaptive controllers, sequence models, etc). In such cases, the goal formula's (dis)satisfaction becomes a training signal, and differentiability becomes a prime concern. Candidate differentiable semantics abound, but navigating them is tricky. Implementations, where available, are shallow embeddings, demanding an upfront commitment to a single semantic algebra and its (usually implicit) conduct. The paper casts the reader as a functional programmer asked to come to terms with this predicament, and refusing. Out of that refusal comes an evaluation engine that is algebra-generic and amenable to differentiation, together with an executable specification of the algebras it can accept. Various algebras are implemented and audited for their behavior, both forward and backward. Each algebra turns out to be a choice of which direction to disappoint, and how. Everything described (and more) is part of the PyTorch library telos, to be found at https://github.com/konstantinosKokos/telos.",
    "categories": "cs.LG cs.LO cs.PL cs.SY eess.SY",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "The T OPAS symbolic computation system",
      "Explicit Provability and Constructive Semantics",
      "Conservative logic"
    ]
  }
]
```

## Output

One JSON object per abstract, one per line, no prose. Every input `arxiv_id`
appears exactly once. Include `ambiguous` even when false.
