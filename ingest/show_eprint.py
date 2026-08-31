#!/usr/bin/env python3
"""Read the cached e-print a curator actually parsed. The missing view.

    show_eprint.py 2506.07459 --list              # what's in the archive
    show_eprint.py 2506.07459 --grep ddG -C 6     # find a definition
    show_eprint.py 2506.07459 --grep "\\\\Delta\\\\Delta G" -C 8
    show_eprint.py 2506.07459 --file main.tex     # dump one member
    show_eprint.py 2506.07459 > /tmp/pz.tex       # dump all .tex

WHY THIS EXISTS.

`ingest/cache/eprint/<id>.bin` is the authoritative record of what a curator
read -- pdf_extract.py fetched those bytes and built the card from them. It is
also, until now, the one artifact in this repo that nothing could display: it is
a gzipped tar, so `grep` on it returns coincidental byte matches rather than
text. (Searching 2506.07459.bin for `ddG` reports 7 hits; searching it for
`ESMFold`, which appears dozens of times in that paper, reports 0. Every count
off the raw blob is noise.)

That gap has a cost, and 2506.07459 is the case that showed it. `card_eval.py
label` displays the abstract from papers.sqlite. That abstract is NOT
necessarily the version the e-print came from -- on both cards checked so far
(2606.07914, 2506.07459) the stored abstract differs materially from arXiv's v1
HTML. So at the moment of judgment the labeller sees neither what the curator
read nor what they would fetch to check it, and a card can be scored 'n' for
inventing a phrase that is sitting in the source on disk.

Use this whenever a verdict turns on whether the paper says something. Absence
in a fetched HTML is not absence in the paper; absence HERE is much closer to
it, because these are the bytes the card was built from.

FORMATS. arXiv e-prints arrive as gzipped tar (usual), a single gzipped file
(short papers), or PDF (when no source was submitted). All three are handled;
PDFs are reported rather than parsed, since pdf_extract.py already does that.
"""

import argparse, gzip, io, re, sys, tarfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
CACHE = ROOT / "ingest" / "cache" / "eprint"

TEXTY = (".tex", ".txt", ".bbl", ".bib", ".cls", ".sty")


def _load(arxiv_id):
    """Return [(name, text)] for the readable members of the cached blob."""
    blob = CACHE / f"{arxiv_id.replace('/', '_')}.bin"
    if not blob.exists():
        sys.exit(f"no cached e-print at {blob.relative_to(ROOT)}\n"
                 f"  (pdf_extract.py caches on first extract; a card whose blob "
                 f"is gone cannot be re-checked this way)")
    raw = blob.read_bytes()
    if not raw:
        sys.exit("cached blob is empty")

    if raw[:4] == b"%PDF":
        sys.exit("this blob is a PDF, not LaTeX source -- arXiv had no source "
                 "submission.\n  Use pdf_extract.py, which already parses it.")

    if raw[:2] == b"\x1f\x8b":
        try:
            raw = gzip.decompress(raw)
        except OSError as e:
            sys.exit(f"gzip header but decompression failed: {e}")

    # tar or a single file?
    try:
        tf = tarfile.open(fileobj=io.BytesIO(raw))
    except tarfile.TarError:
        return [("(single file)", raw.decode("utf-8", "replace"))]

    out = []
    for m in tf.getmembers():
        if not m.isfile():
            continue
        data = tf.extractfile(m).read()
        if m.name.lower().endswith(TEXTY):
            out.append((m.name, data.decode("utf-8", "replace")))
        else:
            out.append((m.name, None))          # binary member, name only
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arxiv_id")
    ap.add_argument("--list", action="store_true", help="list archive members")
    ap.add_argument("--file", help="dump only this member")
    ap.add_argument("--grep", help="regex; prints matching lines with context")
    ap.add_argument("-C", "--context", type=int, default=3)
    ap.add_argument("-i", "--ignore-case", action="store_true", default=True)
    a = ap.parse_args()

    members = _load(a.arxiv_id)

    if a.list:
        for name, text in members:
            kind = f"{len(text):>8} chars" if text is not None else "  (binary)"
            print(f"  {kind}  {name}")
        return

    picked = [(n, t) for n, t in members
              if t is not None and (not a.file or n == a.file)]
    if not picked:
        sys.exit(f"no readable text members"
                 f"{f' named {a.file}' if a.file else ''} -- try --list")

    if not a.grep:
        for name, text in picked:
            print(f"\n===== {name} " + "=" * max(0, 66 - len(name)))
            print(text)
        return

    flags = re.I if a.ignore_case else 0
    rx = re.compile(a.grep, flags)
    hits = 0
    for name, text in picked:
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if not rx.search(line):
                continue
            hits += 1
            lo, hi = max(0, i - a.context), min(len(lines), i + a.context + 1)
            print(f"\n--- {name}:{i+1}")
            for j in range(lo, hi):
                mark = ">>" if j == i else "  "
                print(f"{mark} {lines[j]}")
    print(f"\n{hits} match(es)."
          + ("\n  Nothing found. In LaTeX a phrase is often split across lines "
             "or\n  broken by macros -- search a single distinctive word before "
             "concluding\n  the paper does not say it." if not hits else ""))


if __name__ == "__main__":
    main()
