# Protocol: using `eval/labels.jsonl` as evidence for charter revision

**Status: proposed, not in effect. Nothing has been changed in any charter under it.**

Written because the 180 hand-scored arXiv papers in `eval/labels.jsonl` are simultaneously
(a) the best evidence in the project about how you judge the population triage actually
reads, and (b) the instrument built to measure the charters. Using them for (a) degrades
(b). This file states exactly how far I'll go and what I won't do, so the trade is explicit
before any charter text moves.

Two prior commitments this has to respect:

- `WEEK-1-PLAN.md` §8 — "If the derived charter reads like a description of the 150 papers
  you vetted rather than a specification of what you want, it will admit only more of the
  same." Pass 2 of the charters did this to the canon. **This protocol exists to stop the
  same failure happening to the labels.**
- `DAY-5-HANDOFF.md` §3.3 — labels must be independent of machine scores. The mirror rule,
  which the handoff doesn't state, is that a charter fitted to the labels makes the labels
  non-independent of the charter. Same principle, opposite direction.

---

## The seven rules

### R1 — Minimum support: five papers, never one

No charter text changes on the evidence of fewer than **5 labelled papers pointing the
same way**. Below that threshold a pattern is indistinguishable from hand-scoring noise
across ~200 abstracts.

Calibration for what a real rule looks like: in `vetting-stats.md` you wrote
`Do not include psychology papers` **five times in identical words**. That is a rule.
One paper scored 4 is an observation.

### R2 — Criteria, not instances

No charter may name a paper, title, arXiv ID, or method-specific artifact drawn from the
labelled set. The charter must read the same to someone who has never seen those 180 rows.

Operational test: *if this sentence would be worded differently had one paper been drawn
differently, it is an instance and it comes out.*

This is the rule pass 2 broke against the canon, and §8 of every charter records the repair.

### R3 — Fill silences; do not move boundaries

Two operations that look similar and are not:

**Silence-filling (permitted).** The charter says nothing about an entire class of paper;
the labels contain many of them with a consistent verdict; a criterion gets written.
Low leakage, because the eval's discriminating power lives at the in/out boundary *within*
a domain — not on classes the charter never addressed at all. A charter silent on a class
scores it arbitrarily; that arbitrariness is noise in the eval, not signal being protected.

**Boundary-moving (forbidden).** The charter already has a rule, the labels show it lands
wrong on papers near the threshold, and the wording gets retuned until they land right.
This is the definition of overfitting and it is precisely what the ≥0.70 borderline-agreement
target is supposed to measure. Off the table without fresh data.

### R4 — Labels adjudicate; they do not originate

Labels may choose between candidate readings that **already existed** from the canon —
e.g. the three meta-analysis positions in `charters/stats.rewrite-prep.md` §A1, all of
which were derived before any label was consulted.

Labels may not generate a rule whose only justification is capturing labelled papers.
If the rule cannot be stated as something you believe about statistics, and only as
something true of this sample, it does not go in.

### R5 — One pass, no iteration

The single most reliable way to overfit while obeying every rule above is to loop:
write → check against labels → rewrite → check again. Each cycle fits the sample tighter
while every individual step looks defensible.

**One pass.** Aggregate patterns are extracted once, up front, in a form you can read. The
charter is then written from them and from your judgment. It is not re-scored against the
labels afterwards, and I will not run comparisons "just to see."

### R6 — Every label-derived change is marked and reversible

Any charter text originating in the labels carries a marker in that charter's §8 naming
the aggregate pattern and its **n**. Two reasons: you can see how much of your charter came
from a sample rather than from you, and when the fresh eval disagrees, the affected text
is identifiable and revertible rather than fused into the document.

### R7 — Noise budget, stated honestly

From cross-tabulating your stratum field against your score field: **179 of 180 agree**;
zero `out`-stratum papers scored ≥4. That bounds gross keying errors at roughly 1 in 180.

