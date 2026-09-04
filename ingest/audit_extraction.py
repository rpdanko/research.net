#!/usr/bin/env python3
"""What window did each card's curator actually get? Read-only, offline.

    python3 ingest/audit_extraction.py
    python3 ingest/audit_extraction.py --verbose    # per-card detail

Reproduces every figure quoted in `TODO.md` D0, `CARD-EVAL-HANDOFF.md` §5.2 and
`PROJECT-STATUS.md` §3. Exists because `PROJECT-STATUS.md` §6 item 5 says no
document may quote a metric without naming where it came from, and because the
last two attempts to correct a count in this repo were themselves wrong.

Runs in a few seconds and touches neither the network nor any file.

WHY IT DOES NOT CALL pdf_extract.extract()

  That would be the obvious implementation and it is wrong here, for the reason
  §5.1 spent a session learning. `extract()` resolves the arXiv version before
  fetching and keys the cache on the versioned id. Every blob in
  `ingest/cache/eprint/` is keyed on the BARE id -- all 33 of them, written
  before the 2026-08-28 pinning fix -- so on a machine with network every
  lookup misses, and `extract()` re-downloads all 28 e-prints. Three
  consequences, in increasing order of seriousness:

    - it takes minutes instead of seconds: `_resolve_version` and
      `_fetch_source` each sleep DELAY (3.1s), so ~6s of enforced idling per
      paper before any download
    - it writes new versioned cache entries, so the run is not read-only
    - it audits whatever arXiv serves TODAY, not the bytes the cards were built
      from -- which destroys the only question this script exists to answer

  So it reads the blob directly, by bare id, exactly as `show_eprint.py` does
  and for the same stated reason: that file is the authoritative record of what
  a curator read. Section matching then reuses `pdf_extract`'s own regexes and
  helpers, so the audit cannot drift from the extractor it is measuring.

  Duplicating four lines of `extract()`'s tail is deliberate. `extract()`
  answers "get me this paper"; this answers "what did the curator get from
  these bytes". Those are different questions and the version resolution is
  precisely where they part.

Works against `pdf_extract.py` before or after patch 1 -- `_sections` gained a
second return value there, and the shim below accepts either -- so you can run
it on both sides of the patch and compare.
"""

import argparse
import pathlib
import re
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Self-referential rather than ROOT / "ingest", so this keeps working wherever
# the file sits. Running `python3 ingest/audit_extraction.py` already puts this
# directory on sys.path; the insert only matters if it is ever imported.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

try:
    import yaml
except ImportError:
    sys.exit("needs pyyaml: see README.md's install line "
             "(agents cannot pip install -- settings.json denies it)")

import pdf_extract as px  # noqa: E402

CACHE = ROOT / "ingest" / "cache" / "eprint"
CLOSING_LIKE = re.compile(r"conclu|summar|final|remark|outlook|discuss|closing", re.I)


def cards():
    for p in sorted((ROOT / "kb").glob("*/cards/*.md")):
        fm = yaml.safe_load(p.read_text().split("---")[1])
        yield fm["arxiv_id"], fm


def window(aid):
    """The curator's window, rebuilt from the cached e-print. No network."""
    blob = CACHE / f"{aid.replace('/', '_')}.bin"
    if not blob.exists():
        return {"err": "no cached e-print (cannot be re-checked this way)"}
    data = blob.read_bytes()
    if not data:
        return {"err": "cached blob is empty"}
    tex, why = px._tex_from(data)
    if tex is None:
        return {"err": why}

    res = px._sections(tex)
    secs, docinfo = res if isinstance(res, tuple) else (res, {})

    out = {"docinfo": docinfo, "n_headings": len(secs)}
    for w in ("intro", "conclusion"):
        hit = px._pick(secs, w)
        if hit is None:
            heads = [h for h, _ in secs]
            out[w] = {"missing": True,
                      "unmatched_closing": [h for h in heads if CLOSING_LIKE.search(h)]}
        else:
            head, raw = hit
            text = px._strip(raw)
            out[w] = {"missing": False, "heading": head, "chars": len(text),
                      "truncated": len(text) > px.MAX_SECTION_CHARS,
                      "empty": len(text) < 40}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    patched = hasattr(px, "END_OF_BODY")
    t0 = time.monotonic()

    truncated, empty, unmatched, no_closing, no_source = [], [], [], [], []
    n = 0

    for aid, fm in cards():
        n += 1
        w = window(aid)
        if "err" in w:
            no_source.append((aid, w["err"][:45]))
            if a.verbose:
                print(f"{aid}  [{fm['domain']}]  {w['err']}")
            continue

        for which in ("intro", "conclusion"):
            d = w[which]
            if d["missing"]:
                if d["unmatched_closing"]:
                    unmatched.append((aid, which, d["unmatched_closing"]))
                elif which == "conclusion":
                    no_closing.append(aid)
            else:
                if d["truncated"]:
                    truncated.append((aid, which))
                if d["empty"]:
                    empty.append((aid, which))

        if a.verbose:
            def fmt(which):
                d = w[which]
                if d["missing"]:
                    extra = (f" -- UNMATCHED: {d['unmatched_closing']}"
                             if d["unmatched_closing"] else "")
                    return f"MISSING{extra}"
                return (f"{d['chars']:>6} chars  {d['heading'][:32]!r}"
                        + ("  TRUNCATED" if d["truncated"] else "")
                        + ("  EMPTY" if d["empty"] else ""))
            print(f"{aid}  [{fm['domain']:<17}] conf={str(fm.get('confidence')):<6} "
                  f"sections_read={','.join(fm.get('sections_read') or []) or 'NONE'}")
            print(f"    intro:      {fmt('intro')}")
            print(f"    conclusion: {fmt('conclusion')}")

    dt = time.monotonic() - t0
    print(f"\n{n} cards from {CACHE.relative_to(ROOT)} in {dt:.1f}s  "
          f"(pdf_extract.py: {'patched' if patched else 'UNPATCHED -- pre-patch-1'})\n")
    print(f"  sections truncated at MAX_SECTION_CHARS={px.MAX_SECTION_CHARS}"
          f"   {len(truncated)}  {[f'{i}/{w}' for i, w in truncated]}")
    print(f"  sections delivered EMPTY but reported found  {len(empty)}"
          f"  {[f'{i}/{w}' for i, w in empty]}")
    print(f"  closing section exists but was not matched   {len(unmatched)}"
          f"  {[i for i, _, _ in unmatched]}")
    print(f"  papers with genuinely no closing section     {len(no_closing)}")
    print(f"  no usable cached source                      {len(no_source)}"
          f"  {[i for i, _ in no_source]}")

    print("\nBefore patch 1 (2026-09-03) this read: 8 truncated, 1 empty,\n"
          "3 unmatched closing sections, plus 2 cards silently handed an\n"
          "appendix heading as their conclusion (2506.07459, 2605.29508) --\n"
          "six defective windows in total. After it: 0, 1, 0, 0. The one\n"
          "remaining EMPTY is 2411.02771's intro, which needs level-aware\n"
          "SECTION_RE and is deliberately still open -- see TODO.md D0.")
    print("\nNote what this does NOT catch: a wrong pick that still returns\n"
          "plausible text. 2605.29508's 563-char appendix subsection counted as\n"
          "a delivered conclusion here and had to be found by reading. The\n"
          "columns above are a floor on the defect count, not a ceiling.")


if __name__ == "__main__":
    main()
