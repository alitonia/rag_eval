# Project Plan: RegRAG-VN

**Topic:** Measuring Hallucination and Citation Accuracy of Small Language Models on Vietnamese Banking Operations & Regulatory Compliance with Retrieval-Augmented Generation  
**Target:** Course Deliverable (Seminar 2) & Academic Publication  
**Workflow Paradigm:** QA-Driven Corpus Ingestion & Automated Metric Evaluation  

---

## 1. Project Team & Responsibility Matrix

| Member | Student ID | Primary Role | Core Responsibilities | Current Focus |
|---|---|---|---|---|
| **Nguyễn Huy Hoàng** | 20251325M | Architecture & Experiment Lead | Benchmark design, experimental orchestration, CSV ingestion pipeline, paper lead | Pipeline integration & unanswerable probe design |
| **Đinh Thị Lan Hương** | 20261261M | Domain QA & Legal Engineering | Authoring bank QA set, legal source link verification, Điều/Khoản extraction | Completing 100 QA pairs by EOD (14 submitted) |
| **Vũ Đức Thành** | 20261082M | Domain QA & Benchmark Lead | Authoring bank QA set, question taxonomy, dual annotation protocol & Cohen's $\kappa$ | Completing 100 QA pairs by EOD (50 submitted) |
| **Nguyễn Khắc Duy Ngọc** | 20261206M | Retrieval Pipeline (BM25 & Dense) | Vietnamese word segmentation (`pyvi`), BM25 indexer, BGE-M3 vector indexer, Recall@k | Ingesting documents cited by the 100 QA set |
| **Nguyễn Thắng Phúc** | 20252263M | Core Framework & Persistence Layers | Dual repository pattern (InMemory vs JSON/CSV), Colab runner, unit tests | Ground-truth retrieval alignment & Colab harness |

---

## 2. Research Scope & Experimental Matrix

### 2.1 Refined Regulatory Domain
Based on the real QA dataset authored by the group, the scope covers critical high-stakes banking operations:
- **Lending & Credit Operations:** *Luật Các tổ chức tín dụng 2024* (Điều 134, 135), *Thông tư 39/2016/TT-NHNN* (lending conditions, default interest limits).
- **Foreign Exchange Management:** *Thông tư 06/2019/TT-NHNN*, *Thông tư 08/2023/TT-NHNN*, *Nghị định 70/2014/NĐ-CP*.
- **Deposit & Payment Accounts:** *Thông tư 48/2018/TT-NHNN* (savings deposits), *Thông tư 17/2024/TT-NHNN* (payment accounts & biometric authentication).
- **Collateral, Notarization & Branch Operations:** *Luật Công chứng 2024*, *Nghị định 23/2015/NĐ-CP*, *Nghị định 21/2021/NĐ-CP*, *Thông tư 61/2025/TT-NHNN*.

### 2.2 Research Questions
- **RQ1 (Hallucination Reduction):** How much does RAG reduce hallucination compared to closed-book answering for small LLMs ($\le 7\text{B}$) on Vietnamese banking compliance questions?
- **RQ2 (Citation & Abstention):** How accurately do models cite supporting articles/clauses, and do they abstain when asked unanswerable or out-of-scope regulatory queries?
- **RQ3 (Sparse vs. Dense Retrieval):** How does BM25 (with Vietnamese compound word segmentation) compare with multilingual dense embeddings (`BGE-M3`) in legal retrieval?

### 2.3 Experimental Conditions (9 per question)
- **Models (3):**
  1. `Qwen/Qwen2.5-7B-Instruct` (4-bit BnB)
  2. `meta-llama/Llama-3.2-3B-Instruct` (4-bit BnB)
  3. `Qwen/Qwen2.5-3B-Instruct` or `Viet-Mistral/Vistral-7B-Chat` (4-bit BnB)
- **Retrieval Modes (3):**
  1. `Closed-book` (Direct zero-shot with system prompt)
  2. `RAG-BM25` (Top-$k=3$ retrieved clauses, BM25 + `pyvi`)
  3. `RAG-Dense` (Top-$k=3$ retrieved clauses, `BAAI/bge-m3`)

---

## 3. Dataset Architecture & Annotation Protocol

### 3.1 QA-Driven Corpus Ingestion
Rather than crawling generic circulars, the corpus is determined directly by the 100 QA pairs:
- Each QA item contains `doc_link` and `text_contains_answer_in_the_doc`.
- All referenced official documents (~16 legal instruments) are ingested into `data/raw_legal/` and segmented at the clause level into `data/processed_chunks/corpus_chunks.json`.
- Guarantees 100% ground-truth passage presence in the retrieval corpus.

### 3.2 Benchmark Composition
- **100 Answerable Questions:** Authored by Hương and Thành by EOD, covering factual compliance, synthesis, and definitions.
- **25 Unanswerable Probes:** Authored by Hoàng/Ngọc/Phúc (e.g. cross-jurisdictional questions, repealed circulars, or cryptocurrency regulation) to test model abstention (RQ2).
- **Dual Annotation Protocol:** Two independent annotators review each gold question, and inter-annotator reliability is measured via **Cohen's $\kappa$**.

### 3.3 Automated Evaluation Pipeline
- 125 questions $\times$ 9 conditions = 1,125 generations evaluated automatically:
  - **Citation Precision & Recall:** Regex extraction matching exact circular, article (Điều), and clause (Khoản).
  - **Abstention Accuracy:** Automated classification of standard abstention keyphrases.
  - **Answer Correctness & Hallucination Rate:** Automated lexical/semantic comparison against gold answers.

---

## 4. Phased Execution Roadmap & Status

```
[Phase 1: Scaffolding] (DONE) ──> [Phase 2: QA-Driven Corpus] (IN PROGRESS)
                                            │
[Phase 3: 100 QA Benchmark & Validation] <──┘ (IN PROGRESS - EOD)
       │
[Phase 4: Colab Inference Campaign] ──> [Phase 5: Automated Evaluation] ──> [Phase 6: Report]
```

### Phase Status Overview

| Phase | Description | Status | Primary Output |
|---|---|---|---|
| **Phase 1** | Architecture Scaffolding & Dual Storage | **COMPLETED** | Abstract repository, InMemory & File backends, unit tests (`v0.1.0`) |
| **Phase 2** | QA-Driven Corpus Curation & Chunking | **IN PROGRESS** | 16 legal docs from QA links, regex clause segmenter, BM25/Dense indexes |
| **Phase 3** | Gold QA Benchmark (100 QA + 25 Unanswerable) | **IN PROGRESS (EOD)** | `bank_qa_data - QA.csv` (64/100 done), dual-annotator Cohen's $\kappa$ |
| **Phase 4** | Colab Inference Campaign (9 conditions) | **READY / QUEUED** | `notebooks/colab_runner.ipynb` with Drive backup/restore |
| **Phase 5** | Automated Evaluation & Metric Aggregation | **QUEUED** | Citation P/R, abstention accuracy, hallucination comparison tables |
| **Phase 6** | IEEE LaTeX Report & Final Packaging | **QUEUED** | 6-page manuscript, verified reproducibility artifacts |
