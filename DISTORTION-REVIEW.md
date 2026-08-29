# research-net against a taxonomy of distorted output

An evaluation against Sun, Sheng, Zhou & Wu, *AI hallucination: towards a comprehensive classification of distorted information in AIGC*, Humanit Soc Sci Commun 11:1278 (2024). https://doi.org/10.1057/s41599-024-03811-x

**Status: built.** Invariants 17–19 in `CLAUDE.md`; vocabulary in `rubrics/ERROR-TYPES.md`; three new scripts. Nothing in 1–16 was reversed.

Companion to `HYBRID-SYSTEM-REVIEW.md`, which took the same pipeline against Clark's *Extending Minds*. The two papers turn out to fault it in opposite directions, and the pairing is more useful than either alone — see §5.

---

## 1. What the paper is, and how much of it to believe

A content analysis. 243 ChatGPT failure samples from a public error tracker, decomposed into 284 error points, coded by three people into a taxonomy of 8 first-level and 31 second-level error types.

The method is the strong part and is worth separating from the findings:

- Three coders, independent, "back-to-back" — each blind to the others' coding.
- 70% of samples for pre-coding (building the scheme), 30% held back for test coding (validating it).
- Reliability by Holsti's method against a 70–80% threshold (Boettger & Palmer 2010).
- **First round came in at 68%, below threshold.** They did not proceed. They discussed the discrepancies, re-coded, reached 89%.
- Explicit rule that new categories emerging during test coding means returning to pre-coding, not widening an existing category.
- Merged categories recorded rather than deleted, with reasons.

**The frequency table is the weak part, and the paper does not say why.** Samples came from a Typeform tracker where users voluntarily submitted ChatGPT errors. That measures *what people noticed and bothered to report*, not what models get wrong. Measurement-unit errors topping the table at 40 is at least as consistent with "unit errors are conspicuous and satisfying to report" as with "unit errors are common." The paper lists adjacent limitations candidly — one model, one platform, 2023 vintage, incomplete category coverage — but never addresses the self-selection, which is the sharpest problem with the numbers.

So the taxonomy is used here as a **checklist**, the frequencies as a **weak prior on where to look first**, and nothing is treated as a base rate. This distinction is written into `rubrics/ERROR-TYPES.md` so that a future reader does not inherit the numbers as fact.

Fourteen of the 31 types were kept. The dropped seventeen are consumer-content failures — hate news, clickbait, propaganda, parody, trolling — plus reasoning categories about physical and social situations that never arise in a pipeline reading mathematics. Dropped categories are recorded with reasons, following the paper's own merge convention.

---

## 2. The finding that matters most

**This pipeline was defended against being wrong and undefended against being fabricated, and those need different machinery.**

Invariants 1–16 are a sophisticated apparatus for catching *bad judgment*: three referees split by axis so scores do not contaminate each other, binary gates because binaries track human agreement better, pre-registration hashes because models rationalise after the fact, negative controls in every probe. All of it assumes the failure is a judgment that can be re-judged.

Fabrication is not that. Consider the two most consequential outputs in the system:

```
skeptic.prior_work    "arXiv:2401.xxxxx does X, which is most of this"   -> kills a bridge
referee-novelty       "the closest work is Y, which does Z instead"       -> kills a proposal
```

A fabricated identifier in either produces no visible error. It produces a confident, well-reasoned, correctly-formatted judgment with a reference attached — and the reference is precisely what makes it persuasive to every downstream stage and to you. No gate catches it, because every gate is looking for bad reasoning and the reasoning is fine. The premise is invented.

Sun et al. name this "false academic information" and quote its exact shape: *"fictitious papers, apparently irrelevant fictitious references in reviews, and non-existent web links."* Walters & Wilder (2023), which they cite, found it throughout ChatGPT bibliographies.

And the errors are **asymmetric in the worst direction**. A wrongly-passed bridge costs a few dollars and dies at the next gate. A bridge killed by a fabricated `already-done` citation is gone permanently, and nothing will ever surface it again — the same asymmetry invariant 9 uses to justify recall-over-precision in triage, operating here with nothing defending against it.

`verify_citations.py` resolves every identifier against arXiv and OpenAlex, and a non-resolving one **invalidates the artifact** rather than being logged. Two design points that matter more than the script:

