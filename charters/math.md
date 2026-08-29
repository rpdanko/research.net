# Mathematics — knowledge base charter

> **DRAFT.** Yours to rewrite. Unlike the other three, this KB is **pull-only** — nothing is harvested into it on a schedule.

## 1. Purpose

This KB is not a survey of mathematics and must never become one. It holds **only** the theory that the three applied KBs are demonstrably touching, pulled on demand by math-scout when it identifies a gap between what a field uses and what is known.

The discipline that keeps this useful: **every card here must trace to a specific object in the concordance that a specific applied paper uses.** A math card with no applied contact is a card that should not have been written.

## 2. Admission rule

A math paper is admitted only if math-scout can name:

1. The concordance object it bears on
2. The applied paper(s) using that object
3. What the theory has that the application lacks — a rate, a removed assumption, a general case, an algorithm

If any of the three is missing, do not write the card.

## 3. Categories searched

`math.PR`, `math.OC`, `math.FA`, `math.DG`, `math.NA`, `math.CT`, `math.AT`, `math.ST`, `math.CO`

Searched, not harvested. Targeted queries only.

## 4. Mathematical object normalization — SHARED, identical across all four charters

1. **Name at the level of theory, not notation.**
2. **Use the canonical name; variants go in `aliases`.** This KB is the **authority** for canonical naming — when the applied curators disagree, math-scout's choice wins and the others are merged into it as aliases.
3. **Record the role, not just the presence.**
4. **Include objects the result relies on.**
5. **Exclude objects merely cited.**
6. **Flag unnamed usage** with `evidence`.
7. **Three to seven objects.**

## 5. Volume ceiling

**Fifteen new cards per week, ten searches.** Hard limits.

Exceeding them means math-scout has started indexing mathematics rather than serving the applied KBs, which is a pleasant activity and a total loss. A week with zero new math cards is a normal week.

## 6. Cards are read from abstracts

Math-scout maps terrain; it does not verify proofs. Cards here record what a result claims and what it bears on, not whether it is correct. Any proposal that depends on a specific theorem needs a human to read the actual paper — note this in `limitations` on every card so it is never forgotten downstream.

## 7. The theory_gap field

This field lives only in the concordance and only math-scout writes it. It is the highest-value text in the system, and it must be a **specific, checkable claim**:

- ✗ "could benefit from more modern optimal transport"
- ✓ "compbio uses entropic regularization with fixed epsilon; math.OC has adaptive schedules with better rates since 2024"

The second can be checked and acted on. The first is an impression wearing a technical word.
