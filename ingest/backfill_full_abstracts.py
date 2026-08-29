#!/usr/bin/env python3
"""One-off: replace every truncated abstract in a labels file with the full
text from papers.sqlite.

Why this is safe and not a rewrite: arxiv_pull.py's harvest never truncates
--  abstract TEXT NOT NULL in the schema holds the complete text, whitespace-
normalized only. The only truncation in this project happens in
eval_triage.py's sample(), which used to cap stored abstracts at 1500 chars
before writing them into labels.jsonl. That cap cut at least one real paper
off mid-sentence (2602.05541, the quantum-matrix-multiplication paper -- the
truncated text read "end-to-end coherent computati", missing its own final
clause) and triage.md's classifier correctly followed its own rule for that
input ("Truncated or malformed: score 0, reason malformed"). The agent
wasn't wrong; the stored data was incomplete. Now fixed going forward (the
cap is 8000, effectively unlimited for a real abstract) -- this script
repairs what the old cap already wrote into a labels file.

papers.sqlite is authoritative here, not arXiv itself: querying arXiv per
row would be slower, adds a network dependency, and risks drift if a paper
was revised after harvest. The harvested copy is what triage actually saw
and is what should be corrected.

Usage:  python3 ingest/backfill_full_abstracts.py [--labels eval/labels.dev.jsonl]
Writes the labels file in place. Backs up first to <path>.pre-backfill.bak.
Only touches the abstract field -- title, domain, stratum, my_score, and
everything else in each row is untouched.
"""
import argparse, json, shutil, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DB = ROOT / "ingest" / "papers.sqlite"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", default=str(ROOT / "eval" / "labels.dev.jsonl"))
    a = ap.parse_args()

    labels_path = Path(a.labels)
    if not labels_path.exists():
        sys.exit(f"no {labels_path}")
    if not DB.exists():
        sys.exit(f"no {DB} -- nothing to backfill from")

    recs = [json.loads(l) for l in labels_path.read_text().splitlines() if l.strip()]

    con = sqlite3.connect(DB)
    fixed, missing, already_full = [], [], 0

    for r in recs:
        row = con.execute("SELECT abstract FROM papers WHERE arxiv_id = ?",
                          (r["arxiv_id"],)).fetchone()
        if not row or not row[0]:
            missing.append(r["arxiv_id"])
            continue
        full = row[0]
        if full == r["abstract"]:
            already_full += 1
            continue
        if len(full) < len(r.get("abstract", "")):
            # The stored copy is LONGER than the DB's -- shouldn't happen
            # given the DB is the harvest source, but don't silently prefer
            # a shorter "fix" over what's already there.
            missing.append(f"{r['arxiv_id']} (DB copy shorter, skipped)")
            continue
        fixed.append((r["arxiv_id"], len(r.get("abstract", "")), len(full)))
        r["abstract"] = full

    if fixed:
        backup = labels_path.with_suffix(labels_path.suffix + ".pre-backfill.bak")
        shutil.copy(labels_path, backup)
        labels_path.write_text("".join(json.dumps(r) + "\n" for r in recs))
        print(f"backed up to {backup}\n")

    print(f"{len(fixed)} row(s) had a truncated abstract, now restored to full text:")
    for aid, old_len, new_len in fixed:
        flag = "  <-- was cut mid-sentence at exactly the old cap" if old_len == 1500 else ""
        print(f"  {aid}  {old_len} -> {new_len} chars{flag}")

    print(f"\n{already_full} row(s) already had the full abstract (untruncated originally).")
    if missing:
        print(f"\n{len(missing)} row(s) could not be resolved against papers.sqlite: "
              f"{', '.join(str(m) for m in missing[:10])}"
              f"{' ...' if len(missing) > 10 else ''}")
        print("These predate the current harvest, or arrived by hand -- recheck by hand "
              "if any of them matter for scoring.")

    if fixed:
        print(f"\nAny paper above scored 'malformed' in a past run is worth a fresh look "
              f"-- its input was genuinely incomplete then and isn't now.")


if __name__ == "__main__":
    main()
