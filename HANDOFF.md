# Handoff

Everything designed so far, what state it is in, what you owe it before it runs, and what to do first.

Written to be read by you and by a fresh agent. `CLAUDE.md` is the short version that loads automatically each session.

---

## 1. Setup, before anything else

```bash
mv claude-config .claude          # the tool that generated this could not write a dotted path
```

Move `research-network-architecture.md` into this folder if it is not already here — it is the design record and the cost model, and it belongs with the code.

```bash
pip install pyyaml jsonschema numpy scipy networkx scikit-learn sentence-transformers
mkdir -p kb/{stats,probability,compbio_methods,compbio_mechanism,math}/cards ledger proposals reviews probes \
         digests logs data canon eval/runs
touch ledger/bridges.jsonl ledger/rejection_patterns.md kb/concordance.jsonl
git init && git add -A && git commit -m "scaffold"
```

**Put your email in three files** — `ingest/arxiv_pull.py` (`UA`), `ingest/canon_harvest.py` (`MAILTO`), `ingest/citation_overlap.py` (`MAILTO`). Both arXiv and OpenAlex ask for a contact address and rate-limit anonymous callers harder. All three scripts refuse to run until you do.

**Do not add the cron entries yet.** They belong at Week 2.

---

## 2. Where things stand

**Designed and written:** the full architecture, twelve agent definitions, three skills, four charters, three rubrics plus an anchor-authoring guide, and twelve scripts. Roughly 35 files.

**Never run.** Not one line has executed against real data. Every number in the cost model is an estimate from token arithmetic, not a measurement. Treat the first week's actuals as the real figures and expect them to differ.

**Phase:** Week 1 of a 10-week ramp. See `WEEK-1-PLAN.md`.

### Steady-state target, for orientation

~$46/month (~15M tokens). Daily ingest ~$0.91; the weekly synthesis and review run ~$4.43. About $35 with prompt caching. Roughly 170 cards/week in, ~2 vetted research proposals/week out.

### Costed but unmeasured

The estimate assumes 300 papers/day surveyed, 24 deep-read, ~9k tokens per paper, 6 proposals/week, 70% skeptic kill rate, 50% referee kill rate. **Every one of those is a guess.** The first two are checkable in Week 1; the rest not until Week 6+.

---

## 3. Decision log — why things are the way they are

The list in `CLAUDE.md` is what not to reverse. This is why. Several of these look like obvious savings, which is exactly why they need a written reason.

**Not Gas Town.** Gas Town runs ~$100/hour because 20–30 agents work concurrently on a shared codebase, needing worktrees, an orchestrator daemon, and crash-durable state. This work is read-heavy and append-only — agents never conflict — so it collapses to a sequential pipeline on cron at ~$0.06/hour. The one idea taken directly is `beads`: durable external memory instead of state held in context. Here that is the concordance and the bridge ledger.

**Three referees, not one.** Costs ~$0.59/week more. The rubric literature is consistent that a judge scoring several dimensions in one pass anchors on the first and lets it contaminate the rest — you get three numbers that are really one number wearing three hats. Novelty runs once per proposal rather than per domain, since it is a property of the literature, not a viewpoint.

**Binary gate, advisory scores.** Binary judgments from LLM judges track human agreement more reliably than five-point ones; fine scales invite distinctions the judge cannot defend. Scores are still collected — their distribution is the best drift detector available.

**Spec and pitch split.** project-architect writes both; referees see only the spec. Enthusiastic framing raises scores measurably. It also serves as a check on the architect: a project that cannot survive a neutral spec is not a project.

**Pre-registration with hash verification.** Models are extremely good at explaining results after the fact. Without a verifiable prior commitment, the probe agent is a machine that confirms whatever it is shown. `verify_prereg.py` is the only thing making the file worth writing.

**Escape hatches that cannot route to kill.** `not-probeable` and `inconclusive` both mean "no evidence," and treating either as evidence-against would quietly select for ideas that happen to be easy to simulate. If a month passes with zero `not-probeable` verdicts, the hatch is unused and probes are being manufactured to fit.

**Lagged citation overlap.** OpenAlex needs days to weeks to index a new preprint. On day one the signal is usually absent, and absence is not zero. A live prefilter would silently penalize the newest papers — the entire point of a streaming system. Running it on a 14-day lag turns it into charter-tuning material instead: a rejected paper that cites five canon works is a charter gap with a name on it.

