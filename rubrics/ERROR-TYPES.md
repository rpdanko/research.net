# Error types

A fixed vocabulary for naming what went wrong, adapted from Sun, Sheng, Zhou & Wu, *AI hallucination: towards a comprehensive classification of distorted information in AIGC*, Humanit Soc Sci Commun 11:1278 (2024). https://doi.org/10.1057/s41599-024-03811-x

Used by: `skeptic` (rejection log), the three referees (reject reason), `card_eval.py`, `log_verdict.py`, and counted by `review_audit.py --errors`.

**Read by agents; written only by you.** Same standing as the rubrics next to it, for the same reason.

---

## Why a fixed list at all

`ledger/rejection_patterns.md` ships as free text, and free text is exactly what the source paper argues against: prose categorisation "is inherently subjective and lacks the rigor necessary for accurate classification," which is why they spent three coders and two rounds building a category list instead. The practical consequence here is narrower and worth stating plainly — **you cannot count free text.** Without a fixed vocabulary you can see that the skeptic rejected forty bridges and you cannot see that eighteen of them were the same error, which is the thing that would tell you what to fix.

A tag is not a replacement for the sentence. Every rejection still carries prose. The tag makes it countable.

## How much of the source paper to believe

The taxonomy is worth adapting. The frequency table is worth much less, and the distinction matters for how this file gets used.

Their 243 samples came from a public Typeform error tracker — user-submitted reports of ChatGPT failures. That is a sample of **what users noticed and bothered to report**, not what models get wrong. Measurement-unit errors topping the table at 40 is at least as likely to mean "unit errors are easy to spot and satisfying to report" as "unit errors are common." The paper is candid about adjacent limits — single model, single platform, 2023 vintage, categories that "may lack comprehensiveness in terms of sample categories" — but does not flag the self-selection, and it is the sharpest problem with the numbers.

So: **the categories are a checklist, the frequencies are a weak prior on where to look first.** Where a frequency is quoted below it is marked as theirs, and it should not be treated as a base rate for this pipeline. Six months of your own tagged rejections will be a better prior than their table, and producing that is most of the point of this file.

## What was dropped, and why

Their list has 31 second-level types across 8 first-level. Fourteen are kept. The rest were dropped as inapplicable to a pipeline whose agents read arXiv abstracts and emit structured files:

- **Bias/discrimination, hate news, harmful information, propaganda, clickbait, trolling, parody, manipulation, fake news, fake reviews, conspiracy theory** — these describe consumer-facing content generation. No stage here generates public-facing prose, and no stage has an audience to inflame.
- **Translation, grammar, spelling** — real, low-stakes, and caught by reading. A misspelling in a card does not propagate; a wrong `mathematical_objects` entry does.
- **Satire, metaphorical, spatial reasoning, physical reasoning, psychological/interpersonal reasoning** — these are failures at understanding human or physical situations. The material here is mathematics and method sections.
- **False health information** — no medical claims pass through.
- **Self-awareness** — the source paper itself dropped this between its coding scheme (Table 3) and its final list (Table 4).

Following the paper's own merge convention, dropped categories are recorded rather than deleted, so a future you can tell the difference between "considered and rejected" and "never thought of."

---

## The vocabulary

Fourteen types in six groups. `tag` is the literal string to write into a rejection, review or verdict.

### Fabrication — the class this pipeline is least protected against

| tag | What it is | Where it appears here | What catches it |
|---|---|---|---|
| `fabricated-citation` | A cited paper, arXiv ID, DOI or URL that does not exist, or exists and does not say what it was cited for. Their "false academic information": *"fictitious papers, apparently irrelevant fictitious references in reviews, and non-existent web links."* | `skeptic.prior_work`, `referee-novelty`, `spec.prior_art`, `math-scout.theory_gap` | `verify_citations.py`, as a hard gate. Resolution is automated; **relevance is not** — see below. |
| `false-proof` | A claim about what a theorem gives, what a rate is, or what has been proven, stated with confidence and not true. Their "false proof": *"fabricating the proof process for scientific theorems that have been proven or not yet proven."* | `math-scout.theory_gap` — by the repo's own assessment "the highest-value text in this system" | **Nothing.** Human only. See the note below. |

This group is the reason to read the paper. The pipeline's most consequential claims — *this connection is already known and here is the paper*, *the theory has better rates since 2024* — are exactly the shape the paper identifies as most likely to be fabricated and least likely to be checked, because they arrive with a citation attached and a citation reads as evidence.

`verify_citations.py` resolves every identifier against arXiv and OpenAlex, and a non-resolving citation now invalidates the artifact rather than being logged. But note what that does **not** catch: the paper's phrase is "apparently irrelevant fictitious references" — a real paper cited for a claim it does not support. Resolution proves existence, not relevance. That residue is human work and there is no way around it; the script samples three resolved citations a week for you to spot-check, which is the cheapest honest coverage available.

`false-proof` has no automated check at all and probably cannot have one. A `theory_gap` claim is a compressed literature judgment. It is the single most valuable field the system produces and the single least verified, and that combination is worth holding in mind every time one of them reads well.

### Mathematical — where this system's whole premise sits

| tag | What it is | Where | What catches it |
|---|---|---|---|
| `conceptual-math` | Misunderstanding what a mathematical object *is* — its definition, what it ranges over, which of its properties are being used. Their frequency: 14. | Curator `mathematical_objects.role`; `math-scout` alias clustering; `bridge-finder`'s shared-object claim | `skeptic` step 1; `card_eval.py`; `math-scout` verification |
| `units-and-scale` | Comparing or combining quantities that are not commensurable — different normalisations, different units, unnormalised against normalised, per-sample against total. Their frequency: **40, the highest in their table.** | `numerical-probe` scripts; any claim that one field's rate "improves on" another's | Probe pre-registration now requires a units line |
| `calculation` | Straightforward arithmetic or operational error. Their frequency: **1, the lowest.** | Anywhere | The probe runs real code, so this mostly self-corrects |