- **Unreachable ≠ fabricated.** Exit 2 versus exit 1. A rate-limited scan that read as mass invention would destroy a week's work and teach the wrong lesson, and this is the same distinction invariant 5 already makes between `inconclusive` and `falsified`.
- **Resolution proves existence, not relevance.** The paper's phrase is "apparently *irrelevant* fictitious references" — a real paper cited for a claim it does not support, which they suggest is the more common half. No script can check it. `sample --n 3` shows you the claim beside the actual abstract, three a week, three minutes. Not coverage; enough to notice a rate.

### The one with no check at all

`math-scout.theory_gap` — by the repo's own description "the highest-value text in this system." It reaches `bridge-finder` through no gate whatsoever, and it is shaped exactly like the paper's `false-proof` category: *"fabricating the proof process for scientific theorems that have been proven or not yet proven."*

*"compbio uses entropic regularization with fixed epsilon; math.OC has adaptive schedules with better rates since 2024."*

That is the repo's own example of a good `theory_gap`, and it contains a rate claim, a date, and a subfield attribution, none of which anything verifies. If it is wrong, it produces a real-looking bridge, a well-argued proposal, and a referee gate with no way to check the premise — checking it means reading the mathematics, which is `math-scout`'s job and nobody else's.

Invariant 18 requires a resolvable citation for any asserted frontier, and requires unciteable gaps to be written as questions rather than facts. That is the best available fix and it is not a full one. `ERROR-TYPES.md` records `false-proof` with "what catches it: **nothing**," deliberately, because a row admitting a gap is worth more than a row pretending otherwise.

---

## 3. Where the frequencies were informative anyway

One result survives the sampling critique, because the bias plausibly runs the wrong way to explain it.

**Mathematical errors: measurement-units 40, conceptual 14, calculation 1.**

Arithmetic slips are *easier* to notice and report than incommensurable comparisons — a wrong sum is checkable by anyone, a wrong normalisation is not. Self-selection should therefore inflate `calculation` relative to the other two. It is last by a factor of forty. The ordering is likely real even if the magnitudes are not.

That ordering maps onto this system with unusual precision. Nothing here asks a model to compute; everything here asks a model to decide what a mathematical object *is* and whether two of them are the same. The repo already defends the conceptual half hard — `bridge-finder`'s vocabulary-versus-structure failure mode, `skeptic` step 1's requirement to write down both definitions, invariant 8's refusal to use embeddings for structural identity.

The units half was undefended, and this pipeline *manufactures* the conditions for it: transfer proposals are built on cross-field comparison, and two fields comparing "the same" quantity under different normalisations is the entire premise. The fix is one mandatory field in the probe's pre-registration — what each quantity is measured in, how normalised, over what range, and an explicit claim that the two sides are commensurable — plus `not-probeable / incommensurable` as a legitimate verdict so the agent is not forced to invent a scaling to make the comparison run.

Second-order, from the same table: `contradiction` at 22 is third-highest. The spec/pitch split produces two documents about one thing written by one agent, which is a free consistency surface nothing was checking. `verify_proposals.py` now owns that pass.

---

## 4. The methodology, applied to the human side

This is where the paper earns its place, and it is the part that costs you time rather than tokens.

The repo's Week 8–9 calibration reads: *"run referees but ignore their verdicts: read the proposals yourself, score them on the same three axes, and compare."* Sun et al. do the same activity with a protocol: defined unit of analysis, blind coding, held-back validation set, a reliability statistic, a published threshold, and a specified response when the threshold is missed. The repo has none of the five. It also happens **once**, which means the calibration can never be observed to move.

You are one person, so inter-coder reliability is unavailable. The substitute is **temporal**: re-code your own past judgments, blind, weeks later, and measure agreement with yourself. `recode.py` does this over four judgment sources — triage labels, card evaluations, referee self-scores, promoted-proposal verdicts.

It measures something inter-coder reliability cannot, and it is the thing this system most needs:

> A gate calibrated against a standard is fine until the standard moves. Then it is not broken — it is answering last quarter's question correctly, and every check in `review_audit.py` reports it as healthy.

Two statistics, and the pairing is the point. **Holsti** to match the paper's 0.70–0.80 threshold. **Cohen's kappa** beside it, because if you judged everything "4" then two passes agree perfectly and the agreement means nothing: Holsti says 1.00, kappa says 0.00, and that gap is the same failure `review_audit.py` already flags when 60% of referee scores land on one value — pointed at you instead of the referees. Weighted kappa for the ordinal scales, since 4-vs-5 and 1-vs-5 are not the same disagreement.

