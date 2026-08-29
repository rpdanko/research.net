#!/usr/bin/env python3
"""Runs the triage agent over the labelled set and writes eval/predictions.jsonl.

    run_triage.py prepare                  # build batches: bands, charters, exemplars
    run_triage.py run                      # optional; needs --cmd, see WHY THIS DOESN'T GUESS
    run_triage.py collect                  # validate agent output -> predictions.jsonl
    run_triage.py status                   # what's prepared, what's collected, what's missing

The missing link between a labelled set and a measured charter. `eval_triage.py
score` reads eval/predictions.jsonl; until this file existed, nothing wrote it,
so every number in WEEK-1-PLAN.md sec6 was uncomputable.

THREE PHASES, NOT ONE, AND ON PURPOSE
`prepare` and `collect` are pure Python: deterministic, testable, no model in the
loop. `run` is the only part that talks to a model, and it is the only part that
can break in ways this repo cannot predict. Keeping them separate means a failed
dispatch costs you a re-run of one batch, not a re-embedding of the whole set --
and it means the entire pipeline works with no dispatch mechanism at all: open a
prepared prompt file, paste it into a triage subagent, save the reply into the
run's out/ directory, and `collect` cannot tell the difference.

WHY `run` DOESN'T GUESS AT A CLI CONTRACT
No other script in this repo shells out to an agent, so there is no house pattern
to follow, and the exact invocation for dispatching a named subagent
non-interactively depends on tooling this script cannot verify from inside a
sandbox. Rather than ship a plausible-looking command that fails on first
contact, `run` requires an explicit --cmd (or $RUN_TRIAGE_CMD) template. Set it
once. If you would rather not, the manual path above is fully supported and is
what the two-phase split exists to make painless.

THE LEAK GUARD IS NOT DECORATION
labels.jsonl carries your `my_score` and your `stratum`. If either reaches the
model, the eval is void -- not degraded, void, because triage would be scoring
against the answer key. _batch_record() whitelists fields rather than
blacklists them: a blacklist fails open the day someone adds a field, a
whitelist fails closed.

_papers_json() then asserts the whitelist held, checking KEYS in the serialized
records rather than scanning prose. The first version scanned the whole rendered
prompt for the bare word "stratum" and fired on a math.DS abstract reading "the
grazing-incidence stratum" -- stratification being ordinary vocabulary in
singularity theory. A guard that cries wolf on real papers is worse than no
guard, because it teaches you to switch it off.

DOMAIN SCOPING, SAME BUG AS SAMPLE()
Bands are computed per-domain against that domain's canon slice, using the same
_infer_domain fallback eval_triage.py uses, because papers.sqlite's domain column
is null pre-apply_triage.py. Banding against the whole pooled canon -- 8,320
papers across four domains -- is the exact defect DAY-5-HANDOFF.md sec6.3
documents. It silently dilutes the near/mid/far separation that decides every
threshold below.
"""

import argparse, io, json, os, subprocess, sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
EVAL = ROOT / "eval"
LABELS = EVAL / "labels.jsonl"
PRED = EVAL / "predictions.jsonl"

# NOT eval/runs/ -- eval_triage.py diff() globs eval/runs/*.json for score
# summaries, and dropping batch files there would corrupt run history.
BATCH_ROOT = EVAL / "triage_runs"

BATCH_SIZE = 25            # triage.md: "up to 25 abstracts as JSON"
NEIGHBOURS_SHOWN = 3       # triage.md: "the titles of its three nearest canon papers"
MAX_REASON_WORDS = 25      # triage.md: "one sentence, max 25 words"

# Fields the model is allowed to see. Whitelist, deliberately.
BATCH_FIELDS = ("arxiv_id", "title", "abstract", "categories",
                "band", "threshold", "neighbours")
FORBIDDEN = ("my_score", "stratum")


# ------------------------------------------------------------------ shared

def _load_labels(path):
    if not path.exists():
        sys.exit(f"no {path} -- run eval_triage.py sample and label first")
    recs = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    if not recs:
        sys.exit(f"{path} is empty")
    return recs


def _resolve_domains(recs):
    """Reuse eval_triage.py's inference rather than reimplementing it."""
    sys.path.insert(0, str(Path(__file__).parent))
    from eval_triage import _infer_domain

    unresolved = []
    for r in recs:
        r["_domain"] = r.get("domain") or _infer_domain(r.get("categories"))
        if not r["_domain"]:
            unresolved.append(r["arxiv_id"])
    if unresolved:
        sys.exit(
            f"{len(unresolved)} papers have no inferable domain, e.g. "
            f"{', '.join(unresolved[:5])}.\n"
            f"Not skipping them silently: dropping papers from an eval changes "
            f"what it measures. Either widen SETS in arxiv_pull.py so their "
            f"categories map somewhere, or remove these rows from the labelled "
            f"set deliberately and note why.")
    return recs


