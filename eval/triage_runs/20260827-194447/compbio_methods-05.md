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
