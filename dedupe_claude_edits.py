#!/usr/bin/env python3
"""One-time cleanup: collapse the triage.md / daily-ingest SKILL.md paragraphs
that got pasted in three times (a shell-paste re-submission, not a content
problem). Idempotent -- safe to run again, it will just report 0 removed."""

from pathlib import Path

FIXES = [
    (
        ".claude/agents/triage.md",
        "**Where an exemplar's strike reason contradicts the charter, the charter "
        "governs.** Exemplars are frozen at the time of vetting and predate charter "
        "revisions; the charter is the current specification. If you reject a paper "
        "on a near-miss resemblance, check that the charter still excludes it.",
    ),
    (
        ".claude/skills/daily-ingest/SKILL.md",
        "It also does not catch a paper that is useful to how this project itself "
        "operates — agent-design prior art, background reference material — rather "
        "than an object of study for any domain charter. That paper is correctly "
        "rejected by triage and then genuinely lost; a rejection isn't retrievable "
        "later. No automated tag catches this on purpose (see "
        "`dev-notes/parking-lot.md`) — if you notice one while reading the digest, "
        "add it there yourself.",
    ),
]

for relpath, para in FIXES:
    p = Path(relpath)
    if not p.exists():
        print(f"SKIP {relpath}: not found from this working directory")
        continue
    text = p.read_text()
    block = para + "\n\n"
    n = text.count(block)
    if n == 0:
        print(f"OK   {relpath}: paragraph absent, nothing to do")
        continue
    if n == 1:
        print(f"OK   {relpath}: exactly one copy already, nothing to do")
        continue
    text = text.replace(block, "", n)  # strip every copy
    # Reinsert exactly one, right where the original edit placed it.
    if relpath.endswith("triage.md"):
        anchor = ("Neither block is a whitelist. A paper unlike all 25 exemplars "
                  "can still be a 5 — see the wildcard note below.\n")
    else:
        anchor = ("No synthesis, no bridges, no proposals. If today's papers look "
                  "interesting, that is not actionable here — the weekly run sees "
                  "them in context, which is the only place an intersection is "
                  "visible.\n")
    assert anchor in text, f"{relpath}: anchor line missing, aborting -- nothing written"
    text = text.replace(anchor, anchor + "\n" + block, 1)
    p.write_text(text)
    print(f"FIXED {relpath}: {n} copies -> 1")
