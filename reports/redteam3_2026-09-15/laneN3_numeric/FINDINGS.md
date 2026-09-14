# Lane N3 — Numeric-Consistency Audit, Round 4 (2026-09-15)

Scope: every round-3 number added by commit 86473c4, re-derived from ground truth
(scripts re-run with `/mnt/data/seminar_2/.venv/bin/python`, plus independent
recomputations in `spotcheck_n3.py` / `spotcheck_n3b.py`, stdout archived beside
this file). Paper read in full (main.tex, 277 lines).

---

## VERDICT SUMMARY

| Verdict | Count |
|---|---|
| **MISMATCH** | **3** (one root cause: the conditioned-split script ignores `rag_context_dropped_ranks`) |
| VERIFIED | 47 |
| VERIFIED w/ observation (number correct, wording/definition caveat) | 5 |
| UNVERIFIABLE | 0 |

**The one MISMATCH (root cause):** `scripts/compute_conditioned_rates.py` (and
`scripts/verify_tier1_conditioning.py`) classify a RAG row as INTACT whenever the
gold chunk id is in `retrieved_chunk_ids` and its rank is not in
`rag_context_truncated_ranks`. **Neither script ever reads
`rag_context_dropped_ranks`.** In the campaign, 9/192 BM25 rows and 6/192 dense
rows retrieved the gold chunk at rank 3 and then **dropped it from the prompt
entirely** (budget exhausted; `dropped_ranks=[3]`). Text-level audit of the actual
prompts: 6 of these 15 rows contain **zero** gold text (Q008/BM25, Q039/dense);
the other 9 contain only a **clipped prefix** via truncated sibling chunks
(Q034, Q060). The paper's own split criterion — "Splitting on whether the gold
chunk **actually reached the prompt**" (main.tex:253) — is therefore violated for
those 15 rows, and the quoted intact fractions are wrong:

| Paper (main.tex:253) | Script output | Correct under the paper's stated criterion |
|---|---|---|
| "near 35% ... when it arrives intact **(23/66 BM25**, **31/90 dense)**" | 23/66 = 34.8%; 31/90 = 34.4% | **BM25 19/57 = 33.3%; dense 29/84 = 34.5%** (9 resp. 6 dropped-gold rows move out of the denominator; 4 resp. 2 of the numerator rows were dropped-gold) |
| "sits between at **33–42%** when the context budget clips it" | 14/33 = 42.4%; 17/51 = 33.3% | **33–43%** (clipped bucket becomes 18/42 = 42.9% BM25; 19/57 = 33.3% dense — the BM25 endpoint rounds to 43, not 42) |
| "rises to **61–69%** when it is absent" | 57/93 = 61.3%; 35/51 = 68.6% | unchanged: 57/93 = 61.3%; 35/51 = 68.6% ✓ |

Everything else in the paper checks out. Knock-ons of the same root cause, not
separate errors: abstract "about 35% even when the governing passage reaches the
prompt intact" (main.tex:53) and conclusion "a rate near 35%" (main.tex:266) —
pooled corrected intact rate is 48/141 = 34.0% (vs 54/156 = 34.6% script-level);
the qualitative claim survives, the phrasing is marginally generous.

Minimal fixes (either one resolves it):
1. Re-run the conditioned split honouring `dropped_ranks` (treat a dropped gold
   rank as NOT reaching the prompt; bucket with "clipped" if a sibling carried a
   prefix, else with "absent") and reprint 19/57, 29/84, 33–43%; or
2. Reword main.tex:253 to the chunk-id semantics the scripts implement, e.g.
   "Splitting on whether the gold chunk was retrieved into the top-3 untruncated
   ...", which makes 23/66, 31/90, 33–42% correct as printed.

---

## 1. MISMATCH — full evidence

### N3-M1 — Conditioned-split INTACT bucket includes 15 rows whose gold chunk never reached the prompt