def _band_all(recs):
    """One embedding pass over every paper, banded against its own domain slice.

    Batched on purpose: canon_index.score() reloads the model per call, which is
    fine for one paper and absurd for a few hundred.
    """
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        import numpy as np
        from canon_index import load_model, load_index, NEAR, FAR, TOP_K
    except ImportError as e:
        sys.exit(f"can't band against the canon ({e}). Need numpy, "
                 f"sentence-transformers, and canon/index.npz "
                 f"(canon_index.py build).")

    print(f"embedding {len(recs)} abstracts (one pass)...")
    model, z = load_model(), load_index()
    emb, dom_z, titles_z = z["emb"], z["domains"], z["titles"]

    texts = [f"{r['title']}. {(r.get('abstract') or '')[:1200]}" for r in recs]
    q = model.encode(texts, batch_size=64, normalize_embeddings=True,
                     show_progress_bar=True)

    for r, qi in zip(recs, q):
        mask = dom_z == r["_domain"]
        if not mask.any():
            sys.exit(f"canon has no papers for domain {r['_domain']!r}. "
                     f"Rebuild canon/index.npz or fix domain_map.yaml.")
        sims = emb[mask] @ qi
        order = sims.argsort()[::-1][:TOP_K]
        mean = float(sims[order].mean())
        band = "near" if mean >= NEAR else ("far" if mean < FAR else "mid")

        r["band"] = band
        r["threshold"] = {"near": 3, "mid": 4, "far": 5}[band]
        r["mean_top_k"] = round(mean, 4)
        r["neighbours"] = [str(titles_z[mask][i]) for i in order[:NEIGHBOURS_SHOWN]]
    return recs


def _exemplar_block(domain, _cache={}):
    """Capture canon_index.exemplars() rather than reimplement it -- the negative
    exemplars in particular carry the strike reasons, and a second copy of that
    rendering logic would drift from the first."""
    if domain in _cache:
        return _cache[domain]
    sys.path.insert(0, str(Path(__file__).parent))
    import canon_index
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            canon_index.exemplars(domain)
    except SystemExit as e:
        sys.exit(f"no exemplars for {domain}: {e}\n"
                 f"Mark Tier 0 papers with `*` in canon/vetting-{domain}.md, "
                 f"then run canon_tier.py apply.")
    _cache[domain] = buf.getvalue()
    return _cache[domain]


def _agent_body(_cache={}):
    """triage.md's body, frontmatter stripped.

    In the intended flow (daily-ingest.md) triage.md IS the subagent's system
    prompt, so a batch file only needs the charter, exemplars and abstracts.
    Any other dispatch route -- headless CLI, a general-purpose agent, hand-
    pasting -- has no system prompt, and a batch without the scale, the band
    table and the wildcard rule is not the same task. --inline-agent makes the
    prompt file self-contained so the dispatch method stops mattering.
    """
    if "body" in _cache:
        return _cache["body"]
    for cand in (ROOT / ".claude" / "agents" / "triage.md",
                 ROOT / "claude-config" / "agents" / "triage.md"):
        if cand.exists():
            text = cand.read_text()
            if text.startswith("---"):          # strip YAML frontmatter
                text = text.split("---", 2)[-1]
            _cache["body"] = text.strip()
            return _cache["body"]
    sys.exit("can't find agents/triage.md under .claude/ or claude-config/")


def _batch_record(r):
    """Whitelist. Never build this by deleting keys from the label record."""
    return {k: r[k] for k in BATCH_FIELDS if k in r}


def _papers_json(batch, name):
    """Serialize the batch, and prove nothing forbidden is in it.

    The check is on KEYS, not on prose. An earlier version scanned the whole
    rendered prompt for the bare word "stratum" and fired on a math.DS abstract
    reading "the grazing-incidence stratum" -- stratification is ordinary
    vocabulary in singularity theory, and exemplar titles and the agent body are
    equally full of innocent English. A guard that cries wolf on real papers
    gets disabled by the third time it fires, and then it guards nothing.

    So: the whitelist in _batch_record() is the actual defence, this asserts the
    whitelist held, and the string check looks only for quoted JSON keys inside
    the serialized records.
    """
    recs = [_batch_record(r) for r in batch]
    for rec in recs:
        extra = set(rec) - set(BATCH_FIELDS)
        assert not extra, (
            f"LEAK: batch {name}, paper {rec.get('arxiv_id')} carries {sorted(extra)}. "
            f"_batch_record's whitelist did not hold. Refusing to write.")
    blob = json.dumps(recs, indent=2)
    for bad in FORBIDDEN:
        assert f'"{bad}"' not in blob, (
            f"LEAK: {bad!r} appears as a JSON key in batch {name}. Refusing to "
            f"write. The eval would be scoring against its own answer key.")
    return blob


