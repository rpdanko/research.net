# triage batch 5/5 — domain: compbio_methods

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
  },
  {
    "arxiv_id": "2608.20318",
    "title": "AI4AI-Bench: Benchmarking LLM Agents in Algorithmic Design for Recursive Self-Improvement",
    "abstract": "Recursive self-improvement (RSI) asks whether an AI system can improve the process that produces AI systems, so that the next system inherits the improvement. That process is the training algorithm: a better objective or update rule improves the compute\\mbox{-}capability exchange rate for every subsequent run, including the one that produces the next agent. Whether RSI is feasible therefore turns on whether an agent can design training algorithms. No benchmark isolates that ability: existing suites are won by collecting data or by tuning hyperparameters, and none tells a change to how a run is executed apart from a change to how the model learns. We present AI4AI\\mbox{-}Bench, 10 frozen research repositories spanning 10 training algorithm families. In each task, an agent has 4 hours on one B300 to rewrite the training algorithm; its code is then rerun from scratch for up to 12 hours and scored by a fixed evaluator hidden from the agent, against the repository's original algorithm under the same procedure. Because the 10 metrics are incommensurable, every task is mapped onto one scale on which $0$ is an uninformative model, $0.1$ is the algorithm the repository ships, and $1.0$ is the task optimum. Across 29 configurations of 6 systems on all 10 tasks the mean score is $0.166$, and the best system reaches $0.250$: even the strongest closes under a fifth of the distance between the algorithm that was already there and the optimum. The submissions show where that distance went: ",
    "categories": "cs.AI cs.CL cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "An overview of large AI models and their applications",
      "Classification of adaptive memetic algorithms: a comparative study",
      "Using machine learning as a surrogate model for agent-based simulations"
    ]
  }
]
```

## Output

One JSON object per abstract, one per line, no prose. Every input `arxiv_id`
appears exactly once. Include `ambiguous` even when false.
