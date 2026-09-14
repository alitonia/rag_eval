# Venue Rank — RegRAG-VN vs SOICT 2026 — 2026-09-15

| Venue | Tier | Weighted Score | Acceptance Prob. | Pass Verdict | Best-Paper Verdict | Top P0 Actions |
|---|---|---|---|---|---|---|
| SOICT 2026 (Generative AI / AI Applications track) | Regional symposium, Springer CCIS | **7.48 / 10** *(STEP 2 arm)* | **~72%** *(judgment, base-rate adjusted; acceptance rate unpublished)* | **PASS** (bar ~5.5–6.0, judgment) | **Awards not stated on the live CFP — skipped with note** | P0 (user decision): dual-submission fork vs RIVF; P0 (if chosen): CCIS reformat + expansion |

## Manuscript State

- **Commit**: `c3916a1` (= released `v1.0.0`; content identical to the RIVF submission build).
- **Authors**: Nguyen Huy Hoang, Dinh Thi Lan Huong, Nguyen Thang Phuc, Vu Duc Thanh, Nguyen Khac Duy Ngoc (HUST).
- **Current format**: IEEEtran A4, 6 pp — **SOICT requires Springer CCIS, ≤12 pp excluding references** (page limit per the workspace-verified record, `submission_plan/venue_research/venues_verified.md`, live 2026-08-25; the current CFP page does not restate it). Reformat + expansion is required work, not optional.

## Primary Quantitative Result (STEP 0.1)

Identical to the RIVF ranking (`venue_rank_RIVF2026_2026-09-15.md`): evidence-conditioned citation F1 0.005 → 0.32–0.43; 43–49% mis-citation with gold in prompt; pooled clause ≤0.317; article-level recall@3 49.2–52.4% vs 89.1–90.6% document-level. Capability reading fails, measurement reading succeeds; abstract carries both qualifiers.

## STEP 0 — Venue Facts

- **Deadlines (live soict.org, fetched 2026-09-15)**: abstract and full paper both **September 20, 2026** (earlier Sep 9/16 dates shown struck-through — second extension; matches the workspace's 09-11 observation of the same pattern).
- Notification **Oct 12, 2026**; camera-ready **Oct 23**; conference **Dec 4–5, 2026, Ho Chi Minh City**.
- Proceedings: **Springer CCIS**; post-conference **special issue of Multimedia Tools and Applications (Q1)** for extended selected papers — a venue-specific upside RIVF does not offer.
- Tracks (live CFP): AI Foundations and Big Data; **AI Applications**; **Generative AI**; Multimedia Processing; Networking; Applied OR; Cyber Security. A legal-RAG benchmark fits Generative AI / AI Applications directly.
- Review: single-blind; EasyChair (soict2026); SOICT 2025 "received submissions from 32 countries" (acceptance rate **unpublished**).
- Registration economics (workspace-verified): one full registration ($550 by Oct 23) covers up to 2 papers.

## STEP 1 — Fit Check

| Check | Verdict | Evidence |
|---|---|---|
| Scope | **Valid** | Explicit Generative AI + AI Applications tracks; Vietnamese-domain legal NLP is core SOICT territory; HUST-organized symposium. |
| Format | **Invalid as-is** | 6-pp IEEEtran ≠ Springer CCIS ≤12 pp. Reformat (llncs/ccis class — availability on this TeX tree unverified) plus expansion from on-disk deferred material (latency narrative, token-cap analysis, per-model clause table) required. |
| Deadline | **Valid, 5 days** | Sep 20 abstract+paper; feasible if the decision is made immediately. |

## STEP 2 — Acceptance Verdict (senior-PC arm)

Axis scores identical to the RIVF derivation (the manuscript is unchanged; only venue fit moves):

| Criterion | Score | Note |
|---|---|---|
| Novelty / depth / rigor / writing / impact / completeness | 7.0 / 7.0 / 7.5 / 8.0 / 7.0 / 7.5 | unchanged from `venue_rank_RIVF2026_2026-09-15.md` |
| Venue fit | **9.0** | explicit GenAI track; Vietnamese legal NLP is home turf; HUST symposium |

**Weighted: 7.48.** Ceiling rule: not triggered (measurement paper, abstract self-qualifies). **PASS, ~72% (judgment)** — within noise of the RIVF 73%; the instruments do not distinguish the two venues on acceptance odds.

## STEP 2b — Adversarial Rejection Pass

Reuses the 2026-09-15 deepseek hostile lane (different family from the polishing pipeline; charges are venue-agnostic and this commit's content is identical) plus SOICT-specific deltas:

- The lane's fixed charges (conclusion contradiction, metric scope, denominators, κ transparency) are resolved at `c3916a1`; its structural charges (Tier-1 visibility, 88-row scale, single-expert validation) carry over unchanged.
- **SOICT-specific attack 1 — thinness**: a 6-page-dense paper in a 12-page CCIS format reads under-delivered; the absent Tier-2 end-to-end evaluation becomes more visible with room to spare. Mitigation exists on disk (latency, token-caps, per-model tables) but is unbuilt.
- **SOICT-specific attack 2 — single-blind at the authors' home institution**: reviewers plausibly know the group; no anonymity protection, offset by local appreciation of VN-domain legal NLP.

**Reconciliation**: verdict stays PASS; the dominant risk is procedural (below), not scientific.

## STEP 3 — Best-Paper Potential

The live CFP states no awards; no verified award history is on disk (per the verify-before-claiming rule, the earlier "Best Student Paper realistic" note belonged to a different paper's assessment). **Skipped with note.** The MTAP Q1 special-issue path for an extended version is the concrete upside worth recording.

## STEP 4–6 — Weaknesses, Suggestions, Actions

Weaknesses (reviewer voice): (1) same structural set as RIVF (no end-to-end Tier-2 generation; 88-row scale; single-expert validation); (2) reformat risk under deadline; (3) IEEE→Springer citation-style churn.

| P | Action | Impact | Effort | Before Sep 20? |
|---|---|---|---|---|
| **P0** | **Decide the dual-submission fork** (user): RIVF and SOICT cannot both hold this paper — RIVF notification (Oct 15) falls *after* SOICT's deadline, so there is no wait-and-fallback path. If RIVF was filed today, SOICT requires withdrawal; if RIVF was missed, SOICT is the live target. | gates everything | decision | **today** |
| P0 | If SOICT: reformat to CCIS ≤12 pp, expand from on-disk deferred material, EasyChair soict2026 abstract+paper | required | 2–3 days | yes, tightly |
| P2 | Verify llncs/CCIS class availability on this TeX tree before committing to the reformat | de-risks P0 | 15 min | yes |

## Arm Spread / Blind-Rank Cross-Reference

STEP 2: 7.48 PASS. STEP 2b: hostile-lane charges fixed/structural; venue deltas procedural. Blind-rank: the RIVF-corpus re-eval (7/7/7, 83.3–97.9 pct, desk-round upper bound) transfers qualitatively — SOICT's corpus is similarly regional-competitive — but no SOICT-specific pack was scored; treat the percentile as indicative only.

## Human-Review Delta

None on disk for this paper; no advisor verdict recorded. All numbers instrument-only, labeled judgment.

## Calibration Record

| Date | Venue | Commit | Score | Prob. | Human verdict | Outcome |
|---|---|---|---|---|---|---|
| 2026-09-15 | SOICT 2026 | c3916a1 | 7.48 | ~72% (judgment) | none | Open — decision pending |
| 2026-09-15 | RIVF 2026 | c3916a1 | 7.48 | ~73% (judgment) | none | Filed/pending (EDAS user-side) |
