#!/usr/bin/env python3
"""Abstract, introduction and conclusion for one paper. Never the whole thing.

    pdf_extract.py 2608.01234
    pdf_extract.py 2608.01234 --sections abstract,intro,conclusion
    pdf_extract.py 2608.01234 --json

Called by every curator agent as step 1. The section list is not a convenience
flag -- it is the enforcement point for the rule each curator prompt states
("This is the only text you get. Do not request the full PDF."). There is
deliberately no code path in this file that returns a whole document, so the
rule holds even if a curator asks for one.

WHY LATEX SOURCE AND NOT THE PDF
arXiv serves the author's source at /e-print/<id>, and for almost every paper
that is a LaTeX tarball. Sectioning in LaTeX is explicit -- \\section{Introduction}
is a boundary, unambiguously -- while sectioning in extracted PDF text has to be
guessed from font size and whitespace, which fails on exactly the two-column
theory papers this repo reads most. Source parsing is also stdlib-only
(urllib, tarfile, gzip, re), so it adds nothing to the dependency line in
README.md. The PDF path exists below as a fallback and needs a library you
probably do not have installed; if it fires often, that is worth knowing.

THE ABSTRACT NEVER COSTS A REQUEST
It is already in papers.sqlite, harvested by arxiv_pull.py. Curators asking only
for the abstract -- which is the common case for a paper that turns out thin --
should not cause a network round trip, and with --sections abstract they do not.

MISSING IS REPORTED, NOT SILENTLY DROPPED
Every curator prompt says: if a card cannot be written without the missing
section, write it with `confidence: low` and note what was missing, do not
escalate. That instruction only works if the curator can tell the difference
between "this paper has no conclusion section" and "extraction failed". So a
section that could not be found is printed as an explicit
`## conclusion — NOT FOUND (<why>)` block rather than omitted. An omitted
section looks like a paper without one, and the resulting card would claim
low confidence for the wrong reason.

CACHING IS NOT AN OPTIMISATION
Curators retry: validate_card.py rejects a card, the agent fixes it and re-reads
the source. arXiv's rate limit is one request per three seconds and 429s have
been aggressive since early 2026 (see arxiv_pull.py). Without a cache, a curator
loop over ten papers with two retries each is sixty seconds of sleeping and
thirty chances to get banned. Sources land in ingest/cache/eprint/ and are
reused forever -- an arXiv VERSION is immutable, so there is no staleness
question.

THE VERSION IS IMMUTABLE. THE BARE ID IS NOT, AND THAT USED TO BE A BUG HERE.
    Until 2026-08-28 this script fetched EPRINT + arxiv_id with no version
    suffix, which arXiv resolves to whatever is latest AT FETCH TIME, and cached
    it under the bare id. So the paragraph above was asserting a property the
    code did not secure: two extractions of "2407.01051" months apart could
    return different papers, the cache would serve whichever arrived first, and
    nothing recorded which one a card was built from.

    That is not hypothetical. Card 2407.01051 was checked by hand against the v1
    HTML and appeared to claim a numerical-experiments section that did not
    exist -- it exists in v3. The card was right and the check was wrong, and
    there was no way to tell from the card which of them was looking at the
    paper the curator actually read.

    Now: the version is resolved at extract time, the versioned id is what gets
    fetched, the cache key carries it, and both the version and a sha256 of the
    exact bytes are returned so they can be written onto the card. A card that
    records these can be re-verified against the text it was really made from.
    Same reasoning as verify_prereg.py's mtime+hash check, for the same reason:
    a claim you cannot re-check later is a claim you are taking on trust.
"""

import argparse, gzip, hashlib, io, json, re, sqlite3, sys, tarfile, time
import urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
DB = ROOT / "ingest" / "papers.sqlite"
CACHE = ROOT / "ingest" / "cache" / "eprint"
EPRINT = "http://export.arxiv.org/e-print/"
ABS_API = "http://export.arxiv.org/api/query?id_list="

DELAY = 3.1                 # matches arxiv_pull.py; do not lower
MAX_SECTION_CHARS = 8000    # per section, after cleaning
ALL_SECTIONS = ("abstract", "intro", "conclusion")

