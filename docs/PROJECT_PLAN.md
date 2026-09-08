# Project Plan: RegRAG-VN

**Topic:** Measuring Hallucination and Citation Accuracy of Small Language Models on Vietnamese Banking Operations & Regulatory Compliance with Retrieval-Augmented Generation
**Target venue:** **IEEE-RIVF 2026** (main track) — see §1
**Course deliverable:** Seminar 2
**Workflow paradigm:** QA-driven corpus ingestion, provenance-tagged automated evaluation
**Last re-baselined:** 2026-09-09 against the live repository and the trusted QA CSV

---

## 1. Venue: IEEE-RIVF 2026 (verified 2026-09-09)

| Item | Value |
|---|---|
| Conference | IEEE-RIVF 2026, 20th International Conference on Computing and Communication Technologies |
| **Paper deadline** | **2026-09-15 — stated as a HARD deadline on the official site** (moved Jul 31 → Aug 31 → Sep 15) |
| Notification / camera-ready | 2026-10-15 / 2026-11-11 |
| Conference | 2026-12-18 → 12-20, VinUniversity, Hanoi |
| Format | **≤6 pages**, English, PDF, IEEE A4 — `\documentclass[conference,a4paper]{IEEEtran}` + `\pdfminorversion=6` |
| Portal | EDAS `N35414` (https://edas.info/N35414) |
| Review | Single-blind (no anonymisation required) |
| Originality | Must not be under consideration elsewhere → **no dual submission** (this rules out also filing at SOICT 2026) |
| Presentation | ≥1 author must register **and present in person**; IEEE removes non-presented papers from Xplore |
| Indexing | IEEE Xplore + DBLP confirmed historically; **Scopus not guaranteed** by the official site |
| Registration | Local-VN student ≈$150 early (≤Nov 15) / $200 late, covers 1 paper — *verify on the registration page; two figures are cached locally* |
| Acceptance | ~93–100 papers/edition; RIVF 2023 = 196 submitted / 101 accepted (~52%) |

**Track choice.** Track 1 *AI Foundations and Big Data* lists "Responsible, trustworthy, and reliable AI (**methods and evaluation**)"; Track 2 *AI Applications* lists "AI for … **finance**". Either fits; Track 1 is the closer match.

**Why the fit is good.** The AI-Applications track chair (Zengchang Qin) published *"Mix-of-Granularity: Optimize the Chunking Granularity for Retrieval-Augmented Generation"* (COLING 2025) — clause-level Điều/Khoản segmentation *is* a chunking-granularity decision, so the retrieval-variant axis is chair-aligned as well as novel. The AI-Foundations chair is Than Quang Khoat (HUST SoICT), a two-time RIVF best-student-paper winner; a student-paper award category has precedent. "RAG" appears in **zero** RIVF titles 2022–2024, while LLM/language-model titles went 1 → 4 over 2023–2024. The venue rewards benchmarks/datasets, measurable deltas, regional relevance and an availability statement, and punishes theory without a metric — this project scores natively on the rewarded side.

**Fallback if Sep 15 is missed.** Special-session papers are due **2026-09-30** (notification Oct 30), but the three accepted sessions are SS1 *AI for Smart Cities*, SS2 *ML for 6G ISCC*, SS3 *6G Communications* — only SS1 is even a stretch fit and it would require reframing as e-government AI. SOICT 2026 is closed (abstract 09-09, paper 09-16). The realistic fallbacks are therefore SS1-with-reframe, RIVF 2027, or SOICT 2027.

---

## 2. Project Team & Responsibility Matrix

| Member | Student ID | Primary Role | Current assignment (week of 2026-09-09) |
|---|---|---|---|
| **Nguyễn Huy Hoàng** | 20251325M | Architecture & Experiment Lead | Corpus ingestion + text→RAG transformation, multiple RAG variants (chunking granularity), pipeline integration, unanswerable probe design |
| **Đinh Thị Lan Hương** | 20261261M | Domain QA & Legal Engineering | Finish QA + review (lands 09-10); **manually download** the paywalled/blocked source documents |
| **Vũ Đức Thành** | 20261082M | Domain QA & Benchmark Lead | Finish QA + review (lands 09-10); **manually download** source documents; question taxonomy; cross-annotation for κ |
| **Nguyễn Khắc Duy Ngọc** | 20261206M | Retrieval Pipeline | CSV→canonical-object loading; BM25 (`pyvi`) + BGE-M3 indexing; Recall@k; benchmark design with Phúc |
| **Nguyễn Thắng Phúc** | 20252263M | Core Framework & Persistence | Model loading for the open-model set; Colab/RunPod harness; benchmark design with Ngọc |

Unassigned as of 2026-09-09 and needing a name: the `metrics.py` scorer design, the 20 unanswerable probes, the LaTeX skeleton, and the EDAS entry.

---

## 3. Research Scope

### 3.1 Regulatory domain — derived from the QA CSV, not from a catalogue

The corpus is determined by what the questions actually cite. An earlier catalogue (`data/raw_legal/CATALOG.md`) listed 10 payment/card/security instruments; only **17/2024/TT-NHNN** overlaps the QA set. The catalogue is superseded by `data/raw_legal/INGEST_PLAN.json`, which is generated from the CSV.

**10 instruments carry every resolved question** (57 of 64 rows):

| Priority | Instrument | Questions | Source status (verified 2026-09-09) |
|---|---|---|---|
| 1 | 17/2024/TT-NHNN | 11 | reachable (congbao.chinhphu.vn) |
| 2 | 32/2024/QH15 — Luật Các tổ chức tín dụng 2024 | 10 | **luatvietnam likely PARTIAL** (`-d1.html` = page 1 of 209 articles) → prefer quochoi.vn |
| 3 | 39/2016/TT-NHNN | 10 | reachable; **amendment decision required** |
| 4 | 22/2023/TT-NHNN | 10 | **HTTP 404** → `datafiles.chinhphu.vn/cpp/files/vbpq/2024/01/22-nhnn.pdf`; **amended by 22/2025/TT-NHNN** |
| 5 | 21/2021/NĐ-CP | 10 | **HTTP 403** → `congbao.chinhphu.vn/van-ban/nghi-dinh-so-21-2021-nd-cp-33477/35291.htm` |
| 6 | 48/2018/TT-NHNN | 4 | reachable (PDF) |
| 7 | 61/2025/TT-NHNN | 3 | reachable (PDF) |
| 8 | 06/2019/TT-NHNN | 2 | reachable |
| 9 | 08/2023/TT-NHNN, 46/2024/QH15 | 1 each | reachable |
| 10 | 70/2014/NĐ-CP | 1 | reachable (PDF) |

**The top 5 carry 51 of 57 resolved questions (89%), and 3 of those 5 are the broken sources** — 30 questions depend on a 404, a 403, or a likely-truncated paywall. Those three are the download priority.

`23/2015/NĐ-CP` and `276/2017/NHNN-TTGSNH` are **not** primary for any question (23/2015 became a secondary source for Q007 after the gold-label fix; 276/2017 is 403-blocked with no replacement). They are optional distractors, not requirements.

7 questions (Q002, Q008, Q059, Q060, Q062, Q063, Q064) still map to `UNRESOLVED:manifest-pending` because 5 opaque URLs (`tt-32.pdf`, `91.signed.pdf`, `6pl.pdf`, `62-vbhn-vpqh.pdf`, `vanban docid=211190`) do not spell out their instrument number. Their id must be read off the downloaded document header and added to `data/raw_legal/DOC_MANIFEST.json`.

### 3.2 Research questions

- **RQ1 (Hallucination reduction):** How much does RAG reduce hallucination compared with closed-book answering for small LLMs (≤7B) on Vietnamese banking compliance questions?
- **RQ2 (Citation & abstention):** How accurately do models cite the supporting article/clause, and do they abstain on unanswerable or out-of-scope queries?
- **RQ3 (Sparse vs dense):** How does BM25 with Vietnamese compound-word segmentation compare with multilingual dense embeddings (`BGE-M3`) on legal retrieval?

**Measurement-validity caveat (must be resolved before results are reported).** `regrag/evaluation/metrics.py` currently derives `correctness_score` *entirely* from citation precision/recall — the answer text is never compared to the gold answer — and its `hallucinated` flag is True only when a citation was emitted, so a fabricated answer with no citation scores better than a wrong citation. Abstention detection is 3 hardcoded keyphrases. Every record is therefore tagged `metric_status="placeholder"`. The team's benchmark-design task must replace these with a defensible scorer (groundedness against the retrieved passage is the recommended basis) and validate it against ~50 human-labelled responses, reporting the agreement.

**Headline framing recommendation.** "RAG beats closed-book" is the expected result and reviewers will say so. The defensible headline available from this design is *citation-level unfaithfulness*: models produce fluent, plausible answers carrying the wrong Điều/Khoản, and cite instruments that do not cover the question instead of abstaining. That is a trustworthy-AI finding and matches Track 1's wording exactly.

### 3.3 Experimental matrix

Baseline: **3 models × 3 retrieval modes** (closed-book, RAG-BM25, RAG-Dense), top-k = 3.

Candidate models: `Qwen/Qwen2.5-7B-Instruct`, `Qwen/Qwen2.5-3B-Instruct`, and one architecturally different Vietnamese-capable model (`google/gemma-3-4b-it` or `Viet-Mistral/Vistral-7B-Chat`). `Llama-3.2-3B-Instruct` is English-centric; if included it must be labelled a weak-Vietnamese contrast, not a peer, or it confounds every cross-model number. All candidates must be confirmed loadable before commitment.

**On scaling to 5 models.** The compute is not the obstacle: 5 models × 5 modes × 84 questions ≈ 2,100 generations ≈ 8–14 T4-hours. Cutting models 5→3 and cutting modes 5→3 save *the same* GPU time (1,260 each), so the decision must be made on novelty and integration cost, not compute:

- Each extra **RAG variant** is a config parameter on an existing pipeline — cheap in human time, and it is the most novel axis (chunking granularity, chair-aligned, zero RIVF precedent).
- Each extra **model** is a new tokenizer, chat template, quantization footprint and failure mode — expensive in human time, and the dangerous failure is silent: a wrong chat template produces degenerate output that reads as "this model hallucinates" when the truth is "we prompted it wrong".

Recommendation: protect every RAG variant, keep 3 models, and do not cut the question count (it is the dataset contribution and adds no integration risk). If 5 models are kept, serve them through vLLM on a single GPU rather than 5 sequential Colab loads — that collapses 5 integrations into 1.

### 3.4 Benchmark composition

- **Answerable set: corpus-covered questions, reported honestly.** The CSV holds 64 (review completes 2026-09-10). Chasing a round 100 puts a people-dependency on the critical path. **The corpus determines the answerable set, not the other way round**: ingest what is reachable, keep the questions whose gold passage is verifiably present, and report the final N. A question whose instrument did not arrive must be *excluded*, never left in — otherwise it generates a false hallucination label.
- **20 unanswerable probes** (0 exist as of 2026-09-09). These need no corpus and no gold passage, so they are the cheapest high-value item in the plan and carry half of RQ2. Suggested design, ~5 each: out-of-scope domain (crypto, securities), repealed instrument (e.g. TT 19/2016 replaced by TT 18/2024), precision trap (a numeric threshold that differs from the real one), cross-jurisdictional (US/EU rules).
- **Inter-annotator reliability.** Full dual annotation on every question is not feasible in the window, and κ computed on self-annotation measures nothing (Thành and Hương authored the questions). Recommended: a **30-question genuinely cross-annotated subset** — Thành grades Hương's, Hương grades Thành's — report κ on that subset and disclose the remainder as single-annotator.

---

## 4. Data Architecture

### 4.1 Single trusted source

`data/gold/bank_qa_data.csv` is the **only** trusted artifact. Everything else is derived and regenerable. Do not hand-edit derived files.

Four measured properties of the CSV drive the schema:

| Property | Measured | Consequence |
|---|---|---|
| Passages naming an `Điều` | **64 / 64** | Article-level gold is always derivable → **score citation accuracy at Điều level** |
| Passages containing "Khoản N" | 24 / 64 | Clause-level gold is optional and must never be required for a match |
| Passages preserving line-initial clause numbering | **5 / 64** | Cell line structure is inconsistent → never rely on layout |
| Passages naming their own instrument | **2 / 64** | `doc_id` can never be regexed from prose; it comes from `doc_link` |

The old importer derived gold `doc_id` by regexing answer prose. That produced `doc_id="UNKNOWN"` for 83 citation entries and left 48 of 64 questions all-UNKNOWN, which made RQ2 unscorable. It is deprecated (`scripts/import_qa_csv.py` now refuses to run and points at its replacement).

### 4.2 Canonical schema

`regrag/corpus/qa_loader.py` is the only sanctioned reader of the CSV:

```
gold.doc_id     = DOC_MANIFEST.json  →  else URL slug regex  →  else "UNRESOLVED:<reason>"
gold.article_id = first "Điều N" in the verbatim passage      (64/64)
gold.clause_id  = "Khoản N" in the passage, else null          (24/64)
```

Unresolved rows are **kept and reported, never dropped** — silently shrinking the benchmark is the failure mode this design exists to prevent. `doc_link` cells are malformed (7 of 64 rows contain more than one URL separated by embedded newlines); `canonical.split_urls` recovers 19 real URLs where naive parsing sees 16.

When a row carries several URLs and the passage explicitly names one of them, that one becomes primary (`doc_id_confidence="passage-named"`). URL order is not evidence. This corrected **Q007** (two links; passage names TT 48/2018 but the first URL was NĐ 23/2015) and **Q064**.

### 4.3 Two-tier corpus

| Tier | Source | `corpus_source` | Publishable |
|---|---|---|---|
| **Tier 1** | the 64 verbatim CSV passages, one chunk each | `tier1_passages` | **Never** |
| **Tier 2** | segmented full instruments from `INGEST_PLAN.json` | `tier2_full` | Yes |

Tier 1 exists because the real corpus is not on disk yet. Its interfaces are identical to Tier 2, so schema → index → retrieve → prompt → generate → score → store can be integrated immediately and the real corpus dropped in later. Because each question's gold passage is in it by construction, Recall@3 is trivially ~1.0 and BM25 cannot be distinguished from dense: **it is a development fixture and must never appear in a paper table.** `provenance.assert_publishable` refuses it.

### 4.4 Coverage invariant

Every retained question's `gold_passage` must be found in the Tier 2 corpus, matched via `canonical.normalize_ws` (NFC + whitespace collapse, diacritics preserved) at the strict tier. A passage matching **only** under `fold_diacritics` means the ingested text lost diacritics — that is reported as a distinct diagnostic category, never silently accepted. This is the invariant the whole design rests on; `tests/test_coverage.py` encodes it.

Current state: **0/64 (0.0%)** against `corpus_chunks.json`, **64/64 (100%)** against Tier 1.

### 4.5 Quarantined seed text

`data/raw_legal/18_2024_TT_NHNN.txt` is **not an authentic legal text** and is quarantined in `INGEST_PLAN.json`. It is 3,611 chars / 43 lines containing only Điều 1, 2, 3, 9, 14, 15, 23 — real instruments number articles contiguously, so gaps of 3→9→14→23 cannot occur. Only Chương I–II appear yet Điều 23 is present. Every mandatory element of a Vietnamese circular is absent (no "Căn cứ…" recitals, no effective-date clause, no "Điều khoản thi hành", no signature block) and it ends mid-provision. It is cited by zero questions.

The 22 chunks previously in `corpus_chunks.json` all came from it and are invalid; that file is now empty pending real ingestion. Fabricated provisions are worse than no distractor: a model could retrieve a fake article and be scored against it. Note also that the segmenter was originally validated against this text, which is circular if the prose was generated to match the parser's own regexes — it has since been re-validated against the 64 real CSV passages.

---

## 5. Provenance Discipline

This is a methodological requirement, not housekeeping. Three silent-substitution paths were found in the codebase, each capable of producing a plausible-but-fictional result:

| Path | Before | After |
|---|---|---|
| `indexing/dense.py` | Returned the first `top_k` chunks in corpus order with fabricated scores 1.0 / 0.5 / 0.33 whenever `sentence_transformers` was absent — i.e. the entire RAG-Dense column and RQ3 | Raises `ProvenanceError` naming the missing dependency; stamps the real backend on every result |
| `indexing/bm25.py` | Silently degraded to term-overlap counting without `rank_bm25`, and to whitespace splitting without `pyvi` (destroying the compound-word handling RQ3 tests), still labelled "BM25" | Fallbacks retained but self-identifying: `bm25-rank_bm25+pyvi` vs `DEGRADED:<reason>`, plus a stderr warning |
| `evaluation/metrics.py` | Returned confident numbers from placeholder heuristics | Tags `metric_status="placeholder"` and lists `placeholder_fields` |

Every `LegalChunk`, `RetrievedResult`, `GenerationResult` and `EvaluationRecord` now carries `corpus_source` and/or `retriever_backend`. `provenance.assert_publishable()` raises rather than aggregate any row that is `UNSET`, `DEGRADED`, or Tier 1. **No number reaches a paper table without a clean provenance tag.**

Rule for all new code: a placeholder must fail loudly or self-identify. It must never return a plausible default.

---

## 6. Environment

Audited 2026-09-09 — **none of the retrieval or extraction stack is installed**:

| Purpose | Package | Status |
|---|---|---|
| Dense retrieval | `sentence-transformers` | **missing** → dense refuses to run |
| Sparse retrieval | `rank_bm25` | **missing** → BM25 runs DEGRADED |
| Vietnamese segmentation | `pyvi` | **missing** → BM25 runs DEGRADED |
| PDF extraction | `pypdf`, `pdfplumber` | **missing** → cannot ingest ~7 PDFs |
| HTML extraction | `beautifulsoup4`, `lxml` | **missing** → cannot ingest ~8 HTML pages |
| Present | `torch` 2.13.0+cu130, `pandas`, `numpy`, `requests` | ok |

Setup (uses `--system-site-packages` so the installed torch is reused rather than duplicated):

```bash
python3 -m venv --system-site-packages .venv
.venv/bin/pip install pyvi rank_bm25 pypdf pdfplumber beautifulsoup4 lxml sentence-transformers
```

Until this is done **no retrieval measurement is possible**, and tomorrow's ingestion cannot run. Heavy generation stays off this machine (Colab / RunPod).

Tests are stdlib `unittest`; `pytest` is not installed and `tests/` has no `__init__.py`, so discovery fails. Run by module name:

```bash
python3 -m unittest tests.test_storage tests.test_components tests.test_provenance \
                    tests.test_coverage tests.test_parser_passages
```

---

## 7. Phased Roadmap & Verified Status

| Phase | Description | Claimed | **Verified 2026-09-09** |
|---|---|---|---|
| 1 | Architecture scaffolding & dual storage | DONE | **Done.** 33 tests pass. `file_repo.py` no longer swallows write errors |
| 2 | QA-driven corpus & chunking | IN PROGRESS | **Blocked on downloads.** Loader, canonicaliser, manifest, ingest pipeline, parser hardening and Tier 1 fixture are done; **0 of 10 real instruments ingested**, coverage 0/64 |
| 3 | Gold QA benchmark | 64/100, EOD | **64 answerable** (Thành 50 / Hương 14), review lands 09-10. **0 of 20 unanswerable probes.** κ not started |
| 4 | Inference campaign | READY / QUEUED | **Not ready.** `notebooks/colab_runner.ipynb` = 5 cells, zero outputs, never executed. Generation deps absent |
| 5 | Automated evaluation | QUEUED | **Blocked.** Citation extraction fixed and tested; correctness/hallucination/abstention scorers are tagged placeholders pending design |
| 6 | IEEE report & packaging | QUEUED | **Not started.** No `.tex` in the repository |

### Gates

- **Gate A — pipeline integrity.** End-to-end run on Tier 1 with dense provably real. *Passed except for the missing dependencies.*
- **Gate B — coverage.** ≥80% of retained questions have their gold passage string-matching a Tier 2 chunk. Sets the final answerable N. *Blocked on downloads.*
- **Gate C — retrieval validity.** Recall@3 ≥ ~0.7 on Tier 2, **and BM25 vs dense must actually differ**. Below that, the RAG arm is not measuring retrieval and the schedule should pivot rather than continue. *Blocked on Gate B.*
- **Gate D — generation.** The harness runs the full model × mode grid without OOM or session loss, and checkpoint resume works. *Blocked on the harness being written.*

---

## 8. Schedule to 2026-09-15

| Date | Work | Gate |
|---|---|---|
| **Wed 09-09** | Data layer + provenance (done). Open the **EDAS N35414** entry with title and abstract. Install deps. Downloads begin; top-5 instruments first | A |
| **Thu 09-10** | Revised CSV lands → `scripts/regenerate.py`. Ingest + segment Tier 2. Write the 20 unanswerable probes. LaTeX skeleton + §I–§IV drafted against the design | **B** |
| **Fri 09-11** | BM25+`pyvi` and BGE-M3 indices on Tier 2; Recall@1/@3. Replace the placeholder scorers. Per-model prompt-format sanity probe (3 fixed questions, human-eyeballed) before any campaign | **C** |
| **Sat 09-12** | Inference campaign, checkpointed; every row carries a non-DEGRADED backend tag | D |
| **Sun 09-13** | Metrics, tables, figures. Human-label ~50 responses to validate the automatic scorer. κ on the 30-question cross-annotated subset | — |
| **Mon 09-14** | Write §V–§VI; compile clean (0 errors, 0 undefined refs, ≤6 pages, IEEE A4). Publish repo + Zenodo DOI and add the availability statement | — |
| **Tue 09-15** | Submit to EDAS **≥6 h early**; retain the confirmation receipt | — |

If Gate B or C fails on 09-11, decide that day between SS1 (09-30, needs a reframing stretch) and RIVF 2027 / SOICT 2027. Do not drift into 09-12 hoping.

---

## 9. Risk Register

| # | Risk | Impact | Mitigation / owner |
|---|---|---|---|
| R1 | 3 of the top 5 instruments are behind a 404, a 403, or a partial paywall (30 questions) | High | Replacement government URLs recorded in `INGEST_PLAN.json`; manual download by Thành & Hương |
| R2 | **Amendment trap.** 22/2023/TT-NHNN is amended by 22/2025/TT-NHNN; 39/2016/TT-NHNN has a long amendment history (20 questions) | High — produces *false hallucination labels*, the worst failure available | Record an original-vs-consolidated decision per instrument in `DOC_MANIFEST.json` before ingestion |
| R3 | No PDF/HTML extraction library installed | High | §6 setup; blocks all ingestion |
| R4 | `metrics.py` scorers are placeholders | High — RQ1/RQ2 headline numbers | Design decision + human-validated subset; records tagged until replaced |
| R5 | 7 questions map to unresolved instrument ids | Medium | Read ids off downloaded headers → `DOC_MANIFEST.json`; or exclude those questions |
| R6 | Colab harness never executed; 5 model integrations each with silent prompt-format failure modes | Medium-High | Gate D; per-model sanity probe; prefer vLLM to collapse integrations |
| R7 | CSV changes on 09-10 invalidates today's work | Medium | `scripts/regenerate.py` is idempotent and cache keys bind per-question, so a revision touching 6 questions does not invalidate the whole campaign |
| R8 | Nobody owns the paper; ~3 of 6 pages need no results | Medium | Assign §I–§IV now; only §V–§VI compete with the campaign |
| R9 | Page limit: 3 RQs × 9 conditions × κ × 3 metrics will not fit 6 pages | Medium | Budget 3 tables and 1 figure |
| R10 | Dual submission is forbidden | Low | Do not also file at SOICT 2026 or any journal |

---

## 10. Commands

```bash
# canonical load from the trusted CSV (+ coverage report)
python3 scripts/load_qa_csv.py --report

# Tier 1 development fixture (never publishable)
python3 scripts/build_tier1_corpus.py

# real ingestion, manifest-driven, fails loud on gaps
python3 scripts/build_corpus_chunks.py [--allow-missing] [--dry-run]

# regenerate every CSV-derived artifact; idempotent
python3 scripts/regenerate.py

# tests
python3 -m unittest tests.test_storage tests.test_components tests.test_provenance \
                    tests.test_coverage tests.test_parser_passages
```
