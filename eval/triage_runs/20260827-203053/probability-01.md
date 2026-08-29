# triage batch 1/2 — domain: probability

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
    "arxiv_id": "2605.29769",
    "title": "Surrogate modeling for convection-dominated parametric problems based on error learning",
    "abstract": "Convection-dominated problems are known for their slow Kolmogorov $n$-width decays and are challenging for model order reduction (MOR). In this work, we propose a hybrid surrogate modeling approach and a non-intrusive variant that overcome some drawbacks of linear MOR methods. The proposed hybrid surrogate model is a projection-based reduced-order model (ROM), corrected by the error learned from a deep neural network. With the aid of deep learning, the model component of the surrogate model can be kept in a small reduced dimension. The neural network component and the model component are sequentially but separately built during the offline stage. At the online stage, they are easily coupled to output the solution predictions. Due to the intrusive nature of the hybrid-ROM, the numerically discretized operators of the original model must be available. For problems solved using black-box solvers, where the details of the numerical discretization are not accessible, we further propose a non-intrusive variant of the hybrid surrogate. Compared to the existing MOR methods with nonlinear manifolds, the proposed hybrid ROM is more easily built and is also easily assembled for online prediction. In contrast to the surrogate modeling approaches purely based on deep-learning, the proposed non-intrusive variant has a lighter neural network structure with much fewer parameters to be learned. We test the proposed methods on two nonlinear convection parametric problems. The first is the 1D inviscid Burgers' equation with one parameter, and the second is the 2D inviscid Burgers' equation with two parameters. Since both methods are based on error correction, their online predictions exhibit higher accuracy yet with largely reduced prediction time, compared to state-of-the-art methods.",
    "categories": "math.DS",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Multi-fidelity reduced-order surrogate modelling",
      "Generalised Latent Assimilation in Heterogeneous Reduced Spaces with Machine Learning Surrogate Models",
      "Fast Predictions of Aircraft Aerodynamics Using Deep-Learning Techniques"
    ]
  },
  {
    "arxiv_id": "2401.16556",
    "title": "Duality of causal distributionally robust optimization",
    "abstract": "We study distributionally robust optimization (DRO) in a dynamic context, where model uncertainty is captured by penalizing potential models based on their adapted Wasserstein distance to a reference model. We consider both discrete- and continuous-time settings and derive dynamic duality formulas that reformulate the worst-case expectation as a tractable minimax problem. The inner maximization admits a recursive representation in discrete time, while in continuous time, it is characterized by a path-dependent Hamilton--Jacobi--Bellman equation. We further extend these duality results from the worst-case expectation to the worst-case expected shortfall, a non-linear expectation. Finally, we apply this framework to optimal stopping problems in discrete time. We recast the original problem as a classical Wasserstein DRO on a nested space by introducing a novel relaxation that considers stopping times with respect to general filtrations.",
    "categories": "math.PR math.OC",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Distributionally Robust Stochastic Optimization with Wasserstein Distance",
      "Data-Driven Distributionally Robust Optimization Using the Wasserstein Metric: Performance Guarantees and Tractable Reformulations",
      "Wasserstein Distributionally Robust Stochastic Control: A Data-Driven Approach"
    ]
  },
  {
    "arxiv_id": "2605.29962",
    "title": "Gaussian Multiplicative Chaos for i.i.d. matrices",
    "abstract": "We consider $N\\times N$ matrices $X$ with i.i.d. entries, and prove that the random measure $\\mu_N(z):=\\frac{ | \\det (X-z)|^\\gamma}{\\mathbb{E}[ | \\det (X-z)|^\\gamma]} \\mathrm{d} z\\mathrm{d} \\overline{z}$ converges to the Gaussian Multiplicative Chaos (GMC) on the unit disc in the full subcritical regime $\\gamma \\in (0, 2 \\sqrt{2})$ as $N \\to \\infty$. Our result holds for both symmetry classes and in particular is new even for real Ginibre matrices. This result is the first of its kind for any non-invariant ensemble of random matrices. In the case of real matrices, we further prove that the restriction of $\\mu_N(z)$ to the unit interval converges to a one-dimensional GMC. We establish the asymptotics for the $K$-point function of $| \\det (X-z)|$ at any collection of mesoscopically separated points $z_i$. Our methods are analytic and probabilistic in nature, relying in part on the dynamical approach based on Dyson Brownian motion.",
    "categories": "math.PR math-ph math.MP",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "RANDOM MATRICES: THE CIRCULAR LAW",
      "Deterministic equivalents for certain functionals of large random matrices",
      "Isotropic local laws for sample covariance and generalized Wigner matrices"
    ]
  },
  {
    "arxiv_id": "2307.13826",
    "title": "Spectral Independence and Local-to-Global Techniques for Optimal Mixing of Markov Chains",
    "abstract": "This monograph is an exposition on an exciting new technique known as spectral independence, which has been instrumental in analyzing the convergence rate of Markov Chain Monte Carlo (MCMC) algorithms. For a high-dimensional distribution defined on labelings of the vertices of an $n$-vertex graph, the spectral independence condition, introduced by Anari, Liu, and Oveis Gharan (2020), is a bound on the maximum eigenvalue of the influence matrix capturing the influence between pairs of vertices (closely related to the covariance between the variables). In the first part of the monograph, we present results showing that spectral independence (and related techniques) imply fast mixing of simple Markov chains such as the Glauber dynamics (aka Gibbs sampler). These proofs rely on local-to-global theorems relating local walks encoding pairwise correlations to variance decay and mixing properties of Markov chains. We focus on two applications: the hard-core model on independent sets of a graph (which is a combinatorial example of a binary graphical model) and random bases of a matroid. We apply the techniques presented in this monograph to show recent results of fast mixing of the Glauber dynamics on general graphs in the so-called tree-uniqueness region, polynomial-time mixing on general graphs at the critical point for the uniqueness threshold, polynomial-time mixing on random regular graphs beyond the uniqueness threshold, and fast mixing of the bases-exchange walk for generating a random basis of an arbitrary matroid. Our focus in this monograph is on the analysis of the spectral gap of the associated Markov chains from a functional analysis perspective; we present proofs of the associated local-to-global theorems and the Trickle-Down Theorem from this same Markov chain perspective. The monograph is self-contained and aims to present the proofs in a unified fashion.",
    "categories": "cs.DM math.PR",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Spectra of random graphs with given expected degrees",
      "The Spectra of Random Graphs with Given Expected Degrees",
      "Spectral Statistics of Erd\u0151s-R\u00e9nyi Graphs II: Eigenvalue Spacing and the Extreme Eigenvalues"
    ]
  },
  {
    "arxiv_id": "2109.02644",
    "title": "Resolvent convergence for sample second-moment matrices with heterogeneous profiles under quadratic-form control",
    "abstract": "We study the resolvent \\(G^z=\\left(\\frac{1}{n}XX^{\\top}-zI_p\\right)^{-1}\\), where \\(z\\in\\mathbb{C}\\) satisfies \\(\\Im(z)>0\\) and \\(X=(x_1,\\ldots,x_n)\\in\\mathbb{R}^{p\\times n}\\) is a random matrix with independent, but not necessarily identically distributed, columns. The columns are real-valued and have finite second moments, but need not be centered. We identify a deterministic equivalent \\(\\tilde G^z\\) through a finite-dimensional fixed-point system depending on the full second-moment profile \\((\\mathbb{E}[x_ix_i^{\\top}])_{i\\in[n]}\\). Our quantitative, dimension-dependent bounds are expressed in terms of moments of the centered quadratic forms \\(q_i(A):=x_i^{\\top}Ax_i-\\mathbb{E}[x_i^{\\top}Ax_i]\\), normalized either by the Hilbert--Schmidt norm or by the operator norm of \\(A\\). In particular, no independence between the entries of a given column is required. We prove quantitative comparison bounds between \\(\\operatorname{tr}(BG^z)\\) and \\(\\operatorname{tr}(B\\tilde G^z)\\) in several regimes. We first consider heterogeneous profiles with uniformly bounded operator norm and bounded aspect ratio. Sharper, profile-adapted arguments then cover uniformly bounded Hilbert--Schmidt second moments without any aspect-ratio condition, a common profile for which additional operator-norm estimates are obtained, and profiles taking \\(k\\) pairwise commuting values, for which the Hilbert--Schmidt bounds incur a linear loss in \\(k\\). All probabilistic estimates are global for a fixed \\(z\\in\\mathbb{H}\\); the regime \\(\\Im(z)\\downarrow0\\) is not considered. The Hilbert--Schmidt estimate yields an explicit random-to-deterministic convergence rate and recovers the Marchenko--Pastur limit in the centered i.i.d. setting under the existence of a moment strictly larger than two.",
    "categories": "math.PR stat.ML",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Isotropic local laws for sample covariance and generalized Wigner matrices",
      "CLT for linear spectral statistics of large-dimensional sample covariance matrices",
      "Deterministic equivalents for certain functionals of large random matrices"
    ]
  },
  {
    "arxiv_id": "2408.04690",
    "title": "Modelling parametric uncertainty in PDEs models via Physics-Informed Neural Networks",
    "abstract": "We provide an approach enabling one to employ physics-informed neural networks (PINNs) for uncertainty quantification. Our approach is applicable to systems where observations are scarce (or even lacking), these being typical situations associated with subsurface water bodies. Our novel physics-informed neural network under uncertainty (PINN-UU) integrates the space-time domain across which processes take place and uncertain parameter spaces within a unique computational domain. PINN-UU is then trained to satisfy the relevant physical principles (e.g., mass conservation) in the defined input domain. We employ a stage training approach via transfer learning to accommodate high-dimensional solution spaces. We demonstrate the effectiveness of PINN-UU in a scenario associated with reactive transport in porous media, showcasing its reliability, efficiency, and applicability to sensitivity analysis. PINN-UU emerges as a promising tool for robust uncertainty quantification, with broad applicability to groundwater systems. As such, it can be considered as a valuable alternative to traditional methods such as multi-realization Monte Carlo simulations based on direct solvers or black-box surrogate models.",
    "categories": "physics.data-an cs.NA math.DS math.NA physics.comp-ph physics.geo-ph",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Physics-Informed Neural Network Solution of Thermo\u2013Hydro\u2013Mechanical Processes in Porous Media",
      "NeuralUQ: A Comprehensive Library for Uncertainty Quantification in Neural Differential Equations and Operators",
      "Solving parametric PDE problems with artificial neural networks"
    ]
  },
  {
    "arxiv_id": "2607.27464",
    "title": "Neutral Entry--Exit Cycles with Quadratic Grazing: Uniform Return Reduction and Local Two-Parameter Bifurcations",
    "abstract": "We study planar continuous piecewise-smooth slow--fast return circuits in which an invariant-line entry--exit passage is followed by a separated quadratic grazing and the reference cycle has unit multiplier. We first prove that the physical entry--exit map for positive slow parameter extends, uniformly to any prescribed finite order, to the singular parameter, including nonvertical endpoint fibers. In the exact moving penetration coordinate, composition with the grazing passage gives the extended Poincare displacement $\\Delta(q,p)=S(q,p)+q_+^{3/2}K(\\sqrt{q_+},q,p)$. Under a rank-two unfolding, we use the exact constant and linear coefficients of $\\Delta$ as parameters and construct, for every sufficiently small fixed positive slow parameter, a unique nonpenetrating fold, a unique penetrating fold, and the grazing-incidence stratum. We give the complete marked chamber decomposition by nonpenetrating, grazing, and penetrating cycles and determine their stability from the Poincare multiplier. The open chambers contain zero or two cycles when the smooth and grazing coefficients have the same sign, and one or three when their signs are opposite; the corresponding cyclicity bounds are sharp corollaries. A compact polynomial family realizes both sign classes. In a cutoff-Gause family, interval certificates isolate one singular balanced-neutral point in each of two parameter boxes and verify the required signs and rank; an analytic local pullback transfers the diagram to the response parameters. Thus one local classification records cycle number, itinerary, and stability across the grazing and fold boundaries.",
    "categories": "math.DS",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "The largest eigenvalues of finite rank deformation of large Wigner matrices: Convergence and nonuniversality of the fluctuations",
      "Spatial correlations of the 1D KPZ surface on a flat substrate",
      "Bethe Ansatz Solution of the Asymmetric Exclusion Process with Open Boundaries"
    ]
  },
  {
    "arxiv_id": "2606.14274",
    "title": "Secondary terms for first moments of Selmer groups of twists of elliptic curves over global function fields",
    "abstract": "Let $E$ be a non-isotrivial elliptic curve over a global function field $\\mathbb{F}_q(t)$ of characteristic coprime to $2$ and $3$. Under some explicit conditions, we determine the secondary terms for the first moments of prime Selmer groups of cyclic prime twist families of $E$ over $\\mathbb{F}_q(t)$.",
    "categories": "math.NT math.PR",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "The importance of the Selberg integral",
      "Universality of Soft and Collinear Factors in Hard-Scattering Factorization",
      "Determinantal random point fields"
    ]
  },
  {
    "arxiv_id": "2608.18761",
    "title": "Maximal attractors for perturbations of unimodal maps near a homoclinic tangency",
    "abstract": "We show that small planar perturbations of families of unimodal maps have maximal (equal to the intersection of the iterates of their trapping region) attractors at parameters near homoclinic tangency of one of the fixed points. The results hold for general unimodal maps exhibiting certain hyperbolic properties. Hence, admissible families considered include H\\'enon-like families, Lozi-like families, or perturbations of border collision normal forms. Therefore, our results generalize results of Viana in the case of H\\'enon-like families and Glendinning and Simpson in the case of border collision normal forms.",
    "categories": "math.DS",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "",
      "Values of Brownian intersection exponents, II: Plane exponents",
      "Bethe Ansatz Solution of the Asymmetric Exclusion Process with Open Boundaries"
    ]
  },
  {
    "arxiv_id": "2309.12441",
    "title": "Stabilization by rough noise for an epitaxial growth model",
    "abstract": "In this article we study a model from epitaxial thin-film growth. It was originally introduced as a phenomenological model of growth in the presence of a Schwoebbel barrier, where diffusing particles on a terrace are not allowed to jump down at the boundary. Nevertheless, we show that the presence of arbitrarily small space-time white noise due to fluctuations in the incoming particles surprisingly eliminates all nonlinear interactions in the model and thus has the potential to stabilize the dynamics and suppress the growth of hills in these models.",
    "categories": "math.PR math.AP math.DS",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Growing interfaces uncover universal fluctuations behind scale invariance",
      "Universal Distributions for Growth Processes in<mml:math xmlns:mml=\"http://www.w3.org/1998/Math/MathML\" display=\"inline\"><mml:mn>1</mml:mn><mml:mo>+</mml:mo><mml:mn>1</mml:mn></mml:math>Dimensions and",
      "Viscoelastic subdiffusion: From anomalous to normal"
    ]
  },
  {
    "arxiv_id": "2601.04074",
    "title": "Multi-Dimensional Opinion Formation",
    "abstract": "In this paper we propose and investigate a multi-dimensional opinion dynamics model where people are characterised by both opinions and importance weights across these opinions. Opinion changes occur through binary interactions, with a novel coupling mechanism: the change in one topic depends on the weighted similarity across the full opinion vector. We state the kinetic equation for this process and derive its mean-field partial differential equation to describe the overall dynamics. Analytical computations and numerical simulations confirm that this model exhibits a variety of qualitatively distinct stationary states, and we demonstrate that the final opinion structures are critically determined by the people's opinion weights.",
    "categories": "physics.soc-ph math.AP math.DS",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Variational Koopman models: Slow collective variables and molecular kinetics from short off-equilibrium simulations",
      "Stochastic Gradient Riemannian Langevin Dynamics on the Probability Simplex",
      "Sampling the Dirichlet Mixture Model with Slices"
    ]
  },
  {
    "arxiv_id": "2506.03479",
    "title": "A Real K3 Automorphism with Most of Its Entropy in the Real Part",
    "abstract": "This article describes an example of a real projective K3 surface admitting a real automorphism $f$ satisfying $h_{top}(f, X(\\mathbb{C})) < 2 h_{top}(f, X(\\mathbb{R}))$. The example presented is a $(2,2,2)$-surface in $\\mathbb{P}^1 \\times \\mathbb{P}^1 \\times \\mathbb{P}^1$ given by the vanishing set of $(1 + x^2)(1 + y^2)(1 + z^2) + 10xyz - 2$, first considered by McMullen. Along the way, we develop an ad hoc shadowing lemma for $C^2$ (real) surface diffeomorphisms, and apply it to estimate the location of a periodic point in $X(\\mathbb{R})$. This result uses the GNU MPFR arbitrary precision arithmetic library in C and the Flipper computer program.",
    "categories": "math.DS math.AG",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Determinantal random point fields",
      "Convergence of the Mass-Transport Steepest Descent Scheme for the Subcritical Patlak\u2013Keller\u2013Segel Model",
      ""
    ]
  },
  {
    "arxiv_id": "2608.18431",
    "title": "Process Optimization Under Uncertainty for Improving the Bond Quality of Polymer Filaments in Fused Filament Fabrication",
    "abstract": "This paper develops a computational framework to optimize the process parameters such that the bond quality between extruded polymer filaments is maximized in fused filament fabrication (FFF). A transient heat transfer analysis providing an estimate of the temperature profile of the filaments is coupled with a sintering neck growth model to assess the bond quality that occurs at the interfaces between adjacent filaments. Predicting the variability in the FFF process is essential for achieving proactive quality control of the manufactured part; however, the models used to predict the variability are affected by assumptions and approximations. This paper systematically quantifies the uncertainty in the bond quality model prediction due to various sources of uncertainty, both aleatory and epistemic, and includes the uncertainty and the model discrepancy in the process parameter optimization. Variance-based sensitivity analysis based on Sobol indices is used to quantify the relative contributions of the different uncertainty sources to the uncertainty in the bond quality. A Gaussian process (GP) surrogate model is constructed to compute and include the model discrepancy within the optimization. Physical experiments are conducted for calibration and validation of the physics model and also for validation of the optimum solution. The results show that the proposed formulation for process parameter optimization under uncertainty results in high bond quality between adjoining filaments of the FFF product.",
    "categories": "cs.CE cs.LG cs.NA math.NA math.PR",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Defects and uncertainties of adhesively bonded composite joints",
      "Rapid Bayesian optimisation for synthesis of short polymer fiber materials",
      "Relative Entropy Based Method for Probabilistic Sensitivity Analysis in Engineering Design"
    ]
  },
  {
    "arxiv_id": "2605.29508",
    "title": "Quantum Markovian Dynamics from a Double Covariance Stochastic Framework",
    "abstract": "We develop an interacting extension of the Double Covariance Model (DCM), a stochastic subquantum framework in which macroscopic quantum dynamics emerge through coarse-graining of correlated microscopic fluctuations. Starting from local stochastic differential equations on subsystem Hilbert spaces, we derive a closed evolution equation for a coarse-grained double covariance operator using multi-scale It\\^o calculus and sliding-window averaging. The construction explicitly incorporates two separated temporal scales: a fast microscopic fluctuation scale governing subquantum stochastic processes and a slower macroscopic observation scale associated with coarse-grained dynamics. Within the hydrodynamic limit, where the ratio between microscopic correlation time and averaging-window scale vanishes, rapidly fluctuating corrections disappear and the effective dynamics converges to a deterministic macroscopic transport equation. We show that the emergent macroscopic dynamics has the exact Gorini-Kossakowski-Sudarshan-Lindblad (GKSL) form: coherent Hamiltonian evolution arises from deterministic subquantum flow, while dissipative channels emerge from quadratic noise correlations. The framework further demonstrates how non-separable interaction Hamiltonians can arise from strictly local, state-dependent stochastic feedback fields. In the fluctuation-free limit, the model reduces naturally to the standard von Neumann equation, providing a unified stochastic foundation for both open and closed quantum dynamics.",
    "categories": "quant-ph math.DS math.PR",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Growing interfaces uncover universal fluctuations behind scale invariance",
      "Operator Spreading in Random Unitary Circuits",
      "Large Deviations and Ensembles of Trajectories in Stochastic Models"
    ]
  },
  {
    "arxiv_id": "2608.07605",
    "title": "Random Knots via Stiefel manifolds",
    "abstract": "A fixed simplex, randomly projected into three dimensions and joined in Hamiltonian order, produces a rich and unusually tractable model of random stick knots. We prove that Gaussian projections and Haar-random Stiefel projections have exactly the same knot-type law, despite having different metric shapes, and that at every stick budget the model gives positive probability to precisely the knot types realizable with that many sticks. Its linear-algebraic structure yields an exact marginal distance law, an exact mean planar-crossing count, and crossing concentration, while in the first nontrivial six-stick case the complete tetrahedral sign pattern gives an exact unknot-versus-handed-trefoil classifier for every generic sample. The result is a direct bridge from random projections and finite sign geometry to the topology of random knots.",
    "categories": "math.GT math.CO math.PR",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Determinantal probability measures",
      "Determinantal Processes and Independence",
      "Universality classes of non-Hermitian random matrices"
    ]
  },
  {
    "arxiv_id": "2608.15616",
    "title": "Compact Support Property of Super-Brownian Motion with Irregular Drift",
    "abstract": "We study the one-dimensional stochastic partial differential equation \\[ d_t X_t(x)=\\frac{1}{2}\\Delta X_t(x) +b_1\\unicode{x1D7D9}_{\\{X_t(x)>0\\}} +\\sqrt{X_t(x)}\\dot W(t,x), \\] where $b_1>0$, $\\dot W$ is space-time white noise, and the initial condition is a nonnegative, compactly supported continuous function. We prove that its unique weak solution has the compact support property. The drift term lies outside the usual regularity assumptions for the Dawson--Girsanov theorem. Instead, the proof is based on a layer decomposition in which the solution is constructed as the monotone limit of sums of super-Brownian motions with random immigration rates determined recursively by the positivity sets of the preceding layers. By comparison, the compact support property extends to a broader class of bounded nonnegative drifts vanishing at the origin. Finally, support-radius estimates yield a comparison of the total mass of $X$ with a squared Bessel process, which allows us to show that $X$ has a positive extinction probability.",
    "categories": "math.PR math.AP",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Large deviations for infinite dimensional stochastic dynamical systems",
      "Strong and Weak Error Estimates for Elliptic Partial Differential Equations with Random Coefficients",
      "High-dimensional Bayesian inference via the unadjusted Langevin algorithm"
    ]
  },
  {
    "arxiv_id": "2608.08529",
    "title": "Maximum Spanning Trees of Random Geometric Graphs With Independent Edge Weights",
    "abstract": "In this paper, we study maximum weight spanning trees of the random geometric graph (RGG)~\\(G\\) formed by~\\(n\\) vertices where each edge is independently either open or closed with a certain probability and is also equipped with an independent random positive weight. We use segmentation and iterative path construction to obtain deviation bounds for the order of growth of the maximum weight of a spanning tree in terms of an inverse of the edge weight complementary cumulative distribution function (ccdf) and also illustrate our results for the special cases of power law and exponential decay. We then use martingale difference methods to individually estimate the variance contribution due to randomness in vertex locations and edge states/weights and determine sufficient conditions for~\\(L^2-\\)convergence of the maximum weight, appropriately scaled and centred.",
    "categories": "math.PR",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Uniform spanning forests",
      "Asymptotic Enumeration of Spanning Trees",
      "Weak laws of large numbers in geometric probability"
    ]
  },
  {
    "arxiv_id": "2608.09494",
    "title": "Walk-on-Spheres Monte Carlo and deep neural network approximations of elliptic PDEs with drift and killing",
    "abstract": "In this paper we provide Monte Carlo and deep neural network approximations for stochastic representations of solutions to linear elliptic partial differential equations with constant diffusion, drift and killing. Building on the modified Walk-on-Spheres algorithm of Beznea et al. (arXiv:2209.01432), we introduce Monte Carlo estimators that explicitly incorporate sampled random times arising in the analyzed stochastic representations. We establish uniform error bounds for these estimators and show that, under suitable assumptions, a prescribed approximation accuracy is achieved with sample complexities growing at most polynomially in both the inverse accuracy and the problem dimension. Furthermore, we prove a deep neural network approximation result for the stochastic representations. Assuming suitable neural network representations of the boundary data and the distance function to the boundary, we use the constructed Monte Carlo to design deep neural networks that approximate the representation uniformly with a number of parameters growing at most polynomially in the inverse accuracy and the problem dimension. These results extend previous complexity analyses to a broader class of elliptic equations involving drift and killing.",
    "categories": "math.NA cs.LG cs.NA math.AP math.PR",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "An overview on deep learning-based approximation methods for partial differential equations",
      "Algorithms for solving high dimensional PDEs: from nonlinear Monte Carlo to machine learning",
      "Finite Element Error Analysis of Elliptic PDEs with Random Coefficients and Its Application to Multilevel Monte Carlo Methods"
    ]
  },
  {
    "arxiv_id": "2410.16457",
    "title": "The circular law for random band matrices with arbitrary doubly stochastic variance profiles",
    "abstract": "We consider the convergence of the ESD for non-Hermitian random band matrices with independent entries to the circular law, which is the uniform measure on the unit disk in the center of the complex plane. We assume that the bandwidth of the matrix scales like $n^\\gamma$ for some $\\gamma\\in(0,1]$, where $n$ is the matrix size, and the variance profile of the matrix is only assumed to be doubly stochastic with no additional assumption on its specific mixing properties. We prove that the circular law limit holds either (1) when $\\gamma>\\frac{5}{6}$ and the entries are independent Gaussians, (2) or when $\\gamma>\\frac{8}{9}$ and the entries are independent subgaussian random variables. This new threshold improves the previous threshold $\\gamma>\\frac{32}{33}$ which was only proven for block band matrices and periodic band matrices. After the initial version of this paper, the author further extended the range of circular law for much smaller values of $\\gamma$ in 2508.18143 and 2511.01744 when the variance profile has specific mixing properties, but not for an arbitrary doubly stochastic variance profile. Thus the main contribution of this paper is the circular law for a genuine power law bandwidth for any doubly stochastic variance profile. We also prove an extended form of product circular law with a growing number of matrices. Weak delocalization estimates on eigenvectors are also derived. The new technical input is new polynomial lower bounds on some intermediate small singular values, and this estimate does not depend on the specific structure of the variance profile beyond the fact that it is doubly stochastic.",
    "categories": "math.PR",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "The local semicircle law for a general class of random matrices",
      "RANDOM MATRICES: THE CIRCULAR LAW",
      "Around the circular law"
    ]
  },
  {
    "arxiv_id": "2502.08004",
    "title": "Optimizing Likelihoods via Mutual Information: Bridging Simulation-Based Inference and Bayesian Optimal Experimental Design",
    "abstract": "Simulation-based inference (SBI) is a method to perform inference on a variety of complex scientific models with challenging inference (inverse) problems. Bayesian Optimal Experimental Design (BOED) aims to efficiently use experimental resources to make better inferences. Various stochastic gradient-based BOED methods have been proposed as an alternative to Bayesian optimization and other experimental design heuristics to maximize information gain from an experiment. We demonstrate a link via mutual information bounds between SBI and stochastic gradient-based variational inference methods that permits BOED to be used in SBI applications as SBI-BOED. This link allows simultaneous optimization of experimental designs and optimization of amortized inference functions. We evaluate the pitfalls of naive design optimization using this method in a standard SBI task and demonstrate the utility of a well-chosen design distribution in BOED. We compare this approach on SBI-based models in real-world simulators in epidemiology and biology, showing notable improvements in inference.",
    "categories": "stat.ML cs.LG",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Simulation-based model selection for dynamical systems in systems and population biology",
      "Uncertainty quantification and propagation in surrogate-based Bayesian inference",
      "BayesFlow: Learning Complex Stochastic Models With Invertible Neural Networks"
    ]
  },
  {
    "arxiv_id": "2608.15137",
    "title": "One-Sided Product-Scale Upper Bounds for Nested Complex Wishart Extremes",
    "abstract": "I study the largest eigenvalue \\(\\Lambda_j\\) of \\(X^{(j)}(X^{(j)})^*\\), where \\(X^{(j)}\\) is the \\(M_j\\times j\\) northwest rectangle of one infinite complex Gaussian array. For two upper-tail events and, separately, for two lower-tail events at the largest-eigenvalue soft edge, I prove finite-\\(N\\) one-sided product-scale upper bounds for their joint probabilities. The logarithmic walls have polynomially small marginals, so an additive \\(o(1)\\) covariance estimate may be much larger than the vanishing product that must be controlled. Uniformly for levels in a short macroscopic window, bounded deterministic shifts, and separations at least \\(N^{2/3+\\epsilon}\\), each joint probability is at most \\((1+o(1))\\) times the product of its marginals. The classical \\(N^{2/3}\\) correlation window corresponds to order-one extended-Airy time; the theorem works at supercritical separation. Exact Laguerre operators along admissible row--column paths provide the finite-dimensional input. The upper-tail proof uses occupancy counts and cross-block trace estimates, whereas the lower-tail proof uses gap determinants, diagonal resolvents, and a Schur complement. I transfer the result between the half-integer Laguerre and physical rectangular normalizations and deduce intrinsic first- and second-moment estimates for separated sparse grids under the rarity, count-growth, spacing, and macroscopic-window budget.",
    "categories": "math.PR math.SP",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "USER-FRIENDLY TAIL BOUNDS FOR SUMS OF RANDOM MATRICES",
      "The local semicircle law for a general class of random matrices",
      "Isotropic local laws for sample covariance and generalized Wigner matrices"
    ]
  },
  {
    "arxiv_id": "2608.20472",
    "title": "Free Burnside groups of large odd exponent have cost 1",
    "abstract": "We prove that the free Burnside group $B(m,n)$ with $m\\geq 2$ generators and sufficiently large odd exponent $n$ (e.g., $n\\geq 1003$ if $m=2$, and $n\\geq 665$ if $m\\geq 3$), has cost $1$. It follows that $B(m,n)$ is anti-treeable, and that its first $\\ell^2$-Betti number $\\beta_1^{(2)}(B(m,n))$ vanishes. The latter recovers and extends a result of Feldkamp and Kionke [Proc. Amer. Math. Soc., 2023], who proved that $\\beta_1^{(2)}(B(m,p))=0$ for all sufficiently large prime exponents $p$.",
    "categories": "math.GR math.DS math.PR",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Algebraic aspects of increasing subsequences",
      "The complexity of counting graph homomorphisms",
      ""
    ]
  },
  {
    "arxiv_id": "2408.05840",
    "title": "Iterative Improvement of an Additively Regularized Topic Model",
    "abstract": "Topic modelling is fundamentally a soft clustering problem (of known objects -- documents, over unknown clusters -- topics). That is, the task is incorrectly posed. In particular, the topic models are unstable and incomplete. All this leads to the fact that the process of finding a good topic model (repeated hyperparameter selection, model training, and topic quality assessment) can be particularly long and labor-intensive. We aim to simplify the process, to make it more deterministic and provable. To this end, we present a method for iterative training of a topic model. The essence of the method is that a series of related topic models are trained so that each subsequent model is at least as good as the previous one, i.e., that it retains all the good topics found earlier. The connection between the models is achieved by additive regularization. The result of this iterative training is the last topic model in the series, which we call the iteratively updated additively regularized topic model (ITAR). Experiments conducted on several collections of natural language texts show that the proposed ITAR model performs better than other popular topic models (LDA, ARTM, BERTopic), its topics are diverse, and its perplexity (ability to \"explain\" the underlying data) is moderate.",
    "categories": "cs.CL cs.IR math.PR",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Sampling the Dirichlet Mixture Model with Slices",
      "Bayesian learning via stochastic gradient langevin dynamics",
      "Dirichlet\u2013Laplace Priors for Optimal Shrinkage"
    ]
  },
  {
    "arxiv_id": "2505.00198",
    "title": "Queueing models with random resetting",
    "abstract": "We introduce and study some queueing models with random resetting, including Markovian and non--Markovian models under the first-come first-served (FCFS) discipline. The Markovian models include M/M/$r$ and M/M/1+M queues with random resetting, in which a continuous-time Markov chain is formulated, with transitions including a resetting to state zero in addition to arrivals and services. We explicitly characterize the stationary distributions of the queueing processes in these models by using parting balance equations. We derive expressions for standard performance measures such as the delay probability, expected queue length and waiting time, as well as probability of a customer completing service before resetting in the M/M/$r$ model, and probability of abandonment before service or resetting in the M/M/1+M model. The non--Markovian models include GI/GI/1, GI/GI/$r$ and GI/GI/$\\infty$ queues with random resetting to state zero at arrival times. For GI/GI/1 and GI/GI/$r$ queues under the FCFS discipline, we introduce modified Lindley and Kiefer--Wolfowitz recursions, respectively. Using an operator representation for these recursions, we characterize the stationary distributions via convergent series, as solutions to the modified Wiener--Hopf equations. For GI/GI/$\\infty$ queues with resettings, we utilize a version of the Kiefer--Wolfowitz recursion, and also characterize the corresponding stationary distribution.",
    "categories": "math.PR",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Martingale proofs of many-server heavy-traffic limits for Markovian queues",
      "Statistical Analysis of a Telephone Call Center",
      "Markov Chains: Gibbs Fields, Monte Carlo Simulation, and Queues"
    ]
  },
  {
    "arxiv_id": "2608.09856",
    "title": "Mass erasure on measured $\\mathbb{R}$-trees, applications to L\\'evy forests",
    "abstract": "Let $h>0$. For a complete and separable $\\mathbb{R}$-tree $(T,d)$ equipped with a root $\\rho$ and a finite Borel measure $\\mu$, we define the $h$-mass-erased tree by removing from $T$ all fringe subtrees of mass less than $h$ and we equip it with a suitable measure such that the erasure operators $(\\mathcal{E}_h)_{h\\ge 0}$ form a semigroup that is continuous for the Gromov-weak topology. Then, we say that a sequence $\\boldsymbol{\\mu}_n=(T_n,d_n,\\rho_n,\\mu_n)$, $n\\in\\mathbb{N}$, converges in the sense of mass erasure if $(\\mathcal{E}_h\\boldsymbol{\\mu}_n)_{n\\in\\mathbb{N}}$ converges Gromov-weakly for all $h\\ge 0$. This notion of convergence is strictly weaker than Gromov-weak convergence and we establish criteria to relate the two notions. We define a distance function that metrizes convergence in the sense of mass erasure. By extending the notion of measured $\\mathbb{R}$-trees to allow mass on the boundary (the far ends of infinite geodesics), we obtain a complete metric space. Next, we identify random trees of finite type (that is, discrete trees with edge lengths) satisfying the regenerative branching property as a specific class of measured (sub)critical GW forests. We then show that this class of trees is preserved by mass erasure and we compute the law of these mass-erased GW forests explicitly. Finally, we establish a limit theorem for these measured (sub)critical GW forests to converge to standard measured L\\'evy forests, i.e. those whose total mass has the same distribution as the total population of a continuous-state branching process. This includes cases with bounded variation by crucially using the convergence in the sense of mass erasure and it extends the cases studied previously.",
    "categories": "math.PR",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Uniform spanning forests",
      "Renewal theory and computable convergence rates for geometrically ergodic Markov chains",
      "Broadcasting on trees and the Ising model"
    ]
  }
]
```

## Output

One JSON object per abstract, one per line, no prose. Every input `arxiv_id`
appears exactly once. Include `ambiguous` even when false.
