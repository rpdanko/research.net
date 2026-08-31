# Open questions — decision register

Everything currently unresolved, ordered by what unblocks what. Each item says what it is,
why it is open, what it costs to get wrong, and what I would do.

**Pruned 2026-08-28.** Every item was re-checked against the repo rather than carried
forward. Resolved items have been moved to §Closed at the bottom as one-line entries;
decided-but-still-relevant items keep their decision and its consequence, not the
deliberation that produced it. Pre-prune copy: `OPEN-QUESTIONS.md.pre-prune.bak`.

**Section numbers are stable.** `WEEK-3-HANDOFF.md` and `WEEK-3-PLAN.md` cite §1.3, §1.5,
§1.6, §2.2 and §2.3 by number, so identifiers are preserved even where the body changed or
the item closed. Don't renumber.

**Environment note:** the Linux sandbox will not start on this machine, so anything marked
**[shell]** has to run on your side. I can write and edit files, not execute them.

---

## Tier 1 — decide before harvesting or scoring

### 1.1 The `compbio_methods` firehose — `SETS` in `arxiv_pull.py` — DECIDED

**Decided 2026-08-28: option 3, ranked queue.** `SETS` unchanged
(`["math.OC", "cs.LG", "cs.NE", "stat.ML"]`). Recorded in `compbio_methods.md` §8 and
`daily-ingest.md` §3: for this domain the daily cap is a permanent ranked cutoff, not a
throughput control, so a standing backlog is expected and is **not** a signal to tighten the
charter.

Measured against the 180 labels, retained admits of 76 — kept because these numbers cost a
full pass to recompute: **option 1 → 11**, **option 2 → 4**, **option 3 → 76**. Two facts
drove it: `cs.NE` appears zero times in 180 labelled papers despite §8 treating it as half of
option 1, and essentially none of the 17 pure-`cs.LG` papers scored ≥4 carry a
`math.*`/`stat.*`/`q-bio.*` cross-list, which guts option 2. Options 1 and 2 discard 85%+ of
admissions against an invariant that prices recall over precision 3:1.

### 1.3 `calibrate` has not been re-run since the domain-scoping fix **[shell]** — OPEN

**State.** The NEAR=0.57 / FAR=0.59 result — "distributions overlap almost completely" — was
computed against the pooled 8,320-paper canon instead of the ~2,080 papers of one domain,
which is exactly the comparison that washes out separation.

**`EVAL-01-FINDINGS.md` is now corrected — 2026-08-28.** It was worse than "stale by a label
flip": it analyses run `20260827-144416` while **two later score runs existed and went
unmentioned**. Latest (`20260827-214656`) is recall 0.901 / precision 0.688 / F-beta 0.874,
against 0.803 / 0.570 / 0.771 in the document — both metrics moved from below target to at or
above it. Corrected for the `2509.18530` flip: 0.903 / 0.699 / 0.877. That document now
carries a status block with the run history, the corrected arithmetic, and a note that its
per-stratum cells are unreproducible (strata were rewritten by the §1.2 hygiene pass).

**A new open question came out of it — see §1.7.** §6's own pre-registration said precision
"should stay near 0.57. If it rises without a `triage.md` scoring change, find out why before
believing it." It rose 0.12. Nobody found out why.

**Still open here:** the per-domain re-run itself. Every figure above is pooled across all
four domains.

**What to watch.** If separation is still inverted after re-running per-domain, that is a
much cleaner signal about the canon or the domain map than the pre-fix number was, and
`DAY-5-HANDOFF.md` §3.5 is right that the honest response is to fix those rather than ship a
band that adds noise.

### 1.7 The unexplained precision gain — NEW, 2026-08-28

**State.** Precision went 0.570 → 0.607 → 0.688 across the three score runs. `EVAL-01-FINDINGS.md`
§6 pre-registered exactly this as a thing not to believe without investigation, because §2's
diagnosis — triage rounds up systematically, nothing prices against it — says the routing and
exemplar fixes in §4 should *not* have moved precision at all.

