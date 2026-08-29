# research-net as a hybrid thinking system

An evaluation against Andy Clark, *Extending Minds with Generative AI*, Nat Commun 16:4627 (2025), and six changes that follow from it.

**Status: built.** §4 describes what is now in the repo, not a proposal. The changes became invariants 13–16 in `CLAUDE.md`, Layer 7 in `research-network-architecture.md`, and a decision-log section in `HANDOFF.md` §3. Nothing in invariants 1–12 was reversed; every edit was additive. Two scripts they depend on are still unwritten — `rebuild_index.py --merge-user-concordance` and the `wildcard` marker in `apply_triage.py` — both listed in `HANDOFF.md` §6.

This document is the argument. The other files are the consequences, and they are deliberately terse about the reasoning because a fresh agent reading `CLAUDE.md` needs the rule before it needs the philosophy.

---

## 1. What the paper actually argues

Four claims, in the order they matter here.

**Extension is not offloading.** Clark's central move is that tool use does not produce a brain plus an appliance, but "delicately interwoven new wholes — brain, body, world tapestries in which what the brain does, what the body does, and what the loops via external media and apps provide are all in continuous flux, each adapting to what the rest has to offer." The test of a hybrid system is whether the coupling is *bidirectional and continuous*, not whether the tool is powerful.

**The brain's specialism is trust allocation.** On the predictive-processing account he draws on, the brain is indifferent to where work happens; what it is expert at is choosing the action sequence that best resolves uncertainty. So the human capacity that must be preserved is not any particular skill but the metacognitive one — "skills of knowing what to rely upon and when." Losing hippocampal wayfinding to GPS is a real loss only if you identify yourself with the bare brain. Losing the ability to judge when the GPS is wrong is a loss on any account.

**Generative AI cuts both ways on novelty, and the direction is architectural.** He cites Shin et al. on Go: superhuman AI increased the novelty of *human* moves, and not by imitation — it let players see past centuries of received wisdom. Against that he sets Messeri & Crockett: AI can cement tools and methods in place, "much as an agricultural monoculture improves efficiency while making the crop more vulnerable." His conclusion is that neither is intrinsic — "it is the detailed shape of each specific human-AI coalition that matters."

**The exemplar is FunSearch.** His model of AI-as-extension rather than AI-as-replacement is DeepMind's FunSearch: a prolific and unreliable generator wrapped in a component "expert at rejecting useless suggestions," re-prompting on the survivors. The wrapper, not the model, is where the epistemics live.

---

## 2. Where research-net already gets this right

The architecture anticipates more of the paper than it could have known.

**It is a FunSearch, aimed at research questions instead of programs.** bridge-finder generates ~20 candidates, skeptic kills ~70%, the referee gate kills ~50%, the probe gate kills more. Clark's exemplar is a generate-and-reject loop with the intelligence in the rejector; that is exactly the shape here, and it is the reason this design is defensible in a way that "ask Opus for research ideas" is not.

**Pre-registration is extended cognitive hygiene, mechanised.** Clark's closing demand is "a rich epistemology suited to bio-technological hybrid minds," instilled early. `verify_prereg.py` is a working instance: it targets precisely the failure he warns about — Messeri & Crockett's *illusion of understanding*, a model explaining a result after the fact and a number inviting belief. The mtime-and-hash check is the difference between a hygiene practice and a hygiene aspiration.

**Denying agents write access to `charters/`, `rubrics/`, `ingest/` keeps the value function biological.** Clark's line about treating an LLM's suggestion "as a thought that suddenly occurs to us" — endorsed only after checking whether we are happy to endorse it — presupposes that the standard of endorsement is not itself machine-editable. Invariant 11 is that presupposition in code.

**The wildcard quota is an anti-monoculture device.** 15% of admissions reserved for papers the canon does not recognise is a direct hedge against the Messeri–Crockett failure, arrived at independently. Same for invariant 8 — refusing embeddings in bridge-finding because similarity is not structural identity is a refusal to let the cheap measure define the search space.

