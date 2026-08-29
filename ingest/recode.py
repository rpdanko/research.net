#!/usr/bin/env python3
"""Re-judge your own past judgments, blind, and find out whether you still agree.

Sun et al. (2024) spent three coders and two rounds building their taxonomy, and
the methodological point worth stealing is not the taxonomy at all -- it is the
protocol. Three coders, independent, back-to-back (each blind to the others),
70% of samples for pre-coding and 30% held back for test coding, consistency
measured by Holsti's method against a 70-80% threshold (Boettger & Palmer 2010).
Their first round came in at 68%, below threshold. They did not proceed and
adjust the number; they discussed the discrepancies, re-coded, and reached 89%.

This repo's Week 8-9 calibration is the same activity with none of that:
"read the proposals yourself, score them on the same three axes, and compare."
No reliability statistic, no threshold, no defined protocol for what to do when
agreement is poor, and -- because it happens once -- no way to see it move.

You are one person, so inter-coder reliability is unavailable. The substitute is
TEMPORAL: code the same items twice, weeks apart, blind to your first pass.
That measures something inter-coder reliability cannot, and it happens to be the
thing this system most needs to know.

    A referee gate is calibrated against a standard. If the standard is drifting,
    the gate is not wrong -- it is answering last quarter's question correctly,
    and every check in review_audit.py would report it as healthy.

Falling intra-rater agreement over months is the deskilling signal from
HYBRID-SYSTEM-REVIEW.md 3.3, made numerical. It is the only instrument here that
points at you rather than at the machine.

    python ingest/recode.py sources
    python ingest/recode.py sample --source verdicts --n 20 --min-age-weeks 6
    python ingest/recode.py judge <session>       # blind; prior pass hidden
    python ingest/recode.py score <session>
    python ingest/recode.py trend

BUDGET: about 30-40 minutes, once a quarter. This is the most expensive thing
this repo asks of you and the only one that measures the thing everything else
depends on.
"""

import argparse
import json
import random
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
SESSIONS = ROOT / "eval" / "recode"
HISTORY = ROOT / "eval" / "recode_history.jsonl"

# Boettger & Palmer (2010), as used by Sun et al. Below 0.70 the coding is not
# considered reliable enough to build on.
THRESHOLD_LOW = 0.70
THRESHOLD_OK = 0.80


def read_jsonl(path):
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


# --- judgment sources ------------------------------------------------------
# Each returns a list of {id, date, judgment, ordinal, display}.
# `ordinal` marks a 1-5 scale, where weighted kappa is the right statistic.

def src_verdicts():
    rows = []
    for v in read_jsonl(ROOT / "ledger" / "user_verdicts.jsonl"):
        rows.append({
            "id": v.get("bridge_id"),
            "date": v.get("date", ""),
            "judgment": v.get("verdict"),
            "ordinal": False,
            "display": f"{v.get('object','?')}  [{v.get('type','?')}]  "
                       f"{'+'.join(v.get('domains', []))}\n"
                       f"    spec: proposals/{v.get('bridge_id')}/spec.md",
            "choices": ("pursued", "filed", "discarded"),
        })
    return rows


def src_triage():
    rows = []
    for v in read_jsonl(ROOT / "eval" / "labels.jsonl"):
        rows.append({
            "id": v.get("arxiv_id"),
            "date": v.get("date", v.get("labelled_at", "")),
            "judgment": str(v.get("label", v.get("score", ""))),
            "ordinal": True,
            "display": f"{v.get('title','?')}\n    {v.get('categories','')}\n\n"
                       f"    {' '.join((v.get('abstract') or '').split())[:1400]}",
            "choices": ("0", "1", "2", "3", "4", "5"),
        })
    return rows


def src_cards():
    rows = []
    for v in read_jsonl(ROOT / "eval" / "card_labels.jsonl"):
        rows.append({
            "id": f"{v.get('arxiv_id')}::{v.get('field')}",
            "date": v.get("date", ""),
            "judgment": v.get("label"),
            "ordinal": False,
            "display": f"{v.get('arxiv_id')}  field: {v.get('field')}\n"
                       f"    curator wrote: {v.get('extracted','')}",
            "choices": ("correct", "partial", "wrong"),
        })
    return rows


