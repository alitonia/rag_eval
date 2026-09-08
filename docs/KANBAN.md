# RegRAG-VN Project Kanban Board

Tracked against GitHub Issues in [alitonia/rag_eval](https://github.com/alitonia/rag_eval/issues) and Project Dashboard 6.

---

### 🟢 DONE (Completed)
- [x] **[#1] Architecture Scaffolding & Dual Storage Repositories**
  - *Lead:* Nguyễn Thắng Phúc, Nguyễn Huy Hoàng
  - *Artifacts:* `regrag/storage/` (`InMemoryResultRepository`, `FileResultRepository`), `tests/test_storage.py` passing, tagged `v0.1.0`.
- [x] **Git & Authorship Setup**
  - Configured git user `alitonia <allyofjustice1@gmail.com>`, purged `tun2101`, rewritten commit history.
- [x] **Core Evaluation & Prompt Modules**
  - *Artifacts:* `regrag/evaluation/` (citation regex, Cohen's $\kappa$, metric scorer), `regrag/generation/prompts.py`.
- [x] **Colab Resilience Infrastructure**
  - *Artifacts:* `notebooks/colab_runner.ipynb` with Drive mount, checkpoint restore/save cells.

---

### 🟡 IN PROGRESS (Active Now)
- [ ] **[#6] 100 Gold Banking QA Benchmark**
  - *Lead:* Vũ Đức Thành, Đinh Thị Lan Hương
  - *Current Status:* **64 / 100 questions completed** in `bank_qa_data - QA.csv` (Thành: 50, Hương: 14).
  - *Target:* 100 questions completed by End of Day (EOD).
- [ ] **[#2] QA-Driven Legal Corpus Ingestion**
  - *Lead:* Đinh Thị Lan Hương, Nguyễn Khắc Duy Ngọc
  - *Current Status:* Extracted 16+ legal document links from CSV (Luật Các TCTD 2024, TT 39/2016, TT 17/2024, TT 06/2019, TT 48/2018, TT 08/2023, NĐ 70/2014, NĐ 23/2015, etc.). Ingesting and segmenting into `data/raw_legal/`.
- [ ] **[#3] Clause-Level Legal Document Segmenter & Ground-Truth Alignment**
  - *Lead:* Đinh Thị Lan Hương, Nguyễn Huy Hoàng
  - *Current Status:* Parser running in `scripts/build_corpus_chunks.py`; validating exact snippet matching from `text_contains_answer_in_the_doc`.
- [ ] **Drafting 25 Unanswerable Probes for RQ2**
  - *Lead:* Nguyễn Huy Hoàng
  - *Target:* Synthesize 25 negative/unanswerable regulatory questions (e.g., cryptocurrency regulations under banking circulars, out-of-scope foreign jurisdictions) to evaluate abstention.

---

### 🔵 NEXT UP (Queued upon EOD CSV Handover)
1. **[#7] Dual Annotation Protocol & Cohen's $\kappa$ Calculation**
   - Run pairwise verification across group members on the frozen 100 QA set; calculate inter-annotator agreement score.
2. **[#4 & #5] Finalize BM25 & BGE-M3 Dense Indexes on the Complete Corpus**
   - Re-index all chunks extracted from the 16+ legal documents.
   - Run Recall@1 and Recall@3 sanity check against the 100 ground-truth QA passages.
3. **[#8 & #9] Launch Colab Inference Campaign (9 Configurations)**
   - Upload finalized corpus and QA set to Colab.
   - Execute 1,125 total inferences ($125 \text{ questions} \times 9 \text{ conditions}$) across `Qwen2.5-7B`, `Llama-3.2-3B`, and `Qwen2.5-3B` in 4-bit quantization with Drive checkpointing.

---

### ⚪ BACKLOG (Subsequent Phases)
- [ ] **[#10] Automated Citation Extraction & Precision/Recall Scoring**
- [ ] **[#11] Automated Abstention Classification & Hallucination Rate Analysis**
- [ ] **[#12] Result Aggregation & Comparison Tables/Figures Generation**
- [ ] **[#13] Course LaTeX Report & IEEE 6-Page Manuscript Drafting**
- [ ] **[#14] Final Verification, Reproducibility Audit & Release Packaging**
