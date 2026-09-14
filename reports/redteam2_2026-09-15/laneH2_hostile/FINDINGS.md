# Round-2 hostile review (Reviewer #2 persona) — RegRAG-VN, IEEE-RIVF 2026

Lane: `laneH2_hostile`. Round-1 items (fixed or accepted) are NOT re-reported.
All quotes verified by reading the cited file; line numbers are grep-verifiable.
Data cross-checks used: `data/eval/generations_meta.jsonl`, `data/eval/generations.json`,
`data/eval/tables_paper_2026-09-13.json`, `data/eval/scorer_validation_2026-09-15.json`,
`data/eval/bm25_recall_gate_c_2026-09-11.json`, `data/eval/dense_recall_gate_c_2026-09-13.json`,
`data/processed_chunks/tier1_chunks.json`, `data/gold/questions_canonical.json`, `scripts/compute_tables.py`.

Counts: 2 BLOCKER, 8 WARN, 3 NOTE.

---

## BLOCKER-1 — The Tier-1 fixture's retrieval recall is NOT "trivially perfect": the fix-cycle sentence asserting both retrievers locate the target passage is empirically false, and the abstract's "even with the governing provision in the prompt" holds for only ~52% (BM25) / ~73% (dense) of rows.

Evidence (paper text):
- `paper/main.tex:103` — "Because each question's gold passage is in Tier~1 by construction, retrieval recall on it is trivially perfect and sparse and dense retrievers are indistinguishable"
- `paper/main.tex:147` — "Both BM25 and dense retrieval locate the target passage on the Tier-1 fixture, so differences between RAG-BM25 and RAG-Dense reflect distractor composition and ordering rather than retrieval recall" (fix-cycle sentence)
- `paper/main.tex:53` — "43--49\% of RAG answers on answerable questions still cite an incorrect instrument or non-governing article even with the governing provision in the prompt"
- `paper/main.tex:254` — "even with the governing provision inside the retrieved context, 49\% (BM25) and 43\% (dense) of answerable rows still cite a wrong or non-covering provision"
- `paper/main.tex:146` — "Tables~\ref{tab:main} and~\ref{tab:citation} measure generation when relevant evidence is supplied"

Evidence (campaign log, joined on `cache_key` = `question_id`+`model`+`mode`:
`data/eval/generations_meta.jsonl` `retrieved_chunk_ids` vs `data/processed_chunks/tier1_chunks.json` `metadata.question_id`→`chunk_id`; id namespace verified: all 1,584 retrieved ids exist in the local 64-chunk Tier-1 file, so matching is exact):
- Of 192 answerable rows per mode, the question's own gold chunk is **absent from the retrieved top-3** in **93 BM25 rows (48.4%)** and **51 dense rows (26.6%)**; of the rows where it IS retrieved it is truncated/dropped by the 7,000-char context budget in 42 (BM25) and 57 (dense) more, leaving it fully intact in the prompt in only **57/192 (29.7%)** BM25 and **84/192 (43.8%)** dense rows.
- Text-level confirmation independent of ids: searching each RAG prompt for the question's own gold-passage first 80 normalized characters shows the gold text is absent from 144 of 384 answerable RAG prompts (generations.json, `prompt` fields).
- Context damage is routine, e.g. `generations_meta.jsonl:96` (Q008/bm25/qwen-7b): `"rag_context_truncated_ranks": [1, 2]` — the rank-1 chunk itself ("Điều 3" of the governing passage set) is cut by the budget; `data/eval/tables_paper_2026-09-13.json` `campaign_provenance.rag_context` = `{"rows_stamped": 528, "truncated_rows": 447, "dropped_rows": 240}` (447 of 528 RAG prompts touched).

Why this is a round-2 kill: the round-1 fix added the "distractor composition and ordering" sentence — a NEW falsified empirical claim — while the abstract and RQ2 use "even with the governing provision in the prompt/in the retrieved context" to describe the headline 43–49% figure. For ~1/3 to ~1/2 of the counted rows there was no governing provision in the prompt at all, so the headline number is *not conditional on* evidence being present. This also collapses the paper's stated reason for splitting retrieval evaluation onto Tier-2 ("Independent Retrieval Evaluation", `main.tex:148`) and the "Upper-Bound Conditioning" framing (`main.tex:146`).

