#!/usr/bin/env python3
"""Retrofit source_version / source_sha256 onto cards written before pinning.

    backfill_source_pins.py --dry-run     # report only, touch nothing
    backfill_source_pins.py               # write the pins it can prove
    backfill_source_pins.py --domain stats

WHY THIS CAN BE DONE AT ALL.

pdf_extract.py caches the e-print it fetched at ingest/cache/eprint/<id>.bin and
parses the card's text out of that blob. So for every card whose blob is still
on disk, THE EXACT BYTES THE CURATOR READ ARE STILL HERE -- what was lost is
only the label saying which arXiv version they were. That label is recoverable:
fetch each version in turn and compare sha256 until one matches.

This is a stronger retrofit than it sounds. The sha is the real pin; the version
number is the human-readable name for it. A card that carries the sha can be
re-verified even if arXiv were to replace a version in place.

WHAT IT WILL NOT DO.

It will not guess. If the blob is missing, or no version's bytes match it, the
card is left alone and reported. Writing "probably v3" onto a card would
reintroduce exactly the failure this exists to fix: a confident label that
nobody can check. A card left honestly unpinned is fine -- card_eval.py warns
the labeller when a card has no version, so the gap is visible at the one moment
it matters.

Cost: one API call plus up to N e-print fetches per card, at 3.1s each. For a
28-card KB that is a few minutes of mostly sleeping. Run it once.
"""

import argparse, hashlib, re, sys, time
import urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
KB = ROOT / "kb"
CACHE = ROOT / "ingest" / "cache" / "eprint"
EPRINT = "http://export.arxiv.org/e-print/"
ABS_API = "http://export.arxiv.org/api/query?id_list="
DELAY = 3.1
DOMAINS = ["stats", "probability", "compbio_methods", "compbio_mechanism", "math"]


def _ua():
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from arxiv_pull import UA
        return UA
    except ImportError:
        return "research-net/0.1"


def _get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": _ua()})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
            time.sleep(DELAY)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 1:
                sys.stderr.write("429 from arXiv; backing off 120s\n")
                time.sleep(120)
                continue
            return None
        except Exception:
            return None
    return None


def _latest_version(arxiv_id):
    xml = _get(ABS_API + arxiv_id, timeout=30)
    if not xml:
        return None
    m = re.search(rb"<id>\s*https?://arxiv\.org/abs/[^\s<]+?v(\d+)\s*</id>", xml)
    return int(m.group(1)) if m else None


def _cards(domain=None):
    out = []
    for dom in ([domain] if domain else DOMAINS):
        d = KB / dom / "cards"
        if d.is_dir():
            out.extend(sorted(d.glob("*.md")))
    return out


def _front_matter(text):
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    return parts[1] if len(parts) >= 3 else None


def _insert_pins(text, version, sha):
    """Insert the two keys at the end of the front matter, textually.

    Deliberately NOT a yaml.safe_load / yaml.dump round trip: these cards use
    block scalars and hand-wrapped prose throughout, and dumping would reflow
    every field in the file. A retrofit that rewrites 28 cards wholesale to add
    two lines is indistinguishable, in a diff, from a retrofit that broke them.
    """
    head, fm, body = text.split("---", 2)
    fm = fm.rstrip("\n")
    fm += f'\nsource_version: "{version}"\nsource_sha256: "{sha}"\n'
    return f"{head}---{fm}---{body}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--domain", choices=DOMAINS)
    ap.add_argument("--max-versions", type=int, default=8,
                    help="stop searching back past this many versions")
    a = ap.parse_args()

    cards = _cards(a.domain)
    if not cards:
        sys.exit("no cards found")

    pinned = skipped = no_blob = no_match = 0
    print(f"{len(cards)} cards\n")

    for path in cards:
        text = path.read_text()
        fm = _front_matter(text)
        if fm is None:
            print(f"  {path.name}  SKIP  no front matter")
            skipped += 1
            continue
        if re.search(r"^source_version:", fm, re.M):
            print(f"  {path.name}  skip  already pinned")
            skipped += 1
            continue

        aid = path.stem
        blob = CACHE / f"{aid.replace('/', '_')}.bin"
        if not (blob.exists() and blob.stat().st_size):
            print(f"  {path.name}  NO BLOB  cache miss -- cannot prove a version, "
                  f"left unpinned")
            no_blob += 1
            continue

        sha = hashlib.sha256(blob.read_bytes()).hexdigest()
        latest = _latest_version(aid)
        if not latest:
            print(f"  {path.name}  NO API  could not resolve versions")
            no_match += 1
            continue

        found = None
        for v in range(latest, max(0, latest - a.max_versions), -1):
            data = _get(EPRINT + f"{aid}v{v}")
            if data and hashlib.sha256(data).hexdigest() == sha:
                found = f"{aid}v{v}"
                break

        if not found:
            print(f"  {path.name}  NO MATCH  cached bytes match no version "
                  f"v{latest}..v{max(1, latest - a.max_versions + 1)} "
                  f"(arXiv may have replaced a version in place)")
            no_match += 1
            continue

        note = "" if not a.dry_run else "  (dry run, not written)"
        print(f"  {path.name}  -> {found}{note}")
        if not a.dry_run:
            path.write_text(_insert_pins(text, found, sha))
        pinned += 1

    print(f"\npinned {pinned} · already/skipped {skipped} · "
          f"no cached blob {no_blob} · unmatched {no_match}")
    if no_blob or no_match:
        print("\nCards left unpinned are not a failure -- they are the honest")
        print("state. card_eval.py warns the labeller on any card without a")
        print("version, which is the moment the gap actually costs something.")
    if pinned and not a.dry_run:
        print("\nRe-run validate_card.py over the touched domains: the two new")
        print("keys are optional in card_schema.json, but the insertion is")
        print("textual and a malformed card should fail loudly, not quietly.")


if __name__ == "__main__":
    main()
