# stats.md — rewrite prep

Working document, not a charter. Purpose: put every §2/§3 rule next to the vetting
evidence it was derived from, so you can rewrite in your own words while looking at
what you actually wrote, rather than at my paraphrase of it.

Line numbers refer to `canon/vetting-stats.md`. Reasons are verbatim, typos included.

**How to use this.** Work down §A first — those are the six places the charter says
something you did not. Each has a `RULING:` line; write on it. §B is the routine
rule-to-evidence mapping, for spot-checking. §C is what the evidence contains that the
charter does not mention at all.

Vetting totals: 150 papers, ~45 keeps, ~105 strikes. Strike-reason vocabulary clusters:
"Specific to X" ~45 · reporting/guideline/statement ~25 · "too rudimentary" 11 ·
psychology 7 · meta-analysis 3 · software 3 · political science 2.

---

## §A. Six places the charter goes beyond what you said

### A1. Meta-analysis — you banned it, the charter doesn't mention it

**You wrote** (line 23, on *Quantifying heterogeneity in a meta-analysis*, Higgins &
Thompson, 37k cites): `I don't do metaanalysis`. Again at 395 (`Metanalysis work`) and
767 (`Metal analysis`).

**Charter says:** nothing. Meta-analysis appears in neither §2 nor §3.

**Why this matters more than the psychology ban.** The Higgins paper derives H, R and I²
from mathematical criteria and analyses their properties — it is a methodology paper by
every criterion in §2. You struck it on topic. Under the current charter, triage admits
it and probably scores it 4. This is the cleanest case in the whole worksheet of a rule
that is *about a subject you don't work on*, applied to a paper with real transferable
machinery. The psychology debate in §8 is the same argument with weaker examples.

There are three coherent positions and the charter currently holds none of them:

1. Meta-analysis is out, full stop — a topic ban you're entitled to.
2. Meta-analysis methodology is in, meta-analytic *applications* are out — the §2/§3
   content split applied consistently.
3. It's ambiguous — a §5 flag, admitted but visible.

`RULING:`

---

### A2. "Too rudimentary" — stated 11 times, dropped entirely

**You wrote it at** lines 329, 359, 365, 371, 539, 719, 731, 827, 857, 905, 911. Variants:
`Too rudimentary to be valuable` · `to be helpful` · `to be useful` · `Does not seem like
a great resource, very rudimentary` · `Rudimentary guide not a methods paper`.

**Charter says** (§8): dropped as "unactionable for a Haiku agent scoring a preprint
abstract, and redundant — every 'rudimentary' strike in your worksheet is caught by the
tutorial/expository or no-contribution criteria."

**The redundancy claim is mostly true and worth checking anyway.** The strikes at 905/911
are explicitly guides; 329 pairs it with the political-science rule. But "rudimentary"
was your second-most-used strike word after "specific," and eleven uses of a word is a
judgment the charter now expresses nowhere. If what you meant was closer to *the
statistics in this paper is beneath the level I work at* — a depth threshold rather than
a genre test — that is a real criterion and §7 is where it would live.

`RULING:`

---

### A3. Psychology and political science — the §8 decision, restated with the evidence

**You wrote:** `Do not include psychology papers` (545, 551, 617, 701, 881 — five times,
identical wording) · `Specific to psychology` (257) · `Specific to psychology, which tends
to be rudimentary in terms of statistical advancements` (521) · `Too rudimentary. In
general, do not include political science papers unless they include statistician
coauthors` (329) · `Do not include political science articles` (641).

**Charter says** (§3 + §5): no field ban. Content criteria plus `[applied-field-methodology]`.

**My three arguments, compressed** (full version in §8): the coauthor clause is
unexecutable under `triage.md`'s "do not infer authorship"; Invariant 9 prices recall
over precision ~3:1 and a field ban is permanent invisible recall loss; every paper you
actually struck under those labels is independently caught by the software, tutorial, or
no-contribution criteria.