def _charter_path(domain):
    p = ROOT / "charters" / f"{domain}.md"
    if not p.exists():
        sys.exit(f"no charter at {p}")
    return p


def _render_prompt(domain, batch, idx, total, name, inline_agent=False):
    papers = _papers_json(batch, name)
    preamble = f"{_agent_body()}\n\n---\n\n" if inline_agent else ""
    return f"""{preamble}# triage batch {idx}/{total} — domain: {domain}

Charter: `{_rel(_charter_path(domain))}` — read it first, it is authoritative.

{_exemplar_block(domain)}

## Abstracts

Each carries a `band` computed before you saw it, the `threshold` that band
implies, and the titles of its nearest canon neighbours. Score on merit first,
then apply the threshold.

```json
{papers}
```

## Output

One JSON object per abstract, one per line, no prose. Every input `arxiv_id`
appears exactly once. Include `ambiguous` even when false.
"""


def _pick_run(name=None):
    """Default to the most recent run.

    predictions.jsonl belongs to exactly one run, and collect() overwrites it.
    That is the right semantics -- merging across runs would silently mix
    predictions made against different charter versions, and a metric computed
    over that mixture means nothing. The consequence is that ONE prepare should
    cover every domain you intend to score: four per-domain prepares make four
    runs, and collecting them in turn leaves you with only the last domain's
    predictions. --run exists for deliberately re-collecting an older one.
    """
    if not BATCH_ROOT.exists():
        sys.exit("nothing prepared -- run `run_triage.py prepare` first")
    runs = sorted(p for p in BATCH_ROOT.iterdir() if p.is_dir())
    if not runs:
        sys.exit("nothing prepared -- run `run_triage.py prepare` first")
    if name:
        chosen = BATCH_ROOT / name
        if not chosen.is_dir():
            sys.exit(f"no run {name!r}. Available: "
                     f"{', '.join(p.name for p in runs[-5:])}")
        return chosen
    if len(runs) > 1:
        print(f"(using most recent of {len(runs)} runs: {runs[-1].name}; "
              f"--run <stamp> to pick another)")
    return runs[-1]


# ----------------------------------------------------------------- prepare

def _rel(p):
    """str(p.relative_to(ROOT)), but never fatal.

    A bare `Path("eval/labels.dev.jsonl")` from a CLI arg is relative to
    whatever the CWD was, not to ROOT -- if __file__ resolved to an absolute
    path (Python-version- and invocation-dependent) while the CLI arg stayed
    relative, relative_to() raises. This is purely a display string for the
    manifest; it should never be the reason a run fails after the embedding
    pass has already run.
    """
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def prepare(labels_path, only_domain, inline_agent=False):
    # Anchor to ROOT regardless of invocation directory or Python's __file__
    # resolution behaviour, so downstream relative_to(ROOT) calls are sound
    # rather than merely usually-sound.
    labels_path = Path(labels_path)
    if not labels_path.is_absolute():
        labels_path = ROOT / labels_path
    labels_path = labels_path.resolve()

    recs = _resolve_domains(_load_labels(labels_path))
    if only_domain:
        recs = [r for r in recs if r["_domain"] == only_domain]
        if not recs:
            sys.exit(f"no papers in domain {only_domain!r}")

    recs = _band_all(recs)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run = BATCH_ROOT / stamp
    (run / "out").mkdir(parents=True, exist_ok=True)

    by_domain = defaultdict(list)
    for r in recs:
        by_domain[r["_domain"]].append(r)

    manifest, n_batches = {}, 0
    for domain, rows in sorted(by_domain.items()):
        chunks = [rows[i:i + BATCH_SIZE] for i in range(0, len(rows), BATCH_SIZE)]
        for i, chunk in enumerate(chunks, 1):
            name = f"{domain}-{i:02d}"
            # _papers_json asserts the whitelist held before this returns.
            text = _render_prompt(domain, chunk, i, len(chunks), name, inline_agent)
            (run / f"{name}.md").write_text(text)
            manifest[name] = [r["arxiv_id"] for r in chunk]
            n_batches += 1

    (run / "manifest.json").write_text(json.dumps({
        "labels": _rel(labels_path),
        "batches": manifest,
        "bands": dict(Counter(r["band"] for r in recs)),
        "thresholds": {r["arxiv_id"]: r["threshold"] for r in recs},
    }, indent=2))

    print(f"\nprepared {n_batches} batches over {len(by_domain)} domains "
          f"({len(recs)} papers) in eval/triage_runs/{stamp}/")
    print(f"  bands: {dict(Counter(r['band'] for r in recs))}")
    for domain, rows in sorted(by_domain.items()):
        print(f"    {domain:<20} {len(rows):>4} papers")
    print(f"\nNext: dispatch each .md to the `triage` subagent and save its JSON "
          f"lines to\n  eval/triage_runs/{stamp}/out/<batch>.jsonl\n"
          f"then run `run_triage.py collect`.")