- Paper (verbatim, main.tex:253): `Splitting on whether the gold chunk actually reached the prompt, the rate stays near 35\% in both arms when it arrives intact (23/66 BM25, 31/90 dense), sits between at 33--42\% when the context budget clips it, and rises to 61--69\% when it is absent`
- Script (re-run stdout, `compute_conditioned_rates_stdout.txt`): `INTACT   :  23/ 66 unfaithful (34.8%)` / `INTACT   :  31/ 90 unfaithful (34.4%)`
- Script bug (verbatim, scripts/compute_conditioned_rates.py:65-71): `tr = r.get("rag_context_truncated_ranks") or []` … `if gold not in ret:` → `c = "ABSENT"` / `elif (ret.index(gold) + 1) in tr:` → `c = "TRUNCATED"` / `else: c = "INTACT"` — `tr` is only `rag_context_truncated_ranks`; `rag_context_dropped_ranks` is never read (grep confirms: no occurrence of `dropped` in either round-3 script).
- Ground truth (my recompute, `spotcheck_n3_stdout.txt`): `rag_bm25 {'INTACT': 57, 'ABSENT': 93, 'GOLD_DROPPED': 9, 'TRUNCATED': 33}` / `rag_dense {'INTACT': 84, 'TRUNCATED': 51, 'ABSENT': 51, 'GOLD_DROPPED': 6}`.
- Prompt-text audit (`spotcheck_n3b_stdout.txt`): cross-tab chunk-condition × text-level: `GOLD_DROPPED {'NOTEXT': 6, 'PREFIX': 9}`; every chunk-INTACT row (141/141) does contain the full gold passage, so the rest of the INTACT bucket is sound. Dropped-gold questions: Q008 (BM25), Q034 (both arms), Q060 (BM25), Q039 (dense).
- Corrected arithmetic (rescored per row with the project scorer, `spotcheck_n3b_stdout.txt`): BM25 intact 19/57 (33.3%), clipped 18/42 (42.9%), absent 57/93 (61.3%); dense intact 29/84 (34.5%), clipped 19/57 (33.3%), absent 35/51 (68.6%).

Not affected by this bug: the Q006 example (its gold chunk is rank 1, untruncated,
undropped — full passage verified byte-present in the prompt), §III-B's 33/64 and
47/64 (literal "reaches the top 3 [retrieval]" is true: 30/45 packed + 3/2
retrieved-then-dropped), and the 61–69% absent range.

---

## 2. Per-number verdicts (round-3 additions)