**Largely answered 2026-08-28 — a scoring change did land.** Five triage runs exist under
`eval/triage_runs/`; three produced scoreable output (`142635`, `194728`, `203053`) and map
one-to-one onto the three score runs. Comparing the last two directly:

- **Inputs are identical.** Same `labels.dev.jsonl`, same batch composition, same routing,
  same per-paper bands and thresholds. The `SETS` reorder had already landed by `194728`
  (`compbio_mechanism-01` holds 10 papers in both, against 2 in `142635`).
- **Scores moved anyway, and moved in one direction.** On the 35 papers checked
  (`compbio_mechanism-01` + `probability-01`), **13 scores changed and 11 of the 13 went
  down** — seven of them 5→4. Two admit decisions flipped, both from admit to reject.
- **The reason text changed style**, from terse (`§2 mechanism`) to formulaic and fuller
  (`charter §2 lists branching`).

A systematic downward re-scoring with a visible change in output style is a prompt change,
not sampling noise — so this is branch (a), and §2's round-up diagnosis survives. Precision
rising while recall holds is exactly what removing a round-up bias looks like.

**What is still open, and it is not small.** The change is *nowhere recorded* — not in
`EVAL-01-FINDINGS.md`, not in a handoff, not in `dev-notes/`. Reconstruct what was edited in
`.claude/agents/triage.md` between 19:47 and 20:30 on 2026-08-27 and write it down; a repo
with no `git` cannot recover it later. Note also that the 11-of-13 shift is not clean: two
papers moved *up* against the trend, so some ordinary run-to-run variance is present on top
of the prompt effect and no single run's precision should be read to three decimals.

**Also unresolved from the same pre-registration:** the `probability` null prediction can't be
checked at all, because `score_run()` reports pooled and per-stratum figures but never per-domain.
Same gap as §1.3.

### 1.4 `LABEL-USE-PROTOCOL.md` for `compbio_methods` — DECIDED

**Decided 2026-08-28: adopt.** Both drafted changes are live in `charters/compbio_methods.md`
— the §3 applied-ML-systems exclusion (n≈90) and the §2 property-not-result clause (n=17).
`eval/labels.jsonl` → `eval/labels.dev.jsonl` rename is done.

**Live consequence, not history:** the 180-row set is now a *development* set for this domain
specifically, because it partly drafted the charter. Any recall/precision claim about
`compbio_methods` measured against those same rows is circular — see §1.6. `stats` is
unaffected (zero label-derived changes) and remains a valid eval target as-is.

### 1.5 Which domains does round one actually evaluate? — OPEN, numbers now re-derived

**Counts re-derived 2026-08-28** from the `domain` field in `eval/labels.dev.jsonl`, which is
now backfilled on all 180 rows (the old table below-the-line was by *primary category*, before
the routing fix — every one of its four numbers was wrong). Admits are `my_score ≥ 4`.

| Domain | Rows | Admits | Rejections | Usable for per-charter tuning? |
|---|---|---|---|---|
| `compbio_methods` | 101 | 26 | 75 | Yes — but it is the *dev* set, see §1.4 |
| `stats` | 40 | 26 | 14 | Yes, and uncontaminated — the best target today |
| `probability` | 29 | 17 | 12 | Marginal, better than previously thought |
| `compbio_mechanism` | **10** | **3** | 7 | **Still no** |

Superseded table, for reference — do not use: `compbio_methods` ~127/35, `stats` 32/22,
`probability` 16/11, `compbio_mechanism` 5/1.

**Two things changed the picture.** `stats` is now the strongest usable target, not a marginal
one: it roughly doubled in rows and is the only domain both large enough and uncontaminated.
And `compbio_mechanism` went 5 → 10 rows via the routing fix that moved popgen/phylogenetics
papers in — but only **3** of those 10 score ≥4, so it is still unusable for tuning, just for
a different reason than before.

**Still unconfirmed:** the "8 admitted" figure quoted for `compbio_mechanism` elsewhere. It
does not come from the labels (3 admits, above) and most likely comes from `papers.sqlite`'s
triage-side status. Settle it directly before relying on either number **[shell]**:

```bash
sqlite3 ingest/papers.sqlite \
  "select status, count(*) from papers where domain='compbio_mechanism' group by status"
```

**The bind, unchanged.** `compbio_mechanism` carries the popgen/phylogenetics admission — made
against your stated "I do not work on evolutionary biology" on bridge-finding grounds. It is
the charter most in need of measurement and still the one with the fewest usable labels.
Fixing that needs a targeted `sample --append` draw restricted to `q-bio.*`, which is its own
labelling sitting. Resolve the sqlite question above first — it may show the draw is
unnecessary.

### 1.6 Fresh test set — OPEN. Sampler ordering — FIXED 2026-08-28

**Ordering fix applied.** `random.shuffle(picks)` now runs after the quota loop in
`sample()`, before `new_recs` is built, with a comment recording why. Confirmed this is the
order that matters: `label()` iterates the file top to bottom, so file order *is* the order
you score in. Only the new draw is shuffled — in `--append` mode `existing` is written ahead
of `new_recs` untouched, so already-labelled rows never move. Nothing downstream depends on
stratum grouping; `score_run()` buckets on the `stratum` field, not position.

The bug it removes: the loop shuffled *within* each band, which randomized which rows were
drawn but still emitted an `expect_in` block, then `expect_out`, then `borderline` — the
streaking that produced rows 105–133 (24 admits of 29) and rows 134–147 (fourteen consecutive
rejections) in the existing set.

**Still open: the fresh set itself.** §1.4 makes the 180 rows a dev set for
`compbio_methods`, so a fresh 60–80 is required for any real measurement of that charter.
`stats` does not need one. The sampler is now safe to draw with.

**Noted, not fixed:** `random` is unseeded, so draws are not reproducible. Pre-existing —
the within-band shuffle had the same property — and arguably right for a sampler you re-run.
Only worth changing if you ever need to reconstruct exactly which rows a past draw pulled.

---

## Tier 2 — charter obligations

### 2.2 Rewrite-prep — `compbio_mechanism` DONE 2026-08-28; two still open

`charters/compbio_mechanism.rewrite-prep.md` is written, in the same shape as
`stats.rewrite-prep.md`. **Two of its four rulings are made and applied:**

- **A3 — the molecular-scale bound, ruled: adopt.** "I work at the molecular level," and the
  bound is two-sided. §3 needs a criterion excluding work above the cell (ecology,
  epidemiology, organism- and population-level biology) and below the molecule (force fields,
  atomic modelling). Note when writing it that popgen *theory* is unaffected — Wright-Fisher
  and Moran processes are mathematical objects, and a triage agent will assume otherwise
  unless §3 says so.
- **A2 — the two overturned strikes, ruled: both flip to keep.** Reading the nine
  evolutionary-biology strikes settled §8's claim (two of nine were theory — small, as
  asserted, but now measured). The two are `W1533696952` *Niche Construction* and
  `W2167062553` Nowak's *Five Rules for the Evolution of Cooperation* — precisely the papers
  §2 now admits by name under its popgen-theory and biological-cooperation criteria. Both
  marks are now `k` in `canon/vetting-compbio_mechanism.md` with reasons naming the criterion.

**Blocking follow-up [shell]:** `python3 ingest/canon_tier.py apply`. `exemplars()` reads the
canon records, not the worksheet, so until that runs both papers are still `vetted: struck`
and still eligible for the negative-exemplar block — the exact contradiction the ruling was
meant to remove.

