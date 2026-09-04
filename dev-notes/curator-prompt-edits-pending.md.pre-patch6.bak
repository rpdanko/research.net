# Pending edits the assistant cannot apply — apply by hand

`.claude/**` is not writable from the assistant side (invariant 11;
`OPEN-QUESTIONS.md` §1.8, `PROJECT-STATUS.md` line 183, `CARD-EVAL-HANDOFF.md`
§8), and `CLAUDE.md` is not either. Edits that belong in those files accumulate
here until applied by hand.

**Inventory verified against the live files on 2026-09-01**, not taken on trust
from the notes that raised them. Status column reflects that check.

| # | Edit | Where | Raised in | Status |
|---|---|---|---|---|
| 0 | `Edit()` twins for the six `Write()` denies | `settings.json` | WEEK-2-PLAN Step 0 | **already applied — no action** |
| 1 | `python` → `python3` | 10 files, 32 occurrences | PROJECT-STATUS 183 | **applied 2026-09-01**, verified 0 remaining |
| 2 | Record `source_version` / `source_sha256` | 4 curator prompts | OPEN-QUESTIONS §1.8 | **applied 2026-09-01** — one typo outstanding |
| 3 | Missing read-constraint | `compbio-mechanism-curator.md:16` | CARD-EVAL §5.4a | **decided: option (a)** — text ready, not applied |
| 4 | Alias example + evidence anchor | `compbio-mechanism-curator.md:39, 42` | this session §7.1, and item 3 | pending — **apply as one block** |
| 5 | Charter-over-exemplar precedence | `triage.md` | EVAL-01-FINDINGS B1 | pending |
| 6 | `compbio_methods` cap exception | `daily-ingest/SKILL.md` §3 | WEEK-2-PLAN Step 5 | pending — original draft lost with scratchpad |
| 7 | Tell curators to use `card_notes` | all four `*-curator.md` | ESCALATION-REVIEW #4 | **applied 2026-09-01**, all four verified |
| 8 | `1. Run Run` duplication | `compbio-mechanism-curator.md:16` | this session | **applied 2026-09-01** |
| 9 | Missing blank line before line 53 | `compbio-mechanism-curator.md:52–53` | this session | pending — one keystroke |
| 10 | Two false statements about current state | `CLAUDE.md` lines 5, 13 | PROJECT-STATUS Tier 0 item 4; ESCALATION-REVIEW #3 | pending — **highest value on this list** |

---

## 0. `settings.json` — already done, recorded so it stops resurfacing

WEEK-2-PLAN Step 0 flagged that every `Write()` deny was bypassable via `Edit()`.
All six now have `Edit()` counterparts at `settings.json:34–39`. Verified. The
item is closed; WEEK-2-PLAN's Step 0 text is stale.

---

## 1. `python` → `python3` — APPLIED 2026-09-01

**Done.** `grep -rc 'python ingest/' .claude/` returns nothing. The record below
is kept because `PROJECT-STATUS.md` line 183 still describes this as unswept and
should be updated to match.

**Verified still broken (before the fix):** exactly 32 occurrences across 10
files, matching `PROJECT-STATUS.md`'s table line for line.

This is the only item on the list that breaks agents that are *currently
running*. Per PROJECT-STATUS lines 176–177 the failure is doubled: a dispatched
curator following its own instructions runs a command that fails, **and**
`settings.json:19` allows only `Bash(python3 ingest/*.py:*)`, so the failing
form is not even permitted. It is not cosmetic.

```bash
cd /path/to/research-net
grep -rc 'python ingest/' .claude/          # expect 32 across 10 files
find .claude -type f \( -name '*.md' -o -name '*.json' \) \
  -exec sed -i 's|python ingest/|python3 ingest/|g' {} +
grep -rc 'python ingest/' .claude/          # expect nothing
```

Idempotent — it cannot double-apply to an already-correct `python3 ingest/`.
On macOS use `sed -i ''`.

Distribution: `weekly-synthesis/SKILL.md` 16 · `review-loop/SKILL.md` 5 ·
`stats-curator` 2 · `prob-curator` 2 · `compbio-methods-curator` 2 ·
`compbio-mechanism-curator` 1 · `math-scout` 1 · `bridge-finder` 1 ·
`project-architect` 1 · `settings.json` 1.