**The 10-week phasing is trust calibration.** Weeks 8–9 — run the referees, ignore their verdicts, score the same proposals yourself, compare — is the training regimen Clark says our educational systems will need to install, applied to one system by one person. It is the single most Clark-compliant thing in the repo.

---

## 3. Where it is not yet a hybrid system

The diagnosis is one-sentence: **research-net is a pipeline with a human at each end, not a loop with a human inside it.**

Judgment enters at setup (charters, rubrics, canon vetting, ~11 hours in Week 1) and results exit at the digest. Between those two points, at steady state, there is no channel by which what Robin is currently thinking can reach the machine, and no channel by which what Robin concludes about a proposal can reach it either. That is offloading in exactly the sense Clark distinguishes from extension. Five specific consequences:

**3.1 — The system has no representation of your live state.** Clark's own example of a well-shaped coalition is Digital Andy: a RAG layer whose defining virtue is that responses "are sensitive to changes in what I am currently thinking and writing." research-net's equivalent is `charters/*.md` — hand-tuned, then static for weeks. A charter is a good approximation of a standing interest and a bad approximation of a live question. bridge-finder searches the intersection space you specified last month, every Monday, forever.

**3.2 — Your verdicts are discarded.** `ledger/rejection_patterns.md` feeds the skeptic's rejections back into bridge-finder. Nothing feeds *your* rejections back into anything. After Week 9 the referee gate is never measured against your judgment again, which means the one number that says whether the gate works — agreement rate with you — stops existing at precisely the moment you start trusting it.

**3.3 — Human deskilling is unmodelled, and it is self-undermining here.** The architecture defends against machine drift with unusual care (score distributions, veto rates, `not-probeable` counts, negative-control checks). It contains no defence against the corresponding human drift, and this system has an unusually sharp version of it. The capacity being offloaded is *noticing a cross-domain connection in raw abstracts*. That capacity is also the source of the calibration required to maintain `charters/` and `rubrics/` — the two files that must be in your handwriting. If the system works, you stop reading abstracts; if you stop reading abstracts, your ability to maintain the two files it depends on decays, silently, and nothing in `review_audit.py` would show it. Clark's GPS case is benign because wayfinding is not a prerequisite for maintaining GPS. Here it is.

**3.4 — The most important interface is the cheapest component.** At steady state the digest is the entire surface between you and the system, and it is assembled by Haiku for $0.06. Clark: "it is the detailed shape of each specific human-AI coalition that matters." The shape is decided at that interface. It is currently a rounding error in the budget.

**3.5 — The concordance is agent-owned.** If you know that two objects across two of your KBs are the same structure and math-scout has not clustered them, there is nowhere to put that. The concordance is the system's central knowledge object and it flows one way only. In Clark's terms the coupling is unidirectional, which is the definition of a tool rather than an extension.

---

## 4. Six changes, as built

Ordered by leverage per unit of work. Total marginal cost **~$0.83/month**, almost all of it the Sonnet upgrade on one digest section.

| | Change | Files |
|---|---|---|
| 4.1 | Live-state channel | `focus.md`, `bridge-finder.md`, `math-scout.md`, `weekly-synthesis` §0–2 |
| 4.2 | User-verdict loop | `ingest/log_verdict.py`, `review_audit.py` §4, `project-architect.md` |
| 4.3 | Deskilling defence | `ingest/raw_sample.py`, `weekly-synthesis` §6C |
| 4.4 | User concordance layer | `kb/concordance_user.spec.md`, `math-scout.md`, `weekly-synthesis` §0 |
| 4.5 | Decision-shaped digest | `weekly-synthesis` §6A–D |
| 4.6 | Narrowing instrumentation | `ingest/coalition_audit.py` |

