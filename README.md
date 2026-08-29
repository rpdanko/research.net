# research-net

A continuous multi-agent network that maintains knowledge bases in statistics, probability theory, and computational biology, sources the mathematics underneath them, proposes research at their intersections, and puts those proposals through peer review and cheap numerical falsification before they reach you.

Architecture and cost model: `research-network-architecture.md` (separate file).

---

## Install

```bash
mv claude-config .claude        # shipped under another name; the tooling that
                                # generated this could not write a dotted path
pip install pyyaml jsonschema numpy scipy networkx scikit-learn sentence-transformers
mkdir -p kb/{stats,probability,compbio_methods,compbio_mechanism,math}/cards ledger proposals reviews probes digests logs data canon eval
touch ledger/bridges.jsonl ledger/rejection_patterns.md kb/concordance.jsonl
touch ledger/user_verdicts.jsonl kb/concordance_user.jsonl eval/coalition_history.jsonl
```

Set your email in `ingest/arxiv_pull.py` (`UA`), `ingest/canon_harvest.py` (`MAILTO`), `ingest/citation_overlap.py` (`MAILTO`), and `ingest/verify_citations.py` (`MAILTO`). Both arXiv and OpenAlex ask for a contact address and rate-limit anonymous callers harder. The last one matters most: a 429 mid-scan looks exactly like a fabricated citation, and that is the one confusion the citation gate must never make.

```cron
0 6 * * *  cd ~/research-net && claude -p "/daily-ingest"     >> logs/daily.log 2>&1
0 7 * * 0  cd ~/research-net && claude -p "/weekly-synthesis" >> logs/weekly.log 2>&1
```

**Do not turn the cron on yet.** See Phasing.

---

## Agents

| Agent | Model | When | Role |
|---|---|---|---|
| `triage` | Haiku | daily | Scores abstracts against a charter. The cost governor: ~300 papers → ~24. |
| `stats-curator` | Sonnet | daily | Cards for statistics papers |
| `prob-curator` | Sonnet | daily | Cards for probability papers |
| `compbio-methods-curator` | Sonnet | daily | Cards for computational-biology *methods* papers (optimization, learning, algorithmic methodology) |
| `compbio-mechanism-curator` | Sonnet | daily | Cards for computational-biology *structure/mechanism* papers (protein structure, pathway modeling, single-cell inference); recovers *unnamed* mathematics |
| `math-scout` | Opus | weekly | Clusters objects, finds where applications lag theory, pulls math papers |
| `bridge-finder` | Sonnet | weekly | Proposes intersections from the concordance |
| `skeptic` | Sonnet | weekly | Kills ~70%. Is the shared object real? Is the connection known? |
| `project-architect` | Opus | weekly | Bridges → proposals. Emits a neutral **spec** and a separate **pitch**. |
| `referee-feasibility` | Sonnet | weekly | Can it be done? Per domain. |
| `referee-relevance` | Sonnet | weekly | Would the field care? Per domain. |
| `referee-novelty` | Sonnet | weekly | Has it been done? Once per proposal. |
| `numerical-probe` | Sonnet | weekly | Pre-registered 5-minute tests against the falsification criterion |

Skills: `daily-ingest`, `weekly-synthesis`, `review-loop`.

---

## Three design decisions worth knowing before you change anything

**Referees are split by axis, not just by domain.** A judge scoring feasibility, relevance and novelty in one pass anchors on the first and lets it bleed into the rest — you get three numbers that are really one number wearing three hats. Separate invocations cost more and measure more. Do not merge them to save tokens.

**The gate runs on binary verdicts; the 1–5 scores are advisory.** Binary judgments track human agreement more reliably than five-point scales. The scores rank survivors and reveal drift; they do not decide anything alone.

**The probe's pre-registration is verified by mtime and hash.** Models are excellent at explaining results after the fact. `verify_prereg.py` is the only thing making the pre-registration worth writing — if it fails, the verdict is discarded as `inconclusive`, never as `falsified`.

---

## The files that must be in your handwriting

Everything else here is scaffolding. These encode judgment and no agent can write them for you. All are `deny`-listed in `settings.json` — an agent that can edit its own rubric will eventually edit it toward agreeableness, and an agent that can write your verdicts can manufacture approval for its own past output.

**Set up once, then tuned slowly:**

1. **`charters/*.md`** — what each KB is *for*. Tune daily for the first fortnight by reading triage output and asking "would I have wanted this paper?" Every downstream mistake starts here.
2. **`rubrics/{feasibility,relevance,novelty}.md`** — the review anchors. They ship generic, which means they will produce scores clustered at 4 that measure nothing. **Read `rubrics/WRITING-ANCHORS.md` before replacing them** — it covers where anchors come from (BARS critical-incident collection), how to validate them (retranslation), and the failure patterns to watch for.
3. **`rubrics/ERROR-TYPES.md`** — the vocabulary for naming what went wrong, so rejections become countable. Ships usable; extend it when `unclassified` passes five.

**Written continuously — the three channels that run back into the system:**

