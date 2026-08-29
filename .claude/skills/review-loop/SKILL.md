---
name: review-loop
description: Runs the two proposal gates - domain referees and numerical probe - aggregates verdicts by script, and enforces the revision round cap. Invoked by weekly-synthesis.
---

# Review loop

Two gates, then a capped revision cycle. Order matters: referees first, because novelty rejection is the most common kill and the cheapest to reach — a proposal published in 2019 should never consume CPU.

## Gate 1 — Referees

### Routing

Read `ledger/bridges.jsonl` for the proposal's `domains`. Dispatch:

- `referee-feasibility` — **once per listed domain**
- `referee-relevance` — **once per listed domain**
- `referee-novelty` — **once per proposal**, not per domain

Typically 2 domains → 5 invocations. Add the `math` domain only when the bridge type is `theory-gap`. Do not route to all four domains by default; the extra reviews are mostly abstentions and you pay full price for them.

### Independence — do not optimize this away

Each referee is a **separate subagent invocation**. Never batch axes into one call and never let a referee see another's review.

This looks like an easy token saving and is not. Scoring multiple axes in one context makes the scores correlate — the model anchors on the first axis and it bleeds into the rest — so a single call returns three numbers that are really one number wearing three hats. Separate invocations cost more and measure more.

Referees receive `proposals/<id>/spec.md` only. **Never the pitch.** Never a note that the proposal cleared the skeptic.

### Aggregation — by script, never by an agent

```bash
python ingest/aggregate_reviews.py <id>
```

Rules, applied mechanically:

- Any referee answering `reject: yes` → **kill**.
- All `reject: no` and mean score ≥ **3.5** → **proceed to Gate 2**.
- All `reject: no` and mean score < 3.5 → **revise**.

Do not ask a model to weigh the reviews. The binary verdicts are the gate; the 1–5 scores are for ranking survivors and for tracking drift. This split is deliberate — binary judgments track human agreement more reliably than five-point scales, so the gate runs on the binaries and the scores stay advisory.

## Gate 2 — Numerical probe

Dispatch `numerical-probe` for each proposal that cleared Gate 1. One invocation each.

Enforce before dispatch:

```bash
python ingest/probe_guard.py <id>    # checks spec has a concrete falsification field
```

A proposal whose `falsification` is vague cannot be probed meaningfully. Send it back as `revise` with that as the objection rather than letting the probe invent a test.

After each probe:

```bash
python ingest/verify_prereg.py <id>   # confirms preregistration.md predates probe.py by mtime and hash
```

If the pre-registration was written or modified after the script, **discard the verdict** and mark `inconclusive`. This check is the whole reason the pre-registration is worth anything.

Verdict handling:

| Verdict | Action |
|---|---|
| `supported` | → `promoted` |
| `falsified` | → `killed`, reason recorded |
| `inconclusive` | → `promoted` with a flag. **Not a kill.** |
| `not-probeable` | → `promoted` with a flag |

`inconclusive` and `not-probeable` must never route to kill. A proposal that is hard to test numerically is not a bad proposal, and treating implementation failure as evidence would quietly select for ideas that are easy to simulate.

## Revision cycle

For anything marked `revise`:

```bash
python ingest/check_round_cap.py <id>
```

- `round >= 2` → **shelve**. No exceptions, no appeals, no "this one is close."
- Cumulative spend on this bridge > **$2** → shelve regardless of round.

Otherwise increment `round`, dispatch `project-architect` in revision mode with the failing reviews and the probe verdict **including its pre-registration**.

### Targeted re-review only

v2 goes back **only to the referee that flagged the failing axis**, scoring **only that axis**. Do not re-run the passing referees.

Full re-review costs as much as the original round, almost never changes the other scores, and is how this loop turns into a money fire. If the architect's revision genuinely changed the project enough to affect other axes, it is a new proposal — kill this one and let bridge-finder resurface the idea.

## Ledger states

```
proposed -> refereed -> probed -> { promoted | revising(round n) | killed | shelved | unprobeable }
```

Every transition is written by a script, not by an agent. Agents produce verdicts; the ledger records them.

## Monthly audit

Run `python ingest/review_audit.py --month`. Three numbers to look at:

1. **Referee score distribution.** Mean novelty above ~3 means inflation. Fix the anchors, not the prompt.
2. **`not-probeable` count.** Zero over a month means the escape hatch is unused and probes are being manufactured.
3. **Probe kill rate.** Zero means Gate 2 is not a gate. Check that negative controls are actually running and actually destroying the structure they claim to.
