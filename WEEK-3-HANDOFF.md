# Week 3 handoff

Written 2026-08-28, at the close of Week 2. Everything below is checked
against the actual repo state as of today, not carried forward from memory —
`WEEK-2-HANDOFF.md` had real errors of that kind (stale file claims, `python`
vs `python3`, a stale settings.json description) and this one tries not to
repeat them. Where something is inferred rather than confirmed, it says so.

**Environment.** The Linux sandbox does not start on the assistant side —
everything marked **[shell]** below runs on your machine; the assistant can
read/write/edit repo files directly but not execute anything. Every script
runs with `python3`, not `python`. Subagents (curators, triage, bridge-finder,
skeptic, etc.) are dispatched from your own Claude Code session in this repo,
not from the assistant's side — the working pattern this whole engagement has
used is: assistant hands you a dispatch prompt, you run it, you paste the
report back.

---

## 1. Where Week 2 actually landed

All four of `WEEK-2-PLAN.md`'s "Done means" criteria are met — see that
file's final section for the exact reasoning on each, including two that
needed a precise rather than a pattern-matched reading (`coalition_audit.py`'s
"Concordance is empty" message is expected at this stage, not a failure; the
"≥5 stats cards" criterion is short by the letter but the KB as a whole is
well past what that number was ever a proxy for).

**Knowledge base: 28 validated cards across all four domains.**

| Domain | Cards | Notes |
|---|---|---|
| `stats` | 3 | Started at 5; struck 2 as genuine charter mismatches (see §2) |
| `probability` | 10 | First cards this domain has ever had |
| `compbio_methods` | 9 | Started at 10; struck 1 (DiffGRM, applied-ML-systems) |
| `compbio_mechanism` | 6 | Second domain curated, to give bridge-finder cross-domain material |

All from the same admitted pool in `ingest/papers.sqlite` — no fresh triage
spend this session (see §5 on the untriaged backlog that's separate from
this).

**Pipeline proven end to end.** `kb/concordance.merged.jsonl` builds (3 rows,
all from `concordance_user.jsonl` — the base `concordance.jsonl` is still
empty, math-scout has never run). `bridge-finder` ran once, manually, capped
at 3: produced 2 candidates (`b-2608-001`, `b-2608-002`), both read end to
end, both killed by the skeptic on solid, specific reasoning (not agreeable
rubber-stamping — see `ledger/rejection_patterns.md`). Zero survivors from a
first run is a legitimate result, not a red flag: one candidate pair, two
domains populated at the time, 70% kill rate is a monthly target not a
per-run one.

**Consistent, robust finding across all 28 cards:** none of the three
user-planted concordance objects (`belief propagation`, `Dirichlet process`,
`Kingman's coalescent`) appear by name or alias anywhere in the KB. Go into
the next real `bridge-finder` run expecting it to find structure on its own
(the way it did with `b-2608-001`/`002`), not the three planted bridges.

---

## 2. Fixes made this session, for reference

- **`ingest/apply_triage.py`, `ingest/pdf_extract.py`, `ingest/rebuild_index.py`**
  — written from scratch, all three previously missing. Confirmed working
  against real runs.
- **Negative-exemplar selection bug in `ingest/canon_index.py`** — the
  6-negative block was `[:6]` over citation-count-sorted file order, so one
  high-citation genre (reporting guidelines) permanently crowded out other
  strike patterns. Fixed with bucketed round-robin selection, default raised
  6→10. Verified across all four domains against real triage-prompt output.
- **`ingest/card_schema.json`** — the `evidence`-required `if/then` fired
  vacuously when `named_in_paper` was absent (a JSON-Schema `properties`
  constraint vacuously passes on a missing key), forcing curators to set
  `named_in_paper: true` explicitly rather than relying on the documented
  default. Fixed by adding `required: ["named_in_paper"]` to the `if` clause.
