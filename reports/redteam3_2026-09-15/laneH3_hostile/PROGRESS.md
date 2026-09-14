# Lane H3 (hostile Reviewer #2) — Round-3 red-team — PROGRESS

Round-4 hardening pass for IEEE-RIVF 2026 submission (EDAS N35414).
Read-only except this dir. Read ROUND2_REPORT.md to avoid re-reporting fixed items.

## Plan / checklist

- [x] P0. Read paper/main.tex in full (277 lines); see lines 1–138 + 139–277.
- [x] P0b. Read ROUND2_REPORT.md (prior fixes: Tier-1 conditioning, Q059→Q006, strict=False, budget, refusal artifact, 0.7 floor, κ labels, ceiling inference, Q036 invariant, 6/64 misses, 80/192, 45/264 etc.)
- [x] P0c. Read refs.bib + vnchars.sty header (bib integrity policy in comments).
- [x] P1. Read round-3 scripts: compute_conditioned_rates.py, verify_tier1_conditioning.py, compute_tables.py, regrag/evaluation/metrics.py, run_campaign_pod.py, regenerate.py, build_corpus_chunks.py, abstention.py, config.py, qa_loader.py.
- [x] P2. Re-run compute_conditioned_rates.py (read-only) — verified 23/66, 31/90, 14/33, 17/51, 57/93, 35/51; gates 94/83; refusal cells.
- [x] P3. Independently recomputed conditioned split + refusal counts (7B 16/15, 3B 10/4) + hedged 80/192 (65 exact-keyphrase + 15 soft-only) + 71/72 probes.
- [x] P4. Verified RQ2 closed-book 102 (NON_COVERING) / 76 (WRONG_INSTRUMENT); cite-only vs 4-type union per arm (79/66 vs 94/83).
- [x] P5. Verified answered-row hallucination rates 0.458/0.408 (7B), 0.762→0.556/0.450 (3B), Vistral 0.672/0.694/0.594.
- [x] P6. Verified Q006 (closed+RAG) and Q008 examples verbatim from generations.json + scorer types; Q006 fabricated-quote = 0 corpus hits (consistent only).
- [x] P7. Verified 45/264 identical; 709/83 truncation; 447/528 clipped, 240 dropped, 7085 max/7000 budget; 792 prompt-exact; window 10.16h; model blocks contiguous; RTX 3090; NF4+float16; seed/temp/max_tokens.
- [x] P8. Verified scorer validation (50 rows, 3/3, 10/10, fn 15+8, fp 0/0/5, κ 0.2038/0.3863/0.6154).
- [x] P9. Verified Tier-2 3,703 chunks / 22 instruments / Table III cells / BM25 6 misses vs dense 7 misses; per-clause chunking (3,122/3,703).
- [x] P10. Verified dataset claims: 63/64 strict coverage (Q036 not-found), 40 Khoản golds, Q036 annex, Q037 probe, 63 article gold, 64 source URLs; invariant direction 63 chunk-in-passage / 0 passage-in-chunk.
- [x] P11. Internal-consistency sweep: all \refs resolve; abstract/RQ2/conclusion conditioned numbers consistent; term drift "mis-citation" vs "citation mismatch" noted inside H3-W1.
- [x] P12. Methodology attacks: selection confound, small cells, no test (χ² computed), refusal-artifact soundness (3B BM25 CIs overlap), causal wording.
- [x] P13. Write FINDINGS.md (3 WARN + 6 NOTE, 0 BLOCKER; PRE-EMPTED list; UNCHECKABLE list).

## Result (final)
see FINDINGS.md — verdict table, detailed findings with verbatim quotes + recipes, PRE-EMPTED.