All three input channels are `deny`-listed in `settings.json`. One subtlety worth flagging, because denying the writes was not enough on its own: `Bash(python ingest/*.py:*)` is allowed, so an agent could have appended to the verdict file by running `log_verdict.py` itself and manufactured approval for its own past output. The `log` subcommand is denied specifically; `pending`, `show` and `context` remain open.

### 4.1 `focus.md` — a live-state channel *(highest leverage)*

Half a page, your handwriting, agent-denied for writes, rewritten whenever it stops being true: what I am working on now, what I am stuck on, what I would pay to know this month. Injected into `math-scout` and `bridge-finder` prompts alongside the charters, clearly labelled as *current* rather than *standing* interest.

This is the Digital Andy move, at a few hundred tokens per week. It converts the weekly run from "search the space I specified in Week 1" to "search that space, weighted toward the question I have this week," without touching the charters — which should stay slow-moving, because everything downstream inherits them.

*Cost: ~$0.01/week. Do this first; it is an afternoon.*

### 4.2 `ledger/user_verdicts.jsonl` — close the loop

One line per promoted proposal: `{bridge_id, read: y/n, verdict: pursued|filed|discarded, reason: "<one sentence>", date}`. Two minutes per proposal, ~2 proposals/week.

Two uses, and the second is the important one:

- Appended to bridge-finder's and project-architect's prompts the way `rejection_patterns.md` already is. The system currently learns only from its own skeptic; this is the only path by which it learns from you.
- **A permanent gate-agreement metric.** Add to `review_audit.py`: rate at which your verdict agrees with the referee gate's, monthly. This is the Week 8–9 calibration made continuous instead of one-off, and it is the honest answer to "is the gate still working." Without it, the gate's credibility is frozen at its Week 9 value and decays from there unobserved.

*Cost: ~$0.02/week.*

### 4.3 A deskilling defence: five raw abstracts in every digest

Append to each weekly digest five abstracts that triage admitted and nothing downstream used, unprocessed, unranked, no card. They are already in `papers.sqlite`; the marginal token cost is the digest's.

Purpose is not information, it is calibration maintenance. It keeps periodic unaided contact with the raw stream, which is what §3.3 says your charters and rubrics silently depend on. It doubles as a standing triage audit — you will notice a bad admit here faster than any script will.

If you find yourself skipping this section for a month, that is the signal §3.3 predicts, and it is worth treating as a health check failure rather than a preference.

*Cost: negligible.*

### 4.4 A user-writable concordance layer

`kb/concordance_user.jsonl`, same schema, agent-read, agent-write-denied, merged at read time by `rebuild_index.py`. Lets you plant an identification the machine missed.

Then instrument it: tag bridges whose shared object came from the user layer. The share of promoted proposals traceable to a planted object is the most direct available measure of whether the coupling has become bidirectional. If it stays at zero for two months, either you are not using it or the machine is finding everything you would have — both are worth knowing.

*Cost: negligible.*

### 4.5 Rebuild the digest around decisions, not around reading

Move the promoted-proposal section off Haiku. For each proposal, in this order:

1. The falsification criterion.
2. The strongest reason to reject it (the referees already wrote this — invariant: reject-first ordering).
3. Which gates it passed *narrowly* — a proposal that cleared at mean 3.51 and one that cleared at 4.6 should not look identical on the page.
4. The pitch, last.
5. **The near-misses**: what was killed this week and why, one line each.

Item 5 is the anti-monoculture measure and the reason to bother. Seeing only survivors is how you converge on the machine's taste without noticing you have done it — you lose the ability to tell "the system is finding good work" from "the system has trained me to like what it finds." Item 3 is Clark's trust-and-question applied to your own reading: a promoted proposal currently arrives with no uncertainty attached to it, which is the condition under which a number invites belief.

*Cost: ~$0.15/week to move that section to Sonnet.*

### 4.6 Instrument for narrowing