**The argument against my argument**, which §8 makes too briefly: you said it five times
in identical words. That is not an offhand remark, and "every struck paper is caught
anyway" cuts both ways — if the content rules already catch them, the ban costs nothing
in the canon and only bites on hypothetical arXiv papers neither of us has seen.

`RULING (psychology):`

`RULING (political science):`

---

### A4. "Specific to X" — 45 strikes compressed into one line

This is your dominant strike vocabulary and it deserves more of your attention than the
field bans, because the charter's whole §3 rests on how it's read.

**You wrote:** `Specific to` — the danish civil registration system (143), antidepressants
(179), animal research (191), migration (209), cohort studies (239), polycystic ovary
syndrome (251), psychology (257), physiology (263), FDA reporting (281), consensus building
in biomedical research (287), experimental design (293), study design (305), software (311),
sepsis (317), recommendations (353), surveys (389), reporting (413), exercise science (431),
questionaires (437), actuarial work (443), patient risk (455), ecology (491), patient risk
assessment (497, 503), study design (509), Delphi trudies (557), oncology (575), patient
data applications (581), case reporting (629), smoking (653), epidemiology (671), the
attitudes of populatiojn (695), mass communication (707), drug development (755), animal
research (761), Delphi studies (797), risk analysis in patients (821), peridontics (851),
labor (869), ecology (875) — plus `Seems like a specific thing, not statistics methodology`
(29), `Specific trial framework not general methodology` (647), `Probably too specific to
be useful` (563), `Do not include any chiropractice papers` (35).

**Charter says** (§3, first bullet): "Applications with no methodological contribution,
however good the science."

**The interpretation I made and you should check.** I read "specific to X" as *this paper
is an application in field X with no transferable machinery* — i.e. the operative word is
"application," and X is incidental. The alternative reading is that the operative word is
"specific": the paper is narrow, tied to one setting, and would not generalise even if
there were machinery in it. Those diverge on a real class of paper — a genuinely novel
estimator developed for and demonstrated only on one clinical setting. Reading one rejects
it; reading two rejects it; reading *my* charter admits it, because it has methodological
contribution. Three of your strikes (143 Danish registry, 317 sepsis, 251 PCOS) are close
to this shape.

`RULING — which reading:`

---

### A5. Experimental design — struck five times, then restored as in-scope

**You wrote:** `Experimental design study` (275) · `Specific to experimental design` (293) ·
`Specific study design` (509) · `Study design` (683) · `Trial design` (713).

**Charter says** (§2): "Experimental design with mathematical structure" is in scope.
§8 justifies this as restoring "scope dropped by omission" — that "absence from the canon
is not evidence of exclusion."

**But this was not absence.** You struck design papers five times, and §8's argument
doesn't apply to a category you actively rejected. I checked the papers before writing
this and the restoration is still defensible — 271 is *BJP guidance on planning and
reporting experimental design*, 289 is *ROBINS-I*, a risk-of-bias assessment tool. Both
are reporting/guidance documents that happen to have "design" in the title, and your
reason field named the topic rather than the genre. So the strikes are consistent with
§3, not with a ban on design theory.

**This is the pattern to watch for generally:** your reason fields name topics, my charter
converts them to genres, and the conversion is invisible unless someone reads the papers.
It's right here. Confirm it's right here.

`RULING:`

---

### A6. A keep that contradicts §3 outright

**Line 13–17:** `W2891378911` **PRISMA Extension for Scoping Reviews (PRISMA-ScR)** —
`mark: K`, `reason: Benchmarking paper for methodology and reporting quality`.

**Charter says** (§3): "Reporting and checklist guidelines — CONSORT, PRISMA, ARRIVE,
STROBE, TRIPOD, ROBINS, GRADE and their variants." PRISMA is named explicitly as
out of scope.

You kept a PRISMA paper and I wrote a rule that excludes it by name. Either the keep was
a slip (it is the very first row of the worksheet, and you struck every other reporting
guideline), or "benchmarking paper" means these have a use here I haven't understood.

`RULING:`

---

## §B. Routine rule-to-evidence map

Spot-check these; they're where I think the inference was safe.