- **Two genuine charter-mismatch cards struck**, both found by direct
  independent re-read against charter text, not by trusting any single
  source: `2608.20406` (stats — empirical forecast-combination demo, no
  analyzable properties, fails `stats.md` §2's admission bar) and `2510.21805`
  (compbio_methods — applied recommendation system, hits the newly-adopted
  §3 applied-ML-systems exclusion). `2504.09854` (stats) was also struck —
  clean §3 setting-inseparability case, the curator's own card had already
  flagged it. All three removed from `papers.sqlite` with a real
  `triage_reason` trail (`status='rejected'`, not left dangling at
  `'admitted'` with no card).
- **`compbio_methods.md`'s two label-derived clauses (§2 property-not-result,
  §3 applied-ML-systems exclusion) — confirmed adopted.** They were already
  live in the file when checked; only the file's own header still described
  itself as an unpromoted draft. Header corrected and dated.
- **Firehose decision resolved**: option 3 (ranked queue) for
  `compbio_methods`. `SETS` unchanged. `daily-ingest.md` §3 now carries an
  explicit exception documenting that this domain's cap is a permanent
  ranked cutoff, not a throughput control — a standing backlog there is
  expected, not a signal to narrow the charter.
- **`vetting-stats.md` line 334** — a mark/reason mixup (reason text had
  landed in the `mark:` field) fixed.
- **Three compbio_mechanism tier-0 exemplars demoted** from kept/exemplar to
  struck — all three were disease-specific papers that violated the
  charter's own general-purpose-method bar, caught because the negative-
  exemplar fix above meant the model would otherwise never have seen a real
  A4-shaped negative for this domain.

---

## 3. What's deliberately open, not forgotten

Nothing below blocks Week 3. Listed so it doesn't get rediscovered from
scratch.

- **`compbio_methods` has 26 admitted papers still queued from the
  *pre-clause* charter.** The 10 curated this session were also pre-clause
  admissions — `2510.21805` was struck for exactly that reason. More
  DiffGRM-shaped papers are plausible in the remaining 26; worth a look
  before pulling more from that pool.
- **`probability` has 8 admitted papers still queued** (18 admitted total,
  10 curated).
- **A 5,275-row untriaged harvest from 2026-08-24 sits in `papers.sqlite`**,
  never triaged — discovered mid-session, not yet acted on. ~1,049 of those
  rows infer to `probability` alone. Deliberately not spent against — see
  the reasoning in `WEEK-2-PLAN.md`'s Step-7 writeup on why model-call spend
  should be a deliberate decision, not a reflex, and treat this the same way.
- **`OPEN-QUESTIONS.md` §1.5 (`compbio_mechanism`'s labelled-row count) is
  stale and needs re-deriving**, not just re-reading. Confirmed 10 rows now
  carry `domain: compbio_mechanism` in `eval/labels.dev.jsonl` (up from the
  document's stated 5, after a routing fix reassigned popgen/phylogenetics
  papers into this domain). The document's further claim of "8 admitted" is
  **unconfirmed** — it likely comes from `papers.sqlite`'s triage-side status
  rather than your own labels (by `my_score`, only 3 of the 10 score ≥4).
  Don't treat either number as settled without checking `papers.sqlite`
  directly.
- **`OPEN-QUESTIONS.md` §1.6 (fresh held-out eval set) is no longer
  hypothetical for `compbio_methods`.** Its charter was partly drafted from
  `eval/labels.dev.jsonl`'s 180 rows, so measuring it against those same
  rows again would be circular. `stats` is unaffected (zero label-derived
  changes there) and remains a valid target without a fresh set.
- **`Tier 1.3` (`calibrate()` re-run, per-domain not pooled)** — still open.
  The pooled figures at the top of `EVAL-01-FINDINGS.md` are now stale by
  more than just the domain-scoping issue that motivated re-running them:
  the `2509.18530` label flip (see below) moved one row from false-positive
  to true-positive, which the document's own projections don't account for.
- **Superseded files still on disk, never confirmed deleted**:
  `charters/compbio.md`, `charters/compbio_genomics.md`,
  `.claude/agents/compbio-curator.md`, `.claude/agents/compbio-genomics-curator.md`.
  Your call whether to keep them as deliberate dead-file markers or remove
  them now that the domain split has been live a while.
- **`2509.18530`'s label was corrected this session** (`my_score` 2→5,
  `expect_out`→`expect_in`) — you judged it a miss on your part, not
  triage's. Independently re-confirmed twice since: once against the
  charter text directly, once by reading its actual curated card (real
  universal-approximation proof, clears §2 cleanly). Worth knowing this one
  is solid if it comes up again.
