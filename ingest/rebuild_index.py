#!/usr/bin/env python3
"""Aggregates card front matter into kb/<domain>/index.jsonl, and optionally
merges the user concordance layer into kb/concordance.merged.jsonl.

    rebuild_index.py                              # daily: rebuild every domain's index
    rebuild_index.py --domain stats                # one domain only
    rebuild_index.py --verify                      # full schema check, not the fast path
    rebuild_index.py --merge-user-concordance       # also build concordance.merged.jsonl
    rebuild_index.py --dry-run                      # report, write nothing

The last unwritten piece of the cards -> concordance -> bridges chain.
`bridge-finder` and `math-scout` both read "index lines", never full cards --
this is the script that produces them. Until it existed, `kb/*/index.jsonl`
did not exist, `bridge-finder` had nothing to read regardless of how many
cards `kb/` held, and `kb/concordance_user.jsonl`'s three draft entries could
not be promoted because nothing ever merged them in.

WHY --VERIFY IS A SEPARATE, SLOWER PATH
`daily-ingest.md` sec4 runs `validate_card.py --new-only` immediately before
this script, every day. `weekly-synthesis` sec0 runs this script alone, no
preceding validate step, over cards accumulated across seven daily runs and
however many `--restate` re-triage passes happened in between. The daily
caller has already paid for full jsonschema validation on every new card;
re-paying for it here would be pure waste on a hot path that runs once a day.
The weekly caller has no such guarantee -- a schema edit, a hand-fixed card, a
`redomain`-style script touching files outside the normal pipeline, any of
these could produce a card nothing has re-checked. So: the default path does a
cheap presence check (front matter parses, required keys exist) and trusts the
caller already validated; `--verify` re-runs `validate_card.check()` in full,
schema and the semantic checks both, and is what the weekly skill asks for.

Either way, a card that fails is EXCLUDED from the index and reported, never
included with a warning. `validate_card.py`'s own line: "A card that does not
validate does not exist." An index is exactly the place that sentence has to
be enforced, because it is the only thing `bridge-finder` and `math-scout`
ever read -- a bad card silently indexed is a bad card that reaches both of
them with no gate in between.

WHY AN INDEX LINE IS THE WHOLE CARD, NOT A SUMMARY OF IT
Cards in this repo are YAML front matter and nothing else -- every curator
prompt says "write kb/<domain>/cards/<id>.md following the schema exactly"
and none describes body prose beyond it. There is therefore nothing to trim:
"index lines, never full cards" means *one aggregated file instead of many
small ones*, not a lossy view. If curators ever start writing prose bodies
below the front matter, this script still only reads the front matter block
(same regex `validate_card.py` uses) -- that would become a real information
cut and this comment would stop being true; worth revisiting then, not now.

One field is added beyond the schema: `path`, the card's file path relative to
repo root. Nothing in the schema carries it and `math-scout` needs it for the
"read that one card" fallback when an object is too ambiguous to classify from
the index line alone (math-scout.md sec1).

WHY THE MERGE IS A SEPARATE FLAG, NOT ALWAYS ON
`daily-ingest.md` never passes `--merge-user-concordance`; `weekly-synthesis`
always does. That split is already in the two skill files and this script
follows it rather than picking its own default: `math-scout` is the only
writer of the base concordance and it runs weekly, so a merge computed between
math-scout runs reflects a concordance that hasn't changed, at the cost of a
full re-read and re-write of both files for nothing.

THE NO-MARKER REQUIREMENT IS LITERAL
`README.md`: "union kb/concordance_user.jsonl over the base into
concordance.merged.jsonl, user winning on conflict, base untouched, and no
marker distinguishing the two in the merged output." `bridge-finder.md` is
equally explicit: "do not look for the planted_by field and do not weight an
entry differently because it carries one." So `planted_by` and
`planted_reason` are stripped from every merged row, including passthrough
rows that exist ONLY in the user file -- a passthrough entry that still carried
`planted_by` would be the one row in the merged file bridge-finder could
single out, which defeats the entire point of merging at read time instead of
handing bridge-finder two files and a promise not to look.

`math-scout` still gets `kb/concordance_user.jsonl` as a SEPARATE, unmerged
input (weekly-synthesis sec1) specifically so it CAN tell and can verify what
it's being asked to verify. That is not a contradiction with the paragraph
above -- it is bridge-finder that must not distinguish, because bridge-finder
is not the component qualified to re-check a mathematical identification.

DUPLICATE OBJECTS IN THE BASE FILE ARE A HARD STOP, NOT A MERGE DECISION
If `kb/concordance.jsonl` ever contains two rows with the same `object`, this
script refuses to merge rather than picking one silently. Resolving a
duplicate is math-scout's consolidation job (math-scout.md: "if it passes
~800 lines, spend a week doing nothing but consolidation"), not a merge
script's, and a silent pick would make the merged file wrong in a way nothing
downstream could detect.
"""

