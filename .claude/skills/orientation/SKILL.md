---
name: orientation
description: Read first in a cold session on this repo. Establishes what supersedes what among the status documents, where decisions actually get recorded, which written statements are known false, and what a session may not write. Invoke before acting on any document's to-do list.
---

# Orientation

## What this file is, and what it must never become

A router. Sixteen documents in this repo carry state or an action list, at least three define "done", and the entry point every agent reads first (`CLAUDE.md`) has been two phases stale for weeks. The cost is measured, not theoretical: `dev-notes/notes-consolidation-plan.md` records that assembling one session's pending work required a grep across five documents, and that one item found had already been applied.

So this file holds **reading order, supersession, and traps**. It holds no state.

**If you want to add a fact here, it belongs in `PROJECT-STATUS.md` instead.** A router that accumulates facts becomes the seventeenth stale document, which is the problem it exists to solve. The only content that earns permanence here is the kind that does not go stale: what supersedes what, where decisions hide, and what you are not allowed to write.

## Read in this order

1. **`PROJECT-STATUS.md` §2 and §5.** Where the project is; what is next, tiered. This is the current phase document.
2. **`TODO.md`.** The single unchecked box under `## Next step` is the next thing, with its procedure in subtasks and its reasoning beneath. The backlog is split into evaluation (`E`) and development (`D`) and ordered by gate, never by size.
3. **`CLAUDE.md` §Invariants.** Nineteen rules, each with a reason. Several look like obvious optimizations and are not. Do not reverse one without reading `HANDOFF.md` §3.
4. **`CARD-EVAL-HANDOFF.md` §1 and §6.** The current phase's actual program. Everything else in that file is reference.

Then, only for what you are touching: the domain's charter, the relevant rubric, the specific handoff. Do not read the week plans for instructions — see below.

## What supersedes what

`PROJECT-STATUS.md` > `WEEK-3-PLAN.md` > `WEEK-2-PLAN.md` > `WEEK-1-PLAN.md`. **The week plans are records, not instructions.** They are worth reading for why a decision was made and for the open items they left behind; they are not worth reading for what to do next, and `CLAUDE.md` currently points you at the oldest of them.

`TODO.md` and `PROJECT-STATUS.md` §5 overlap and **neither is a superset**. The TODO carries the next-step procedure and the gate graph; §5 carries the tiering and the "integrity floor" framing. Read both.

Three separate definitions of done exist — `PROJECT-STATUS.md` §6, `DAY-5-HANDOFF.md` §5, `WEEK-3-PLAN.md`. §6 is current. Consolidating all of this is `D9`, deliberately gated behind the first `card_eval.py score` run, because that run is expected to produce content for the consolidated files.

## Where decisions actually live

`OPEN-QUESTIONS.md` is the decision register and `CARD-EVAL-HANDOFF.md` §7 is the schema-decision register. **Neither is reliably current, because rulings land in `dev-notes/` first and are not always propagated back.**

The worked case, and it cost two sessions:

> `CARD-EVAL-HANDOFF.md` §7.1 asks whether `aliases` means synonyms or related terms, and says "`card_schema.json` does not say." The schema has said since 2026-09-01. The ruling is recorded in `dev-notes/curator-prompt-edits-pending.md` under "Context: the §7.1 ruling that item 4 implements" — *"`aliases` means synonyms. Settled 2026-09-01"* — with five corroborating files, a rejected alternative, and a caveat. The implementing prompt edit is applied. §7.1 was never touched, and its stated expectation (that the ruling would dissolve half the alias defects) is wrong in direction: five of six stand.

So, before treating any register item as open:

```bash
grep -rn "APPLIED\|DECIDED\|Settled\|CLOSED\|ANSWERED" dev-notes/ | head -40
```

and grep `dev-notes/` for the item's section number. A question presented as open may be answered, implemented, and merely unrecorded.

The reverse also holds. `dev-notes/curator-prompt-edits-pending.md` is where proposed text for `.claude/**` waits, because that tree is applied by hand. An item there without an APPLIED marker has not landed.

## Statements known to be false

Do not act on these on sight. Each is a filed task, which means each has been seen and not yet fixed.

- **`CLAUDE.md` line 5** — names `WEEK-1-PLAN.md` as the active phase. It is not. (`D1`)
- **`CLAUDE.md` line 13** — says `card_eval.py` does not exist. It is roughly a thousand lines and was last edited 2026-09-01. (`D1`)
- **`TODO.md` D2** — asserts the KB holds 30 cards and that the 28 in `CLAUDE.md` line 10 is wrong. **28 is correct.** It re-derives to probability 10, compbio_methods 9, compbio_mechanism 6, stats 3, and all four `index.jsonl` files agree. Executing D2 as written would introduce the error it was filed to remove. D2's second half stands: `CARD-EVAL-HANDOFF.md` §3 tabulates 21 sampled cards where `card_labels.jsonl` holds 20.
- **`OPEN-QUESTIONS.md` environment note** — "the Linux sandbox will not start on this machine, so anything marked **[shell]** has to run on your side." Test this rather than believing it; it has been false in at least one session. Two caveats survive even when the sandbox runs: there is no network, so anything resolving against arXiv or OpenAlex is still the user's side, and a sandbox holds a *copy*, so state-mutating runs do not transfer. Read-only diagnostics are the useful class.
- **`CARD-EVAL-HANDOFF.md` §5.3** — attributes `KL divergence → trust region` to 2608.17381. That card has no KL object. The alias is on 2506.07459, which already has its own row in the same table, so the defects span four cards and not five. `dev-notes` copied the error forward.

