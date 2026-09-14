# RESULTS — IEEE RIVF Blind-Rank Paired Re-Eval (2026-09-15)

**TIER-1 (ABSTRACT DESK-ROUND ONLY — NOT A PAPER VERDICT).**
Paper: *Citation-Level Unfaithfulness of Small Language Models on Vietnamese Banking Regulation: A Provenance-Guarded RAG Benchmark* — `paper/main.tex` at commit `df91770`.

**Why a re-run:** the 2026-09-13 calibration (commit `dc90047`, `RESULTS.md` in this directory's parent) is void after the manuscript changed (validation landed, honesty patches, red-team fixes). Per the paired-re-eval protocol, the pack was rebuilt with the **mapping held fixed** (same 49 positions, ours still **R33**) and the identical RIVF-2025 corpus; the only ours-side change is the abstract text (two qualifiers added: "with gold evidence in context", "even with the governing provision in the prompt"). Corpus abstracts re-fetched from OpenAlex 2026-09-15, 48/48 resolved, archived at `../blind_rank_rivf2026/corpus_rivf2025_2026-09-15.json`.

## Headline

| Arm | Family / posture | Ours overall | Corpus median | Strict pct | Verdict | Δ vs 09-13 |
|---|---|---|---|---|---|---|
| A | DeepSeek std | **7** | 6.0 | **83.3%** | accept | 0 |
| B | GLM std | **7** | 5.0 | **95.8%** | accept | **+1** (6→7) |
| C | Gemini hostile | **7** | 4.5 | **97.9%** | accept | **+2** (5→7, major-revision→accept) |

**Spread (the result, never the best arm): overall 7–7 across arms; strict percentile 83.3–97.9.** All three arms return *accept*. The hostile arm — which scored ours 5/major-revision on the pre-fix abstract — now returns 7/accept with the note "Excellent rigorous benchmark exposing specific citation-level failures in LLMs." Since corpus, positions, and scoring protocol are otherwise identical, the delta isolates the abstract's honesty qualifiers: the disclosure-forward abstract reads stronger to a hostile judge at desk round.

## Per-metric (ours = R33)

| Metric | A (std) | B (std) | C (hostile) |
|---|---|---|---|
| novelty | 7 (87.5%) | 6 (77.1%) | 7 (97.9%) |
| rigor | 8 (100%) | 7 (100%) | 8 (100%) |
| evidence | 7 (89.6%) | 7 (100%) | 7 (95.8%) |
| reproducibility | 7 (91.7%) | 6 (83.3%) | 6 (91.7%) |
| clarity | 7 (95.8%) | 6 (47.9%) | 8 (100%) |
| significance | 7 (83.3%) | 6 (68.8%) | 7 (100%) |
| **overall** | **7 (83.3%)** | **7 (95.8%)** | **7 (97.9%)** |

## Acceptance conversion

Venue acceptance rate **unpublished**; base rate for a regional IEEE full-paper track estimated ~40%. Ours sits above the corpus median under every arm. Converted forecast: **~73% (judgment)** — consistent with the independent venue-rank arm (7.48, ~73%, `../../venue_rank_RIVF2026_2026-09-15.md`). A percentile is not an acceptance forecast: the reject pool is invisible to this instrument.

## Mandatory caveats

1. **DESK-ROUND ONLY — NOT A PAPER VERDICT.** Titles + abstracts only. Tier 2 did not run: OpenAlex OA survey records **1/48** competitor full texts as openly accessible (IEEE Xplore walls the rest; Wayback/manual-download not exercised on deadline day). No user-assisted download was requested.
2. **Survivor bias:** every corpus entry was accepted; a high percentile bounds ours against the venue's floor, not its submission pool.
3. **Disclosure inversion (calibrated, ACSF 2026-09-11):** LLM judges reward dense limitation disclosure; a human reviewer can read the same disclosure as failure evidence. The +2 hostile-arm gain on a *more* disclosed abstract is exactly the direction that instrument bias predicts — treat this tier-1 percentile as an **upper bound** and weight the full-text adversarial red-team (`/tmp/redteam_B`, fixes at `df91770`) above it.
4. **Topic presence:** corpus is not topic-absent (9/48 LLM papers, 7/48 Vietnamese-NLP, 3/48 RAG, 2/48 legal-domain) — ours scored against near-neighbors, not a void. Citation-level scoring appears in 0/48 entries, so that axis measures a real niche gap.
5. **Scorer variance:** ±1 is noise; arm C's corpus median (4.5) shows the hostile judge also graded the whole corpus harder, inflating percentile-relative-to-median reads.
6. **Staleness:** these numbers describe `df91770` exactly; any later manuscript change voids them.
7. No human-review calibration point exists for this paper yet; the first advisor/co-author verdict should be recorded beside these scores.

## Artifacts

- Pack + stats: `/tmp/rivf_reeval_2026-09-15/` (ephemeral) — per-entry files, `pack_stats.json` (ours 1550 chars, corpus 729–2105, median 1299; length symmetry verified, no truncation).
- Scores: `../blind_rank_rivf2026/scores_reeval_arm{A_deepseek,B_glm,C_gemini}_2026-09-15.csv` (repo-side copies).
- Builders: `scripts/build_rivf_blind_reeval.py`, `scripts/unblind_rivf_reeval.py`.
- Blinding audit: per-pattern grep — "RegRAG" only in R33 (its own system name, symmetric with competitors' self-naming); no author/repo/URL markers unique to ours.
