# Week 1 — Build the canon, derive the charters, measure the triage

The original Week 1 was "run ingest and triage, tune the charters by reading output." That works but it is slow and unmeasured: you would be rewriting prose charters based on impressions, with no way to tell whether an edit helped.

Grounding the charters in a **canon of influential papers** is the better version of the same idea, and it is the same principle as the rubric anchors — a specification grounded in exemplars beats a specification made of adjectives. The canon is to the charter what critical incidents are to a BARS scale.

Scope: 2000–present, ~2000 papers per domain, with a hand-vetted core.

---

## 1. The thing to get right before anything else

**A large canon and a good triage prompt are two different projects, and conflating them is the main way this goes wrong.**

The instinct behind "a large base of influential papers so triage can evaluate relevance" is right, but "large" helps in a way that is not the way it first appears. Two thousand papers per domain is far too many to put in front of a model — and even if you could, it would not help. Beyond roughly twenty well-chosen exemplars, additional examples do not sharpen an LLM's category judgment; they dilute it.

What a large canon *is* good for is **deterministic, zero-token filtering**: citation overlap, author overlap, similarity ranking. Those are the jobs where 2000 beats 300 and where scale genuinely pays.

So the canon gets split by job:

| Tier | Size / domain | Vetting | Consumed by |
|---|---:|---|---|
| **0 — Exemplars** | 25 | Hand-picked by you | The triage **prompt**. Never more than this. |
| **1 — Core** | 150 | Abstracts read (your 3 hours) | **Charter derivation**, and the similarity index |
| **2 — Shell** | ~2000 | Title-skim only | Citation overlap, similarity index, drift detection |

Tier 0 is a subset of Tier 1, which is a subset of Tier 2. One file, three flags.

---

## 2. Getting "influential" right over a 25-year window

Raw citation counts across 25 years are useless: a 2003 paper beats a 2023 paper on volume alone, and a canon built on raw counts would be a museum.

**Use OpenAlex's `citation_normalized_percentile`**, which normalizes by work type, publication year, and subfield — the same information as FWCI, expressed as a percentile. Then take a **fixed quota per year**: 80 papers per domain per year × 25 years = 2000. This makes the canon uniform across the window by construction and means recent work is never crowded out.

### Why OpenAlex

Free, no key required, covers journals as well as preprints (important — a canon of only arXiv papers would badly skew statistics pre-2015 and computational biology in general), and exposes `referenced_works`, which is what the citation-overlap filter needs. Include your email in the `mailto` parameter; OpenAlex asks for it and service is more reliable with it. Watch for 403 (slow down) and 429 (daily limit).

### The subfield problem you will hit immediately

OpenAlex's taxonomy is `domain > field > subfield > topic`, 254 subfields, derived from Scopus ASJC. **Statistics and Probability is a single subfield.** Your KBs need them separate.

So domain assignment happens at the **topic** level, not the subfield level, using a map you edit yourself:

```yaml
# canon/domain_map.yaml
stats:
  topics: [T10521, T11423, ...]     # inference, estimation, experimental design
probability:
  topics: [T10883, T12044, ...]     # stochastic processes, random matrices
compbio:
  subfields: [1312, 1311]            # molecular biology, genetics
  topics: [...]
```

`canon_harvest.py resolve` queries OpenAlex, prints candidate topics with names and work counts, and writes a starter map. **Editing that map is the first real decision you make this week** — it is a charter in numeric form, and it is worth an hour.

### What the automated pass will get wrong

Citation percentile finds influential papers, not papers useful to *this* system. It will hand you:

- **Tool and software papers.** Enormously cited, methodologically empty. BLAST, Bowtie, limma, Seurat. A canon full of these teaches triage that compbio means software announcements.
- **Reviews and benchmarks.** High citations, no method.
- **Consortium and resource papers.** Same problem, larger author lists.
- **Papers influential for reasons orthogonal to method** — a dataset everyone used, a controversy.

This is exactly what your 3 hours of vetting is for, and it is why the vetting is not optional. Strike these from Tier 1. Leave them in Tier 2 — for citation-overlap purposes a tool paper is a perfectly good signal that a new paper is in the neighbourhood.

---

## 3. How triage actually consumes the canon

