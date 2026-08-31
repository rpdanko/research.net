#!/usr/bin/env python3
"""Monthly audit of the review gates.

Four numbers decide whether to trust the gates. Read the SHAPE of the
distributions, not the means -- an axis where 80% of scores land on one
value is not measuring anything, it is decorating.

    python3 ingest/review_audit.py --month

Sections 1-3 check the gate against itself: is it discriminating, is it
rejecting anything, are the probe escape hatches in use. Section 4 checks it
against you, and is the only external check it ever gets. It needs
ledger/user_verdicts.jsonl, which ingest/log_verdict.py writes.

For the health of the human half of the loop -- narrowing, coupling, whether the
digest is read at all -- see ingest/coalition_audit.py.
"""

import argparse, json, sys, statistics
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml")

ROOT = Path(__file__).parent.parent


def load(days):
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    reviews, probes = [], []
    for f in (ROOT / "reviews").glob("*/*.md"):
        if f.stem == "skeptic":
            continue
        try:
            r = yaml.safe_load(f.read_text().split("---")[1])
        except Exception:
            continue
        if isinstance(r, dict):
            reviews.append(r)
    for f in (ROOT / "probes").glob("*/verdict.md"):
        try:
            v = yaml.safe_load(f.read_text().split("---")[1])
        except Exception:
            continue
        if isinstance(v, dict):
            probes.append(v)
    return reviews, probes


def histogram(scores):
    c = Counter(scores)
    total = len(scores) or 1
    lines = []
    for s in (1, 2, 3, 4, 5):
        n = c.get(s, 0)
        lines.append(f"    {s}: {'#' * int(30 * n / total):<30} {n:>3} ({100*n/total:4.1f}%)")
    return "\n".join(lines), max(c.values(), default=0) / total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", action="store_true")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--errors", action="store_true",
                    help="count rejections by error type (rubrics/ERROR-TYPES.md)")
    a = ap.parse_args()
    if a.month:
        a.errors = True

    reviews, probes = load(a.days)
    if not reviews:
        sys.exit("no reviews found")

    print(f"=== Review audit, trailing {a.days} days ===\n")

    # 1. Score distribution per axis. Inflation and collapse both show here.
    by_axis = defaultdict(list)
    for r in reviews:
        if r.get("score") is not None:
            by_axis[r.get("axis", "?")].append(int(r["score"]))

    print("1. SCORE DISTRIBUTION\n")
    for axis, scores in sorted(by_axis.items()):
        hist, concentration = histogram(scores)
        mean = statistics.mean(scores)
        print(f"  {axis}  n={len(scores)}  mean={mean:.2f}")
        print(hist)
        if axis == "novelty" and mean > 3.0:
            print("    ^ WARNING: novelty mean > 3.0. Most research ideas have")
            print("      been had before. This is inflation. Fix the ANCHORS,")
            print("      not the prompt -- see rubrics/WRITING-ANCHORS.md.")
        if concentration > 0.6:
            print(f"    ^ WARNING: {concentration:.0%} of scores on one value.")
            print("      This axis is not discriminating. The anchors are")
            print("      probably still doing adjective work.")
        print()

    # 2. Veto rate -- the binaries are what the gate actually uses.
    vetoes = sum(1 for r in reviews if str(r.get("reject", "")).lower() in ("yes", "true"))
    print(f"2. VETO RATE: {vetoes}/{len(reviews)} ({100*vetoes/len(reviews):.0f}%)")
    if vetoes == 0:
        print("   ^ WARNING: no vetoes at all. A gate that never rejects is not a gate.")
    print()

    # 3. Probe verdicts. The escape hatches must actually be used.
    print("3. PROBE VERDICTS")
    if not probes:
        print("   none yet")
    else:
        vc = Counter(p.get("verdict", "?") for p in probes)
        for k, n in vc.most_common():
            print(f"   {k:<15} {n}")
        if vc.get("not-probeable", 0) == 0:
            print("\n   ^ WARNING: zero 'not-probeable' verdicts. The escape hatch")
            print("     is unused, which means probes are being manufactured to fit.")
            print("     Some proposals genuinely have no cheap numerical test.")
        if vc.get("falsified", 0) == 0:
            print("\n   ^ WARNING: zero falsifications. Check that negative controls")
            print("     are running AND actually destroying the structure they claim to.")
    print()

    # 4. Agreement with the user. The only external check this gate ever gets.
    gate_agreement(a.days)

    # 5. What KIND of error, counted. Needs the tags to be written.
    if a.errors:
        error_types(a.days)


