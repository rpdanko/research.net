# How to write rubric anchors

The rubric files in this directory ship with placeholder anchors. They are structurally correct and substantively generic, which means they will produce scores that cluster at 4 and measure nothing. **Replacing them is the single highest-leverage hour you will spend on this system**, and it is the one part no agent can do for you, because the anchors have to encode *your* judgment.

This document is how to do that.

---

## 1. Where this method comes from

The technique is **BARS** — Behaviorally Anchored Rating Scales — developed by Smith and Kendall in 1963 for performance appraisal, and built on Flanagan's 1954 **critical incident technique**. The insight is simple and holds up sixty years later:

> A rating scale becomes reliable when each scale point is anchored to a **specific, observable example** rather than an adjective.

"3 = adequate novelty" is not a scale point. It is a word that each rater, human or model, resolves against their own priors. "3 = the method is new but the question it answers has an accepted answer obtained another way" is a scale point, because two raters can look at a proposal and agree on whether that describes it.

The LLM-as-judge literature arrived at the same conclusion independently. Rubrics that specify concrete evidence — citations, numerical checks, logical structure — measurably outperform rubrics of vague descriptors, and a small number of *graded worked examples* calibrates a judge better than any amount of instruction.

---

## 2. The six rules

**1. Anchor on observable properties of the artifact, not on your reaction to it.**

The test: could two people disagree about whether the anchor applies, without disagreeing about the proposal? If yes, rewrite.

- ✗ `4 = a strong and well-motivated project`
- ✓ `4 = names a specific dataset, states an access route, and the effort estimate identifies which single component dominates`

**2. Write in present tense, describing the artifact.**

BARS anchors are written as behaviors: "completes quality checks before shipping," not "is quality-conscious." The equivalent here is describing what the spec *does*, not what it *is*. "Cites prior work that does most of this" beats "is derivative."

**3. Levels must differ in kind, not in degree.**

The most common broken rubric is one where the levels are "poor / fair / good / very good / excellent" with the nouns swapped in. Each level should describe a **different situation**, so that moving between levels means something changed about the proposal rather than about your mood.

- ✗ `2 = somewhat novel`, `3 = moderately novel`, `4 = quite novel`
- ✓ `2 = done, by someone else, this way` / `3 = same question answered by a different method` / `4 = same method, different question`

Notice the ✓ version is not even ordered by how much you like it. It is ordered by a fact about the literature. That is what makes it usable.

**4. Make the top achievable.**

BARS practice: if the 5 describes performance nobody reaches, raters stop using the top of the scale and the effective range collapses to 1–4. Your 5 should describe something you have actually seen, or expect to see a few times a year. If your novelty 5 is "opens a new subfield," you have a four-point scale.

**5. Make the bottom reachable too.**

The mirror problem, and worse for LLM judges, which are reluctant to use 1. If your 1 is "incoherent," nothing project-architect writes will ever score 1, because it writes fluent prose. Your 1 should describe something a *competent-sounding* proposal can be: `1 = the named dataset does not exist and no route to equivalent data is given`.

**6. One rubric per dimension. Never combine.**

Keep `feasibility.md`, `relevance.md`, and `novelty.md` as separate files, evaluated in separate agent invocations. A judge scoring several dimensions in one pass anchors on the first and lets it bleed into the rest, returning correlated scores that look like three measurements and are really one. This is why the referee agents are split by axis rather than by domain alone.

---

## 3. Where your anchors come from

Do not write anchors from your armchair. They come from **critical incidents** — real cases where your judgment was strong and clear. The Weeks 8–9 calibration period exists to generate them.

### The procedure

**Step 1 — Collect (2 weeks).** Run the referees but ignore their verdicts. Read each proposal yourself and score all three axes. Keep a file per axis. When you have a strong reaction — "obviously infeasible," "this is clearly novel" — **write down the reason immediately, in one sentence, in the proposal's own vocabulary.** The reason is the anchor. The score is just where it goes.

You want 8–15 incidents per axis. Twelve proposals over two weeks gets you there.

**Step 2 — Sort.** Lay the incidents out per axis and group them by *kind of reason*, not by score. Kinds that recur become levels. You will usually find you have three or four natural kinds, not five — that is fine and better than inventing a fifth.

**Step 3 — Write one to three anchors per level**, in the language of the incidents. Do not generalize them into abstractions; the specificity is the value. `1 = the data would require a cohort that has not been assembled` is a better anchor than `1 = data unavailable`, even though it looks narrower.

**Step 4 — Retranslate.** This is the BARS validation step and the one everybody skips.

Take your scored proposals from Step 1. Strip your scores. Hand them, plus your new anchors, to a fresh agent, and have it score them cold:

```bash
python3 ingest/retranslate.py --axis novelty --cases calibration/novelty/*.md
```

Compare against your scores. In classical BARS you keep only the incidents where independent raters agree closely and discard the rest. Apply the same discipline: **anchors that fail to reproduce your judgment are bad anchors, not evidence that the model is bad.** Rewrite or delete them.

Agreement within ±1 on 80% of cases is a working rubric. Below that, the anchors are still doing adjective work somewhere — find the cases where the model diverged and read what it quoted.

**Step 5 — Re-check quarterly.** Your judgment drifts as the KBs teach you things. So does the character of what project-architect produces. Rerun the retranslation on a fresh dozen cases every few months.

---

## 4. Worked example

Here is the novelty axis, before and after.