Three signals, fused by a rule simple enough to audit.

### Signal A — Exemplars in the prompt (LLM, day one)

Tier 0's 25 papers per domain go into the triage prompt as title + one-line "why this is in scope," alongside **five deliberate near-misses**: highly-cited papers in the neighbourhood that are *out* of scope, with the reason. Negative exemplars do more work than positive ones — they are what stop the model from admitting on topical adjacency.

Roughly 3k tokens per domain, entirely cacheable. This is the whole of the LLM's contact with the canon.

### Signal B — Similarity to Tier 1/2 (deterministic, day one)

Embed all canon abstracts with a **local** sentence-transformer (`all-MiniLM-L6-v2` or similar). Zero API cost, runs on a laptop, ~6000 abstracts in under a minute. For each new paper, retrieve the top-5 nearest canon papers and their cosine scores.

This is not fed to the model as a score to obey. It becomes a **band** — `near` / `mid` / `far` — that adjusts the admission threshold, and the top-3 matched titles get shown to the model as context. A model told "0.83 similarity" will anchor on the number; a model shown "the closest things we already trust are these three papers" reasons better.

> This is the vector-search I argued against in the architecture doc, and the distinction is real: for *intersection-finding*, embeddings surface exactly the "both use entropy" slop the skeptic exists to kill, because semantic similarity is not structural identity. For *relevance triage*, semantic similarity is the actual question being asked. Use it here, keep it out of bridge-finding.

### Signal C — Citation overlap (deterministic, but lagged)

Does the new paper cite anything in Tier 2? Two or more canon references is a strong in-scope signal, close to free.

**The catch, and do not build around it without knowing this:** OpenAlex needs days to weeks to index a new arXiv preprint and extract its references. On the day a paper appears, this signal is usually *absent* — and absence is not evidence of no overlap. A prefilter that treats missing reference data as zero overlap will silently penalize the newest papers, which are the entire point of a streaming system.

So citation overlap does **not** gate the live decision. It runs on a **14-day lag** as a *corrector*: `citation_overlap.py --audit` re-scores papers triaged two weeks ago and reports where the citation signal disagrees with the triage verdict. Those disagreements are your best charter-tuning material — a rejected paper that turns out to cite five canon works is a charter gap with a name on it.

### The fusion rule

```
base threshold: admit at score >= 4

similarity band 'near' (top-5 mean cosine >= 0.62):  admit at >= 3
similarity band 'far'  (top-5 mean cosine <  0.38):  admit at >= 5
```

Not a weighted model. A threshold shift, logged per paper, that you can read and argue with. The daily per-domain cap of 10 remains the real volume governor; the threshold decides ranking, not floodgates.

---

## 4. Two hazards worth designing against now

### The canon makes triage conservative — by construction

A system anchored on what is already influential will reliably admit papers resembling what is already influential, and reliably miss the genuinely novel. That is a bad property in general and an actively self-defeating one here, because this network exists to find creative intersections, and intersections live precisely where the existing canon has nothing to match against.

**Mitigation — the wildcard quota.** Reserve **15% of each day's admissions** (so 1–2 of the 10 per domain) for papers in the `far` similarity band that scored well on the charter alone. These are admitted *because* the canon does not recognize them. Tag them `wildcard: true` in the card and track them: if in six months no wildcard card has ever participated in a bridge, drop the quota. If wildcards are over-represented in bridges — which is my expectation — raise it.

This costs about $0.02/day and is the cheapest insurance in the system.

### Recall matters far more than precision here

The two errors are not symmetric, and the default instinct gets this backwards.

- A **wrongly admitted** paper costs ~$0.03 for a card nobody uses, and gets filtered again at every downstream stage.
- A **wrongly rejected** paper is gone. Nothing downstream can recover it, and you will never know it existed.

So tune the threshold for recall, and let the daily cap and the downstream gates handle precision. In the eval harness, weight recall roughly 3:1 against precision. If you find yourself proud of a high-precision triage, you have optimized the wrong thing.

---

## 5. Day by day

**Day 1 — Harvest.** Run `canon_harvest.py resolve`, edit `canon/domain_map.yaml`, run the harvest. Expect 20–40 minutes of runtime and a few hours of your attention on the topic map. Output: `canon/canon.jsonl`, ~6000 works.

