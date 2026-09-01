# TODO

Read by `pmd` once a day, which surfaces the single item under `## Next step` on
the dashboard. Everything under `## Backlog` is counted but not surfaced —
promote an item up when it becomes the next thing.

Keep exactly one unchecked box under `## Next step`. The reasoning behind any
item here lives in `PROJECT-STATUS.md`, `OPEN-QUESTIONS.md` and
`CARD-EVAL-HANDOFF.md`; this file is the index, not the argument.

## Next step

- [ ] Run the card-eval path end to end for the first time: smoke-test `python3 ingest/show_eprint.py 2506.07459 --list`, then `card_eval.py import` each of the four files in `eval/drafts/`, then `label`, then `score`. Nothing has ever been scored — `eval/card_runs/` is empty — and a large share of `score_run()` has never executed, so treat the first pass as debugging rather than measurement. ~3h

## Backlog

- [ ] Insert a blank line between lines 52 and 53 of `.claude/agents/compbio-mechanism-curator.md`, where the alias paragraph runs into the `named_in_paper: false` sentence and markdown folds them into one
- [ ] Settle `CARD-EVAL-HANDOFF.md` §7.2 and §7.3 — whether `named_in_paper` gets renamed or just documented, and renaming `score_run()`'s printed "object recall" label, which reports curator fidelity under a name that reads as KB completeness. Both are text-only and neither blocks labelling
- [ ] Run `python3 ingest/backfill_source_pins.py`. The four curator prompts now tell curators to record `source_version` and `source_sha256`, so new cards will carry a pin and the existing 28 will not until this runs
- [ ] Add a `name` validator to `ingest/validate_card.py` rejecting `(`, `/` and ` and ` in a `mathematical_objects` name. Catches `Hermitization (Girko's method)`, `Subset-rank and no-cancellation conditions`, and `Circuit skeleton / ansatz topology` at write time — all three are real and all three currently score `y`
- [ ] Check whether arXiv 2601.03123 has a v2. If it does not, the abstract stored in `papers.sqlite` came from a version arXiv does not serve, which bears on all 28 cards (`CARD-EVAL-HANDOFF.md` §5.1)
- [ ] Run `python3 ingest/show_eprint.py 2506.07459 --grep` against the §3.2.2 wording quoted in that card's `evidence` field, to settle whether the card was built outside its declared `sections_read` (§5.4a)
- [ ] Run `python3 ingest/canon_tier.py apply`, then re-render exemplars. The `compbio_mechanism` worksheet edits — two strike reversals and ten rewritten reasons — are inert until this runs, and the two reversed papers are still eligible for the negative block (`PROJECT-STATUS.md` Tier 0 item 5)
- [ ] Correct `CLAUDE.md`'s phase marker and point it at `PROJECT-STATUS.md` (Tier 0 item 4)
- [ ] Add an optional `strike_superseded` field to `ingest/canon_index.py` so `exemplars()` skips overruled strike reasons, keeping the vetting record intact while keeping a reversed judgment out of the triage prompt (`EVAL-01-FINDINGS.md` B2, ~5 lines)