| §2 criterion | Evidence | Confidence |
|---|---|---|
| Causal inference — identification/estimation | DiD (161, 203, 485), TWFE (467), RDD (743), weak IV (587), propensity scores (101, 215), confounder theory (533), program evaluation (347), cluster-robust (137) | **Strongest signal in the worksheet.** 9 keeps, several starred, and you volunteered "incredibly active topic" three separate times. |
| High-dimensional inference | Lasso/Dantzig (623), Lasso (725) | Solid — 2 starred keeps, both with "highly active topic" language. |
| Estimators/tests with analyzable properties | `Statistics methodology` ×6 (47, 53, 59, 155, 269, 635), `Methodology paper` ×7 (773, 815, 839, 845, 863, 899, 917), `Serious memthdological advance` (401) | Solid, but your reason field is a bare label here — the criterion's *content* is my construction, not yours. Worth a sentence in your words. |
| Statistical computation with provable properties | Stan struck as `Description of STAN` (515); `Specific software paper` (593); `Specific software` (311) | The algorithm/implementation split is mine. Your evidence establishes only the negative half. |
| Evaluation methodology | `Prediction model evaluation` (167), `Good resource for the performance of classifying algorithms` (407), `Evaluation of regressions` (449), `Model analytics` (479) | Good. |
| Nonparametric / semiparametric, function-space | — | **No direct evidence.** Restored in pass 3 on the "absence ≠ exclusion" argument. Entirely my inference from a canon that had none. |
| Assumption-lean inference, misspecification | — | **No direct evidence.** Same as above. |
| Bayesian foundations | `Good basis for bayesian methods` (425), `Foundational material for statistical procedures` (131), `Important book foundational to modern data science` (791) | Present in your keeps, absent from §2 as a named criterion — folded into "computation" and "estimators." |

| §3 criterion | Evidence | Confidence |
|---|---|---|
| Reporting/checklist guidelines | ~25 strikes (65, 77, 95, 107, 113, 173, 245, 323, 413, 419, 737, 779, 887, 893…) | Overwhelming — largest struck category. |
| Reviews, tutorials, expository | `Discussion paper` (71), `Statement not really a paper` (569), `Statement not paper` (665), `Culture statement` (611), `Statement paper not methdology` (803), rudimentary guides (905, 911) | Strong. |
| Software announcements | 311, 515, 593 | 3 strikes, all unambiguous. |
| Applications w/o contribution | the ~45 "specific to" cluster — see A4 | Strong on volume, ambiguous on meaning. |
| Reproductions and errata | — | **No evidence.** My addition. Harmless, but not yours. |

---

## §C. In the evidence, absent from the charter

- **Reproducibility as a value.** `Reproducibility is a valuable philosophical framework
  for this project` (83), `Reproducibility is fundamental to scientific research` (149),
  `Philosophical underpinning behind statistics` (197) — three keeps, and the first one
  says *for this project*. Nothing in the charter admits methodology-of-science work.
  §2's evaluation-methodology bullet is the closest and doesn't cover it.
- **Flow cytometry / arcsinh** (227): `Important for using flow cytometry data which uses
  arcsinh transformations`. A keep justified by your own downstream use. Whether the KB
  should admit papers because *you need them* rather than because they bridge is a
  question the charter doesn't raise anywhere.
- **`Interesting idea and worth thinking about*`** (383) — a keep on interest alone, with
  a Tier-0 star. Same question.
- **Meta-publishing / metascience** (89 `More meta of publishing than actual statistics`,
  221 sponsorship effects, 833 `more like metametrics`) — struck consistently. Sits
  uneasily beside the three reproducibility keeps above; worth one line distinguishing them.

---

## §D. Two data defects to fix while you're in these files

- `vetting-stats.md` line 334: `mark: Surgical guidelines` / `reason:` (empty). The mark
  field holds what was meant as the reason; the strike is correct by the leading "s" but
  the reason is lost. Restore it as `mark: S` / `reason: Surgical guidelines`.
- `vetting-compbio_methods.md` line 148 (`W4408399347`): never marked, so it sits in
  Tier 1 by default rather than by review.
