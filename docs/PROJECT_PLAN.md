# Project Plan: RegRAG-VN

**Topic:** Measuring Hallucination and Citation Accuracy of Small Language Models on Vietnamese Banking Regulations with Retrieval-Augmented Generation  
**Target Tracks:** Course Deliverable (Seminar 2 / Chuyên đề 2) + RIVF 2026 (IEEE, 6 pages, deadline Sep 15, 2026)  
**Date of Baseline:** 2026-09-08  

---

## 1. Project Team & Responsibility Matrix

| Member | Student ID | Primary Role | Core Responsibilities |
|---|---|---|---|
| **Nguyễn Huy Hoàng** | 20251325M | Architecture & Benchmark Lead | Benchmark design, experimental orchestration, evaluation metrics, LaTeX report lead |
| **Đinh Thị Lan Hương** | 20261261M | Legal Corpus Engineering | 10–12 SBV circular curation, clause-level segmentation parser, metadata schema |
| **Vũ Đức Thành** | 20261082M | Gold Set & Annotation Lead | 100 QA taxonomy design, unanswerable query curation, dual-annotator protocol & Cohen's $\kappa$ |
| **Nguyễn Khắc Duy Ngọc** | 20261206M | Retrieval Pipeline (BM25 & Dense) | Vietnamese tokenization (pyvi/underthesea), BM25 indexer, BGE-M3 / multilingual dense indexer, Recall@k |
| **Nguyễn Thắng Phúc** | 20252263M | Core App & Dual Persistence | Software architecture (Repository pattern: In-Memory vs JSON/CSV), CLI/Colab runners, unit testing |

---

## 2. Research Questions & Experimental Matrix

- **RQ1 (Hallucination reduction):** Closed-book vs. RAG with small LLMs ($\le 7\text{B}$) on domain-specific Vietnamese legal QA.
- **RQ2 (Citation & Abstention):** Precision/Recall of citing specific Điều/Khoản, and accuracy on 30 unanswerable queries.
- **RQ3 (Sparse vs. Dense Retrieval):** BM25 (word-segmented) vs. Multilingual Dense Embeddings (`BAAI/bge-m3` or `bkai-foundation-models/vietnamese-bi-encoder`).

### 3x3 Experimental Matrix (9 conditions per question)
- **Models (3):**
  1. `Qwen/Qwen2.5-7B-Instruct` (4-bit BnB / AWQ)
  2. `meta-llama/Llama-3.2-3B-Instruct` (4-bit BnB)
  3. `bkai-foundation-models/vietnamese-bi-encoder` + `Qwen/Qwen2.5-3B-Instruct` (or `Viet-Mistral/Vistral-7B-Chat`)
- **Retrieval Modes (3):**
  1. `Closed-book` (Direct zero-shot with system prompt)
  2. `RAG-BM25` (Top-$k=3$ retrieved chunks, BM25 + pyvi/underthesea)
  3. `RAG-Dense` (Top-$k=3$ retrieved chunks, BGE-M3 / e5-multilingual)

---

## 3. Architecture & Course Deliverable Compliance

### 3.1 Two-Persistence-Layers Requirement
To fulfill the course requirement without touching business logic:
- Define `BenchmarkResultRepository` interface.
- Implement `InMemoryResultRepository` (Python memory dict/list).
- Implement `FileResultRepository` (JSON / CSV on disk with atomic writes).
- Dependency injection handles switching at configuration time without modifying retrieval, generation, or evaluation services.

### 3.2 System Components
```
regrag/
├── corpus/               # Document ingestion & legal parser (Điều/Khoản/Điểm)
├── indexing/             # BM25 and Dense vector indexes
├── retrieval/            # Query processor & hybrid/dense/sparse retrieval
├── generation/           # Prompt templates, model loader (4-bit), LLM callers
├── evaluation/           # Citation extraction, abstention judge, correctness rubric
├── storage/              # Repository pattern (InMemory vs File/JSON/CSV)
└── cli.py                # Command-line interface
```

---

## 4. 7-Day Sprint Schedule (Sep 8 – Sep 15, 2026)

| Day | Milestone | Key Deliverables | Owners |
|---|---|---|---|
| **Day 1 (Sep 8)** | **Scaffolding & Scope Freeze** | • Freeze list of 10–12 active SBV circulars<br>• Repo structure & abstract repository interface<br>• Gold set schema defined | All |
| **Day 2 (Sep 9)** | **Corpus Parsing & Baseline Indexing** | • Clause-level JSON corpus produced<br>• BM25 + BGE-M3 indexing pipeline functioning<br>• First 40 gold QA pairs drafted | Hương, Ngọc, Thành |
| **Day 3 (Sep 10)** | **Gold Set Completion & Colab Harness** | • Full 100 QA pairs completed (70 answerable, 30 unanswerable)<br>• Colab notebook with 4-bit model inference running | Thành, Phúc, Hoàng |
| **Day 4 (Sep 11)** | **Dual-Annotation & Experiment Campaign** | • Inter-annotator pass on 100 QA pairs (Cohen's $\kappa$ computed)<br>• Full 9-condition inference run on Colab, raw results saved | All (Annotation)<br>Hoàng, Phúc |
| **Day 5 (Sep 12)** | **Evaluation & Metric Aggregation** | • Citation precision/recall parser run<br>• Abstention accuracy & Hallucination rate computed<br>• Result tables and comparison figures generated | Ngọc, Phúc, Hoàng |
| **Day 6 (Sep 13)** | **LaTeX Report / Draft Assembly** | • 6-page IEEE template draft written<br>• Introduction, Related Work, Method, Results, Discussion | Hoàng (lead), all |
| **Day 7 (Sep 14)** | **Polish & Camera-Ready Packaging** | • Self-audit against checklist, bibtex cleanup, code cleanup<br>• Tag v1.0.0 on GitHub, compile final PDF | Hoàng, all |
| **Sep 15** | **Submission Deadline** | • Submit to RIVF 2026 / Course milestone submission | Hoàng |