**Day 2 — Tier and skim.** `canon_tier.py` ranks within domain and emits vetting worksheets. Title-skim the full 2000 per domain (fast — you are only striking obvious misfits) and mark the Tier 1 candidates. Output: Tier 2 clean, Tier 1 nominated.

**Day 3 — Vet the core (your 3 hours).** Read 150 abstracts per domain. For each, mark keep/strike and, when you strike, **write one line saying why.** Those lines are worth more than the keeps — they are the negative exemplars for Signal A and the raw material for the charter's out-of-scope section. Then hand-pick 25 Tier 0 exemplars per domain.

**Day 4 — Derive charters, build the index.** Dispatch an Opus pass over the Tier 1 abstracts per domain to propose a charter, then **rewrite it yourself.** The model's version is a first draft that has read 150 papers; the judgment has to be yours. Run `canon_index.py build`.

**Day 5 — Build the labeled eval set.** Sample 150 papers from a recent arXiv window, stratified: 50 you expect in, 50 out, 50 genuinely borderline. The borderline stratum is the only one that will teach you anything — a labeled set of easy cases measures nothing. Score them yourself 0–5 before running triage on them even once.

**Days 6–7 — Measure and tune.** Run `eval_triage.py score`, read the confusion matrix and the disagreements, edit the charter or the exemplars, re-run. Each cycle costs about six cents. Aim for five or six cycles.

**The human bottleneck is Days 3 and 5**, and both will probably slip. That is fine — nothing downstream starts until Week 2, and a rushed labeled set is worse than a late one.

---

## 6. What "done" looks like

Week 1 is complete when `eval_triage.py score` reports:

- **Recall ≥ 0.90** on your labeled in-scope papers. Below this, the charter is too narrow; look at what was missed before touching anything else.
- **Precision ≥ 0.60.** Lower is tolerable. Much higher probably means recall is being bought away.
- **Borderline-stratum agreement ≥ 0.70** within ±1 of your score. This is the number that actually matters and the one that will be worst.
- **No systematic miss** — the false negatives should look random, not like a coherent subfield you forgot to describe.

And, qualitatively: you should be able to read ten triage `reason` strings and agree with eight of them for the stated reason, not just agree with the verdict. Agreeing with the verdict for the wrong reason is how a charter passes eval and fails in production.

---

## 7. Cost

| Item | Cost |
|---|---:|
| OpenAlex harvest (6000 works) | $0 |
| Local embeddings (6000 abstracts) | $0 |
| Charter derivation, 3 domains, Opus | ~$0.83 |
| Eval cycles, ~6 runs × 150 papers, Haiku | ~$0.40 |
| Live triage, days 5–7 | ~$0.21 |
| **Week 1 total** | **~$1.50** |

The canon is essentially free. Everything expensive about Week 1 is your time, which is the correct place for it to be.

Ongoing, the canon adds about **$0.01/day** to triage (the exemplar block, cached) and zero to everything else. The similarity index is refreshed quarterly, not daily.

---

## 8. Failure modes

**The canon becomes a museum.** Symptom: the yearly quota is met but post-2020 entries are sparse because recent papers have not accumulated percentile yet. Check the year histogram in `canon_tier.py --stats`. If the last three years are thin, lower the percentile floor for those years specifically rather than accepting the skew.

**Vetting fatigue on Day 3.** Three hours of abstracts is genuinely tiring and quality drops in the last hour. Do it in two sittings, and do the domain you know *least* well first, while attention is fresh.

**Charter overfits the canon.** If the derived charter reads like a description of the 150 papers you vetted rather than a specification of what you want, it will admit only more of the same. The test: does the charter admit a hypothetical paper that does something new in this area? Write one such abstract yourself and check.

**Silent embedding drift.** If you ever change the embedding model, every stored similarity is invalid. `canon_index.py` records the model name and dimension in the index header and refuses to score against a mismatch.

**Wildcard quota quietly unused.** If `far`-band papers never clear even the relaxed bar, the quota is decorative. `eval_triage.py score` reports the wildcard admission count; if it is zero over a week, the far-band threshold needs lowering, not the quota removing.
