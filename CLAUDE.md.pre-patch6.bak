# research-net

A gated pipeline that maintains knowledge bases in statistics, probability, and computational biology, sources the mathematics underneath them, proposes research at their intersections, and reviews those proposals before they reach the user.

Read `PROJECT-STATUS.md` for current state and next actions. `research-network-architecture.md` has the full design and cost model. `WEEK-1-PLAN.md` is the active phase. `HYBRID-SYSTEM-REVIEW.md` is why invariants 13–16 exist and `DISTORTION-REVIEW.md` is why 17–19 do; read the relevant one before touching either group.

Phase — stated as gates passed, not as a week number, because a week number goes stale on a timer.

Ingest + triage: live and measured. recall 0.903 / precision 0.699 — eval/runs/20260827-214656, corrected for the 2509.18530 label flip.
All four curators: running, ahead of their gate. 28 cards.
Everything downstream: not enabled. math-scout has never run; bridge-finder has been run once by hand, not wired in. Cron is off, correctly.

Before enabling anything further: card extraction has never been measured — card_eval.py does not exist, so the phasing gate "the schema stops moving" has not been passed. Each gate goes live only after the user has personally audited its judgment for two weeks.

---

## Invariants

These were decided deliberately, usually against a cheaper or simpler alternative. Each has a reason recorded in `HANDOFF.md` §3. **Do not reverse one without reading that section**; several look like obvious optimizations and are not.

1. **Referees are three agents split by axis** (feasibility, relevance, novelty), never one scoring three. Merging them saves ~$0.59/week and destroys the measurement — a judge scoring multiple dimensions in one pass anchors on the first and lets it bleed into the rest.

2. **The review gate acts on binary verdicts. The 1–5 scores are advisory.** Binary judgments track human agreement more reliably. Scores rank survivors and detect drift; they decide nothing alone.

3. **Referees see the spec, never the pitch**, and are not told a proposal cleared the skeptic. Enthusiastic framing raises scores.

4. **Probes are pre-registered, and the pre-registration is verified by mtime and hash** (`verify_prereg.py`). If verification fails, the verdict is `inconclusive` — never `falsified`.

5. **`inconclusive` and `not-probeable` never route to a kill.** A proposal that resists numerical testing is not a bad proposal, and treating implementation failure as evidence would select for ideas that are easy to simulate.

6. **Citation overlap is lagged (14 days), never live.** OpenAlex takes days to index new preprints. Missing reference data is *not* zero overlap, and collapsing the two silently penalizes the newest papers.

7. **The wildcard quota stays.** 15% of daily admissions are reserved for papers the canon does *not* recognize. A canon-anchored filter is conservative by construction; this is the only channel open to unfamiliar work.

8. **Embeddings are for relevance triage only — never for bridge-finding.** Semantic similarity is the actual question in triage. In intersection-finding it surfaces exactly the "both papers mention entropy" slop the skeptic exists to kill, because similarity is not structural identity.

9. **Recall beats precision in triage, ~3:1.** A wrongly admitted paper costs three cents and is filtered downstream. A wrongly rejected paper is gone and nobody learns it existed.

10. **Revision rounds cap at 2, enforced in code** (`check_round_cap.py`), plus a $2 cumulative spend ceiling per bridge. An instruction in a prompt is not a cap.

11. **Agents cannot write `charters/`, `rubrics/`, or `ingest/`.** Denied in `settings.json`. An agent that can edit its own rubric will edit it toward agreeableness; one that can edit a validator will fix the validator instead of its card.

12. **State transitions are written by scripts, not agents.** Agents produce verdicts; the ledger records them.

### Invariants 13–16: the return path

Invariants 1–12 govern the pipeline. These four govern the loop *back*, and they were added later — see `HYBRID-SYSTEM-REVIEW.md` for the argument and `HANDOFF.md` §3 for the short version. They exist because every defence in 1–12 protects against the machine going wrong and none protects against the coalition going wrong.

13. **`focus.md` weights, it never gates.** The live-state channel reorders `bridge-finder`'s ranking and `math-scout`'s search order. It cannot admit a paper the charters exclude and cannot suppress a candidate that meets the bar. A channel that could gate would let one bad week narrow the system permanently, which is the failure the static version already risks. If every candidate in a week carries a non-null `focus_link`, the channel has become a filter and the system has become a mirror.

14. **The user's verdicts flow back; nothing may write them but the user.** `ledger/user_verdicts.jsonl` is appended only by `ingest/log_verdict.py`. `log` hides referee scores until the verdict is committed — same reasoning as reject-first ordering, and as item 4 of `HANDOFF.md` §4. An agreement rate computed from contaminated verdicts is indistinguishable from one that means something.

15. **The concordance is readable by agents and writable by both sides, in separate files.** `math-scout` owns `kb/concordance.jsonl`; the user owns `kb/concordance_user.jsonl`; `rebuild_index.py` merges them into `concordance.merged.jsonl` and downstream agents read only the merge. `math-scout` must **not** be able to tell which entries came from the user — an agent that knows an identification is user-supplied defers to it, and deference is the wrong response. Verify planted objects exactly as you verify a curator's `named_in_paper: false`.

