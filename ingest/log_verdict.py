#!/usr/bin/env python3
"""Record YOUR verdict on a promoted proposal. The other half of the loop.

The system already learns from the skeptic: every kill lands in
ledger/rejection_patterns.md and goes back into bridge-finder's prompt. It
learns nothing from you. After the Week 8-9 calibration ends, the referee gate
is never again measured against the only judgment that matters, which means its
credibility is frozen at its Week 9 value and decays from there unobserved.

This is the fix, and it costs two minutes per proposal.

    python ingest/log_verdict.py pending          # what is awaiting your verdict
    python ingest/log_verdict.py log b-2608-014   # blind: scores hidden until after
    python ingest/log_verdict.py show b-2608-014  # your verdict vs. the gate's
    python ingest/log_verdict.py context --weeks 12   # block for agent prompts

ONE RULE, and it is the same rule as reject-first ordering in the referee
prompts and item 4 of HANDOFF.md section 4: `log` does not show you the referee
scores until you have committed your own. Once you have seen a machine score you
cannot unsee it, and an agreement rate computed from contaminated verdicts is a
number that measures nothing while looking exactly like a number that does.

Non-interactive form is available and deliberately awkward -- it exists for
scripting, not for speed:

    python ingest/log_verdict.py log b-2608-014 --read y \\
        --verdict discarded --reason "assumes exchangeability across batches"
"""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml")

ROOT = Path(__file__).parent.parent
LEDGER = ROOT / "ledger" / "bridges.jsonl"
VERDICTS = ROOT / "ledger" / "user_verdicts.jsonl"
REVIEWS = ROOT / "reviews"
PROPOSALS = ROOT / "proposals"

VERDICT_VALUES = ("pursued", "filed", "discarded")

VERDICT_HELP = """
  pursued    You are going to do something with this. Reading the three papers
             counts; intending to counts only if you put it on a calendar.
  filed      Real, not now. This is the honest majority verdict and it is NOT a
             soft discard -- keep it distinct or the signal collapses to binary.
  discarded  You would not want to see this proposal again, and a system working
             properly would not have surfaced it.
"""


def read_jsonl(path):
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            print(f"  ! unparseable line in {path.name}, skipped", file=sys.stderr)
    return out


def ledger_state():
    """Last state wins -- the ledger is append-only, so later lines supersede."""
    state = {}
    for row in read_jsonl(LEDGER):
        if "id" in row:
            state[row["id"]] = {**state.get(row["id"], {}), **row}
    return state


def logged_ids():
    return {v["bridge_id"] for v in read_jsonl(VERDICTS) if "bridge_id" in v}


def gate_record(bid):
    """Referee binaries and scores for one proposal. Read AFTER the verdict."""
    axes = {}
    d = REVIEWS / bid
    if not d.exists():
        return axes
    for f in sorted(d.glob("*.md")):
        if f.stem == "skeptic":
            continue
        try:
            r = yaml.safe_load(f.read_text().split("---")[1])
        except Exception:
            continue
        if not isinstance(r, dict):
            continue
        axis = r.get("axis", f.stem)
        axes[axis] = {
            "reject": str(r.get("reject", "")).lower() in ("yes", "true"),
            "score": r.get("score"),
        }
    return axes


def probe_record(bid):
    f = ROOT / "probes" / bid / "verdict.md"
    if not f.exists():
        return None
    try:
        v = yaml.safe_load(f.read_text().split("---")[1])
    except Exception:
        return None
    return v.get("verdict") if isinstance(v, dict) else None


def mean_score(axes):
    vals = [a["score"] for a in axes.values() if isinstance(a.get("score"), (int, float))]
    return sum(vals) / len(vals) if vals else None


def cmd_pending(a):
    state = ledger_state()
    done = logged_ids()
    rows = [
        (bid, b) for bid, b in state.items()
        if b.get("state") == "promoted" and bid not in done
    ]
    if not rows:
        print("Nothing awaiting your verdict.")
        return
    rows.sort(key=lambda r: r[1].get("created", ""))
    print(f"{len(rows)} promoted proposal(s) awaiting your verdict:\n")
    for bid, b in rows:
        print(f"  {bid}  [{b.get('type','?')}]  {b.get('object','?')}")
        print(f"      {'+'.join(b.get('domains', []))}")
        spec = PROPOSALS / bid / "spec.md"
        print(f"      spec: {spec.relative_to(ROOT) if spec.exists() else 'MISSING'}")
    print("\n  python ingest/log_verdict.py log <id>")
    if len(rows) > 6:
        print("\n  ^ More than six unlogged. Either the digest is going unread --")
        print("    which is the deskilling signal, see HYBRID-SYSTEM-REVIEW.md 3.3 --")
        print("    or the promote bar is too low. Both are worth acting on; the")
        print("    second is a one-line fix (raise the bar to mean >= 4.0).")


def ask(prompt, valid=None):
    """valid=None means free text, and free text is NOT lowercased -- the reason
    field is prose that ends up in an agent prompt, not an enum."""
    while True:
        try:
            v = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit("\naborted, nothing written")
        if valid is None:
            if len(v) >= 10:
                return v
            print("    -> a sentence, not a word. this is the whole point of the file.")
            continue
        if v.lower() in valid:
            return v.lower()
        print(f"    -> one of: {', '.join(valid)}")