Their strongest finding for this repo is the shape of the mathematics row rather than its size: **conceptual and unit errors dominate; calculation is negligible.** Whatever the sampling bias does to the magnitudes, it does not plausibly invert that ordering — arithmetic slips are *easier* to notice and report than conceptual confusion, so if anything the bias understates the gap.

That maps directly onto what this system does. Nothing here asks a model to compute; everything here asks a model to decide what an object *is* and whether two of them are the same. The repo already defends the vocabulary-versus-structure version of this (`bridge-finder`'s failure mode, `skeptic` step 1, invariant 8). `units-and-scale` is the version it did not defend, and it is one line in the probe's pre-registration.

### Overfitting — the class my own last change made more likely

| tag | What it is | Where | What catches it |
|---|---|---|---|
| `flattery` | *"Generate false, exaggerated, or one-sided content to please or cater to the wishes and expectations of the audience."* Their frequency: 5. | Referee grade inflation; `project-architect` writing toward `user_verdicts.jsonl` | `review_audit.py` §1; `coalition_audit.py` §5 |
| `falling-into-traps` | Accepting the questioner's framing and reasoning inside it. Their frequency: 11. | A leading `focus.md`; the architect adopting a referee's framing during revision | Prompt-level only. Human. |
| `illusions-of-confidence` | *"Overconfidence and over-reliance on one's own judgments, ignoring other information and possible errors."* Their frequency: 9. | `skeptic.confidence`, referee scores, `theory_gap` | Score distributions; the `confidence` field being used at all |

The source paper names something the return path built in the previous round quietly created room for. `user_verdicts.jsonl` exists so `project-architect` learns what you actually valued. Read one way that is closing a loop; read another it is a training signal for flattery with a documented failure mode and an empirical frequency. The architect's prompt already forbids optimising against it, and `coalition_audit.py` §5 now measures the thing a prompt cannot enforce — whether proposal objects are converging on the set you have previously pursued.

`falling-into-traps` is the same argument aimed at `focus.md`. A focus file that states a conclusion rather than an obstruction is a trap, and the agents will reason inside it. This is why `focus.md`'s template asks for what you are *stuck on* rather than what you *think*.

### Logic

| tag | What it is | Where | What catches it |
|---|---|---|---|
| `contradiction` | Self-contradictory or inconsistent output. Their frequency: **22, third-highest.** | `spec.md` against `pitch.md`; revision v2 against v1; a card's `limitations` against its `contribution` | `verify_proposals.py` (spec/pitch consistency pass) |
| `causal-uncorrelation` | *"No clear causal relationship between the generated content and the associated problem or context."* | `bridge-finder.asymmetry` — a stated asymmetry that does not follow from the shared object | `skeptic` step 2 |

The spec/pitch split was built to stop enthusiasm reaching referees. It also produces two documents about one thing, written by one agent, which is a free consistency surface that nothing was checking. Given contradiction is third in their table, checking it is cheap insurance.

### Factual

| tag | What it is | Where | What catches it |
|---|---|---|---|
| `objective-fact` | Wrong date, wrong venue, wrong number, wrong attribution of a result. Their frequency: **34, second-highest.** | Card fields; `prior_art` descriptions; `theory_gap` dates | Partially `verify_citations.py`; otherwise human |
| `authors-work` | Attributing a result, method or claim to the wrong paper or author. | `skeptic.prior_work`, `spec.prior_art` | `verify_citations.py` relevance sampling |
| `common-sense` | Contrary to generally accepted knowledge in the field. | Anywhere | The domain referees, if the charters are good |

### Process

| tag | What it is | Where | What catches it |
|---|---|---|---|
| `restrictive-filtering` | *"Automatically ignores certain words or statements in the question."* An agent silently dropping a required field, constraint or step. | A bridge missing one of the four required elements; a probe without a negative control; a referee scoring before writing its reject reason | Schema validators; `verify_proposals.py`; `probe_guard.py` |

Worth its own row because it is the failure that looks like success. Every other type produces something wrong; this one produces something *absent*, and absence does not read as an error unless a validator is looking for it. Most of the repo's existing script-level checks turn out to be defences against this one type.

---

## How to use it

**On a rejection or a reject reason.** One tag, then the sentence. The tag is not the reason.

```yaml
verdict: not-same-object
error_type: conceptual-math
reasoning: |
  Both papers say "mixing time". The stats paper means the relaxation time of a
  reversible chain; the compbio paper means an empirical burn-in cutoff chosen
  by eye. Not the same object and not comparable work.
```

**When two tags fit.** Pick the earliest in the causal chain. A fabricated citation that produced a wrong novelty judgment is `fabricated-citation`, not `objective-fact`. This is the source paper's mutual-exclusion requirement, and it is what keeps counts meaningful.

**When none fits.** Write `unclassified` and the sentence. Do not stretch a tag — a forced fit is worse than a gap, because it makes the counts lie in a direction you cannot see. Review `unclassified` entries when there are more than five: either a category is missing, or the vocabulary is drifting out of date. The source paper's own protocol says the same thing in stronger terms — new categories emerging during test coding means returning to pre-coding, not widening an existing category to swallow them.

**Adding a type.** Allowed and expected. Record what it is, where it appears, and what catches it — the third column is the useful one, and a row whose third column reads "nothing" is a finding, not an omission.