**The wildcard quota.** A canon-anchored triage is conservative by construction, which is self-defeating for a system built to find intersections — intersections live where the canon has nothing to match. 15% of admissions are reserved for papers the canon does *not* recognize. ~$0.02/day. Track whether they participate in bridges; the expectation is they will be over-represented.

**Embeddings in triage but not in bridge-finding.** These look inconsistent and are not. In triage, "does this resemble work we trust?" *is* the question. In intersection-finding, semantic similarity surfaces precisely the vocabulary matches the skeptic exists to kill — "the same mathematical object" is a structural relation, not a similarity one. The concordance is symbolic for that reason.

**Recall over precision, 3:1.** Asymmetric errors: a false admit costs three cents and gets filtered again downstream; a false reject is unrecoverable and invisible. `eval_triage.py` reports F-beta(3) and warns when precision is being bought with recall.

**Caps in code, not prompts.** The review loop is the only cycle in an otherwise acyclic pipeline, and cycles are where token budgets die. Two rounds and $2 per bridge, both enforced by `check_round_cap.py`.

**Charters, rubrics, and ingest denied to agents.** An agent that can edit its own rubric will drift it toward agreeableness. One that can edit a validator will fix the validator rather than its card.

**Phasing with human audit at each gate.** Each gate goes live only after two weeks of you scoring the same items and comparing. A gate you do not trust is worse than no gate: it discards work silently and you never learn what you lost.

### The return path (invariants 13–16, added after the original design)

These came out of reading this architecture against Andy Clark, *Extending Minds with Generative AI*, Nat Commun 16:4627 (2025). Full argument in `HYBRID-SYSTEM-REVIEW.md`; the short version is one sentence.

**Everything in invariants 1–12 defends against a way the machine can go wrong. Nothing defended against a way the coalition could go wrong**, and those failures are slower, quieter, and not fixed by re-running anything. As originally designed this was a pipeline with a human at each end — judgment in during Week 1, proposals out at the digest — with no channel between those points in either direction. That is offloading. Four channels close it, all cheap, none reversing anything above.

**`focus.md` weights but cannot gate.** The charters are a good approximation of a standing interest and a bad approximation of a live question; without this file `bridge-finder` searches the space specified in Week 1, every Monday, forever. The hard limit — it reorders, it never restricts — is what stops the fix from becoming a worse version of the problem. A live-state channel with veto power would let one preoccupied month narrow the system permanently, and the resulting mirror would be worth less than the static version it replaced. `focus_link` on every candidate is how you check: an all-non-null week means the limit is being broken.

**`focus.md` goes to `bridge-finder` and `math-scout` only, never `project-architect`.** Applying it at two stages compounds the weighting — a proposal would have to be about this month's preoccupation to survive two independent filters for it. One application, at the earliest point where it can reorder rather than restrict.

**User verdicts, logged blind.** The system learns from its own skeptic (`rejection_patterns.md`) and learned nothing from you. Worse: after Week 9 the referee gate is never measured against your judgment again, so its credibility is frozen at its Week 9 value and decays unobserved. Two minutes per proposal fixes both. Scores are hidden until the verdict is committed for the same reason referees write their rejection before their score, and the same reason you label 150 papers before triage sees them — once you have seen a machine score you cannot unsee it. The interesting cell is not the agreement rate but the **false promotes**: things the gate rated ≥4.0 and you discarded. Each one names an axis the rubric is not measuring, which is exactly what `WRITING-ANCHORS.md` §2 asks you to collect.

**A user concordance layer, invisible to `math-scout`.** The concordance is the central data structure and flowed one way only; an identification you were sure of had nowhere to go. The non-obvious part is that `math-scout` must not know which entries are yours. An agent told an identification is user-supplied will defer to it, and deference is the wrong response — your identifications are not more reliable than its own, and a wrong one poisons every bridge built on it. It verifies planted objects on exactly the standard it applies to a curator's `named_in_paper: false`.

**Five raw abstracts in every digest.** The one that looks like padding and is not. The capacity this system offloads is *noticing a connection in raw abstracts*; that capacity is also what you draw on to maintain `charters/` and `rubrics/`, the two files everything downstream inherits. If the pipeline works you stop reading abstracts, and if you stop reading abstracts your ability to maintain the two files it depends on decays silently. Clark's GPS case is benign because wayfinding is not a prerequisite for maintaining GPS. Here it is. Nothing in `review_audit.py` would ever show this, which is why it is a standing digest section rather than a check.

