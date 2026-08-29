# compbio_mechanism.md — rewrite prep

Working document, not a charter. Purpose: put every §2/§3 rule next to the vetting
evidence it was derived from, so you can rewrite in your own words while looking at
what you actually wrote, rather than at my paraphrase of it.

Line numbers refer to `canon/vetting-compbio_mechanism.md`. Reasons are verbatim,
typos included.

**Why this domain first.** `OPEN-QUESTIONS.md` §2.2 picked it because it holds the
largest inference-from-strike-reasons in the set, and §1.5 confirms its labels cannot
help: 10 labelled rows, only 3 scoring ≥4. The charter here rests on strike reasons
almost entirely. That makes this document the main check on it.

**How to use this.** §A is the four places the charter and the evidence disagree —
each has a `RULING:` line, write on it. §B is the routine rule-to-evidence mapping,
for spot-checking. §C is what the evidence contains that the charter never mentions.
§D is a prompt-pipeline defect found while building this; it is not a charter question
but it changes what triage actually sees, so it belongs in the same sitting.

**Status 2026-08-28. All four rulings made and applied.** What remains is not a charter
question but two **[shell]** propagation steps, and one thing that is neither:

- `python3 ingest/canon_tier.py apply` — until this runs, A2's two reversals and all ten of
  A4's rewrites exist only in the worksheet. `exemplars()` reads the canon records.
- `python3 ingest/canon_index.py exemplars --domain compbio_mechanism` — eyeball the block
  afterwards; it also settles §D's cross-domain-reason question.
- **§3 itself is still unwritten.** A3 ruled that a molecular-scale criterion belongs there
  and A1 corrected §8's narrative, but no criteria text has been added to §3 by anyone.
  `README.md` asks for that in your hand, and the rewrite-prep deliberately stops short of it.

**Vetting totals:** 150 papers, ~128 strikes, ~22 keeps. Strike-reason clusters:
package/tool/program papers **~47** · sequencing & genomics **~29** ·
disease- or condition-specific **17** · vague ("not relevant to me") **~10** ·
evolutionary biology & phylogenetics **9** · scale-mismatch (above and below the
molecular level) **8** · dataset/database releases **5** · laboratory methods **2** ·
administrative **1**.

---

## §A. Four places the charter and the evidence disagree

### A1. §8's central factual claim is overstated

**Charter says** (§8, the paragraph justifying the tooling reframe): *"Nearly every
paper struck under 'I do not do sequencing work' was a software announcement:
SAMtools, BWA, Trimmomatic, minimap2, Kraken2, HTSeq, fastp, TopHat2, and so on."*

**The evidence is more mixed than that.** The sequencing cluster (~29 strikes) contains
at least three papers that are not software announcements at all:

- line 29 — *Initial sequencing and analysis of the human genome* (Nature 2001,
  24,703 cites): `I do no work on genome sequencing`. A result-and-resource paper.
- line 41 — *A global reference for human genetic variation* (1000 Genomes):
  `I do not do work on genome sequencing`. A resource release.
- line 59 — `I do not do work in genomics`, on a paper struck for the field, not the
  artifact.

**Why it matters.** §8 uses that claim to justify restating the rule as *data-processing
tooling* rather than *genomics*, on the grounds that the software criterion catches
everything anyway. For most of the cluster it does. For genome-resource papers it does
not — those are caught, if at all, by §3's *dataset, cohort, and resource releases*
bullet, which §8 never mentions in this argument. The reframe still looks right, but it
is carried by two §3 bullets rather than one, and the charter should say so.

`RULING: Minor correction — applied 2026-08-28.` §8 now reads "Most papers struck under…"
rather than "Nearly every paper," and carries a dated note naming the three
genome-result/resource papers the software criterion does not reach, plus the point that
the reframe depends on **both** §3 bullets surviving, not just the software one.

