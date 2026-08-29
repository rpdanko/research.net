# Relevance — anchors

> **STARTER ANCHORS.** Replace with your own calibration cases. See `WRITING-ANCHORS.md`.

**Axis question:** if this project succeeded, would *this domain* care?

Domain-specific by design. A proposal can be highly relevant to statistics and irrelevant to computational biology, and the two referees should say so. Opposite scores across domains are the routing working correctly, not a contradiction to reconcile.

## Binary (what the gate uses)

> Would you reject this proposal on the grounds that the field would not care about the answer?

## Scale (advisory)

```yaml
5: Answers a question the field is visibly working on right now. Cite the
   cards — several in the last twelve weeks address it directly.

4: Relevant to an active line of work, though not the question currently
   being asked. The field would read it.

3: Relevant to a line of work the field has largely moved on from, or to one
   it has not yet started. Note WHICH — they point opposite directions.

2: The question is unasked because the field considers it uninteresting, and
   the proposal gives no reason that judgment should change.

1: Settled. The field has an accepted answer and no live disagreement about
   it. Cite the settling result.
```

## The distinction that carries this axis

**Settled** and **unasked** both look like "nobody works on this" and mean opposite things.

- *Settled* → level 1. A real rejection.
- *Unasked because uninteresting* → level 2.
- *Unasked because the tools did not exist until now* → level 3 or higher, and possibly the entire point of the proposal.

Always record `field_status` explicitly. Collapsing these into "nobody works on it, so it does not matter" is the characteristic failure of this axis and it will systematically kill exactly the proposals this system exists to find.

## Evidence

Ground the judgment in your KB. "Four cards in the last twelve weeks address this estimation problem" is evidence. "This seems like an active area" is not. Cite card IDs in `kb_evidence`.

Search at most twice, only to check whether a subfield is currently active. Never to check novelty.

## Do not

- Do not confuse relevance with fashion. Note the distinction rather than collapsing it.
- Do not speculate about publication venue or impact.
- Do not assess general importance. The question is whether **your domain** cares.