# Deliberately generous on the conclusion side. A theory paper may close with
# "Discussion", "Concluding remarks", "Summary and outlook" or nothing at all,
# and a curator reading a missing conclusion writes a worse card than one
# reading a section called Discussion.
HEADINGS = {
    "intro": re.compile(r"^\s*(\d+[.\s]*)?introduction\b", re.I),
    "conclusion": re.compile(
        r"^\s*(\d+[.\s]*)?(conclusion|concluding\s+remarks|discussion"
        r"|summary\s+and\s+(outlook|discussion|conclusion)|outlook)\b", re.I),
}

SECTION_RE = re.compile(
    r"\\(?:sub)?section\*?\s*\{((?:[^{}]|\{[^{}]*\})*)\}", re.S)


# ------------------------------------------------------------------ metadata

def _from_db(arxiv_id):
    if not DB.exists():
        return None
    con = sqlite3.connect(DB)
    row = con.execute(
        "SELECT title, abstract, categories FROM papers WHERE arxiv_id=? "
        "OR arxiv_id LIKE ?", (arxiv_id, arxiv_id.split("v")[0] + "%")).fetchone()
    return {"title": row[0], "abstract": row[1], "categories": row[2]} if row else None


# --------------------------------------------------------------- source pull

def _ua():
    """Reuse arxiv_pull's contact string rather than inventing a second one --
    anonymous callers are rate-limited harder, and two different user agents
    from one project is the kind of thing that gets both of them throttled."""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from arxiv_pull import UA
        if "YOUR_EMAIL_HERE" in UA:
            print("warning: arxiv_pull.UA still has the placeholder address. "
                  "arXiv rate-limits\n         anonymous callers harder; set a "
                  "real mailto before a full run.", file=sys.stderr)
        return UA
    except ImportError:
        return "research-net/0.1"


def _resolve_version(arxiv_id):
    """Bare id -> versioned id ('2407.01051' -> '2407.01051v3'), or None.

    One extra API call per extraction. That is cheap next to what follows it --
    the e-print fetch plus full-text parsing -- and it is the difference between
    a card that can be re-verified and one that cannot.

    Returns None rather than raising if arXiv is unreachable or the response is
    unparseable: an unpinned extraction is worse than a pinned one but far
    better than no card, and the caller records the null so the gap is visible
    on the card rather than silently absent.
    """
    if re.search(r"v\d+$", arxiv_id):
        return arxiv_id                      # already pinned by the caller
    try:
        req = urllib.request.Request(ABS_API + arxiv_id,
                                      headers={"User-Agent": _ua()})
        with urllib.request.urlopen(req, timeout=30) as r:
            xml = r.read().decode("utf-8", "replace")
        time.sleep(DELAY)
    except Exception as e:
        print(f"warning: could not resolve version for {arxiv_id} ({e}); "
              f"fetching the bare id, which is whatever arXiv serves today.",
              file=sys.stderr)
        return None
    m = re.search(r"<id>\s*https?://arxiv\.org/abs/([^\s<]+?v\d+)\s*</id>", xml)
    if not m:
        print(f"warning: no versioned id in the API response for {arxiv_id}.",
              file=sys.stderr)
        return None
    return m.group(1)