3. **`focus.md`** — what you are working on and stuck on *this month*. Deliberately volatile, unlike a charter. It **weights** `bridge-finder`'s ranking and `math-scout`'s search order; it can never gate. Rewrite it whenever it stops being true; empty is a legitimate state.
4. **`ledger/user_verdicts.jsonl`** — two minutes per promoted proposal via `log_verdict.py`. Feeds next week's synthesis, and is the only input to the gate-agreement number. The tool hides referee scores until your verdict is committed, on purpose.
5. **`kb/concordance_user.jsonl`** — mathematical objects you have identified by hand that `math-scout` missed. Perhaps ten a year. Spec in `kb/concordance_user.spec.md`.

Items 1–2 decide what the system looks at. Items 3–5 are the only path by which anything you know or conclude gets back in. Without them this is a pipeline you stand at the end of; `HYBRID-SYSTEM-REVIEW.md` is the long argument for why that distinction is not philosophical.

---

## Phasing — do not skip this

Each gate goes live only after you have personally audited its judgment for two weeks. A gate you don't trust is worse than no gate: it discards work silently and you never learn what you lost.

| Weeks | Do |
|---|---|
| 1 | **Build the canon, derive the charters, measure the triage.** See `WEEK-1-PLAN.md` — this is the detailed version and it replaces "tune the charters by impression." ~$1.50. Write `focus.md` the same day as the charters, so you feel the difference between the two. |
| 2–3 | One curator, the domain you know best. Hand-check 20 cards with `card_eval.py` (see below) rather than eyeballing them. The card schema will need revising — find out now, with a number. |
| 4 | Remaining curators, once the schema stops moving. **Start the raw-abstract habit here**, not at Week 10 — the point at which you stop reading the stream yourself is the point the deskilling clock starts, and that is Week 4, when the curators take over all three domains. |
| 5 | `math-scout`. Let it run twice before wiring it in; its clustering is the hardest judgment here. |
| 6–7 | `bridge-finder` + `skeptic`, no architect. **Read the rejects** — they tell you whether it is finding structure or vocabulary. Then enable the architect. |
| 8–9 | Referees, **verdicts ignored**. Score the proposals yourself on the same axes and compare. This is your critical-incident collection; it is the only chance to calibrate before you start trusting scores. |
| 10+ | Probe gate — signal-recovery and negative-control only at first. Revision loop last. **Start logging verdicts the first week anything is promoted** (`log_verdict.py`) — this is the Week 8–9 calibration made permanent, and starting it late means the gate is trusted for months on a fortnight's evidence. |
| Monthly, from ~Week 6 | `coalition_audit.py --month --snapshot`. It says almost nothing useful for the first three months and then starts showing you a trend. Run it anyway from the beginning; a trend needs a baseline and you cannot backfill one. |

---

## Cost

~$47/month at steady state (~15.4M tokens): ~$0.91/day for ingest and curation, ~$4.62 for the weekly synthesis, review run and digest. About $36 with prompt caching on charters, rubrics, and schemas.

The return path — the three input channels, the two audits, and the Sonnet upgrade on the digest's proposal section — is ~$0.83/month of that. Cheapest layer in the system, and the only one that measures whether the others are working.

The dominant driver is deep reads per day; everything else is second-order. See the architecture doc for the sensitivity tables.

---

## Health checks

```bash
# weekly
python ingest/log_verdict.py pending      # what's awaiting your judgment
python ingest/verify_citations.py sample --n 3   # does the cited paper say what it was cited for?
tail -5 logs/health.jsonl                 # daily ingest health

# monthly
python ingest/review_audit.py --month     # score shape, veto rate, probes, agreement with you, error types
python ingest/coalition_audit.py --month --snapshot   # narrowing, coupling, wildcard, flattery, engagement
python ingest/verify_citations.py report --month
python ingest/concordance_stats.py        # concordance size; consolidate above 800 lines

# quarterly — the only check pointed at you rather than the machine
python ingest/recode.py sources
```

Read the **shape** of the score distributions, not the means. Warning signs the review audit prints for you:

- Novelty mean above 3 → inflation. Fix the anchors, not the prompt.
- Any axis with >60% of scores on one value → not discriminating.
- Zero vetoes in a month → the gate is not a gate.
- Zero `not-probeable` verdicts → probes are being manufactured to fit.
- Zero falsifications → check the negative controls actually destroy the structure they claim to.
- Gate scores that don't separate what you keep from what you discard → the gate runs and predicts nothing. Rewrite the anchors from the false promotes it lists; do not touch the threshold.

The coalition audit is the one with no natural alarm — every number in it can drift for months while each weekly run looks perfectly normal. Read its `--snapshot` trend, not any single month:

- Effective object count falling against total → the concordance is narrowing onto a few objects.
- Recycling rate rising past ~80% → the system is eating its own tail.
- Wildcards under-represented in bridges → either invariant 7's prediction was wrong (write that down) or wildcard papers are admitted and never carded (a bug).
- Unread digests, or unlogged proposals piling past six → the human half of the loop has stopped, and that degrades the charters before it shows up anywhere else.

