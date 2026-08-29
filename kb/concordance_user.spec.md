# The user concordance layer

`kb/concordance_user.jsonl` — your handwriting. Agent-read, **agent-write-denied** (`settings.json`).

## Why it exists

The concordance is the central data structure in this system: everything downstream operates on it, and its cross-domain entries are the raw material for every bridge. It is written entirely by `math-scout` and read by everything else. Until this file existed, information flowed one way only — out of the machine, never into it. That is the definition of a tool rather than an extension.

Concretely: if you know that the object in a stats paper and the object in a compbio paper are the same structure, and `math-scout` has not clustered them, there is nowhere to put that. The knowledge dies in your head and the bridge is never proposed.

This file is where it goes.

## Schema

Identical to `kb/concordance.jsonl`, plus one required field.

```json
{"object": "Schur complement",
 "aliases": ["marginal precision", "conditional covariance block"],
 "papers": {"stats": ["2601.04412"], "compbio": ["2602.09934"]},
 "cross_domain": true,
 "theory_gap": "the GRN inference paper inverts the full precision matrix; the block identity gives it in O(k^3)",
 "planted_by": "user",
 "planted_reason": "the compbio paper never names it — it writes the update out by hand in eq. 7",
 "first_seen": "2026-08-23"}
```

`planted_by: "user"` is required and is what makes the layer measurable. `coalition_audit.py` counts how many bridges trace back to a planted object; without the marker there is no way to tell whether the channel is doing anything.

`planted_reason` is for you, six months from now, when you have forgotten why you were sure.

## How it merges

`rebuild_index.py` merges this layer over `kb/concordance.jsonl` at read time and hands agents the merged view. The merge is **union, user wins on conflict**:

- Object present in both → aliases and papers are unioned; your `theory_gap` overrides `math-scout`'s.
- Object present only here → passed through as if `math-scout` had written it.
- The base file is never modified. `math-scout` continues to write `concordance.jsonl` and cannot see the difference.

That last property is deliberate and it is the one to preserve if you rewrite the merge. `math-scout` must not be able to tell which entries came from you, because an agent that knows an identification is user-supplied will defer to it, and deference is exactly the wrong response — you want it to *check* your planted objects the same way it checks a curator's `named_in_paper: false` flag. A wrong identification here poisons every bridge built on it, and yours are not more reliable than its own.

## Discipline

**Plant structures, not interests.** The bar is the same one `bridge-finder` is held to: could you write the object down in both papers and check they are the same mathematical thing? If you are planting because a connection *feels* promising, that belongs in `focus.md` instead, which weights the search without asserting a fact.

**Do not plant to steer.** This file is not a way to make the system propose what you already want. If you find yourself planting an object because it would generate a bridge you have in mind, you have written the bridge yourself and are asking the machine to launder it — and the referee gate will not catch it, because the gate reviews proposals, not the concordance they were built from.

**Expect it to stay small.** Ten entries a year is a healthy rate. If it is growing faster, either `math-scout` is underperforming badly enough to be worth investigating on its own terms, or the bar above has slipped.

## What to watch

`coalition_audit.py` section 2 reports objects planted, bridges using one, and how many of those were promoted. Three readings:

- **Empty for three months** — either you have nothing to add, or the file is not in your way at the moment you would use it. The second is fixable; add the reminder to the digest.
- **Planted objects, zero bridges** — check `first_seen` in the base concordance. If `math-scout` found them independently a week later, the channel is redundant and that is good news. If it did not, `bridge-finder` may not be reading the merged view, which is a bug and not a finding.
- **Planted objects consistently promoted** — the coupling works. Also worth checking they survive the skeptic at the same rate as `math-scout`'s; if yours survive noticeably more often, confirm the skeptic is not being shown the `planted_by` field.
