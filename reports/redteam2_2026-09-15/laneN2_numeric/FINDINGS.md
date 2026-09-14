# laneN2 — ROUND 2 numeric-consistency re-audit of paper/main.tex (2026-09-15)

Auditor: laneN2 (mechanical numeric re-audit, fresh from scratch post-fix-cycle).
Target: `/mnt/data/seminar_2/paper/main.tex` (278 lines, read IN FULL; lines 124–142 re-read after display truncation).
Ground truth (read in full): `data/eval/tables_paper_2026-09-13.json`, `data/eval/scorer_validation_2026-09-15.json`, `data/eval/bm25_recall_gate_c_2026-09-11.json`, `data/eval/dense_recall_gate_c_2026-09-13.json`; `data/eval/generations.json` spot-checked programmatically (792 rows) plus two read-only cross-checks: scorer re-run (`regrag.evaluation.metrics.detect_abstention`) and `scripts/run_campaign_pod.py`.

## Verdict summary

| Verdict | Count (distinct numeric claims/cells) |
|---|---|
| VERIFIED | 96 (incl. all 27 Table I cells, 16 Table II cells, 8 Table III cells) |
| MISMATCH | **1** — "115 of the 192" (denominator error) |
| UNVERIFIABLE (absent from all five JSONs) | 6 (see §6) |

Rounding direction: consistent throughout — every paper value is the round-half-up of the unrounded JSON/raw value to the printed precision. Only true tie: 0.3125 → "0.313" (main.tex:165), half-up, correct. No truncation-vs-rounding contradictions found.

---

## 1. THE MISMATCH

**[MISMATCH] main.tex:254 (§RQ2) — "115 of the 192 closed-book answerable rows" misstates the denominator. 115 is the count over ALL 264 closed-book rows; the answerable-only count is 80.**

- main.tex:254: `Another 115 of the 192 closed-book answerable rows state the sentinel yet answer anyway;`
- JSON backing for the number 115 itself (verbatim): tables_paper_2026-09-13.json, pooled `closed_book` block: `"rows": 264,` … `"hedged_then_answered": 115,`
- Denominator proof (three independent lines):
  1. `scripts/compute_tables.py:160`: `hedged = sum(1 for r in records if "HEDGED_THEN_ANSWERED=1" in (r.notes or ""))` — `records` is the whole block (n=264), no answerable filter.
  2. Scorer re-run over `data/eval/generations.json` closed-book rows with the project's own `detect_abstention`: `closed_book rows: 264 | hedged ALL: 115 | hedged answerable: 80 | hedged probes: 35` (80+35=115).
  3. `regrag/evaluation/metrics.py:681`: `hedged = bool((exact_names or soft_names) and n_assert > 0)` — probe hedge-then-answer rows qualify too.
- Correct statements would be: "Another 80 of the 192 closed-book answerable rows …" or "115 of the 264 closed-book rows …". Note the neighboring claim "71 of 72 probe rows receive substantive answers" (same line region) is correct and consistent: 35 hedging probes + 36 plain-answer probes = 71 non-abstaining probe rows.
- Cross-check of the internal arithmetic that survives: 80 + 35 = 115; 192 = 64×3; 72 = 24×3.

---

## 2. Fix-cycle additions — word-by-word vs JSONs (Task 4)

