# Novelty — anchors

> **STARTER ANCHORS.** These are structurally correct and substantively generic. Replace them with anchors drawn from your own Week 8–9 calibration cases before you trust a score. See `WRITING-ANCHORS.md`.

**Axis question:** has this specific project already been done?

**Not** whether the *connection* is new — the skeptic judged that. A well-known connection can support a project nobody has built.

## Binary (this is what the gate uses)

> Would you reject this proposal on the grounds that it has already been done?

## Scale (advisory — for ranking and drift detection)

```yaml
5: No paper approaches this question from any direction. The closest work is
   in a field that would not recognize the question as theirs.
   Reachable but rare. Expect a few per year.

4: Prior work exists and is citable but does not answer this. Either the same
   method applied to a different question, or the same question approached
   with a method this field has not tried.

3: The question has an accepted answer obtained by another route, and this
   would re-derive it. Can still be worth doing if the new route is cheaper
   or more general — but then THAT is the contribution and the spec must
   say so explicitly. If the spec does not, score 2.

2: Done in another field under different vocabulary. The translation may have
   value; the research does not. Name the field and the paper.

1: A paper exists doing this question, this method, this purpose. Cite it.
```

## Confidence is part of the finding

A search that found nothing is weak evidence, and this is the axis where absence of evidence most readily reads as evidence of absence. `score: 4, confidence: low` is a more useful output than a confident 5 you cannot support. Record how hard you looked.

## Calibration expectations

Most research ideas have been had before, including good ones. A monthly mean above ~3 on this axis almost certainly indicates inflation rather than an unusually inventive month.

## Do not

- Do not re-run the skeptic's searches. They are in `reviews/<id>/skeptic.md`. Search elsewhere.
- Do not credit the bridge's novelty to the project. Separate claims.
- Do not treat "no review article exists" as strong evidence — many worked areas have no survey.
