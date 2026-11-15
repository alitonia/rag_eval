# Venue Rank — RegRAG-VN vs IEEE RIVF 2026 — camera-ready re-scoring (2026-11-16)

| Venue | Tier | Weighted Score | Acceptance Prob. | Pass Verdict | Best-Paper Verdict | Outcome |
|---|---|---|---|---|---|---|
| IEEE RIVF 2026 (AI & Data Science track) | Regional IEEE | **7.5 / 10** | **accepted** (outcome) | **PASS — outcome confirmed** | LONG SHOT (unchanged) | **ACCEPTED** (notification Oct 2026; camera-ready due 2026-11-25) |

## Manuscript State

- **Commit**: `378ea03` (camera-ready state: gold-citation fix + re-scored tables + release-prep cleanups on top of the submitted build).
- **Authors**: Dinh Thi Lan Huong (first), Nguyen Huy Hoang, Nguyen Thang Phuc, Vu Duc Thanh, Nguyen Khac Duy Ngoc (HUST), Thanh Phuong Nguyen (U. L'Aquila).
- **Format**: IEEEtran conference A4, 6 pages, 0 overfull, 0 undefined.

## Primary Quantitative Result (post-fix)

> With gold evidence in context, article-level citation F1 rises from 0.005 (closed-book) to 0.33–0.43 across 792 single-GPU runs on ≤7B models; 43–48% of RAG answers still fail citation-level checking, roughly 34% even with the governing provision in the prompt intact; pooled clause accuracy ≤0.317; on the full 3,703-chunk corpus, article-level recall@3 is 49.2–52.4% against 89.1–90.6% document-level.

Capability reading fails; measurement reading succeeds (unchanged). The abstract carries both qualifiers.

## Delta vs the 2026-09-15 ranking (`df91770`) — prior ranking NOT void

No restructuring, no authorship change. Five printed numbers moved one step from the Q059–Q061 gold correction (F1 BM25 0.321→0.326; unfaithful 49→48%; cite-only 41→40%; clipped range 33–44→33–41%; khoản BM25 0.300→0.308). Two dense rows that cited the umbrella law's unrelated article are now correctly flagged wrong-instrument. Direction: slightly less damning on BM25, slightly more honest on dense. Axis scores below move by less than the noise floor (±0.1); the weighted total moves 7.48 → 7.5 only via rounding. Additionally, the deposit now carries a replay gate (shipped scorer re-derives the printed tables from the shipped log), which strengthens the reproducibility story without touching any axis score.

## Scores (STEP 2 arm, camera-ready state)

| Criterion | Score | Justification |
|---|---|---|
| Novelty | 7.0 | Unchanged: first VN banking-regulation benchmark with Điều/Khoản citation scoring + abstention probes + coverage-verified corpus; citation-level scoring appeared in 0/48 accepted RIVF-2025 abstracts (blind-corpus check, 2026-09-15). |
| Technical depth | 7.0 | Unchanged: two-tier corpus, coverage invariant, provenance-guarded aggregation, error taxonomy. |
| Experimental rigor | 7.5 | Adversarial repricing stands. The gold fix removes one mis-scored failure class and the replay gate makes the tables mechanically reproducible from the deposit; single-expert validation (κ 0.20/0.39/0.62), no significance tests, and 88-question scale remain the honest ceiling. |
| Writing | 8.0 | Unchanged; disclosure-forward abstract is what the hostile blind arm rewarded (+2 at desk round). |
| Impact | 7.0 | Unchanged: regional deployment relevance (SBV domain, ≤7B local serving). |
| Completeness | 7.5 | Scorer validation in-text; κ honestly reported as not measured; audited, hash-sealed deposit. |
| Venue fit | 9.0 | Vietnamese statutory corpus, Hanoi venue, in-person presentation confirmed. |

**Weighted: 7.5.** Ceiling rule: not triggered (measurement paper). Framing bifurcation unchanged: ~30% residual risk of a capability reading, held down by the abstract qualifiers.

## Outcome Calibration (the headline of this report)

| Date | Venue | Commit | Score | Prob. | Human verdict | Outcome |
|---|---|---|---|---|---|---|
| 2026-09-13 | RIVF 2026 | dc90047 | 7.45 printed / 7.70 arithmetic | 78% | none | superseded |
| 2026-09-15 | RIVF 2026 | df91770 | 7.48 | ~73% (judgment) | none | **ACCEPTED** (Oct 2026) |
| 2026-09-15 | SOICT 2026 | c3916a1 | 7.48 | ~72% (judgment) | not submitted (fork rejected; deadline passed) | n/a |
| 2026-11-16 | RIVF 2026 | 378ea03 | 7.5 | accepted | **accepted** | camera-ready |

First outcome-calibrated point for this instrument: judgment ~73% → accept. The blind-rank desk percentile (83.3–97.9 strict, tier-1, upper bound per the disclosure-inversion calibration) is consistent with the outcome but stays labeled an upper bound.

## Best-Paper Potential

**LONG SHOT** (unchanged). RIVF winners profile as applied/deployment breakthroughs; this is a benchmark/measurement paper with off-the-shelf models. The with-evidence mis-citation finding and the provenance discipline are its distinctive material, not award material at this venue.

## Above-RIVF ladder (grounded in the sibling reports)

| Rung | Venue | Instrument evidence | Reachable? |
|---|---|---|---|
| Same tier | SOICT 2026 (Springer CCIS) | 7.48 / ~72%, statistically tied with RIVF; deadline passed 2026-09-20; MTAP Q1 special issue exists for extended versions | tied, not above |
| +1 band | **EASE 2027 (CORE A, ACM, Hanoi; abstract 2027-01-15, full 2027-01-22; RENE ~Mar)** | `venue_rank_EASE2027_2026-09-13.md`: 7.85/68% PASS, bar 6.5–7.0; its rigor 8.5 assumed validations filled — adversarially repriced state is 7.5–7.85. RENE track (reproducibility & negative results) is tailor-made and the best-paper verdict there was **REALISTIC** | **yes with work**: ACM sigconf 10+2 pp, double-anonymous, Empirical Standards checklist, expansion (latency narrative, token-caps, per-model clause tables on disk) |
| +1 band | LREC-class resource/evaluation venues | not instrument-scored; judgment: benchmark/resource papers are home ground, modest expansion suffices | plausible, unverified |
| +2 bands | Mid-tier journals: Artificial Intelligence and Law (Springer), Natural Language Engineering, Computer Law & Security Review | judgment only; needs the sequel expansion (Tier-2 end-to-end campaign, larger gold, second annotator) to reach journal length and depth | with sequel expansion |
| Not at current scale | NeurIPS/ICML/ACL/EMNLP main, Q1 ML journals | bar 7.5–8+; the 88-question scale, no frontier baseline, and single-expert validation are the known rejection reasons | no, at any current state |

## Remaining Actions

| P | Action | Owner |
|---|---|---|
| P0 | EDAS metadata check + acceptance-email mechanics (eCF, PDF validation, author registration) | user |
| P0 | Release-asset refresh of `regrag-vn` v1.0.0 with the corrected PDF (on approval; public push) | assistant, on approval |
| P1 | EASE 2027 RENE decision for the expanded version (deadline 2027-01-22) | user decision |
| P2 | Latency/token-cap narrative in camera-ready (only if page budget allows; not needed) | — |