| main.tex (line) | Paper text | Ground truth | Verdict |
|---|---|---|---|
| 127 | "misses 15 expert-correct answers" | scorer_validation: `"correct": {… "confusion": {"tp": 3, "fn": 15, …}` | VERIFIED |
| 127 | "8 expert-judged abstentions" | scorer_validation: `"abstained": {… "fn": 8,` | VERIFIED |
| 127 | "(3/3 and 10/10)" | correct tp=3/fp=0; abstained tp=10/fp=0 ("auto_positive": 3 / 10, all true positives) | VERIFIED |
| 127 | "$\kappa = 0.20$ … $0.39$ … $0.62$" | `"cohens_kappa": 0.20382165605095534` → 0.20; `0.38625204582651385` → 0.39; `0.6153846153846153` → 0.62 | VERIFIED |
| 127 | "misses ten and over-flags five, netting the undercount of five" | hallucinated: `"fn": 10, "fp": 5`; 10−5=5; also `"human_positive": 32` − `"auto_positive": 27` = 5 | VERIFIED |
| 254 | "102 of 192 closed-book answerable rows (64 $\times$ 3 models) asserting a provision that does not govern" | tables: closed_book `"NON_COVERING_PROVISION": 102`; `"answerable": 192`; 64×3=192 | VERIFIED |
| 254 | "76 citing an instrument other than the governing one" | tables: closed_book `"WRONG_INSTRUMENT": 76` | VERIFIED |
| 254 | "49\% (BM25) and 43\% (dense) of answerable rows" | 94/192=48.96%→49% (`"citation_unfaithfulness_rows": 94` rag_bm25); 83/192=43.23%→43% (`"citation_unfaithfulness_rows": 83` rag_dense) | VERIFIED |
| 254 | "71 of 72 probe rows receive substantive answers" | tables closed_book: `"probe_answered": 71`, `"probes": 72`; scorer re-run: probe_abstained closed = 1 (qwen-7b) | VERIFIED |
| 254 | "Another 115 of the 192 …" | see §1 | **MISMATCH** |
| 147 | "identical answers in only 45 of 264 shared instances" | tables: `"tier1_rag_arm_identical_answers": {"identical": 45, "of": 264}` | VERIFIED |
| 148 | "full Tier-2 corpus of 3,703 chunks … across the 22 legal instruments" | bm25 json: `"corpus_chunk_count": 3703, "instrument_count": 22` (dense json same) | VERIFIED |
| 259 | "clearing our 0.7 document-recall floor" | no JSON field; recalls 0.734/0.719 do clear 0.7 | UNVERIFIABLE (policy constant) |
| 138 | "one ten-hour window" | tables: `"generated_at": ["2026-09-12T18:55:44+00:00", "2026-09-13T05:05:14+00:00"]` = 10 h 09 m 30 s | VERIFIED (approx; 10 h 10 m rounded down to "ten-hour") |
| 262–263 (comment) | "Vistral RAG rows 164--175 s vs.\ Qwen 4.9--10.2 s per campaign_provenance" | tables latency: `"vistral-7b::rag_bm25": 164.072, "vistral-7b::rag_dense": 175.4115` → 164–175; `"qwen-7b::rag_bm25": 4.9253` min, `"qwen-3b::closed_book": 10.2109` max → 4.9–10.2 | VERIFIED (LaTeX comment) |

---

## 3. Arithmetic re-derivations (Task 2) — all check out

- 3×3×88 = 792 = `"prompt_exact_true": 792` = 709 stop + 83 length (`"finish_reasons": {"stop": 709, "length": 83}`). main.tex:138, 238.
- Pooled F1 = 2PR/(P+R): BM25 2(0.2932×0.3545)/(0.2932+0.3545) = 0.3209 → 0.321 (main.tex:190,254). Dense 2(0.3989×0.4762)/(0.3989+0.4762) = 0.4341 → 0.434 (main.tex:191,254). Matches JSON `"citation_f1": 0.3209 / 0.4341`.
- 94/192 = 48.96% → "49%"; 83/192 = 43.23% → "43%" (main.tex:53, 254, 267).
- 189 = 63×3 (`"citation_scorable_rows": 189`; article n_scored 63 in both recall JSONs, `excluded_ids: ["Q036"]`); 120 = 40×3 (`"clause_gold_rows": 120`, `"clause_gold": 40`) — main.tex:186–188 caption.
- 63 + 1 annex = 64: article n_scored 63 + Q036; direct evidence Q036 is the annex row: dense_recall json Q036 entry has `"gold_article_id": null`.
- 64 + 24 = 88 (`"answerable": 64, "probes": 24`, `"questions": 88`).
- 71/72: `"probe_answered": 71` of `"probes": 72` (closed_book pooled).
- 115/192: number 115 exists (`"hedged_then_answered": 115`) but is over 264 rows — see §1.
- 25.0%/23.4% (main.tex:251): source is qwen-7b per-model cells — `"false_abstentions": 16` → 16/64 = 0.25 → 25.0% (rag_bm25); `"false_abstentions": 15` → 15/64 = 0.2344 → 23.4% (rag_dense); matches `"false_abstention_rate": 0.25 / 0.2344`; closed-book 0 (`"false_abstentions": 0`). (The pooled false-abstention fields 28/19/1 are different quantities, not quoted in the paper.)
- Binomial noise "six and ten percentage points" (main.tex:138): sqrt(0.25/64) = 0.0625 → 6.25 pp ≈ six; sqrt(0.25/24) = 0.10206 → 10.2 pp ≈ ten. VERIFIED (p=0.25 worst case).
- "a 3.2-point gap" (main.tex:259): 52.4% − 49.2% = 3.2 pp (33/63 − 31/63).
- Conclusion bounds (main.tex:267): "reaches 90%" ≤ 90.625% ✓; "drops below 53%" — max 52.381% < 53 ✓; "at or below 0.32" — max clause 0.3167 ✓.

