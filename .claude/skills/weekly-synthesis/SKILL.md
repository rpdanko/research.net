---
name: weekly-synthesis
description: Weekly pipeline. Runs math-scout, bridge-finder and the skeptic, then hands survivors to project-architect. Invokes review-loop at the end. Run from cron Sunday 07:00.
---

# Weekly synthesis

Runs after seven daily ingests. Sequential.

## 0. Preflight

```bash
python3 ingest/rebuild_index.py --verify --merge-user-concordance
python3 ingest/concordance_stats.py
python3 ingest/log_verdict.py context --weeks 12
```

Keep the third command's output in context and pass it to the agents below as text. **Do not redirect it to a file** — shell redirection is outside the `Bash(python3 ingest/*.py:*)` allow pattern and will simply fail, and the `log` subcommand is denied outright so that no agent can append approval for its own past output (see `settings.json`).

`--merge-user-concordance` writes `kb/concordance.merged.jsonl` — the base concordance with `kb/concordance_user.jsonl` unioned over it, user winning on conflict. Everything downstream reads the merged file; `math-scout` alone still writes the base. Spec in `kb/concordance_user.spec.md`. If the merge step fails, **stop the run** rather than falling back to the base file: a silent fallback means the user's planted objects stop reaching `bridge-finder` and nothing anywhere would say so.

If the concordance exceeds **800 lines**, stop the normal run and instead dispatch `math-scout` in consolidation mode: merge aliases, collapse duplicates, write nothing new. A fragmented concordance degrades every bridge silently, and one week spent consolidating is cheaper than a month of bad candidates.

Check `focus.md` exists. Empty is fine and the agents fall back to the charters. **Missing is not fine** — that means a rename or a bad path, and the failure is invisible from the output, since a run with no live-state channel looks exactly like a run where the user had nothing to say.

If `focus.md` has not been touched in **six weeks**, note it at the top of the digest. It is then describing a month that has ended and is weighting the search toward it.

## 1. math-scout

Dispatch with the week's card index across all domains, `kb/concordance.merged.jsonl`, `kb/concordance_user.jsonl` (separately, so it knows which entries it is being asked to verify), and `focus.md`.

Expected output: up to 15 new math cards, an updated **base** concordance, `theory_gap` fields filled where a gap exists, and a verification note on any user-planted object it could not confirm. **A week with zero new math cards is normal.** Do not re-dispatch to get a non-empty result.

## 2. bridge-finder

Dispatch with `kb/concordance.merged.jsonl`, the last 8 weeks of index lines, the full ledger, `ledger/rejection_patterns.md`, `focus.md`, and the user-verdict context from §0.

Expected: at most 20 candidates, ranked, deduplicated by hash against the ledger, each carrying a `focus_link` field naming the line of `focus.md` it touches or `null`.

If **every** candidate has a non-null `focus_link`, note it in the digest. The channel is meant to reorder the ranking, not to decide what gets emitted, and a clean sweep means it has become a filter — which would make this system a mirror.

## 3. skeptic

One dispatch per candidate. Expect ~70% to be killed.

```bash
python3 ingest/verify_citations.py scan
python3 ingest/check_skeptic_rate.py
```

**The citation scan is a gate, not a report.** It resolves every arXiv ID and DOI the skeptic and math-scout emitted against the live APIs. A non-resolving identifier **invalidates its artifact**: re-dispatch that agent, do not hand-patch the file. An `already-done` kill resting on a paper that does not exist removes a real bridge permanently and does so persuasively, because the identifier is what made it convincing.

Non-zero exit means something did not resolve. **Exit code 2 means unreachable, which is a network failure and not a fabrication** — retry rather than re-dispatching. Confusing those two is the one mistake this step must never make.

If the pass rate is above 40% or below 10% over the trailing month, note it in the digest — the first means the skeptic has drifted agreeable, the second means bridge-finder is broken. Neither is fixed by re-running.

## 4. project-architect

Dispatch with the surviving bridges, capped at **6**, plus the user-verdict context from §0. **Do not pass `focus.md`** — `bridge-finder` has already applied it, and applying it twice would require a proposal to be about this month's preoccupation to survive two independent filters. Produces `proposals/<id>/spec.md` and `proposals/<id>/pitch.md` for each.

Verify both files exist for every proposal before continuing:

```bash
python3 ingest/verify_proposals.py
```

A missing spec means the referees would get nothing; a missing pitch means the architect wrote advocacy into the spec. Both are blocking.