def error_types(days):
    """Count rejections by error type.

    The point of a fixed vocabulary (rubrics/ERROR-TYPES.md) is that free text
    cannot be counted. Without tags you can see that the skeptic killed forty
    bridges; with them you can see that eighteen were one error, which is the
    thing that tells you what to fix.

    Concentration in one type is good news -- it is a fixable prompt problem.
    A flat distribution across ten types usually means the tags are being applied
    loosely, not that ten distinct things are going wrong.
    """
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    tags = Counter()
    by_agent = defaultdict(Counter)

    for f in (ROOT / "reviews").glob("*/*.md"):
        try:
            r = yaml.safe_load(f.read_text().split("---")[1])
        except Exception:
            continue
        if isinstance(r, dict) and r.get("error_type"):
            tags[r["error_type"]] += 1
            by_agent[f.stem][r["error_type"]] += 1

    for p in (ROOT / "ledger" / "citation_failures.jsonl",):
        if p.exists():
            for line in p.read_text().splitlines():
                if not line.strip():
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if r.get("date", "") >= cutoff and r.get("error_type"):
                    tags[r["error_type"]] += 1
                    by_agent[r.get("agent", "?")][r["error_type"]] += 1

    print("\n5. ERROR TYPES")
    if not tags:
        print("   No tags recorded. Either nothing has been rejected, or agents")
        print("   are not writing the `error_type` field. Check one review file")
        print("   before concluding the first.")
        return
    total = sum(tags.values())
    for tag, n in tags.most_common():
        bar = "#" * int(30 * n / total)
        print(f"   {tag:<24} {bar:<30} {n:>3} ({100*n/total:4.1f}%)")

    if tags.get("unclassified", 0) > 5:
        print("\n   ^ More than five `unclassified`. Either a category is missing")
        print("     from rubrics/ERROR-TYPES.md or the vocabulary has aged. Sun")
        print("     et al.'s protocol is explicit here: new categories emerging")
        print("     means returning to the coding scheme, not widening an existing")
        print("     category to swallow them.")

    if tags.get("fabricated-citation", 0):
        print(f"\n   ^ {tags['fabricated-citation']} fabricated citation(s). See")
        print("     `python3 ingest/verify_citations.py report --month` for which")
        print("     agent. Concentration in one agent is a prompt problem.")

    print("\n   by agent:")
    for agent, c in sorted(by_agent.items()):
        top = ", ".join(f"{k}={v}" for k, v in c.most_common(3))
        print(f"     {agent:<20} {top}")


def gate_agreement(days):
    """Does the gate still agree with you?

    Weeks 8-9 calibrate the rubric against your judgment, once. After that the
    gate is trusted forever on the strength of a fortnight, and nothing checks it
    again. This section is that fortnight made permanent, and it costs two
    minutes per proposal -- see ingest/log_verdict.py.

    The interesting cell is not the agreement rate. It is FALSE PROMOTES: things
    the gate rated highly and you discarded. Each one is a rubric anchor waiting
    to be written, and per rubrics/WRITING-ANCHORS.md that is where anchors are
    supposed to come from -- your own critical incidents, not adjectives.
    """
    path = ROOT / "ledger" / "user_verdicts.jsonl"
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    rows = []
    if path.exists():
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            try:
                v = json.loads(line)
            except json.JSONDecodeError:
                continue
            if v.get("date", "") >= cutoff:
                rows.append(v)

    print("4. AGREEMENT WITH YOU")
    if not rows:
        print("   No verdicts logged this period.")
        print("   Every number above describes the gate agreeing with itself.")
        print("   `python3 ingest/log_verdict.py pending`")
        return

    scored = [r for r in rows if isinstance(r.get("gate", {}).get("mean_score"), (int, float))]
    if not scored:
        print(f"   {len(rows)} verdicts, none with a recorded gate score.")
        return

    # The gate promoted all of these; the split that matters is what YOU did.
    kept = [r for r in scored if r["verdict"] in ("pursued", "filed")]
    dropped = [r for r in scored if r["verdict"] == "discarded"]
    agree = len(kept) / len(scored)

    print(f"   n={len(scored)}  agreement {agree:.0%} "
          f"({len(kept)} kept / {len(dropped)} discarded)")

    if kept:
        print(f"   mean gate score, kept      {statistics.mean([r['gate']['mean_score'] for r in kept]):.2f}")
    if dropped:
        print(f"   mean gate score, discarded {statistics.mean([r['gate']['mean_score'] for r in dropped]):.2f}")

    if kept and dropped:
        sep = (statistics.mean([r["gate"]["mean_score"] for r in kept])
               - statistics.mean([r["gate"]["mean_score"] for r in dropped]))
        print(f"   separation                 {sep:+.2f}")
        if sep <= 0.2:
            print("\n   ^ WARNING: the gate's scores do not separate what you keep from")
            print("     what you throw away. The gate is running and it is not")
            print("     predicting you. Rewrite the anchors from the discards below;")
            print("     do not adjust the promote threshold, which would only change")
            print("     how much of the same undifferentiated output reaches you.")

    false_promotes = [r for r in dropped if r["gate"]["mean_score"] >= 4.0]
    if false_promotes:
        print(f"\n   FALSE PROMOTES ({len(false_promotes)}) -- gate >= 4.0, you discarded:\n")
        for r in false_promotes:
            print(f"     {r['bridge_id']}  {r['gate']['mean_score']:.1f}  {r.get('object','?')}")
            print(f"       you: {r.get('reason','')}")
        print("\n   ^ These are your critical incidents. Each names an axis the")
        print("     rubric is not measuring. This is the raw material WRITING-ANCHORS.md")
        print("     section 2 asks for, and it is the only place it comes from.")

    unread = sum(1 for r in rows if not r.get("read"))
    if unread:
        print(f"\n   {unread}/{len(rows)} logged without being read. Verdicts on unread")
        print("   proposals are weak evidence; they measure the digest, not the gate.")


if __name__ == "__main__":
    main()
