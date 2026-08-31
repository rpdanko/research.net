#!/usr/bin/env python3
"""Eval harness for the curators. The thing that makes card extraction measurable.

    card_eval.py sample --n 20                 # draw cards for hand-checking
    card_eval.py sample --n 10 --domain stats  # or restrict to one domain
    card_eval.py sample --n 10 --append        # add more without losing existing judgments
    card_eval.py import drafts/2606.07914.json # load a drafted judgment
    card_eval.py label                         # your judgment, per field
    card_eval.py score                         # curator vs. you
    card_eval.py diff                          # did the last schema/prompt edit help

WHO IS ALLOWED TO LABEL, AND WHAT THE NUMBER MEANS IF IT IS NOT YOU.

  README.md puts card_labels.jsonl among the files in your handwriting, for the
  reason invariant 15 gives: the whole system is one model's judgment, and an
  eval scored by another instance of that model measures agreement, not
  accuracy. Shared training produces shared blind spots, and they are invisible
  in exactly the place they matter -- `conceptual-math`, which ERROR-TYPES.md
  calls "where this system's whole premise sits."

  `import` exists anyway, because the alternative in practice is that the
  measurement does not happen at all on the domains where you cannot referee
  the mathematics unaided. It is a compromise and it is instrumented as one:

    - it writes to `drafted`, never to `judgments`
    - every drafted verdict carries a reason, shown at the prompt
    - accepting still requires you at the keyboard, card by card
    - overrides are recorded, and score() prints the split and complains
      loudly if a whole run went by without a single disagreement

  Read the drafts adversarially, and spot-check two or three cards a batch
  against the actual papers. That is the same coverage verify_citations.py
  settles for, for the same reason: resolution proves existence, not relevance.

`validate_card.py` checks that a card is WELL-FORMED. It cannot check that the
extraction is CORRECT. This file does, the same way eval_triage.py checks triage
instead of trusting it, and README.md sec"Card accuracy" asks for it at the start
of Weeks 2-3 -- before the hand-check step, "otherwise 'the schema needs
revising' is an impression."

SCORE ON EQUIVALENCE, NOT STRING MATCH.

  A curator that writes "optimal transport" for a paper that says "Sinkhorn
  divergence" is CORRECT. So is "Wright-Fisher diffusion" for a paper that
  writes the generator without naming it -- that is the system working as
  designed, not a miss. Exact-match scoring badly undercounts correct-but-
  reworded extraction (the LLM-NERRE manual-scoring table is the reference
  README.md cites), and `mathematical_objects` is the field it bites hardest,
  because canonical-name normalization is exactly what sec4 of every charter
  asks the curator to do.

  The question for every field is: WOULD A READER OF THIS CARD BE MISLED?
  Not: is this how I would have phrased it.

WHY `mathematical_objects` GETS ITS OWN TREATMENT.

  Every other field is prose a human reads. This one is the load-bearing field
  -- the concordance is built from it, `math-scout` clusters it, and
  `bridge-finder` proposes intersections from those clusters. A wrong object
  does not just make one card worse; it puts a false node in the graph that
  everything downstream reasons over. So it is scored per OBJECT, with both
  halves measured: objects the curator listed that are not really there
  (precision), and objects that are there and the curator missed (recall).

  `named_in_paper: false` claims are scored separately again, and deliberately.
  They are the highest-value output in the system -- recovering unnamed
  mathematics from biological or applied vocabulary is what compbio_mechanism
  exists for -- and they are the least checkable, because there is no string in
  the paper to point at. Invariant 15 makes the same point from the other side:
  verify a planted user object exactly as you verify a curator's
  named_in_paper: false. An unnamed-object precision that is materially worse
  than the named one is the single most actionable number this script produces.

ERROR TYPES, AND ONE DELIBERATE DIVERGENCE FROM ERROR-TYPES.md.

  Each card takes a free-text note and any number of tags from
  rubrics/ERROR-TYPES.md, which already names this script as a consumer. The
  vocabulary is read out of that file at run time rather than duplicated here,
  so adding a type to the markdown is the only step required. Invariant 19's
  reasoning is the entire justification: you cannot count free text. One note on
  one card is an anecdote; the same tag on six cards is a curator-prompt change
  with a number attached.

  THE DIVERGENCE: ERROR-TYPES.md says one tag per rejection, and states that
  mutual exclusion "is what keeps counts meaningful." This script allows several
  per card, because a card is not one judgment -- it is six fields plus an
  object list, and two fields can fail in genuinely different ways. Recorded
  here as a decision rather than left as an accident.

  If the counts start looking muddy, the cleaner fix is tags per FIELD rather
  than per card: that restores mutual exclusion inside each judgment without
  pretending a whole card has a single error. It costs one more prompt per
  field, which is why it is not the default yet.
"""