And once a quarter, `recode.py` asks the question none of the others can: **is your own standard still the standard the gates were calibrated against?** Re-judge twenty of your own past calls, blind, six weeks or more after the fact.

- Holsti below 0.70 → stop and read the disagreements before adjusting anything downstream. A systematic shift in one direction is drift, and the charters and rubrics predate it.
- High Holsti with kappa under 0.4 → you agree with yourself because you give everything the same judgment. Same failure as a referee axis with 60% of scores on one value.
- Agreement falling across quarters → the deskilling signal, quantified. Check whether you are still reading the five raw abstracts; that habit is what maintains this.

A cron job that starts failing quietly is the most likely way this system dies. A human who stops reading the digest is the second, and it takes longer to notice. A human whose standard has drifted while every gate reports healthy is the third, and without `recode.py` there is nothing that would ever surface it.

---

## The canon

A three-tier base of influential papers (2000–present, ~2000/domain from OpenAlex) that grounds the charters in exemplars rather than adjectives — the same principle as the rubric anchors.

```bash
python ingest/canon_harvest.py resolve     # discover topic IDs -> canon/domain_map.yaml
python ingest/canon_harvest.py harvest     # ~6000 works, free, ~30 min
python ingest/canon_tier.py --stats        # museum check: is the canon year-skewed?
python ingest/canon_tier.py nominate       # emit vetting worksheets
python ingest/canon_tier.py apply          # after your 3 hours of vetting
python ingest/canon_index.py build         # local embeddings, zero API cost
python ingest/eval_triage.py sample --n 150
```

Tier 0 (25/domain, hand-picked) goes in the triage prompt. Tier 1 (150, abstracts vetted) derives the charters. Tier 2 (~2000, title-skimmed) drives similarity and citation overlap. Detail and rationale in `WEEK-1-PLAN.md`.

Two things there worth knowing before you build on it: **citation overlap is lagged, not live** — OpenAlex takes days to index a new preprint, and missing reference data is not zero overlap — and triage reserves a **wildcard quota** for papers the canon does *not* recognize, because a canon-anchored filter is conservative by construction and this system exists to find the unfamiliar.

## Card accuracy

`validate_card.py` only checks that a card is well-formed — required fields present, `role` not a generic presence statement. It does not check that the extraction is *correct*. `card_eval.py` does, the same way `eval_triage.py` checks triage instead of just trusting it:

```bash
python ingest/card_eval.py sample --n 20 --domain stats   # pull cards for hand-checking
python ingest/card_eval.py label                          # your judgment, per field, before you second-guess it
python ingest/card_eval.py score                           # curator vs. you
python ingest/card_eval.py diff                             # did the last schema/prompt edit actually help
```

Score on field *equivalence*, not exact string match — a curator writing "optimal transport" for a paper that says "Sinkhorn divergence" is correct, not wrong. This is the same lesson the LLM-NERRE paper's manual-scoring table teaches for materials-science extraction (exact-match badly undercounts correct-but-reworded output); it applies just as much to `mathematical_objects`.

Run this **at the start of Weeks 2–3**, before the "hand-check 20 cards" step in the phasing table — otherwise "the schema needs revising" is an impression, and impressions are what the canon and the rubric anchors both exist to replace with something you can point to.

If a field comes back weak and stays weak after a schema/prompt revision, that is the trigger to consider fine-tuning a small model on that field specifically (`mathematical_objects` is the strongest candidate — tight schema, high downstream leverage) rather than reworking the curator prompt again. Not a Week 2 decision; a thing to know is on the table if prompting plateaus.

## Not yet written

`pdf_extract.py`, `apply_triage.py`, `rebuild_index.py`, `concordance_stats.py`, `check_skeptic_rate.py`, `verify_proposals.py`, `probe_guard.py`, `retranslate.py`, `card_eval.py`. All are small; write them as you reach each phase rather than up front. `retranslate.py` matters most for the eventual rubric work — it is the anchor-validation step in `WRITING-ANCHORS.md` §3, and you need it at Week 9. `card_eval.py` is the one to write earliest of the rest: it gates Weeks 2–3, and skipping it means the first curator ships unmeasured.

Three of those carry requirements the checks depend on, and all three are easy to write without them by accident:

- **`verify_proposals.py` needs a spec/pitch consistency pass.** Not just "both files exist" — does the pitch assert anything the spec's `limitations` or `falsification` deny? One agent writing two documents about one thing, one to persuade and one deliberately not, is a structural invitation to contradiction. Same check on revision v2 against v1.


- **`rebuild_index.py` needs `--merge-user-concordance`** — union `kb/concordance_user.jsonl` over the base into `concordance.merged.jsonl`, user winning on conflict, base untouched, and no marker distinguishing the two in the merged output. ~30 lines. The weekly skill halts if it fails rather than falling back, because a silent fallback disconnects your planted objects from `bridge-finder` and nothing would say so.
- **`apply_triage.py` must write `wildcard` into `triage_reason`** for quota admissions. It is the only handle `coalition_audit.py` has on them; without it invariant 7 stays an unverified belief.