**A1 and A4 also applied 2026-08-28.** A1: §8's "nearly every sequencing strike was a
software announcement" corrected — three are genome-result/resource papers the software
criterion does not reach, so the reframe depends on two §3 bullets, not one. A4: all ten
uninformative strike reasons ("Not relevant", "Really interesting but not relevant to what I
do") rewritten against the criterion that actually applies, originals preserved verbatim
inline. `strike_superseded` was not used — those strikes were correct, just badly worded, and
the field means "overruled," which would corrupt its meaning for §A2's cases.

Five of the ten turned out to be molecular-scale rejections, which is A3's bound appearing
retrospectively. Three were LLM/NLP-on-text papers with no biological content at all — not
near misses inside the domain but outside it, and useless as negative exemplars. One of those
three is `W4391836235`, the LLM-NERRE paper `README.md` cites for card-accuracy scoring:
useful to the project, not KB material. That is `EVAL-01-FINDINGS.md` §5 step 2's metatool
shelf, still homeless, now recurring in a second domain.

**Still open:** §3's criteria text is unwritten — A3 ruled a molecular-scale bound belongs
there, but adding it is handwriting work per `README.md`. Rewrite-prep for `probability.md`
and `compbio_methods.md`.

### 2.3 Deferred by the protocol's own floor — OPEN

- **AI-for-science flag** (`PASS-4-DRAFTS.md` §1.3). Lines 86 and 108 scored 4, lines 17 and
  46 scored 2–3 — a plausible contribution-vs-review boundary. n=4, below R1's floor of 5.
  Re-examine against the fresh set, not the dev set.
- **Line 80** — cytoskeletal statistical-mechanical framework, `q-bio.CB/MN/SC`, scored 2
  despite sitting in the centre of `compbio_mechanism.md` §2. Re-read candidate, n=1.
- **Line 109** — *"Evaluating RL Explainability Methods…"*, stratum `in`, score 2. The only
  internal contradiction in 180 rows. Likely a keying slip; worth confirming.
- **`2307.13826`** (probability) — expository monograph with real proofs but no new theorems,
  a closer call against `probability.md` §3's "reviews… without a result" exclusion than the
  admission implies. Left in deliberately; seen, not missed. Revisit if the pattern recurs.

---

### 1.8 Curator prompts must be told to record the version — NEW, 2026-08-28 **[you]**

**Fixed already:** `pdf_extract.py` resolves the arXiv version before fetching, fetches the
*versioned* id, keys the cache on it, and returns `source_version` + `source_sha256`, printed
where the curator cannot miss them. `card_schema.json` accepts both fields.
`ingest/backfill_source_pins.py` retrofits the existing 28 by matching cached e-print bytes
against each version's sha256. `card_eval.py` shows the version while labelling and warns when
a card has none.

**Not fixed, and it is the half that makes the rest work:** the four curator prompts under
`.claude/agents/` still do not tell the curator to copy those two values onto the card, and
`.claude/**` is not writable from the assistant side. Until that line is added, `pdf_extract`
prints the pin and every curator ignores it.

**Why this was worth interrupting Tier 1 for.** `pdf_extract.py` used to fetch
`e-print/<bare id>`, which arXiv resolves to whatever is latest *at fetch time*, and cache it
under the bare id — while the module docstring asserted "an arXiv version is immutable, so
there is no staleness question." True of a version, false of the bare id, and the code relied
on the false reading. Two extractions months apart could return different papers with no
record of which one a card was built from.

It cost something immediately: card `2407.01051` was hand-checked against the v1 HTML and
appeared to claim a numerical-experiments section that does not exist there. It exists in v3.
**The card was right and the check was wrong** — and nothing on the card could have settled
which of the two was looking at the paper the curator read. A verification step that reports
correct extractions as fabrications is worse than no verification step, because it spends the
scarcest thing in the system on manufacturing false positives.

**Deliberately optional, not required, in the schema.** All 28 existing cards lack these
fields, and "a card that does not validate does not exist" means requiring them would delete
the KB. Make them required after a re-curation pass, not before.

## Tier 3 — small, cheap, easy to lose

- **Routing precedence on multi-cross-listed numerical papers — new, low priority.** Surfaced
  while closing the coverage gap below. `_infer_domain()` assigns a paper to the *first*
  domain in `SETS` whose category list intersects, and `probability` precedes
  `compbio_methods`. So line 117 (`math.NA cs.LG cs.NA math.AP math.PR`) routes to
  `probability` on its `math.PR` cross-list, even though `math.NA` and `cs.LG` both point at
  `compbio_methods`. No harm in this instance — it scored 5 and probability is a defensible
  home — but precedence order is doing real work on numerical papers that cross-list into
  probability, and nobody has checked whether it lands right in general. Worth one pass over
  the `math.NA` admissions when there are enough to look at.

---

## Closed

Verified against the repo on 2026-08-28. Kept as one-liners so they stop being rediscovered;
full pre-prune text in `OPEN-QUESTIONS.md.pre-prune.bak`.

- **0.1 `run_triage.py` missing** — written; `ingest/run_triage.py` exists.
- **0.2 `apply_triage.py` missing** — written, along with `pdf_extract.py` and
  `rebuild_index.py`. The consequences named under it are also gone: `papers.sqlite`'s
  `domain` column is populated, and `kb/` now holds 28 cards (`stats` 3, `probability` 10,
  `compbio_methods` 9, `compbio_mechanism` 6), so cards → concordance → bridges has run end to
  end. `bridge-finder` produced `b-2608-001`/`002`; both were killed by the skeptic.
- **1.2 Label hygiene** — done. All 180 rows carry `expect_in`/`expect_out`/`borderline`; no
  `In`, `Borderline`, `borderlinne` or `pit` remain, so the case-sensitive
  `startswith("border")` blind spot is closed. `domain` is backfilled on all 180 rows, zero
  nulls. `2608.07528` (the `"pit"` row) is resolved.
- **2.1 `stats.pass4.md` promotion** — done; no `.pass4.md` files remain in `charters/` and
  `charters/stats.md` is live.
- **3.x `vetting-stats.md` line 334** — fixed; `mark: s` with a full `reason:` on line 335.
- **3.x `vetting-compbio_methods.md` line 148** — `W4408399347` now carries `mark: S`.
- **3.x stray file `research-net/To`** — deleted.
- **3.x Domain-map coverage gap** — closed 2026-08-28, as **not a gap**. The bullet was wrong
  three ways. (a) *Wrong file:* `canon/domain_map.yaml` holds OpenAlex topic IDs for slicing
  the canon; it contains no arXiv categories at all, so "no `math.NA` entry" was never
  meaningful. Harvest coverage lives in `arxiv_pull.py`'s `SETS`. (b) *Wrong test:*
  `harvest_oai()` filters on `wanted.intersection(cats)` — **any** category, not the primary
  one. All seven papers reach the DB today through their cross-lists (`math.PR`, `math.ST`,
  `stat.ME`, `cs.LG`), and `math.NA` was since added to `compbio_methods` explicitly, with a
  comment giving exactly this reason. (c) *Wrong count:* six of the seven scored ≥4, not all
  seven — line 36 (`math.NA cs.LG cs.NA`) scored 2. Nothing to decide; nothing was ever
  unreachable. The one real residual is routing, not harvesting — see Tier 3 above.
- **3.x Superseded files** — all deleted: `charters/compbio.md`,
  `charters/compbio_genomics.md`, `.claude/agents/compbio-curator.md`,
  `.claude/agents/compbio-genomics-curator.md`, `canon/vetting-compbio_genomics.md`. The
  "deliberate dead-file markers" question is moot.

---

## If I had to pick three

1. **`compbio_mechanism`'s real admitted count** (1.5) — one sqlite query, and it decides
   whether a whole `q-bio.*` labelling sitting is needed or not.
2. **The unexplained precision gain** (1.7) — 0.570 → 0.688 against an explicit
   pre-registered warning not to believe it un-investigated. It decides whether §2's round-up
   diagnosis, which shaped the pass-4 charters, was right.
3. **The `compbio_methods` fresh test set** (1.6) — §1.4 makes it mandatory for any honest
   number about that charter, and the sampler is now safe to draw it with.

~~The sampler ordering fix (1.6)~~ — done 2026-08-28.
~~The domain-map coverage gap (Tier 3)~~ — closed 2026-08-28; it was not a gap. See §Closed.

Note what is *not* on this list: `ingest/card_eval.py`. It is Week 3's actual program
(`WEEK-3-PLAN.md` §3) rather than an open question — the decision to build it is made, only
the building is left.
