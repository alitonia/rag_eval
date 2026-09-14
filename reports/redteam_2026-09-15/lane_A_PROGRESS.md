# Numeric-consistency audit — 2026-09-14T17:49:38Z
Reading main.tex + 4 JSON sources + refs.bib
- 17:54:22Z main.tex changed UNDER AUDIT (mtime 2026-09-15 00:51+0700); 1.8x/1.7x sentence no longer present; snapshot taken md5 below; auditing snapshot
36a1add849b8dc0e0af084d909a991b3  /mnt/data/seminar_2/paper/main.tex
- 17:56Z Read tables_paper_2026-09-13.json (Table I/II source), scorer_validation_2026-09-15.json, bm25_recall_gate_c_2026-09-11.json, dense_recall_gate_c_2026-09-13.json, refs.bib in full.
- 17:57Z Table I: 27/27 cells match JSON (rounding half-up verified, e.g. 0.4375->0.438, 0.0417->0.042). Table II: 12/12 cells match; F1=harmonic mean re-derived (0.3209, 0.4341); 189=63x3, 120=40x3 confirmed.
- 17:58Z Table III: all 8 cells re-derived from hit counts (47/64, 58/64, 24/63, 31/63; 46/64, 57/64, 23/63, 33/63); denominators n=64 doc / n=63 article, Q036 excluded in both logs; corpus_chunk_count=3703, instrument_count=22.
- 17:59Z Sec IV-C scorer validation: 50, 41/9, 3/3 (tp3 fp0), 10/10 (tp10 fp0), fn15, fn8, agreement 0.70, kappa 0.3863->0.39, net undercount fn10-fp5=5. ALL MATCH.
- 18:00Z Campaign: 3x3x88=792; stop709+length83=792; prompt_exact_true=792; 45/264 identical; window 18:55:44Z->05:05:14Z = 10h09m30s ~= "about ten hours". MATCH.
- 18:01Z RQ1/RQ2/RQ3 prose: all percentages re-derived (94/192=49.0%, 83/192=43.2%, 102, 76, 71/72, 115, 90.6/73.4/49.2/38.1, 89.1/52.4). Denominator-label issue found ("answered rows" vs 192 answerable). Clause-acc ceiling 0.317 holds pooled only (per-cell 0.375 exists in log).
- 18:02Z Citations: 29 cited keys all defined in refs.bib; all \ref targets defined; uncited: thakur2021beir (live), rajpurkar2018squad2_DISABLED (intentional). fig:pipeline never \ref'd. "assertion gate" never defined in IV-C.
- 18:03Z Arithmetic: 0.906/0.492=1.842, 0.891/0.524=1.700 (ratios removed from current rev by concurrent edit, were correct); binomial noise 6.25pp/10.2pp ~= "six and ten"; py round(0.3545,3)=0.354 matches Table II.
- 18:04Z Wrote FINDINGS.md (10 findings, 0 BLOCKER / 2 WARN / 8 NOTE). Audit base = snapshot md5 36a1add849b8dc0e0af084d909a991b3.