| # | Paper claim (verbatim, location) | Ground truth | Arithmetic | Verdict |
|---|---|---|---|---|
| 1a | "gold chunk reaches the top 3 for only 33 of 64 answerable questions under BM25 and 47 of 64 under dense retrieval" (§III-B, main.tex:103) | re-run `rag_bm25: gold chunk in top-3 for 33/64 answerable questions`; `rag_dense: ... 47/64`; independent recount 30/45 "packed" + 3/2 "retrieved at rank 3 but dropped" = 33/47 | 64−33=31 absent-questions BM25 (93/3 rows); 64−47=17 dense (51/3) | **VERIFIED** as literally worded ("reaches the top 3" = retrieved); observation: for 3 BM25 + 2 dense questions the chunk was retrieved at rank 3 and then dropped from the prompt |
| 1b | (task item) absent from top-3: 93/192 BM25, 51/192 dense | re-run: `rag_bm25: absent=93 ... total=192`; `rag_dense: absent=51` | 93/192 = 48.4375% → 48.4 ✓; 51/192 = 26.5625% → 26.6 ✓ | **VERIFIED** (script outputs; neither figure printed in the paper) |
| 2a | "arrives intact (23/66 BM25, 31/90 dense)" (main.tex:253) | see §1 | 23/66 = 34.8%; correct 19/57 = 33.3%; 31/90 = 34.4%; correct 29/84 = 34.5% | **MISMATCH** (N3-M1) |
| 2b | "33--42\% when the context budget clips it" (main.tex:253) | script 14/33 = 42.4%, 17/51 = 33.3% | corrected 18/42 = 42.9% → 43 | **MISMATCH** (endpoint; same root cause) |
| 2c | "rises to 61--69\% when it is absent" (main.tex:253) | 57/93 = 61.29 → 61; 35/51 = 68.63 → 69 | same under corrected buckets | **VERIFIED** |
| 2d | Sanity gate 94/192, 83/192 | re-run `rag_bm25: overall_unfaithful=94/192 (gate: expect 94/83)`; tables_paper JSON `citation_unfaithfulness_rows` = 94 (bm25), 83 (dense); my recount H: UNF 94 / 83 | 94/192 = 48.96% → 49%; 83/192 = 43.23% → 43% | **VERIFIED** |
| 2e | "near 35\%" (RQ2), "about 35\%" (abstract, main.tex:53), "near 35\%" (conclusion, main.tex:266) | script 34.8/34.4; corrected 33.3/34.5, pooled 34.0 | — | **VERIFIED w/ observation** — survives as approximation; slightly generous under corrected buckets (34.0% pooled) |
| 3a | "answered-row rates are $0.438\to0.458/0.408$ for Qwen2.5-7B" (main.tex:250) | re-run: `qwen-7b closed_book ... answered-only=28/64`; `rag_bm25 ... 22/48 (45.8%)`; `rag_dense ... 20/49 (40.8%)` | 28/64 = 0.4375 → 0.438; 22/48 = 0.45833 → 0.458; 20/49 = 0.40816 → 0.408 | **VERIFIED** |
| 3b | "Qwen2.5-3B keeps a genuine reduction ($0.762\to0.556/0.450$)" (main.tex:250) | re-run: `qwen-3b closed_book answered-only=48/63 (76.2%)`; `rag_bm25 30/54 (55.6%)`; `rag_dense 27/60 (45.0%)` | 48/63 = 0.76190 → 0.762; 30/54 = 0.55556 → 0.556; 27/60 = 0.450 | **VERIFIED** |
| 3c | Vistral answered-row 0.694/0.594 (task item) | re-run: `vistral-7b rag_bm25 answered-only=43/62 (69.4%)`; `rag_dense 38/64 (59.4%)` | — | **VERIFIED** (0.694 appears nowhere in the paper; Table I's 0.594 is the all-row dense rate 38/64 = 0.59375, a different, also-correct quantity) |
| 3d | "Vistral ... (0.672 vs.\ 0.625)" (main.tex:250); Table I 0.672/0.625 | tables_paper: 0.6719, 0.625; re-run 43/64, 40/64 | 43/64 = 0.671875 → 0.672 | **VERIFIED** |
| 3e | "Qwen2.5-7B falsely refuses 25.0\% and 23.4\% ... against 0\% closed-book" (main.tex:250) | tables_paper false_abstentions 16 / 15 / 0; re-run refused=16/15/0 | 16/64 = 25.0%; 15/64 = 23.4375 → 23.4% (half-up) | **VERIFIED** |
| 3f | "Qwen2.5-3B falsely refuses 15.6\% and 6.3\%" (main.tex:250) | tables_paper 10 (0.1562) / 4 (0.0625) | 10/64 = 15.625 → 15.6%; 4/64 = 6.25 → 6.3% (half-up) | **VERIFIED** |
| 4a | "shared 7{,}000-character context budget" (main.tex:119) | regrag/generation/config.py:143 `RAG_CONTEXT_TOTAL_CHARS: int = 7_000` | — | **VERIFIED** (observation: assembled context max is 7,085 chars — `rag_context.max_chars` — because per-block headers overshoot the passage allowance; the *budget* is 7,000 as stated; 7,085 is not quoted in the paper) |
| 4b | "447 of 528 RAG prompts are clipped" (main.tex:119) | tables_paper `rag_context.truncated_rows: 447`, `rows_stamped: 528`; my recount 447/528 | 528 = 2 modes × 3 models × 88 | **VERIFIED** |
| 4c | "240 ranked passages dropped" (main.tex:119) | tables_paper `dropped_rows: 240`; my recount: 240 rows have `dropped_ranks` and **total dropped ranks = 240** (every event drops exactly rank 3) | — | **VERIFIED** (unit coincidentally identical: compute_tables.py counts *rows with drops*; the passage count is also 240) |
| 5 | "Another 80 of the 192 closed-book answerable rows state the sentinel yet answer anyway" (main.tex:253) | my scorer re-run: `hedged answerable: 80 \| hedged probes: 35` (80+35 = 115 = JSON pooled `hedged_then_answered`); tables_paper closed_book `hedged_then_answered: 115` over 264 rows | 192 = 64×3 | **VERIFIED** (observation: 65 of the 80 match the exact benchmark sentinel; 15 hedge via the scorer's soft refusal paraphrases — "state the sentinel" is mildly loose for those 15) |
| 6a | "six of 64 questions retrieving no chunk of the governing instrument at $k{=}3$" (main.tex:258) | bm25_recall_gate_c_2026-09-11.json: `hits@3: 58, n: 64`, `doc_misses_at_k3` lists exactly 6 (Q002, Q008, Q043, Q044, Q054, Q061) | 64−58 = 6 | **VERIFIED** for BM25 (observation: the dense arm has **7** misses — Q006, Q008, Q011, Q036, Q046, Q047, Q061; sentence reads as BM25-specific, one clause further from its antecedent than ideal) |
| 6b | "a two-question difference, 33 versus 31 of 63" (main.tex:258) | dense JSON `article_level_hits.hits@3: 33`; BM25 JSON `31`; both `n_scored: 63` | 33/63 = 52.381 → 52.4 ✓; 31/63 = 49.206 → 49.2 ✓; 33−31 = 2 | **VERIFIED** |
| 7 | Q006 example (main.tex:255): gold Article 52(4) of the 2024 Notarization Law verbatim-intact; opens "Điều 52 của Nghị định 23/2015/NĐ-CP, sửa đổi bởi Nghị định 111/2020/NĐ-CP…"; WRONG_INSTRUMENT / NON_COVERING_PROVISION; substantively correct | generations.json row (vistral-7b/rag_bm25/Q006): answer_text opens `Theo Điều 52 của Nghị định 23/2015/NĐ-CP, sửa đổi bởi Nghị định 111/2020/NĐ-CP và…`; extracted = [23/2015/NĐ-CP Điều 52; 46/2024/QH15 Điều 32]; gold = 46/2024/QH15 art. 52 khoản 4; my rescore: correctness 1.0, types {NON_COVERING_PROVISION, WRONG_INSTRUMENT}; gold passage (Điều 52, "điều 52. sửa lỗi kỹ thuật trong văn bản công chứng…") verified as substring of the prompt; conditioning INTACT genuinely (rank 1, no truncation, no drop) | — | **VERIFIED** (all five elements) |
| 8 | "validated it against 50 expert-annotated responses"; "(3/3 and 10/10)"; "misses 15 ... and 8"; "$\kappa = 0.20$ / 0.39 / 0.62"; "misses ten and over-flags five"; "validation post-dates the campaign ... (\texttt{strict=False} in the log)" (main.tex:127) | scorer_validation_2026-09-15.json: n_rows 50; correct tp 3 fp 0, fn 15; abstained tp 10 fp 0, fn 8; κ 0.2038 / 0.3863 / 0.6154; hallucinated fn 10, fp 5; date 2026-09-15; tables_paper `metric_status: "unvalidated (aggregated strict=False)"`, tables generated 2026-09-13, campaign 2026-09-12→13 | 0.2038→0.20; 0.3863→0.39; 0.6154→0.62; 10−5 = 5 | **VERIFIED** |
| 9a | "49\% (BM25) and 43\% (dense) of answerable rows cite a wrong or non-covering provision" (main.tex:253) | 94/192, 83/192 (see 2d) | 48.96 → 49; 43.23 → 43 | **VERIFIED** |
| 9b | "102 of 192 closed-book answerable rows (64 $\times$ 3 models) asserting a provision that does not govern ... and 76 citing an instrument other than the governing one (categories overlap)" (main.tex:253) | tables_paper closed_book types: NON_COVERING_PROVISION 102, WRONG_INSTRUMENT 76; my recount identical | 192 = 64×3; 102+76 > 116 total unfaithful rows ⇒ overlap real | **VERIFIED** |
| 9c | "article-level F1 $= 0.005$"; Table II closed-book row 0.005/0.005/0.005/0.008 (main.tex:185,187) | tables_paper closed_book P/R/F1 0.0053, clause 0.0083 | 0.0053 → 0.005; 0.0083 → 0.008 | **VERIFIED** |
| 9d | "0.321 (BM25) and 0.434 (dense)"; Table II 0.293/0.354/0.321/0.300 and 0.399/0.476/0.434/0.317 | tables_paper bm25 0.2932/0.3545/0.3209/0.300; dense 0.3989/0.4762/0.4341/0.3167 | F1 = 2PR/(P+R): 0.32088 → 0.321; 0.43414 → 0.434; 0.3545(=67/189 raw 0.35450…) → 0.354 | **VERIFIED** |
| 9e | "71 of 72 probe rows receive substantive answers" (main.tex:253) | tables_paper closed_book `probe_answered: 71, probe_abstained: 1`; Table I 0.042 = 1/24 | 72 = 24×3 | **VERIFIED** |
| 9f | "identical answers in only 45 of 264 shared instances" (main.tex:147) | tables_paper `tier1_rag_arm_identical_answers {identical: 45, of: 264}`; my independent recount 45/264 (exact `answer_text` equality, 88×3) | 264 = 88×3 | **VERIFIED** |
| 9g | Table I, all 27 cells (main.tex:162-172) vs tables_paper `table1_by_model_mode` | e.g. 0.4375→0.438, 0.3438→0.344, 0.3125→0.313, 0.4688→0.469, 0.4219→0.422, 0.6719→0.672, 0.5938→0.594, 0.9848→0.985, 0.9499→0.950, 0.9158→0.916, 0.9116→0.912, 0.9393→0.939, 1/24=0.0417→0.042, 12/24=0.500, 9/24=0.375, 3/24=0.125 | all round-half-up correct at 3 dp | **VERIFIED** |
| 9h | Table III (main.tex:220-221): BM25 0.734/0.906/0.381/0.492; dense 0.719/0.891/0.365/0.524 | bm25 JSON 47/64, 58/64, 24/63, 31/63; dense JSON 46/64, 57/64, 23/63, 33/63 | 0.734375→0.734; 0.90625→0.906; 0.38095→0.381; 0.49206→0.492; 0.71875→0.719; 0.890625→0.891; 0.36508→0.365; 0.52381→0.524 | **VERIFIED** |
| 9i | RQ3 percentages "90.6% (73.4%)", "49.2% (38.1%)", "89.1%", "52.4% against 49.2%", conclusion "reaches 90\%" / "below 53\%" (main.tex:258, 266) | same JSONs | 90.625→90.6; 73.4375→73.4; 49.206→49.2; 38.095→38.1; 89.0625→89.1; 52.381→52.4; 90.6≥90 ✓; 52.4<53 ✓ | **VERIFIED** |
| 9j | "the 3,703-chunk Tier-2 corpus ... across 22 instruments" (main.tex:148) and "full 3,703-chunk statutory corpus" (main.tex:266) | both recall JSONs: `corpus_chunk_count: 3703`, `instrument_count: 22` | — | **VERIFIED** |
| 9k | "In the delivered revision, 63 of the 64 passages consist of verbatim article text substituted" (§III-A, main.tex:97) | data/gold/passage_repair_log.json: `repaired: 63`, `already_verbatim: 0`, `unrepairable_locator: 1` (= Q036, the annex row) | 63 + 1(Q036) = 64 | **VERIFIED** |
| 9l | "Article-level gold citations ... derivable for 63 of the 64 answerable rows; clause-level gold ... present for 40" (§III-A, main.tex:99); Table II comment 189 = 63×3, 120 = 40×3 | questions_canonical.json recount: 64 answerable, 63 with article gold, 40 with clause gold; Q036 `gold_citations` empty; recall JSONs `n_scored: 63, excluded Q036`; tables_paper `citation_scorable_rows: 189`, `clause_gold_rows: 120` | — | **VERIFIED** |
| 9m | "792 generated answers"; "709 answers finish naturally and 83 hit the token cap"; "All 792 prompts round-trip byte-identical" (main.tex:138) | generations.json 792 rows; tables_paper finish_reasons {stop 709, length 83}, prompt_exact_true 792 | 709+83 = 792 | **VERIFIED** |
| 9n | "64 answerable ... 24 unanswerable probes" (abstract, §III-A, contributions); "88 rows"; "$3\times3\times88$" | tables_paper gold {88, 64, 24}; questions_canonical recount | 64+24 = 88; 3×3×88 = 792 | **VERIFIED** |
| 9o | "Closed-book hallucination rates span 0.44--0.75" and "Groundedness ... (0.91--0.98)" (main.tex:250) | Table I extremes 0.4375–0.750 and 0.9116–0.9848 | 0.4375→0.44 ✓; 0.9848→0.98 ✓ | **VERIFIED** |
| 9p | "top-3 retrieval over the 64-chunk fixture" (main.tex:103) | tier1_chunks.json: 64 chunks | — | **VERIFIED** |
| 9q | "roughly doubles without it" (main.tex:253) | 34.8→61.3 (×1.76), 34.4→68.6 (×1.99); corrected 33.3→61.3 (×1.84), 34.5→68.6 (×1.99) | — | **VERIFIED** (qualitative, holds both ways) |

---

## 3. Cross-place consistency map (multi-place values)

| Value | Places | Consistent? |
|---|---|---|
| 43–49% mis-citation | abstract :53 ("43--49\%"), RQ2 :253 ("49\% (BM25) and 43\% (dense)"), conclusion :266 ("43--49\%") | ✓ all = 94/192, 83/192 |
| ~35% intact-evidence rate | abstract :53 ("about 35\%"), RQ2 :253 ("near 35\%" + fractions), conclusion :266 ("near 35\%") | ✓ mutually; ⚠ inherits N3-M1 (corrected pooled 34.0%) |
| 33–42% clipped | RQ2 :253 only | ⚠ endpoint under corrected buckets = 43% (N3-M1) |
| 61–69% absent | RQ2 :253 only | ✓ |
| F1 0.005 | abstract :53, RQ2 :253, Table II :187 | ✓ = 0.0053 |
| 0.32–0.43 F1 lift | abstract :53 vs Table II :189–190 (0.321, 0.434) | ✓ |
| clause ≤ 0.317 / "0.32" | RQ2 :253 ("never exceeds 0.317"), conclusion :266 ("at or below 0.32"), Table II (0.300, 0.317) | ✓ (0.3167 max) |
| 3,703 chunks / 22 instruments | §III-B bullet :148, conclusion :266, both recall JSONs | ✓ |
| 64/24/88/792 | abstract, contributions :83, §III-A :95, §V :138, Fig. :237, captions | ✓ |
| 33/64 & 47/64 | §III-B :103 only (RQ2 split uses row-level fractions) | ✓ internally |
| 45 of 264 | §III-B bullet :147 only | ✓ |
| 447/528/240/7,000 | §IV-A :119 only | ✓ |
| 90% / below 53% | conclusion :266 vs Table III 0.906 / 0.524 | ✓ |
| 71 of 72 & 80 of 192 | RQ2 :253 only; 80+35 = 115 = JSON pooled over 264 | ✓ |

---

## 4. Script-logic audit (the two round-3 scripts + compute_tables.py)

1. **`compute_conditioned_rates.py` — BUG (drives N3-M1).** Conditioning test
   (lines ~57-61) checks only `retrieved_chunk_ids` membership and
   `rag_context_truncated_ranks`; `rag_context_dropped_ranks` is never consulted.
   15 rows (9 BM25: Q008, Q034, Q060 ×3 models; 6 dense: Q034, Q039 ×3) retrieved
   the gold chunk at rank 3 with `dropped_ranks=[3]` and are bucketed INTACT.
   Prompt-text audit: 6 of 15 have zero gold text in the prompt, 9 only a clipped
   prefix via truncated siblings. Denominators 66/90 are wrong under the paper's
   stated criterion; corrected 57/84 with numerators 19/29.
2. **`verify_tier1_conditioning.py` — same bug**, plus a masking artifact: its
   text-level check tests only the **first 80 normalized chars** of the gold
   passage, so the 9 PREFIX-carrying dropped-gold rows pass as "text present";
   its printed `absent_text == absent (93/51)` equality is partly coincidental
   (3 BM25 ABSENT rows have an 80-char prefix present via same-opening sibling
   articles of the same instrument family, offsetting the 3 NOTEXT dropped-gold
   rows). The equality therefore does *not* prove chunk-presence ⟺ text-presence.
3. **Join keys — OK.** Both `qid2chunk` variants (`question_ids`-preferred in
   verify script, `question_id`-preferred in compute_conditioned_rates) produce
   identical 64-question maps (verified: 0 differently-mapped questions); tier1
   chunks = 64, bijection with answerable questions; `rows with retrieved ids
   outside tier1 file: 0`.
4. **Denominators — OK elsewhere.** Row totals 192/192 (93+33+66, 51+51+90 under
   the script's buckets); per-model retrieval identical within a mode (absent
   counts divisible by 3); answered-row rates use answered-only denominators
   (48/49/54/60/62/63/64 as appropriate); refused counts 16/15/10/4/2/0 match
   tables_paper `false_abstentions`.
5. **Sanity gate — genuine.** `overall_unfaithful=94/192` and `83/192` reproduce
   tables_paper `citation_unfaithfulness_rows` (94, 83) via the same
   `score_response` path as `compute_tables.py`; my independent rescore agrees
   (UNF 116/94/83; NCP 102/71/64; WI 76/34/21).
6. **`compute_tables.py` (context block)** — `truncated_rows`/`dropped_rows` are
   *row* counts, not passage counts; the paper's "240 ranked passages dropped" is
   numerically right only because every drop event dropped exactly one passage
   (rank 3). `max_chars: 7085` is assembled-context length incl. per-block
   headers; the configured budget is 7,000 (`config.py:143`), so the paper's
   "7,000-character context budget" stands.
7. **Q006 candidate filter — sound.** Requires cond INTACT, WRONG_INSTRUMENT,
   correctness ≥ 1.0; the printed Q006 row independently re-verified (rank 1,
   untruncated, undropped, full gold passage substring of prompt, correctness
   1.0, extracted citations 23/2015/NĐ-CP Điều 52 + 46/2024/QH15 Điều 32).

---

## 5. Artifacts (this lane)

- `verify_tier1_conditioning_stdout.txt` — re-run of scripts/verify_tier1_conditioning.py
- `compute_conditioned_rates_stdout.txt` — re-run of scripts/compute_conditioned_rates.py
- `spotcheck_n3.py` / `spotcheck_n3_stdout.txt` — independent meta/conditioning/hedge/identical-answers/Q006 recount
- `spotcheck_n3b.py` / `spotcheck_n3b_stdout.txt` — chunk-condition × prompt-text cross-tab + corrected text-level rates

All analysis read-only; nothing outside `reports/redteam3_2026-09-15/laneN3_numeric/` modified.
