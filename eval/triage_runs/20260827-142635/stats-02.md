# triage batch 2/2 — domain: stats

Charter: `charters/stats.md` — read it first, it is authoritative.

## In scope — 25 exemplars from the canon

- **Regularization Paths for Generalized Linear Models via Coordinate Descent** (2010) — IN SCOPE: add a one-line reason
- **Hierarchical Linear Models: Applications and Data Analysis Methods** (2003) — IN SCOPE: add a one-line reason
- **SOME PRACTICAL GUIDANCE FOR THE IMPLEMENTATION OF PROPENSITY SCORE MATCHING** (2008) — IN SCOPE: add a one-line reason
- **Handbook of Parametric and Nonparametric Statistical Procedures** (2004) — IN SCOPE: add a one-line reason
- **A Practitioner’s Guide to Cluster-Robust Inference** (2015) — IN SCOPE: add a one-line reason
- **Combining Pattern Classifiers: Methods and Algorithms** (2005) — IN SCOPE: add a one-line reason
- **How much should we trust staggered difference-in-differences estimates?** (2022) — IN SCOPE: add a one-line reason
- **Revisiting Event-Study Designs: Robust and Efficient Estimation** (2024) — IN SCOPE: add a one-line reason
- **Why Propensity Scores Should Not Be Used for Matching** (2019) — IN SCOPE: add a one-line reason
- **Local Projections and VARs Estimate the Same Impulse Responses** (2021) — IN SCOPE: add a one-line reason
- **Recent Developments in the Econometrics of Program Evaluation** (2009) — IN SCOPE: add a one-line reason
- **Stochastic variational inference** (2013) — IN SCOPE: add a one-line reason
- **Statistical Comparisons of Classifiers over Multiple Data Sets** (2006) — IN SCOPE: add a one-line reason
- **Bayes and Empirical Bayes Methods for Data Analysis** (2001) — IN SCOPE: add a one-line reason
- **The coefficient of determination R-squared is more informative than SMAPE, MAE, MAPE, MSE and RMSE in regression analysis evaluation** (2021) — IN SCOPE: add a one-line reason
- **Two-Way Fixed Effects Estimators with Heterogeneous Treatment Effects** (2020) — IN SCOPE: add a one-line reason
- **Permutation inference for the general linear model** (2014) — IN SCOPE: add a one-line reason
- **A More Credible Approach to Parallel Trends** (2023) — IN SCOPE: add a one-line reason
- **Weak Instruments in Instrumental Variables Regression: Theory and Practice** (2019) — IN SCOPE: add a one-line reason
- **Simultaneous analysis of Lasso and Dantzig selector** (2009) — IN SCOPE: add a one-line reason
- **Deciding on the Number of Classes in Latent Class Analysis and Growth Mixture Modeling: A Monte Carlo Simulation Study** (2007) — IN SCOPE: add a one-line reason
- **The Adaptive Lasso and Its Oracle Properties** (2006) — IN SCOPE: add a one-line reason
- **Robust Nonparametric Confidence Intervals for Regression-Discontinuity Designs** (2014) — IN SCOPE: add a one-line reason
- **Logs with Zeros? Some Problems and Solutions** (2023) — IN SCOPE: add a one-line reason
- **High-Dimensional Probability: An Introduction with Applications in Data Science** (2018) — IN SCOPE: add a one-line reason

## Out of scope — near misses

_Highly cited and topically adjacent. These are the traps._

- **Quantifying heterogeneity in a meta‐analysis** (2002) — OUT: I don't do metaanalysis
- **The Cochrane Collaboration's tool for assessing risk of bias in randomised trials** (2011) — OUT: Seems like a specific thing, not statistics methodology
- **A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research** (2016) — OUT: Do not include any chiropractice papers
- **CONSORT 2010 Statement: updated guidelines for reporting parallel group randomised trials** (2010) — OUT: Control trial reporting
- **Discussion on the paper by Spiegelhalter, Best, Carlin and van der Linde** (2002) — OUT: Discussion paper
- **Better reporting of interventions: template for intervention description and replication (TIDieR) checklist and guide** (2014) — OUT: Reporting paper


## Abstracts

Each carries a `band` computed before you saw it, the `threshold` that band
implies, and the titles of its nearest canon neighbours. Score on merit first,
then apply the threshold.