## 5. Hand off to the review loop

Invoke the `review-loop` skill. It owns both gates, the aggregation, and the round cap.

When it returns, before the digest:

```bash
python3 ingest/verify_citations.py scan
```

Run again here because `referee-novelty` is the heaviest citer in the system and the one under most pressure to name a prior work — its output *is* a kill decision, and "I found nothing" feels to a model like a failure to do the job. A fabricated reference in a novelty review is the single most expensive error this pipeline can make: it is unrecoverable, it looks rigorous, and nothing downstream re-checks it.

## 6. Digest

At steady state this file is the **entire** surface between the user and this system. It is not a report of what happened; it is the interface where the whole coalition either works or does not, and it is built to be *decided on*, not read.

Two dispatches, deliberately. Section A is judgment work and goes to **Sonnet**; the rest is assembly and stays on Haiku. This is the one place in the pipeline where spending an extra $0.15/week is obviously correct — everything upstream exists to produce it.

### A — Promoted proposals *(Sonnet)*

For each, **in this order**. The order is the point: it front-loads what a decision needs and puts advocacy last, for the same reason referees see the spec and never the pitch.

1. **The falsification criterion**, verbatim from the spec. What result would end this project.
2. **The strongest reason to reject it.** The referees already wrote this — reject-first ordering means every review opens with it. Quote the best one; do not summarise it into something softer.
3. **How narrowly it passed.** Per axis: the score, and flag anything within 0.3 of the bar. A proposal that cleared at mean 3.51 and one that cleared at 4.6 must not look alike on the page. Include the probe verdict, and print `inconclusive` and `not-probeable` in full rather than collapsing them to "no result" — they mean different things and invariant 5 depends on the difference.
4. **The pitch**, last.
5. `focus_link`, if non-null — the line of `focus.md` this came from. It lets the user see when the system is answering a question they already had, which is useful and is also the thing to be suspicious of.

### B — Near-misses *(Haiku)*

Everything killed this week: skeptic kills, referee kills, probe falsifications. One line each, with the reason and the axis.

**This section is not optional and not padding.** Seeing only survivors is how you converge on the machine's taste without noticing you have done it — after a few months of promoted-only digests there is no way to distinguish "the system finds good work" from "the system has trained me to like what it finds." The kills are the only visible evidence of what the gates are actually doing, and they are the cheapest anti-monoculture measure available.

### C — Raw abstracts *(no agent)*

```bash
python3 ingest/raw_sample.py --n 5
```

Paste the output verbatim. **Do not summarise, rank, or comment on it** — an agent between the user and the text is precisely what this section exists to remove.

Alternate `--band nearmiss` roughly monthly, and `--band mixed` once the other two have been running for a month.

### D — Health *(Haiku)*

Skeptic pass rate, referee score distribution, probe verdict distribution, `not-probeable` count, concordance size, backlog, `focus.md` age, and any flags raised in §0 or §2.

Plus, when they apply:

```bash
python3 ingest/log_verdict.py pending     # every week
```

Monthly, on the first run of the month:

```bash
python3 ingest/review_audit.py --month              # agreement with you, error-type counts
python3 ingest/coalition_audit.py --month --snapshot
python3 ingest/verify_citations.py report --month
```

Quarterly, and this one is yours rather than the pipeline's:

```bash
python3 ingest/recode.py sources
```

The health block is the part to actually read every week. The proposals are the output; the health block is what tells you whether to believe them — and §C is what keeps you able to judge whether the health block is telling the truth.

## 7. After the digest — the two minutes that close the loop

Not part of the cron run. This is the user's half and nothing in the pipeline can do it.

```bash
python3 ingest/log_verdict.py log <bridge-id>
python3 ingest/verify_citations.py sample --n 3
```

One line per promoted proposal: read or not, pursued / filed / discarded, and one sentence of reason. It feeds `bridge-finder` and `project-architect` next week, and it is the only input to the gate-agreement number in `review_audit.py` §4.

The citation sample is three minutes and covers the half no script can. `scan` proves a cited paper exists; it cannot prove the paper says what it was cited for, and Sun et al. find the second failure more common than outright invention. Three a week is not coverage — it is enough to notice a rate.

`log` hides the referee scores until the verdict is committed, for the same reason as reject-first ordering: once you have seen a machine score you cannot unsee it, and an agreement rate computed from contaminated verdicts looks exactly like one that means something.

Unlogged proposals piling up past six is itself a finding — see the note `log_verdict.py pending` prints.