# --------------------------------------------------------------------- run

def run(cmd_template, only, run_name=None):
    run_dir = _pick_run(run_name)
    manifest = json.loads((run_dir / "manifest.json").read_text())

    if not cmd_template:
        sys.exit(
            "run needs --cmd (or $RUN_TRIAGE_CMD): a shell template containing\n"
            "  {prompt}  path to the batch .md\n"
            "  {out}     path the agent's JSON lines must land in\n\n"
            "This script does not guess at an invocation it cannot verify --\n"
            "see the module docstring. The manual path works today:\n"
            f"  open eval/triage_runs/{run_dir.name}/<batch>.md, paste into a\n"
            f"  triage subagent, save the reply to out/<batch>.jsonl, then collect.")

    for name in sorted(manifest["batches"]):
        if only and only not in name:
            continue
        out = run_dir / "out" / f"{name}.jsonl"
        if out.exists() and out.stat().st_size:
            print(f"  {name}: already collected, skipping")
            continue
        cmd = cmd_template.format(prompt=str(run_dir / f"{name}.md"), out=str(out))
        print(f"  {name}: {cmd}")
        rc = subprocess.call(cmd, shell=True)
        if rc != 0:
            print(f"  {name}: exit {rc} -- stopping. Re-run to resume; "
                  f"completed batches are skipped.")
            return
    print("\nall batches dispatched. Run `run_triage.py collect`.")


# ----------------------------------------------------------------- collect

def _parse_lines(path):
    """Tolerate a fenced code block or stray prose around the JSON lines --
    the agent is told not to emit any, but a whole batch should not be lost to
    one stray sentence."""
    objs, junk = [], 0
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("```"):
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            junk += 1
            continue
        if isinstance(o, dict) and "arxiv_id" in o:
            objs.append(o)
        else:
            junk += 1
    return objs, junk