import argparse, json, sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml")

ROOT = Path(__file__).parent.parent
KB = ROOT / "kb"
CONCORDANCE = KB / "concordance.jsonl"
USER_CONCORDANCE = KB / "concordance_user.jsonl"
MERGED = KB / "concordance.merged.jsonl"

DOMAINS = ("stats", "probability", "compbio_methods", "compbio_mechanism", "math")

sys.path.insert(0, str(Path(__file__).parent))
from validate_card import check as full_check, FM  # noqa: E402  same parser, not a second copy

SCHEMA = json.loads((ROOT / "ingest" / "card_schema.json").read_text())
REQUIRED = SCHEMA["required"]


# --------------------------------------------------------------- card index

def _parse_front_matter(path):
    m = FM.match(path.read_text())
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None


def _index_one(path, verify):
    """Returns (row, None) on success, (None, [problems]) on failure.

    `verify=True` runs the exact check `validate_card.py` runs on every card,
    daily. `verify=False` only confirms the front matter parses and the
    schema's required keys are present -- catches a card so broken it would
    poison every index line silently, without re-paying for a full jsonschema
    pass on a card the daily run already validated.
    """
    if verify:
        problems = full_check(path)
        if problems:
            return None, problems

    data = _parse_front_matter(path)
    if data is None:
        return None, ["no parsable YAML front matter"]

    if not verify:
        missing = [k for k in REQUIRED if k not in data]
        if missing:
            return None, [f"missing required field(s): {', '.join(missing)} "
                          f"-- re-run with --verify for the full schema check"]

    row = dict(data)
    row["path"] = str(path.relative_to(ROOT))
    return row, None


def build_domain(domain, verify):
    cards_dir = KB / domain / "cards"
    cards = sorted(cards_dir.glob("*.md")) if cards_dir.exists() else []

    rows, failed = [], []
    for path in cards:
        row, problems = _index_one(path, verify)
        if row is None:
            failed.append((path, problems))
        else:
            rows.append(row)

    rows.sort(key=lambda r: (r.get("date") or "", r.get("arxiv_id") or ""))
    return rows, failed


# ------------------------------------------------------------ concordance merge

def _read_jsonl_strict(path):
    """Unlike coalition_audit's read_jsonl, a malformed line here is fatal.

    That script tolerates junk because an audit is read-only and a skipped
    row just under-counts one metric. This one is about to WRITE a file every
    other agent trusts unconditionally; a base concordance that doesn't parse
    is not something to merge around quietly.
    """
    if not path.exists():
        return []
    rows = []
    for i, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            sys.exit(f"malformed JSON at {path.relative_to(ROOT)}:{i}: {e}\n"
                     f"Refusing to merge -- fix the line by hand, this is the "
                     f"kind of failure weekly-synthesis's halt-the-run note "
                     f"exists for.")
    return rows