Minimal fix: recompute/restate every Tier-1 conditioning claim from the per-row prompt actually stamped (split RQ2's 49%/43% into "rows with gold chunk in top-3" vs "rows without"); delete or replace `main.tex:147`'s "both locate the target passage"; report and discuss the 7000-char truncation as an experimental variable (it is currently mentioned nowhere in the paper); weaken `main.tex:103` to "recall on the Tier-1 fixture is corpus-relative, not top-k-perfect".

## BLOCKER-2 — The Q059 flagship example mis-describes both the prompt content and the "unrelated circular": the prompt contained only TT 61/2025/TT-NHNN Điều 3 text, and the model cited exactly that; the benchmark itself labels the passage 32/2024/QH15 while its text is verbatim from 61/2025/TT-NHNN.

Evidence:
- `paper/main.tex:256` — "In Q059 (RAG-BM25), even with the governing text of the 2024 Law on Credit Institutions present in the prompt, the model attributes Article~3 to Circular 61/2025/TT-NHNN---retaining the correct article number while substituting an unrelated circular."
- `generations_meta.jsonl:147` (Q059/bm25/qwen-7b): retrieved ids `["tier1_200c31c7320b7be8_3", "tier1_200c31c7320b7be8", "tier1_200c31c7320b7be8_2"]` — three segments all of the 61/2025 Điều 3 family (`tier1_chunks.json`: Q059→`tier1_200c31c7320b7be8`, Q060→`..._2`, Q061→`..._3`; each has `author` "passage repaired 2026-09-11 from corpus 61/2025/TT-NHNN Điều 3 (verbatim; was annotator summary)").
- Text check: Q059's gold passage text matches Tier-2 chunk 61/2025/TT-NHNN Điều 3 ("Điều3.Giảithíchtừngữ...Mạnglướihoạtđộngcủangânhàngthươngmạibaogồmchỉnhánh,phònggiaodịch...") and NOT Tier-2 32/2024/QH15 Điều 3 ("Điều 3. Áp dụng tập quán thương mại"); the 2024-Law text appears nowhere in the Q059 prompt (`generations.json` row for `cache_key 66c86331d767f680ad70ef92`, line ~2819: `"extracted_citations": [{"doc_id": "61/2025/TT-NHNN", "article_id": "3", "clause_id": "5"}]`; prompt contains "Mạng lưới hoạt động" (=61/2025 text), not "Áp dụng tập quán thương mại" (=32/2024 text)).
- The row is internally ambiguous by the benchmark's own record (`data/gold/questions_canonical.json`, Q059: `"gold_doc_ids": ["32/2024/QH15", "61/2025/TT-NHNN"]`, `"doc_id_confidence": "ambiguous-multi-url"`, gold citation 32/2024/QH15 art 3 — the SAME Điều 3 Q059/Q060/Q061 all share, split across three chunks).

What actually happened: the prompt gave the model verbatim 61/2025/TT-NHNN Điều 3 text; the model cited 61/2025/TT-NHNN Điều 3 Khoản 5, i.e. it cited the instrument/article whose text it was reading. Calling that "substituting an unrelated circular" requires the 32/2024 gold citation to be ground truth — which the benchmark's own ambiguous-multi-url record and its own passage repair contradict. This example is presented as the paper's canonical demonstration of mis-citation despite evidence (¶: "In regulatory compliance, such citation errors are particularly hazardous..."), and the Q059 row contributes to the 49% headline numerator, which is exactly the number BLOCKER-1 shows to be confounded. If a curator trusts the 32/2024/QH15 gold, then the benchmark fed the model the WRONG passage for this row (61/2025 text under a 32/2024 label), which is itself a data-integrity failure that the provenance section claims cannot happen ("preventing degraded or unverified data from silently corrupting benchmark results", `main.tex:53`).

Minimal fix: delete or replace the Q059 example (e.g. with a verified closed-book example); resolve the Q059–Q061 triple before camera-ready (which instrument's Điều 3 governs, and why three questions share one article); if the 32/2024 gold is kept, the Tier-1 passage for Q059 must be the 32/2024 text and the example must be re-run.

## WARN-3 — The provenance "guarantee" is contradicted by the production log: the tables underpinning Tables I–II were aggregated with the publishability gate bypassed (`strict=False`, scorer `unvalidated`), and the paper never discloses this.

Evidence:
- `paper/main.tex:131` — "Aggregation functions strictly refuse to score or summarize rows whose backend is unverified, degraded, or mismatched with the evaluation setting." plus `main.tex:133` "By enforcing immutable provenance metadata across every stage, RegRAG-VN ensures that experimental conclusions rest entirely on authentic documents and verified execution paths." and `main.tex:77` "(iii) a provenance architecture for RAG benchmarks that guarantees execution integrity across complex multi-stage pipelines."
- `scripts/compute_tables.py:12-15` — "the lexical scorer is metric_status=\"unvalidated\" until the ~50-response human-label validation runs. assert_metrics_publishable would rightly refuse these rows, so aggregation runs with strict=False and every emitted table is stamped with both facts; the paper's §V carries the same disclosure." (the disclosure claim is false: `main.tex` never contains "unvalidated", "strict=False", or "publishable" — grep-verified)
- `data/eval/tables_paper_2026-09-13.json:3` — `"metric_status": "unvalidated (aggregated strict=False)"`

The mechanism advertised as contribution (iii) — "strictly refuse ... unverified" — did not run for its own headline tables; the code's own gate "would rightly refuse these rows". A reviewer cannot tell from the paper whether the 43–49% / 0.32–0.43 / kappa story changed because the scorer was validated afterwards (the 2026-09-15 validation post-dates the 2026-09-13 tables). No row in any shipped log ever carries a `DEGRADED:` tag, so the rejection path has zero exercised test evidence either.

Minimal fix: state in §V (not only in a code comment) that Tables I–II were aggregated with `strict=False` because the scorer was not yet validated, and that validation completed on 2026-09-15 with the reported kappas; add one exercised rejection test or drop "guarantees"/"strictly refuse" wording.

## WARN-4 — "the top-3 retrieved passages are concatenated into the prompt with identical formatting, isolating retrieval representation as the sole experimental variable" is violated by the 7,000-char budget (447/528 truncated, 240 ranks dropped); truncation is unmentioned in the paper.

Evidence:
- `paper/main.tex:119` — "In both RAG configurations, the top-3 retrieved passages are concatenated into the prompt with identical formatting, isolating retrieval representation as the sole experimental variable."
- `data/eval/tables_paper_2026-09-13.json` (`campaign_provenance.rag_context`): `"truncated_rows": 447, "dropped_rows": 240, "max_chars": 7085`; `generations_meta.jsonl:92` (Q004/bm25): `"rag_context_truncated_ranks": [3]`; `generations_meta.jsonl:96` (Q008/bm25): `"rag_context_truncated_ranks": [1, 2]`.
- Underlying mechanism `regrag/generation/prompts.py`: passages are clipped per-passage to a budget and "A passage whose remaining share is under the floor is dropped whole", with a truncation marker `[...Nội dung bị cắt do vượt giới hạn ngữ cảnh...]` — i.e. the two RAG arms' prompts differ in *how much evidence is cut*, not only in retrieval representation, so the "sole experimental variable" claim is false as an experimental design statement (and it interacts with BLOCKER-1's gold-chunk truncation counts).

Minimal fix: describe the context budget in §IV-A/§V-A, report truncated/dropped shares per arm, and either equalize the budgets' effect or analyze truncation as a covariate.

## WARN-5 — RQ1's headline causal claim survives the fix-cycle refusal disclosure unadjusted; under the paper's own logic the claimed reduction for Qwen2.5-7B-BM25 could be entirely a refusal artifact.

Evidence:
- `paper/main.tex:251` — "Conditioning on retrieved evidence lowers hallucination for both Qwen models (Qwen2.5-7B $0.438\!\to\!0.344/0.313$ ... The aggregate delta also entangles with refusal (a refused row cannot be scored hallucinated) ... Qwen2.5-7B falsely refuses 25.0\% and 23.4\% of answerable questions under RAG against 0\% closed-book"
- `data/eval/tables_paper_2026-09-13.json` (`table1_by_model_mode`): qwen-7b rag_bm25 `false_abstentions: 16` (=25%), rag_dense `false_abstentions: 15`, qwen-3b `10` and `4`, vistral `2` and `0`.

Since 16 of 64 rows "cannot be scored hallucinated" when refused, the 0.438→0.344 reduction (28 hallucinated→22) is within what refusals alone can produce; the section header "RQ1: evidence conditioning reduces hallucination for two of three models" and the lead sentence assert the reduction as established while the new sentence only discloses the confound — and the confound numbers are reported for Qwen-7B only, even though Qwen-3B also refuses (10/4 rows) and Vistral hallucination *rises* under RAG. If the refusal effect were the true mechanism, the honest conclusion is "no measurable hallucination reduction in answered rows" — which would flip RQ1.

Minimal fix: report hallucination rate restricted to answered rows (or with refusal handled as missing), and state the answered-row comparison in the RQ1 conclusion; disclose 3B/Vistral refusal counts in the same sentence.

## WARN-6 — "a 3.2-point gap within sampling noise at this corpus size" asserts statistical insignificance without a test, while the paper elsewhere disclaims significance testing; the "0.7 document-recall floor" is undefined.

Evidence:
- `paper/main.tex:259` — "the dense arm clears the same floor (89.1\% doc-level at $k{=}3$) and edges BM25 at article level at $k{=}3$ (52.4\% against 49.2\%), a 3.2-point gap within sampling noise at this corpus size"
- `paper/main.tex:138` — "binomial noise is on the order of six and ten percentage points respectively, so we report point estimates without significance tests"
- `paper/main.tex:259` — "clearing our 0.7 document-recall floor for article-level comparison" — the floor appears nowhere else in the paper (grep-verified), has no definition or rationale, and is trivially cleared by both arms, so it discriminates nothing.

The fix-cycle sentence converts a 2-row difference (33 vs 31 of 63) into a statistical verdict without a test — precisely the thing line 138 says the paper does not do. "Within sampling noise" without a McNemar/binomial test is an unbacked claim, especially since the paper's own headline 43 vs 49 (a 6-point gap at n=192, ~12 rows) is treated as signal in the abstract under the same noise scale.

Minimal fix: either run and report a paired test for the BM25-vs-dense Điều@3 difference, or rephrase to "a 2-row difference we cannot resolve at this scale"; delete the undefined floor or define and justify it.

## WARN-7 — "Expert agreement is κ=…" mislabels scorer-vs-expert agreement and collides with §III-D's "Inter-annotator agreement … was not measured"; "so its positive calls are exact" contradicts the over-flagging counted on the next line.

Evidence:
- `paper/main.tex:127` — "Every correctness and abstention call the scorer makes is confirmed by the expert (3/3 and 10/10), but it misses 15 expert-correct answers and 8 expert-judged abstentions, so its positive calls are exact and its rates conservative. Expert agreement is $\kappa = 0.20$ for correctness, $0.39$ for hallucination, and $0.62$ for abstention \cite{cohen1960kappa}; on hallucination the scorer misses ten and over-flags five"
- `paper/main.tex:112` — "Inter-annotator agreement on the gold labels was not measured" (§III-D, the minimal fix-cycle subsection)
- `data/eval/scorer_validation_2026-09-15.json` — `hallucinated.confusion = {"tp": 22, "fn": 10, "fp": 5, ...}` (fp=5 ⇒ hallucination positive calls are NOT exact) and `cohens_kappa` values 0.204/0.386/0.615.

Two adjacent-sentence contradictions introduced by the round-1 kappa fix: (a) "its positive calls are exact" is scoped to correctness/abstention but written as a blanket conclusion, and the very next sentence discloses 5 hallucination false positives; (b) "Expert agreement" — agreement between scorer and one expert on 50 responses — is a different quantity from inter-expert agreement, which §III-D denies measuring; the label invites a reader to think expert agreement was measured for the gold while the paper simultaneously says it was not.

Minimal fix: rename to "scorer–expert agreement"; qualify "its correctness and abstention positive calls are exact"; merge the disclosure into §III-D with one consistent vocabulary.

## WARN-8 — "bounding the end-to-end citation ceiling before generation begins" (conclusion) and "bounding end-to-end citation below the evidence-conditioned rates of RQ2" (RQ3) draw a causal ceiling from a recall number without the stated-model assumption; the bound also presupposes the falsehood of BLOCKER-1.

Evidence:
- `paper/main.tex:267` — "article-level retrieval drops below 53\%, bounding the end-to-end citation ceiling before generation begins"
- `paper/main.tex:259` — "only about half of questions can carry the governing article into the prompt, bounding end-to-end citation below the evidence-conditioned rates of RQ2"

Problems: (1) no end-to-end sentence was ever generated on Tier-2 — the claim is a model-based inference, not a measured result; (2) citation F1 is not bounded by recall@3 at 0.524: F1 ≤ 2R/(1+R) ≈ 0.69, so "drops below 53%" does not bound a citation *ceiling* at 53%; (3) the inference requires P(correct citation | governing article absent from top-3) = 0, which the paper elsewhere refutes — closed-book (no article at all) still yields F1 = 0.005 and 102 rows assert *some* provision (`main.tex:254`); (4) the comparison target "the evidence-conditioned rates of RQ2" presupposes RQ2 rows were evidence-conditioned, which BLOCKER-1 falsifies (half of BM25 rows had no governing passage at all).

Minimal fix: report this as the modeling assumption it is ("assuming correct citation requires the governing article in context, article-level recall@3 is an upper bound on end-to-end citation recall, with F1 ≤ ~0.69 at k=3…"), or run the Tier-2 end-to-end arm; do not present the bound as an empirical result.

## WARN-9 — Abstract and contributions overstate the coverage invariant: "requiring each question's supporting gold passage to match an ingested legal chunk exactly" is false for Q036 (annex row), whose gold is an unsubstituted annotator summary.

Evidence:
- `paper/main.tex:53` — "the retrieval corpus is aligned with the benchmark questions by requiring each question's supporting gold passage to match an ingested legal chunk exactly"
- `paper/main.tex:105` — "every retained answerable question's verbatim gold passage must string-match a chunk of the Tier~2 corpus"
- `paper/main.tex:99` — "one cites a \emph{Phụ lục} annex rather than a numbered article and is retained as an annotator summary" and `data/processed_chunks/tier1_chunks.json` Q036: `gold_citation: null` (Q036 also carries `"confidence"` absent; in `tables_paper…` Q036 is `citation_unscorable` and in the recall gates `article_level.excluded_ids: ["Q036"]`).

For Q036 there is no verbatim gold passage to string-match; the coverage invariant is vacuously satisfied, so "verifiably present" (`main.tex:77`) is certified for 63 of 64 rows, not "each". The paper does disclose the Q036 exception in §III-A, but the abstract and the invariant sentence overstate it.

Minimal fix: abstract/invariant wording "each of the 63 article-gold rows…" or verify the annex summary's text against the Tier-2 annex before claiming full coverage.

## WARN-10 — The headline "43–49% of RAG answers … still cite … even with the governing provision in the prompt" mixes rows with and without the provision in context; within-condition rates are not reported.

Evidence:
- `paper/main.tex:53` and `paper/main.tex:254` (quoted in BLOCKER-1); `data/eval/tables_paper_2026-09-13.json` `table2_by_mode_pooled`: `rag_bm25.citation_unfaithfulness_rows: 94` over `answerable: 192` (48.96%), `rag_dense: 83/192` (43.2%).
- BLOCKER-1's counts: of those 192-row denominators, the governing passage was absent from the context in 93 (BM25) / 51 (dense) rows and truncated-or-dropped in 42 / 57 more.

Rows that refused or had no passage can neither "cite an incorrect instrument" nor "cite with the provision in context", so the reported 49%/43% is an unconditional mixture, not the conditional "even with…" quantity the abstract and RQ2 claim it to be. The number is at least directionally unstable: with refusal rows excluded the mis-citation share can only rise, which a hostile reading will use as "the paper understates its own headline failure" — but the paper should not leave the reader to guess.

Minimal fix: report the mis-citation rate over the subset with the goid chunk intact in the prompt, and over the subset without it, with the refusal rows handled explicitly.

## NOTE-11 — "instrument-level retrieval is nearly solved" overstates 90.6% doc@3 in a closed 22-instrument corpus.

Evidence: `paper/main.tex:259` ("instrument-level retrieval is nearly solved") vs the gate files (`bm25_recall_gate_c_2026-09-11.json`: doc@3 58/64 = 0.906, six questions miss their instrument entirely; doc-level hits can also be inflated by instrument size — a 12-chunk-per-instrument average, 22 instruments). "Nearly solved" invites a 1-page rebuttal table of the six misses. Minimal fix: "doc-level recall is high (~91%) but six of 64 questions retrieve no chunk of the governing instrument; conflation with corpus-size effects is unchecked."

## NOTE-12 — No evidence the provenance rejection path ever fired: zero `DEGRADED:` tags in any shipped log, and no fault-injection test is described, so "prevents"/"guarantees" are untested claims about a mechanism the paper never exercised.

Evidence: `main.tex:75` ("Our evaluation harness explicitly rejects any row carrying degraded or unverified execution tags"), `main.tex:133`; grep of `data/eval/*.json*` for `DEGRADED` returns nothing. Minimal fix: one §V sentence reporting the rejection counts (which rows, why) during the campaign.

## NOTE-13 — Tier-1's use is framed as a design choice, while the pipeline log records it as recovery from a failure: "the Tier-2 re-ingest was rejected on duplicate chunk ids".

Evidence: `scripts/compute_tables.py:12-13` ("the 2026-09-13 campaign ran on the Tier-1 development fixture (corpus_source=tier1_passages - the Tier-2 re-ingest was rejected on duplicate chunk ids)") vs `paper/main.tex:103` ("built so that indexing, retrieval, prompting, generation and scoring could be integrated before the real instruments arrived") and `main.tex:146` ("measure generation when relevant evidence is supplied"). The paper never discloses that the campaign's Tier-1-only design was (at least in part) a consequence of a rejected Tier-2 ingest. Minimal fix: one sentence in §V-A naming the ingest failure and its fix status, or the reader will assume intentionality the log contradicts.

---

## Kill-shot paragraph (as Reviewer #2)

"This paper should not be accepted in its current form, because its central empirical claim is falsified by its own released logs. The abstract and RQ2 assert that 43–49% of RAG answers mis-cite 'even with the governing provision in the prompt', and the revised §V-A claims both retrievers locate the target passage on the Tier-1 fixture 'so differences between RAG-BM25 and RAG-Dense reflect distractor composition and ordering rather than retrieval recall'; but joining the campaign's own `generations_meta.jsonl` against the released `tier1_chunks.json` shows the question's gold chunk was absent from the retrieved top-3 in 48.4% of BM25 and 26.6% of dense answerable rows, and truncated or dropped by an undisclosed 7,000-character context budget in dozens more — 447 of 528 RAG prompts were damaged and the paper nowhere mentions a character budget. The flagship Q059 example is worse: its prompt contained only verbatim text of Thông tư 61/2025/TT-NHNN Điều 3 (the question's own gold passage, 'ambiguous-multi-url' in the canonical gold), and the model cited exactly 61/2025 Điều 3 — which the paper calls 'an unrelated circular' while asserting the 2024 Law's text was in the prompt, which it was not. Meanwhile the provenance architecture advertised as contribution (iii) — 'Aggregation functions strictly refuse to score or summarize rows whose backend is unverified' — produced the paper's own tables under `metric_status: 'unvalidated (aggregated strict=False)'`, because the code's publishability gate 'would rightly refuse these rows'; none of this is disclosed in the paper. When the conditionality of the headline numbers, the flagship example, and the provenance guarantee each fail on inspection of files the authors themselves ship as the authoritative artifacts of this benchmark, the paper's empirical core cannot be certified as written, regardless of what a re-run might salvage."