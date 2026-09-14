# Lane H3 — Hostile Reviewer #2 — Round-3 (Round-4 pass) Red-Team Findings

Repo: `/mnt/data/seminar_2` (read-only; scripts under `reports/redteam3_2026-09-15/laneH3_hostile/`)
Target: `paper/main.tex` (277 lines, IEEEtran, 6-page limit), EDAS N35414, deadline 2026-09-15.
Method: every claim re-derived from `data/eval/*.json`, `data/gold/*`, `data/processed_chunks/*`,
`regrag/**`, `scripts/**`; repo scorer (`regrag.evaluation.metrics.score_response`) used exactly
as `scripts/compute_tables.py` / `scripts/compute_conditioned_rates.py` do. Prior rounds read
(`reports/redteam2_2026-09-15/ROUND2_REPORT.md`); fixed items not re-reported unless the fix
created a defect.

**Verdict table**

| ID | Severity | One-line summary |
|---|---|---|
| H3-W1 | WARN | "49%/43% … cite a wrong or non-covering provision" and "~35% intact" count the 4-type unfaithfulness union; rows that cite nothing at all are included (cite-only: 41%/34% overall, 29%/23% intact) |
| H3-W2 | WARN | "80 … state the sentinel yet answer anyway": 0/80 contain the sentinel as §III-C defines it; 65/80 contain the prompted keyphrase, 15/80 match only soft paraphrase templates — and "the sentinel" names two different strings in one paper |
| H3-W3 | WARN | §III-B "chunks are articles (Điều), with clause (Khoản) boundaries preserved inside them" contradicts the delivered per-clause corpus (3,122/3,703 clause-level chunks) |
| H3-N4 | NOTE | "six of 64 questions retrieving no chunk … at k=3" is the BM25 count; the dense arm misses 7 (57/64 @ 89.1%), so the sentence understates dense misses by one |
| H3-N5 | NOTE | "sits between at 33--42%" fails for dense: clipped 33.3% < intact 34.4% (only BM25's 42.4% sits between) |
| H3-N6 | NOTE | Post-hoc conditioning split has a selection confound + small cells + no test; the intact-vs-absent difference is real (χ²≈10.8 / 15.3, p≈0.001 / 0.0001) but intact-vs-clipped is not (χ²≈0.54) — quote a test or drop "roughly doubles" |
| H3-N7 | NOTE | "Qwen2.5-3B keeps a genuine reduction": BM25 arm d=20.6pp ≈ 2.5 SE, Wald 95% CIs overlap; only the dense arm is clearly significant — inconsistent statistical standard vs "indistinguishable" for the 7B |
| H3-N8 | NOTE | Refused rows concentrate in gold-ABSENT cells (BM25: 20/28); "falsely refuses" as pure calibration defect is undercut by refusals being evidence-aware |
| H3-N9 | NOTE | Q006 RAG narrative is verified but selective: same answer also cites the *right* instrument 46/2024/QH15 with the *wrong* article (Điều 32); the "fabricated quotation" claim is only consistent with (not proven by) the corpus |

No BLOCKER found. All headline numbers survive verification; the defects are labeling/precision
and one factual misdescription of the corpus chunking.

---

## H3-W1 — "cite an incorrect instrument" headline counts rows that cite nothing at all

**Paper text (abstract, line 53):**
> "However, 43--49\% of RAG answers on answerable questions still cite an incorrect instrument or non-governing provision---about 35\% even when the governing passage reaches the prompt intact---"

**Paper text (§V-B RQ2, line 253):**
> "but mis-citation remains the modal failure: 49\% (BM25) and 43\% (dense) of answerable rows cite a wrong or non-covering provision. Splitting on whether the gold chunk actually reached the prompt, the rate stays near 35\% in both arms when it arrives intact (23/66 BM25, 31/90 dense)…"

**What the numbers actually are.** Both tables/conditioned scripts define unfaithfulness as the union
`{WRONG_INSTRUMENT, NON_COVERING_PROVISION, UNCITED_ASSERTION, NUMERIC_THRESHOLD_MISMATCH}`
(`scripts/compute_conditioned_rates.py` lines 27–31; `scripts/compute_tables.py` lines 67–72).
`UNCITED_ASSERTION` is, per `regrag/evaluation/metrics.py` lines 58–59, "a fluent fabrication
carrying no citation at all … scored strictly WORSE than a wrong citation". Re-scoring every row
with the repo scorer and splitting the union:

| arm | 4-type union (paper's %-tile) | cite-only WI∪NC | rows w/ no citation type |
|---|---|---|---|
| rag_bm25 | 94/192 = 49.0% | **79/192 = 41.1%** | 15 |
| rag_dense | 83/192 = 43.2% | **66/192 = 34.4%** | 17 |
| BM25 INTACT | 23/66 = 34.8% ("~35%") | **19/66 = 28.8%** | 4 |
| Dense INTACT | 31/90 = 34.4% ("~35%") | **21/90 = 23.3%** | 10 |
| BM25 ABSENT | 57/93 = 61.3% | 50/93 = 53.8% | 7 |
| Dense ABSENT | 35/51 = 68.6% | 33/51 = 64.7% | 2 |

So the literal claim "cite an incorrect instrument or non-governing provision" — the paper's own
Related-Work definition of "citation mismatch" (line 83) — overstates the measured mechanism by
~8 pp (BM25) and ~9 pp (dense), and the "~35% intact" headline would be ~29% (BM25) / ~23% (dense).
The phenomenon survives; the magnitude and mechanism are mislabeled because no-citation fabrications
and right-article-wrong-figure rows are folded into "cite a wrong provision".

**Recipe:** `.venv/bin/python - <<'EOF'` — load `data/eval/generations.json`, score with
`score_response` (as `compute_conditioned_rates.py` does, incl. `UNFAITHFULNESS_TYPES`), then
intersect `set(r._types)` with `{"WRONG_INSTRUMENT","NON_COVERING_PROVISION"}`; split cells via
`generations_meta.jsonl` `retrieved_chunk_ids`/`rag_context_truncated_ranks` vs the question's
Tier-1 chunk (`data/processed_chunks/tier1_chunks.json` metadata). Copy of the script:
`reports/redteam3_2026-09-15/laneH3_hostile/verify_h3.py`.

---

## H3-W2 — "80 … state the sentinel": no row contains the §III-C sentinel; 15/80 contain no benchmark-defined refusal string at all

**Paper text (§V-B RQ2, line 253):**
> "Another 80 of the 192 closed-book answerable rows state the sentinel yet answer anyway; a simple keyphrase abstention scorer would credit these as correct refusals, motivating our scorer's assertion requirement."

**Paper text (§III-C, line ~108):** "their gold target is the sentinel string \emph{Không có trong kho văn bản} (``not in the document corpus'')".

**Ground truth.** §III-C's sentinel is `Không có trong kho văn bản`
(`regrag/generation/config.py` line 157). The prompt actually instructs refusal with a different
string, `ABSTENTION_KEYPHRASE = "THÔNG TIN KHÔNG CÓ TRONG TÀI LIỆU"` (`regrag/generation/prompts.py`,
quoted in the `abstention.py` module docstring). Of the 80 scored-hedged closed-book answerable rows
(recomputed via the repo scorer, exactly 80): **0/80** contain the §III-C sentinel; **65/80** contain
the prompted keyphrase; **15/80** match only soft paraphrase templates (counts by template: `unable_english` 2, `không đủ thông tin`-family, `không tìm thấy`, `corpus_silent`, etc. — e.g. Q039/Q046 qwen-7b match `unable_english` only; Q006 qwen-3b matches `no_information` only). Therefore "a simple keyphrase abstention scorer would credit these" holds for 65, not 80, and "state the sentinel" is false under the paper's own §III-C definition of "sentinel". The Q008 example (line 255) is nevertheless CORRECT — Q008/qwen-7b/closed-book does begin with the prompted keyphrase verbatim ("THÔNG TIN KHÔNG CÓ TRONG TÀI LIỆU."); the defect is the blanket "80" and the dual use of "the sentinel" (§III-C gold target vs §IV-B prompted string).

**Recipe:** score closed-book answerable rows via `score_response`; keep records with
`abstention.hedged_then_answered`; on each `answer_text` run
`regrag.evaluation.metrics.detect_abstention` and split `dec.matched` (exact) vs `dec.soft_matched`.
Script: `reports/redteam3_2026-09-15/laneH3_hostile/verify2_h3.py` (function `metrics_detect` used for the split).

---

## H3-W3 — §III-B "chunks are articles" contradicts the delivered per-clause corpus (which also breaks the intuitive reading of "string-match a chunk")

**Paper text (§III-B, line 103):**
> "Tier~2 is the segmented full text of the ingested instruments and is the corpus on which retrieval quality is measured (Table~\ref{tab:retrieval}). Segmentation follows the statutory hierarchy: chunks are articles (\emph{Điều}), with clause (\emph{Khoản}) boundaries preserved inside them, and preambles retained rather than discarded."

**Ground truth.** `data/processed_chunks/corpus_chunks.json` (3,703 chunks): **3,122 chunk ids are
per-clause** (`46/2024/QH15_D52_K1` holds only Khoản 1's text, 273 normalized chars, vs the
1,723-char Điều 52 passage); **830 of 1,081 (doc,article) pairs have >1 chunk**; doc 46/2024/QH15 has
77 articles → 297 chunks. The builder's own header says "clause-level chunks at
data/processed_chunks/corpus_chunks.json" (`scripts/build_corpus_chunks.py` line 2). Short articles
are single chunks marked `D1_Kall`. So the delivered corpus is clause-chunked, not article-chunked.

Corollary, also verified: the coverage invariant's strict tier (`scripts/regenerate.py` lines 112–120)
accepts `chunk ⊆ passage`; running it on the delivered files gives strict=63 / squash=0 / loose=0 /
not-found=Q036 exactly as the paper claims — but a direction split shows **all 63 strict matches are
chunk-in-passage (63/0/0)**; no passage is contained in any single chunk. For article-length passages
in a per-clause corpus this is near-tautological after the §III-A repair, which the paper discloses
("partly self-satisfying", line 99); the undisclosed part is the mismatch between the §III-B
description of the corpus granularity and the data shipped with the paper.

**Recipe:** `json.load(data/processed_chunks/corpus_chunks.json)`; count chunk_ids matching
`_K\d+$` (3122/3703); count articles with >1 chunk (830/1081). For the direction split:
`normalize_ws(gold_passage) in normalize_ws(chunk)` vs `normalize_ws(chunk) in normalize_ws(gold_passage)`
with the ≥30-char floor, exactly as `scripts/regenerate.py` lines 112–120.

---

## H3-N4 — "six of 64 questions retrieving no chunk … at k=3" is BM25-only; dense misses 7

**Paper text (§V-C RQ3, line 258):**
> "Document-level retrieval is strong but incomplete, with six of 64 questions retrieving no chunk of the governing instrument at $k{=}3$, and placing the specific governing article in context remains difficult"

**Ground truth.** `data/eval/bm25_recall_gate_c_2026-09-11.json`: `doc_level.recall@3=0.90625`, hits@3=58 → 6 misses. `data/eval/dense_recall_gate_c_2026-09-13.json`: `recall@3=0.890625`, hits@3=57 → **7 misses** (dense `doc_misses_at_k3` = Q006, Q008, Q011, Q036, Q046, Q047, Q061). Because the preceding sentence compares the dense arm ("The dense arm is close behind at document level (89.1\% at $k{=}3$)"), the sentence reads as pooled and undercounts the dense arm by one.

**Recipe:** read the two recall JSONs' `doc_level` hits and subtract from 64.

---

## H3-N5 — "sits between at 33--42%": false for the dense arm

**Paper text (line 253):** "the rate stays near 35\% in both arms when it arrives intact (23/66 BM25, 31/90 dense), sits between at 33--42\% when the context budget clips it, and rises to 61--69\% when it is absent".

**Ground truth:** BM25 clipped = 14/33 = 42.4% (between 34.8% intact and 61.3% absent ✓). Dense clipped = 17/51 = **33.3%**, which is *below* dense intact 34.4% — it does not "sit between" intact (34.4%) and absent (68.6%). The "33–42%" range itself is a fair two-arm span; the word "between" is not.

**Recipe:** `scripts/compute_conditioned_rates.py` output (re-run, read-only) — `rag_dense TRUNCATED: 17/51 (33.3%)` vs `INTACT: 31/90 (34.4%)`.

---

## H3-N6 — Post-hoc conditioning split: selection confound, small cells, no test; recommend either a test or softer claims

**Paper text (line 253):** "citation failure persists under full evidence conditioning and roughly doubles without it."

**Attacks that partially land:**
1. Intact/clipped/absent assignment is the retriever's own ranking, which correlates with question difficulty; the groups are not exchangeable. The paper nowhere flags this selection bias as a limitation of the new split.
2. Cells are small (66/90/33/51/93/51) with no CI and no multiple-comparison note; refused rows sit in the denominators (INTACT BM25: 6 refused of 66; excluding them 23/60 = 38.3%, same story).
3. Defensive fact for the author: the intact-vs-absent difference is not noise — Pearson χ² from the contingency tables: BM25 [[23,43],[57,36]] χ²≈10.8 (p≈0.001); dense [[31,59],[35,16]] χ²≈15.3 (p≈0.0001). But intact-vs-clipped is indistinguishable ([[23,43],[14,19]] χ²≈0.54, p≈0.46) — consistent with the paper's own "35 vs 33–42" span. "Roughly doubles" = 1.76×/1.99× — fine.

**Recipe:** recompute χ² from the four published cell counts by hand; no test or corrected claim appears anywhere in the paper.

---

## H3-N7 — "genuine reduction" (3B) vs "indistinguishable" (7B): same sample size, different statistical standards

**Paper text (§V-A RQ1, line 250):** "answered-row rates are $0.438\to0.458/0.408$ for Qwen2.5-7B, indistinguishable from closed-book at this sample size, whereas Qwen2.5-3B keeps a genuine reduction ($0.762\to0.556/0.450$)."

**Ground truth (repo scorer):** 3B answered: closed 48/63 = 76.2%, BM25 30/54 = 55.6%, dense 27/60 = 45.0%. Wald 95% CIs: closed [0.657, 0.867]; BM25 [0.423, 0.689] — **overlapping**; dense [0.325, 0.575] — non-overlapping (d ≈ 3.7 SE). So only the dense arm clearly supports "genuine"; the BM25 arm is within the same noise band used to call 7B "indistinguishable". Recommend "partially genuine / significant only in the dense arm" or attach the test stats.

**Recipe:** proportions test on 48/63 vs 30/54 and 27/60 (n≈54–63 → SE ≈ 6–7pp per arm).

---

## H3-N8 — Refusals concentrate exactly where the gold is absent

**Ground truth (repo scorer):** of 28 BM25 answerable refusals (16 7B + 10 3B + 2 Vistral),
**20 are in ABSENT cells** (71% vs 48% base rate); dense 6/19 (7B) in ABSENT. The paper calls these
"falsely refuses" (line 250) as a calibration defect without noting that most refusals occur when the
supporting evidence was never retrieved — which reads as evidence-aware behavior and tempers the
"shift to refusal" story. No number is wrong; the framing is one-sided.

**Recipe:** split scorer-abstained answerable rows by the conditioned cells (scripts in this lane).

---

## H3-N9 — Q006 RAG example: verified but the same answer contains a second, unmentioned citation error; "fabricated quotation" unprovable

**Paper text (line 255):** "Returning to Q006 under RAG-BM25 (Vistral-7B), with that gold text intact in the prompt, the answer is substantively correct yet opens by citing ``\emph{Điều 52 của Nghị định 23/2015/NĐ-CP...}''---the right article number under the wrong instrument".

**Ground truth (generations.json row q006/vistral-7b/rag_bm25):** opening citation `23/2015/NĐ-CP Điều 52` ("right article number, wrong instrument") ✓; gold `46/2024/QH15 Điều 52 Khoản 4`, INTACT ✓, correctness ≥ 1.0 ✓, types {NON_COVERING_PROVISION, WRONG_INSTRUMENT} ✓. **However the same answer's extracted citations include `46/2024/QH15 Điều 32`** — the right instrument with the *wrong* article — so the model committed both error directions at once; the paper's "the right article number under the wrong instrument" exhibits only one. Also, "appends a fabricated statutory quotation" (Q006/closed-book/7B): the quoted fragment "Hợp đồng phải ghi rõ các nội dung sau đây" occurs **nowhere** in the 3,703-chunk corpus (0/3,703, including 869 BLDS-2015 chunks) — consistent with fabrication, but proving "fabricated" requires the real BLDS 2015 text, which is offline here: UNCHECKABLE.

**Recipe:** `generations.json` → row (q006, vistral-7b, rag_bm25) `extracted_citations` + `answer_text`; corpus grep for the quoted fragment.

---

## PRE-EMPTED (attacked, verified FINE — defensive facts for the author)

1. **Conditioned split reproduces exactly** (repo scorer, both arms; gate 94/83 matched): ABSENT 57/93, 35/51; TRUNCATED 14/33, 17/51; INTACT 23/66, 31/90; per-question top-3 presence 33/64 BM25, 47/64 dense; text-level gold-missing 144/384. (`compute_conditioned_rates.py` + independent run)
2. **RQ1 arithmetic is self-consistent**: 7B BM25 22/64 = 34.4% all-row and 22/48 = 45.8% answered-row ⇒ the 16 refused rows are necessarily not hallucinated (0 refused∩hallucinated), matching "a refused row cannot be scored hallucinated" (line 250). All six answered-row percentages (0.458/0.408/0.762/0.556/0.450) verified; Vistral 0.694 answered-only not claimed.
3. **False-refusal counts**: 7B 16/64=25.0% & 15/64=23.4%, 3B 10/64=15.6% & 4/64=6.3%, "against 0% closed-book" accurate for 7B (3B's single closed-book refusal is not claimed as 0).
4. **102/76 closed-book counts**: NON_COVERING_PROVISION=102, WRONG_INSTRUMENT=76, cite-only union=102 (WI⊆NC) — the "102 … and 76 … (categories overlap)" sentence is literally correct.
5. **71 of 72 probe rows** answered closed-book (1 abstained, 7B/closed); Vistral abstains on no probe in any mode (Table I all 0.000).
6. **45 of 264** identical RAG answers; **709/83** finish reasons; **447/528** clipped, **240** dropped, max 7085 chars — and "7,000-character context budget" is exact (`RAG_CONTEXT_TOTAL_CHARS = 7_000`, `config.py` line 147; the 7085 recorded max includes prompt wrappers).
7. **Table I/II/III cells** (tables_paper_2026-09-13.json + the two recall JSONs): every cell matches (0.438/0.344/0.313/0.750/0.469/0.422/0.625/0.672/0.594; 0.985/0.951/0.950/0.916/0.912/0.939; 0.042/0.500/0.375/0/0/0.125/0/0/0; 0.005/0.321/0.434 P/R/F1; 0.008/0.300/0.317; 0.734/0.906/0.381/0.492; 0.719/0.891/0.365/0.524); denominators 189 and 120; "33 versus 31 of 63"; "38.1% vs 36.5%".
8. **Scorer validation** (scorer_validation_2026-09-15.json): n=50 stratified 17/17/16 modes, 41 answerable; 3/3 fp=0 correctness; 10/10 fp=0 abstention; fn 15 and 8; hallucination fn=10, fp=5 (net −5); κ = 0.2038 / 0.3863 / 0.6154 → "0.20/0.39/0.62" — all disclosed statements exact.
9. **Coverage invariant**: strict=63, squash=0, loose=0, not-found=["Q036"] — matches "63 of the 64 passages … with the single annex-citing row excepted" (lines 99, 105). Q036 truly has no article gold (`gold_citations=[]`), annex passage "Phụ lục 1, Phần A, mục I…"; probe arm has the capital-adequacy row Q037; 24 probes; 64/64 answerable have source URLs; article gold 63; clause gold 40.
10. **Campaign claims**: single RTX 3090, `bnb-4bit-nf4+float16`, one model at a time (contiguous per-model time blocks), window 10.16 h ("one ten-hour window"), `max_new_tokens=512`, temperature 0, `do_sample=False`, seed 1234, 792/792 prompts byte-identical, 0 rows with a `DEGRADED:` backend tag, corpus_source `tier1_passages` on all rows.
11. **§IV-C/§IV-D disclosures** match the log: `metric_status: "unvalidated (aggregated strict=False)"`; the two tables aggregated strict=False; the "built to refuse" gate text is accurate for the code (`metrics.py` `assert_metrics_publishable`) with the relaxation disclosed.
12. **Abstract/RQ2/conclusion conditioned story is internally consistent**: 43–49% / ~35% / 33–42% / 61–69% / clause ≤ 0.32 / article recall < 53% all match the same sources; no stale blanket qualifier remains.
13. **Q008 example** verified verbatim (prompted keyphrase "THÔNG TIN KHÔNG CÓ TRONG TÀI LIỆU" then "Nghị định 02/2021/NĐ-CP … Điều 14 … Điều 15"); Q006 closed-book example verified verbatim ("Điều 405 Bộ Luật Dân sự năm 2015", wrong instrument 91/2015/QH13).
14. **\ref/label sweep**: all 12 referenced labels exist (`sec:intro/related/benchmark/method/results/disclosure/provenance/conclusion`, `tab:main/citation/retrieval`, `fig:pipeline`); `\S\ref{sec:benchmark}-A/-B`, `\S\ref{sec:method}-C` correct.
15. Refusals cannot be scored hallucinated (see #2); hedged-then-answered note `HEDGED_THEN_ANSWERED=1` is what the 80 count derives from — the count itself is right, only its "sentinel" description is loose (H3-W2).

## UNCHECKABLE
- Whether the Q006/closed-book quotation is *fabricated* vs a real (misapplied) BLDS 2015 quote — no offline copy of the Civil Code.
- The §IV-B "automated memory preflight" run (script exists, `scripts/preflight_memory.py`; no per-run log checked).
- 4-bit quantization fidelity of `transformers-4bit` vs a vLLM reference (tag present; no cross-check artifact).

## Files produced in this lane (scripts, read-only w.r.t. repo)
`verify_h3.py`, `verify2_h3.py` (scoring + conditioned/hedged split recomputations).