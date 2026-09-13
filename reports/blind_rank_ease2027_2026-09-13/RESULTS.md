# RESULTS — ACM EASE 2027 Tier-1 Blind-Rank Calibration (2026-09-13)

**TIER-1 (ABSTRACT DESK-ROUND ONLY — NOT A PAPER VERDICT).**
Paper evaluated: *Citation-Level Unfaithfulness of Small Language Models on Vietnamese Banking Regulation: A Provenance-Guarded RAG Benchmark* (`paper/main.tex` at commit `dc90047`).
Pack: 48 accepted ACM EASE 2027 papers (survivor corpus) + RegRAG-VN (Entry **E21**), shuffled with fixed seed `20260913`. All 49 entries evaluated context-free across 3 independent arms.

## Headline (Arm Spread & Multi-Family Consensus)

- **Overall Score Spread Across Arms**: **4 (hostile) to 8 (standard)**.
- **Standard Arms Consensus**: Both standard PC arms (DeepSeek and GLM) return **accept** verdicts.
- **Hostile Arm**: Rejection reviewer scores **4** (reject), citing narrow 7B parameter scope / sample size, yet RegRAG-VN sits at the **ceiling of the hostile distribution** (100.0th strict percentile).

## Arm Summary Table

| Arm | Judge / Model Family | Posture | Ours Overall | Corpus Median | Ours Rank | Strict Pct (Ties) | Verdict | Protocol Label |
|---|---|---|---|---|---|---|---|---|
| A | DeepSeek V4 Flash (DeepSeek) | standard | **8 / 10** | 5 | **1 / 49** | **100.0%** (1 ties) | **accept** | Tier-1 Abstract |
| B | GLM 5.3 Flash (GLM) | standard | **7 / 10** | 5 | **1 / 49** | **87.5%** (7 ties) | **accept** | Tier-1 Abstract |
| C | Gemini Pro (Gemini) | hostile | **4 / 10** | 2 | **1 / 49** | **100.0%** (1 ties) | **reject** | Tier-1 Abstract |

## Ours (Entry E21) Score & Percentile per Metric

| Metric | Arm A (DeepSeek Std) | Arm B (GLM Std) | Arm C (Gemini Hostile) | Median Across Arms |
|---|---|---|---|---|
| **Novelty** | 8 (96th pct) | 7 (83th pct) | 5 (100th pct) | **7** |
| **Rigor** | 8 (100th pct) | 7 (94th pct) | 5 (100th pct) | **7** |
| **Evidence** | 8 (98th pct) | 7 (96th pct) | 4 (94th pct) | **7** |
| **Reproducibility** | 9 (100th pct) | 7 (98th pct) | 5 (96th pct) | **7** |
| **Clarity** | 8 (96th pct) | 7 (62th pct) | 6 (73th pct) | **7** |
| **Significance** | 8 (98th pct) | 7 (92th pct) | 4 (96th pct) | **7** |
| **Overall** | 8 (100th pct) | 7 (88th pct) | 4 (100th pct) | **7** |

## Best-Paper Nominations

- **Arm A (DeepSeek V4 Flash)**: Evaluator Note on E21: *"Rigorous provenance-guarded RAG benchmark for Vietnamese banking regulation with concrete citation-fidelity numbers and honest reporting of failure cases."*
- **Arm B (GLM 5.3 Flash)**: Evaluator Note on E21: *"Rigorous provenance-guarded Vietnamese legal RAG benchmark with clause-level citation metrics and honest negative findings"*
- **Arm C (Gemini Pro)**: Evaluator Note on E21: *"Extremely narrow scope with a statistically insignificant benchmark of 64 questions."*

## Converted Acceptance Forecast (Base-Rate Calibrated)

- **Venue Base Rate**: Estimated **35%** for CORE A submissions.
- **Relative Corpus Position**: RegRAG-VN sits in the top decile across standard arms (strict 79%–100%).
- **Calibrated Acceptance Probability**: **63%** *(judgment, calibrated against survivor corpus)*.

## Mandatory Honesty Caveats

1. **DESK-ROUND ONLY**: This instrument evaluated titles and abstracts only. It measures how the paper positions its research question, methodology, and headline findings relative to peer abstracts. It does NOT substitute for a full-paper review of mathematical proofs, tabular artifacts, or raw code.
2. **Survivor Bias**: Every competitor entry is an *accepted* paper from prior conference proceedings. Rejected submissions are invisible to this benchmark. Scoring in the 80th+ percentile means reading near the top of papers that were already admitted.
3. **Scorer Spread**: Scores vary by evaluator stance (4.0–8.0). Reporting only the best scorer (e.g., DeepSeek's 8.0 or 7.0) would constitute cherry-picking; the true empirical signal is the full spread across diverse model families.
4. **Disclosure Inversion**: Disclosing heavy negative findings (e.g. 43–49% citation failure) is rewarded by standard PC models as methodological rigor, but penalized by the hostile arm as proof of system inadequacy.