def _fetch_source(arxiv_id, refresh=False):
    """Returns raw bytes of the e-print, cached. None if arXiv has no source.

    `arxiv_id` should already carry its version when the caller could resolve
    one -- the cache key is only immutable if the id is.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    blob = CACHE / f"{arxiv_id.replace('/', '_')}.bin"
    if blob.exists() and blob.stat().st_size and not refresh:
        return blob.read_bytes()

    req = urllib.request.Request(EPRINT + arxiv_id, headers={"User-Agent": _ua()})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            time.sleep(DELAY)
            blob.write_bytes(data)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 1:
                sys.stderr.write("429 from arXiv; backing off 120s\n")
                time.sleep(120)
                continue
            if e.code in (403, 404):
                return None          # withdrawn, or PDF-only submission
            raise
    return None


def _tex_from(data):
    """Pull the main .tex out of whatever arXiv returned.

    Three shapes in practice: a gzipped tar of many files, a single gzipped
    .tex, or (rarely) a bare PDF. The main file is the one that declares the
    document; concatenating every .tex would fold appendices and supplementary
    material into the body and defeat the point of this script.
    """
    if data[:4] == b"%PDF":
        return None, "arXiv has no LaTeX source, only a PDF"

    texts = {}
    try:
        with tarfile.open(fileobj=io.BytesIO(data)) as tf:
            for m in tf.getmembers():
                if m.isfile() and m.name.lower().endswith((".tex", ".ltx")):
                    f = tf.extractfile(m)
                    if f:
                        texts[m.name] = f.read().decode("utf-8", "replace")
    except (tarfile.TarError, EOFError):
        try:
            texts["main.tex"] = gzip.decompress(data).decode("utf-8", "replace")
        except OSError:
            try:
                texts["main.tex"] = data.decode("utf-8", "replace")
            except Exception:
                return None, "source is neither tar, gzip, nor text"

    if not texts:
        return None, "source archive contains no .tex file"

    for name, body in texts.items():
        if "\\begin{document}" in body:
            # \input/\include split the body across files. Splice them in so a
            # paper whose introduction lives in intro.tex is not reported
            # missing -- that pattern is common in collaborations.
            def splice(m):
                stem = m.group(1).strip()
                for cand in (stem, stem + ".tex", stem.lstrip("./") + ".tex"):
                    for k, v in texts.items():
                        if k == cand or k.endswith("/" + cand):
                            return v
                return ""
            return re.sub(r"\\(?:input|include)\s*\{([^}]+)\}", splice, body), None

    return max(texts.values(), key=len), None


# ------------------------------------------------------------------ cleaning

def _strip(tex):
    """Light. Enough that a curator reads prose instead of markup, not so much
    that the mathematics goes -- `mathematical_objects` is the field the whole
    knowledge base is built from, and it is often named only inside math mode."""
    tex = re.sub(r"(?<!\\)%.*", "", tex)                      # comments
    tex = re.sub(r"\\(label|ref|eqref|cite[a-z]*)\s*\{[^}]*\}", " ", tex)
    tex = re.sub(r"\\begin\{(figure|table)\*?\}.*?\\end\{\1\*?\}", " ",
                 tex, flags=re.S)
    tex = re.sub(r"\\(emph|textit|textbf|texttt|mathrm|text)\s*\{([^{}]*)\}",
                 r"\2", tex)
    tex = re.sub(r"\\(newpage|clearpage|noindent|par|hfill|vspace\*?\{[^}]*\})",
                 " ", tex)
    tex = re.sub(r"[ \t]+", " ", tex)
    return re.sub(r"\n{3,}", "\n\n", tex).strip()


def _sections(tex):
    """[(heading, body)] in document order, from \\begin{document} onward."""
    start = tex.find("\\begin{document}")
    body = tex[start:] if start >= 0 else tex
    marks = [(m.start(), m.end(), m.group(1)) for m in SECTION_RE.finditer(body)]
    out = []
    for i, (s, e, head) in enumerate(marks):
        stop = marks[i + 1][0] if i + 1 < len(marks) else len(body)
        out.append((re.sub(r"\\[a-zA-Z]+", "", head).strip(), body[e:stop]))
    return out


def _pick(sections, which):
    pat = HEADINGS[which]
    hits = [(h, b) for h, b in sections if pat.match(h)]
    if not hits:
        return None
    # Last match for conclusions (a paper that says "Discussion" mid-body and
    # "Conclusion" at the end should give you the second), first for intros.
    return hits[-1] if which == "conclusion" else hits[0]


def _abstract_from_tex(tex):
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S)
    return _strip(m.group(1)) if m else None


# -------------------------------------------------------------------- driver

def extract(arxiv_id, wanted, refresh=False):
    meta = _from_db(arxiv_id)
    out = {"arxiv_id": arxiv_id,
           "title": (meta or {}).get("title"),
           "categories": (meta or {}).get("categories"),
           "source_version": None, "source_sha256": None,
           "sections": {}, "missing": {}}

    if "abstract" in wanted:
        if meta and meta.get("abstract"):
            out["sections"]["abstract"] = meta["abstract"]
        else:
            out["missing"]["abstract"] = "no row in papers.sqlite"

    need_source = [w for w in wanted if w in HEADINGS]
    if not need_source:
        return out          # abstract only: no network, no cache, done

    # Pin the version BEFORE fetching, so the bytes and the cache key both refer
    # to something immutable. See the version note in this module's docstring.
    versioned = _resolve_version(arxiv_id)
    out["source_version"] = versioned
    data = _fetch_source(versioned or arxiv_id, refresh)
    if data is None:
        for w in need_source:
            out["missing"][w] = "arXiv returned no e-print (withdrawn, or PDF-only)"
        return out
    out["source_sha256"] = hashlib.sha256(data).hexdigest()

    tex, why = _tex_from(data)
    if tex is None:
        for w in need_source:
            out["missing"][w] = why
        return out

    if "abstract" in wanted and "abstract" in out["missing"]:
        alt = _abstract_from_tex(tex)
        if alt:
            out["sections"]["abstract"] = alt
            del out["missing"]["abstract"]

    sections = _sections(tex)
    if not sections:
        for w in need_source:
            out["missing"][w] = "no \\section commands found in source"
        return out

    for w in need_source:
        hit = _pick(sections, w)
        if hit is None:
            out["missing"][w] = (
                f"no section heading matched; document has: "
                f"{', '.join(h for h, _ in sections[:8])}")
            continue
        head, raw = hit
        text = _strip(raw)
        if len(text) > MAX_SECTION_CHARS:
            text = text[:MAX_SECTION_CHARS] + \
                f"\n\n[truncated at {MAX_SECTION_CHARS} chars]"
        out["sections"][w] = text
        out.setdefault("headings", {})[w] = head
    return out


def render(res):
    lines = [f"# {res['arxiv_id']}"]
    if res.get("title"):
        lines.append(f"**{res['title']}**")
    if res.get("categories"):
        lines.append(f"`{res['categories']}`")

    # The pin, stated where the curator cannot miss it. These two values go
    # straight onto the card as source_version and source_sha256; without them
    # nobody re-checking the card later can tell which version it was made from,
    # and a correct card looks like a fabricated one against the wrong version.
    if res.get("source_version"):
        lines.append("")
        lines.append(f"**Source version: `{res['source_version']}`** — copy this "
                     f"to the card's `source_version`.")
        if res.get("source_sha256"):
            lines.append(f"**Source sha256: `{res['source_sha256']}`** — copy this "
                         f"to `source_sha256`.")
    elif res.get("sections"):
        lines.append("")
        lines.append("**Source version: UNRESOLVED.** arXiv did not return a "
                     "versioned id, so this text is whatever was latest today "
                     "and cannot be pinned. Set the card's `source_version` to "
                     "`unresolved` rather than guessing, and say so in "
                     "`limitations`.")
    lines.append("")
    for name in ALL_SECTIONS:
        if name in res["sections"]:
            head = (res.get("headings") or {}).get(name)
            lines.append(f"## {name}" + (f" — {head}" if head else ""))
            lines.append("")
            lines.append(res["sections"][name])
            lines.append("")
        elif name in res["missing"]:
            lines.append(f"## {name} — NOT FOUND ({res['missing'][name]})")
            lines.append("")
    if res["missing"]:
        lines.append("---")
        lines.append(
            "One or more sections are missing above. Per your curator prompt: "
            "if the card\ncannot be written without them, write it with "
            "`confidence: low` and say in\n`limitations` what was missing. Do "
            "not escalate and do not request the full PDF.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arxiv_id")
    ap.add_argument("--sections", default=",".join(ALL_SECTIONS),
                    help="comma-separated subset of abstract,intro,conclusion")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--refresh", action="store_true",
                    help="ignore the cached e-print and re-fetch")
    a = ap.parse_args()

    wanted = [s.strip() for s in a.sections.split(",") if s.strip()]
    bad = [w for w in wanted if w not in ALL_SECTIONS]
    if bad:
        sys.exit(f"unknown section(s) {bad}. This script returns "
                 f"{ALL_SECTIONS} and nothing else -- there is no option for "
                 f"the full text, on purpose.")

    res = extract(a.arxiv_id, wanted, a.refresh)
    print(json.dumps(res, indent=2) if a.json else render(res))

    # Non-zero when nothing at all came back, so a curator loop can tell an
    # empty result from a quiet one. Partial success stays zero: a paper with
    # an abstract and no conclusion is a card worth writing at low confidence.
    if not res["sections"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
