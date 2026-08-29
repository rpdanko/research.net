---
name: daily-ingest
description: Daily pipeline. Harvests new arXiv submissions, triages them against domain charters, and dispatches curators to write cards for what passes. Run from cron at 06:00.
---

# Daily ingest

Sequential. Do not parallelize; there is no time pressure and serial execution makes failures legible.

## 1. Harvest (no model calls)

```bash
python3 ingest/arxiv_pull.py --since yesterday
```

Writes new rows to `ingest/papers.sqlite` with `status='new'`. Idempotent on `arxiv_id` — safe to re-run after a failure.

If it exits non-zero, **stop the entire run** and write the error to `logs/health.jsonl`. Do not proceed with a partial harvest; a gap in the corpus is invisible later and there is no way to detect one after the fact.

## 2. Triage

For each domain in `stats, probability, compbio_methods, compbio_mechanism`:

- Pull `status='new'` rows whose categories overlap the domain's category list (see `charters/<domain>.md`).
- Batch into groups of 25.
- Dispatch the `triage` subagent per batch, passing the charter path and output path.

Then:

```bash
python3 ingest/apply_triage.py apply --dry-run   # read the transitions first
python3 ingest/apply_triage.py apply
```

## 3. Curate

For each domain, take admitted papers, **capped at 10 per domain per day**. If more than 10 pass, take the highest-scoring 10 and leave the rest at `status='admitted'` — they will be picked up tomorrow. Do not raise the cap to clear a backlog; a backlog that never clears means the charter is too broad and should be tightened instead.

**Exception: `compbio_methods`.** The firehose decision (`OPEN-QUESTIONS.md` §1.1, `compbio_methods.md` §8 — resolved 2026-08-28, option 3) keeps `SETS` broad on purpose: narrowing categories would discard 85%+ of real admissions against the labelled-set analysis, spending recall the invariants price at 3:1 over precision. For this domain only, a standing backlog is the expected, permanent state — not evidence the charter is too broad. The cap is deliberately reinterpreted as a ranked cutoff ("top 10 by score today") rather than a throughput control. Do not narrow `SETS` to clear it.

Dispatch the matching curator subagent (`stats-curator`, `prob-curator`, `compbio-methods-curator`, `compbio-mechanism-curator`) with the list of IDs. One subagent invocation per domain, not per paper.

## 4. Validate

```bash
python3 ingest/validate_card.py kb/*/cards/*.md --new-only
python3 ingest/rebuild_index.py
```

Any card that fails validation: log it, set the paper back to `status='admitted'`, and **do not** retry the curator today. Repeat failures on the same paper are a schema problem, not a model problem, and retrying hides that.

## 5. Health record

Append one line to `logs/health.jsonl`:

```json
{"date": "", "harvested": 0, "triaged": 0, "admitted": 0, "cards_written": 0,
 "validation_failures": 0, "backlog": 0, "errors": []}
```

Check this weekly. A cron job that starts failing quietly is the most likely way this system dies, and `backlog` climbing steadily is the earliest signal that the charters need work.

## What this skill does not do

No synthesis, no bridges, no proposals. If today's papers look interesting, that is not actionable here — the weekly run sees them in context, which is the only place an intersection is visible.

It also does not catch a paper that is useful to how this project itself operates — agent-design prior art, background reference material — rather than an object of study for any domain charter. That paper is correctly rejected by triage and then genuinely lost; a rejection isn't retrievable later. No automated tag catches this on purpose (see `dev-notes/parking-lot.md`) — if you notice one while reading the digest, add it there yourself.