And the response to a low score is theirs, not an invention: **below 0.70, stop and read the disagreements before adjusting anything downstream.** They hit 68% and re-coded rather than proceeding. A systematic shift in one direction is drift, and the charters and rubrics predate it. Scatter in both directions is noise, and the category boundary is the problem — which is a rubric-anchor finding, not a personal one.

Third use, and the one that closes a loop opened by the previous round of work: **falling intra-rater agreement over months is the deskilling signal from `HYBRID-SYSTEM-REVIEW.md` §3.3, made numerical.** That argument previously ended at "nothing would show this." Now something does.

Cost: 30–40 minutes a quarter. The most expensive thing this repo asks of you, and the only instrument pointed at the human rather than the machine.

---

## 5. The two papers disagree, usefully

Clark says the risk is treating AI as mind-*replacing* when it is mind-*extending*, and prescribes tighter coupling: more channels in, more of your live state reaching the machine, more of its output shaping your thinking.

Sun et al. document what flows through those channels when it fails: fabricated citations, invented proofs, flattery, illusions of confidence. Their prescription is closer to *audit everything before you incorporate it*.

Both are right and the tension is productive, because each names the failure the other's prescription creates:

- Clark's `focus.md` — a live-state channel — is Sun et al.'s **`falling-into-traps`** if it states a conclusion rather than an obstruction. The agents will reason inside the frame you hand them. This is why the template asks what you are *stuck on*, not what you think.
- Clark's user-verdict loop — closing the coupling — is Sun et al.'s **`flattery`**: *"content that caters to the wishes and expectations of the audience,"* now with a training signal. Both agent prompts forbid optimising against it. A prompt is not enforcement, so `coalition_audit.py` §5 measures the share of bridges built on objects you have already pursued.
- And running the other way: Clark's answer to the audit burden is that the metacognitive skill — "knowing what to rely upon and when" — is the thing to cultivate. `recode.py` is the only instrument here that measures whether you still have it.

Clark also supplies the frame that keeps `verify_citations.py` from feeling like bureaucracy. His formulation is that we should treat a generated suggestion "as a thought that suddenly occurs to us during a conversation" — provisionally ours, and then checked before endorsement. Citation resolution is that check, mechanised, at the one point in the pipeline where an unchecked thought is indistinguishable from evidence.

---

## 6. What was built

| | Change | Files |
|---|---|---|
| Citation gate | Resolve every arXiv ID and DOI; non-resolving invalidates the artifact. Weekly relevance sampling for the half that cannot be automated. | `ingest/verify_citations.py`, `skeptic.md`, `referee-novelty.md`, `project-architect.md`, `weekly-synthesis` §3, §5 |
| `theory_gap` discipline | Cite the frontier or write the gap as a question. | `math-scout.md`, invariant 18 |
| Error vocabulary | 14 adapted types, each mapped to where it appears and what catches it. Counted monthly. | `rubrics/ERROR-TYPES.md`, `review_audit.py --errors`, agent output schemas |
| Units in pre-registration | Commensurability stated before the code. `not-probeable / incommensurable` as a valid verdict. | `numerical-probe.md` |
| Contradiction pass | Spec against pitch, v2 against v1. | `project-architect.md`, `verify_proposals.py` spec |
| Flattery metric | Convergence of bridges on your previously-pursued objects. | `coalition_audit.py` §5 |
| Intra-rater reliability | Blind re-coding, Holsti + kappa, 0.70 threshold, trend over quarters. | `ingest/recode.py` |

**Standing cost to you: +3 min/week** (citation relevance sample) **and +35 min/quarter** (re-coding). Token cost is negligible; the citation APIs are free and the audits are arithmetic.

**Still owed.** `verify_proposals.py` must gain the spec/pitch consistency pass — it was already on the unwritten list and now carries a requirement. `MAILTO` needs setting in `verify_citations.py`, making four scripts that refuse to run without it. And `recode.py`'s `triage` and `cards` sources read `eval/labels.jsonl` and `eval/card_labels.jsonl`; the first exists from Week 1, the second waits on `card_eval.py`.

**When to start.** The citation gate from the first week the skeptic runs — Week 6, and it is a hard gate from day one, not a warning period, because the errors it catches are unrecoverable. `recode.py` from the first quarter that has 10+ judgments older than six weeks, which is Week 1's triage labels re-coded around Week 8 — usefully, right as the referee calibration begins, so you find out whether your standard held before you write anchors from it.
