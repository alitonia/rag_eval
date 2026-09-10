# RegRAG-VN Kanban

Tracked against GitHub Issues in [alitonia/rag_eval](https://github.com/alitonia/rag_eval/issues) and the [Seminar_2_board](https://github.com/users/alitonia/projects/6) project (statuses, priorities and target dates synced 2026-09-09).
**Target: IEEE-RIVF 2026 — paper deadline 2026-09-15 (hard).** See `docs/PROJECT_PLAN.md` §1.

**P0 right now:** Colab campaign (`notebooks/colab_runner.ipynb`, model set settled: qwen-7b + qwen-3b + vistral-7b) → Tables I–II + dense row of Table III · #7 κ subset (Thành & Hương) · §V–§VI · EDAS N35414 submission ≥6 h early.

Last re-baselined **2026-09-11** against the live repository and the trusted QA CSV. Statuses below are *verified*, not claimed — every "done" has a command that demonstrates it. Full session detail: `docs/HANDOFF_2026-09-11.md` §0.

---

## 🔴 Deadline

| | |
|---|---|
| Paper due | **Tue 2026-09-15**, EDAS `N35414`, ≤6 pp IEEE A4 |
| Days remaining | 4 (as of Fri 09-11) |
| Notification / camera-ready | 2026-10-15 / 2026-11-11 |
| Conference | 2026-12-18→20, VinUniversity Hanoi — **in-person presentation required** |
| Fallback | Special sessions 2026-09-30 (only SS1 *AI for Smart Cities* is even a stretch fit) |

---

## 🟢 DONE (verified 2026-09-11)

- [x] **[#1] Architecture scaffolding & dual storage** — `regrag/storage/`, `tests/test_storage.py`. `file_repo.py` no longer swallows write/parse errors silently.
- [x] **Data layer: canonical CSV → benchmark schema** *(new)*
  - `regrag/corpus/canonical.py` — URL→`doc_id` (manifest, then slug regex, else loud `UNRESOLVED:`), passage→`Điều`/`Khoản`, two-tier text normalisation.
  - `regrag/corpus/qa_loader.py` — the only sanctioned CSV reader. 64 questions → 57 resolved ids, **10 distinct instruments**, article gold 64/64.
  - `data/raw_legal/DOC_MANIFEST.json` — human-verified URL map + `unreachable_sources` (with working replacement URLs) + `amendments`.
  - `scripts/load_qa_csv.py`, `data/gold/questions_canonical.json`.
- [x] **Gold-label correctness fixes** *(new)*
  - `doc_id` is no longer regexed out of answer prose (only 2/64 passages name their instrument — that was the cause of 83 `UNKNOWN` citations and 48/64 all-UNKNOWN questions).
  - `regrag/evaluation/citation.py`: broadcasting bug fixed (Điều 5 no longer inherits Điều 8's clause); patterns extended to Luật / Bộ luật / Quyết định / Pháp lệnh / Công văn; P/R tightened so a right-article/wrong-document citation scores 0.
  - `prefer_passage_named_doc` corrected **Q007** and **Q064**, whose gold citation pointed at the wrong instrument.
- [x] **[#3 partial] Segmenter hardened** — `regrag/corpus/parser.py`: preamble no longer discarded, `Phần`/`Chương` nesting for Luật, PDF artefacts (`Đi ều 2`, `Điều8`, page footers), and `parse_with_report()` so nothing is dropped silently. Validated against all 64 real CSV passages: **63/64 segment with zero text loss**. The one failure (Q007) is a point-level citation, correctly declined.
- [x] **Tier 1 development corpus** *(new)* — `scripts/build_tier1_corpus.py` → `data/processed_chunks/tier1_chunks.json`, 64 chunks, **100% strict coverage**, all stamped `tier1_passages`. Lets retrieval/generation be integrated before the real documents arrive. **Never publishable** — `assert_publishable` refuses it.
- [x] **Provenance discipline** *(new)* — `regrag/provenance.py`. Three silent-substitution paths eliminated: the `dense.py` mock that returned corpus-order chunks with fabricated scores (this would have faked RQ3 entirely), `bm25.py`'s unlabelled downgrades, and `metrics.py`'s confident placeholder numbers. Every result row now carries `corpus_source` / `retriever_backend`; `assert_publishable()` refuses `UNSET`, `DEGRADED` and Tier 1 rows.
- [x] **Ingestion pipeline rebuilt** *(new)* — `scripts/build_corpus_chunks.py` is now manifest-driven (`data/raw_legal/INGEST_PLAN.json`), handles txt/pdf/html, fails loud, flags any extraction with no "Điều" as suspect, and refuses to write an empty corpus. Previously it hardcoded one entry and `continue`d past missing files, so a partial delivery would print "Saved 0 total chunks" and exit 0.
- [x] **Idempotent regeneration** *(new)* — `scripts/regenerate.py`: CSV content hash, per-question cache keys (a revision touching 6 questions does not invalidate 2,000 cached generations), coverage report per corpus file, verified NO-OP on re-run.
- [x] **Test suite: 269 passing** (was 33 at the 09-09 re-baseline) — adds squash-tier, repair-guards, articleless-whole-doc, harness, metrics, probes modules.
- [x] **Seed corpus quarantined** — `data/raw_legal/18_2024_TT_NHNN.txt` is **not authentic legal text** (43 lines; Điều 1,2,3,9,14,15,23 — real instruments number contiguously; no recitals, no effective-date clause, no signature block). Its 22 chunks were the entire previous corpus and are invalid. See `INGEST_PLAN.json`.
- [x] **[#15] Environment resolved** *(2026-09-11)* — `.venv` has `sentence-transformers`, `rank_bm25`, `pyvi`, `pypdf`, `pdfplumber`, `bs4`, `lxml`; system tesseract 5.3.4 with `vie`.
- [x] **[#6] Gold QA benchmark: 88 rows, verified and corrected** *(2026-09-11)* — 64 answerable + 24 probes (probe rows pinned to explicit IDs Q066–Q088 + Q037). 26 rows corrected from verified primary sources (`scripts/correct_gold_labels.py`; evidence in `TT41_FINDINGS.md`/`TT39_FINDINGS.md`): CAR block re-pointed to TT 41/2016 + TT 22/2023, lending block to the 39/2016 VBHN / TT 21/2017, Q037 converted to a coverage-gap probe, Q065's phantom instrument numbers fixed. 63/64 passages repaired to verbatim article text under guards A/B/C (`scripts/repair_gold_passages.py`, originals in `data/gold/passage_repair_log.json`). **64/64 doc_ids resolved.** Remaining for #6: the κ subset only.
- [x] **[#2] Source documents complete** *(2026-09-11)* — 23 documents ingested, 3,703 chunks, every cited instrument present (real TT 22/2023 official scan fetched + OCR'd; VBHN 39/2016 as single primary; TT 21/2017; Công văn 276/2017 via the articleless wholedoc opt-in). Original-vs-consolidated decisions recorded per instrument in `INGEST_PLAN.json`. Verify: `scripts/build_corpus_chunks.py --allow-missing` → chunks 3703, missing 0.
- [x] **Gate B passed** *(settled 2026-09-11)* — Gate B redefined as provision-level (cited Điều present in cited instrument); verbatim strict coverage **63/64 = 98.44%** reported as a data-quality metric with the repair's partial self-satisfaction disclosed. Verify: `scripts/regenerate.py --force`.
- [x] **Extraction hardening** *(2026-09-11)* — `build_corpus_chunks.py` prefers pdfplumber (pypdf inserts intra-word spaces in four CÔNG BÁO layers: single-char-token ratio 0.11–0.13 → 0.02–0.06); whitespace-squash match tier added as a distinct damage category; 14 corrupt/absent text layers OCR'd.
- [x] **[#4 sparse half] Gate C BM25 measured** *(2026-09-11)* — `scripts/eval_bm25_recall.py` + `data/eval/bm25_recall_gate_c_2026-09-11.json`, reproduced twice. Doc-level 0.734@1 / **0.906@3** (≥0.7 bar: PASS); article-level 0.381@1 / 0.492@3 — the doc≫article gap is a finding and sets the citation-recall ceiling for RAG modes. Dense half + the "must differ" clause of Gate C settle on Colab.
- [x] **[#8/#9 partial] Harness built** *(2026-09-11)* — `notebooks/colab_runner.ipynb` regenerated (31 cells: setup, Drive checkpoint/resume, sanity probe cell 11, `HUMAN_APPROVED_MODELS` human gate cell 13, campaign + provenance-guarded aggregation). Phúc's vLLM serving scripts merged (`feat/load_model` 3532f36 now in main's history). Model set settled: **qwen-7b + qwen-3b + vistral-7b**; llama-3b = labelled weak-Vietnamese contrast only; qwen-1.5b dropped.
- [x] **[#13 partial] Paper §I–§IV complete prose** *(2026-09-11)* — `paper/main.tex` compiles clean (0 errors, 0 overfull, 5 pp); §III synced to 64/24/63/40 + squash tier + repair disclosure; Table III BM25 row filled from the Gate C log; §V–§VI carry `% TODO(results)` markers.
- [x] **[#11] Placeholder scorers replaced** *(2026-09-10/11)* — groundedness/citation/abstention scorers in `regrag/evaluation/metrics.py` with `metric_status` discipline and publishability asserts on all aggregators; pinned by `tests/test_metrics.py`. Remaining: validation against ~50 human-labelled responses (pairs with the κ subset).

---

## 🟡 IN PROGRESS

- [ ] **Colab generation campaign** — *blocker for §V*
  - Run `notebooks/colab_runner.ipynb` on a T4 (~4.1 h for 3 models × 3 modes × 88; Drive-resumable). **Cell 13 requires a human to set `HUMAN_APPROVED_MODELS = ["qwen-7b", "qwen-3b", "vistral-7b"]` after reading the cell-11 sanity probe.** Never run generation or embedding builds locally.
  - Output: campaign log → `scripts/run_eval.py` → Tables I–II + Table III dense row.
- [ ] **[#7] Inter-annotator reliability** — *Thành & Hương* — κ on the 30-question genuinely cross-annotated subset (each grades the other's questions); also feeds the ~50-response scorer validation. Last human-only dependency before §V.

---

## 🔵 BLOCKED

*(nothing blocked on environment or data as of 2026-09-11; the only external dependency is Colab GPU time)*

---

## ⚪ NEXT UP

### [#4 / #5] Retrieval — *Ngọc*
- [ ] Index Tier 2 with BM25 (`pyvi`) and BGE-M3; measure Recall@1 / Recall@3.
- [ ] **Gate C: Recall@3 ≥ ~0.7 and BM25 vs dense must actually differ.** Below that the RAG arm is not measuring retrieval — pivot, don't continue.
- [ ] Confirm every result row carries a clean backend tag (`bm25-rank_bm25+pyvi`, `BAAI/bge-m3`) — never `DEGRADED:`.

### [#8 / #9] Inference — *Phúc*
- [ ] `notebooks/colab_runner.ipynb` is **5 cells with zero outputs — it has never been executed.** Build the real harness: setup, Drive checkpoint save/restore, resume.
- [ ] Per-model **prompt-format sanity probe** (3 fixed questions, human-eyeballed) before any campaign. A wrong chat template produces degenerate output that reads as "this model hallucinates".
- [ ] Model set: 3 confirmed Vietnamese-capable models. `Llama-3.2-3B` is English-centric — include only as a labelled weak-Vietnamese contrast, never as a peer.
- [ ] If scaling to 5 models, serve via vLLM on one GPU rather than 5 sequential Colab loads.

### RAG variants — *Hoàng*
- [ ] Chunking-granularity variants (Điều / Khoản / document) × BM25 / dense. This is the most novel axis and the cheapest to extend — each variant is a config parameter, not a new integration.

### [#10 / #11] Evaluation — *owner: unassigned*
- [ ] **Replace the placeholder scorers in `regrag/evaluation/metrics.py`.** `correctness_score` is currently derived entirely from citation P/R (the answer text is never compared to the gold answer), and `hallucinated` is False for a fabricated answer that emits no citation — backwards. Abstention is 3 hardcoded keyphrases.
- [ ] Recommended basis: groundedness against the retrieved passage + citation P/R + abstention accuracy, **validated on ~50 human-labelled responses with the agreement reported**.
- [ ] Records stay tagged `metric_status="placeholder"` until replaced. Do not report them.

### [#7] Inter-annotator reliability — *Thành & Hương*
- [ ] κ on a **30-question genuinely cross-annotated subset** (Thành grades Hương's, Hương grades Thành's). κ on self-annotation measures nothing, and the AI-Foundations track chair is an ML-theory person who will notice.

### [#13 / #14] Paper & packaging — *owner: unassigned*
- [ ] **No `.tex` file exists in the repository.** ~3 of the 6 pages need no results (§I intro with regional-relevance framing, §II related work, §III benchmark, §IV method) — draft those on 09-10/09-11 so only §V–§VI compete with the campaign.
- [ ] Cite Qin, *"Mix-of-Granularity: Optimize the Chunking Granularity for RAG"* (COLING 2025) — the AI-Applications track chair, and directly relevant to clause-level segmentation.
- [ ] Publish repo + Zenodo DOI **at submission** and add an availability statement; the committee treats its absence as a red flag.
- [ ] **Open the EDAS N35414 entry now** with title and abstract. Having results and no submission slot is the classic way to miss a hard deadline. Submit ≥6 h early on 09-15.
- [ ] Budget 3 tables and 1 figure — 3 RQs × 9 conditions × κ × 3 metrics will not fit 6 pages.

---

## Schedule

| Date | Work | Gate |
|---|---|---|
| Wed 09-09 | Data layer + provenance ✅ · EDAS entry · install deps · downloads begin | A |
| Thu 09-10 | Revised CSV → `regenerate.py` ✅ · ingest Tier 2 ✅ · probes ✅ · LaTeX §I–IV ✅ | **B: coverage ≥80% ✅ (provision-level, settled 09-11; strict 98.44%)** |
| Fri 09-11 | Recall@k ✅ (BM25: doc@3 0.906) · scorers ✅ · harness + sanity gate ✅ | **C: sparse PASS; dense half on Colab** |
| Sat 09-12 | Inference campaign, checkpointed | D |
| Sun 09-13 | Metrics, tables, figures · 50 human labels · κ subset | — |
| Mon 09-14 | §V–§VI · clean compile ≤6 pp · artifacts + availability statement | — |
| Tue 09-15 | **Submit ≥6 h early** | — |

If Gate B or C fails on 09-11, decide that day: SS1 (09-30, needs reframing) vs RIVF 2027 / SOICT 2027.

---

## ⛔ Standing rules

- **`data/gold/bank_qa_data.csv` is the only trusted artifact.** Everything else is derived — regenerate, never hand-edit.
- **A placeholder must fail loudly or self-identify.** Never return a plausible default. This repo already had three paths that silently fabricated results.
- **No number reaches a paper table without a clean provenance tag.** `assert_publishable()` enforces it.
- **Dual submission is forbidden** by the RIVF CFP — this work cannot also go to SOICT 2026 or a journal.
- Verify commands by module name; `pytest` is not installed and `unittest discover` fails (no `tests/__init__.py`).