def src_referee():
    rows = []
    for v in read_jsonl(ROOT / "eval" / "referee_calibration.jsonl"):
        rows.append({
            "id": f"{v.get('bridge_id')}::{v.get('axis')}",
            "date": v.get("date", ""),
            "judgment": str(v.get("score", "")),
            "ordinal": True,
            "display": f"{v.get('bridge_id')}  axis: {v.get('axis')}\n"
                       f"    spec: proposals/{v.get('bridge_id')}/spec.md",
            "choices": ("1", "2", "3", "4", "5"),
        })
    return rows


SOURCES = {
    "verdicts": (src_verdicts, "your pursued/filed/discarded calls on promoted proposals"),
    "triage":   (src_triage,   "the Week 1 labelled set -- your 0-5 relevance labels"),
    "cards":    (src_cards,    "your card_eval.py field judgments"),
    "referee":  (src_referee,  "your Week 8-9 self-scores on the three axes"),
}


# --- statistics ------------------------------------------------------------

def holsti(a, b):
    """CR = 2M/(N1+N2). With one coder over the same units this reduces to
    simple percent agreement, which is what Sun et al.'s threshold refers to."""
    m = sum(1 for x, y in zip(a, b) if x == y)
    return 2 * m / (len(a) + len(b)) if a else None


def cohen_kappa(a, b):
    """Chance-corrected. The reason to report it beside Holsti: if you judged
    everything '4', two passes agree perfectly and the agreement means nothing.
    Holsti says 1.00; kappa says 0.00. That gap IS the finding, and it is the
    same failure review_audit.py warns about when 60% of scores land on one
    value -- here pointed at you instead of the referees."""
    n = len(a)
    if not n:
        return None
    cats = sorted(set(a) | set(b))
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else None


def weighted_kappa(a, b):
    """Linear weights, for ordinal scales. A 4-vs-5 disagreement is not the same
    as a 1-vs-5 disagreement and nominal kappa cannot tell them apart."""
    try:
        ai = [float(x) for x in a]
        bi = [float(x) for x in b]
    except (TypeError, ValueError):
        return None
    cats = sorted(set(ai) | set(bi))
    k = len(cats)
    if k < 2:
        return None
    idx = {c: i for i, c in enumerate(cats)}
    n = len(ai)

    def w(i, j):
        return 1 - abs(i - j) / (k - 1)

    po = sum(w(idx[x], idx[y]) for x, y in zip(ai, bi)) / n
    ca, cb = Counter(ai), Counter(bi)
    pe = sum(w(idx[c1], idx[c2]) * (ca[c1] / n) * (cb[c2] / n)
             for c1 in cats for c2 in cats)
    return (po - pe) / (1 - pe) if pe < 1 else None


def within_one(a, b):
    try:
        return sum(1 for x, y in zip(a, b) if abs(float(x) - float(y)) <= 1) / len(a)
    except (TypeError, ValueError):
        return None


# --- commands --------------------------------------------------------------

def cmd_sources(a):
    print("Judgment sources available for re-coding:\n")
    for name, (fn, desc) in SOURCES.items():
        rows = [r for r in fn() if r.get("id") and r.get("judgment")]
        cutoff = (date.today() - timedelta(weeks=6)).isoformat()
        eligible = [r for r in rows if r.get("date", "9999") < cutoff]
        print(f"  {name:<10} {len(rows):>4} judgments, {len(eligible):>4} older than 6 weeks")
        print(f"             {desc}")
    print("\n  Nothing older than six weeks is worth re-coding -- you would be")
    print("  remembering rather than re-judging, and the number would flatter you.")