```json
[
  {
    "arxiv_id": "2608.12603",
    "title": "Hierarchical Bayesian Calibration with Bayesian Committee Machine",
    "abstract": "Calibrating computational models to experimental data is a core task in applied statistics, especially in scientific domains, where physical experiments are costly and simulations play a central role in design and inference. Motivated by uncertainty quantification challenges in particle accelerator experiments, we develop and evaluate a Hierarchical Bayesian Calibration framework. In contrast to standard Bayesian calibration, certain inputs - such as beam injection amplitude - must be estimated separately for each experiment. We adopt the Kennedy-O'Hagan formulation and extend it with a hierarchical prior structure to model the distribution of experiment-specific calibration parameters, thus borrowing strength and improving generalisation across repeated experiments. A key methodological challenge arises from the need to evaluate a large number of forward simulations, which renders conventional Markov chain Monte Carlo approaches computationally prohibitive. To address this, we leverage the Bayesian Committee Machine as a scalable modelling strategy for Gaussian Process emulators. The BCM provides a principled divide-and-conquer approach, enabling parallel inference and reducing computational cost without requiring problem-specific tuning of the emulator approximation. Posterior sampling is performed using the No-U-Turn Sampler, supported by automatic differentiation in Julia, which removes the need for analytic gradient derivation and facilitates flexible model specification",
    "categories": "stat.CO physics.data-an",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "dynesty: a dynamic nested sampling package for estimating Bayesian posteriors and evidences",
      "Bayesian Computing with INLA: A Review",
      "Variational Inference: A Review for Statisticians"
    ]
  },
  {
    "arxiv_id": "2608.16365",
    "title": "Mixed-effects Outcome-Adaptive Lasso for Propensity Score Estimation under Partial Interference",
    "abstract": "Interference occurs when one individual's treatment or exposure affects another individual's outcome. In particular, we assume partial interference, where individuals are divided into groups such that there is no interference between individuals in different groups. In observational studies, inverse probability weighting (IPW) based on propensity scores is often used for causal effect estimation. However, under partial interference, the group-level propensity score must be estimated, and it is more likely to take extreme values than the usual individual-level propensity score. As a result, IPW estimators may have large variances. This problem can become more serious when many covariates are available. In this study, we propose an Outcome-Adaptive Lasso based on a mixed-effects logistic regression model to stably estimate causal effects under partial interference. The proposed method performs covariate selection and estimation in the propensity score model simultaneously while accounting for unobserved group-level heterogeneity in treatment assignment. Under regularity conditions, we show that the proposed method has the oracle property and that the IPW estimators based on the proposed method are consistent and asymptotically normal. Through Monte Carlo simulations, we demonstrate that the proposed method tends to select confounders and prognostic factors at high frequencies, while excluding instrumental variables and spurious variables. The results further suggest that the pr",
    "categories": "stat.ME",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Towards optimal doubly robust estimation of heterogeneous causal effects",
      "Addressing Extreme Propensity Scores via the Overlap Weights",
      "Covariate Balancing Propensity Score"
    ]
  },
  {
    "arxiv_id": "2608.11121",
    "title": "Generative AI use in Statistical Research: A Literature Review and Code Generation Case Study",
    "abstract": "Generative artificial intelligence (GenAI) is a large language model (LLM) that has the ability to generate media based on user-provided prompts. Given the demonstrated capabilities of models such as ChatGPT in information synthesis and programming, there is growing interest in their potential role within the research process. However, little work has evaluated recent GenAI models for research tasks in the domain of statistical research. This case study examines GenAI as a tool for developing a literature review and translating methodology from academic papers into code, for the topic of dynamic treatment regime (DTR) estimation via the dynamic weighted ordinary least squares (dWOLS) approach. Specifically, we utilize ChatGPT-5 and ScholarAI (Sept-Nov 2025 release) in the processes of identifying relevant sources for the literature review, creating summaries of papers, identifying gaps in research, and R code generation to implement methodology. Our findings show that current GenAI models lack the depth and contextual understanding required to accomplish these tasks without careful prompting and supervision of a knowledgeable researcher. Nonetheless, GenAI has potential to increase efficiency of tasks which take advantage of its search and summarization abilities, as well as basic code debugging and algorithm formation. We demonstrate that under a knowledgeable guide, GenAI can function as a research tool, but not as a substitute for methodological expertise.",
    "categories": "stat.OT stat.ME",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "How generative AI models such as ChatGPT can be (mis)used in SPC practice, education, and research? An exploratory study",
      "Artificial intelligence for literature reviews: opportunities and challenges",
      "Accelerating clinical evidence synthesis with large language models"
    ]
  },
  {
    "arxiv_id": "2608.13154",
    "title": "Extreme principal minors of Wishart and deformed GOE matrices",
    "abstract": "We study the laws of large numbers for the largest eigenvalues among all principal minors of Wishart matrices and deformed GOE matrices. We propose a new method based on identifying the deterministic sets to which the random sets formed by suitably normalized principal minors converge in Hausdorff distance, thereby reducing the original extreme-value problems to finite-dimensional convex optimization problems. We demonstrate the effectiveness of this method in regimes not covered by the existing second-moment arguments in \\cite{cai2021asymptotic,hu2023extreme}. For deformed GOE matrices with fixed minor size \\(k\\), we determine the limit for every diagonal variance \\(a>0\\) and identify a phase transition at \\(a=2\\). Above the transition, the limiting constant satisfies an explicit recursion with no close-form expression, and the optimizers exhibit a nested hierarchical structure, thereby resolving the case left open in \\cite{cai2021asymptotic}. For Wishart matrices with general sub-Gaussian entries and fixed \\(k\\), we characterize the limit through an entropy-constrained deterministic convex set. When the entries are standard Gaussian, we solve the resulting optimization problem explicitly and obtain the exact value of the limiting constant.",
    "categories": "math.PR math.ST stat.TH",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "High-Dimensional Probability: An Introduction with Applications in Data Science",
      "A unified framework for high-dimensional analysis of M-estimators with decomposable regularizers",
      "Adaptive estimation of a quadratic functional by model selection"
    ]
  },
  {
    "arxiv_id": "2511.19735",
    "title": "Integrating RCTs, RWD, AI/ML and Statistics: Next-Generation Evidence Synthesis",
    "abstract": "Randomized controlled trials (RCTs)have been the cornerstone of clinical evidence; however, their cost, duration, and restrictive eligibility criteria limit power and external validity. Studies using real-world data (RWD), historically considered less reliable for establishing causality, are now recognized as an important source of real-world evidence (RWE). In parallel, artificial intelligence and machine learning (AI/ML) are increasingly used throughout the drug development process, providing scalability and flexibility but also presenting challenges in interpretability and statistical rigor. This Perspective argues that the future of evidence generation will not depend on RCTs versus RWD, or statistics versus AI/ML, but on their principled integration under a statistical evidence framework that clarifies estimands, evaluates data fitness, controls bias, quantifies uncertainty, and determines when evidence is strong enough to support decisions. Building on the Causal Roadmap for high-quality real-world evidence, we present a six-step statistical roadmap for integrative evidence synthesis and organize the discussion around five core questions that statisticians must confront: when RWD is fit for causal use and when it is not; what AI genuinely contributes across the evidence lifecycle; what remains distinctly statistical and indispensable; how to build trustworthy end-to-end evidence systems in pharmaceutical, regulatory, and industry settings; and how statistical training s",
    "categories": "stat.ME cs.LG",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Integrating Model\u2010Informed Drug Development With AI : A Synergistic Approach to Accelerating Pharmaceutical Innovation",
      "The role of machine learning in clinical research: transforming the future of evidence generation",
      "A comprehensive review of methodologies and application to use the real-world data and analytics platform TriNetX"
    ]
  },
  {
    "arxiv_id": "2606.23363",
    "title": "Optimal Poisson subsampling for quantile regression with large-scale longitudinal data",
    "abstract": "To address the computational challenges arising from large-scale longitudinal data, an optimal Poisson subsampling algorithm is proposed for quantile regression. The proposed method can substantially alleviate computational burden. Under some regularity conditions, we derive the asymptotic properties of the estimators from weighted quantile generalized estimating equations. For practical implementation, an efficient algorithm is proposed for parameter estimation. Furthermore, asymptotic theory is established for penalized weighted smooth quantile generalized estimating equations, and regularized parameter estimation is performed within the optimal Poisson subsampling framework. Both numerical simulations and a real data application demonstrate that the proposed optimal Poisson subsampling algorithm outperforms the uniform Poisson subsampling algorithm, and the regularized estimation exhibits satisfactory performance as well.",
    "categories": "stat.CO",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Quantile Regression",
      "Unconditional Quantile Regressions",
      "VARIABLE SELECTION IN QUANTILE REGRESSION"
    ]
  },
  {
    "arxiv_id": "2606.18512",
    "title": "Causal Forecasting in Panel Data: A Two-Way Synthetic Forecasting Approach",
    "abstract": "Estimating causal effects in panel data is central to policy evaluation, yet existing methods largely address retrospective questions: what would have happened to a target unit under a different intervention during the observed panel? In many applications, however, decision-makers instead face a prospective question: what will happen to a target unit under an intervention it has not yet experienced, beyond the observed horizon? We develop a framework for such causal forecasting problems by combining the counterfactual logic of synthetic controls methods with the extrapolative structure of multivariate time-series forecasting. Building on latent factor models for synthetic controls, we impose a low-rank temporal structure on the treated latent time factors to identify prospective causal forecast estimands. We operationalize this idea through the Two-Way Synthetic Forecasting estimator (TWSF), which learns cross-unit relationships from pre-treatment outcomes and temporal dynamics from the post-treatment trajectories of donors exposed to the intervention of interest. Under suitable conditions, we establish finite-sample error bounds and pointwise consistency, and derive asymptotic normality and feasible pointwise inference for prespecified linear summaries over fixed multi-step horizons. Simulation studies support the theoretical results, and an application to the opening of NFL stadiums during the 2020 season illustrates how TWSF can inform prospective policy evaluation using o",
    "categories": "econ.EM stat.ME",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "A Practical Guide to Counterfactual Estimators for Causal Inference with Time\u2010Series Cross\u2010Sectional Data",
      "On the Use of Two-Way Fixed Effects Regression Models for Causal Inference with Panel Data",
      "Explaining Fixed Effects: Random Effects Modeling of Time-Series Cross-Sectional and Panel Data"
    ]
  },
  {
    "arxiv_id": "2509.10383",
    "title": "Network Meta-Analysis of survival outcomes with non-proportional hazards using flexible M-splines",
    "abstract": "Network meta-analysis (NMA) is widely used in healthcare decision-making, where estimates of the effect of multiple treatments on outcomes are required. For time-to-event outcomes such as survival or disease progression the most common approach is to model log hazard ratios; however, this relies on the proportional hazards assumption. Novel treatments such as immunotherapies are expected to display complex hazard functions that cannot be captured by standard parametric models, which results in non-proportional hazards when comparing treatments from different classes. As a result, alternative models such as fractional polynomials or restricted cubic splines are often used. These allow substantial flexibility on the shape of the baseline hazard, but require time-consuming model selection or are intractable for Bayesian analysis. We propose a flexible NMA model using M-splines on the baseline hazard, with a novel weighted random walk prior distribution that provides shrinkage to avoid overfitting and is invariant to the choice of knots and timescale. Non-proportional hazards are modelled either by stratifying by treatment or by introducing treatment effects on the spline coefficients, and covariates may be included on the log hazard rate and spline coefficients. Treatment and covariate effects on the spline coefficients are given random walk prior distributions to smoothly model departures from proportionality over time. The methods are implemented in the user-friendly R package",
    "categories": "stat.ME",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Flexible parametric proportional\u2010hazards and proportional\u2010odds models for censored survival data, with application to prognostic modelling and estimation of treatment effects",
      "Further Development of Flexible Parametric Models for Survival Analysis",
      "Regression models for relative survival"
    ]
  },
  {
    "arxiv_id": "2608.13311",
    "title": "Distributed Selective Inference for Quantile Regression",
    "abstract": "We propose a distributed selective inference framework tailored for high-dimensional quantile regression. To enable valid post-selection inference in this context, we address the computational challenge posed by the non-smooth quantile loss via a response-surrogation strategy. This strategy transforms the problem into a penalized least-squares formulation, thereby facilitating the application of distributed selective inference. For valid post-selection inference, a randomized procedure is introduced, in which the Lasso selection event is characterized through the associated Karush-Kuhn-Tucker conditions and the conditional distribution of the aggregated estimator is derived given the selection event. The resulting algorithm requires only three rounds of communication between local machines and the central server. Under standard regularity conditions, we establish the asymptotic validity of the proposed procedure and develop a large-deviation approximation to the selective likelihood for computationally tractable implementation. Simulation studies and a real-data application demonstrate the satisfactory finite-sample performance of the proposed method.",
    "categories": "stat.ME stat.AP",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "VARIABLE SELECTION IN QUANTILE REGRESSION",
      "Variable Selection via Nonconcave Penalized Likelihood and its Oracle Properties",
      "Unconditional Quantile Regressions"
    ]
  },
  {
    "arxiv_id": "2608.16017",
    "title": "A Two Stage Quasi-Likelihood Estimation Method for High Dimensional Generalized Structural Equation Models",
    "abstract": "Estimating high dimensional Generalized Structural Equation Models presents severe computational challenges. Traditional simultaneous estimators frequently suffer from numerical instability and prohibitive computational costs. Moreover, there are no tractable algorithms for families such as Poisson, negative binomial, and gamma. To overcome these limitations, this article introduces a Two Stage Quasi-Likelihood Expectation-Maximization framework. The proposed method isolates the structural model from the measurement model. First, it approximates the conditional distribution of the latent variables given the observed indicators. Second, it employs marginal quasi-likelihood estimating equations to evaluate the structural parameters, deriving the necessary conditional moments either exactly or through Monte Carlo integration. This approach completely avoids the need to evaluate the full joint likelihood. Extensive simulations demonstrate that our method drastically reduces computational runtime, providing a numerically stable framework that minimizes the mean squared error and structural bias to yield a scalable and flexible solution for analyzing complex latent variable models.",
    "categories": "stat.ME stat.AP stat.CO",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Structural Equation Models of Latent Interactions: Evaluation of Alternative Estimation Strategies and Indicator Construction.",
      "The impact of nonnormality on full information maximum-likelihood estimation for structural equation models with missing data.",
      "On the Merits of Orthogonalizing Powered and Product Terms: Implications for Modeling Interactions Among Latent Variables"
    ]
  },
  {
    "arxiv_id": "2605.03674",
    "title": "Statistical Inference via T-Posterior Randomised Estimators",
    "abstract": "Given a statistical model, we propose a novel estimation method that yields randomised estimators for the unknown distribution of an observed random variable. We establish non-asymptotic bounds for the performance of these estimators and demonstrate their robustness to potential model misspecification. Notably, these properties are established by circumventing the use of concentration inequalities and empirical process theory. We provide an illustration of this approach to the problem of estimating the intensity of a Poisson process.",
    "categories": "math.ST stat.TH",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Convergence rates of posterior distributions",
      "Efficient Estimation of Models with Conditional Moment Restrictions Containing Unknown Functions",
      "Variational Inference: A Review for Statisticians"
    ]
  },
  {
    "arxiv_id": "2206.06901",
    "title": "Improving sampling efficacy on high dimensional distributions with thin high density regions using Conservative Hamiltonian Monte Carlo",
    "abstract": "Hamiltonian Monte Carlo is a prominent Markov Chain Monte Carlo algorithm, which employs symplectic integrators to sample from high dimensional target distributions in many applications, such as statistical mechanics, Bayesian statistics and generative models. However, such distributions tend to have thin high density regions, posing a significant challenge for symplectic integrators to maintain the small energy errors needed for a high acceptance probability. Instead, we propose a variant called Conservative Hamiltonian Monte Carlo, using $R$--reversible energy-preserving integrators to retain a high acceptance probability. We show our algorithm can achieve approximate stationarity with an error determined by the Jacobian approximation of the energy-preserving proposal map. Numerical evidence shows improved convergence and robustness over integration parameters on target distributions with thin high density regions and in high dimensions. Moreover, a version of our algorithm can also be applied to target distributions without gradient information.",
    "categories": "math.NA cs.NA stat.CO stat.ME",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Variational Inference: A Review for Statisticians",
      "Bayesian Computing with INLA: A Review",
      "Approximate Bayesian Inference for Latent Gaussian models by using Integrated Nested Laplace Approximations"
    ]
  },
  {
    "arxiv_id": "2608.19454",
    "title": "Dummy RAPM: Representing Low-Minute Players in Regularized Adjusted Plus-Minus",
    "abstract": "Regularized Adjusted Plus-Minus (RAPM) uses stint-level lineup indicators to estimate player contributions to scoring margin. When low-minute player columns are removed, their stints remain in the data, but the design matrix no longer represents the complete lineup. Dummy RAPM restores this information using five indicators for the number of excluded players on each lineup side. Across 16 NBA seasons, chronological validation selects a 10-minute-per-appearance threshold and a dummy-to-player penalty ratio of 2.2. On held-out March-April games, Dummy RAPM reduces mean season game-margin RMSE from 12.897 to 12.856 and achieves lower RMSE in 13 of 16 seasons. The average reduction is 0.042 points, or 0.30%. Although the improvement in game-level predictive accuracy is small, it is consistent: RAPM performs better when it records how many excluded players are on each side.",
    "categories": "stat.AP",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Cognitive Assessment Models with Few Assumptions, and Connections with Nonparametric Item Response Theory",
      "The coefficient of determination R-squared is more informative than SMAPE, MAE, MAPE, MSE and RMSE in regression analysis evaluation",
      "A New Typology Design of Performance Metrics to Measure Errors in Machine Learning Regression Algorithms"
    ]
  },
  {
    "arxiv_id": "2608.10305",
    "title": "COMPACT: Spectral Adjustment Scores from a Complete and Irreducible Causal Criterion",
    "abstract": "Observational datasets frequently contain many baseline variables, yet investigators estimating causal effects may not know which variables to include in the adjustment set. Confounding information may also be distributed weakly across many variables. Propensity scores can simplify adjustment by reducing high-dimensional covariates to a scalar with binary treatment. Although the propensity score is the coarsest balancing score, this distributional optimality does not imply maximal specificity over causal graphs. We instead examine all causal graphs among a candidate score, treatment, and outcome while allowing latent variables. Under faithfulness, we identify the largest set of unconditional and conditional dependence relations whose truth is invariant to whether treatment causes the outcome, leaving treatment-effect estimation to the downstream analysis. This criterion defines the maximally specific graph class expressible through these relations. We then develop the proposed algorithm, which operationalizes the criterion through a generalized eigenvalue problem whose score space targets the span of a balancing coordinate and an outcome-guided coordinate. We show that sufficiently informative proxies can recover this span without direct observation of the adjustment variables, characterize the resulting estimation and causal errors, and establish bootstrap validity for the complete procedure. Simulations and a real-data application demonstrate superior performance over sever",
    "categories": "stat.ME stat.ML",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Covariate Balancing Propensity Score",
      "Entropy Balancing for Causal Effects: A Multivariate Reweighting Method to Produce Balanced Samples in Observational Studies",
      "Principles of confounder selection"
    ]
  },
  {
    "arxiv_id": "2501.16979",
    "title": "A totally non-compensatory multi-criteria method for evaluating and improving level of satisfaction (LoS): proposal and application on Airport Terminal of Passengers",
    "abstract": "To evaluate and assign a service according customer's level of satisfaction (LoS) is a relevant issue in operations management. This is a typical situation in which the evaluators, have passed by heterogeneous experiences along their life which implies they could consider different variables when evaluating a product. Despite it, the models for measuring Los usually consider a homogeneous set of criteria when facing LoS evaluation. This study applies a totally non-compensatory modeling that allows each customer to select the criteria, from a whole set of aspects, the customer wants to use for evaluating LoS. The proposal was tested in evaluating LoS regarding the services provided by Airport Terminal of Passengers (ATPs) in Brazil, with data collected in a survey involving 19,240 passengers, interviewed at 15 Brazilian international airports. The data collected was imputed into ELECTRE TRI ME algorithm to obtain the a credibility degree of sorting the instances. The values of credibility degree were them used to obtain groups of ATPs. Finally, the statistical modes of the evaluations in each group were analyzed and compared. The proposal allowed a full non-compensatory approach to obtain the credibility degree even when considering perceptions from several evaluators that could use different criteria. As a result, it was identified, for each cluster of ATP, the criteria sets to be improved and even those to be prioritized. The pioneer modeling proposed in this article for eva",
    "categories": "stat.ME",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Fifty years of multiple criteria decision analysis: From classical methods to robust ordinal regression",
      "A Modified CRITIC Method to Estimate the Objective Weights of Decision Criteria",
      "Criteria list for assessment of methodological quality of economic evaluations: Consensus on Health Economic Criteria"
    ]
  }
]
```

## Output

One JSON object per abstract, one per line, no prose. Every input `arxiv_id`
appears exactly once. Include `ambiguous` even when false.
