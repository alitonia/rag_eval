# Venue Rank — RegRAG-VN vs EASE 2027 (Hanoi) — 2026-09-13

| Venue | Tier | Weighted Score | Acceptance Prob. | Pass Verdict | Best-Paper Verdict | Top P0/P1 Actions |
|---|---|---|---|---|---|---|
| EASE 2027 (Research / RENE Tracks) | CORE A, ACM ICPS | **7.85 / 10** | **68%** *(judgment, base-rate adjusted)* | **PASS** (bar ~6.5–7.0) | **REALISTIC** (RENE track) / **LONG SHOT** (Research) | P0: Expand 6 pp $\to$ 10+2 pp ACM `sigconf`; P0: Anonymize for double-blind; P1: Complete Empirical Standards Checklist |

---

## Manuscript State & Primary Result

- **Manuscript**: `paper/main.tex` at commit `dc90047` (`style: comprehensive academic voice humanization`).
- **Target Edition**: 31st International Conference on Evaluation and Assessment in Software Engineering (EASE 2027), June 15–18, 2027, Hanoi, Vietnam.
- **Current State**: 6 pages IEEE A4; for EASE submission, requires format conversion to ACM `sigconf` (10 pages body + 2 pages references, double-anonymous).
- **Primary Quantitative Result**:
  > Retrieval augmentation raises article-level citation F1 from 0.005 to 0.321--0.434 across 792 single-GPU runs on $\le$7B models; however, 43--49% of RAG-generated answers still produce non-governing or incorrect citations even when gold evidence is in prompt, clause accuracy remains $\le 0.317$, and on the full 3,703-chunk legal corpus, article-level retrieval drops to 49.2--52.4% despite 89.1--90.6% document-level recall.
- **Capability-Reading Test (Step 0.1)**:
  - *Capability Reading*: The system does not reliably work for autonomous regulatory compliance.
  - *Assessment & Empirical Standards Reading*: **Exceptional fit**. EASE was the first conference to adopt the ACM SIGSOFT Empirical Standards. The paper's negative results (citation unfaithfulness, hedge-then-answer behavior, granularity mismatch) paired with frozen coverage invariants and provenance guards match the exact ethos of EASE.

---

## STEP 0 — Venue Resolution & Facts

- **Edition**: 31st EASE (June 15–18, 2027, Hanoi, Vietnam).
- **Deadlines**:
  - *Research Papers Track*: Abstract Fri Jan 15, 2027 / Full Paper Fri Jan 22, 2027 (AoE). Notification: March 12, 2027.
  - *RENE Track (Reproducibility & Negative Results)*: ~Early March 2027 (~Mar 1–2, 2027 based on 2026 pattern).
  - *AI Models / Data Track*: ~Early March 2027.
- **Format**: ACM `sigconf` (`\documentclass[sigconf,review,anonymous]{acmart}`), strictly max 10 pages main text + 2 extra pages references-only. Double-anonymous review.
- **Review Criteria**: Standards-based review via the **Empirical Standards Checklist** (soundness, significance, novelty, verifiability/transparency, presentation). Open Science policy mandatory (open replication package).
- **Acceptance Rate**: Historical full paper rate 33%–44% (CORE A specialist conference; pass bar ~6.5–7.0).
- **Award Profile**:
  - Most Influential Paper (MIP) awards consistently celebrate empirical methodology and meta-science (systematic literature reviews, empirical standards, code smell benchmarks).
  - Best Paper awards reward large-scale empirical studies of software and AI artifacts (e.g., 2026 co-winner: YARA ecosystem census; LLM4SE evaluation studies).

---

## STEP 1 — Fit Check

| Check | Verdict | Evidence |
|---|---|---|
| **Track/scope alignment** | **Valid (Research) / Strongest (RENE)** | EASE CFP explicitly invites *Empirical evaluation of AI models*, *Benchmarking methodologies*, *Meta-science*, and *"Studies with negative findings or non-significant results"*. RENE track is tailor-made for the negative citation finding and provenance audit. |
| **Format compliance** | **Risky (Now) $\to$ Valid (After Expansion)** | Current draft is 6 pp IEEE single-blind. Must be rewritten into ACM `sigconf` (10 pp + 2 pp refs), stripped of author names, and packaged with an anonymized Zenodo replication repo. 4 months of runway available before Jan 22, 2027. |
| **Deadline feasibility** | **Valid** | 124 days remaining to Research track (Jan 22, 2027) and ~165 days to RENE track (Mar 2027). More than ample time to expand narrative, add error taxonomy, and integrate human validation numbers. |