## Numbers: re-derive before quoting

`PROJECT-STATUS.md` §6 item 5: no document may quote a metric without naming the run it came from. The D2 case above is the same failure one layer up — a number written once, corrected once, and wrong both times, because neither pass re-derived it. `_load_cards` warns about exactly this.

So: count from the artifact, not from a document that counts it. Card counts from `kb/*/cards/*.md`. Label counts from `eval/card_labels.jsonl`. Triage figures with their run stamp from `eval/runs/`. If you are about to write a number you read somewhere, derive it first or attribute it explicitly to the document you read it in.

## What you may not write

`.claude/settings.json` is the authority; its deny list covers `charters/**`, `rubrics/**`, `ingest/**`, `focus.md`, `kb/concordance_user.jsonl`, `ledger/user_verdicts.jsonl`, and the `log_verdict.py log` subcommand specifically. Invariant 11 is the reason: an agent that can edit its own rubric edits it toward agreeableness, and one that can edit a validator fixes the validator instead of its card.

Two things the deny list does not say:

- **`.claude/**` is not writable from the assistant side in practice.** Propose the text in `dev-notes/curator-prompt-edits-pending.md` with the exact replacement block, and the user applies it by hand. Precedent: `OPEN-QUESTIONS.md` §1.8, `CARD-EVAL-HANDOFF.md` §8.
- **`eval/card_labels.jsonl` is nominally writable and is the user's handwriting** per `README.md`. See the next section.

`pip install` is also denied. If `validate_card.py` fails on a missing import, that is `README.md`'s install line and the user's step — not something to route around.

## Labelling: the rule easiest to break while being helpful

`card_eval.py import` exists as an instrumented compromise. Its own docstring states the terms: an eval scored by another instance of this model measures *agreement, not accuracy*, and shared blind spots are worst on `conceptual-math`, which `rubrics/ERROR-TYPES.md` calls "where this system's whole premise sits." The compromise is justified only because otherwise "the measurement does not happen at all on the domains where you cannot referee the mathematics unaided."

**Statistics is not one of those domains.** `TODO.md`'s next-step reasoning says the stats cards come first because "they are where you form a standard rather than inherit one." A drafted verdict is an inherited one, and `import` turns it into a press-enter default. Supplying drafts there manufactures the zero-override run that `score_run()` reports as uninterpretable. Do not draft verdicts for stats cards. Offer the checkable facts and where they sit; leave the letters.

Where drafting is warranted, use the method adopted from 2506.07459 onward: pull quotes into a numbered inventory **first**, assign verdicts only from what the quotes say, and mark anything without a quote `[prior]` rather than hunting for a near-miss. The earlier method — form the verdict, then reach back for support — produced four citations on 2606.07914 that pointed at sentences not establishing the claim, while all four conclusions survived re-check.

## The gate you are standing at

Card extraction has never been measured, so the phasing table's "once the schema stops moving" gate has not been passed. Four curators are already running past it, which `PROJECT-STATUS.md` §4.1 calls the most consequential deviation in the project. Nothing downstream should be enabled, cron stays off, and per Tier 4 the three backlogs get no model spend until the number exists.

The master gate, `README.md` line 85: *"Each gate goes live only after you have personally audited its judgment for two weeks. A gate you don't trust is worse than no gate: it discards work silently and you never learn what you lost."*

## Session-start checks

All read-only.

```bash
git log --oneline | head                                  # what the last session did
sed -n '/^## Next step/,/^## Backlog/p' TODO.md           # the one live task
ls eval/card_runs/ 2>/dev/null | tail                     # empty => score has never run
python3 -c "import pathlib,collections; c=collections.Counter(p.parts[1] for p in pathlib.Path('kb').glob('*/cards/*.md')); print(dict(c), sum(c.values()))"
grep -rn "APPLIED\|DECIDED\|Settled" dev-notes/ | head -40
```

The fourth exists because of D2. The fifth exists because of §7.1.

## Maintaining this file

It lives in `.claude/`, so changes are applied by hand.

When something here goes stale, **delete it rather than update it** — unless it is a trap. Reading order and supersession are structural and change rarely. The false-statement list is the volatile part, and each entry should name the task that will close it, so an entry can be removed when the task lands rather than surviving as folklore. An entry with no task behind it is not a trap; it is a fact, and facts belong in `PROJECT-STATUS.md`.
