#!/usr/bin/env python3
"""Validate knowledge cards against card_schema.json.

Cards are markdown with YAML front matter. This runs on every card the
curators write, every day. Schema drift is silent and cumulative -- by the
time you notice bridge quality dropping, three months of cards are wrong.
Fail loudly here instead.

    python ingest/validate_card.py kb/stats/cards/2608.01234.md
    python ingest/validate_card.py kb/*/cards/*.md --new-only

Exit 0 if all pass, 1 otherwise.
"""

import argparse, json, sys, re
from pathlib import Path

try:
    import yaml, jsonschema
except ImportError:
    sys.exit("pip install pyyaml jsonschema")

SCHEMA = json.loads((Path(__file__).parent / "card_schema.json").read_text())
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)

# Roles that pass the schema's minLength but carry no information.
EMPTY_ROLES = re.compile(
    r"^(used|appears|present|referenced|mentioned|employed)\b.{0,25}$", re.I)


def check(path):
    """Returns a list of problem strings. Empty means the card is good."""
    text = Path(path).read_text()
    m = FM.match(text)
    if not m:
        return ["no YAML front matter"]

    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return [f"unparseable YAML: {e}"]

    problems = [f"{'/'.join(str(p) for p in e.path) or '(root)'}: {e.message}"
                for e in jsonschema.Draft7Validator(SCHEMA).iter_errors(data)]

    # Checks the schema cannot express -- these catch the ways a technically
    # valid card is still useless downstream.
    if data.get("arxiv_id") and Path(path).stem != data["arxiv_id"]:
        problems.append(f"filename does not match arxiv_id {data['arxiv_id']}")

    if str(data.get("domain")) not in str(path):
        problems.append(f"domain '{data.get('domain')}' does not match path")

    for i, o in enumerate(data.get("mathematical_objects") or []):
        role = (o.get("role") or "").strip()
        if EMPTY_ROLES.match(role):
            problems.append(
                f"mathematical_objects[{i}] ({o.get('name')}): role '{role}' is "
                "a presence statement, not a role. Say what work the object does.")
        if o.get("named_in_paper") is False and len(o.get("evidence", "")) < 15:
            problems.append(
                f"mathematical_objects[{i}] ({o.get('name')}): unnamed-object "
                "claim needs a substantive evidence quote")

    return problems


def main():
    p = argparse.ArgumentParser()
    p.add_argument("paths", nargs="+")
    p.add_argument("--new-only", action="store_true",
                   help="only cards modified in the last 24h")
    a = p.parse_args()

    import time
    cutoff = time.time() - 86400
    failed = 0

    for path in a.paths:
        f = Path(path)
        if not f.is_file():
            continue
        if a.new_only and f.stat().st_mtime < cutoff:
            continue
        problems = check(f)
        if problems:
            failed += 1
            print(f"FAIL {f}")
            for pr in problems:
                print(f"     {pr}")

    print(f"\n{failed} card(s) failed" if failed else "all cards valid")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
