# Lane N3 — numeric consistency audit — PROGRESS

- [x] Paper main.tex read in full (277 lines)
- [x] Scripts verify_tier1_conditioning.py / compute_conditioned_rates.py read
- [x] Scripts re-run with venv python (stdout archived)
- [x] Ground-truth JSONs read (tables_paper, scorer_validation, both recall JSONs, repair log)
- [x] generations.json row-level checks (Q006 verified; 792 rows; 709/83; 45/264; hedge 80+35)
- [x] Independent conditioning recount — found 9+6 GOLD_DROPPED rows misbucketed INTACT
- [x] Text-level prompt audit (spotcheck_n3b) — 6 rows zero gold text, 9 clipped prefix
- [x] Corrected text-level rates computed (19/57, 29/84; clipped 42.9%)
- [x] Per-number verdicts drafted (3 MISMATCH, 1 root cause; 47 VERIFIED; 5 w/ observation)
- [x] FINDINGS.md written