The wildcard quota exists; nothing measures whether it is working. Add to `review_audit.py --month`:

- **Concordance concentration.** Herfindahl index over `mathematical_objects` frequency, tracked monthly. Rising concentration means the KBs are converging on a shrinking set of tools.
- **Recycling rate.** Share of this month's bridges whose shared object was already in the concordance eight weeks ago. Rising means the system is eating its own tail.
- **Wildcard participation.** Share of bridges involving a wildcard-admitted paper, against the 15% admission rate. `HANDOFF.md` §3 predicts over-representation; if they are *under*-represented, the quota is a cost with no return and the reason needs finding.

These three are Messeri & Crockett operationalised, and they are the gap in the failure-mode list in `research-network-architecture.md` §6 — every failure mode there is a way the machine goes wrong, and none is a way the coalition goes wrong.

*Cost: zero, it is arithmetic over files you already have.*

---

## 5. One thing not to change

The five-minute probe cap. `research-network-architecture.md` §4 already says resist raising it, on the grounds that the value is speed of falsification rather than rigour. Clark's FunSearch example is the outside argument for the same call: FunSearch works because the rejector is *cheap enough to run on everything the generator produces*. A rejector that becomes an experiment is a rejector that stops being applied at volume, and the loop collapses back into a single expensive judgment — which is the thing this whole architecture is built to avoid.

---

## 6. Summary

| | Clark's criterion | As designed | As built |
|---|---|---|---|
| Rejector-centred, not generator-centred | FunSearch | ✅ skeptic + 3 referees + probe | unchanged |
| Machine's standards not machine-editable | endorsement presupposes a standard | ✅ invariant 11 | unchanged |
| Hygiene against post-hoc rationalisation | illusions of understanding | ✅ `verify_prereg.py` | unchanged |
| Sensitive to current thinking | Digital Andy | ❌ static charters | ✅ `focus.md`, invariant 13 |
| Bidirectional coupling | "continuous flux, each adapting" | ❌ one-way pipeline | ✅ verdicts + user concordance, invariants 14–15 |
| Preserves the human meta-skill | "knowing what to rely upon and when" | ❌ unmodelled | ✅ raw abstracts + narrow-pass flags, invariant 16 |
| Resists monoculture | agricultural monoculture | ⚠️ wildcard quota, unmeasured | ✅ `coalition_audit.py` §1, §3 |

The architecture was unusually well defended against every way the machine can go wrong and undefended against every way the *coalition* can. That asymmetry was the whole finding, and §4 is six cheap corrections.

**What is still owed.** The two unwritten scripts in `HANDOFF.md` §6 — without the merge flag, 4.4 is inert; without the wildcard marker, a third of `coalition_audit.py` prints "not measurable". And the standing obligations in `HANDOFF.md` §4: two minutes of verdicts a week, three minutes of raw abstracts, ten minutes a month on `focus.md`. None of them is enforceable, which is the point — a system that could compel them would not need a human in it. Their *absence* is instrumented instead.

**Phasing.** 4.1 and 4.2 are live from Week 1. 4.3 and 4.6 must be habits before Week 4, not Week 10: the deskilling clock starts when the curators take over all three domains and you stop reading the stream yourself, and `coalition_audit.py` needs a baseline months before its trend says anything.

**The failure this introduces.** Worth stating so it is not discovered later. Every one of these channels, pushed one step further, produces a mirror — a system that returns what you already believe, faster and better argued. `focus.md` gating instead of weighting; `project-architect` optimising against the verdict file; `math-scout` deferring to planted objects instead of checking them. The three hard limits in invariants 13–15 exist for that reason, and `HANDOFF.md` §7 lists the six plausible-sounding suggestions that would each remove one.

---

## Source

Clark, A. Extending Minds with Generative AI. *Nature Communications* **16**, 4627 (2025). https://doi.org/10.1038/s41467-025-59906-9
