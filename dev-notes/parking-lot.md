# Parking lot — papers useful to the project, not to any KB

A third bucket the charters don't have. Every charter recognizes two outcomes for a
paper: belongs in this domain's KB, or doesn't. Nothing catches a paper that is useful
to **how the project itself works** — a technique for an agent this repo runs, or
background a curator needs to read a paper it does hold — without being an object of
study for any domain. Forced through a charter, such a paper is either admitted on the
wrong pretext or correctly rejected and then genuinely lost, because a triage rejection
isn't retrievable later.

Two flavors so far, kept in one file per `EVAL-01-FINDINGS.md` §5 — split into separate
files only if volume ever justifies it:

- **Agent-design references** — prior art for `bridge-finder`, `project-architect`,
  `triage`, or any agent this repo runs. Read by whoever next revises that agent, not
  ingested as a card.
- **Background references** — toolkit material a curator or you might want on hand when
  a paper name-drops machinery without explaining it. Read on demand.

Not `rubrics/` — that shelf is evaluation criteria for judging this project's own
proposals (novelty, feasibility, relevance), a different job from either of these.

**How something lands here:** no automated tag. Detecting "this paper is about the
project's own construction" requires knowing the project's architecture, which
`triage.md`'s classifier deliberately doesn't — it stays domain-general on purpose, and
teaching it a third category risks the same false-positive problem the charters already
have. This is caught by you, the same way the two entries below were: during labelling,
the five-raw-abstracts habit, or the weekly digest. Add an entry, and — if it came from
`eval/labels.jsonl` — drop the label's score to reflect no-KB-scope so it stops reading
as a charter miss (see `EVAL-01-FINDINGS.md` for two already fixed this way).

---

## Agent-design references

- **SGHA: Evidence-Grounded Research Problem Discovery with Local Language Models**
  (`2608.17501`, `cs.AI cs.LG`) — corpus-first system: structures a literature corpus
  into an evidence-linked graph, detects unresolved structural patterns, generates
  research-problem candidates from a local LLM. Prior art for `bridge-finder.md` and
  `project-architect.md`'s job, not KB material for any domain. Added 2026-08-27.

## Background references

- **Advanced Linear Algebra with Applications — Part I** (`2608.21234`,
  `math.NA cs.LG cs.NA`) — lecture notes: sparse systems, Krylov methods, spectral
  clustering, preconditioning, multigrid. Covers exactly the toolkit
  `compbio_methods.md` §2 claims ("numerical methods and matrix algorithms where the
  contribution is the method") without itself contributing one — reference material, not
  a research contribution. Useful background for reading papers in that criterion. Added
  2026-08-27.
