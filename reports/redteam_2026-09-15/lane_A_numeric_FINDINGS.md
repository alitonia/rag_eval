# Numeric-Consistency Audit — RegRAG-VN paper (IEEE-RIVF 2026, EDAS N35414)

Audit base: `/tmp/redteam_A/main_tex_snapshot_2026-09-14T1754Z.tex` (md5 `36a1add849b8dc0e0af084d909a991b3`, = repo state 2026-09-14T17:54Z).
**main.tex was edited by a concurrent process DURING the audit** (repo mtime 2026-09-15 00:51:15 +0700); see F10.
Line numbers below refer to the snapshot (identical to repo file at hash time).

Verdict: **0 BLOCKER / 2 WARN / 8 NOTE.** Every table cell, scorer-validation number, campaign count, and derived ratio that has a value in the four JSON sources matches them. The two WARNs are denominator/wording issues, not wrong numbers.

## Findings (most severe first)

### F1 — WARN — "of answered rows" mislabels the denominator of the 49%/43% mis-citation rates
- Quote (main.tex:254): `49\% (BM25) and 43\% (dense) of answered rows still cite a wrong or non-covering provision`
- Quote (main.tex:254): `with 102 of 192 answered questions asserting a provision that does not govern the question`
- Quote (main.tex:53): `43--49\% of RAG-generated answers still cite an incorrect instrument or non-governing article`
- Source: tables_paper_2026-09-13.json `table2_by_mode_pooled`: `rag_bm25.citation_unfaithfulness_rows: 94`, `rag_dense.citation_unfaithfulness_rows: 83`, `answerable: 192`, `rag_bm25.false_abstentions: 28`, `rag_dense.false_abstentions: 19`.
- Check: 94/192 = 48.96% → "49%", 83/192 = 43.23% → "43%" — the percentages are correct **only with the 192-answerable-rows denominator**. Under BM25, 28 of those 192 rows were false refusals that never produced an answer, so the rate *among actually answered rows* would be 94/164 = 57.3% (dense: 83/173 = 48.0%). Likewise closed-book had 1 false abstention, so "102 of 192 answered questions" should be "of 192 answerable questions" (191 answered). Same slack in "Another 115 of 192 closed-book answers" (main.tex:254) and in the abstract/conclusion phrase "RAG-generated answers" (lines 53, 267). Wrong-word, right-number: replace "answered" with "answerable" in all four places.

### F2 — WARN — clause-accuracy ceiling "never exceeds 0.317" / "at or below 0.32" holds only for pooled values; the cited log contains a per-cell 0.375
- Quote (main.tex:254): `and clause-level (\emph{Khoản}) accuracy never exceeds 0.317`
- Quote (main.tex:267): `clause accuracy remains at or below 0.32`
- Source: tables_paper_2026-09-13.json `table2_by_mode_pooled` max `clause_accuracy` = 0.3167 (→ 0.317, Table II) — the claim is true for the pooled Table II rows; but `table1_by_model_mode."qwen-3b::rag_bm25".clause_accuracy: 0.375` exceeds it.
- The paper never prints per-model clause accuracy, so no reader-visible contradiction — but the sentence as an unconditional statement ("never exceeds") is falsified by the paper's own log file. Safer wording: "pooled clause accuracy never exceeds 0.317 (Table II)".

### F3 — NOTE — abstract F1 range "0.32--0.43" is exact only under pooled-per-mode reading
- Quote (main.tex:53): `raises article-level citation F1 from 0.005 (closed-book) to 0.32--0.43`
- Source: pooled F1 0.3209 → 0.32 and 0.4341 → 0.43 (exact, Table II). However the minimum per-cell RAG article-F1 in the log is 0.3143 (`qwen-3b::rag_bm25.citation_f1`), which renders as 0.31 — if the range is read as spanning the six RAG cells, the lower bound is 0.31, not 0.32. Abstract does not state the pooling.

### F4 — NOTE — §III-A arithmetic wording suggests 63+1+1 rows inside a 64-row set
- Quote (main.tex:99): `Of the remaining rows, one cites a \emph{Phụ lục} annex rather than a numbered article and is retained as an annotator summary, while another whose governing instrument is absent was transferred to the unanswerable probe arm`
- 64 answerable = 63 verbatim + 1 annex leaves exactly one "remaining" row inside the 64; the "another" (transferred) row is outside the 64 (65 rows originally authored). The arithmetic is recoverable but the phrasing invites a 63+1+1-in-64 miscount.

### F5 — NOTE — refs.bib: one live entry never cited
- Quote (refs.bib:189): `@inproceedings{thakur2021beir,`
- `thakur2021beir` is defined but never `\cite`d and is not marked `_DISABLED`. (`rajpurkar2018squad2_DISABLED`, refs.bib:194, is intentionally disabled — fine per policy.) No rendered effect under BibTeX (uncited entries are dropped), listed per audit instructions. Verified: all 29 cited keys resolve; all `\ref` targets defined; no duplicate labels.

### F6 — NOTE — pipeline figure never referenced in text
- Quote (main.tex:247): `\label{fig:pipeline}`
- `grep -c "ref{fig:pipeline}" main.tex` = 0. IEEE style expects every figure called out in the text.

### F7 — NOTE — "\S IV-C assertion gate" referenced but never defined there
- Quote (main.tex:254): `motivating the assertion gate of \S\ref{sec:method}-C`
- The term "assertion gate" occurs exactly once in the paper (this sentence); §IV-C (scorer validation) describes exact positive calls and the hedge-then-answer undercount but never names or defines an assertion gate.