def merge_concordance():
    base = _read_jsonl_strict(CONCORDANCE)
    user = _read_jsonl_strict(USER_CONCORDANCE)

    dupes = [o for o, n in Counter(r.get("object") for r in base).items() if n > 1]
    if dupes:
        sys.exit(f"kb/concordance.jsonl has duplicate 'object' entries: "
                 f"{dupes[:5]}. Refusing to merge on top of an ambiguous base "
                 f"-- this is math-scout's consolidation pass to run, not a "
                 f"merge decision for this script to make silently.")

    by_object = {r["object"]: dict(r) for r in base if r.get("object")}
    added, modified, warnings = [], [], []

    for u in user:
        obj = u.get("object")
        if not obj:
            sys.exit(f"a kb/concordance_user.jsonl row has no 'object' field: "
                     f"{u!r}. Refusing to merge.")
        if u.get("planted_by") != "user":
            warnings.append(
                f"{obj!r}: missing planted_by:'user' -- "
                f"concordance_user.spec.md requires it; without it "
                f"coalition_audit.py's coupling measurement can't see this row.")

        if obj in by_object:
            b = by_object[obj]
            merged = dict(b)
            merged["aliases"] = sorted(set(b.get("aliases") or [])
                                       | set(u.get("aliases") or []))
            paper_union = defaultdict(set)
            for src in (b.get("papers") or {}), (u.get("papers") or {}):
                for dom, ids in src.items():
                    paper_union[dom].update(ids or [])
            merged["papers"] = {d: sorted(ids) for d, ids in paper_union.items()}
            merged["cross_domain"] = bool(b.get("cross_domain")) or bool(u.get("cross_domain"))
            if u.get("theory_gap"):
                merged["theory_gap"] = u["theory_gap"]   # user overrides, per spec
            dates = [d for d in (b.get("first_seen"), u.get("first_seen")) if d]
            if dates:
                merged["first_seen"] = min(dates)
            merged.pop("planted_by", None)
            merged.pop("planted_reason", None)
            by_object[obj] = merged
            modified.append(obj)
        else:
            passthrough = {k: v for k, v in u.items()
                           if k not in ("planted_by", "planted_reason")}
            by_object[obj] = passthrough
            added.append(obj)

    rows = [by_object[k] for k in sorted(by_object)]
    return rows, added, modified, warnings


# ------------------------------------------------------------------- driver

def main():
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--domain", choices=DOMAINS, help="restrict to one domain")
    ap.add_argument("--verify", action="store_true",
                    help="full validate_card.py check on every card, not just "
                         "the required-fields presence check")
    ap.add_argument("--merge-user-concordance", action="store_true",
                    help="also build kb/concordance.merged.jsonl")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    domains = [a.domain] if a.domain else list(DOMAINS)

    print(f"{'domain':<20} {'indexed':>8} {'failed':>7}")
    total_rows, total_failed = 0, 0
    per_domain = {}
    for domain in domains:
        rows, failed = build_domain(domain, a.verify)
        per_domain[domain] = (rows, failed)
        total_rows += len(rows)
        total_failed += len(failed)
        print(f"{domain:<20} {len(rows):>8} {len(failed):>7}")

    if total_failed:
        print(f"\n{total_failed} card(s) excluded from the index:")
        for domain in domains:
            for path, problems in per_domain[domain][1][:10]:
                print(f"  {path.relative_to(ROOT)}")
                for p in problems:
                    print(f"      {p}")
        shown = sum(min(10, len(per_domain[d][1])) for d in domains)
        if total_failed > shown:
            print(f"  ... and {total_failed - shown} more")

    merged_rows = added = modified = warnings = None
    if a.merge_user_concordance:
        merged_rows, added, modified, warnings = merge_concordance()
        print(f"\nconcordance merge: {len(merged_rows)} objects "
              f"({len(added)} from user only, {len(modified)} merged with base)")
        if warnings:
            print("  warnings:")
            for w in warnings:
                print(f"    {w}")

        if a.verify:
            all_ids = {r.get("arxiv_id") for d in domains
                       for r in per_domain[d][0]} - {None}
            dangling = set()
            for row in merged_rows:
                for ids in (row.get("papers") or {}).values():
                    dangling.update(set(ids or []) - all_ids)
            if dangling:
                print(f"\n  {len(dangling)} arxiv_id(s) in the concordance have "
                      f"no indexed card (not fatal, worth a look): "
                      f"{', '.join(sorted(dangling)[:8])}")

    if a.dry_run:
        print("\n--dry-run: nothing written.")
        return

    for domain in domains:
        rows, _ = per_domain[domain]
        out = KB / domain / "index.jsonl"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("".join(json.dumps(r) + "\n" for r in rows))

    print(f"\nwrote {total_rows} index line(s) across {len(domains)} domain(s)")

    if a.merge_user_concordance:
        MERGED.write_text("".join(json.dumps(r) + "\n" for r in merged_rows))
        print(f"wrote {len(merged_rows)} row(s) to {MERGED.relative_to(ROOT)}")

    if total_failed:
        sys.exit(1)   # matches arxiv_pull.py: a partial result still halts the caller


if __name__ == "__main__":
    main()