Note this touched only §8's narrative. **§3's criteria text is unchanged** and still awaits
your handwriting, per `README.md` — this correction does not substitute for that.

---

### A2. The popgen/phylogenetics admission rests on a claim the worksheet cannot confirm

**Charter says** (§8): *"The number of theory papers in that literature you rejected on
evolutionary-biology grounds is small."* This is the load-bearing sentence for the
single largest scope decision in the charter — admitting population-genetics and
phylogenetics theory against your own stated "I do not work on evolutionary biology."

**RESOLVED 2026-08-28 — the eight titles were read.** The reasons alone could not
distinguish theory from tooling (only 599 names it), so the papers themselves were
checked. All nine:

| Line | Paper | What it actually is | Theory? |
|---|---|---|---|
| 155 | *TNT, a free program for phylogenetic analysis* | software announcement | no |
| 263 | *Niche Construction: The Neglected Process in Evolution* | theory monograph; abstract cites "theoretical population genetics" | **yes** |
| 341 | *Inferring the mammal tree* | inference pipeline + downloadable tree resource, ~6,000 species | no |
| 389 | *Five Rules for the Evolution of Cooperation* (Nowak, Science 2006) | evolutionary game theory — kin selection, direct/indirect/network reciprocity, group selection | **yes** |
| 509 | *A Rapid Bootstrap Algorithm for the RAxML Web Servers* | software + web server | no |
| 545 | *Site-specific genetic divergence in parallel hybrid zones* | empirical popgen result (microsatellites, *Littorina*) | no |
| 581 | *DESATURASE-2 … in Drosophila melanogaster* | empirical evolutionary genetics result | no |
| 599 | (phylogenetics package paper) | software announcement | no |
| 899 | *The Draft Genome of Ciona intestinalis* | genome resource release | no |

**§8's claim is substantively correct: two of nine.** Four are caught by §3's
software/resource rules, three more are empirical results rather than theory, and after
the §A3 ruling four of them (341, 545, 581, 899) are additionally caught by the
molecular-scale bound. The sentence should be restated as measured — "two of the nine
evolutionary-biology strikes were theory papers" — rather than asserted.

**But the two that remain are not incidental. They are the exact papers §2 now admits
by name.**

- **389, Nowak's *Five Rules*, is the canonical paper of the evolutionary game theory of
  cooperation.** §2's sixth bullet admits *"game-theoretic and economic models of
  biological cooperation"* — "admitted by name" — and §5 flags every instance as
  `[econ-bio-cooperation]`.
- **263, *Niche Construction*, is a theoretical-population-genetics monograph.** §2's
  seventh bullet admits *"population-genetics and phylogenetics theory"* as of this pass.

So the charter's two newest §2 admissions each have a high-citation counterexample sitting
in the worksheet marked `S`, with a strike reason that reads as a flat field rejection.
This is `EVAL-01-FINDINGS.md` §4B's mechanism precisely — frozen exemplars silently
overriding revised charters — and here it is pointed at the two criteria the charter is
least sure of.

**The risk is getting worse, not better.** Both papers are heavily cited (5,945 and
2,950). Under the old `[:6]`-over-citation-order exemplar selection they sat behind the
tooling bulk; under Week 2's bucketed round-robin with the default raised to 10, a
distinct-genre strike becomes *more* likely to surface, not less. If either is rendered
into the negative block, triage will be told to reject the thing §2 says to admit.

**Three coherent responses:**

1. Reverse both marks to `k` — the charter changed, the judgments should follow it.
2. Keep the marks, set `strike_superseded` on both (the `EVAL-01-FINDINGS.md` §4B/B2
   field), preserving the vetting record while keeping them out of the prompt.
3. Keep them struck and narrow §2 — decide that the cooperation and popgen-theory
   admissions were too broad, and say what they exclude.

`RULING: Option 1 — both flip to keep. Confirmed 2026-08-28. APPLIED: both marks in`
`canon/vetting-compbio_mechanism.md are now k, with keep reasons naming the §2 criterion`
`that admits each and recording the reversal.`