---

## STEP 2 — Acceptance Verdict (Standard Senior PC Arm)

Weights: Novelty (20%), Technical Depth (20%), Experimental Rigor (20%), Writing Quality (15%), Impact (10%), Completeness (5%), Venue Fit (10%).

| Criterion | Score | Justification |
|---|---|---|
| **Novelty** | **7.5 / 10** | Formalizes citation-level faithfulness and hierarchical statutory granularity for RAG evaluation; introduces provenance-guarded benchmark pipelines. |
| **Technical depth** | **8.0 / 10** | Coverage gates, deterministic string substitution audit, immutable metadata (`corpus_source`, `retriever_backend`), and decoupled evidence conditioning provide genuine methodological depth. |
| **Experimental rigor** | **8.5 / 10** | Complete 792-row matrix across 3 models and 3 modes; single-hardware provenance; greedy decoding controls; 3,703-chunk corpus with deduplication. *(Assumes human $\kappa$ and 50-row validation are filled)*. |
| **Writing quality** | **8.0 / 10** | Disciplined academic register, transparent disclosures of limitations, clean tabular presentation. |
| **Impact** | **7.5 / 10** | Establishes cautionary empirical evidence against unverified LLM deployment in safety-critical legal and regulatory compliance software. |
| **Completeness** | **8.0 / 10** | Permanent Zenodo archive, open code, raw corpora, and evaluation logs. |
| **Venue fit** | **8.5 / 10** | Evaluation and assessment is EASE's home ground; fits the Empirical Standards for Benchmark and Evaluation Studies. Hosted in Hanoi (home advantage). |

**Weighted Score**: $0.20(7.5) + 0.20(8.0) + 0.20(8.5) + 0.15(8.0) + 0.10(7.5) + 0.05(8.0) + 0.10(8.5) = \mathbf{7.85 / 10}$.
**Pass Threshold**: ~6.5–7.0 *(CORE A specialist conference bar)*.
**Standard Verdict**: **PASS** (Substantial margin over CORE A bar).
**Acceptance Probability**: **68%** *(judgment, base-rate adjusted from ~35% base acceptance rate for double-blind ACM submissions)*.

---

## STEP 2b — Adversarial Rejection Pass (Hostile Reviewer #2)

**Mandatory Rejection Review**:
> "I recommend **REJECT**. 
> 1. *Domain Fit / Generalizability*: EASE is a software engineering venue. This paper evaluates Vietnamese legal and regulatory QA. Why is an NLP regulatory compliance benchmark being submitted to EASE rather than an NLP venue like EMNLP/ACL or legal AI like JURIX? How does this generalize beyond Vietnamese banking circulars to software engineering artifacts, API documentation, or code compliance?
> 2. *Scale of Dataset*: An 88-question benchmark is insufficient for a full 10-page CORE A paper. Industrial and SE benchmarks at EASE typically evaluate hundreds or thousands of instances (e.g., SWE-bench, Defects4J, repository mining studies).
> 3. *Negative Result without Remedy*: The paper shows small models fail to cite accurately and retrievers fail at article resolution, but it proposes no architectural or prompting solution to fix the problem."

### Explicit Reconciliation

| Dimension | Standard PC Reading | Adversarial Reading | Reconciled Finding |
|---|---|---|---|
| **SE Scope Match** | Regulatory compliance is a critical software requirement for fintech/banking systems; benchmark methodology is core SE meta-science. | Paper reads like an NLP/legal application, not traditional software engineering. | **Crucial Strategy**: When expanding to 10 pp, the paper must frame regulatory RAG as *automated software compliance verification* (checking software features against regulatory specs), citing SE literature on requirements traceability and compliance checking. |
| **Benchmark Scale** | 88 gold questions with verbatim statutory alignment is labor-intensive and expert-authored; 792 full generation runs. | 88 questions is small compared to automated mined datasets. | **Track Routing Decision**: If submitted to the main Research Track, add error analysis and taxonomy across the 88 rows. If routed to the **RENE track**, 88 curated rows with 792 runs is more than sufficient. |
| **Negative Results** | EASE explicitly values negative results that prevent wasted industrial effort and disprove common assumptions. | Lacks a positive fix or algorithm. | **RENE Track Advantage**: The RENE track specifically solicits well-documented negative results where standard techniques (RAG) fail to solve the stated task. |

