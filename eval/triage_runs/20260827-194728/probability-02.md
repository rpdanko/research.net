# triage batch 2/2 — domain: probability

Charter: `charters/probability.md` — read it first, it is authoritative.

## In scope — 25 exemplars from the canon

- **Rank-Normalization, Folding, and Localization: An Improved Rˆ for Assessing Convergence of MCMC (with Discussion)** (2020) — IN SCOPE: add a one-line reason
- **Particle Markov Chain Monte Carlo Methods** (2010) — IN SCOPE: add a one-line reason
- **Distributionally Robust Stochastic Optimization with Wasserstein Distance** (2022) — IN SCOPE: add a one-line reason
- **Measurement of the Ratios of Branching Fractions <mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML" display="inline"><mml:mi mathvariant="script">R</mml:mi><mml:mo stretchy="false">(</mml:mo><mml:msup><mml:mi>D</mml:mi><mml:mo>*</mml:mo></mml:msup><mml:mo stretchy="false">)</mml:mo></mml:math> and <mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML" display="inline"><mml:mrow><mml:mi mathvariant="script">R</mml:mi><mml:mo stretchy="false">(</mml:mo><mml:msup><mml:mrow><mml:mi>D</mml:mi></mml:mrow><mml:mrow><mml:mn>0</mml:mn></mml:mrow></mml:msup><mml:mo stretchy="false">)</mml:mo></mml:mrow></mml:math>** (2023) — IN SCOPE: add a one-line reason
- **Data-Driven Distributionally Robust Optimization Using the Wasserstein Metric: Performance Guarantees and Tractable Reformulations** (2017) — IN SCOPE: add a one-line reason
- **Data-driven discovery of partial differential equations** (2017) — IN SCOPE: add a one-line reason
- **Monte Carlo Statistical Methods** (2000) — IN SCOPE: add a one-line reason
- **Near-ideal model selection by ℓ1 minimization** (2008) — IN SCOPE: add a one-line reason
- **Hanson-Wright inequality and sub-gaussian concentration** (2013) — IN SCOPE: add a one-line reason
- **Piecewise linear quadratic optimal control** (2000) — IN SCOPE: add a one-line reason
- **Lorentzian polynomials** (2020) — IN SCOPE: add a one-line reason
- **Constructing Summary Statistics for Approximate Bayesian Computation: Semi-Automatic Approximate Bayesian Computation** (2012) — IN SCOPE: add a one-line reason
- **Probabilistic Inference Using Markov Chain Monte Carlo Methods** (2011) — IN SCOPE: add a one-line reason
- **Crossings and nestings of matchings and partitions** (2006) — IN SCOPE: add a one-line reason
- **Matrix estimation by Universal Singular Value Thresholding** (2014) — IN SCOPE: add a one-line reason
- **Robust Stochastic Approximation Approach to Stochastic Programming** (2009) — IN SCOPE: add a one-line reason
- **Sparsity in multiple kernel learning** (2010) — IN SCOPE: add a one-line reason
- **The composite absolute penalties family for grouped and hierarchical variable selection** (2009) — IN SCOPE: add a one-line reason
- **Convergence in law of the minimum of a branching random walk** (2013) — IN SCOPE: add a one-line reason
- **Sparse principal component analysis and iterative thresholding** (2013) — IN SCOPE: add a one-line reason
- **Examples of Adaptive MCMC** (2009) — IN SCOPE: add a one-line reason
- **Reliable mixed passive and filtering for semi‐Markov jump systems with randomly occurring uncertainties and sensor failures** (2014) — IN SCOPE: add a one-line reason
- **Tuning parameter selectors for the smoothly clipped absolute deviation method** (2007) — IN SCOPE: add a one-line reason
- **Riemann Manifold Langevin and Hamiltonian Monte Carlo Methods** (2011) — IN SCOPE: add a one-line reason
- **A weak instrument <mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML" altimg="si3.gif" display="inline" overflow="scroll"><mml:mi>F</mml:mi></mml:math>-test in linear IV models with multiple endogenous variables** (2015) — IN SCOPE: add a one-line reason

