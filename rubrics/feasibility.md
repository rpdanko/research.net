# Feasibility — anchors

> **STARTER ANCHORS.** Replace with your own calibration cases. See `WRITING-ANCHORS.md`.

**Axis question:** could this project actually be carried out?

**Not** whether it would succeed. A method that is easy to attempt and likely to fail is **feasible** — the numerical probe tests whether it works. Confusing these two is the most common error on this axis.

## Binary (what the gate uses)

> Would you reject this proposal on the grounds that it could not be carried out?

## Scale (advisory)

```yaml
5: Every input exists and is accessible today. The effort estimate names what
   dominates and it is measured in months, not years. Someone could start
   this week.

4: One acquisition step stands between here and starting — a data use
   agreement, a modest compute allocation, learning a specific tool. The
   route is named and routine.

3: A prerequisite is missing but obtainable: a dataset that would need
   assembling from existing sources, a collaborator with a specific
   specialism, a preliminary result the proposal itself could produce first.
   Adds six to twelve months.

2: Depends on something that does not exist and whose creation is its own
   project — a cohort not yet collected, an assay not yet developed, a
   theoretical result stated as an assumption.

1: The named dataset does not exist and no route to equivalent data is given.
   Or the effort is plainly mis-estimated by an order of magnitude and the
   proposal shows no sign of knowing it.
```

## In scope

Data existence and access. Compute, equipment, wet lab. Time, and what dominates it. Missing prerequisites. Whether it needs three specialisms rarely found together.

## Out of scope — belongs to other agents

- Will the method work? → numerical probe
- Does the field care? → relevance referee
- Has it been done? → novelty referee

## Do not

- Do not score down for ambition. Ambitious and infeasible are different.
- Do not score up for clear writing. A well-written impossible project is impossible.
- Do not search the web. If you need to search to judge feasibility, the spec under-specified its data — and that is your finding, scored accordingly.