### F8 — NOTE — comment-only latency range "Qwen 5--9 s" contradicted by the log
- Quote (main.tex:262): `% budget allows: latency spread (Vistral RAG rows 164--175 s vs.\ Qwen 5--9 s)`
- LaTeX comment, not rendered. Vistral part correct (164.072 s, 175.4115 s); Qwen means in `campaign_provenance.latency_s_mean_by_model_mode` span 4.93–10.21 s (`qwen-3b::closed_book: 10.2109`), outside "5--9 s". Fix before reinstating the TODO.

### F9 — NOTE — numbers with no value in the four provided JSONs (no contradiction found, unverifiable here)
- Quote (main.tex:138): `greedy decoding (temperature 0, seed 1234, at most 512 new tokens)`
- Decode parameters and "two domain annotators" (main.tex:113) appear in none of the four JSON sources; flagged as not-covered-by-ground-truth, not as errors.

### F10 — NOTE — target edited during audit; removed "1.8×/1.7×" sentence verified correct before removal
- Quote (main.tex:5): `% IEEEtran.cls V1.8b and IEEEtran.bst are NOT installed in this TeX Live tree;` (only remaining "1.8" matches in the current revision)
- The first read (17:52Z) contained `The instrument-to-article gap persists across both retrievers (1.8$\times$ for BM25, 1.7$\times$ for dense)`; a concurrent edit at 00:51:15 +0700 removed it. Arithmetic had it right: 0.90625/0.49206 = 1.842 → 1.8×; 0.890625/0.52381 = 1.700 → 1.7×. All findings above are against snapshot md5 `36a1add849b8dc0e0af084d909a991b3`; re-diff before submission if edits continue.

## Verified categories (explicit)

- **verified: Table I** — all 27 cells match tables_paper_2026-09-13.json under half-up rounding (0.4375→0.438, 0.3125→0.313, 0.0417→0.042, 0.2344→0.234 in prose, groundedness 0.9116–0.9848→0.912–0.985).
- **verified: Table II** — all 12 cells; pooled denominators 189 = 63×3 (3 unscorable, Q036 annex) and 120 = 40×3; F1 = harmonic mean of pooled P,R re-derived: 2·0.2932·0.3545/(0.2932+0.3545) = 0.3209, 2·0.3989·0.4762/(0.3989+0.4762) = 0.4341.
- **verified: Table III** — BM25 47/64=0.734, 58/64=0.906, 24/63=0.381, 31/63=0.492; dense 46/64=0.719, 57/64=0.891, 23/63=0.365, 33/63=0.524 — all re-derived from raw hit counts in bm25_recall_gate_c_2026-09-11.json and dense_recall_gate_c_2026-09-13.json; doc n=64 / article n=63 (Q036 excluded in both logs); corpus_chunk_count=3703 ("3,703" ×2 in paper); instrument_count=22.
- **verified: §IV-C scorer validation** — 50 rows, 41 answerable/9 probes, 3/3 correctness (tp=3, fp=0), 10/10 abstention (tp=10, fp=0), misses 15 (fn) and 8 (fn), agreement 0.70, κ=0.3863→0.39, net undercount = 10−5 = 5.
- **verified: campaign counts** — 3×3×88 = 792; stop 709 + length 83 = 792; prompt_exact_true=792; 45/264 identical RAG answers; window 2026-09-12T18:55:44Z→2026-09-13T05:05:14Z = 10 h 09 m ("about ten hours"); RTX 3090; binomial noise √(0.25/64)=6.25 pp and √(0.25/24)=10.2 pp ("six and ten percentage points").
- **verified: RQ1/RQ2/RQ3 prose numbers** — 0.44–0.75 span; 0.438→0.344/0.313; 0.750→0.469/0.422; 0.672 vs 0.625; groundedness 0.91–0.98; false refusals 25.0%/23.4%/0%; F1 0.005 (0.0053); 102 NON_COVERING_PROVISION; 76 WRONG_INSTRUMENT; F1 0.321/0.434; 71 of 72 probes answered closed-book; 115 hedged-then-answered; Vistral 0 probe refusals in all modes; 90.6/73.4/49.2/38.1 and 89.1/52.4; ≥0.7 gate passed by both retrievers.
- **verified: Conclusion** — 90% doc recall (90.6%), article below 53% (52.4%), 3,703 chunks, 43–49%, ≤0.32 (pooled).
- **verified: cross-place consistency** — no numeric claim carries two different values in two places (abstract vs body vs conclusion vs captions vs comments-with-values: 0.005, 0.32–0.43, 43–49%, 792, 64/24, 63-of-64, 40, 189, 120, 45/264, 3,703, 22, 709/83).
- **verified: citations & refs** — 29/29 cited keys defined in refs.bib; all `\ref` targets defined once; uncited: `thakur2021beir` (F5); `rajpurkar2018squad2_DISABLED` intentionally disabled.
- **verified: narrative examples** — Q006 (gold Art. 52(4) of 46/2024/QH15; model cited Điều 405, 91/2015/QH13) and Q008 (sentinel then substantive answer citing 02/2021/NĐ-CP Điều 14/15) match `narrative_examples` in the tables log; Q059 corroborated indirectly (absent from BM25 `article_miss_ids_at_k3`, so the gold article was in the prompt); the specific Q059 model output (Art. 3 → 61/2025/TT-NHNN) has no entry in the provided JSONs — unverifiable, no contradiction.