---

## 4. Full numeric inventory (Task 1) — VERIFIED items with JSON anchors

### Abstract (main.tex:53)
- "64 answerable questions", "24 unanswerable probes" — tables `"answerable": 64, "probes": 24`. VERIFIED.
- "$3\times3\times88$ generation campaign" — 88 questions × 3 models × 3 modes; `"questions": 88`; models/modes lists of 3. VERIFIED.
- "at most 7B parameters" — `"hf_model_ids": ["Qwen/Qwen2.5-3B-Instruct", "Qwen/Qwen2.5-7B-Instruct", "Viet-Mistral/Vistral-7B-Chat"]`. VERIFIED.
- "from 0.005 (closed-book) to 0.32--0.43" — `"citation_f1": 0.0053` → 0.005; 0.3209 → 0.32; 0.4341 → 0.43. VERIFIED.
- "43--49\% of RAG answers" — 83/192 → 43%, 94/192 → 49%. VERIFIED.

### Introduction
- "3--7B parameter model" (main.tex:63), "64 answerable statutory questions and 24 unanswerable operational probes" (main.tex:77). VERIFIED (as above).

### Benchmark (main.tex:99–113)
- "88 rows: 64 answerable … 24 unanswerable probes" (99). VERIFIED.
- "Article-level gold citations … derivable for 63 of the 64 answerable rows; clause-level gold … present for 40" (100) — bm25 json `"n_scored": 63` + `excluded_ids ["Q036"]`; `"clause_gold": 40`. VERIFIED.
- "63 of the 64 passages consist of verbatim article text substituted" (99) — no literal `substitutions` field in the five JSONs; arithmetically forced by 64 − 1 annex and consistent with Q036 `"gold_article_id": null` + n_scored 63. VERIFIED-by-arithmetic (count itself not a JSON field).
- "two domain annotators" (113) — UNVERIFIABLE (see §6).

### Method (main.tex:118–136)
- "top-$k=3$" (118) — recall JSONs report hits@1/hits@3. VERIFIED.
- "4-bit quantisation (NF4 weights, float16 compute)" (122) — tables `"quant_config": ["bnb-4bit-nf4+float16"]`. VERIFIED.
- "single 24\,GB GPU" (122) — `"gpu_names": ["NVIDIA GeForce RTX 3090"]` names the GPU; VRAM not in JSONs. UNVERIFIABLE-in-JSONs (hardware spec).
- "50 expert-annotated responses stratified across models and modes" (127) — `"n_rows": 50`; composition models {16,17,17}, modes {16,17,17}. VERIFIED.
- κ/misses — see §2. VERIFIED.

### Results intro (main.tex:138)
- "all 88 benchmark rows, producing 792 generated answers"; "all 792 prompts round-trip byte-identical" (`"prompt_exact_true": 792`); "709 answers finish naturally and 83 hit the token cap" (`"finish_reasons": {"stop": 709, "length": 83}`). VERIFIED.
- "RTX 3090" — VERIFIED. "(24\,GB)" — UNVERIFIABLE-in-JSONs.
- "temperature 0, seed 1234, at most 512 new tokens" — absent from all five JSONs (generations.json rows carry no such fields); corroborated outside JSONs by `scripts/run_campaign_pod.py`: `SAMPLING = SamplingConfig(max_new_tokens=512, temperature=0.0, do_sample=False, seed=1234)`. UNVERIFIABLE-in-JSONs (repo-corroborated).
- "With 64 answerable rows and 24 probes per cell"; "six and ten percentage points". VERIFIED (§3).

### Disclosure (main.tex:147–148)
- "45 of 264"; "3,703 chunks"; "22 legal instruments". VERIFIED (§2).

### Table I (main.tex:157–171) — all 27 cells vs `table1_by_model_mode`
0.438/–/0.042 (7b cb: 0.4375, 0.0417); 0.344/0.985/0.500 (0.3438, 0.9848, 0.5); 0.313/0.951/0.375 (0.3125, 0.9511, 0.375); 0.750/–/0.000 (0.75, 0.0); 0.469/0.950/0.000 (0.4688, 0.9499, 0.0); 0.422/0.916/0.125 (0.4219, 0.9158, 0.125); 0.625/–/0.000 (0.625, 0.0); 0.672/0.912/0.000 (0.6719, 0.9116, 0.0); 0.594/0.939/0.000 (0.5938, 0.9393, 0.0). Caption "64 answerable questions", "24 probes". All VERIFIED. Bonus: Abst column independently re-derived from raw generations.json via the project scorer — abstained probe counts qwen-7b {cb:1, bm25:12, dense:9}, qwen-3b {dense:3}, vistral {0,0,0} — exact match to 1/24, 12/24, 9/24, 3/24, 0.