The `settings.json` occurrence is inside `_comment_log_verdict_subcommand`,
which describes the allow-rule as `Bash(python ingest/*.py:*)` while the rule
itself at line 19 correctly reads `python3`. Prose only, but sweep it — a
comment that misdescribes its own rule is how the next person reintroduces the
bug.

---

## 2. Record the source pin — APPLIED 2026-09-01, one typo outstanding

**Done** in all four prompts, inserted as step 2 with the following steps
correctly renumbered. `OPEN-QUESTIONS.md` §1.8's "not fixed" half can be closed.

**Outstanding — `compbio-methods-curator.md:17`:**

```diff
-2.`pdf_extract.py` prints `source_version` and `source_sha256`.
+2. `pdf_extract.py` prints `source_version` and `source_sha256`.
```

Markdown requires whitespace after the list number. Without it the line stops
being a list item and is absorbed by lazy continuation into step 1 — so the pin
instruction renders glued to the end of "**Do not request the full PDF.**",
which is exactly where a skimming curator slides past it. The other three files
have the space and are correct. Low severity, since agents consume the raw text
rather than rendered markdown, but this edit exists to stop the pin being
ignored and burying it inside another step works against that.

**Why the edit was needed:** `pdf_extract.py` resolves the version, keys the cache on it, and prints
`source_version` + `source_sha256` where the curator cannot miss them.
`card_schema.json` accepts both. `backfill_source_pins.py` retrofits the old 28.
Every piece is in place **except the line telling the curator to copy them** —
so, per §1.8, "`pdf_extract` prints the pin and every curator ignores it."

This is also the upstream fix for `CARD-EVAL-HANDOFF.md` §5.1, where stored
abstracts drift from what arXiv serves and a card was twice scored against a
version its curator never read.

**Apply to all four:** `stats-curator.md`, `prob-curator.md`,
`compbio-methods-curator.md`, `compbio-mechanism-curator.md`. Insert as a new
step between the current steps 1 and 2 in `## Procedure, per paper`
(all four have this section at line 14, with step 1 at line 16):

> 2. `pdf_extract.py` prints `source_version` and `source_sha256`. **Copy both
>    onto the card verbatim.** They pin which paper, and which bytes, the card
>    was built from; without them nobody can later tell whether arXiv changed
>    the paper underneath the card. Do not reconstruct or guess them — if the
>    extractor could not resolve a version, write `source_version: unresolved`
>    and omit `source_sha256` entirely.

Renumber the following steps. The `unresolved` fallback matches
`card_schema.json`'s pattern for `source_version`; `source_sha256` has no such
escape value and must simply be absent.

---

## 3. `compbio-mechanism-curator.md:16` — the missing read-constraint

**Status:** pending · **contains the one real judgment call on this list**

### What is missing

Line 16 currently reads, in full:

> 1. Run `python ingest/pdf_extract.py <arxiv_id> --sections abstract,intro,conclusion`.

The three siblings all carry the prohibition, and two add a fallback:

| File | Prohibition | `confidence: low` fallback |
|---|---|---|
| `prob-curator.md:16` | yes | no |
| `stats-curator.md:16` | yes | yes |
| `compbio-methods-curator.md:16` | yes | yes |
| `compbio-mechanism-curator.md:16` | **no** | **no** |

### DECIDED 2026-09-01 — option (a): prohibition + fallback

**Replace line 16 with:**

> 1. Run `python3 ingest/pdf_extract.py <arxiv_id> --sections abstract,intro,conclusion`. This is the only text you get. **Do not request the full PDF.** If a card cannot be written without the methods section, write it with `confidence: low` and note what was missing — do not escalate.

**This also requires the line 42 change in item 4** — see below. Applying the
prohibition while leaving a worked example whose `evidence` cites §2.3 would
have the prompt forbid in step 1 exactly what it demonstrates in its example,
and examples carry more force than rules.

### Why (a), and a correction to how this was framed

**The narrow window was never actually in question for this curator.** Line 3 of
its own frontmatter reads *"Reads abstract, introduction and conclusion only."*
The constraint is declared at the top of the file; only the procedure step
failed to carry it. So this is not a policy choice between two defensible
windows — it is a file that contradicts itself, resolved in the direction it
already commits to.

**Correction.** An earlier draft of this note argued the omission might be a
deliberate loosening, on the grounds that line 42's `evidence: "Section 2.3 …"`
implies a wider window and the file was internally consistent with one. That was
wrong: line 3 declares the narrow window, so line 42 contradicts the file's own
frontmatter and always has. It is a plain internal inconsistency predating both
this session and §5.4a — not evidence of intent.