- **`2307.13826`** (probability — an expository monograph with real proofs
  but no new theorems) was flagged as a closer call against `probability.md`
  §3's "reviews... without a result" exclusion and left in. Seen, not
  missed, but worth a second look if the pattern recurs.

---

## 4. Week 3's actual job: `card_eval.py`

Per `WEEK-2-PLAN.md`'s own closing note and `README.md`'s original phasing
table (row for "2–3"): the point of these weeks is hand-checking cards with
a real tool, "rather than eyeballing them" — and finding out whether the
card schema needs revising *with a number*, not a feeling. That didn't
happen before Week 2's curation the way the original plan wanted; it got
done by direct hand-review instead this session (which is how the DiffGRM
and stats mismatches got caught) — real, but not a repeatable measurement,
and not what `recode.py` needs (its `cards` judgment source is blocked on
this file existing).

**Spec, pulled directly from `README.md` and `HANDOFF.md` (not invented):**
same shape as `eval_triage.py` — `sample` / `label` / `score` / `diff`
subcommands.

```bash
python3 ingest/card_eval.py sample --n 20 --domain stats   # pull cards for hand-checking
python3 ingest/card_eval.py label                          # your judgment, per field
python3 ingest/card_eval.py score                           # curator vs. you
python3 ingest/card_eval.py diff                             # did the last schema/prompt edit help
```

Score on field **equivalence, not exact string match** — a curator writing
"optimal transport" for a paper that says "Sinkhorn divergence" is correct,
not wrong. `README.md` §"Card accuracy" cites the LLM-NERRE paper's
manual-scoring table for why: exact-match badly undercounts correct-but-
reworded extraction, and `mathematical_objects` is exactly the field this
bites hardest.

**Practical starting point for the next session:** write `card_eval.py`
mirroring `eval_triage.py`'s actual file shape (`_infer_domain`, `sample`,
`label`, a `_save`/`_resolve` pair, `score_run`-equivalent, `diff`,
`main()`/argparse) — the assistant can write this the same way it wrote
`apply_triage.py`/`pdf_extract.py`/`rebuild_index.py` this session, without
shell access, and hand it over for you to run. Then run `sample --n 20`
across the now-28-card KB (or per-domain, if 20 from one domain is more
useful given `stats` only has 3), hand-label your own judgment per field,
and get the first real curator-vs-you number this project has ever had.
That number is what tells you whether the schema (or the curator prompts)
need revising — not another round of manual spot-checks like this session's.

**If a field comes back weak and stays weak after a schema/prompt revision**,
`README.md` names `mathematical_objects` as the strongest fine-tuning
candidate (tight schema, high downstream leverage) — not a Week 3 decision,
but on the table if prompting plateaus.

---

## 5. Suggested order

1. Build `card_eval.py`, confirm it runs.
2. `sample` + `label` + `score` against the current 28-card KB — the first
   real number on curator accuracy.
3. Decide, with that number in hand, whether any schema/prompt revision is
   needed before curating further into the `compbio_methods` (26 remaining)
   or `probability` (8 remaining) backlogs.
4. Only then: the deferred items in §3, roughly in this order —
   `compbio_mechanism` §1.5 recount (cheap, clarifies whether a targeted
   `q-bio.*` draw is even still needed), the `calibrate()` per-domain re-run,
   the `compbio_methods` fresh eval set, a decision on the 5,275-row
   untriaged backlog.

Nothing in §3 blocks §4's step 1–2; card evaluation is the thing this
project has never actually measured, and it's cheap relative to everything
else on the list.