**Kills in the digest, not just promotions.** Seeing only survivors is how you converge on the machine's taste without noticing — after some months there is no way to distinguish "the system finds good work" from "the system trained me to like what it finds." The kills are the only visible evidence of what the gates do.

**A second audit for the coalition.** `coalition_audit.py` measures narrowing (concordance concentration, recycling rate), coupling (bridges traceable to a planted object), wildcard return, flattery, and whether the digest is read at all. The wildcard number is the pointed one: invariant 7 has always been an unverified belief, §3 above predicts over-representation, and nothing has ever checked. Read the `--snapshot` trend, not any single month.

### Distorted output (invariants 17–19, added after 13–16)

From Sun et al. (2024), Humanit Soc Sci Commun 11:1278. Full argument in `DISTORTION-REVIEW.md`. One sentence: **everything above defends against agent output being *wrong*; nothing defended against it being *fabricated*, and a judgment gate cannot catch fabrication because fabrication arrives looking like evidence.**

**Citations are resolved, and failure invalidates rather than logs.** The two most consequential outputs here are citation-shaped — `skeptic.prior_work` kills a bridge, `referee-novelty` kills a proposal — and both kill *persuasively*, because an identifier reads as evidence to every downstream stage and to you. A fabricated one produces no visible error: the reasoning is fine, the premise is invented. The error is also asymmetric in the worst direction, by the same logic as invariant 9: a wrongly-passed bridge costs a few dollars and dies at the next gate, a bridge killed by a fabricated `already-done` is gone and nobody learns it existed. So `verify_citations.py` re-dispatches the agent rather than annotating the file — hand-patching would fix the artifact and hide the rate.

**Unreachable is not fabricated.** Exit 2 versus exit 1, and this is the same distinction invariant 5 makes between `inconclusive` and `falsified`. A rate-limited scan reading as mass invention would discard a week of good work and teach exactly the wrong lesson about the gate.

**Resolution proves existence, not relevance, and the residue is yours.** Sun et al.'s category is "apparently *irrelevant* fictitious references" — a real paper cited for a claim it does not support — which they suggest is the more common half. No script can check it. Three sampled citations a week, shown beside the claim they were attached to. That is not coverage; it is enough to see a rate, which is all that is available.

**`theory_gap` gets discipline instead of a gate, because it cannot have one.** It is the highest-value text in the system and reaches `bridge-finder` through no check at all, in exactly the shape Sun et al. call `false-proof`. The repo's own model example — "math.OC has adaptive schedules with better rates since 2024" — contains a rate, a date and an attribution, none verified. `math-scout` must now cite the paper establishing any frontier it asserts and write unciteable gaps as questions. `ERROR-TYPES.md` records this row's "what catches it" as **nothing**, on purpose: a table admitting a gap is worth more than one pretending otherwise.

**Units before code in the probe.** The one frequency in their table worth trusting, because the sampling bias runs the wrong way to explain it: measurement-unit errors 40, conceptual 14, calculation **1**. Arithmetic slips are easier to spot and report than bad normalisations, so self-selection should have inflated `calculation`; it is last by a factor of forty. This pipeline manufactures the conditions — transfer proposals *are* cross-field comparison — and `not-probeable / incommensurable` exists so the agent is never forced to invent a scaling to make a comparison run.

**A tag on every rejection.** Free text cannot be counted. Forty kills look like forty problems until tagging shows eighteen were one. The tag never replaces the sentence, and `unclassified` is legitimate — five of them means the vocabulary needs revising, not that a nearby category should be widened, which is Sun et al.'s own protocol rule.

**Intra-rater reliability, quarterly.** The expensive one. Week 8–9 calibrates the gates against your judgment once, with no statistic, no threshold, and no protocol for a bad result — and then never again. Sun et al. supply all three, plus the response: they hit 68%, below the 70–80% threshold, and re-coded rather than proceeding. You are one person, so the substitute for inter-coder reliability is temporal — re-judge your own past calls, blind, weeks later. Holsti to match their threshold, Cohen's kappa beside it because judging everything "4" gives perfect agreement and zero information, which is the same failure `review_audit.py` flags at 60% concentration. **Falling agreement over quarters is the deskilling signal from `HYBRID-SYSTEM-REVIEW.md` §3.3, made numerical** — that argument previously ended at "nothing would show this."