**The variance is the real cost of leaving it.** Two cards from this one curator
behave oppositely. On 2608.17381 it flagged UCT `named_in_paper: false` and
missed three occurrences sitting in §3 and a figure caption — behaving exactly
as though the window were closed. On 2506.07459 its `evidence` quotes wording
matching §3.2.2 — behaving as though it were not. An undefined constraint
predicts precisely that, and unpredictable behaviour is what makes
`sections_read` unreliable, which is §5.4's problem and the reason a card you had
already judged needed revisiting.

### What this costs, and how to see it

Expect unnamed-object yield to fall. Both of §5.5's genuine wins look like they
involve methods-section material: the PMI identification is confirmed against
§3.2.2 eq (4), and query-by-committee rests on §3.1 plus equations (6) and (8).
That is the clearest evidence that the narrow window constrains this curator's
distinctive job — and it is the price of the decision, not an argument that the
decision is wrong.

The effect is measurable. `score_run()` already splits object precision by
`named_in_paper` (`named_ok/named_tot` against `unnamed_ok/unnamed_tot`), and
`card_eval.py diff` exists to answer "did the last prompt edit help." Watch the
unnamed split across the next curation batch. **If unnamed yield collapses
rather than dips, reopen this** — the fallback position is not option (b) or (c)
but moving the methods read to a checker, per §7.2's conclusion that the
full-text search "belongs to the *checker*, not the curator." `math-scout`
already holds the verification role for `named_in_paper: false` claims; whether
it has the text access to use it needs checking, since it writes its own cards
from abstracts only.

### The §5.4a test still matters, for a different reason

`python3 ingest/show_eprint.py 2506.07459 --grep "<§3.2.2 wording>"` against the
cached blob no longer gates this decision. It now answers a narrower question:
whether existing cards were built outside their declared window, and therefore
whether any already-judged card needs re-judging. Note the innocent reading
remains live — papers routinely preview methods in a numbered contributions
paragraph, and §5.1's abstract drift makes a version difference entirely
possible.

---

## 4. `compbio-mechanism-curator.md` — the worked example, lines 39 and 42