### Table II (main.tex:186–191) — all 16 cells vs `table2_by_mode_pooled`
closed-book 0.005/0.005/0.005/0.008 (0.0053, 0.0083); RAG-BM25 0.293/0.354/0.321/0.300 (0.2932, 0.3545[=67/189=0.354497], 0.3209, 0.3); RAG-Dense 0.399/0.476/0.434/0.317 (0.3989, 0.4762, 0.4341, 0.3167). Caption 189=63×3, Q036 annex, 120=40×3. All VERIFIED (0.354 is correct half-up of 0.354497; the JSON's 0.3545 is its own 4-dp display).

### Table III (main.tex:216–218) — all 8 cells vs recall JSONs
BM25 0.734/0.906/0.381/0.492 (`"recall@1": 0.734375` [47/64], `"recall@3": 0.90625` [58/64], `"recall@1": 0.380952…` [24/63], `"recall@3": 0.492063…` [31/63]); Dense 0.719/0.891/0.365/0.524 (46/64, 57/64, 23/63, 33/63: 0.71875, 0.890625, 0.365079, 0.523809). Caption doc n=64, article n=63, annex row. All VERIFIED. Hit counts 47/58/24/31 and 46/57/23/33 present in JSONs exactly.

### RQ1 (main.tex:251)
- "0.44--0.75" span (closed-book 0.4375/0.625/0.75); "0.438→0.344/0.313"; "0.750→0.469/0.422"; "0.672 vs 0.625"; "0.91--0.98" (groundedness min 0.9116, max 0.9848); "25.0\% and 23.4\% … against 0\%". All VERIFIED.

### RQ2 (main.tex:254–256)
- "F1 $= 0.005$"; "102 of 192"; "76 citing … (categories overlap)"; "0.321 (BM25) and 0.434 (dense)"; "49\% … 43\%"; "never exceeds 0.317"; "71 of 72"; "Vistral-7B refuses no probe in any mode" (probe_abstained 0/0/0; scorer re-run confirms). All VERIFIED except "115 of the 192" (§1).
- Q006 example: tables narrative_examples Q006 gold `{doc 46/2024/QH15, article 52, clause 4}`; extracted `91/2015/QH13 / 405`; answer contains "Điều 405 Bộ Luật Dân sự năm 2015". VERIFIED.
- Q008 example: answer begins `THÔNG TIN KHÔNG CÓ TRONG TÀI LIỆU.` (= registered `ABSTENTION_KEYPHRASE`, `regrag/generation/prompts.py:20`) then cites `02/2021/NĐ-CP` Điều 14, 15 — both in JSON answer_text. VERIFIED. (Gold reference_answer for all 24 probes is `Không có trong kho văn bản` — 24/24 in questions_canonical.json — so §III-C's gold-target string is also correct; scorer exact tier accepts both strings.)
- Q059 example: generations.json qwen-7b/rag_bm25 row: "Theo quy định tại Điều 3, Khoản 5 của Thông tư [61/2025/TT-NHNN]" — attribution of Article 3 to Circular 61/2025/TT-NHNN VERIFIED in raw log.

### RQ3 (main.tex:259)
- "90.6\% … at $k{=}3$ (73.4\% at $k{=}1$)" (58/64, 47/64); "49.2\% (38.1\% at $k{=}1$)" (31/63, 24/63); "(89.1\% doc-level at $k{=}3$)" (57/64); "(52.4\% against 49.2\%), a 3.2-point gap" (33/63). All VERIFIED. "about half of questions" — consistent.

### Conclusion (main.tex:267)
- "43--49\%", "at or below 0.32", "3,703-chunk", "reaches 90\%", "below 53\%". All VERIFIED.

### Comments with values
- main.tex:6 "md5 5b2e4fa15b0f7eabb840ebf67df4c0f7" — `md5sum paper/IEEEtran.cls` = `5b2e4fa15b0f7eabb840ebf67df4c0f7`. VERIFIED (on-disk, outside JSONs).
- main.tex:203–206 "30-question dual grading … kappa column removed 2026-09-14" — never-filled scaffold; UNVERIFIABLE (comment-only metadata; deliberately disclosed as un-performed, so no results claim).
- main.tex:262–263 latency 164–175 / 4.9–10.2 s. VERIFIED (§2).

---

## 5. Cross-place consistency map (Task 3)

Every multi-place value carries the same value everywhere:

| Value | Places | Consistent? |
|---|---|---|
| 64 / 24 | :53, :77, :99, :138, :157 (captions), :251, :254 | yes |
| 88, 3×3×88 | :53, :99, :138, :238 (figure) | yes |
| 792, 709, 83 | :138, :263 (comment "the 83 token-capped answers") | yes |
| 0.005 | :53 (abstract), :189 (Table II), :254 (RQ2) | yes |
| 0.32–0.43 vs 0.321/0.434 | :53 vs :190–191/:254 | yes (rounding of same) |
| 43–49% | :53, :254 (49/43), :267 | yes |
| 3,703; 22 | :148, :267 (chunks; instruments once) | yes |
| 189 / 63 / 120 / 40 | :100 (63, 40), :186–188 (caption 189, 63, 120, 40), JSON | yes |
| k=3 | :118, :138, :216 (caption k=1/3), :237 | yes |
| 4-bit NF4 | :122, :138, :238 | yes |
| 24 GB | :122, :138 | yes (both UNVERIFIABLE-in-JSONs) |
| ≤7B / 3–7B | :53, :63, :122 | yes |
| 0.734/0.906/0.381/0.492 vs 73.4/90.6/38.1/49.2% | Table III :217 vs RQ3 :259 | yes |
| 0.719/0.891/0.365/0.524 vs 71.9(unquoted)/89.1/36.5(unquoted)/52.4% | :218 vs :259 | yes |
| "90%" / "below 53%" bounds vs table maxima | :267 vs :217–218 | yes (90.625 ≥ 90; 52.381 < 53) |
| ≤0.32 vs 0.317 | :267 vs :191/:254 | yes |
| 45 of 264 | :147 only | n/a |
| 115 | :254 only — wrong denominator (§1) | **MISMATCH** |

Also checked, no contradiction: "agreement": 0.70 and composition 41/9 (scorer json) are not quoted in the paper; pooled false-abstentions 28/19/1 not quoted.

---

## 6. Numbers appearing ONLY in prose with no JSON backing (Task 5)

1. "single 24\,GB GPU" (main.tex:122) and "RTX 3090 (24\,GB)" (main.tex:138) — GPU name is in JSON; the 24 GB figure is not (true hardware spec of a 3090).
2. "temperature 0, seed 1234, at most 512 new tokens" (main.tex:138) — absent from all five JSONs; corroborated by `scripts/run_campaign_pod.py` `SamplingConfig(max_new_tokens=512, temperature=0.0, do_sample=False, seed=1234)` (repo code, not a JSON log).
3. "our 0.7 document-recall floor" (main.tex:259) — policy constant, no JSON field.
4. "authored by two domain annotators" (main.tex:113) — no JSON.
5. "an owner under 18" (probe example, §III-C ~main.tex:109) — illustrative scenario, no JSON.
6. "% … the 30-question dual grading" (main.tex:203, comment) — no JSON (scaffold never filled; paper discloses exactly that).
7. "63 of the 64 passages … substituted" (main.tex:99) — no literal substitution-count field in the five JSONs; value is arithmetically forced (64 − 1 annex) and consistent with Q036 `gold_article_id: null` + n_scored 63 (counted VERIFIED-by-arithmetic above; flagged here for completeness).

Email addresses, doc IDs (e.g. 46/2024/QH15, 61/2025/TT-NHNN, 91/2015/QH13, 02/2021/NĐ-CP) and citation years are identifiers, not results numbers; the example IDs were nonetheless checked against generations.json/tables narrative_examples and match.

---

## 7. Non-blocking observations (no paper change required)

- generations.json rows carry no `finish_reason`/`seed`/`temperature` fields; the 709/83 split is backed by tables_paper `campaign_provenance.finish_reasons`, not by generations.json itself.
- The raw `abstained` boolean in generations.json is a sentinel-presence flag, NOT the scorer verdict (e.g. qwen-7b/bm25: flag on 24/24 probes vs 12 credited). Table I uses the scorer verdict and is correct; noted to prevent future confusion.
- main.tex:206 comment says "\S III-B (annotation subsection)"; the annotation subsection is the 4th subsection of Section III (III-D). Stale comment pointer only.
- "one ten-hour window" is a round-down of 10 h 09 m 30 s (generated_at pair); defensible as written.
- "ten-hour window", "0.7 floor", "under 18", "two annotators" are the only numeric-ish prose tokens without JSON anchors (§6).

## Artifacts in this directory
- `PROGRESS.md` — audit progress log.
- `spotcheck_generations.py` — read-only generations.json spot-check script (row totals, sentinel/hedge variants, example rows).