import argparse, json, random, re, sqlite3, sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
KB = ROOT / "kb"
EVAL = ROOT / "eval"
LABELS = EVAL / "card_labels.jsonl"
RUNS = EVAL / "card_runs"
DB = ROOT / "ingest" / "papers.sqlite"

DOMAINS = ["stats", "probability", "compbio_methods", "compbio_mechanism", "math"]

# The prose fields worth sitting through. Deliberately not every field in the
# schema: 20 cards x every field is ~200 judgments and nobody finishes that, and
# a measurement you abandon halfway is worth less than a smaller one you finish.
# `date`/`domain`/`arxiv_id` are structural and validate_card.py already covers
# them; `sections_read` is provenance, not extraction; `confidence` is not judged
# at all but is used in score() to check whether the curator's self-assessment
# predicts anything.
DEFAULT_FIELDS = ["problem", "setting", "method", "contribution",
                  "mathematical_objects", "limitations"]

VERDICTS = {
    "y": "correct -- equivalent to what the paper says, however worded",
    "p": "partial -- not wrong, but thin, vague, or missing something load-bearing",
    "n": "wrong -- asserts something the paper does not support",
}

ERROR_TYPES_MD = ROOT / "rubrics" / "ERROR-TYPES.md"


def _error_types():
    """The tag vocabulary, read from rubrics/ERROR-TYPES.md rather than defined
    here.

    That file already lists card_eval.py among its consumers, and it is the
    user's handwriting -- duplicating the list in code would give the repo two
    vocabularies that drift apart, which is the failure this whole file exists
    to measure in the cards. Parsed from the table rows so that adding a type to
    the markdown is the only step needed; invariant 19 expects the vocabulary to
    grow from real rejections.
    """
    if not ERROR_TYPES_MD.exists():
        print(f"warning: {ERROR_TYPES_MD.relative_to(ROOT)} not found -- "
              f"tagging disabled, notes still recorded.", file=sys.stderr)
        return []
    tags, seen = [], set()
    for line in ERROR_TYPES_MD.read_text().splitlines():
        m = re.match(r"^\|\s*`([a-z][a-z0-9-]+)`\s*\|", line)
        if m and m.group(1) not in seen:
            seen.add(m.group(1))
            tags.append(m.group(1))
    return tags


# ------------------------------------------------------------------- loading

def _load_cards(domain=None):
    """Read the card FILES, not kb/<domain>/index.jsonl.

    The index is generated by rebuild_index.py and is what agents read, but it
    can lag the cards on disk, and an eval that silently scores a stale copy of
    the thing it is measuring is worse than no eval. The cards are the artifact
    the curator actually produced. (This is the same failure this project has
    already hit repeatedly in its own documents -- a number written down once
    and never re-derived.)
    """
    try:
        import yaml
    except ImportError:
        sys.exit("pip install pyyaml")

    out = []
    for dom in ([domain] if domain else DOMAINS):
        cards_dir = KB / dom / "cards"
        if not cards_dir.is_dir():
            continue
        for path in sorted(cards_dir.glob("*.md")):
            text = path.read_text()
            if not text.startswith("---"):
                print(f"warning: {path.relative_to(ROOT)} has no front matter, skipped",
                      file=sys.stderr)
                continue
            _, fm, _ = text.split("---", 2)
            try:
                card = yaml.safe_load(fm)
            except yaml.YAMLError as e:
                print(f"warning: {path.relative_to(ROOT)} front matter unparseable "
                      f"({e}), skipped", file=sys.stderr)
                continue
            card["_path"] = str(path.relative_to(ROOT))
            card["_domain_dir"] = dom
            out.append(card)
    return out


def _abstracts(arxiv_ids):
    """Pull abstracts from papers.sqlite so `label` can show you the source next
    to the card. Without this you would be judging the card against your memory
    of the paper, which is the failure mode the card is supposed to prevent."""
    if not DB.exists():
        return {}
    con = sqlite3.connect(DB)
    out = {}
    for aid in arxiv_ids:
        row = con.execute(
            "select title, abstract from papers where arxiv_id = ?", (aid,)).fetchone()
        if row:
            out[aid] = {"title": row[0], "abstract": row[1]}
    con.close()
    return out


# ------------------------------------------------------------------- sample

