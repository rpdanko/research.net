# triage batch 1/2 — domain: stats

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
    "arxiv_id": "2403.18115",
    "title": "Assessing Vaccine Effectiveness in Observational Studies via Nested Trial Emulation",
    "abstract": "Observational data are frequently used to evaluate real-world vaccine effectiveness (VE). For vaccines such as those developed against COVID-19, VE may vary over calendar time because of changes in circulating viral variants and over time since vaccination because of waning immunity. Nested trial emulation (NTE) provides a framework for estimating causal effects from observational data while reducing biases common to standard observational analyses. NTE involves emulating a sequence of hypothetical trials, each initiated from a different calendar date. This manuscript considers a NTE inverse probability weighted estimator of vaccine effectiveness that may vary over calendar time, time since vaccination, or both. The proposed approach characterizes trial-specific VE and uses those estimates to assess changes in vaccine protection across calendar time. As changes in VE estimates across trials may be attributable to variation in covariate distributions across trial-eligible populations, standardization of trial-specific estimates is considered. Statistical testing for evaluating heterogeneity in VE across trials is also considered. The methods are used to estimate vaccine effectiveness against COVID-19 outcomes using observational data on over 110,000 residents of Abruzzo, Italy during 2021.",
    "categories": "stat.ME stat.AP",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Target Trial Emulation to Improve Causal Inference from Observational Data: What, Why, and How?",
      "Constructing Inverse Probability Weights for Marginal Structural Models",
      "Improved tests for a random effects meta\u2010regression with a single covariate"
    ]
  },
  {
    "arxiv_id": "2511.07736",
    "title": "Improved Bounds for Context-Dependent Evolutionary Models Using Sequential Monte Carlo",
    "abstract": "Statistical inference in evolutionary models with site-dependence is a long-standing challenge in phylogenetics and computational biology. We consider the problem of approximating marginal sequence likelihoods under dependent-site models of biological sequence evolution. We prove an upper bound on the mixing time for a Markov chain Monte Carlo algorithm that samples the conditional distribution over latent sample paths, when the chain is initialized with a warm start. We then introduce a sequential Monte Carlo (SMC) algorithm for approximating the marginal likelihood, and show that our mixing time bound can be combined with recent importance sampling and finite-sample SMC results to obtain bounds on the finite sample approximation error of the resulting estimator. Our results show that the proposed SMC algorithm yields an efficient randomized approximation scheme for many practical problems of interest, and offers a significant improvement over a recently developed importance sampler for this problem. Our approach combines recent innovations in obtaining bounds for MCMC and SMC samplers, and may prove applicable to other problems of approximating marginal likelihoods and Bayes factors.",
    "categories": "stat.CO",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Sequential Monte Carlo without likelihoods",
      "Approximate Bayesian Computation in Population Genetics",
      "dynesty: a dynamic nested sampling package for estimating Bayesian posteriors and evidences"
    ]
  },
  {
    "arxiv_id": "2505.10510",
    "title": "Efficient Uncertainty Propagation in Bayesian Two-Step Procedures",
    "abstract": "Bayesian inference provides a principled framework for probabilistic reasoning. If inference is performed in two steps, uncertainty propagation plays a crucial role in accounting for all sources of uncertainty and variability. This becomes particularly important when both aleatoric uncertainty, caused by data variability, and epistemic uncertainty, arising from incomplete knowledge or missing data, are present. Examples include surrogate models and missing data problems. In surrogate modeling, the surrogate is used as a simplified approximation of a resource-heavy and costly simulation. The uncertainty from the surrogate-fitting process can be propagated using a two-step procedure. For modeling with missing data, methods like Multivariate Imputation by Chained Equations (MICE) generate multiple datasets to account for imputation uncertainty. These approaches, however, are computationally expensive, as multiple models must be fitted separately to surrogate parameters respectively imputed datasets. To address these challenges, we propose an efficient two-step approach that reduces computational overhead while maintaining accuracy. By selecting a representative subset of draws or imputations, we construct a mixture distribution to approximate the desired posteriors using Pareto smoothed importance sampling. For more complex scenarios, this is further refined with importance weighted moment matching and an iterative procedure that broadens the mixture distribution to better captu",
    "categories": "stat.ME",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Multiple Imputation of Missing Values",
      "Multiple Imputation by Chained Equations (MICE): Implementation in<i>Stata</i>",
      "Multiple imputation with multivariate imputation by chained equation (MICE) package."
    ]
  },
  {
    "arxiv_id": "2608.15455",
    "title": "Competing-Risk Cure Models: A Five-Axis Systematic Review of Methodological Literature",
    "abstract": "Competing-risk cure models describe time-to-event populations with individuals immune to all event types or an event of interest, yet literature is fragmented across model families. We review 26 papers across five axes: cure definition/scope; decomposition/cure mechanism; latency; dependence, censoring, and masked causes; and estimation. We distinguish global from cause-specific cure and incidence--latency mixtures from vertical susceptibility factorizations, latent competing-causes/zero-count constructions, defective-survival models, and zero-inflated mixture or cumulative incidence function (CIF) formulations. We compare parametric, piecewise-constant, PH, AFT, transformation, CIF-based, nonparametric, and partially specified latency models for right/interval censoring, clustering, and masked causes. Mixture formulations dominate, but similar names can mask different estimands, cure mechanisms, latent-risk/censoring assumptions, and regression interpretations. Latent-failure dependence is modeled less often than cure or latency; failure--censoring dependence, within-cluster association, and masked causes occur in smaller subsets. Estimation spans likelihood and expectation-maximization (EM), including neural-network M-steps, estimating equations, inverse-probability-of-censoring weighting, Bayesian computation, and copula-graphic estimation. A reproducible defective-Gompertz analysis of public bone-marrow-transplant data shows that fitted tail probabilities require model- a",
    "categories": "stat.ME",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Estimation in a Cox Proportional Hazards Cure Model",
      "Competing risks in epidemiology: possibilities and pitfalls",
      "Introduction to the Analysis of Survival Data in the Presence of Competing Risks"
    ]
  },
  {
    "arxiv_id": "1312.2291",
    "title": "Predictive analysis of microarray data",
    "abstract": "Microarray gene expression data are analyzed by means of a Bayesian nonparametric model, with emphasis on prediction of future observables, yielding a method for selection of differentially expressed genes and a classifier.",
    "categories": "stat.ME stat.AP",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A Bayesian missing value estimation method for gene expression profile data",
      "Empirical bayes methods and false discovery rates for microarrays",
      "Robust hyperparameter estimation protects against hypervariable genes and improves power to detect differential expression"
    ]
  },
  {
    "arxiv_id": "2608.08658",
    "title": "Mass Lumping and Numerical Quadrature for Approximation of Fractional Elliptic Differential Equations Driven by Gaussian White Noise",
    "abstract": "Fractional elliptic stochastic partial differential equations (SPDEs) are widely used in statistics and machine learning for computationally efficient and flexible modeling of Gaussian random fields. The computational efficiency of the SPDE approach relies on finite element approximations combined with numerical quadrature and mass lumping, which enable sparse matrix methods during inference. Although many works have studied finite element approximations of fractional SPDEs, the effect of the mass lumping and quadrature approximations used in practice has not been fully analyzed. To fill this gap, we derive convergence rates for numerical approximations of fractional SPDEs based on finite element discretizations combined with numerical quadrature and mass lumping. Specifically, we obtain explicit convergence rates for the mean-squared error of the covariance function in a general framework that covers the main settings where mass lumping is used in the SPDE approach. We also analyze non-stationary variance-control factors of the form $L^\\beta(\\tau u)=\\mathcal{W}$, where $\\tau$ is spatially varying, and derive covariance error estimates showing how the regularity of $\\tau$ affects the convergence rate. As specific examples, we provide results for random fields on bounded Euclidean domains, Riemannian manifolds, and metric graphs. Numerical experiments are presented that confirm the theoretical results.",
    "categories": "math.NA cs.NA math.ST stat.TH",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Bayesian Computing with INLA: A Review",
      "Adaptive estimation of a quadratic functional by model selection",
      "A Proximal Stochastic Gradient Method with Progressive Variance Reduction"
    ]
  },
  {
    "arxiv_id": "2603.24786",
    "title": "Refined Cluster Robust Inference",
    "abstract": "It has become standard for empirical studies to conduct inference robust to cluster dependence and heterogeneity. With a small number of clusters, the normal approximation for the $t$-statistics of regression coefficients may be poor. This paper tackles this problem using a critical value based on the conditional Cram\\'er-Edgeworth expansion for the $t$-statistics. The proposed critical value guarantees third-order refinement, and it does not require resampling because it is a closed-form function of the estimated score skewness and kurtosis. Simulations show that our proposal can make a difference in size control with as few as 10 clusters. Keywords: Cluster robust inference, Cram\\'er-Edgeworth expansion, Asymptotic refinement",
    "categories": "econ.EM math.ST stat.TH",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "A Practitioner\u2019s Guide to Cluster-Robust Inference",
      "Cluster-Sample Methods in Applied Econometrics",
      "Bootstrap-Based Improvements for Inference with Clustered Errors"
    ]
  },
  {
    "arxiv_id": "2409.18804",
    "title": "Convergence of Diffusion Models Under the Manifold Hypothesis in High-Dimensions",
    "abstract": "Denoising Diffusion Probabilistic Models (DDPM) are powerful state-of-the-art methods used to generate synthetic data from high-dimensional data distributions and are widely used for image, audio, and video generation as well as many more applications in science and beyond. The \\textit{manifold hypothesis} states that high-dimensional data often lie on lower-dimensional manifolds within the ambient space, and is widely believed to hold in provided examples. While recent results have provided invaluable insight into how diffusion models adapt to the manifold hypothesis, they do not capture the great empirical success of these models, making this a very fruitful research direction. In this work, we study DDPMs under the manifold hypothesis and prove that they achieve rates independent of the ambient dimension in terms of score learning. In terms of sampling complexity, we obtain rates independent of the ambient dimension w.r.t.\\ the Wasserstein distance. We do this by developing a new framework connecting diffusion models to the well-studied theory of extrema of Gaussian Processes.",
    "categories": "stat.ML cs.LG math.ST stat.TH",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "The Nonparanormal: Semiparametric Estimation of High Dimensional Undirected Graphs",
      "Noise-contrastive estimation of unnormalized statistical models, with applications to natural image statistics",
      "Gaussian Predictive Process Models for Large Spatial Data Sets"
    ]
  },
  {
    "arxiv_id": "2509.01604",
    "title": "A Time-Series Model for Areal Data Using Area-Specific Gaussian Processes with Spatially Correlated Hyperparameters",
    "abstract": "In many applied settings, areal data are observed repeatedly over long time periods, as commonly occurs in infectious disease surveillance and environmental or demographic monitoring. Accurate characterization of local temporal dynamics and uncertainty is important for monitoring disease trends, identifying local changes, and supporting public health decision-making. Traditional spatio-temporal models generally represent spatial, temporal, and space-time interaction components through structured random effects acting on the latent outcome process. We propose a Bayesian spatio-temporal hierarchical framework in which temporal dynamics are modeled using area-specific Gaussian processes, while spatial dependence is introduced through spatially correlated Gaussian-process covariance hyperparameters. This allows neighboring regions to share information about the characteristics of their temporal dependence while retaining area-specific temporal trajectories, providing an alternative representation of spatio-temporal dependence. Inference is performed using Markov chain Monte Carlo methods. The approach is illustrated using monthly malaria incidence data from three Mozambican provinces and evaluated using the Root Mean Squared Error, Continuous Ranked Probability Score, empirical coverage probability, and credible interval width. Compared with established spatio-temporal models, the proposed framework achieves competitive predictive accuracy and better-calibrated predictive uncerta",
    "categories": "stat.ME",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Bayesian Spatial Modelling with<i>R</i>-<b>INLA</b>",
      "Gaussian Predictive Process Models for Large Spatial Data Sets",
      "Approximate Bayesian Inference for Latent Gaussian models by using Integrated Nested Laplace Approximations"
    ]
  },
  {
    "arxiv_id": "2411.02771",
    "title": "Doubly robust inference via calibration",
    "abstract": "Doubly robust estimators are widely used for estimating average treatment effects and other linear summaries of regression functions. While consistency requires only one of two nuisance functions to be estimated consistently, asymptotic normality for linear functionals typically requires sufficiently fast convergence of both. We address this mismatch by showing that calibrating the nuisance estimators within a doubly robust procedure can yield doubly robust asymptotic normality. We introduce the idea of calibrated debiased machine learning (DML) and propose a specific implementation in which standard DML is augmented with a simple isotonic regression adjustment. We show that, under a partial orthogonality condition, a calibrated DML estimator remains asymptotically normal if either the regression function or Riesz representer of the functional is estimated sufficiently well, allowing the other to converge arbitrarily slowly or even inconsistently. We also propose a bootstrap-assisted method for constructing confidence intervals, enabling doubly robust inference without additional nuisance estimation. In a range of semi-synthetic benchmark datasets, calibrated DML reduces bias and improves coverage relative to standard DML. Our method can be integrated into existing DML pipelines by adding just a few lines of code to calibrate cross-fitted estimates via isotonic regression.",
    "categories": "stat.ME math.ST stat.ML stat.TH",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Inference on Treatment Effects after Selection among High-Dimensional Controls",
      "Double/debiased machine learning for treatment and structural parameters",
      "Towards optimal doubly robust estimation of heterogeneous causal effects"
    ]
  },
  {
    "arxiv_id": "2509.12173",
    "title": "Extrapolation of Tempered Posteriors",
    "abstract": "Tempering is a popular tool in Bayesian computation, being used to transform a posterior distribution $p_1$ into a reference distribution $p_0$ that is more easily approximated. Several algorithms exist that start by approximating $p_0$ and proceed through a sequence of intermediate distributions $p_t$ until an approximation to $p_1$ is obtained. Our contribution reveals that high-quality approximation of terms up to $p_1$ is not essential, as knowledge of the intermediate distributions enables posterior quantities of interest to be extrapolated. Specifically, we establish conditions under which posterior expectations are determined by their associated tempered expectations on any non-empty $t$ interval. Harnessing this result, we propose novel methodology for approximating posterior expectations based on extrapolation and smoothing of tempered expectations, which we implement as a post-processing variance-reduction tool for sequential Monte Carlo.",
    "categories": "stat.CO math.ST stat.ME stat.TH",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Approximate Bayesian Inference for Latent Gaussian models by using Integrated Nested Laplace Approximations",
      "Bayesian Computing with INLA: A Review",
      "Transitional Markov Chain Monte Carlo Method for Bayesian Model Updating, Model Class Selection, and Model Averaging"
    ]
  },
  {
    "arxiv_id": "2608.13131",
    "title": "Huber-Wasserstein barycenters for robust distribution-valued data",
    "abstract": "We propose a robust barycenter for distribution-valued data by incorporating the Huber loss directly into the optimal transport cost. In contrast to metric-space Huber means, which apply the Huber loss to the Wasserstein distance after optimization, our construction acts on individual transport displacements, preserving quadratic behavior locally while limiting the influence of large displacements. The resulting Huber-Wasserstein barycenters form a natural interpolation between Wasserstein means and $L^1$-type Wasserstein medians. We establish the analytical and statistical foundations of this construction. For optimal transport with Huber loss, we prove regularity and uniqueness properties of dual potentials, existence of optimal transport maps, and stability as the Huber parameter varies. For the associated barycenter problem, we prove existence and characterization results, consistency of empirical plug-in estimators, and a finite-sample breakdown point essentially equal to $1/2$. In dimension one, we further derive the pointwise influence function and asymptotic distribution, quantify the associated robustness-efficiency trade-off, and show that displacement-wise Huberization can retain first-order information that is lost by distance-based Huberization under localized shape contamination. Numerical experiments on contaminated distribution-valued data demonstrate the robustness of the proposed barycenters and illustrate their interpolation between mean- and median-like be",
    "categories": "stat.ME math.PR stat.ML",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Distributionally Robust Convex Optimization",
      "Robust Solutions of Optimization Problems Affected by Uncertain Probabilities",
      "Frameworks and Results in Distributionally Robust Optimization"
    ]
  },
  {
    "arxiv_id": "2608.16529",
    "title": "Randomization inference for treatment effects on survival outcomes",
    "abstract": "The log-rank test and Kaplan--Meier plot are standard tools for analyzing time-to-event data in randomized clinical trials, yet neither provides a summary of the magnitude of the treatment effect. Practitioners typically fill this gap by reporting a hazard ratio from a Cox proportional-hazards model or an acceleration factor from an accelerated failure time (AFT) model, but both require assumptions beyond those needed for the log-rank test or Kaplan--Meier estimator. We propose two nonparametric confidence intervals for scalar effect-size summaries, an additive shift c and a multiplicative factor $\\rho$, obtained by inverting the log-rank test under sharp null hypotheses of constant treatment effects. Building on the randomization-inference framework of Li and Small (2023), both intervals are valid under the randomization distribution alone, requiring no assumptions for the event-time distribution. We evaluate the proposed multiplicative interval via simulation, finding that it maintains nominal coverage across a range of censoring rates and sample sizes, including under data-generating processes that misspecify a parametric AFT model, while incurring only a modest efficiency loss compared to parametric AFT inference under correct specification. We illustrate the approach using data from a randomized trial of rhDNase for cystic fibrosis and provide R code and a Shiny application for ease of implementation.",
    "categories": "stat.ME",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Flexible parametric proportional\u2010hazards and proportional\u2010odds models for censored survival data, with application to prognostic modelling and estimation of treatment effects",
      "Understanding survival analysis: Kaplan-Meier estimate",
      "Enhanced secondary analysis of survival data: reconstructing the data from published Kaplan-Meier survival curves"
    ]
  },
  {
    "arxiv_id": "2502.00924",
    "title": "On the Graphical Rules for Recovering the Average Treatment Effect Under Selection Bias",
    "abstract": "Selection bias is a major obstacle toward valid causal inference in epidemiology. Over the past decade, several graphical rules based on causal diagrams have been proposed as sufficient identification conditions for addressing selection bias and recovering causal effects. However, these simple graphical rules are typically coupled with specific identification strategies and estimators. In this article, we show two important cases of selection bias that fall outside the scope of these existing simple rules and their estimators: one case where selection is a descendant of a collider of the treatment and the outcome, and the other case where selection is affected by a mediator. To address selection bias and recover the marginal average treatment effect in these two cases, we propose an alternative set of graphical rules and construct identification formulas using g-computation and inverse probability weighting (IPW) based on single-world intervention graphs (SWIGs), leveraging external information from individuals outside the selected sample. We conduct simulation studies to verify the performance of the estimators when the traditional crude selected-sample analysis (i.e., complete-case analysis) yields erroneous conclusions that contradict the truth. We emphasize that identifying causal effects in the presence of selection bias depends critically on both the target estimand and the availability of external information.",
    "categories": "stat.ME",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Toward a Clearer Definition of Selection Bias When Estimating Causal Effects",
      "A tutorial on propensity score estimation for multiple treatments using generalized boosted models",
      "Moving towards best practice when using inverse probability of treatment weighting (IPTW) using the propensity score to estimate causal treatment effects in observational studies"
    ]
  },
  {
    "arxiv_id": "2504.09654",
    "title": "A flexible Bayesian framework for detecting cross-sample spatial expression variability in heterogeneous tissues",
    "abstract": "Spatial transcriptomics measures gene expression alongside the spatial coordinates of each capture spot or cell across tissue samples. The detection of spatially variable (SV) genes, whose expression exhibits systematic spatial variation, enables the delineation of functional tissue domains and the identification of region-specific transcriptional changes that underlie disease heterogeneity. However, empirical evidence from spatial transcriptomics data indicates that existing methods are hindered by two practical issues: reliance on predefined spatial patterns that often miss tissue complexity, and a lack of standardized approaches for multi-sample integration, which undermines reproducibility and biological interpretability. To address these issues, we propose a novel integrated Bayesian hierarchical model that combines flexible nonparametric spatial modeling with information sharing across samples. The model uses an adaptive spatial process that can capture a wide range of spatial patterns while remaining interpretable. We also introduce a new prior that borrows strength across samples, enabling robust detection of SV genes from multiple tissue sections. An efficient variational approximation is developed for scalable posterior computation. Analyzing spatial transcriptomics data from human brain and skin cancer tissues, our framework identifies spatially structured SV genes, enabling the delineation of tissue domains and the discovery of functionally coherent gene clusters ",
    "categories": "stat.AP",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Gaussian Predictive Process Models for Large Spatial Data Sets",
      "Bayesian Spatial Modelling with<i>R</i>-<b>INLA</b>",
      "Model-Based Clustering, Discriminant Analysis, and Density Estimation"
    ]
  },
  {
    "arxiv_id": "2608.15497",
    "title": "Energy Balancing Weights for Mediation Analysis",
    "abstract": "Causal mediation analysis requires reconstruction of counterfactual distributions to estimate natural direct and indirect effects. Inverse probability weighting estimators rely on models for treatment assignment and mediator density ratios, whereas moment balancing approaches require researchers to specify in advance which functions of the covariates and mediators should be balanced. We propose Energy Balancing Weights for Mediation Analysis (EBWMA), which targets the joint mediator-covariate distribution used to identify counterfactual means such as E[Y(1, M(0))]. Under standard identification conditions for natural effects, EBWMA constructs weights whose weighted empirical distribution approximates this target, without modeling treatment assignment, mediator density ratios, or the outcome regression. The weights minimize energy distance through two quadratic programming problems solved sequentially. In simulations with nonlinearly transformed, skewed, or binary covariates and nonlinear mediator and outcome models, EBWMA generally achieved favorable bias and root mean squared error, with uniformly lower Monte Carlo variability than gradient boosting-based inverse probability weighting and moment balancing weights. In an illustrative analysis of the National Health and Nutrition Examination Survey I Epidemiologic Follow-up Study, EBWMA gave the smallest standardized mean differences for most covariates and for the mediator.",
    "categories": "stat.ME",
    "band": "near",
    "threshold": 3,
    "neighbours": [
      "Entropy Balancing for Causal Effects: A Multivariate Reweighting Method to Produce Balanced Samples in Observational Studies",
      "Mediation Analysis with Multiple Mediators",
      "Balancing Covariates via Propensity Score Weighting"
    ]
  },
  {
    "arxiv_id": "2512.16061",
    "title": "Parameter Estimation for Time-Scaled Inhomogeneous Phase-Type Distributions from Discrete Observations",
    "abstract": "Inhomogeneous phase-type (IPH) distributions extend classical phase-type (PH) models by allowing transition intensities to vary over time, offering greater flexibility for modeling heavy-tailed distributions or time-dependent absorption phenomena. Statistical inference for these models has largely assumed that absorption times, or entire trajectories, are observed exactly. In many applications, however, the process is observed only at discrete, irregularly spaced time points, so that transition and absorption times are unknown and estimation becomes a missing-data problem. We address this setting for the subclass with time-scaled sub-intensity matrices $\\boldsymbol{\\Lambda}(t) = h_{\\beta}(t)\\boldsymbol{\\Lambda}$, which admits a time transformation to a homogeneous Markov jump process (MJP). We develop an inference framework that combines Markov-bridge data augmentation with a Stochastic Expectation-Maximization (SEM) algorithm: at each iteration the latent continuous-time trajectories are simulated conditionally on the discrete observations, and the parameters are then updated by maximizing the resulting complete-data likelihood. The baseline sub-intensity matrix $\\boldsymbol{\\Lambda}$ is updated by its closed-form complete-data maximum-likelihood estimator, while the time-scaling parameter $\\beta$ is refined by gradient ascent on the same complete-data log-likelihood. The reported estimators are thus obtained from complete-data maximum-likelihood updates, avoiding constraine",
    "categories": "stat.ME stat.AP",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Transitional Markov Chain Monte Carlo Method for Bayesian Model Updating, Model Class Selection, and Model Averaging",
      "Markov Chain Monte Carlo Methods and the Label Switching Problem in Bayesian Mixture Modeling",
      "Variational inference for Dirichlet process mixtures"
    ]
  },
  {
    "arxiv_id": "2608.09872",
    "title": "Safe Start: Configuring Optimization Algorithms for Decision-Making under Extreme Risks",
    "abstract": "We consider stochastic optimization where the goal is not only to optimize an average-case objective, but also to mitigate the occurrence of rare catastrophic events. This problem is motivated by safety-aware decision-making and AI training. We first argue that, in the presence of a simulation model, natural attempts to integrate variance reduction into optimization, even executed in a reasonable adaptive fashion, encounter fundamental challenges in guaranteeing realistic runtime when using common stochastic gradient descent algorithms. This challenge arises from the extreme sensitivity of tail-based objectives with respect to the decision variables, which renders a dichotomic failure of convergence regardless of what step size we select. We offer remedies based on a new notion of safe start that allows for efficient finite-time error control, and show how the sampling complexity scales favorably under the combination of safe start and variance reduction. We illustrate our methodologies on examples in portfolio optimization and robust classification with neural networks.",
    "categories": "math.OC stat.ME",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A Proximal Stochastic Gradient Method with Progressive Variance Reduction",
      "Convexity, Classification, and Risk Bounds",
      "Robust Solutions of Optimization Problems Affected by Uncertain Probabilities"
    ]
  },
  {
    "arxiv_id": "2608.07303",
    "title": "Winning by Peeking: Unenforced Budgets and Test-Set Selection Inflate Short-Budget AutoML Comparisons",
    "abstract": "Comparisons between AutoML systems at short time budgets -- tens of seconds rather than hours -- are common in tool READMEs and workshop papers, and they are easy to get wrong. We report a case study in which a simple AutoML engine, Orcetra, appeared to beat FLAML and AutoGluon on 513 OpenML datasets, winning 57.1% of them at a nominal 60-second budget and 78.4% of datasets against FLAML alone at 30 seconds. Both margins came from protocol defects that a results table cannot show. The search loop scored every candidate on the test split and reported the best, making the headline metric a maximum over dozens of noisy estimates while the baselines selected on training data and touched the test set once; and the budget was checked before launching a candidate but never enforced during one, so the system consumed a median of 120 s against a 60-second budget, 2.24x the wall-clock AutoGluon used. Re-running with selection moved to a validation split, the deadline enforced externally and every framework pinned to an equal share of the machine, Orcetra's win rate on the re-run subset falls from 59.4% to 34.3% and no pairwise difference against either competitor remains significant. Recording both estimands inside a single search lets us attribute the collapse: the selection rule accounts for 4.8 percentage points and unequal compute for most of the rest. The same traces give the selection bias as a function of budget, measured rather than assumed: it grows with $K$ but reaches only 0",
    "categories": "cs.AI cs.LG math.ST stat.TH",
    "band": "far",
    "threshold": 5,
    "neighbours": [
      "Accelerating clinical evidence synthesis with large language models",
      "Evaluating the effectiveness of large language models in abstract screening: a comparative analysis",
      "LAG Length Selection and the Construction of Unit Root Tests with Good Size and Power"
    ]
  },
  {
    "arxiv_id": "2608.09612",
    "title": "Local conformal prediction for individual causal effects",
    "abstract": "Standard CATE estimators become inadequate under strong treatment-effect heterogeneity: confidence intervals for conditional means need not cover individual counterfactual effects. We propose an Individualized Causal Prediction (ICP) framework that constructs finite-sample valid conformal prediction intervals for the individual causal effect of a specific query unit. The method localizes calibration to a causally relevant neighborhood using cosine similarity weighted by Causal Forest variable importance, augments small local samples synthetically, and calibrates intervals with doubly robust AIPW conformity scores satisfying Neyman orthogonality. Under standard identifying assumptions (SUTVA and strong ignorability) and an outcome-independent calibration-set selection condition, the resulting intervals attain marginal coverage at the nominal level. The local design also supports approximately conditional coverage by making calibration scores more representative of the query unit. Experiments on a high-heterogeneity synthetic dataset and the IHDP benchmark demonstrate that local strategies improve point accuracy over global baselines while maintaining nominal or above-nominal coverage.",
    "categories": "stat.ME econ.EM",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Estimation and Inference of Heterogeneous Treatment Effects using Random Forests",
      "Causal inference and the data-fusion problem",
      "Recursive partitioning for heterogeneous causal effects"
    ]
  },
  {
    "arxiv_id": "2608.20406",
    "title": "Machine Learning and ARIMA Model Averaging for Adaptive Public Health Forecasting: Comparative Evaluation and an Ontario COVID-19 Case Study",
    "abstract": "Public health forecasts must respond to abrupt changes in surveillance data without over-extrapolating noise, reporting artifacts, or temporary trends. We evaluated autoregressive integrated moving average (ARIMA), random forest, and extreme gradient boosting (XGBoost) models using 190 weekly observations of publicly available Ontario COVID-19 case counts from January 2020 to October 2023. Rolling-origin time-series cross-validation preserved temporal order during model tuning and evaluation. Performance was assessed across three operating dimensions: responsiveness following selected turning points, forecast horizons of one to six weeks, and the amount of historical training data. We also developed Machine Learning and ARIMA Model Averaging (MLAMA), a non-negative performance-weighted ensemble with weights that vary by forecast horizon and responsiveness setting. Retrospective comparisons showed that ARIMA adapted rapidly after turning points but its normalized error increased at longer horizons. Random forest and XGBoost were less responsive initially but maintained more stable normalized error over longer horizons. For two-week forecasts at the end of the study period, training on the most recent data outperformed using longer historical periods, particularly for XGBoost. MLAMA achieved the lowest normalized mean absolute percentage error across most forecast horizons and ranked among the best-performing methods across responsiveness settings. These findings support select",
    "categories": "cs.LG stat.AP",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Interrupted time series analysis using autoregressive integrated moving average (ARIMA) models: a guide for evaluating large-scale health interventions",
      "Evaluating epidemic forecasts in an interval format",
      "Stability of clinical prediction models developed using statistical or machine learning methods"
    ]
  },
  {
    "arxiv_id": "2105.01962",
    "title": "Discrepancy geometry in approximate Bayesian inference: transport and risk perspectives",
    "abstract": "Approximate Bayesian Computation (ABC) replaces the evaluation of an intractable likelihood with comparisons between observed and simulated data. We develop a unified measure-theoretic framework for discrepancy-based Bayesian inference in which such comparisons are encoded through nonnegative compatibility weights. The proposed formulation provides a mathematical setting for studying both vanishing compatibility thresholds and large-sample asymptotic regimes, leading to convergence results and an asymptotic characterization of compatibility, including situations in which posterior concentration may fail. It also admits a natural variational interpretation through an entropy-regularized minimization principle and, when the discrepancy is induced by a Wasserstein distance, an intrinsic transport representation on spaces of probability measures, giving rise to risk-theoretic functionals. These results provide a unified probabilistic, asymptotic, variational, and geometric perspective on discrepancy-based Bayesian inference.",
    "categories": "math.ST math.PR stat.TH",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Variational Inference: A Review for Statisticians",
      "Markov Chain Monte Carlo Methods and the Label Switching Problem in Bayesian Mixture Modeling",
      "Variational inference for Dirichlet process mixtures"
    ]
  },
  {
    "arxiv_id": "2608.13152",
    "title": "Estimation of distribution functions, their jumps and interval probabilities under measurement error",
    "abstract": "We consider the classical additive measurement-error model $X=Y+Z$, where the latent random variable $Y$ has unknown distribution $F_Y$ and the error $Z$ has a known distribution. We develop direct estimators for three functionals of $F_Y$: (i) $F_Y(x)$ at continuity points; (ii) interval probabilities $F_Y(y)-F_Y(x)$ when $x<y$ are continuity points; and (iii) the size of a jump at a prespecified discontinuity. We derive non-asymptotic bias and variance bounds, and establish asymptotic unbiasedness and consistency. Unlike previous work, we do not require $F_Y$ to admit a density, have a mixture representation, or satisfy global Sobolev smoothness assumptions. The framework accommodates arbitrary latent distributions, including those with both discrete and continuous components, and distributions with multiple jumps. These results rely on a link between Fourier inversion theorems and the algebraic structure of a class of estimators proposed in Mynbaev, Martins-Filho and Henderson (2022). A simulation study evaluates feasible tuning procedures and, where available, compares the finite-sample performance of the proposed estimators with existing methods.",
    "categories": "econ.EM math.ST stat.ME stat.TH",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Efficient Estimation of Models with Conditional Moment Restrictions Containing Unknown Functions",
      "Optimal Bandwidth Choice for the Regression Discontinuity Estimator",
      "Convergence rates of posterior distributions"
    ]
  },
  {
    "arxiv_id": "2608.17248",
    "title": "Information fusion and machine learning for sensitivity analysis using physics knowledge and experimental data",
    "abstract": "When computational models (either physics-based or data-driven) are used for the sensitivity analysis of engineering systems, the sensitivity estimate is affected by the accuracy and uncertainty of the model. This paper considers global sensitivity analysis (GSA) for situations where both a physics-based model and experimental observations are available, and investigates physics-informed machine learning strategies to effectively combine the two sources of information in order to maximize the accuracy of the sensitivity estimate. Two representative machine learning (ML) techniques are considered, namely, deep neural networks (DNN) and Gaussian process (GP) modeling, and two strategies for incorporating physics knowledge within these techniques are investigated, namely: (i) incorporating loss functions in the ML models to enforce physics constraints, and (ii) pre-training and updating the ML model using simulation and experimental data respectively. Four different models are built for each type (DNN and GP), and the uncertainties in these models are included in the Sobol indices computation. The DNN-based models, with many degrees of freedom in terms of model parameters and training options, are found to result in smaller bounds on the sensitivity estimates when compared to the GP-based models. The proposed methods are illustrated for additive manufacturing and lake temperature modeling examples.",
    "categories": "cs.CE cs.LG stat.ME stat.ML",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "A review of predictive uncertainty estimation with machine learning",
      "Review on Graph Neural Networks for Process Soft Sensor Development, Fault Diagnosis, and Process Monitoring",
      "Fault Detection and Diagnosis in Industry 4.0: A Review on Challenges and Opportunities"
    ]
  },
  {
    "arxiv_id": "1209.4947",
    "title": "Bayesian Analysis of Simple Random Densities",
    "abstract": "A tractable nonparametric prior over densities is introduced which is closed under sampling and exhibits proper posterior asymptotics.",
    "categories": "math.ST stat.TH",
    "band": "mid",
    "threshold": 4,
    "neighbours": [
      "Convergence rates of posterior distributions",
      "Variational inference for Dirichlet process mixtures",
      "The horseshoe estimator for sparse signals"
    ]
  }
]
```

## Output

One JSON object per abstract, one per line, no prose. Every input `arxiv_id`
appears exactly once. Include `ambiguous` even when false.