**This is not finished until the marks are propagated [shell].** `exemplars()` reads
`canon_records()`, not the worksheet — positives are `tier == 0`, negatives are
`vetted == "struck"` with a `strike_reason`. Until `canon_tier.py apply` runs, both papers
are still `struck` in the canon records and both are still eligible for the negative block.
Run it before the next triage dispatch:

```bash
python3 ingest/canon_tier.py apply          # propagate the worksheet marks
python3 ingest/canon_index.py exemplars --domain compbio_mechanism   # eyeball the block
```

**Open sub-question: should either be marked `k*` (tier-0 exemplar)?** Not ruled on. The
worksheet header aims for 25 exemplars; this domain rendered 21 on 2026-08-27 and three were
demoted in the Week 2 session, so it is now at ~18. These two are the strongest available
positives for the two §2 criteria with the least evidence behind them, and putting them in
the *positive* block would state the admission rather than merely removing a contradiction.
Recommended, but it changes the prompt, so it is a separate call. Plain `k` for now.

---

### A3. Scale mismatch — struck 8 times, in §1's framing, absent from §3

**You wrote:**

*Above the molecular level:* line 455 `I do not work in epidemiology but this sounds
pretty interesting` · 569 `Specific to oceanography` · 677 `I work at the molecular
level and this seems to be be studying things at the level of higher-order organisms`
· 785 `Specific to marsupials` · 863 `Specific to oceans` · 869 `I don't work on ocean
data`.

*Below the molecular level:* line 245 `I do not do any work in the study of force
fields but this sounds highly interesting` · 845 `Specific to atomic modeling which I
have not dipped into yet`.

