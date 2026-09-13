# RegRAG-VN Kanban

Tracked against GitHub Issues in [alitonia/rag_eval](https://github.com/alitonia/rag_eval/issues) and the [Seminar_2_board](https://github.com/users/alitonia/projects/6) project.
**Target: IEEE-RIVF 2026 — paper deadline 2026-09-15 (hard).** See `docs/PROJECT_PLAN.md` §1.

**P0 right now:** #7 κ subset (Thành & Hương grade 30 rows in `data/human/kappa_grading_{thanh,huong}.csv`) · ~50 scorer validation labels (`data/human/scorer_validation_50.csv`) · Zenodo DOI reservation · EDAS N35414 submission ≥6 h early.

Last re-baselined **2026-09-13** against the live repository and the completed 792-row campaign. Statuses below are *verified*, not claimed — every "done" has a command that demonstrates it.

---

## 🔴 Deadline

| | |
|---|---|
| Paper due | **Tue 2026-09-15**, EDAS `N35414`, ≤6 pp IEEE A4 |
| Days remaining | 2 (as of Sun 09-13) |
| Notification / camera-ready | 2026-10-15 / 2026-11-11 |
| Conference | 2026-12-18→20, VinUniversity Hanoi — **in-person presentation required** |
| Fallback | Special sessions 2026-09-30 (only SS1 *AI for Smart Cities* is even a stretch fit) |

---

## 🟢 DONE (verified 2026-09-13)

- [x] **Generation campaign: 792 rows (3x3x88), 0 errors** *(2026-09-13)* — Completed on RunPod RTX 3090 (`scripts/run_campaign_pod.py`). All rows single-hardware provenance (transformers-4bit, bnb-nf4, float16). Log: `data/eval/generations.json`, `data/eval/generations_meta.jsonl`. Mirrored to private HF repo `hunopapa/regrag-artifacts`.
- [x] **Tier 2 duplicate chunk IDs fixed** *(2026-09-13)* — `scripts/build_corpus_chunks.py` disambiguates 324 colliding IDs with deterministic suffixes (`-2`, `-3`). `data/processed_chunks/corpus_chunks.json` has 3,703 unique chunks over 22 instruments. Idempotency verified.
- [x] **Gate C complete: BM25 + Dense (BGE-M3) measured on Tier 2** *(2026-09-13)*
  - BM25 (`pyvi`): doc@1 0.734, doc@3 **0.906**; article@1 0.381, article@3 **0.492** (`data/eval/bm25_recall_gate_c_2026-09-11.json`).
  - BGE-M3 dense: doc@1 0.719, doc@3 **0.891**; article@1 0.365, article@3 **0.524** (`data/eval/dense_recall_gate_c_2026-09-13.json`).
  - Both pass $\ge$0.7 retrieval gate and order oppositely at article level ($k=3$), proving the retrievers genuinely differ.
- [x] **Table I & II computed and filled** *(2026-09-13)* — `scripts/compute_tables.py` scores all 792 rows with the repository scorer (`data/eval/tables_paper_2026-09-13.json`). Filled in `paper/main.tex`.
- [x] **Paper manuscript complete: 6 pages, 0 errors** *(2026-09-13)* — `paper/main.tex` compiles cleanly with zero warnings/errors. Full §I–§VI narrative, TikZ pipeline figure, Tables I, II, III (dense row filled). Tier-1 campaign corpus disclosed in §V-A. 3 humanize passes completed. Author order: Hoang¹, Huong², Phuc³, Thanh⁴, Ngoc⁵ with ASCII names and SIS emails.
- [x] **Human labeling instruments prepared & verified** *(2026-09-13)* — `scripts/build_human_label_sets.py` (seed=20260913):
  - `data/human/kappa_grading_{thanh,huong}.csv` (30 rows, 24 answerable + 6 probes, 15/15 authorship) + `KAPPA_INSTRUCTIONS.md`.
  - `data/human/scorer_validation_50.csv` (50 rows stratified across 3x3 grid, auto labels pre-filled) + `VALIDATION_INSTRUCTIONS.md`.
- [x] **Zenodo packaging ready** *(2026-09-13)* — `scripts/build_zenodo_bundle.sh` creates dirty-tree-refusing bundle from HEAD (151 MB, includes raw legal sources, code, corpora, eval logs, paper PDF). `zenodo_metadata.json` updated. `scripts/zenodo_deposit.sh` ready to reserve DOI.
- [x] **Test suite: 100% green** *(2026-09-13)* — 10 test modules, 290+ tests passing, 0 errors, 0 failures.
- [x] **Git synced** *(2026-09-13)* — Pushed to `origin/main`.

---

## 🟡 IN PROGRESS (Human-only tasks)

- [ ] **[#7] Cohen's $\kappa$ on 30-question cross-annotated subset** — *Thành & Hương*
  - Thành grades `data/human/kappa_grading_thanh.csv`; Hương grades `data/human/kappa_grading_huong.csv`.
  - Once both return: run `compute_cohens_kappa` and fill the single open cell in Table III (`\kappa` column).
- [ ] **Scorer validation on 50 human labels** — *one grader*
  - Grade 50 rows in `data/human/scorer_validation_50.csv` (`human_correct`, `human_hallucinated`, `human_abstained`).
  - Run `validation_report(pairs)` to compute agreement for §IV-C.
- [ ] **Confirm teammate SIS email addresses** — *Team*
  - Verify: `Huong.DTL20261261M@`, `Thanh.VD20261082M@`, `Ngoc.NKD20261206M@`, `Phuc.NT20252263M@sis.hust.edu.vn`.
- [ ] **Zenodo DOI reservation** — *User*
  - Provide `ZENODO_ACCESS_TOKEN` to reserve DOI and insert into `paper/main.tex`.

---

## ⚪ SUBMISSION DAY (Tue 2026-09-15, $\ge$6h early)

- [ ] Rebuild Zenodo bundle and publish record (`bash scripts/zenodo_deposit.sh dist/zenodo_bundle/regrag-vn-rivf2026 --publish`).
- [ ] Make GitHub repository public.
- [ ] Submit PDF and metadata on EDAS `N35414`.