def cmd_log(a):
    bid = a.bridge_id
    state = ledger_state()
    if bid not in state:
        sys.exit(f"{bid} is not in the ledger")
    if bid in logged_ids() and not a.again:
        sys.exit(f"{bid} already has a verdict. --again to log a revised one.")

    b = state[bid]
    if a.verdict:
        read, verdict, reason = a.read, a.verdict, a.reason
        if not reason:
            sys.exit("--reason is required; an unreasoned verdict teaches nothing")
        if not read:
            sys.exit("--read y|n is required; a verdict on an unread proposal is "
                     "still worth logging, but it measures the digest, not the gate")
    else:
        print(f"\n{bid}  [{b.get('type','?')}]  {b.get('object','?')}")
        print(f"domains: {'+'.join(b.get('domains', []))}")
        print(f"spec:    proposals/{bid}/spec.md")
        print("\nScores are hidden until you have committed. That is the point.")
        print(VERDICT_HELP)
        read = ask("read it? [y/n] ", ("y", "n"))
        verdict = ask(f"verdict [{'/'.join(VERDICT_VALUES)}] ", VERDICT_VALUES)
        print("\none sentence, for bridge-finder. be specific about WHY --")
        print("'not interesting' is not a reason, 'assumes exchangeability across")
        print("batches, which single-cell data never satisfies' is.")
        reason = ask("> ")

    axes = gate_record(bid)
    rec = {
        "bridge_id": bid,
        "date": date.today().isoformat(),
        "read": read == "y",
        "verdict": verdict,
        "reason": reason,
        "object": b.get("object"),
        "type": b.get("type"),
        "domains": b.get("domains", []),
        # Snapshotted so agreement is computable later without re-parsing reviews,
        # and so a rewritten rubric cannot retroactively change past agreement.
        "gate": {
            "mean_score": mean_score(axes),
            "axes": {k: v["score"] for k, v in axes.items()},
            "any_reject": any(v["reject"] for v in axes.values()),
            "probe": probe_record(bid),
        },
    }
    VERDICTS.parent.mkdir(parents=True, exist_ok=True)
    with VERDICTS.open("a") as f:
        f.write(json.dumps(rec) + "\n")

    print(f"\nlogged -> ledger/user_verdicts.jsonl")
    if axes:
        m = rec["gate"]["mean_score"]
        print(f"\nthe gate said: mean {m:.2f}" if m else "\nthe gate said:")
        for k, v in sorted(axes.items()):
            print(f"  {k:<14} {v['score']}  {'REJECT' if v['reject'] else ''}")
        if verdict == "discarded" and m and m >= 4.0:
            print("\n  ^ You discarded something the gate rated highly. This is the")
            print("    most informative row in the file. Check that your reason")
            print("    above names the axis the gate missed -- that sentence is")
            print("    what a rubric anchor gets written from.")


def cmd_show(a):
    for v in read_jsonl(VERDICTS):
        if v.get("bridge_id") == a.bridge_id:
            print(json.dumps(v, indent=2))
            return
    sys.exit("no verdict logged for that id")


def cmd_context(a):
    """Emitted into bridge-finder's and project-architect's prompts.

    Discards carry nearly all the signal, so they are listed in full and first.
    'filed' is summarised only -- it is the majority verdict and letting it
    dominate the block would train the agents toward whatever you happen to be
    busy with, which is a slower version of the monoculture failure.
    """
    cutoff = (date.today() - timedelta(weeks=a.weeks)).isoformat()
    rows = [v for v in read_jsonl(VERDICTS) if v.get("date", "") >= cutoff]
    if not rows:
        print("(no user verdicts logged yet)")
        return

    counts = {k: sum(1 for v in rows if v.get("verdict") == k) for k in VERDICT_VALUES}
    print(f"# User verdicts, trailing {a.weeks} weeks")
    print(f"# {counts['pursued']} pursued / {counts['filed']} filed / "
          f"{counts['discarded']} discarded, n={len(rows)}\n")
    print("These are the user's own judgments on proposals this pipeline promoted.")
    print("They outrank your priors and they outrank the referee scores. Treat a")
    print("discard as a standing instruction, not as one data point.\n")

    print("## Discarded -- do not propose this shape again\n")
    for v in [v for v in rows if v.get("verdict") == "discarded"]:
        print(f"- **{v.get('object','?')}** ({'+'.join(v.get('domains',[]))}, "
              f"{v.get('type','?')}): {v.get('reason','')}")
    print("\n## Pursued -- more of this shape\n")
    for v in [v for v in rows if v.get("verdict") == "pursued"]:
        print(f"- **{v.get('object','?')}** ({'+'.join(v.get('domains',[]))}, "
              f"{v.get('type','?')}): {v.get('reason','')}")

    unread = sum(1 for v in rows if not v.get("read"))
    if unread > len(rows) / 2:
        print(f"\n<!-- {unread}/{len(rows)} promoted proposals went unread. The"
              f" digest is not landing. -->")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("pending").set_defaults(fn=cmd_pending)

    p = sub.add_parser("log")
    p.add_argument("bridge_id")
    p.add_argument("--read", choices=("y", "n"))
    p.add_argument("--verdict", choices=VERDICT_VALUES)
    p.add_argument("--reason")
    p.add_argument("--again", action="store_true",
                   help="log a revised verdict over an existing one")
    p.set_defaults(fn=cmd_log)

    p = sub.add_parser("show")
    p.add_argument("bridge_id")
    p.set_defaults(fn=cmd_show)

    p = sub.add_parser("context")
    p.add_argument("--weeks", type=int, default=12)
    p.set_defaults(fn=cmd_context)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