def collect(force, run_name=None):
    run_dir = _pick_run(run_name)
    manifest = json.loads((run_dir / "manifest.json").read_text())
    expected_thr = manifest["thresholds"]

    preds, hard, soft = {}, [], Counter()
    missing_batches = []

    for name, ids in sorted(manifest["batches"].items()):
        out = run_dir / "out" / f"{name}.jsonl"
        if not out.exists() or not out.stat().st_size:
            missing_batches.append(name)
            continue

        objs, junk = _parse_lines(out)
        if junk:
            soft["unparseable lines"] += junk

        got = Counter(o["arxiv_id"] for o in objs)
        want = set(ids)

        # triage.md: "Never skip. Every input ID appears in the output exactly once."
        for aid in want - set(got):
            hard.append(f"{name}: no prediction for {aid}")
        for aid, c in got.items():
            if aid not in want:
                hard.append(f"{name}: prediction for {aid}, which was not in the batch")
            elif c > 1:
                hard.append(f"{name}: {aid} predicted {c} times")

        for o in objs:
            aid = o["arxiv_id"]
            if aid not in want or aid in preds:
                continue

            s = o.get("score")
            if not isinstance(s, int) or not 0 <= s <= 5:
                hard.append(f"{name}: {aid} score {s!r} is not an int 0-5")
                continue

            # The band decides the threshold (triage.md). If the model returned a
            # different one, prepare()'s value wins -- score_run() reads whatever
            # is stored here, so letting the model move its own goalposts would
            # quietly change what "admitted" means.
            if o.get("threshold") != expected_thr.get(aid):
                soft["threshold overridden by model"] += 1
            o["threshold"] = expected_thr.get(aid)

            if "ambiguous" not in o:
                soft["missing `ambiguous` key"] += 1
                o["ambiguous"] = False
            if o.get("ambiguous") and not str(o.get("reason", "")).startswith("["):
                soft["ambiguous without a bracketed tag"] += 1

            # triage.md: far-band papers scored >=4 must carry wildcard.
            if o.get("band") == "far" and s >= 4 and not o.get("wildcard"):
                soft["far-band >=4 missing wildcard"] += 1
                o["wildcard"] = True

            if len(str(o.get("reason", "")).split()) > MAX_REASON_WORDS:
                soft["reason over 25 words"] += 1

            preds[aid] = o

    print(f"run: eval/triage_runs/{run_dir.name}")
    if missing_batches:
        print(f"\n  {len(missing_batches)} batches have no output yet: "
              f"{', '.join(missing_batches[:6])}"
              f"{' ...' if len(missing_batches) > 6 else ''}")

    if soft:
        print("\n  contract warnings (repaired where repairable):")
        for k, v in soft.most_common():
            print(f"    {v:>4}  {k}")

    if hard:
        print(f"\n  {len(hard)} STRUCTURAL errors:")
        for h in hard[:15]:
            print(f"    {h}")
        if len(hard) > 15:
            print(f"    ... and {len(hard) - 15} more")
        if not force:
            sys.exit(
                "\nRefusing to write predictions.jsonl. Missing or duplicated\n"
                "predictions change the denominator of every metric downstream,\n"
                "and a recall number computed over a silently shrunken set is\n"
                "worse than no number. Re-run the affected batches, or pass\n"
                "--force if you have decided the gap is acceptable and will say\n"
                "so when you report the result.")
        print("\n  --force: writing anyway.")

    if not preds:
        sys.exit("nothing collected")

    with PRED.open("w") as f:
        for aid in sorted(preds):
            f.write(json.dumps(preds[aid]) + "\n")

    dist = Counter(p["score"] for p in preds.values())
    print(f"\n  wrote {_rel(PRED)}  ({len(preds)} predictions)")
    print(f"  score distribution: {dict(sorted(dist.items()))}")
    print(f"  wildcards: {sum(1 for p in preds.values() if p.get('wildcard'))}   "
          f"ambiguous: {sum(1 for p in preds.values() if p.get('ambiguous'))}")
    print("\nNext: eval_triage.py score")


# ------------------------------------------------------------------ status

def status(run_name=None):
    run_dir = _pick_run(run_name)
    manifest = json.loads((run_dir / "manifest.json").read_text())
    print(f"run: eval/triage_runs/{run_dir.name}   labels: {manifest['labels']}")
    print(f"bands: {manifest['bands']}\n")
    done = 0
    for name, ids in sorted(manifest["batches"].items()):
        out = run_dir / "out" / f"{name}.jsonl"
        n = len(_parse_lines(out)[0]) if out.exists() else 0
        done += bool(n)
        mark = "ok " if n == len(ids) else ("part" if n else "-   ")
        print(f"  {mark} {name:<24} {n:>3}/{len(ids)}")
    print(f"\n{done}/{len(manifest['batches'])} batches have output")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        epilog="Start with: run_triage.py prepare --domain stats",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # dest is "action", not "cmd" -- the `run` subcommand defines --cmd, and two
    # arguments writing the same namespace attribute means the flag silently
    # overwrites the subcommand name.
    sub = ap.add_subparsers(dest="action", required=True, metavar="{prepare,run,collect,status}")

    p = sub.add_parser("prepare")
    p.add_argument("--labels", default=str(LABELS),
                   help="defaults to eval/labels.jsonl; point at labels.dev.jsonl "
                        "if the protocol rename has happened")
    p.add_argument("--domain", help="restrict to one domain")
    p.add_argument("--inline-agent", action="store_true",
                   help="prepend triage.md's body so the prompt file is "
                        "self-contained. Needed for any dispatch route where "
                        "triage.md is not already the system prompt.")

    r = sub.add_parser("run")
    r.add_argument("--cmd", default=os.environ.get("RUN_TRIAGE_CMD"))
    r.add_argument("--only", help="substring match on batch name")
    r.add_argument("--run", dest="run_name", help="run stamp; default is latest")

    c = sub.add_parser("collect")
    c.add_argument("--force", action="store_true")
    c.add_argument("--run", dest="run_name", help="run stamp; default is latest")

    s = sub.add_parser("status")
    s.add_argument("--run", dest="run_name", help="run stamp; default is latest")
    a = ap.parse_args()

    if a.action == "prepare":
        prepare(Path(a.labels), a.domain, a.inline_agent)
    elif a.action == "run":
        run(a.cmd, a.only, a.run_name)
    elif a.action == "collect":
        collect(a.force, a.run_name)
    else:
        status(a.run_name)


if __name__ == "__main__":
    main()