def cmd_sample(a):
    if a.source not in SOURCES:
        sys.exit(f"unknown source. one of: {', '.join(SOURCES)}")
    rows = [r for r in SOURCES[a.source][0]() if r.get("id") and r.get("judgment")]
    cutoff = (date.today() - timedelta(weeks=a.min_age_weeks)).isoformat()
    pool = [r for r in rows if r.get("date", "9999") < cutoff]
    if len(pool) < 10:
        sys.exit(f"only {len(pool)} judgments older than {a.min_age_weeks} weeks. "
                 f"Below about 10 the statistics are noise; wait.")

    pick = random.Random(f"{date.today().isoformat()}-{a.source}").sample(
        pool, min(a.n, len(pool)))
    sid = f"{a.source}-{date.today().isoformat()}"
    SESSIONS.mkdir(parents=True, exist_ok=True)
    path = SESSIONS / f"{sid}.json"
    if path.exists() and not a.force:
        sys.exit(f"session {sid} already exists. --force to replace.")

    path.write_text(json.dumps({
        "session": sid,
        "source": a.source,
        "created": date.today().isoformat(),
        "min_age_weeks": a.min_age_weeks,
        # pass1 is stored so `score` can compare, and is never shown by `judge`.
        "items": [{"id": r["id"], "display": r["display"], "choices": r["choices"],
                   "ordinal": r["ordinal"], "pass1": r["judgment"],
                   "pass1_date": r.get("date", ""), "pass2": None} for r in pick],
    }, indent=1))
    print(f"session {sid}: {len(pick)} items from '{a.source}'")
    print(f"  python ingest/recode.py judge {sid}")
    print("\nYour original judgments are in the file and will not be shown to you")
    print("during `judge`. Do not open it. The whole measurement is the blinding,")
    print("and there is no way to un-see a prior judgment once you have looked.")


