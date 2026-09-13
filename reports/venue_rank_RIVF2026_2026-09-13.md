# Venue Rank — RegRAG-VN vs IEEE RIVF 2026 (Track 1) — 2026-09-13

| Venue | Tier | Weighted Score | Acceptance Prob. | Pass Verdict | Best-Paper Verdict | Top P0/P1 Actions |
|---|---|---|---|---|---|---|
| IEEE RIVF 2026 (Track 1: AI & Data Science) | Regional IEEE | **7.45 / 10** | **78%** *(judgment, base-rate adjusted)* | **PASS** (bar ~5.5–6.0) | **LONG SHOT** (upper 15%) | P0: Grade human label sets (30-row $\kappa$ + 50-row validation); P0: Reserve Zenodo DOI; P0: Submit EDAS N35414 $\ge$6h early |

---

## Manuscript State & Primary Result

- **Manuscript**: `paper/main.tex` at commit `dc90047` (`style: comprehensive academic voice humanization`).
- **Author List**: Nguyen Huy Hoang¹ (First Author), Dinh Thi Lan Huong², Nguyen Thang Phuc³, Vu Duc Thanh⁴, Nguyen Khac Duy Ngoc⁵ (Hanoi University of Science and Technology, Hanoi, Vietnam).
- **Format**: IEEE conference format (`IEEEtran.cls`), A4, strictly 6 pages, 0 errors, 0 warnings.
- **Primary Quantitative Result**:
  > Retrieval augmentation raises article-level citation F1 from 0.005 (closed-book) to 0.321 (BM25) and 0.434 (dense) across 792 single-GPU runs on $\le$7B models; however, 43--49% of RAG-generated answers still cite non-governing or incorrect provisions with gold evidence in prompt, clause accuracy remains $\le 0.317$, and on the full 3,703-chunk legal corpus, article-level retrieval drops to 49.2--52.4% despite 89.1--90.6% document-level recall.
- **Capability-Reading Test (Step 0.1)**:
  - *As a deployed system*: Fails completely. Small open-weight models served on commodity GPUs cannot autonomously act as reliable regulatory compliance officers (43–49% citation error rate, brittle abstention, 23–25% false refusal).
  - *As a benchmark & empirical measurement*: Succeeds strongly. The paper does not claim small models solve regulatory compliance; it exposes *why* aggregate accuracy metrics conceal citation-level failure, isolates the statutory hierarchy retrieval bottleneck (1.7–1.8$\times$ document-to-article drop), and establishes an immutable provenance architecture.

---

## STEP 0 — Venue Resolution & Facts

- **Edition**: 20th IEEE International Conference on Research, Innovation and Vision for the Future (RIVF 2026).
- **Host**: VinUniversity, Hanoi, Vietnam (Dec 18–20, 2026).
- **CFP & Submission**: `https://rivf2026.org` (verified); EDAS portal `https://edas.info/N35414`.
- **Deadline**: September 15, 2026 (hard, 2 days remaining). Notification: October 15, 2026. Camera-ready: November 11, 2026.
- **Scope & Tracks**:
  - Track 1: "Artificial Intelligence, Data Science and Machine Learning" — covers NLP, information retrieval, deep learning, knowledge graphs, and applied ML. Exact match for legal RAG evaluation.
  - Track 4: "Cyber-Security, Cryptography, Blockchain" — covers security/privacy in AI/data systems (secondary match).
- **Format**: Up to 6 pages IEEE A4; single-blind (author block present).
- **Acceptance Rate**: Unpublished historically (estimated ~35–45% for full papers at regional IEEE conferences; pass bar ~5.5–6.0).
- **Award Profile**: Applied, empirical, domain-grounded works addressing Vietnamese or regional systems (e.g., 2024 Best Paper: applied IoT botnet detection, DOI 10.1109/RIVF64335.2024.11009118).

---

## STEP 1 — Fit Check

| Check | Verdict | Evidence |
|---|---|---|
| **Track/scope alignment** | **Valid** | Track 1 CFP: "Natural Language Processing", "Information Retrieval", "Machine Learning Applications". RegRAG-VN directly addresses retrieval-augmented language models on domestic statutory texts. |
| **Format compliance** | **Valid** | `paper/main.tex` compiles to exactly 6 pages, A4 IEEEtran, 0 overfull hboxes, 0 undefined citations, complete author block with HUST SIS emails. |
| **Deadline feasibility** | **Valid** | 2 days remaining (Sep 13 to Sep 15). Manuscript is fully drafted, compiled, and audited; all 792 campaign rows are scored and verified. Only human labeling and DOI insertion remain. |

---