**Reconciled Verdict**: **PASS** for **RENE Track** (Confidence: High); **BORDERLINE / PASS** for **Research Papers Track** (dependent on SE framing).

---

## STEP 3 — Best-Paper Potential

- **Research Papers Track**: **LONG SHOT (10–15%)**. Competition from large-scale repository mining studies (e.g., YARA 152k-artifact study) and multi-model code-agent audits.
- **RENE Track**: **REALISTIC (Top Contender)**. A rigorous, pre-registered, provenance-guarded demonstration of RAG citation failure in statutory compliance with full Zenodo artifacts matches the exact criteria for EASE RENE awards (often forwarded to *JSEP* special issue).

---

## STEP 4 — Weaknesses for EASE (Reviewer Voice)

1. **CRITICAL (SE Framing)**: "The paper currently frames the problem as an NLP and banking compliance task. To warrant a full paper at EASE, the author must explicitly ground the work in software engineering: compliance verification of software requirements, specification traceability, and validation of automated regulatory checking tools."
2. **MAJOR (Page Budget Expansion)**: "At 6 pages IEEE, the text would be sparse if simply converted to ACM 10+2. A full EASE paper requires an in-depth qualitative error taxonomy, detailed analysis of the 83 token-capped answers, and latency/resource profiling across model families."
3. **MAJOR (Double-Blind Anonymity)**: "All references to HUST, authors, and local repository paths must be rigorously scrubbed, and the replication package hosted on an anonymous repository (e.g., Anonymous GitHub / Zenodo sandbox)."
4. **MINOR (Empirical Standards Compliance)**: "EASE reviewers use formal Empirical Standards rubrics for Benchmark and Evaluation studies. The paper should explicitly include an Empirical Standards appendix or mapping table demonstrating adherence."

---

## STEP 5 — Suggestions for EASE Expansion (Roadmap to Jan 2027)

1. **(Content)**: Reframe Introduction and Related Work: position regulatory RAG as *Automated Regulatory Compliance for Software Systems* (referencing SE compliance standards and API requirement specifications).
2. **(Content)**: Expand Section V with a deep qualitative error taxonomy: categorize the 43–49% citation errors into (a) adjacent-article confusion, (b) cross-instrument false attribution, and (c) statutory obsolescence / hallucinated decree numbers.
3. **(Presentation)**: Convert LaTeX sources to ACM `acmart` with `[sigconf,review,anonymous]`, hydrating full references.
4. **(Procedural)**: Target Research Papers track by Jan 22, 2027; if portfolio priorities prioritize other papers, fall back cleanly to RENE track in early March 2027.

---

## STEP 6 — Priority-Ordered Actions for EASE 2027

| P | Action | Impact | Effort | Timeline |
|---|---|---|---|---|
| **P0** | Port manuscript to ACM `sigconf` 10+2 template with anonymous mode | Critical | Med (2–3 days) | Dec 2026 |
| **P1** | Add qualitative error taxonomy & token-cap analysis into §V | High | Med (2 days) | Dec 2026 |
| **P1** | Reframe §I & §II around SE compliance and requirement verification | High | Med (1–2 days) | Jan 2027 |
| **P2** | Fill ACM SIGSOFT Empirical Standards checklist | Med | Low (3 hours) | Jan 2027 |
| **P3** | Finalize anonymous replication bundle on Zenodo / Figshare | Med | Low (2 hours) | Jan 2027 |

---

## Calibration Record

| Date | Venue | Target Track | Weighted Score | Acceptance Prob. | Status |
|---|---|---|---|---|---|
| 2026-09-13 | EASE 2027 | Research / RENE | 7.85 / 10 | 68% (judgment) | Planning / Post-RIVF Submission |
