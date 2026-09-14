# laneN2 numeric re-audit — PROGRESS

Target: /mnt/data/seminar_2/paper/main.tex (278 lines, read in full incl. re-read of lines 124-142 after display truncation).

Ground truth read in full:
- data/eval/tables_paper_2026-09-13.json  [DONE]
- data/eval/scorer_validation_2026-09-15.json  [DONE]
- data/eval/bm25_recall_gate_c_2026-09-11.json  [DONE]
- data/eval/dense_recall_gate_c_2026-09-13.json  [DONE]
- data/eval/generations.json (7.6 MB, 792 rows) — spot-check script in this dir.

Status: COMPLETE — FINDINGS.md written.

- [x] main.tex read in full (278 lines; 124–142 re-read after display truncation)
- [x] 4 small JSONs read in full
- [x] generations.json spot-check: 792 rows, 264×3 models/modes, 88 questions; finish_reason/seed/temp fields ABSENT from rows (backed by tables JSON / run_campaign_pod.py instead)
- [x] Scorer re-run (regrag.evaluation.metrics.detect_abstention) on closed-book rows: hedged ALL 115 = answerable 80 + probes 35 → paper's "115 of the 192" is a MISMATCH (denominator)
- [x] Table I Abst column re-derived from raw rows via scorer: 1/12/9/3, rest 0 — exact match
- [x] md5 of paper/IEEEtran.cls = 5b2e4fa15b0f7eabb840ebf67df4c0f7 — matches header comment
- [x] seed 1234 / temp 0 / 512 tokens corroborated in scripts/run_campaign_pod.py SamplingConfig
- [x] Gold probe reference_answer = "Không có trong kho văn bản" (24/24) — §III-C correct; prompt keyphrase "THÔNG TIN KHÔNG CÓ TRONG TÀI LIỆU" is the other registered exact-tier string

Verdict: 96 VERIFIED, 1 MISMATCH (main.tex:254 "115 of the 192" → 115 is over 264 rows; answerable-only = 80), 6 UNVERIFIABLE-in-JSONs.
