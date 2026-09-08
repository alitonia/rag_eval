# RegRAG-VN Kanban

Tracked against GitHub Issues in [alitonia/rag_eval](https://github.com/alitonia/rag_eval/issues) and the [Seminar_2_board](https://github.com/users/alitonia/projects/6) project (statuses, priorities and target dates synced 2026-09-09).
**Target: IEEE-RIVF 2026 — paper deadline 2026-09-15 (hard).** See `docs/PROJECT_PLAN.md` §1.

**P0 right now:** #15 environment deps (blocks #2/#4/#5) · #2 downloads · #6 QA + probes · #13 paper · #11 replace the placeholder scorers.

Last re-baselined **2026-09-09** against the live repository and the trusted QA CSV. Statuses below are *verified*, not claimed — every "done" has a command that demonstrates it.

---

## 🔴 Deadline

| | |
|---|---|
| Paper due | **Tue 2026-09-15**, EDAS `N35414`, ≤6 pp IEEE A4 |
| Days remaining | 6 (as of Wed 09-09) |
| Notification / camera-ready | 2026-10-15 / 2026-11-11 |
| Conference | 2026-12-18→20, VinUniversity Hanoi — **in-person presentation required** |
| Fallback | Special sessions 2026-09-30 (only SS1 *AI for Smart Cities* is even a stretch fit) |

---

## 🟢 DONE (verified 2026-09-09)

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
- [x] **Test suite: 33 passing** — `test_storage`, `test_components`, `test_provenance`, `test_coverage`, `test_parser_passages`.
- [x] **Seed corpus quarantined** — `data/raw_legal/18_2024_TT_NHNN.txt` is **not authentic legal text** (43 lines; Điều 1,2,3,9,14,15,23 — real instruments number contiguously; no recitals, no effective-date clause, no signature block). Its 22 chunks were the entire previous corpus and are invalid. See `INGEST_PLAN.json`.

---

## 🟡 IN PROGRESS

- [ ] **[#6] Gold QA benchmark** — *Thành & Hương*
  - 64/100 written (Thành 50, Hương 14). **Review completes 2026-09-10.**
  - On landing: run `python3 scripts/regenerate.py`. Cache keys are per-question, so only edited questions invalidate.
  - **0 of 20 unanswerable probes written.** These need no corpus and no gold passage — cheapest high-value item left, carries half of RQ2. *Owner: unassigned.*
- [ ] **[#2] Source document downloads** — *Thành & Hương, EOD 09-09*
  - Work from `data/raw_legal/INGEST_PLAN.json`, **priority order**. Top 5 = 51 of 57 questions (89%).
  - **Do these three first** — 30 questions depend on them and their listed URLs are broken:
    - `22/2023/TT-NHNN` → original **404**; use `datafiles.chinhphu.vn/cpp/files/vbpq/2024/01/22-nhnn.pdf`
    - `21/2021/NĐ-CP` → original **403**; use `congbao.chinhphu.vn/van-ban/nghi-dinh-so-21-2021-nd-cp-33477/35291.htm`
    - `32/2024/QH15` → luatvietnam returns 200 but is **probably page 1 of 209 articles**; prefer quochoi.vn
  - Drop each file at `data/raw_legal/<expected_file>` and set its `status` to `downloaded`.
  - **Record an original-vs-consolidated decision** for `22/2023/TT-NHNN` (amended by 22/2025) and `39/2016/TT-NHNN`. Ingesting the original while gold answers quote amended wording produces *false hallucination labels*.
  - 7 questions still `UNRESOLVED`: read the instrument id off the downloaded header and add it to `DOC_MANIFEST.json`.

---

## 🔵 BLOCKED

- [ ] **Environment: no retrieval or extraction dependencies installed** — *blocks #4, #5, and all ingestion*
  - Missing: `sentence-transformers`, `rank_bm25`, `pyvi`, `pypdf`/`pdfplumber`, `beautifulsoup4`/`lxml`. Present: torch 2.13, pandas, numpy.
  - Consequence today: BM25 runs self-declared `DEGRADED`, dense **refuses**, and no PDF or HTML can be read — so tomorrow's 10-instrument ingest cannot run at all.
  - Fix (`--system-site-packages` reuses the installed torch instead of pulling a second copy):
    ```bash
    python3 -m venv --system-site-packages .venv
    .venv/bin/pip install pyvi rank_bm25 pypdf pdfplumber beautifulsoup4 lxml sentence-transformers
    ```
  - This is also why the earlier "BM25 retrieval smoke test" passed: it ran in degraded mode and nothing said so.

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
| Thu 09-10 | Revised CSV → `regenerate.py` · ingest Tier 2 · 20 probes · LaTeX skeleton §I–§IV | **B: coverage ≥80%** |
| Fri 09-11 | Indices + Recall@k · replace placeholder scorers · model sanity probes | **C: Recall@3 ≥0.7** |
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
