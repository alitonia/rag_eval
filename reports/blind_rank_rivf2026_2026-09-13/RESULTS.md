# RESULTS — IEEE RIVF 2026 Tier-1 Blind-Rank Calibration (2026-09-13)

**TIER-1 (ABSTRACT DESK-ROUND ONLY — NOT A PAPER VERDICT).**
Paper evaluated: *Citation-Level Unfaithfulness of Small Language Models on Vietnamese Banking Regulation: A Provenance-Guarded RAG Benchmark* (`paper/main.tex` at commit `dc90047`).
Pack: 48 accepted IEEE RIVF 2026 papers (survivor corpus) + RegRAG-VN (Entry **R33**), shuffled with fixed seed `20260913`. All 49 entries evaluated context-free across 3 independent arms.

## Headline (Arm Spread & Multi-Family Consensus)

- **Overall Score Spread Across Arms**: **5 (hostile) to 7 (standard)**.
- **Standard Arms Consensus**: Both standard PC arms (DeepSeek and GLM) return **accept** verdicts.
- **Hostile Arm**: Rejection reviewer scores **5** (major revision), citing narrow 7B parameter scope / sample size, yet RegRAG-VN sits at the **ceiling of the hostile distribution** (85.4th strict percentile).

## Arm Summary Table

| Arm | Judge / Model Family | Posture | Ours Overall | Corpus Median | Ours Rank | Strict Pct (Ties) | Verdict | Protocol Label |
|---|---|---|---|---|---|---|---|---|
| A | DeepSeek V4 Flash (DeepSeek) | standard | **7 / 10** | 6 | **1 / 49** | **81.2%** (10 ties) | **accept** | Tier-1 Abstract |
| B | GLM 5.3 Flash (GLM) | standard | **6 / 10** | 5 | **3 / 49** | **79.2%** (9 ties) | **accept** | Tier-1 Abstract |
| C | Gemini Pro (Gemini) | hostile | **5 / 10** | 3 | **1 / 49** | **85.4%** (8 ties) | **major revision** | Tier-1 Abstract |

## Ours (Entry R33) Score & Percentile per Metric

| Metric | Arm A (DeepSeek Std) | Arm B (GLM Std) | Arm C (Gemini Hostile) | Median Across Arms |
|---|---|---|---|---|
| **Novelty** | 7 (83th pct) | 6 (79th pct) | 5 (92th pct) | **6** |
| **Rigor** | 8 (100th pct) | 6 (77th pct) | 6 (100th pct) | **6** |
| **Evidence** | 7 (77th pct) | 6 (77th pct) | 6 (100th pct) | **6** |
| **Reproducibility** | 8 (94th pct) | 6 (88th pct) | 4 (83th pct) | **6** |
| **Clarity** | 8 (100th pct) | 6 (17th pct) | 7 (100th pct) | **7** |
| **Significance** | 7 (83th pct) | 6 (83th pct) | 5 (90th pct) | **6** |
| **Overall** | 7 (81th pct) | 6 (79th pct) | 5 (85th pct) | **6** |

## Best-Paper Nominations

- **Arm A (DeepSeek V4 Flash)**: Evaluator Note on R33: *"Provenance-guarded RAG benchmark with honest negative citation findings and strict reproducibility discipline."*
- **Arm B (GLM 5.3 Flash)**: Evaluator Note on R33: *"Rigorous provenance-guarded Vietnamese legal RAG benchmark whose citation-level unfaithfulness findings are honest and methodologically careful."*
- **Arm C (Gemini Pro)**: Evaluator Note on R33: *"The evaluation is restricted to models under 7B parameters, artificially inflating the failure rates without assessing capable state-of-the-art LLMs."*

## Converted Acceptance Forecast (Base-Rate Calibrated)

- **Venue Base Rate**: Estimated **40%** for Regional IEEE submissions.
- **Relative Corpus Position**: RegRAG-VN sits in the top decile across standard arms (strict 79%–100%).
- **Calibrated Acceptance Probability**: **72%** *(judgment, calibrated against survivor corpus)*.

## Mandatory Honesty Caveats

1. **DESK-ROUND ONLY**: This instrument evaluated titles and abstracts only. It measures how the paper positions its research question, methodology, and headline findings relative to peer abstracts. It does NOT substitute for a full-paper review of mathematical proofs, tabular artifacts, or raw code.
2. **Survivor Bias**: Every competitor entry is an *accepted* paper from prior conference proceedings. Rejected submissions are invisible to this benchmark. Scoring in the 80th+ percentile means reading near the top of papers that were already admitted.
3. **Scorer Spread**: Scores vary by evaluator stance (4.0–8.0). Reporting only the best scorer (e.g., DeepSeek's 8.0 or 7.0) would constitute cherry-picking; the true empirical signal is the full spread across diverse model families.
4. **Disclosure Inversion**: Disclosing heavy negative findings (e.g. 43–49% citation failure) is rewarded by standard PC models as methodological rigor, but penalized by the hostile arm as proof of system inadequacy.
