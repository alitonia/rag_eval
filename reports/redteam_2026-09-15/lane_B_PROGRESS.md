# Red-team B — progress trace (hostile Review #2 pass on paper/main.tex)

## Scope / state
- Read `/mnt/data/seminar_2/paper/main.tex` in full (278 lines, the version it stabilized at
  after mid-session edits — wording on lines 127/147/259 changed between my first read and live
  greps; all quotes below were re-verified against the live file on 2026-09-15).
- Read `paper/refs.bib` (228 lines) — citation-integrity comments present; no rendered-field issues.
- Read `data/eval/scorer_validation_2026-09-15.json` (68 lines).

## Cross-checks that PASSED (no finding)
- 3x3x88 = 792 answers; 709+83 = 792; 64+24 = 88 rows. ✓
- Abstract F1 range 0.32–0.43 matches Table II (0.321 / 0.434); 43–49% matches RQ2 prose. ✓
- κ=0.39 (paper) vs 0.3863 (JSON hallucinated) ✓; "3/3 and 10/10" (precision 1.0 correct/abstained) ✓;
  "net undercount of five" = fn 10 − fp 5 ✓; 50 rows, 41/9 splits ✓.
- Table I numbers reproducible from the table itself; closed-book abstention 0.042×24 = 1 row,
  consistent with "71 of 72 probe rows" answered. ✓
- Doc-vs-article gap math consistent with the table.
- Disclosure of Tier-1 conditioning IS present (Sec V-A) — but see Finding 2 re abstract.
- Binomial-noise disclosure present at line 138 — but see Findings 10/3 for self-application.

## Key contradiction discovered (F1)
Conclusion (line 267) claims legal RAG is "constrained by statutory granularity before generation
begins" — yet RQ2 (line 254) shows 43–49% mis-citation with the governing provision guaranteed in
the prompt, and Sec V-A (line 142) states such citations "reflect model generation failures rather
than retrieval omissions". The body's mechanism contradicts the conclusion's attribution.

## Scorer validation findings (F4)
JSON kappas: correct=0.2038 (auto recall 0.167), hallucinated=0.3863 (fp=5), abstained=0.6154.
Paper reports only the 0.39 one and telescopes fp=5 into "net undercount of five".

## Files written
- /tmp/redteam_B/PROGRESS.md (this file)
- /tmp/redteam_B/FINDINGS.md (final findings)