def cmd_judge(a):
    path = SESSIONS / f"{a.session}.json"
    if not path.exists():
        sys.exit(f"no session {a.session}")
    data = json.loads(path.read_text())
    todo = [i for i in data["items"] if i["pass2"] is None]
    if not todo:
        print("session complete. `score` it.")
        return

    print(f"\n{len(todo)} item(s) left. Judge as if for the first time.")
    print("Ctrl-C stops; progress is saved after each.\n")

    for item in todo:
        print("=" * 70)
        print(f"  {item['display']}")
        print("=" * 70)
        opts = "/".join(item["choices"])
        while True:
            try:
                v = input(f"  [{opts}] > ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                path.write_text(json.dumps(data, indent=1))
                print("\nsaved. resume with the same command.")
                return
            if v in item["choices"]:
                break
            print(f"    -> one of: {opts}")
        item["pass2"] = v
        item["pass2_date"] = date.today().isoformat()
        path.write_text(json.dumps(data, indent=1))
        print()

    print(f"done. python ingest/recode.py score {a.session}")


def cmd_score(a):
    path = SESSIONS / f"{a.session}.json"
    if not path.exists():
        sys.exit(f"no session {a.session}")
    data = json.loads(path.read_text())
    done = [i for i in data["items"] if i["pass2"] is not None]
    if not done:
        sys.exit("nothing judged yet")
    if len(done) < len(data["items"]):
        print(f"note: {len(done)}/{len(data['items'])} judged\n")

    p1 = [str(i["pass1"]) for i in done]
    p2 = [str(i["pass2"]) for i in done]
    ordinal = any(i.get("ordinal") for i in done)

    h = holsti(p1, p2)
    k = cohen_kappa(p1, p2)
    kw = weighted_kappa(p1, p2) if ordinal else None
    w1 = within_one(p1, p2) if ordinal else None

    gap = (date.fromisoformat(done[0].get("pass2_date", date.today().isoformat()))
           - date.fromisoformat(done[0]["pass1_date"] or "2000-01-01")).days \
        if done[0].get("pass1_date") else None

    print(f"=== Intra-rater reliability: {data['source']}, n={len(done)} ===\n")
    if gap:
        print(f"  gap between passes    ~{gap} days\n")
    print(f"  Holsti (raw agreement) {h:.2f}")
    print(f"  Cohen's kappa          {k:.2f}" if k is not None else "  Cohen's kappa          n/a")
    if kw is not None:
        print(f"  weighted kappa         {kw:.2f}   (linear, ordinal)")
    if w1 is not None:
        print(f"  within 1 point         {w1:.2f}")
    print()

    if h < THRESHOLD_LOW:
        print(f"  BELOW THRESHOLD ({THRESHOLD_LOW:.2f}).")
        print("  Sun et al. hit 68% on their first round and did not proceed --")
        print("  they discussed the discrepancies and re-coded. Do the same thing:")
        print("  read the disagreements below and decide, for each, which pass was")
        print("  right. If you cannot tell, the CATEGORY is underdefined, and that")
        print("  is a rubric-anchor problem rather than a you problem.")
        print("\n  Do not adjust anything downstream until this is above 0.70. A gate")
        print("  calibrated against a standard you no longer hold is not measuring.")
    elif h < THRESHOLD_OK:
        print(f"  Acceptable ({THRESHOLD_LOW:.2f}-{THRESHOLD_OK:.2f}) but not comfortable.")
        print("  Worth reading the disagreements.")
    else:
        print(f"  Above {THRESHOLD_OK:.2f}. Your standard is stable.")

    if k is not None and h >= THRESHOLD_OK and k < 0.4:
        print("\n  ^ BUT: high agreement, low kappa. You are agreeing with yourself")
        print("    because you give almost everything the same judgment, not because")
        print("    you are discriminating. This is the exact failure review_audit.py")
        print("    flags when 60% of referee scores land on one value -- and it means")
        print("    the anchors you would write from these judgments would encode a")
        print("    distinction you are not actually making.")

    dis = [i for i in done if str(i["pass1"]) != str(i["pass2"])]
    if dis:
        print(f"\n  DISAGREEMENTS ({len(dis)}/{len(done)}):\n")
        for i in dis:
            print(f"    {i['id']}")
            print(f"      then ({i['pass1_date']}): {i['pass1']}")
            print(f"      now:                      {i['pass2']}")
        print("\n  Read these as a set, not one at a time. A systematic shift in one")
        print("  direction is drift and the charters/rubrics predate it. Scatter in")
        print("  both directions is noise, and the category boundary is the problem.")

    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a") as f:
        f.write(json.dumps({
            "date": date.today().isoformat(), "session": data["session"],
            "source": data["source"], "n": len(done),
            "holsti": round(h, 3) if h is not None else None,
            "kappa": round(k, 3) if k is not None else None,
            "weighted_kappa": round(kw, 3) if kw is not None else None,
            "within_one": round(w1, 3) if w1 is not None else None,
            "gap_days": gap,
        }) + "\n")
    print(f"\n  appended -> {HISTORY.relative_to(ROOT)}")


def cmd_trend(a):
    hist = read_jsonl(HISTORY)
    if not hist:
        print("No re-coding sessions yet. `recode.py sources`")
        return
    print("=== Intra-rater reliability over time ===\n")
    print(f"  {'date':<12} {'source':<10} {'n':>4} {'holsti':>7} {'kappa':>7} {'wtd':>7}")
    for h in hist:
        def c(v):
            return f"{v:.2f}" if isinstance(v, (int, float)) else "  -"
        print(f"  {h['date']:<12} {h['source']:<10} {h['n']:>4} "
              f"{c(h.get('holsti')):>7} {c(h.get('kappa')):>7} {c(h.get('weighted_kappa')):>7}")

    by_src = {}
    for h in hist:
        by_src.setdefault(h["source"], []).append(h)
    print()
    for src, rows in by_src.items():
        if len(rows) < 3:
            continue
        first, last = rows[0].get("holsti"), rows[-1].get("holsti")
        if first and last and last < first - 0.10:
            print(f"  ^ '{src}' agreement has fallen {first:.2f} -> {last:.2f}.")
            print("    This is the deskilling signal. It is not that you are getting")
            print("    worse at judging -- it is that you are judging less often, so")
            print("    the standard has stopped being reinforced by contact with the")
            print("    material. Check whether you are still reading the five raw")
            print("    abstracts in the digest; that habit is what maintains this.")
    if len(hist) < 3:
        print("  Fewer than three sessions. The single numbers are close to")
        print("  meaningless; the trend is the instrument. Keep going.")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("sources").set_defaults(fn=cmd_sources)

    p = sub.add_parser("sample")
    p.add_argument("--source", required=True)
    p.add_argument("--n", type=int, default=20)
    p.add_argument("--min-age-weeks", type=int, default=6)
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_sample)

    p = sub.add_parser("judge")
    p.add_argument("session")
    p.set_defaults(fn=cmd_judge)

    p = sub.add_parser("score")
    p.add_argument("session")
    p.set_defaults(fn=cmd_score)

    sub.add_parser("trend").set_defaults(fn=cmd_trend)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
