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
  },
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
  }
]
```

## Output

One JSON object per abstract, one per line, no prose. Every input `arxiv_id`
appears exactly once. Include `ambiguous` even when false.