**Charter says:** §1's framing note quotes `I work on molecular biological processes
and pathways` (line 275) as evidence that the exclusions are about fit. §3 contains no
scale criterion at all.

**Why this is the most consequential gap.** The domain is bounded on *both* sides — you
rejected ecology and epidemiology above, and force-field and atomic physics below — and
§3 encodes neither bound. Nothing in the current §3 excludes a statistical-mechanical
model of an ecosystem, or a molecular-dynamics force-field paper. Both would sail
through §2's *stochastic and dynamical models of biological systems* bullet.

Note the live consequence: `OPEN-QUESTIONS.md` §2.3 flags line 80 of the label set —
a cytoskeletal statistical-mechanical framework you scored **2** despite it sitting in
the centre of §2. A scale criterion would not explain that one (cytoskeleton is
molecular), but the same absence is why §2 currently over-claims.

Three positions, and the charter holds none:

1. A scale bar in §3 — "systems above the cell or below the molecule are out."
2. A §5 flag — admitted but visible, on the grounds that scale is where bridges hide.
3. Nothing — accept that eight strikes were personal fit and don't generalize.

`RULING: Option 1 — confirmed 2026-08-28. "I work at the molecular level." The bound is`
`real and it is two-sided. §3 needs a scale criterion excluding work above the cell`
`(ecology, epidemiology, organism- and population-level biology) and below the molecule`
`(force fields, atomic modelling), with the existing §2 admissions unaffected.`

**Knock-on effects, both already visible:**

- It resolves four of the nine evolutionary-biology strikes in §A2 on their own terms —
  341 (mammal tree, ~6,000 species), 545 (*Littorina* hybrid zones), 581 (*Drosophila*),
  899 (*Ciona* genome) are all organism- or population-level, struck for the field but
  excluded by scale regardless of field.
- It sharpens the §2 popgen-theory admission rather than contradicting it. Coalescent
  theory, Wright-Fisher and Moran processes are *mathematical* objects; a scale bar
  written about the biological system studied does not touch them. Worth saying so
  explicitly in §3, because "population genetics" reads as population-level on its face
  and a triage agent will make that mistake unless told otherwise.

---

### A4. Ten strike reasons say nothing a triage agent can use

**You wrote:** line 137 `Seems too specific and I don't work in this area` · 209 `This
seems very specific to work that I am not interested in, but it does sound very
interesting.` · 251 `Really interesting but not at all relevant to what I do` · 257
`Really interesting but not relevant to what I do` · 269 `Specific to one application,
but does seem interesting` · 347 `This seems specific to one application that has
nothing to do with what I'm working on` · 743 `Not relevant to this study` · 791 `Not
relevant to me` · 911 `Not relevant`. Plus line 71 `Cannot seem to get an open access
copy, abstract is uninformative` — not a scope judgment at all.

**Why this matters more here than it would elsewhere.** The worksheet's own header says
strike reasons *"become the negative exemplars in the triage prompt and matter more than
the keeps."* A negative exemplar reading `Not relevant` teaches an agent nothing except
that rejection can be arbitrary — which is the exact failure mode
`EVAL-01-FINDINGS.md` §4B describes, where a frozen exemplar silently overrides a
charter rule.

These ten are ~8% of the strike pool and they are eligible for selection into the
6-to-10 negative block. Either rewrite them against the criterion that actually applies,
or mark them `strike_superseded` (the field §4B's B2 proposes) so they stay in the
vetting record but out of the prompt.

`RULING: Rewrite — applied 2026-08-28.` All ten papers were read and each reason now names
the criterion that actually applies. Every original is preserved verbatim in brackets on
the same line, so nothing you wrote is lost and any rewrite can be checked against it.
`strike_superseded` was deliberately **not** used: these strikes were correct, merely
badly worded, and that field means "a judgment the charter has since overruled." Using it
for vagueness would corrupt its meaning for the cases in §A2 that genuinely need it.

**How the ten resolved:**

| Criterion the reason now names | n | Lines |
|---|---|---|
| Above the molecular level (per §A3) | 5 | 137, 209, 251, 257, 347 |
| Outside computational biology altogether | 3 | 743, 791, 911 |
| §3 software announcement | 1 | 71 |
| §3 disease-specific finding | 1 | 269 |

**Two things worth keeping from the exercise.**

*The scale bound was doing most of the work invisibly.* Five of the ten vague strikes were
scale rejections you had no vocabulary for at vetting time — which is why they came out as
"not relevant to what I do." §A3's ruling gives them a name retrospectively, and it is the
same bound in each case.

*A genre appeared that no §3 bullet covers:* **LLM/NLP work on text with no biological
content at all** — line 743 (information extraction, demonstrated on materials chemistry),
791 (clinical note summarisation safety), 911 (ChatGPT in scientific writing). These are not
near misses inside the domain; they are outside it. They presumably entered the canon slice
by citation adjacency rather than subject. Two implications:

1. As negative exemplars they are close to useless — the block is meant to hold *traps*,
   topically adjacent papers, and these are not adjacent to anything in §2.
2. Line 743 is `W4391836235`, *Structured information extraction from scientific text with
   large language models* — **the LLM-NERRE paper `README.md` cites for card-accuracy manual
   scoring.** It is directly useful to this project and not KB material, which is exactly the
   metatool-shelf pattern `EVAL-01-FINDINGS.md` §5 step 2 says needs a home. That home still
   does not exist, and the pattern has now recurred in a second domain.

---

## §B. Routine mapping — rules that the evidence supports

Spot-check only; nothing here needs a decision.

| Charter rule | Evidence | Verdict |
|---|---|---|
| §3 *software and package announcements* | ~47 strikes, lines 125, 149, 185, 227, 239, 305, 335, 359–401, 425–497, 515–557, 599, 623–695, 719, 767–779, 815–905 | **Strongest rule in the charter.** §3's "largest struck category by a wide margin" is correct: 37% of all strikes. |
| §3 *sequence data-processing tooling* | ~29 strikes, lines 29–233, 293–419, 479–521, 635–725, 761, 797, 893 | Well supported. See A1 for the one overstatement. |
| §3 *disease- or condition-specific findings* | 17 strikes: cancer 83/101/749/803/887, Alzheimer's 131/461, neuro 107/287, plus 587 depression, 629 anorexia, 641 antibiotic, 701 aphasia, 737 diabetes, 755 & 317 drug | Well supported, and the "unless the contribution is a general-purpose modelling method" escape is doing real work — it is what demoted 83, 107 and 131 from exemplar to strike this pass. |
| §3 *dataset, cohort, and resource releases* | 5 strikes: 89, 437, 551, 611, 773 | Supported, and quietly load-bearing per A1. |
| §3 *laboratory and wet-bench protocol papers* | 2 strikes: 575, 593 | Thin (n=2) but unambiguous, and the genre is distinctive enough that two is probably enough. |
| §2 *protein structure and interaction modelling* | The keep pool: AlphaFold (line 17, `part of the general program of leveraging biological and physical knowledge into the design of learning algorithms`), AlphaFold 3, ESMFold, RFdiffusion | Well supported. |

---

## §C. In the evidence, absent from the charter

- **The scale bound, both directions** — see A3. The largest genuine omission.
- **"Interesting but not load-bearing"** (lines 23, 35, 47) — you used *load-bearing*
  three times as a strike criterion, and §2 uses the same phrase as an *admission*
  criterion ("where the biology is structurally load-bearing"). The term is doing two
  different jobs. In your strikes it means "not central to my research"; in §2 it means
  "not removable from the method." Worth disambiguating, because triage sees both.
- **"Included in the genomics canon"** — a bookkeeping note, not a scope judgment. See
  §D; it is currently being shown to the model as a reason to reject.

---

## §D. Not a charter question — a prompt-pipeline defect found while building this

Checked against the actual dispatch prompt at
`eval/triage_runs/20260827-203053/compbio_mechanism-01.md`. Its negative-exemplar block
holds six entries. **Three of them carry strike reasons written in other domains'
worksheets:**

| Exemplar shown | Reason shown to triage | Where the reason was written |
|---|---|---|
| *Correlation Coefficients: Appropriate Use and Interpretation* | `Too rudimentary to be helpful` | `vetting-stats.md:539` |
| *Why 90% of clinical drug development fails* | `Specific to drug development` | `vetting-stats.md:751` |
| *Tensor-Train Decomposition* | `Included in the genomics canon` | `vetting-compbio_methods.md:29` |

Two of the remaining three are the same STROBE-MR paper twice, leaving *RAxML* as the
only distinct negative exemplar actually drawn from this domain's own judgments.

Two consequences, both concrete:

1. **The single largest strike genre in this domain — package/tool papers, ~47 of 128 —
   is not represented in the negative block at all.** The model was shown zero examples
   of the thing you reject most often.
2. **`Included in the genomics canon` is not a scope judgment.** It means "this paper
   lives in another domain's slice." Presented as a rejection rationale, it is noise at
   best.

The `[:6]`-over-citation-order selection bug was fixed in Week 2 (bucketed round-robin,
default 6→10), which should fix (1). It does **not** obviously fix the cross-domain
reason provenance, which is a different question: `exemplars()` selects records by the
domain's canon slice, but `strike_reason` comes from whichever worksheet happened to
mark that record. Worth confirming against a freshly rendered prompt before the next
triage run — if it persists, it is a `canon_index.py` fix, not a charter one.

**Also worth knowing before the next render:** the 2026-08-27 prompts showed 21 tier-0
exemplars for this domain. Three were demoted to strikes in the Week 2 session
(lines 83, 107, 131 — breast cancer, GABAergic epigenetics, Alzheimer's). Expect the
next render to show ~18, and expect the negative block to change composition
substantially now that both fixes are in. Do not read a score change across that
boundary as a charter effect.
