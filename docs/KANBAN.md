# RegRAG-VN Project Kanban Board

Tracked against GitHub Issues in [alitonia/rag_eval](https://github.com/alitonia/rag_eval/issues) and Project Dashboard 6.

---

### 🟢 DONE (Completed)
- [x] **[#1] Architecture Scaffolding & Dual Storage Repositories**
  - *Lead:* Nguyễn Thắng Phúc, Nguyễn Huy Hoàng
  - *Artifacts:* `regrag/storage/` (`InMemoryResultRepository`, `FileResultRepository`), `tests/test_storage.py` passing, tagged `v0.1.0`.
- [x] **Git & Authorship Configuration**
  - Configured git user `alitonia <allyofjustice1@gmail.com>`, purged `tun2101`, rewritten clean commit history.
- [x] **Core Evaluation & Prompt Modules**
  - *Artifacts:* `regrag/evaluation/` (citation regex, Cohen's $\kappa$, metric scorer), `regrag/generation/prompts.py`.
- [x] **Colab Resilience Infrastructure**
  - *Artifacts:* `notebooks/colab_runner.ipynb` with Drive mount, checkpoint restore/save cells.
- [x] **Seed Legal Corpus & Chunking Pipeline**
  - *Artifacts:* `data/raw_legal/CATALOG.md`, `18_2024_TT_NHNN.txt`, `scripts/build_corpus_chunks.py`, BM25 retrieval smoke test.
- [x] **QA Import Pipeline & Dataset Snapshot**
  - *Artifacts:* `data/gold/bank_qa_data.csv` (local copy), `scripts/import_qa_csv.py`, `data/gold/questions_in_progress.json` (64 questions validated).

---

### 🟡 IN PROGRESS (Currently Active)
- [ ] **[#6] 100 Gold Banking QA Benchmark**
  - *Assignees:* **Vũ Đức Thành & Đinh Thị Lan Hương**
  - *Status:* **64 / 100 questions completed** in `data/gold/bank_qa_data.csv` (Thành: 50, Hương: 14).
  - *Active Work:* Writing the remaining 36 questions to finish by **End of Day (EOD) today**.

---

### 🔵 NEXT UP (Assigned to Members for Today & EOD Handover)

#### For Nguyễn Khắc Duy Ngọc:
- [ ] **[#2] Legal Corpus Ingestion from QA Sources:**
  - Download and ingest the full texts of the 16 legal documents identified from `bank_qa_data.csv` into `data/raw_legal/`.
- [ ] **[#3] Full Clause Segmentation:**
  - Run `scripts/build_corpus_chunks.py` to segment all 16 legal texts into `data/processed_chunks/corpus_chunks.json`.

#### For Nguyễn Thắng Phúc:
- [ ] **[#8] Colab 4-Bit Preflight Test:**
  - Open `notebooks/colab_runner.ipynb` on Google Colab T4.
  - Test-load `Qwen/Qwen2.5-7B-Instruct` in 4-bit (`load_in_4bit=True`) and verify Drive checkpoint synchronization.

#### For Nguyễn Huy Hoàng (You):
- [ ] **Draft 25 Unanswerable Probes for RQ2:**
  - Author 25 out-of-scope/unanswerable regulatory questions to evaluate model abstention.
- [ ] **Finalize Citation & Metric Extraction Script ([#10]):**
  - Verify regex citation extraction across all phrasing variants in the 64+ questions.

#### For Group (Upon EOD Handover):
- [ ] **[#7] Dual Annotation Protocol:**
  - Run cross-check pass between Hương and Thành on the 100 QA set; calculate Cohen's $\kappa$ inter-annotator agreement.
- [ ] **[#4 & #5] Retriever Sanity & Benchmark:**
  - Index the complete corpus with BM25 (`pyvi`) and BGE-M3; test Recall@1 and Recall@3 against ground-truth passages.
- [ ] **[#9] Launch 900-Inference Campaign on Colab:**
  - Execute batch generation across 3 models $\times$ 3 modes with automatic checkpointing.

---

### ⚪ BACKLOG (Subsequent Phases)
- [ ] **[#11] Automated Abstention Classification & Hallucination Rate Analysis**
- [ ] **[#12] Result Aggregation & Comparison Tables/Figures Generation**
- [ ] **[#13] Course LaTeX Report & IEEE 6-Page Manuscript Drafting**
- [ ] **[#14] Final Verification, Reproducibility Audit & Release Packaging**
