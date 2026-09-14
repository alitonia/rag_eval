# Venue Rank — RegRAG-VN vs IEEE RIVF 2026 — 2026-09-15 (submission-day re-derivation)

| Venue | Tier | Weighted Score | Acceptance Prob. | Pass Verdict | Best-Paper Verdict | Top P0/P1 Actions |
|---|---|---|---|---|---|---|
| IEEE RIVF 2026 (AI & Data Science track) | Regional IEEE | **7.48 / 10** *(STEP 2 arm)* | **~73%** *(judgment, base-rate adjusted; RIVF acceptance rate unpublished)* | **PASS** (bar ~5.5–6.0, judgment) | **LONG SHOT** | P0: Zenodo DOI + EDAS N35414 upload (user); no remaining paper-side P0 |

**Supersedes** `venue_rank_RIVF2026_2026-09-13.md`, which is void per the staleness rule (manuscript materially changed since `dc90047`: related-work merge, scorer validation landed, κ promise removed, honesty patches, red-team fix cycle). **Arithmetic correction to the prior report:** its own axis scores (7.0/7.0/8.5/8.0/7.5/7.0/9.0 under weights 20/20/20/15/10/5/10) compute to **7.70**, not the 7.45 it printed.

---

## Manuscript State

- **Commit**: `df91770` (this ranking describes exactly this state; includes the 2026-09-15 hostile-lane fix cycle).
- **Authors**: Nguyen Huy Hoang, Dinh Thi Lan Huong, Nguyen Thang Phuc, Vu Duc Thanh, Nguyen Khac Duy Ngoc (HUST).
- **Format**: IEEEtran conference A4, exactly 6 pages, 0 undefined citations/references.

## Primary Quantitative Result (STEP 0.1)

> With gold evidence in context, article-level citation F1 rises from 0.005 (closed-book) to 0.32–0.43 across 792 single-GPU runs on ≤7B models; 43–49% of RAG answers still cite a wrong or non-governing provision **even with the governing provision in the prompt**; clause accuracy ≤0.317; on the full 3,703-chunk corpus, article-level recall@3 is 49.2–52.4% against 89.1–90.6% document-level.

**Capability-reading test**: as a deployed system, fails (models unfit for unassisted compliance use — the paper says so); as a benchmark/measurement, succeeds (isolates generation-side citation failure from retrieval, bounds the end-to-end ceiling, validated scorer with disclosed conservative-exact profile). The abstract now carries both qualifiers ("with gold evidence in context", "even with the governing provision in the prompt"), which moved the paper toward the measurement reading at the one place reviewers actually look.

## STEP 0 — Venue Facts (re-verified live 2026-09-15)