**The two papers pull against each other, and that is useful.** Clark prescribes tighter coupling; Sun et al. document what comes through the channel when it fails. Each names the failure the other's prescription creates: `focus.md` is a Clark channel and a Sun `falling-into-traps` risk; the verdict loop is Clark coupling and a Sun `flattery` training signal. The limits in invariants 13–15 were already the right shape; `coalition_audit.py` §5 now measures the one a prompt cannot enforce.

---

## 4. What you owe this system

No agent can do these. They encode judgment, and everything downstream inherits their mistakes.

| | What | When | Effort |
|---|---|---|---|
| 1 | **`canon/domain_map.yaml`** — split OpenAlex's single "Statistics and Probability" subfield into your two domains at topic level | Week 1 Day 1 | ~1 hr |
| 2 | **Vet 150 abstracts × 3 domains.** Write a reason on every strike — the strikes become negative exemplars and matter more than the keeps | Week 1 Day 3 | ~3 hr |
| 3 | **Rewrite the four charters.** An Opus pass over the vetted core gives you a first draft; the judgment must be yours | Week 1 Day 4 | ~2 hr |
| 4 | **Label 150 papers yourself**, before triage sees them. Once you have seen a machine score you cannot unsee it | Week 1 Day 5 | ~2 hr |
| 5 | **Rewrite the rubric anchors** from your own calibration cases | Week 8–9 | ~3 hr |
| 6 | **Fill in `focus.md`.** Half a page. Do it the same day as the charters, precisely so you feel the difference between "what this KB is for" and "what I am on this month" — they are easy to conflate on paper and behave completely differently in the pipeline | Week 1 Day 4 | ~15 min |

Items 2 and 4 are the ones that will slip. Let them — a rushed labelled set is worse than a late one, and nothing downstream starts until Week 2.

### And then, standing, forever

The four items above are setup. These three are the ones that do not end, and the system degrades from the human side if they stop. Total: about ten minutes a week.

| | What | When | Effort |
|---|---|---|---|
| A | **Log a verdict on each promoted proposal** — `python3 ingest/log_verdict.py log <id>` | weekly, ~2/wk | 4 min |
| B | **Read the five raw abstracts** in the digest. Not skim — read | weekly | 3 min |
| C | **Spot-check three citations** — `python3 ingest/verify_citations.py sample --n 3`. The script proves a paper exists; only you can tell whether it says what it was cited for | weekly | 3 min |
| D | **Rewrite `focus.md`** whenever it stops being true. The skill flags it at six weeks | ~monthly | 10 min |
| E | **Re-code 20 of your own past judgments, blind** — `python3 ingest/recode.py`. Below 0.70 agreement, stop and read the disagreements before adjusting anything downstream | quarterly | 35 min |

About ten minutes a week and half an hour a quarter. None of it is enforceable and that is the point: a system that could make you do these would not need you in it. What *is* instrumented is their absence — `coalition_audit.py` §4 reports unlogged proposals and unread digests, `log_verdict.py pending` says so every week, and `verify_citations.py report` shows an empty relevance table. Treat a month of skipped verdicts as a health-check failure rather than a busy month; the effect is identical either way.

Item E is the one that will feel least urgent and is the hardest to reconstruct if skipped. It is also the only check in the repo pointed at you: everything else asks whether the machine is working, and E asks whether the standard the machine was calibrated against is still the standard you hold. A quarter with no re-coding is not a gap in the record — the sample has to be six weeks stale to be worth judging, so a skipped quarter cannot be made up later.


For item 5, read `rubrics/WRITING-ANCHORS.md` first. The shipped anchors are structurally correct and substantively generic, which means they will produce scores clustered at 4 that measure nothing.

---

## 5. Do this next

**Days 1–4 are done. See `DAY-5-HANDOFF.md`** — it carries current state, the four decisions still open, and the Day 5 process in detail.

Two things from it that belong here because they are obligations rather than steps:

1. **The charters are still agent-written, through three passes.** Day 5 measures them, so rewriting them in your own hand comes first. `DAY-5-HANDOFF.md` §1 has the minimum viable version if time is short.
2. **`eval_triage.py sample` used to not actually stratify — fixed.** It assigned strata by index position over a random draw rather than by anything resembling similarity to the canon. Now fixed to band candidates against the canon index (`near`/`mid`/`far` → `expect_in`/`expect_out`/`borderline`) before assigning strata. See `DAY-5-HANDOFF.md` §3.2 for the original bug and the fix.
3. **Labelling is mid-flight (180 rows) and needs a one-time fixup before you trust `calibrate` again.** `papers.sqlite`'s `domain` column is null pre-triage, which was silently degrading canon-similarity scoring to the whole pooled canon instead of each paper's own domain. Fixed in code; the already-written rows need `python3 ingest/fixup_labels_stratum_domain.py` run once. See `DAY-5-HANDOFF.md` §6 for the full state and exact resume commands.

<details>
<summary>Days 1–2, for reference (complete)</summary>

```bash
python3 ingest/canon_harvest.py resolve      # -> canon/domain_map.generated.yaml
python3 ingest/canon_harvest.py harvest      # ~6000 works, free, ~30 min
python3 ingest/canon_tier.py --stats         # museum check — read before vetting
python3 ingest/canon_tier.py nominate        # emits canon/vetting-*.md
```

Outcome: 8,320 canon records across four domains (2,080 each, no gaps), vetting applied, `canon/index.npz` built.

</details>

Full schedule in `WEEK-1-PLAN.md` §5.

---

## 6. Known gaps

**`run_triage.py` does not exist and blocks Week 1 Days 6–7.** `eval_triage.py score` reads `eval/predictions.jsonl`; nothing currently writes it. You need a small runner that batches the labelled set through the triage subagent — attach the similarity band from `canon_index.py score`, dispatch in batches of 25, collect the JSON lines. Write this first when you reach Day 6; it is perhaps 60 lines.

Other unwritten scripts, in the order they become blocking:

