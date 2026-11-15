# Q059–Q061 gold-citation fix (the Thông tư 61/2025 triple) — 2026-11-16

Status: FIXED. Mechanism: `data/gold/citation_overrides.json` applied by
`regrag/corpus/qa_loader.py::load_gold_questions` (override may only reorder
URL-resolved candidates; it can never invent an instrument). Canonical JSON
regenerated; tier-1 fixture rebuilt; generation log re-scored.

## Defect

Q059, Q060 and Q061 are three questions sharing one gold passage: Điều 3
("Giải thích từ ngữ") of Thông tư 61/2025/TT-NHNN on the operating network of
commercial banks. The loader-derived gold was wrong on two axes for all three:

1. **Wrong instrument (Q059, Q060).** The `doc_link` cell carries two URLs
   (the vanban.chinhphu.vn portal page and `datafiles.chinhphu.vn/.../61-nhnn.pdf`).
   URL resolution returned `["32/2024/QH15", "61/2025/TT-NHNN"]` and, because
   the passage names no instrument ("Trong Thông tư này…"), URL order made the
   2024 Law on Credit Institutions the primary and the gold-citation target.
   But the passage text is verbatim Điều 3 of the circular (network terms:
   mạng lưới hoạt động, chi nhánh, phòng giao dịch, văn phòng đại diện…), and
   the 2024 Law's own Điều 3 ("Áp dụng tập quán thương mại") is unrelated.
   The annotator's reference answers cite "Khoản 3 Điều 3 Thông tư
   61/2025/TT-NHNN" as their legal basis.
2. **Wrong clause (all three).** `extract_gold_citation` takes the FIRST
   `khoản N` match in the passage. In this passage that match is the
   cross-reference "…không thuộc phạm vi quy định tại **khoản 9** Điều này"
   (inside item 10), so all three rows carried `clause_id: "9"` with
   `confidence: "passage-header"`. The governing clauses are 3 (Q059, Q060:
   the Phòng giao dịch definition with the 2-billion-VND lending prohibition)
   and 1 (Q061: the network definition used to classify the proposed off-site
   desk).

Downstream the defect propagated to: the tier-1 chunk `doc_id` labels
(`gold_doc_ids[0]` = 32/2024 under a 61/2025 text — first flagged during the
September 2026 audit of the released logs), every campaign row scored
against the triple, and the RQ2/RQ1 counts derived from those rows.
The paper text was already insulated (the Q059 narrative example was replaced
by a verified Q006 example before submission), but the numbers were not.

## Decision (content-verified gold)

| row | primary instrument | gold citation | row confidence |
|-----|--------------------|---------------|----------------|
| Q059 | 61/2025/TT-NHNN | Điều 3 Khoản 3 | ambiguous-multi-url (unchanged; still true of the URLs) |
| Q060 | 61/2025/TT-NHNN | Điều 3 Khoản 3 | ambiguous-multi-url (unchanged) |
| Q061 | 61/2025/TT-NHNN | Điều 3 Khoản 1 | ambiguous-multi-url (unchanged) |

Notes:

* The second candidate stays in `gold_doc_ids` (the reference answers also
  list the 2024 Law as umbrella legislation; Q061's answer additionally rests
  on Công văn 276/NHNN-TTGSNH, which has no numbered article and therefore
  cannot be a citation gold target).
* The row-level `doc_id_confidence` stays `ambiguous-multi-url` because the
  URL ambiguity itself remains; the override settles which candidate is
  primary, and the citation carries `confidence: "reference-verified"`.
* Gold passages are unchanged (the verbatim 61/2025 text was already correct),
  so tier-1 chunk ids (content hashes) are unchanged and the campaign's
  conditioning structure is untouched.

## Invariants (verified after regenerating)

* **Table III (Gate C) is unchanged by construction**: doc-level recall tests
  membership in the whole `gold_doc_ids` set (same two instruments per row),
  and article-level recall tests `chunk.article_id == "3"` against the same
  set. Confirmed by re-running the BM25 gate locally; the dense arm needs no
  re-run for the same reason.
* 64 answerable + 24 probes unchanged; 63 article-gold rows unchanged
  (Q036 annex exception); 40 clause-gold rows unchanged (clauses 9→3, 9→3,
  9→1 are corrections, not additions).

## What moved in the paper numbers

Re-scored with `scripts/compute_tables.py --out
data/eval/tables_paper_2026-11-16-goldfix.json` (campaign log untouched;
only the gold joined against it changed). Affected printed numbers:
Table II citation P/R/F1 and Khoản accuracy, Table I hallucination rates for
rows whose only hallucination type was `WRONG_INSTRUMENT` under the old gold,
the RQ2 unfaithfulness counts, and the RQ2 conditioned split
(`scripts/compute_conditioned_rates.py`). Section V of the paper was updated
from the new logs; abstract and conclusion carry the new headline numbers.

## Audit commands

```bash
.venv/bin/python scripts/load_qa_csv.py --report          # coverage green, 3 rows corrected
.venv/bin/python scripts/build_tier1_corpus.py            # chunk ids stable, 3 labels fixed
.venv/bin/python -m pytest tests/test_citation_overrides.py -q
.venv/bin/python scripts/compute_tables.py --out data/eval/tables_paper_2026-11-16-goldfix.json
.venv/bin/python scripts/eval_bm25_recall.py              # Table III reproduced identically
```