def sample(n, domain=None, append=False, fields=None):
    EVAL.mkdir(exist_ok=True)
    fields = fields or DEFAULT_FIELDS

    existing, seen = [], set()
    if append and LABELS.exists():
        existing = [json.loads(l) for l in LABELS.read_text().splitlines() if l.strip()]
        seen = {r["arxiv_id"] for r in existing}
        done = sum(1 for r in existing if _is_judged(r))
        print(f"append mode: keeping {len(existing)} existing rows ({done} judged), "
              f"excluding their arxiv_ids from the new draw.")
    elif append:
        print("append mode: no existing card_labels.jsonl, behaving like a fresh sample.")

    cards = [c for c in _load_cards(domain) if c["arxiv_id"] not in seen]
    if not cards:
        sys.exit(f"no cards found{f' for {domain}' if domain else ''} "
                 f"(after excluding {len(seen)} already sampled)")

    if len(cards) < n:
        print(f"\nNOTE: asked for {n}, only {len(cards)} cards available"
              f"{f' in {domain}' if domain else ''}. Taking all of them.")
        if domain:
            print("  Per-domain card counts are uneven -- `stats` in particular is")
            print("  thin. A per-domain number off 3 cards is not a number. Consider")
            print("  pooling across domains instead, or drawing from a larger one.\n")
        n = len(cards)

    picks = random.sample(cards, n)

    # Shuffle before writing, ALWAYS. eval_triage.py's sample() shuffled within
    # each band but emitted stratum-blocks, so labelling arrived in same-band
    # streaks and invited anchoring against neighbours rather than the scale.
    # random.sample already returns in arbitrary order; this is here so that any
    # future grouping added above (by domain, by confidence, by date) cannot
    # reintroduce the bug silently. See OPEN-QUESTIONS.md sec1.6.
    random.shuffle(picks)

    src = _abstracts([c["arxiv_id"] for c in picks])
    if not src:
        print("warning: no abstracts available from papers.sqlite -- you will be "
              "judging cards without the source in front of you.", file=sys.stderr)

    new = []
    for c in picks:
        objs = c.get("mathematical_objects") or []
        new.append({
            "arxiv_id": c["arxiv_id"],
            "title": c.get("title", ""),
            "domain": c.get("domain") or c["_domain_dir"],
            "path": c["_path"],
            "confidence": c.get("confidence"),
            "source_version": c.get("source_version"),
            "sections_read": c.get("sections_read") or [],
            "abstract": (src.get(c["arxiv_id"], {}).get("abstract") or "")[:8000],
            "card": {f: c.get(f) for f in fields},
            "fields": fields,
            # per-field verdicts, filled in by label()
            "judgments": {f: None for f in fields},
            # mathematical_objects detail, filled in by label()
            "objects": [{"name": o.get("name"),
                          "named_in_paper": o.get("named_in_paper", True),
                          "verdict": None} for o in objs],
            "objects_missed": None,
            "notes": None,
            "error_types": [],
            # WHO judged this card. None until labelled. See import_draft().
            # score() refuses to print a headline number without this split,
            # because "curator vs. you" and "curator vs. another model" are
            # different measurements and only one of them is the eval README.md
            # asked for.
            "labeller": None,
            # A drafted judgment, if one was imported. Kept even after you
            # override it, so disagreements stay recoverable -- that record is
            # the only evidence of whether the drafts were trustworthy.
            "drafted": None,
        })

    all_recs = existing + new
    with LABELS.open("w") as f:
        for r in all_recs:
            f.write(json.dumps(r) + "\n")

    by_dom = defaultdict(int)
    for r in new:
        by_dom[r["domain"]] += 1
    print(f"\nwrote {LABELS.relative_to(ROOT)} ({len(new)} new"
          f"{f', {len(all_recs)} total' if existing else ''})")
    print("  by domain: " + ", ".join(f"{d}={n}" for d, n in sorted(by_dom.items())))
    print(f"  fields to judge: {', '.join(fields)}")
    print("\nNow run `card_eval.py label`. Read the abstract first, then the card.")


def _is_judged(r):
    """A card is judged when it is COMPLETE, not merely started.

    The original version (`any(...)`) meant a card with one field answered and
    five still None counted as done. That made a quit mid-card invisible to
    the resume logic: label() would skip the in-progress card entirely on
    restart and open the next untouched one instead. Fixed 2026-08-30 after
    exactly that happened on 2410.16457.
    """
    fields_done = all(v is not None for v in r["judgments"].values())
    objects_done = (all(o["verdict"] is not None for o in r["objects"])
                     if r["objects"] else True)
    return fields_done and objects_done


# -------------------------------------------------------------------- label