| Script | Blocks | Notes |
|---|---|---|
| `run_triage.py` | Week 1 Day 6 | see above |
| `apply_triage.py` | Week 2 | sets `status` from triage scores. **Must write the literal string `wildcard` into `triage_reason` for quota admissions** — `coalition_audit.py` §3 has no other way to identify them, and without it invariant 7 stays an unverified belief costing $0.02/day for an unmeasured return. **Same requirement for `ambiguous`, different format** (added with the charters' Ambiguous sections, Week 1) — when triage emits `ambiguous: true`, its `reason` already starts with a bracketed tag like `[shared-sparse-estimation]` per `triage.md`; copy `reason` into `triage_reason` verbatim (don't strip the tag) so the bracket prefix survives, regardless of admit/reject status. `coalition_audit.py` §6 (`ambiguous_backlog()`) already reads for `triage_reason LIKE '[%]%'` and parses the tag — it's written and waiting, just dark until this script exists. |
| `pdf_extract.py` | Week 2 | abstract/intro/conclusion only, never full PDFs |
| `rebuild_index.py` | Week 2 | card files → `index.jsonl`. **Also needs `--merge-user-concordance`**: union `kb/concordance_user.jsonl` over `kb/concordance.jsonl` into `concordance.merged.jsonl`, user winning on conflict, base file untouched. Spec in `kb/concordance_user.spec.md`. The weekly skill stops the run if this fails rather than falling back to the base — a silent fallback disconnects the user's planted objects from `bridge-finder` and nothing would report it. ~30 lines |
| `card_eval.py` | Week 2 Day 1 of curation, before the hand-check in §4 item 2 | same shape as `eval_triage.py` — `sample`/`label`/`score`/`diff`. Scores curator extractions against your own judgment on field equivalence, not exact string match (the NERRE paper's Table 2 vs. Table 3 is why: exact-match badly undercounts correct-but-reworded extraction). Without it, "the schema will need revising" in the phasing table is a feeling, not a number. |
| `retranslate.py` | Week 9 | the anchor-validation step, `WRITING-ANCHORS.md` §3 |
| `concordance_stats.py` | Week 5 | size check; consolidate above 800 lines |
| `check_skeptic_rate.py`, `probe_guard.py` | Week 6+ | small |
| `verify_proposals.py` | Week 6+ | now carries a requirement beyond "both files exist": a **spec/pitch consistency pass**. One agent writing two documents about one thing, one of them to persuade and one deliberately not, is a structural invitation to `contradiction` — third-highest in Sun et al.'s table. Cheap Haiku pass: does the pitch assert anything the spec's `limitations` or `falsification` deny? Same check on revision v2 against v1. |

**Also set `MAILTO` in `ingest/verify_citations.py`**, making four scripts that refuse to run without a contact address. Same reason as the other three: anonymous callers are rate-limited harder, and here a 429 mid-scan would look exactly like a fabricated citation — the one confusion that gate must never make.

`recode.py` reads four judgment sources. `verdicts` and `triage` work now; `cards` waits on `card_eval.py`, and `referee` waits on the Week 8–9 calibration writing `eval/referee_calibration.jsonl` — which it should, one line per proposal per axis, or that fortnight of work stays unmeasurable forever.

**Unverified against live APIs.** `canon_harvest.py` uses OpenAlex topic and subfield filters that were confirmed to exist but not exercised. Expect to adjust the filter syntax on first run. Same for the arXiv OAI-PMH namespace handling in `arxiv_pull.py`.

**Never load-tested.** The concordance consolidation threshold (800 lines), the 8-week synthesis window, and the similarity thresholds (`NEAR=0.62`, `FAR=0.38`) are all guesses. `eval_triage.py calibrate` will suggest real values for the last two once you have 30+ labelled papers.

---

## 7. Starting a fresh session

Open this folder in Claude Code. `CLAUDE.md` loads automatically and carries the invariants.

A reasonable opening message:

> Read CLAUDE.md, HANDOFF.md, and WEEK-1-PLAN.md. I'm on Week 1 Day <N>. <what you just did>. What's next?

**One warning about fresh agents.** Several invariants in `CLAUDE.md` look like obvious optimizations — merging the three referees, making citation overlap live, dropping the wildcard quota, parallelizing the pipeline, unifying the two embedding stances. An agent without this context will propose all of them, plausibly and in good faith. §3 above is the answer to each. If an agent suggests one and does not engage with the reason, that is the tell.

Invariants 13–16 attract a second, subtler class of suggestion, and it is worth naming because it sounds like helpfulness rather than optimization:

- *"Let `focus.md` filter the candidate set — why review bridges the user isn't interested in?"* Because then the system only ever returns what you already thought of. Invariant 13.
- *"Pass `focus.md` to `project-architect` too, for consistency."* Compounds the weighting; two independent filters for the same preoccupation. §3.
- *"Show `math-scout` which concordance entries the user planted, so it doesn't waste time re-verifying them."* The verification is the entire value of the layer. Invariant 15.
- *"Have an agent log the verdicts / prefill them from the referee scores."* Then the agreement rate measures the gate against itself. Invariant 14.
- *"Drop the raw abstracts, the digest is long."* That section is the only defence against the human half degrading, and it is the section you will most want to cut in a busy month. Invariant 16.
- *"Summarise the raw abstracts so they're faster to read."* Puts an agent back between you and the text, which is the one thing the section exists to prevent.

The pattern in all six: each removes friction, and the friction is the mechanism. An agent proposing one of these is not being careless — it is optimizing the pipeline, which is the correct instinct applied to the wrong object.

Invariants 17–19 attract a third set, all of which sound like proportionality:

- *"Log non-resolving citations rather than invalidating the artifact — re-dispatching is expensive."* It costs about thirty cents. A bridge killed by a fabricated citation is unrecoverable, and hand-patching the file fixes the artifact while hiding the rate, which is the number that tells you whether the agent has a prompt problem.
- *"Treat unreachable citations as failures, it's simpler."* Then every rate-limit event reads as mass fabrication and you discard a good week. Invariant 5 already refused this trade for probes.
- *"Drop the manual relevance sampling — `scan` already checks citations."* `scan` checks existence. The paper's more common category is real papers cited for claims they do not make, and no script reaches it.
- *"Let an agent do the intra-rater re-coding."* The measurement is of you. There is nothing to automate.
- *"Skip `recode.py` this quarter, nothing has changed."* You cannot know that without running it — that is what it measures — and a skipped quarter cannot be made up, because the sample must be six weeks stale.
- *"Merge ERROR-TYPES into the rubrics, it's another file to maintain."* The rubrics say how good something is; this says what kind of wrong it was. Different questions, different readers, and merging them would put a counting vocabulary inside a scoring document.