Two changes to one YAML block: the alias (this session's §7.1 ruling) and the
evidence anchor (required by item 3's decision). **Apply them together.**

Line numbers are post-item-2, which added five lines to the procedure. The block
now sits at lines 37–43.

**Status:** pending · raised 2026-09-01 · implements the §7.1 ruling below

### Why

This is the **only** curator prompt carrying a worked `mathematical_objects`
YAML block; the other three state the rule in prose. Examples are copied in a
way rules are not, so this one block has more downstream force than three
correct paragraphs.

Its aliases run in the direction the vocabulary cannot express. `math-scout.md`
lines 28–30 give three cases — **Alias** (same object), **Instance** (narrower),
**Unnamed rediscovery** (orthogonal). There is no slot for *broader*, and
`factor graph inference` is broader: it is the family of inference algorithms
over factor graphs, of which belief propagation is one member. `message passing`
leans broader too — it covers EP, variational message passing, and GNN message
passing — though usage often treats it as BP's nickname.

So the prompt demonstrates the error it forbids, in the format most likely to be
imitated.

### The replacement block — paste over lines 37–43

```yaml
mathematical_objects:
  - name: "belief propagation"
    aliases: ["message passing", "sum-product algorithm"]
    role: "inference over the pedigree graph"
    named_in_paper: false      # <- flag it
    evidence: "Intro describes iterative updates between neighbouring nodes, run to a fixed point"
```

**Line 39, the alias.** `sum-product algorithm` is a true equality: belief
propagation on a factor graph *is* the sum-product algorithm. It replaces a
genus with a synonym without making the example less realistic.

**Line 42, the evidence anchor.** The original cited `"Section 2.3"`, which
contradicts the file's own frontmatter (line 3, *"Reads abstract, introduction
and conclusion only"*) and would contradict item 3's new step 1 outright. The
replacement anchors the same identification in the introduction, where this
curator is actually permitted to read.

Worth being honest about what this costs: an intro-level anchor is a weaker
demonstration than a methods-level one, because the real cases are harder than
the example now suggests. That weakness is the decision in item 3 showing
through, and the right place to argue with it is there, not here — a prompt that
forbids reading §2.3 and then shows evidence drawn from §2.3 teaches the
opposite of its own rule.

### Insert — after the closing fence, before the "`named_in_paper: false` entries are prioritized" paragraph

> `aliases` carries **synonyms only** — other names for the *same* object. It is
> a merge instruction, not a tag: `math-scout` collapses concordance entries
> that share one. `sum-product algorithm` qualifies because BP on a factor graph
> is that algorithm; `factor graph inference` would not, being the broader
> family that contains it. Siblings, parts and uses go in `role`. Within that
> rule be generous — list every genuine variant. A false merge produces a bridge
> the `skeptic` can catch; a missed synonym produces no bridge and reaches no
> check at all.

---

## 5. `triage.md` — charter governs over a frozen exemplar

**Status:** pending · text drafted in `EVAL-01-FINDINGS.md` lines 180–183

**Why:** `canon_index.exemplars()` renders `strike_reason` straight from the
vetting worksheet, and `triage.md` says the negative block "matters more" than
the positives. Exemplars are frozen at pass-1 judgments while charters are
revisable, so **every future charter ruling that contradicts a strike reason is
silently reversed at triage time.** A1 is the known case; A4 and A6 are exposed
to the same mechanism.

**Paste into the "What the exemplars are for" section:**

> **Where an exemplar's strike reason contradicts the charter, the charter
> governs.** Exemplars are frozen at the time of vetting and predate charter
> revisions; the charter is the current specification. If you reject a paper on
> a near-miss resemblance, check that the charter still excludes it.

Note this is only the prompt half. B2 — the `strike_superseded` field in
`canon_index.py` — is ~5 lines in a file the assistant *can* write to, and the
two are complementary: this line asks the agent to notice the conflict, B2
removes the overruled judgment from the prompt entirely.

---

## 6. `daily-ingest/SKILL.md` §3 — the `compbio_methods` cap exception

**Status:** pending · **verified still missing** — line 37 carries the
unqualified rule, and the corrected file WEEK-2-PLAN wrote to the scratchpad was
lost when that folder cleared between sessions.

Line 37 currently ends:

> …Do not raise the cap to clear a backlog; a backlog that never clears means the charter is too broad and should be tightened instead.

That instruction is now wrong for one domain. WEEK-2-PLAN Step 5 decided the
ranked-queue option and deliberately left `SETS` in `arxiv_pull.py` unnarrowed,
which makes a permanent `compbio_methods` backlog the intended steady state.
As written, the skill tells the agent to read that as a charter defect.

**Append to line 37:**

> **Exception — `compbio_methods`.** A standing backlog in this domain is the
> deliberate and permanent result of the ranked-queue decision
> (`charters/compbio_methods.md` §6 and §8; `OPEN-QUESTIONS.md` §1.1). `SETS` in
> `arxiv_pull.py` is intentionally not narrowed, so more admissions than the cap
> is the expected steady state here, not a signal to tighten the charter.

---

## 7. Tell curators to use `card_notes` — UNBLOCKED 2026-09-01

The two dependencies are now applied:

- **ERROR-TYPES.md** carries `schema-inadequate` in `### Process`, as the exact
  inverse of `restrictive-filtering`, with its third column honestly reading
  "nothing" and an explicit note that it is a local addition and therefore
  carries **no source frequency** and must not be counted alongside Sun et al.'s.
- **`card_schema.json`** carries `card_notes` — an optional array of
  `{kind, note}` with `kind` in `naming` / `no-field` / `extraction`. Optional
  for the same reason as `source_version`.
- **`card_eval.py score`** tallies them, and prints the alarm on zero. That
  counter is the part ESCALATION-REVIEW did not specify and without which this
  would repeat the `theory_gap` failure — the highest-value text in the system
  and the least verified, precisely because nothing reads it.

### Apply to all four curator prompts

Append to the `## The field that matters` section, after the canonical-name rule.

> **When the card cannot hold what you found, say so in `card_notes`.** Three kinds:
>
> - `naming` — you could not name an object canonically and used the nearest available name. **This is the important one.** The card will validate clean and read as confident, and by the canonical-name rule above the bridge is then silently lost. Nothing downstream can detect it; flagging it costs you nothing.
> - `no-field` — the paper does something the schema has nowhere to record.
> - `extraction` — text you needed was not in the sections you were given.
>
> `card_notes` is about **this record**. `limitations` is about **the paper**. "No conclusion section was available" is a limit of the card and belongs here, not there — downstream, referees and `bridge-finder` read `limitations` as evidence about the work itself.
>
> Using `card_notes` is not an escalation and does not lower your `confidence`. Leaving it empty when the schema did not fit is the failure, not the success; `rubrics/ERROR-TYPES.md` calls that `schema-inadequate`.

### Two things to watch

**The `extraction` kind is deliberate duplication.** `confidence` and
`sections_read` already measure extraction shortfall, so this overlaps them. It
is included anyway because the alternative is that curators keep writing those
sentences into `limitations`, which is the leak being fixed. If the tally shows
`extraction` swamping the other two, the field is being used as a second
`confidence` and the enum should lose it.

**`score` now depends on PyYAML where it did not before,** because the counter
reads the card files rather than the label records. In practice nothing changes
— `sample` already required it, and there is no `labels.jsonl` without `sample`.

---

## 9. `compbio-mechanism-curator.md` — missing blank line at 52/53

The alias paragraph from item 4 runs straight into the pre-existing sentence
below it with no blank line, so markdown folds them into one paragraph:

```
52  check at all.
53  `named_in_paper: false` entries are prioritized by `math-scout`. Include …
```

Insert a blank line between them. Same class as item 2's missing space — an
inserted block colliding with the line that followed it.

**This is the only collision.** All four `card_notes` insertions from item 7 are
correctly separated by a blank line; checked, not assumed. The defect is item 4's
alias paragraph alone.

**Optional polish while there.** The `card_notes` text says "by the
canonical-name rule above." That rule is literally above in `stats-curator.md`
(line 33) and `compbio-methods-curator.md` (line 33), but `prob-curator.md` and
`compbio-mechanism-curator.md` incorporate it by reference from their charters
instead, so in those two "above" points at something that is not there. Either
reword to name the charter, or leave it — the referent is recoverable. Low
severity, but dangling references are how a prompt drifts from what it claims.

---

## 10. `CLAUDE.md` — two false statements in the file every agent reads first

**Status:** pending · **do this one first.** It is the cheapest item here and the
only one that misinforms every agent at boot.

`CLAUDE.md` is the entry point. Both defects are already on record —
`PROJECT-STATUS.md` Tier 0 item 4 and `ESCALATION-REVIEW.md` §6 item 3 — and
neither has been applied.

### Edit A — line 5: the phase pointer is two weeks stale

Current:

> Read `PROJECT-STATUS.md` for current state and next actions. `research-network-architecture.md` has the full design and cost model. **`WEEK-1-PLAN.md` is the active phase.** `HYBRID-SYSTEM-REVIEW.md` is why invariants 13–16 exist and `DISTORTION-REVIEW.md` is why 17–19 do; read the relevant one before touching either group.

`WEEK-3-PLAN.md` exists, and `PROJECT-STATUS.md` supersedes *it*. A fresh agent
is being pointed two phases back. Proposed:

> Read `TODO.md` for the next action and `PROJECT-STATUS.md` for current state. `OPEN-QUESTIONS.md` is the decision register — check it before re-opening a settled question. `research-network-architecture.md` has the full design and cost model. `HYBRID-SYSTEM-REVIEW.md` is why invariants 13–16 exist and `DISTORTION-REVIEW.md` is why 17–19 do; read the relevant one before touching either group. **The week plans and the handoffs are superseded records, not current state — do not take a next action from one.**

That last sentence is the part that keeps working after the next phase lands. It
inoculates against the whole class rather than fixing one instance of it.

### Edit B — line 13: says a file that exists does not exist

Current:

> Before enabling anything further: card extraction has never been measured — **`card_eval.py` does not exist**, so the phasing gate "the schema stops moving" has not been passed. Each gate goes live only after the user has personally audited its judgment for two weeks.

It exists, it is roughly a thousand lines, and it gained `import`, a `u` verdict
with reason codes, `--recheck`, a precision band and a `card_notes` counter on
2026-09-01. Proposed:

> Before enabling anything further: card extraction has never been measured. `ingest/card_eval.py` is written but has never been run — **check whether `eval/card_runs/` is empty rather than trusting this sentence**, which is exactly the kind of claim that goes stale. Until a run exists, the phasing gate "the schema stops moving" has not been passed. Each gate goes live only after the user has personally audited its judgment for two weeks.

Pointing at a checkable artifact instead of restating state is deliberate. The
original sentence was true when written and became false without anything
noticing, which is the failure `ingest/card_eval.py`'s own `_load_cards`
docstring warns about: "a number written down once and never re-derived."

### Not proposed

Lines 9–11 carry the ingest/triage figures with a run id attached
(`eval/runs/20260827-214656`). That is sourced correctly and should stay as it
is. The `Layout` block's `.claude/` line was not verified against a file count.

---

## Context: the §7.1 ruling that item 4 implements

**`aliases` means synonyms.** Settled 2026-09-01. `card_schema.json` was silent,
but five other files agree and are now joined by a schema description:

| File | Text |
|---|---|
| `math-scout.md:28` | "**Alias** — same object, different name." Its sibling case **Instance** is where narrower terms go. |
| `stats-curator.md:27` | "Use the **canonical name** where one exists, and list variants under `aliases`." |
| `compbio-methods-curator.md:27` | Same rule. |
| `charters/math.md:30` | Aliases are the merge mechanism — losers "are merged into it as aliases". |
| `weekly-synthesis/SKILL.md:22` | Consolidation = "merge aliases, collapse duplicates". |

`ingest/card_schema.json` now carries this on the `aliases` property. **That edit
is applied.**

### Consequence for CARD-EVAL-HANDOFF.md §5.3

The handoff expected this ruling to dissolve roughly half the alias defects.
It does the opposite — five of six stand:

| Card | Alias | Relation | Verdict |
|---|---|---|---|
| 2506.07459 | `GRPO → RAFT, DPO` | siblings | defect |
| 2606.07914 | `Finite mixture model → mixing matrix` | part | defect |
| 2601.03123 | `Unitary synthesis → unitary compilation` | §2 separates them | defect — **settles the §6 disagreement in the draft's favour (`p`)** |
| 2608.17381 | `KL divergence → trust region` | use | defect |
| 2407.01051 | instances-as-synonyms; PL/QG | narrower | defect (Instance exists and was unused) |
| 2410.16457 | zero aliases on 7 objects | — | under-population, a different failure — see below |

### A `related` field was considered and rejected

The four non-synonym relations above have no slot in `math-scout`'s taxonomy,
which suggested adding one: `related: [{term, relation}]` over
broader/narrower/sibling/part-of/uses.

Rejected, for three reasons:

1. **Nothing would read it.** `bridge-finder` wants identity — "two domains
   independently model the same object" (`bridge-finder.md:39`). Siblings and
   parts are noise to it. An unread field is pure cost, and this repo already
   has the cautionary case in `theory_gap`, "the least verified text in this
   system" precisely because nothing checks it.
2. **The existing fields already cover it.** `KL → trust region`,
   `mixture model → mixing matrix` and `GRPO → DPO` all describe what work the
   object does, which is `role` — and on 2606.07914 the `role` text *already
   said it correctly* while the alias contradicted it. `belief propagation →
   factor graph inference` is not data to store but a decision about canonical
   level, i.e. about `name`.
3. **It enlarges a discipline problem.** The failure was everything relational
   routing to the one relational field. A second relational field gives that
   more surface area, not less.

Nothing here is trained — the curators are prompted instances reading files at
runtime. The levers that change their behaviour are the prompt text, the worked
examples in it, and the error-type tallies fed back from `score_run`. That is
why item 4 matters and a schema field would not.

### The asymmetry worth remembering when applying the ruling

A **false merge** produces a phantom bridge, and bridges hit the `skeptic`.
A **missed merge** produces no bridge, and nothing notices — there is no gate on
an absence.

So 2410.16457's "zero aliases on all 7 objects" is plausibly the *more*
expensive defect in §5.3, not a lesser one, and a curator told "synonyms only,
strictly" may list fewer aliases and trade a caught failure for an uncaught one.
Both the schema description and item 4's insert therefore pair the strict rule
with an explicit instruction to be generous within it.

### Not established

An earlier draft of this analysis called the bad example "a plausible upstream
cause of the card drift." That does not survive the distribution: alias defects
appear across all four domains and at least three curators, and the worst single
card (2407.01051, "over-populated and corrupted") comes from `compbio_methods`,
which has the correct prose rule and no YAML example. §5.3's own "not
curator-specific" already said so. The example is worth fixing on its own
merits; it is not the explanation.

**Keep this separate from §5.4a** (item 3 above). Two defects in one prompt file
feels like confirmation and is not — that is §4's failure mode operating at file
level instead of quote level.