def _wrap(s, width=78, indent="    "):
    if s is None:
        return indent + "(absent)"
    if isinstance(s, list):
        return "\n".join(f"{indent}- {str(x).strip()}" for x in s)
    words, lines, cur = str(s).split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(indent + cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(indent + cur)
    return "\n".join(lines)


def _ask(prompt, valid, default=None):
    while True:
        v = input(prompt).strip().lower()
        if not v and default is not None:
            return default
        if v in valid:
            return v


def label():
    if not LABELS.exists():
        sys.exit(f"no {LABELS.relative_to(ROOT)} -- run `card_eval.py sample` first")
    recs = [json.loads(l) for l in LABELS.read_text().splitlines() if l.strip()]
    todo = [r for r in recs if not _is_judged(r)]
    if not todo:
        print("all judged.")
        return

    tags = _error_types()

    print(f"{len(todo)} cards to judge.")
    for k, v in VERDICTS.items():
        print(f"  {k} = {v}")
    print("  s = skip this field    q = save and quit\n")
    if tags:
        print(f"Error types come from rubrics/ERROR-TYPES.md ({len(tags)} tags). "
              f"You will be\nasked for them once per card, after the note. One tag "
              f"does not replace the\nsentence -- it makes sentences countable, "
              f"which is the whole point (invariant 19).\n")
    print("The question is whether a READER OF THIS CARD would be misled --")
    print("not whether it is phrased the way you would phrase it. A correct")
    print("object under a different canonical name is 'y'.\n")

    for r in todo:
        print("=" * 78)
        # sections_read is shown because it is often the decisive test for a
        # field that describes machinery the abstract does not mention. If the
        # curator only read the abstract, standard-for-the-area detail was
        # supplied from priors rather than extracted -- which is right most of
        # the time in a well-trodden area and wrong exactly where a paper
        # deviates from the standard scheme, i.e. where the novelty is.
        # Self-reported, so it is evidence rather than proof.
        print(f"{r['arxiv_id']}  [{r['domain']}]  curator confidence: "
              f"{r.get('confidence') or '?'}  "
              f"sections_read: {', '.join(r.get('sections_read') or []) or 'NONE'}")
        ver = r.get("source_version")
        if ver and ver != "unresolved":
            print(f"source: arxiv.org/abs/{ver}   <- CHECK AGAINST THIS VERSION")
        else:
            print("source version: UNKNOWN — this card predates version pinning.")
            print("  arxiv.org/abs/<id> serves the LATEST version, which may not be")
            print("  the one the curator read. A clause absent from the version you")
            print("  open is not evidence the curator invented it. If a field turns")
            print("  on that, check the other versions before scoring it 'n'.")
        print(f"\n{r['title']}\n")
        print("--- ABSTRACT " + "-" * 65)
        print(_wrap(r["abstract"][:2200] or "(not in papers.sqlite)"))
        print("-" * 78)

        draft = r.get("drafted") or {}
        dj = draft.get("judgments") or {}
        dreasons = draft.get("reasons") or {}
        if draft:
            print("\n  A DRAFT JUDGMENT IS LOADED. Each field shows the drafted")
            print("  verdict and its one-line reason; press enter to accept it, or")
            print("  type a letter to override. Overrides are recorded separately.")
            print("  Read the reason, not just the letter -- accepting without")
            print("  reading turns this eval into two models agreeing with")
            print("  each other, which is not what it measures.")

        quit_now = False
        overrides = []
        for field in r["fields"]:
            if field == "mathematical_objects":
                continue                      # handled separately, below
            print(f"\n### {field}")
            print(_wrap(r["card"].get(field)))
            d = dj.get(field)
            if d:
                if dreasons.get(field):
                    print(f"\n  draft: {d} — {dreasons[field]}")
                else:
                    print(f"\n  draft: {d}")
                v = _ask(f"  {field} [y/p/n/s/q, enter={d}]: ", set("ypnsq"), default=d)
            else:
                v = _ask(f"  {field} [y/p/n/s/q]: ", set("ypnsq"))
            if v == "q":
                quit_now = True
                break
            if v != "s":
                if d and v != d:
                    overrides.append(f"{field}: draft {d} -> you {v}")
                r["judgments"][field] = v

        if quit_now:
            _save(recs)
            print("saved.")
            return

        if "mathematical_objects" in r["fields"] and r["objects"]:
            print("\n### mathematical_objects — per object")
            print("    y = real and correctly roled · p = right object, role is off")
            print("    n = not really in this paper, or misidentified\n")
            # Roles come from the snapshot taken at sample() time, not from the
            # card file as it stands now. If the card has been edited since you
            # drew the sample, the thing you are judging is the version you drew
            # -- otherwise a mid-labelling re-curation silently changes what the
            # number means.
            roles = {x.get("name"): x.get("role")
                     for x in (r["card"].get("mathematical_objects") or [])}
            dobj = draft.get("objects") or {}
            for o in r["objects"]:
                flag = "" if o["named_in_paper"] else "   << named_in_paper: FALSE"
                print(f"  - {o['name']}{flag}")
                if roles.get(o["name"]):
                    print(_wrap(roles[o["name"]], indent="      "))
                d = dobj.get(o["name"])
                if isinstance(d, dict):
                    d, reason = d.get("verdict"), d.get("reason")
                else:
                    reason = None
                if d:
                    print(f"      draft: {d}" + (f" — {reason}" if reason else ""))
                    v = _ask(f"    verdict [y/p/n/s/q, enter={d}]: ",
                             set("ypnsq"), default=d)
                else:
                    v = _ask("    verdict [y/p/n/s/q]: ", set("ypnsq"))
                if v == "q":
                    _save(recs)
                    print("saved.")
                    return
                if v != "s":
                    if d and v != d:
                        overrides.append(f"object {o['name']}: draft {d} -> you {v}")
                    o["verdict"] = v
            verdicts = [o["verdict"] for o in r["objects"] if o["verdict"]]
            if verdicts:
                r["judgments"]["mathematical_objects"] = (
                    "n" if all(v == "n" for v in verdicts)
                    else "y" if all(v == "y" for v in verdicts) else "p")

            print("\n  How many load-bearing objects did the curator MISS?")
            print("  (objects the paper's result actually rests on, absent from the card.")
            print("   This is the recall half; without it a curator that lists one safe")
            print("   object per paper scores perfectly.)")
            dm = draft.get("objects_missed")
            if dm is not None:
                print(f"    draft: {dm}" +
                      (f" — {draft['missed_reason']}" if draft.get("missed_reason") else ""))
                m = _ask(f"    missed [0-9/s/q, enter={dm}]: ",
                         set("0123456789sq"), default=str(dm))
            else:
                m = _ask("    missed [0-9/s/q]: ", set("0123456789sq"))
            if m == "q":
                _save(recs)
                print("saved.")
                return
            if m != "s":
                if dm is not None and int(m) != dm:
                    overrides.append(f"objects_missed: draft {dm} -> you {m}")
                r["objects_missed"] = int(m)

        if draft.get("notes"):
            print("\n  draft note:")
            print(_wrap(draft["notes"], indent="    "))
            note = input("\n  note (enter to accept the draft note, or type your own): ").strip()
            r["notes"] = note or draft["notes"]
            if note:
                overrides.append("notes: rewritten")
        else:
            note = input("\n  note (optional, enter to skip): ").strip()
            if note:
                r["notes"] = note

        if tags:
            print("  error types (comma-separated numbers, 'u' unclassified, "
                  "enter for none):")
            print("    " + "  ".join(f"{i+1}={t}" for i, t in enumerate(tags)))
            raw = input("  tags: ").strip().lower()
            if raw:
                chosen = []
                for part in raw.split(","):
                    part = part.strip()
                    if part in ("u", "unclassified"):
                        chosen.append("unclassified")
                    elif part.isdigit() and 1 <= int(part) <= len(tags):
                        chosen.append(tags[int(part) - 1])
                    elif part in tags:
                        chosen.append(part)
                    elif part:
                        print(f"    ignored unknown tag {part!r} -- do not invent "
                              f"tags; use 'u' and the vocabulary grows later.")
                r["error_types"] = sorted(set(chosen))

        # Provenance. A card you sat through is yours even where you accepted
        # every drafted verdict -- you read the reasons and let them stand, and
        # that is a judgment. But a card judged with a draft loaded is not the
        # same evidence as one judged cold, so the two are named differently and
        # score() reports the split rather than pooling them.
        r["labeller"] = "user-reviewed-draft" if draft else "user"
        if overrides:
            r["overrides"] = overrides
            print(f"  {len(overrides)} override(s) recorded.")
        elif draft:
            print("  draft accepted in full.")
        print()

    _save(recs)
    print("judged.")


def _save(recs):
    LABELS.write_text("".join(json.dumps(r) + "\n" for r in recs))


# ------------------------------------------------------------------- import

def import_draft(path, force=False):
    """Load drafted verdicts into `drafted` so `label` can offer them as defaults.

    THIS DOES NOT WRITE JUDGMENTS. Nothing here touches `judgments` or an
    object's `verdict`; those are only ever set by a human sitting in `label`.
    The draft is a proposal with reasons attached, and the reasons are the
    point -- a drafted verdict you accept without reading its reason is a
    number measuring model-model agreement while claiming to measure card
    accuracy, which is the specific way this eval could quietly become
    worthless.

    Expected JSON: one object or a list of them.

        {"arxiv_id": "...",
         "judgments": {"problem": "y", ...},
         "reasons":   {"problem": "one line on WHY, shown at the prompt", ...},
         "objects":   {"<object name>": {"verdict": "p", "reason": "..."}, ...},
         "objects_missed": 2, "missed_reason": "...",
         "notes": "...", "error_types": ["objective-fact"]}

    Object names are checked against the card's actual object list and a
    mismatch is reported rather than silently dropped: a drafter inventing an
    object name is exactly the failure mode this whole file exists to catch,
    and it should not first show up as a silently missing prompt.
    """
    if not LABELS.exists():
        sys.exit(f"no {LABELS.relative_to(ROOT)} -- run `card_eval.py sample` first")
    data = json.loads(Path(path).read_text())
    if isinstance(data, dict):
        data = [data]

    recs = [json.loads(l) for l in LABELS.read_text().splitlines() if l.strip()]
    by_id = {r["arxiv_id"]: r for r in recs}
    vocab = set(_error_types()) | {"unclassified"}

    loaded = skipped = 0
    for d in data:
        aid = d.get("arxiv_id")
        r = by_id.get(aid)
        if not r:
            print(f"  {aid}  SKIP  not in card_labels.jsonl (sample it first)")
            skipped += 1
            continue
        if r.get("labeller") in ("user", "user-reviewed-draft") and not force:
            print(f"  {aid}  SKIP  already judged by you -- --force to replace "
                  f"the draft anyway (your judgments are never overwritten)")
            skipped += 1
            continue

        bad = [f"{k}={v}" for k, v in (d.get("judgments") or {}).items()
               if v not in ("y", "p", "n")]
        if bad:
            print(f"  {aid}  SKIP  bad verdicts: {', '.join(bad)}")
            skipped += 1
            continue

        known = {o["name"] for o in r["objects"]}
        drafted_objs = d.get("objects") or {}
        unknown = [k for k in drafted_objs if k not in known]
        missing = [k for k in known if k not in drafted_objs]
        if unknown:
            print(f"  {aid}  WARNING  drafted object(s) not on the card: "
                  f"{', '.join(unknown)}")
            print( "           the drafter named something the curator did not. "
                   "Check that before accepting anything on this card.")
        if missing:
            print(f"  {aid}  note  {len(missing)} object(s) undrafted, "
                  f"you will be asked cold: {', '.join(missing)}")

        badtags = [t for t in (d.get("error_types") or []) if t not in vocab]
        if badtags:
            print(f"  {aid}  WARNING  tags outside ERROR-TYPES.md: "
                  f"{', '.join(badtags)} -- dropped, use 'u' instead of inventing")
        d["error_types"] = [t for t in (d.get("error_types") or []) if t in vocab]

        r["drafted"] = d
        r["labeller"] = "claude-drafted"
        loaded += 1
        print(f"  {aid}  draft loaded")

    _save(recs)
    print(f"\nloaded {loaded}, skipped {skipped}")
    if loaded:
        print("\nRun `card_eval.py label`. Each drafted verdict shows with its")
        print("reason and enter accepts it. The cards are still unjudged until")
        print("you go through them -- an imported draft is not a label.")


# -------------------------------------------------------------------- score

def score_run(labels_path=None):
    path = Path(labels_path) if labels_path else LABELS
    if not path.exists():
        sys.exit(f"no {path} -- run `sample` and `label` first")
    recs = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    judged = [r for r in recs if _is_judged(r)]
    if not judged:
        sys.exit("nothing judged yet -- run `card_eval.py label`")

    n = len(judged)
    print(f"=== Card eval, n={n} cards judged ===\n")

    # ---- who judged these, before any number is shown
    prov = Counter(r.get("labeller") or "unrecorded" for r in judged)
    n_draft = prov.get("user-reviewed-draft", 0)
    n_over = sum(1 for r in judged if r.get("overrides"))
    print("  labelled by: " + ", ".join(f"{k}={v}" for k, v in prov.most_common()))
    if n_draft:
        print(f"    {n_draft} of {n} were reviewed against a drafted judgment, "
              f"{n_over} with overrides.")
        if n_draft and not n_over:
            print("    ^ NO OVERRIDES ANYWHERE. Either the drafts were right, or")
            print("      they were accepted without resistance. These look identical")
            print("      in this file and are not identical. Spot-check a few cards")
            print("      against the papers before trusting the numbers below --")
            print("      see verify_citations.py for the same argument about")
            print("      resolution not proving relevance.")
    print()

    # ---- per-field agreement
    per_field = defaultdict(lambda: {"y": 0, "p": 0, "n": 0})
    for r in judged:
        for f, v in r["judgments"].items():
            if v in ("y", "p", "n"):
                per_field[f][v] += 1

    print("  by field   (y = correct, p = partial, n = wrong)\n")
    print(f"    {'field':<24} {'n':>4}  {'y':>4} {'p':>4} {'n':>4}   {'correct':>8}")
    weakest, weakest_rate = None, 1.1
    for f in DEFAULT_FIELDS:
        c = per_field.get(f)
        if not c:
            continue
        tot = c["y"] + c["p"] + c["n"]
        rate = c["y"] / tot if tot else 0.0
        flag = ""
        if tot >= 5 and rate < 0.70:
            flag = "  <- weak"
            if rate < weakest_rate:
                weakest, weakest_rate = f, rate
        print(f"    {f:<24} {tot:>4}  {c['y']:>4} {c['p']:>4} {c['n']:>4}   "
              f"{rate:>7.2f}{flag}")

    # ---- mathematical_objects, per object
    listed = correct = partial = wrong = 0
    named_ok = named_tot = unnamed_ok = unnamed_tot = 0
    missed_total, missed_cards = 0, 0
    for r in judged:
        for o in r["objects"]:
            if o["verdict"] not in ("y", "p", "n"):
                continue
            listed += 1
            correct += o["verdict"] == "y"
            partial += o["verdict"] == "p"
            wrong += o["verdict"] == "n"
            if o["named_in_paper"]:
                named_tot += 1
                named_ok += o["verdict"] == "y"
            else:
                unnamed_tot += 1
                unnamed_ok += o["verdict"] == "y"
        if r["objects_missed"] is not None:
            missed_total += r["objects_missed"]
            missed_cards += 1

    obj_prec = correct / listed if listed else 0.0
    obj_rec = correct / (correct + missed_total) if (correct + missed_total) else 0.0

    print(f"\n  mathematical_objects — the load-bearing field\n")
    print(f"    objects listed        {listed}")
    print(f"    correct / partial / wrong   {correct} / {partial} / {wrong}")
    print(f"    object precision      {obj_prec:.2f}   (of what it listed, how much is real)")
    if missed_cards:
        print(f"    object recall         {obj_rec:.2f}   "
              f"({missed_total} missed across {missed_cards} cards)")
    else:
        print("    object recall         not scored -- no 'missed' counts recorded")

    if unnamed_tot:
        nr = named_ok / named_tot if named_tot else 0.0
        ur = unnamed_ok / unnamed_tot
        print(f"\n    named_in_paper: true   {named_ok}/{named_tot} = {nr:.2f}")
        print(f"    named_in_paper: false  {unnamed_ok}/{unnamed_tot} = {ur:.2f}")
        if named_tot and ur < nr - 0.15:
            print("\n    ^ The unnamed identifications are materially worse than the")
            print("      named ones. That is the recovery of unnamed mathematics --")
            print("      the highest-value output in the system and the one no")
            print("      downstream stage can check. Fix this before anything else:")
            print("      a false object here becomes a node bridge-finder reasons over.")
    else:
        print("\n    no named_in_paper: false claims in this sample.")
        print("    For compbio_mechanism that is itself a finding -- its charter sec4")
        print("    calls unnamed usage 'the main event, not an edge case'.")

    # ---- does the curator's self-reported confidence predict anything?
    by_conf = defaultdict(lambda: [0, 0])
    for r in judged:
        vs = [v for v in r["judgments"].values() if v in ("y", "p", "n")]
        if not vs:
            continue
        c = r.get("confidence") or "?"
        by_conf[c][0] += sum(1 for v in vs if v == "y")
        by_conf[c][1] += len(vs)
    if len(by_conf) > 1:
        print("\n  curator confidence vs. your agreement")
        for c in ("high", "medium", "low", "?"):
            if c in by_conf:
                ok, tot = by_conf[c]
                print(f"    {c:<8} {ok}/{tot} = {ok/tot:.2f}")
        print("    If low-confidence cards are not actually worse, the field is")
        print("    decorative and should either be dropped or given a rubric.")

    # ---- error types: the countable half
    tag_counts = Counter(t for r in judged for t in (r.get("error_types") or []))
    if tag_counts:
        print("\n  error types  (rubrics/ERROR-TYPES.md)\n")
        for tag, c in tag_counts.most_common():
            bar = "#" * c
            print(f"    {tag:<26} {c:>3}  {bar}")
        top, topn = tag_counts.most_common(1)[0]
        if topn >= 3 and top != "unclassified":
            print(f"\n    `{top}` on {topn} of {n} cards. One card is an anecdote;")
            print( "    this is a curator-prompt or schema change with a number")
            print( "    attached, which is what this script exists to produce.")
        unc = tag_counts.get("unclassified", 0)
        if unc > 5:
            print(f"\n    {unc} unclassified -- past ERROR-TYPES.md's threshold of five.")
            print( "    Per that file: add a category, do not widen a nearby one to")
            print( "    swallow them. A forced fit makes the counts lie in a")
            print( "    direction you cannot see.")
    else:
        print("\n  no error types recorded.")

    # ---- the notes, in full
    noted = [r for r in judged if r.get("notes")]
    if noted:
        print(f"\n  notes ({len(noted)} of {n} cards)\n")
        for r in noted:
            tagstr = ", ".join(r.get("error_types") or []) or "untagged"
            print(f"    --- {r['arxiv_id']} [{r['domain']}] ({tagstr})")
            for line in str(r["notes"]).splitlines():
                print(f"      {line}")
            print()

    # ---- what to do about it
    print("\n  ---")
    if weakest:
        print(f"  Weakest field: {weakest} ({weakest_rate:.2f}).")
        print("  Revise the schema description or the curator prompt for that field,")
        print("  re-curate the same papers, and run `diff`. One change at a time --")
        print("  two changes and you cannot attribute the difference.")
        if weakest == "mathematical_objects":
            print("\n  README.md names this field as the strongest fine-tuning candidate")
            print("  IF it stays weak after a schema/prompt revision. Not before: a")
            print("  prompt fix is cheap and a fine-tune is not.")
    else:
        print("  No field below 0.70. If that holds on a second sample, the schema")
        print("  is not what is limiting card quality and the next question is")
        print("  coverage, not accuracy.")

    print("\n  Cards judged here were extracted under the CURRENT schema. If you")
    print("  revise it, the existing cards were built to the old one -- decide")
    print("  explicitly whether they get re-extracted or grandfathered, and write")
    print("  the decision down. (See PROJECT-STATUS.md sec4.1: all four curators")
    print("  ran before this measurement existed, so that question is live.)")

    RUNS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = {
        "n_cards": n,
        "fields": {f: dict(c) for f, c in per_field.items()},
        "field_correct_rate": {
            f: (c["y"] / (c["y"] + c["p"] + c["n"]))
            for f, c in per_field.items() if (c["y"] + c["p"] + c["n"])},
        "objects": {"listed": listed, "correct": correct, "partial": partial,
                     "wrong": wrong, "missed": missed_total,
                     "precision": obj_prec, "recall": obj_rec,
                     "named_ok": named_ok, "named_total": named_tot,
                     "unnamed_ok": unnamed_ok, "unnamed_total": unnamed_tot},
        "error_types": dict(tag_counts),
        "notes": {r["arxiv_id"]: r["notes"] for r in judged if r.get("notes")},
        "arxiv_ids": [r["arxiv_id"] for r in judged],
        # Provenance travels with the number, permanently. A run file that says
        # 0.82 without saying who produced the labels is the same class of
        # artifact as EVAL-01-FINDINGS.md's stale figures: true when written,
        # unfalsifiable later.
        "labellers": dict(prov),
        "n_overridden": n_over,
        "overrides": {r["arxiv_id"]: r["overrides"]
                       for r in judged if r.get("overrides")},
    }
    (RUNS / f"{stamp}.json").write_text(json.dumps(out, indent=2))
    print(f"\n  saved eval/card_runs/{stamp}.json")


# --------------------------------------------------------------------- diff

def diff():
    runs = sorted(RUNS.glob("*.json"))
    if len(runs) < 2:
        sys.exit("need at least two runs -- score twice, with a schema or prompt "
                 "change in between, or there is nothing to compare")
    a, b = json.loads(runs[-2].read_text()), json.loads(runs[-1].read_text())
    print(f"{runs[-2].stem}  ->  {runs[-1].stem}\n")

    fa, fb = a.get("field_correct_rate", {}), b.get("field_correct_rate", {})
    for f in DEFAULT_FIELDS:
        if f in fa and f in fb:
            print(f"  {f:<24} {fa[f]:.2f} -> {fb[f]:.2f}  ({fb[f]-fa[f]:+.2f})")

    oa, ob = a.get("objects", {}), b.get("objects", {})
    for k in ("precision", "recall"):
        if k in oa and k in ob:
            print(f"  objects {k:<16} {oa[k]:.2f} -> {ob[k]:.2f}  ({ob[k]-oa[k]:+.2f})")

    ta, tb = a.get("error_types", {}), b.get("error_types", {})
    if ta or tb:
        print()
        for tag in sorted(set(ta) | set(tb)):
            x, y = ta.get(tag, 0), tb.get(tag, 0)
            print(f"  {tag:<26} {x:>3} -> {y:>3}  ({y-x:+d})")

    same = set(a.get("arxiv_ids", [])) & set(b.get("arxiv_ids", []))
    print(f"\n  cards in common: {len(same)} of {a.get('n_cards')} -> {b.get('n_cards')}")
    if len(same) < min(a.get("n_cards", 0), b.get("n_cards", 0)) * 0.8:
        print("  ^ Mostly different cards. This diff is comparing two samples as")
        print("    much as two schema versions; a change smaller than the sampling")
        print("    spread means nothing. Re-curate the SAME papers to attribute it.")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample")
    s.add_argument("--n", type=int, default=20)
    s.add_argument("--domain", choices=DOMAINS)
    s.add_argument("--append", action="store_true",
                    help="add --n new cards to the existing card_labels.jsonl "
                         "instead of overwriting it; excludes arxiv_ids already "
                         "in the file")
    s.add_argument("--fields", help="comma-separated override of the fields to judge; "
                                     f"default {','.join(DEFAULT_FIELDS)}")
    sub.add_parser("label")
    im = sub.add_parser("import", help="load drafted verdicts as defaults for `label`")
    im.add_argument("path", help="JSON file of drafted judgments")
    im.add_argument("--force", action="store_true",
                     help="replace a draft on a card you have already judged; "
                          "your judgments themselves are never overwritten")
    sc = sub.add_parser("score")
    sc.add_argument("--labels", help="defaults to eval/card_labels.jsonl")
    sub.add_parser("diff")
    a = ap.parse_args()

    {"sample": lambda: sample(a.n, a.domain, a.append,
                              a.fields.split(",") if a.fields else None),
     "label": label,
     "import": lambda: import_draft(a.path, a.force),
     "score": lambda: score_run(a.labels),
     "diff": diff}[a.cmd]()


if __name__ == "__main__":
    main()