## Out of scope — near misses

_Highly cited and topically adjacent. These are the traps._

- **K-Alpha Calculator–Krippendorff's Alpha Calculator: A user-friendly tool for computing Krippendorff's Alpha inter-rater reliability coefficient** (2024) — OUT: Software paper
- **Importance Nested Sampling and the MultiNest Algorithm** (2019) — OUT: Too rudimentary
- **Human error: models and management** (2000) — OUT: Not really probability theory at all
- **The Journal of Strength and Conditioning Research** (2013) — OUT: Strength and conditioning not probability
- **Eigenvalue-based spectrum sensing algorithms for cognitive radio** (2009) — OUT: Specific to radio
- **Climate as a moderator of the relationship between leader-member exchange and content specific citizenship: Safety climate as an exemplar.** (2003) — OUT: Do not include psychology paper


## Abstracts

Each carries a `band` computed before you saw it, the `threshold` that band
implies, and the titles of its nearest canon neighbours. Score on merit first,
then apply the threshold.

```json
[
  {
    "arxiv_id": "2608.14978",
    "title": "An Idealized Delay-Differential Model of Scuba Diver Porpoising and Runaway Ascent",
    "abstract": "A scuba diver holding constant depth balances on an unstable equilibrium: the gas carried in the suit and buoyancy compensator compresses with depth, so the buoyant force falls as the diver sinks and rises as the diver ascends. We represent the diver as a proportional-derivative controller that regulates this compressible-buoyancy saddle after a finite reaction delay, and we derive the governing delay differential equation from the vertical force balance and the isothermal gas law, reducing it to a damping ratio, two control gains, and a dimensionless delay. The characteristic spectrum, obtained by pseudospectral collocation of the semigroup generator and checked against a direct Newton solution of the characteristic equation, locates the Hopf boundary that separates stable hovering from sustained porpoising; for the baseline diver the critical reaction delay is 3.36 s and the onset period is 28.8 s. The bifurcation is supercritical, and because the saturating force is the quadratic hydrodynamic drag, the limit-cycle amplitude grows in proportion to the delay excess rather than as its square root. The safe-operating envelope shows that runaway ascent is triggered by saturation of the compensator, not by loss of linear stability, so a stable and an unstable diver can share the same escape threshold. As onset is approached, the lag-one autocorrelation and variance rise while the fitted recovery rate falls and matches the spectral abscissa, giving an eigenvalue-exact early warni",
    "categories": "nlin.CD cs.SY eess.SY math.DS physics.bio-ph",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Semi\u2010discretization method for delayed systems",
      "Nonmodal Stability Theory",
      "Non-intrusive reduced-order modeling for fluid problems: A brief review"
    ]
  },
  {
    "arxiv_id": "2608.11071",
    "title": "Scaling Laws for Majority-based Opinion Dynamics in the Presence of Stubborn Agents",
    "abstract": "In a multi-agent system, there are often stubborn followers of specific opinions or beliefs. Motivated by this observation, in this paper, we aim to understand how stubborn agents affect the distribution of opinions in a network where both stubborn and non-stubborn agents interact with each other. To do so, we assume that all agents have an opinion in the set $\\{0,1\\}$ and each non-stubborn agent updates its opinion according to the $2k$\\textit{-choices rule}, where the agent samples $2k$ neighbours (including both stubborn and non-stubborn neighbours) uniformly at random and adopts the majority opinion among the sampled group of neighbours and itself. We assume that a proportion of agents, $\\gamma_i$, are stubborn followers of opinion $i\\in \\{0,1\\}$. It is natural to expect that the steady-state distribution of the opinions in the network will be dominated by the opinion with the larger proportion of stubborn followers. We show that while this is true, the time to reach steady-state depends heavily on the values of the parameters $\\gamma_0$ and $\\gamma_1$. When the individual values of these parameters, as well as their difference, are small, it can take an exponentially long time (in the network size) to reach the steady-state. In sharp contrast, when at least one of the parameters $\\gamma_0$ and $\\gamma_1$ is large, the network reaches the steady-state in a time that is only logarithmic in the network size. Hence, there exists a sharp phase transition in the network dynami",
    "categories": "math.PR cs.MA",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "The stability\u2013complexity relationship at age 40: a random matrix perspective",
      "Efficient Monte Carlo and greedy heuristic for the inference of stochastic block models",
      "Decentralized Federated Averaging"
    ]
  },
  {
    "arxiv_id": "2608.09092",
    "title": "Exact Periodicity, Surjectivity, and a Haar Limit Law for a Restarting Josephus Process",
    "abstract": "We study a restarting Josephus process in which the participants retain their linear order and counting restarts at the current leftmost survivor after every deletion. For step size $m$, put $q=m-1$, and let $F_n(q)$ denote the initial position of the survivor. Reverse insertion gives $F_1(q)=1$ and $F_k(q)=F_{k-1}(q)+\\mathbf{1}_{\\{q\\bmod k<F_{k-1}(q)\\}}$. Writing $L_n=\\operatorname{lcm}(1,\\ldots,n)$, we establish three results for the compatible residue system in this recurrence. First, the full period group of $F_n$ is exactly $L_n\\mathbb{Z}$. Second, $F_n$ is surjective onto $\\{1,\\ldots,n\\}$. The proof is constructive and unconditional but computer-assisted: a Chinese-remainder construction and explicit prime estimates reduce it to a finite exact certificate. Third, if $\\widetilde Q_n$ is uniform modulo $L_n$, then $(F_n(\\widetilde Q_n)-1)/(n-1)$ converges to a symmetric, nondegenerate law on $[0,1]$. A common Haar coupling yields almost-sure and $L^r$ convergence for every $1\\le r<\\infty$, together with an $O(n^{-1/4})$ bound in $W_1$. Logarithmic boundary-mass estimates rule out every symmetric beta law. We also formulate endpoint dominance as an open problem, prove strict dominance over the two nearest internal positions for every $n\\ge4$, exclude prime levels as minimal counterexamples, and verify the claim exactly through $n=49$.",
    "categories": "math.CO math.PR",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Almost all orbits of the Collatz map attain almost bounded values",
      "Algebraic aspects of increasing subsequences",
      "The importance of the Selberg integral"
    ]
  },
  {
    "arxiv_id": "2606.07914",
    "title": "Identifiability and Estimation for Unlabeled Finite Mixtures under Marginal Independence",
    "abstract": "We study component recovery and mixing-matrix estimation from unlabeled finite mixtures whose observable distributions share the same latent components but have unknown mixing weights. The main identifying signal is marginal independence: each component is assumed to be independent on at least one coordinate pair, but no labels, clean component samples, or mixing weights are observed. We first prove a structural result for product components: under a subset-rank condition on the spans of the univariate marginals, any independent affine combination of the components must coincide with a single component. We then extend this principle to observable mixtures and show that, under the corresponding subset-rank, full-rank, and no-cancellation conditions, marginally independent affine combinations recover the corresponding latent components. When every component is independent on some coordinate pair, all components are identifiable, and the mixing matrix is recoverable under the stated completion conditions. Finally, we propose a Product-Marginal Maximum Mean Discrepancy (PM-MMD) estimator over affine combinations of the observable mixtures and prove uniform convergence and stability under approximate marginal independence. This framework also separates the empirical roles of the assumptions: irreducibility is, in general, not directly testable from the unlabeled mixtures alone, whereas marginal independence yields a candidate-level diagnostic through held-out PM-MMD. Controlled an",
    "categories": "stat.ML cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Identifiability of parameters in latent structure models with many observed variables",
      "On-Line Expectation\u2013Maximization Algorithm for latent Data Models",
      "Properties of Coherent Systems with Dependent Components"
    ]
  }
]
```

## Output

One JSON object per abstract, one per line, no prose. Every input `arxiv_id`
appears exactly once. Include `ambiguous` even when false.