### Before — what not to ship

```yaml
5: Highly novel, opens new ground
4: Novel contribution
3: Moderately novel
2: Limited novelty
1: Not novel
```

Every level is the same sentence with the intensity dialed. A model will score almost everything 4, because most proposals are fluent and "novel contribution" is not falsifiable.

### After — anchored on the state of the literature

```yaml
5: No paper approaches this question from any direction. The closest work
   is in a field that would not recognize the question as theirs.
   Rare — expect a few per year, not per month.

4: Same method applied to a different question, or the same question
   approached with a method the field has not tried. Prior work exists
   and is citable, but does not answer this.

3: The question has an accepted answer obtained by another route, and
   this proposal would re-derive it. May still be worth doing if the new
   route is substantially cheaper or more general — but that, not the
   result, is then the contribution, and the spec must say so.

2: Done in another field under different vocabulary. The translation may
   have value; the research does not.

1: A paper exists doing this question, this method, this purpose. Cite it.
```

Now the levels differ in kind. A referee can find the state of the literature and read off a level. And crucially, **you can disagree with a score by pointing at a fact** — "no, level 2 is wrong, that field's version assumes X" — which is what makes the rubric improvable rather than merely present.

Note that anchor 3 carries a conditional. Real rubrics need those. Do not smooth them out for tidiness; the conditionals are where your actual judgment lives.

---

## 5. Failure patterns to watch for

| Symptom | Cause | Fix |
|---|---|---|
| Everything scores 4 | Adjective anchors; unreachable 5 and 1 | Rewrite extremes with reachable, concrete descriptions |
| Scores track writing quality | Anchors describe the *proposal*, not the *world* | Re-anchor on facts about data, literature, or the field |
| Three axes move together | Axes scored in one pass, or anchors overlap | Verify separate invocations; check no anchor mentions another axis |
| Model quotes an anchor that does not fit | Anchors are not mutually exclusive | Add a disambiguating clause to whichever is broader |
| You disagree but cannot say why | The anchor encodes a judgment you have not articulated | Good signal — write the missing incident down and add a level |
| Scores drift upward over months | Nothing; this is normal | Quarterly retranslation catches it |

The `review_audit.py --month` script reports the score distribution per axis. **Watch the shape, not the mean.** A healthy axis has spread. An axis where 80% of scores land on one value is not measuring; it is decorating.

---

## 6. On the binary verdict

Each referee gives both a binary `reject: yes/no` and a 1–5 score, and **the gate acts only on the binary**. This is deliberate.

Binary judgments from LLM judges track human agreement more reliably than 5-point ones; fine-grained scales invite a judge to invent distinctions it cannot defend. The scores are still worth collecting — they rank survivors, and their distribution is your best drift detector — but they should not decide anything on their own.

So write your anchors carefully, and then don't let them hold the trigger.

---

## 7. Reading

**On anchored scales**

- Smith, P.C. & Kendall, L.M. (1963), *Retranslation of expectations: an approach to the construction of unambiguous anchors for rating scales*, Journal of Applied Psychology. The original BARS paper, and the source of the retranslation step in §3.
- Flanagan, J.C. (1954), *The Critical Incident Technique*, Psychological Bulletin. Where "collect real cases before writing the scale" comes from.
- Jonsson, A. & Svingby, G. (2007), *The use of scoring rubrics: reliability, validity and educational consequences*, Educational Research Review. Meta-review; the finding that matters here is that rubric reliability comes from specificity plus rater training, not from scale granularity.

**On research-evaluation rubrics specifically** — worth reading as anchor examples, since these people have been refining this exact problem for decades

- **NIH scored review criteria** (Significance, Innovation, Approach; 1–9). The closest institutional analogue to your three axes. Note how the guidance describes *what a reviewer should look for*, not how good it should be.
- **NSF merit review** (Intellectual Merit, Broader Impacts). Useful mostly as a contrast: deliberately broader anchors, and correspondingly noisier outcomes.
- **NeurIPS / ICLR reviewer guidelines**, current cycle. The best public example of separating "is it correct," "is it novel," and "does it matter" into axes that are scored independently — and the annual reviewer-calibration discussions are a live case study in anchor drift.

**On LLM judges**

- Zheng et al. (2023), *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. Foundational; documents position bias, verbosity bias, and self-preference.
- Liu et al. (2023), *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment*. On structured chain-of-thought before scoring — the ancestor of the reject-first ordering in the referee agents.
- [Rubric-Conditioned LLM Grading: Alignment, Uncertainty, and Robustness](https://arxiv.org/abs/2601.08843) (2026). Recent, and directly on point for rubric-conditioned grading, calibration anchors, and deferral.
- [LLM-as-a-Judge: A Practical Guide](https://towardsdatascience.com/llm-as-a-judge-a-practical-guide/) — practitioner-level, good on the one-rubric-per-dimension point.

**Practitioner references on BARS construction**

- [Behaviourally Anchored Rating Scale: A Complete Guide](https://engagedly.com/blog/behaviourally-anchored-rating-scale-a-complete-guide/)
- [BARS templates and examples by competency and level](https://sprad.io/blog/behaviorally-anchored-rating-scale-bars-templates-examples-by-competency-and-level-free-downloads)

The HR framing is a poor fit for research proposals, but the *construction mechanics* — incident collection, clustering, retranslation, discarding low-agreement items — transfer directly, and those blog posts spell them out more concretely than the original papers do.