- Deadline: **September 15, 2026, hard** — rivf2026.org: "The paper submission deadline is extended to September 15, 2026. This is a hard deadline".
- Notification **Oct 15, 2026**; camera-ready **Nov 11, 2026**; conference **Dec 18–20, 2026, VinUniversity, Hanoi**.
- Portal: EDAS. Format ≤6 pp IEEE. Acceptance rate: **unpublished** (bar below is judgment).
- Award profile (from the 09-13 report's verified record): RIVF best papers favor applied/deployment work (2024: applied IoT botnet detection, DOI 10.1109/RIVF64335.2024.11009118).

## STEP 1 — Fit Check

| Check | Verdict | Evidence |
|---|---|---|
| Scope | **Valid** | AI & Data Science track covers NLP/IR/applied ML; Vietnamese legal RAG benchmark is on-theme for a Hanoi-hosted regional venue. |
| Format | **Valid** | 6 pp exactly, IEEEtran, complete author block (single-blind). |
| Deadline | **Valid but today** | Manuscript complete; only DOI insertion + EDAS upload remain (user actions). |

## STEP 2 — Acceptance Verdict (senior-PC arm, this assistant)

| Criterion | Score | Justification |
|---|---|---|
| Novelty | 7.0 | First VN banking-regulation benchmark with Điều/Khoản citation scoring + abstention probes + coverage-verified corpus; the related-work gap statement is now grounded in four verified VN-legal NLP citations. |
| Technical depth | 7.0 | Two-tier corpus + coverage invariant + provenance-guarded aggregation; error taxonomy (retrieval/generation/citation) now named and implemented. |
| Experimental rigor | **7.5** | Repriced down from the prior 8.5: the landed validation shows κ=0.20 correctness / 0.39 hallucination agreement against one expert, no significance tests (now disclosed), 83/792 truncated answers scored as-is. Complete 792-row campaign, deterministic scoring, honest disclosures keep it well above the venue norm. |
| Writing | 8.0 | Post-humanization prose survived two adversarial passes with only mechanical fixes; abstract now self-qualifies. |
| Impact | 7.0 | Regional deployment relevance (SBV-domain, ≤7B local serving). |
| Completeness | 7.5 | 50-response validation landed in-text; gold-row κ honestly reported as not measured. |
| Venue fit | 9.0 | Vietnamese statutory corpus, HUST team, Hanoi venue. |

**Weighted**: 7.48. **Ceiling rule**: not triggered — the headline number *is* the measurement (negative-capability finding), and the abstract now frames it as such.
**Framing bifurcation**: ~30% of reviewers may still read it as a capability paper ("small models fail") — the residual risk. The abstract qualifiers are what move that number down.
**Verdict: PASS. Probability ~73%** *(judgment; base rate for a well-executed empirical regional-IEEE submission with unpublished acceptance rate)*.

## STEP 2b — Adversarial Rejection Pass (deepseek-flash hostile lane, different family from the polishing pipeline)

The hostile lane returned 15 findings: 1 BLOCKER, 11 WARN, 3 NOTE. **Reconciliation with STEP 2:**

- The BLOCKER (conclusion claiming retrieval-granularity constraint "before generation begins" contradicted RQ2's with-evidence mis-citation) and five WARNs were **real defects, now fixed at `df91770`** (metric scope, 63+1+1 arithmetic, denominator ambiguity, refusal entanglement, selective κ reporting).
- The surviving adversarial charges are the structural ones the disclosures address rather than eliminate: Tier-1 visibility beyond the abstract (disclosed §V-A), 88-row scale, single-expert validation, truncation handling, no frontier baseline.
- **Agreement**: both arms put the paper above the RIVF bar; the adversarial arm's strongest specific charges were fixable presentation/consistency bugs, not missing experiments. Where they disagreed (rigor axis: 8.5 vs "self-graded toy fixture"), the fix cycle + validation numbers support the repriced 7.5 rather than either extreme.
- Final verdict **moves toward the adversarial pass only on rigor** (7.5, not 8.5); overall **PASS** stands.

## STEP 3 — Best-Paper Potential

**LONG shot.** RIVF winners profile as applied breakthroughs with deployment evidence; this is a benchmark/measurement paper using off-the-shelf models. The provenance discipline and the with-evidence mis-citation finding are its distinctive material.

## STEP 4 — Remaining Weaknesses (reviewer voice)

1. **MAJOR**: no end-to-end generation on Tier-2; retrieval and generation evaluated as disconnected halves (bounded, not measured, end-to-end). 2. **MAJOR**: 88-row benchmark scale; statistical power limited (now disclosed). 3. **MAJOR**: single-expert scorer validation, κ=0.39 hallucination agreement (now fully reported). 4. **MINOR**: 83 truncated answers scored as-is. 5. **MINOR**: no >7B or frontier-API arm.

## STEP 5 — Suggestions (1:1 with weaknesses)

1. Tier-2 end-to-end generation campaign (experiment; next version). 2. Grow benchmark + dual-grade gold rows (content; camera-ready or journal extension). 3. Second validation annotator (procedural; post-deadline). 4. Truncation-aware scoring or per-cell truncation table (presentation; camera-ready). 5. Frontier baseline (experiment; extension).

## STEP 6 — Priority Actions

| P | Action | Impact | Effort | Before deadline? |
|---|---|---|---|---|
| P0 | Publish Zenodo record, insert DOI (user) | blocks availability claim | 15 min | **today** |
| P0 | Upload PDF to EDAS N35414 ≥6h early (user) | blocks submission | 30 min | **today** |
| P2 | Latency/token-cap narrative | polish | — | camera-ready |
| P3 | Tier-2 end-to-end + frontier arm | extension | — | next version |

## Arm Spread / Blind-Rank Cross-Reference

- STEP 2 (this report): 7.48, PASS. STEP 2b (deepseek hostile): strongest charge fixed; residual = structural disclosures.
- **Blind-rank re-eval (2026-09-15, paired pack, same 49 positions as the 09-13 run, ours = R33, abstract at `df91770`): overall 7–7 across all three arms (deepseek std, glm std, gemini hostile), strict percentile spread 83.3–97.9, all arms *accept*; hostile arm +2 vs the 09-13 run (5/major-revision → 7/accept). TIER-1 DESK-ROUND ONLY — upper bound per the ACSF disclosure-inversion calibration.** Full numbers: `blind_rank_rivf2026_2026-09-15/RESULTS_reeval.md`. The blind-rank arm independently supports the ~73% judgment above.

## Human-Review Delta

No advisor/co-author verdict exists on disk for this paper (the 2026-09-13 report's "pending co-author check" never materialized). No averaging was possible; all scores above are instrument-only and labeled judgment.

## Calibration Record

| Date | Venue | Commit | Score | Prob. | Human verdict | Outcome |
|---|---|---|---|---|---|---|
| 2026-09-13 | RIVF 2026 | dc90047 | 7.45 printed / 7.70 correct arithmetic | 78% | none | superseded |
| 2026-09-15 | RIVF 2026 | df91770 | 7.48 | ~73% | none | Open (notif. Oct 15) |