It does **not** bound judgment drift, because both fields were typed in the same sitting
against the same abstract. And there is a specific drift risk in the file: rows 110–180
were drawn by the fixed banded `sample()` and arrived in long same-band streaks — rows
105–133 are 24 admits out of 29, rows 134–147 are fourteen consecutive rejections. Streaks
invite anchoring against neighbours instead of against the scale.

Consequence for this protocol: **treat any pattern with n < 10 as a question, not evidence.**
R1's floor of 5 is the absolute minimum for anything; 10+ is what I'd want before proposing
text.

### R8 — The one-way door, and the file path that has to change with it

Once a charter is written against these 180 rows, **they can never serve as that charter's
eval**. This is irreversible and it needs a physical safeguard, because
`eval_triage.py score` defaults to reading `eval/labels.jsonl` and will happily produce a
confident, meaningless number.

If you adopt this protocol: rename to `eval/labels.dev.jsonl`, leave a stub or a line in
`HANDOFF.md` recording why, and let the fresh set take the canonical path. Without that,
a future session scores against its own training data and never finds out.

---

## The protocol applied to what I already found

So you can see the rules bite before agreeing to them. Nothing below has been written into
any charter.

| Finding | n | Verdict under protocol |
|---|---|---|
| Papers with analyzable mathematical structure are admitted regardless of applied wrapper — conformal prediction, Koopman operators, GD convergence guarantees, PSD sampling, quantum complexity, topological DL | 17 admits, no charter mentions any of it | **Permitted.** R3 silence-filling, clears R7's n≥10. Must be written as a criterion in your words (R2), not as a list of these 17. |
| Applied-ML systems work — benchmarks, pipelines, retrieval, agents, deployment — is rejected | ~65 rejections | **Permitted.** Same reasoning. The canon contained essentially none of this literature, so §3 of every charter is silent on the largest single class triage will meet. |
| Presence of a `math.*`/`stat.*`/`q-bio.*` cross-list predicts admission 60% vs 21% | 98 vs 82 rows | **Permitted as calibration only.** Informs the `SETS` firehose decision in `arxiv_pull.py`. Not charter text — a category is not a criterion. |
| Meta-analysis: line 128, an NMA methodology paper, scored 4, against 3 canon strikes | 1 | **Refused.** Fails R1 and R7. Stays an open question in `stats.rewrite-prep.md` §A1 for you to rule on. |
| `compbio_mechanism` boundary: line 80, cytoskeletal statistical-mechanical framework, scored 2 despite sitting in the centre of §2 | 1 | **Refused.** Re-read candidate for you, nothing more. |
| Retuning §2's causal-inference or high-dimensional bullets | — | **Refused.** R3 boundary-moving, and both already have strong independent canon support (9 and 2 starred keeps). |

Net: of six things the labels appear to say, **two become charter text, one informs a code
decision, three stay questions.**

---

## What this costs and what it buys

**Costs.** The 180 rows stop being a valid eval for whatever charters are written under
this protocol. Recovering a measurement means one more labelling sitting of 60–80 papers.

**Buys.** Charters that say something about the ~57% of the arXiv stream carrying `cs.LG`,
instead of being silent on it and letting triage improvise. Right now that silence is not
neutral — an unaddressed class gets scored on whatever the exemplars happen to suggest,
and neither of us knows what that is.

**The alternative is not free either.** Keeping the labels pristine means measuring
charters that were built entirely from a journal canon the charters themselves describe
as "weak evidence about what triage will actually see" (`stats.md` §9). A clean measurement
of a charter fitted to the wrong population is still a clean measurement of the wrong thing.

---

## Outstanding decision

Whether to adopt this at all. If yes, R8's rename happens before any charter text moves.
If no, `stats.rewrite-prep.md` stands as canon-derived only and the labels stay sealed
until `run_triage.py` exists.

I won't propose charter revisions from the labels until this is settled either way.