16. **The digest carries the kills, and it carries five raw abstracts.** Promoted-only digests are how you converge on the machine's taste without noticing. The raw sample (`ingest/raw_sample.py`) is not an information channel — it is the only defence against the human half of the loop degrading, and the capacity it maintains is the same one the charters and rubric anchors are written from. Do not summarise it, do not let an agent touch it, and do not drop it to save space.

### Invariants 17–19: distorted output

From Sun et al. (2024), Humanit Soc Sci Commun 11:1278 — see `DISTORTION-REVIEW.md`. Invariants 1–16 assume agent output is *wrong* in ways a judgment gate can catch. These three cover output that is **fabricated**, which a judgment gate cannot catch because fabrication arrives looking like evidence.

17. **Every citation the system emits is resolved, and a non-resolving one invalidates its artifact.** `verify_citations.py` runs after the skeptic and again after the referees. Not logged — invalidated: the agent is re-dispatched. A novelty kill resting on a paper that does not exist removes a real proposal permanently and does so persuasively. **Unreachable is not fabricated** (exit 2 vs exit 1); collapsing those two would make every network outage look like mass invention. Resolution proves existence, not relevance — the relevance half is `verify_citations.py sample`, three a week, by hand, and there is no automating it.

18. **`theory_gap` is the highest-value and least-verified text in the system, and both halves are load-bearing.** It reaches `bridge-finder` through no gate at all. `math-scout` must cite the paper establishing any frontier it asserts, and write unciteable gaps as questions rather than facts. A wrong `theory_gap` produces a real-looking bridge and a well-argued proposal whose premise no downstream referee can check.

19. **Rejections carry an error-type tag from `rubrics/ERROR-TYPES.md`.** The tag never replaces the sentence; it makes sentences countable. Without it you can see that the skeptic killed forty bridges and not that eighteen were one error. `unclassified` is a legitimate tag and more than five of them means the vocabulary needs revising — not that a nearby category should be widened to absorb them.

---

## Layout

```
charters/     what each KB is for          — user's handwriting, agent-denied
rubrics/      review anchors + guidance    — user's handwriting, agent-denied
focus.md      what the user is on THIS MONTH — user's handwriting, agent-denied
canon/        influential-paper base       — three tiers, see WEEK-1-PLAN.md
ingest/       all scripts                  — agent-denied
kb/           cards + concordance
              ├─ concordance.jsonl         — math-scout writes
              ├─ concordance_user.jsonl    — user writes, agent-denied
              └─ concordance.merged.jsonl  — generated; what agents read
ledger/       bridges.jsonl, rejection_patterns.md
              └─ user_verdicts.jsonl       — log_verdict.py only, agent-denied
eval/         labelled set, run history, coalition_history.jsonl
.claude/      agents (13 active + 2 superseded), skills (3), settings.json
```

## The three channels running back in

Everything in `Layout` above flows one way except these. If one of them is empty for months, that is the finding — not the absence of a finding.

| Channel | File | Written by | Read by |
|---|---|---|---|
| Live state | `focus.md` | you, whenever it stops being true | `bridge-finder`, `math-scout` |
| Judgment | `ledger/user_verdicts.jsonl` | `log_verdict.py`, 2 min/proposal | `bridge-finder`, `project-architect`, `review_audit.py` §4 |
| Knowledge | `kb/concordance_user.jsonl` | you, ~10 entries/year | everything, via the merge |
| Vocabulary | `rubrics/ERROR-TYPES.md` | you, when a category is missing | `skeptic`, referees, all audits |

## Three audits, three questions

| Script | Asks | Cadence |
|---|---|---|
| `review_audit.py --month` | Is the machine's judgment working? Score shape, veto rate, probe hatches, agreement with you, error-type counts. | monthly |
| `coalition_audit.py --month --snapshot` | Is the human-plus-machine system working? Narrowing, coupling, wildcard return, engagement, flattery. | monthly |
| `recode.py` | **Is your own standard still the standard the gates were calibrated against?** Blind re-coding of your past judgments; Holsti + kappa. | quarterly |

The third is the odd one and the one to protect. A referee gate calibrated in Week 9 against a standard that has since moved is not broken — it is answering last quarter's question correctly, and every check in `review_audit.py` reports it as healthy. Falling intra-rater agreement is also the deskilling signal (invariant 16) expressed as a number instead of a worry.

## Conventions

- Sequential execution. Parallelism buys nothing here and costs debuggability; the one exception is dispatching a proposal's referees concurrently, since they must be independent anyway.
- Cheap models do volume, expensive models do judgment.
- Agents read indexes and the concordance, not corpora. A paper's full text enters context once, ever.
- Every artifact is a file with a fixed schema, validated by a script.
- A card that does not validate does not exist.
- Two audits, and they answer different questions. `review_audit.py` asks whether the machine is working. `coalition_audit.py` asks whether the human-plus-machine system is working — narrowing, coupling, wildcard return, whether the digest is read. The second is the one with no natural alarm: a coalition failing degrades quietly for months while every weekly run looks normal.