## STEP 2 — Acceptance Verdict (Standard Senior PC Arm)

Weights: Novelty (20%), Technical Depth (20%), Experimental Rigor (20%), Writing Quality (15%), Impact (10%), Completeness (5%), Venue Fit (10%).

| Criterion | Score | Justification |
|---|---|---|
| **Novelty** | **7.0 / 10** | First benchmark targeting Vietnamese statutory banking regulations with fine-grained article (*Điều*) and clause (*Khoản*) attribution; addresses hierarchical statutory chunking. |
| **Technical depth** | **7.0 / 10** | Provenance discipline with immutable execution tags (`corpus_source`, `retriever_backend`) and coverage gates; decouples evidence conditioning from upstream retrieval recall. |
| **Experimental rigor** | **8.5 / 10** | 792 campaign answers on single-hardware environment (RTX 3090, 4-bit NF4, greedy 512 tokens); all prompt hashes tracked; 3,703-chunk Tier-2 corpus with disambiguated chunk IDs; deterministic lexical scoring. |
| **Writing quality** | **8.0 / 10** | Clear academic voice, disciplined formal register (IELTS Band 8--9), zero LLM filler/sprint jargon, exact narrative grounding in Tables I, II, and III. |
| **Impact** | **7.5 / 10** | Highly relevant to domestic banking, fintech, and legal compliance deployment in Vietnam; exposes the danger of false confidence in unfaithful citations. |
| **Completeness** | **7.0 / 10** | Code, corpus, and 792-row log ready for Zenodo deposit; capped slightly pending human-agreement study completion (Cohen's $\kappa$ and 50-row validation). |
| **Venue fit** | **9.0 / 10** | Tailor-made for RIVF: Vietnamese domain corpus (SBV circulars/decrees/laws), local research team (HUST), hosted in Hanoi. |

**Weighted Score**: $0.20(7.0) + 0.20(7.0) + 0.20(8.5) + 0.15(8.0) + 0.10(7.5) + 0.05(7.0) + 0.10(9.0) = \mathbf{7.45 / 10}$.
**Ceiling Rule Check**: Cap is not triggered. The primary result is a measurement of negative capability (citation unfaithfulness), which is the exact contribution of the benchmark.
**Pass Threshold**: ~5.5–6.0 *(judgment, regional IEEE conference)*.
**Standard Verdict**: **PASS** (Clear margin above venue bar).
**Acceptance Probability**: **78%** *(judgment, base-rate adjusted from estimated 40% base rate for well-executed empirical submissions)*.

---

## STEP 2b — Adversarial Rejection Pass (Hostile Reviewer #2)

**Mandatory Rejection Review**:
> "I recommend **REJECT**. While the paper addresses an interesting domestic domain, it suffers from three fatal methodological flaws:
> 1. *Self-Contained Fixture Generation*: The entire generation campaign of 792 rows was run on 'Tier 1'—a curated fixture of 64 passages where the gold text is guaranteed to be in the prompt. This is an artificial toy setting, not realistic RAG. Real RAG operates over the 3,703-chunk corpus where article retrieval is coin-flip (49.2%). By evaluating generation only under perfect evidence conditioning, the paper measures prompting on cherry-picked text rather than end-to-end RAG.
> 2. *Small and Unvalidated Annotations*: 88 questions total (64 answerable, 24 probes) is very small for an NLP benchmark. Furthermore, the automated scorer is deterministic and unvalidated, and the human agreement cell in Table III is explicitly empty ('--'). The paper admits that 63 of 64 passages were 'repaired' via string substitution from the corpus, which makes the coverage metric self-satisfying.
> 3. *Models Do Not Work*: With a 43--49% citation error rate and clause accuracy below 0.32, these models are completely unfit for regulatory use. The paper merely documents that small 7B models fail at legal reasoning."

### Explicit Reconciliation

| Dimension | Standard PC Reading | Adversarial Reading | Reconciled Finding |
|---|---|---|---|
| **Tier-1 Conditioning** | Isolates generation error from retrieval omission error (methodological control). | Toy setting that artificially inflates context relevance. | **Methodological win, presentation risk**: The paper explicitly discloses Tier 1 as an empirical upper bound (§V-A). For RIVF, this is acceptable because Table III independently measures retrieval over all 3,703 chunks. |
| **Dataset Scale (88 rows)** | Typical for expert-annotated domain benchmarks in low-resource languages (e.g., specialized legal QA). | Small scale; statistical power limited across sub-categories. | **Valid observation**: 88 rows is sufficient for exploratory benchmark characterization at a regional conference, but human $\kappa$ must be inserted to close the validation gap. |
| **Negative Capability Results** | Valuable empirical finding: proves small models cannot be deployed without human verification. | Negative results prove the pipeline fails. | **Standard reading prevails**: Exposing failure modes (citation unfaithfulness, hedge-then-answer) is standard for benchmark papers in AAAI/EMNLP/RIVF. |

**Reconciled Verdict**: **PASS** (Confidence: High). The adversarial objections are largely preempted by the explicit disclosures in §III-A, §III-B, and §V-A.

---

## STEP 3 — Best-Paper Potential

- **Verdict**: **LONG SHOT (Upper 15% contender)**.
- **Comparison to Past Winners**: RIVF best papers (e.g., 2024 IoT botnet detection) typically feature either (a) extensive real-world enterprise/government deployment, or (b) a novel algorithmic architecture that beats competitive baselines by a wide margin.
- **The Gap**: RegRAG-VN is an evaluation/benchmark paper without a proposed novel generator architecture (it uses off-the-shelf Qwen and Vistral with BM25/BGE-M3). While its provenance discipline and citation scoring are highly rigorous, regional IEEE committees tend to favor positive capability breakthroughs over benchmark audits.

---

## STEP 4 — Weaknesses (Reviewer Voice, Ordered by Severity)

1. **MAJOR (Validation Gap)**: "Table III lists Cohen's $\kappa$ as '--' and the human validation study of 50 responses is described as 'pending'. Without these numbers, the reliability of both the benchmark annotations and the lexical evaluation scorer is asserted rather than demonstrated." (Manuscript `paper/main.tex:141, 215`).
2. **MAJOR (Decoupled Retrieval & Generation)**: "The end-to-end RAG pipeline is evaluated in two disconnected halves: Table III evaluates retrieval on the 3,703-chunk Tier-2 corpus, while Tables I and II evaluate generation on the Tier-1 fixture. The paper never reports end-to-end generation quality when fed actual top-3 Tier-2 retrieved chunks." (Manuscript `paper/main.tex:162-177`).
3. **MINOR (Annex Handling)**: "One question (Q036) cites a Phụ lục annex rather than an article, reducing the article denominator to 63. While disclosed, this reveals slight edge-case irregularity in statutory schema parsing." (Manuscript `paper/main.tex:100`).
4. **MINOR (Model Scale)**: "Evaluation is restricted to models $\le$7B under 4-bit quantization. A frontier API baseline (e.g., GPT-4o or Claude 3.5 Sonnet) is missing to establish whether citation unfaithfulness is an intrinsic small-model bottleneck or a universal failure." (Manuscript `paper/main.tex:42, 126`).

---

## STEP 5 — Suggestions for Improvement

1. **(Procedural/P0)**: Complete the 30-row cross-annotated grading (`kappa_grading_{thanh,huong}.csv`) and 50-row scorer validation (`scorer_validation_50.csv`) and insert the computed numbers into Table III and §IV-C before the deadline.
2. **(Presentation/P1)**: In §V-A, reinforce why decoupling generation on Tier 1 from retrieval on Tier 2 is a deliberate experimental design choice (isolating generator error from retriever recall error), citing similar controlled-conditioning protocols in FACTScore or Attributed QA.
3. **(Future Work/P2)**: Note in §VI that future extensions will evaluate 14B/32B parameter models and frontier APIs to measure scaling behavior on statutory citation faithfulness.

---

## STEP 6 — Priority-Ordered Actions

| P | Action | Impact | Effort | Feasible Before Sep 15 Deadline? |
|---|---|---|---|---|
| **P0** | Grade 30-row $\kappa$ subset (`kappa_grading_{thanh,huong}.csv`) and fill Table III | High | Low (1–2 h human work) | **Yes** |
| **P0** | Grade 50-row scorer validation set (`scorer_validation_50.csv`) | High | Low (1 h human work) | **Yes** |
| **P0** | Reserve Zenodo DOI and paste into `Data and Code Availability` | Med | Low (15 min) | **Yes** |
| **P0** | Upload PDF to EDAS `N35414` $\ge$6h early on Tuesday Sep 15 | Critical | Low (30 min) | **Yes** |
| **P1** | Verify teammate SIS email addresses with co-authors | Med | Low (15 min) | **Yes** |

---

## Calibration Record

| Date | Venue | Manuscript Commit | Weighted Score | Acceptance Prob. | Human Verdict | Final Outcome |
|---|---|---|---|---|---|---|
| 2026-09-13 | IEEE RIVF 2026 | `dc90047` | 7.45 / 10 | 78% (judgment) | Pending co-author check | Open (Notif: 2026-10-15) |
