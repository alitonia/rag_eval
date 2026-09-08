# Project Plan: RegRAG-VN

**Topic:** Measuring Hallucination and Citation Accuracy of Small Language Models on Vietnamese Banking Regulations with Retrieval-Augmented Generation  
**Target:** Course Deliverable (Seminar 2) & Academic Publication  

---

## 1. Project Team & Responsibility Matrix

| Member | Student ID | Primary Role | Core Responsibilities |
|---|---|---|---|
| **Nguyễn Huy Hoàng** | 20251325M | Architecture & Experiment Lead | Benchmark design, experimental orchestration, metric pipelines, report lead |
| **Đinh Thị Lan Hương** | 20261261M | Legal Corpus Engineering | 10–12 SBV circular curation, clause-level segmentation parser, metadata schema |
| **Vũ Đức Thành** | 20261082M | Gold QA Set & Human Annotation | 100 QA taxonomy design, unanswerable query curation, dual-annotator protocol & Cohen's $\kappa$ |
| **Nguyễn Khắc Duy Ngọc** | 20261206M | Retrieval Pipeline (BM25 & Dense) | Vietnamese word segmentation (`pyvi`), BM25 indexer, dense vector indexer (`BGE-M3`), Recall@k |
| **Nguyễn Thắng Phúc** | 20252263M | Core Framework & Persistence Layers | Software architecture (Repository pattern: In-Memory vs JSON/CSV), CLI/Colab runners, unit tests |

---

## 2. Research Questions & Experimental Matrix

- **RQ1 (Hallucination Reduction):** How much does RAG reduce hallucination compared to closed-book answering for small LLMs ($\le 7\text{B}$) on Vietnamese regulatory questions?
- **RQ2 (Citation & Abstention):** How accurately do models cite supporting articles and clauses, and do they abstain when the corpus does not contain the answer?
- **RQ3 (Sparse vs. Dense Retrieval):** How does sparse retrieval (BM25 with Vietnamese word segmentation) compare with dense multilingual embeddings (`BGE-M3`) in this domain?

### Experimental Conditions (9 per question)
- **Models (3):**
  1. `Qwen/Qwen2.5-7B-Instruct` (4-bit quantization)
  2. `meta-llama/Llama-3.2-3B-Instruct` (4-bit quantization)
  3. `Qwen/Qwen2.5-3B-Instruct` or `Viet-Mistral/Vistral-7B-Chat` (4-bit quantization)
- **Retrieval Modes (3):**
  1. `Closed-book` (Direct zero-shot with system prompt)
  2. `RAG-BM25` (Top-$k=3$ retrieved clauses, BM25 + `pyvi`)
  3. `RAG-Dense` (Top-$k=3$ retrieved clauses, `BAAI/bge-m3`)

---

## 3. Annotation & Evaluation Protocol

### 3.1 Human Annotation Scope: 100 Gold QA Benchmark
Human annotation is concentrated strictly on authoring and validating the **100 Gold Reference Pairs**:
- **Dataset Composition:**
  - 70 answerable questions covering factual extraction, multi-clause synthesis, and boundary/definition checks across the curated SBV circulars.
  - 30 unanswerable questions (out-of-scope, cross-domain, or repealed provisions) to rigorously test abstention.
- **Dual-Annotation Process:**
  - Each question, its reference answer, supporting document ID, and exact article/clause citation are reviewed by two independent annotators.
  - Inter-annotator agreement is computed and reported via **Cohen's $\kappa$** on the categorization rubric before freezing the benchmark.

### 3.2 Automated Evaluation Pipeline (900 Model Responses)
All downstream evaluations across the 9 experimental configurations ($100 \text{ questions} \times 9 \text{ conditions} = 900 \text{ responses}$) are automated by the code pipeline:
- **Citation Precision & Recall:** Deterministic regex and structured schema parser matching cited circulars, articles (Điều), and clauses (Khoản) against ground-truth metadata.
- **Abstention Classification:** Automated classifier evaluating whether the model generated the required abstention response on unanswerable questions (abstention precision, recall, F1).
- **Correctness & Hallucination Scoring:** Automated evaluation using exact reference comparison, lexical overlap, and an automated LLM-as-a-judge scoring component.

---

## 4. Software Architecture & Persistence

### 4.1 Two-Persistence-Layers Requirement
To fulfill course requirements without duplicating business logic:
- `BenchmarkResultRepository` (Abstract Base Class) defines the persistence interface (`save_run()`, `get_run()`, `list_runs()`, `export()`).
- `InMemoryResultRepository`: In-memory dictionary/list store for fast test runs and notebook iteration.
- `FileResultRepository`: File-based store serializing results to structured JSON and CSV formats with atomic file writes.
- Business logic (indexing, retrieval, generation, evaluation) interacts strictly with `BenchmarkResultRepository` via dependency injection.

### 4.2 Colab Execution & Resilience Infrastructure
Per runtime requirements, the Colab notebook (`notebooks/colab_runner.ipynb`) provides:
- Complete environment setup cells (installing `transformers`, `bitsandbytes`, `accelerate`, `pyvi`, `rank-bm25`).
- Google Drive mount and automated checkpoint restore/save cells to guarantee resilience against disconnects.
- Idempotent execution (skips already-generated responses stored in Drive checkpoints).

---

## 5. Phased Execution Workflow

```
[Phase 1: Scaffolding] ──> [Phase 2: Corpus & Retrieval] ──> [Phase 3: Gold Set & Annotation]
                                                                        │
[Phase 6: Paper & Report] <── [Phase 5: Automated Evaluation] <── [Phase 4: Colab Experiment Campaign]
```

### Phase 1: Environment & Architecture Scaffolding
- Initialize project structure, dependencies (`requirements.txt`), and abstract persistence repository.
- Implement and unit-test `InMemoryResultRepository` and `FileResultRepository`.
- Establish Git workflow, coding conventions, and PR practices for all 5 members.

### Phase 2: Corpus Processing & Retrieval Pipeline
- Ingest and clean 10–12 active SBV circulars (and Decree 52/2024/NĐ-CP).
- Implement regex parser segmenting texts into clause-level chunks with parent article metadata.
- Build BM25 indexer with `pyvi` word segmentation.
- Build dense vector indexer using `BAAI/bge-m3`.
- Validate retrieval top-$k$ recall on sample legal queries.

### Phase 3: Gold Set Creation & Human Annotation
- Draft 100 question-answer pairs (70 answerable, 30 unanswerable) with exact legal citations.
- Execute dual independent annotation pass across group members.
- Calculate and report Cohen's $\kappa$ inter-annotator agreement; resolve discrepancies and freeze `questions_100.json`.

### Phase 4: Colab Inference Campaign
- Deploy `colab_runner.ipynb` with Drive checkpoint restore/save.
- Run 4-bit quantized inference for 3 models across Closed-book, RAG-BM25, and RAG-Dense (900 total generations).
- Persist all outputs as structured JSON and CSV records.

### Phase 5: Automated Metric Computation
- Run automated evaluation pipeline on the 900 generated responses:
  - Exact citation precision and recall.
  - Abstention accuracy, precision, and recall on the 30 unanswerable queries.
  - Answer correctness and hallucination rates.
- Generate automated result tables, statistical significance summaries, and comparison charts.

### Phase 6: LaTeX Report & Deliverable Packaging
- Assemble LaTeX report following the course template / IEEE 6-page format.
- Integrate verified result tables and figures.
- Review codebase, verify tests, ensure all member contributions are committed, and package release artifact.
