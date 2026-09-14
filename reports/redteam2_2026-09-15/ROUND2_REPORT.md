# Round-2 Red-Team & Audit — RegRAG-VN (IEEE-RIVF 2026, EDAS N35414) — 2026-09-15

Post-v1.0.0 deep audit, run on deadline day against commit `5a0ad43`.
Protocol: thesis-audit skill (Reviewer #2 mode), 3 adversarial lanes + main-thread
adjudication + conditioned re-analysis + fix cycle + verification pass.

## Lanes

| Lane | Model | Scope | Output |
|---|---|---|---|
| H2 hostile | deepseek-flash | fresh Review-#2 charges + fix-regression hunt | `laneH2_hostile/FINDINGS.md` (2 BLOCKER / 8 WARN / 3 NOTE) |
| N2 numeric | glm-flash | every number vs the 5 ground-truth JSONs | `laneN2_numeric/FINDINGS.md` (96 VERIFIED / 1 MISMATCH / 6 UNVERIFIABLE) |
| W2 build/writing | gemini-pro | build, figures, diacritics, bibliography, prose | `laneW2_writing/FINDINGS.md` (incl. diacritics A/B) |
| executor | — | vnchars.sty arm-B glyph application | vnchars v0.2 + rebuild |

## Adjudicated verdicts (main thread, every claim re-derived from the logs)

### BLOCKER-1 — Tier-1 conditioning premise false — CONFIRMED, FIXED
Independent join (`scripts/verify_tier1_conditioning.py`): gold Tier-1 chunk absent from the
retrieved top-3 in **93/192 (48.4%) BM25** and **51/192 (26.6%) dense** answerable rows;
text-level check agrees exactly (144/384 prompts lack the gold passage head). Per question:
gold in top-3 for 33/64 (BM25) and 47/64 (dense).
Falsified claims removed: §III-B "retrieval recall on it is trivially perfect"; §V-A "Both
BM25 and dense retrieval locate the target passage"; abstract/RQ2/conclusion
"even with the governing provision in the prompt" as a blanket qualifier.
Replacement: conditioned split computed with the repo scorer itself
(`scripts/compute_conditioned_rates.py`, sanity gate reproduced 94/192 and 83/192 exactly):
mis-citation **~35% with gold intact** (23/66 BM25, 31/90 dense), 33–42% when clipped by the
7,000-char budget, **61–69% when absent**. The phenomenon survives conditioning; the paper
now says precisely that.

### BLOCKER-2 — Q059 example unsupportable — CONFIRMED, REPLACED
Q059's three retrieved chunks all carry TT 61/2025-style circular text ("trong Thông tư
này"), including the two chunks *labeled* 32/2024/QH15 (a law); canonical gold is
`doc_id_confidence: ambiguous-multi-url` between the two instruments. The model cited
exactly the text it was reading. Replaced with **Q006 under RAG-BM25 (Vistral-7B)**:
gold Article 52(4) of the 2024 Notarization Law verbatim-intact in the prompt,
substantively correct answer, opens by citing "Điều 52 của Nghị định 23/2015/NĐ-CP" —
right article number, wrong instrument (verified from `generations.json` + scorer types
WRONG_INSTRUMENT/NON_COVERING_PROVISION, correctness ≥ 1.0, gold INTACT).

### WARN-3 (strict=False) — CONFIRMED, FIXED
`tables_paper_2026-09-13.json` carries `metric_status: "unvalidated (aggregated
strict=False)"`; `compute_tables.py` admits the gate "would rightly refuse these rows" while
its docstring falsely claims "the paper's §V carries the same disclosure". Now disclosed in
§IV-C (validation post-dates the campaign; strict=False in the log) and §IV-D ("built to
refuse" + relaxed-gate disclosure). Contribution (iii) wording "guarantees" → "tags and gates".

### WARN-4 (7,000-char budget) — CONFIRMED, FIXED
`rag_context`: truncated_rows 447 / rows 528, dropped 240, max_chars 7085. Now stated in
§IV-A; "sole experimental variable" claim replaced with "only factor varied by design,
though the budget's clipping depends on each retriever's ranking".

### WARN-5 (RQ1 refusal artifact) — CONFIRMED, FIXED
Answered-row hallucination rates (computed via the repo scorer): Qwen2.5-7B
0.438→0.458/0.408 — **indistinguishable from closed-book**; the aggregate reduction is
refusal-driven (16/15 false refusals). Qwen2.5-3B keeps a real reduction (0.762→0.556/0.450).
RQ1 header and body rewritten; 3B refusal rates (15.6%/6.3%) added.

### WARN-6 (0.7 floor, "within sampling noise") — CONFIRMED, FIXED
The 0.7 constant exists nowhere in the harness (only a "gate":"C" log label) — deleted.
"3.2-point gap within sampling noise" → "a two-question difference, 33 versus 31 of 63,
that this sample size cannot resolve".

### WARN-7 (κ labelling) — CONFIRMED, FIXED
"Expert agreement" → "Scorer--expert agreement"; "its positive calls are exact" scoped to
correctness and abstention (hallucination fp=5 disclosed on the next line).

### WARN-8 (ceiling inference) — CONFIRMED, FIXED
Conclusion/RQ3 now state the assumption: "unless a model cites correctly from parametric
memory … caps end-to-end citation well below the conditioned rates".

### WARN-9 (Q036 invariant overstatement) — CONFIRMED, FIXED
Abstract now says "aligned with the questions by an exact-match coverage invariant"
(no per-question claim); §III-B invariant sentence carries the annex exception.

### WARN-10 — merged into BLOCKER-1's conditioned split.

### NOTE-11 ("nearly solved") — FIXED: "strong but incomplete, with six of 64 questions
retrieving no chunk of the governing instrument at k=3" (58/64 ⇒ 6 misses).

### NOTE-12 (rejection path never fired) — PARTLY REFUTED + FIXED: zero `DEGRADED:` row
tags (verified), but the ingest-level rejection *did* fire (Tier-2 re-ingest rejected on
duplicate chunk ids) — now stated in §IV-D.

### NOTE-13 (Tier-1 framing) — FIXED via the same §IV-D sentence; dense gate log confirms
`corpus_source: tier2_full` for Table III.

### N2-MISMATCH — "115 of the 192 closed-book answerable rows" — CONFIRMED, FIXED
115 is hedged-then-answered over ALL 264 closed-book rows (compute_tables.py has no
answerable filter); answerable-only count is **80** (glm re-ran `detect_abstention`:
80 + 35 probes = 115). Fixed to "Another 80 of the 192".

### W2 build findings — CONFIRMED, FIXED
- **Diacritics**: vnchars v0.1 hook (raised 'r') judged unacceptable at print size; A/B test
  (gemini, 300 dpi, native-reader criteria) chose arm B decisively. Applied as **vnchars
  v0.2**: hook = rotated `\textquestiondown`, horn = `\textquoteright`. Final visual
  verification in `laneW2_writing/FINDINGS.md` §9.
- "W. tau Yih" garble → `{Wen-tau}` braces in 3 entries (verified in built PDF).
- `bohnet2022attributed` rendered "in arXiv preprint" → converted to @article; later the
  citation itself was dropped (page budget; rashkin2023attribution carries the point) and
  the entry is now absent from the reference list.
- PyVi/rank_bm25 missing years → `note = {accessed 2026-09-11}` (no fabricated years).
- Author-block 3.4pt overfull → emails reflowed 2/2/1 across 3 lines.
- 88-word metrics sentence split; 57-word Tier-1 sentence restructured.

## Page budget
Fix cycle initially pushed the paper to 7 pages (+~26 lines of disclosure text).
Reclaimed through: redundancy trims across all new passages, venue abbreviations
(Proc. EMNLP/ACL/ICLR/AAAI/EACL/COLING, Findings of ACL 2026, Trans. ACL, ACM Comput.
Surv., etc.), dropping the bohnet citation, and caption/comment tightening.
**Final: exactly 6 pages, 0 undefined citations/references, 0 overfull boxes.**

## Numbers added this round (all from repo-tracked scripts, not hand-entered)
- 93/192, 51/192 absent; 33/64, 47/64 per-question top-3 presence
- Conditioned mis-citation: 23/66, 31/90 (intact ~35%), 14/33 & 17/51 (33–42% clipped),
  57/93 & 35/51 (61–69% absent)
- Answered-row hallucination: 0.458/0.408 (7B), 0.556/0.450 (3B), 0.694/0.594 (Vistral)
- False refusals: 15.6%/6.3% (3B)
- Context budget: 7,000 chars, 447/528 clipped, 240 dropped
- Hedged-then-answered answerable: 80/192
- Six of 64 doc-level misses; 33 vs 31 of 63

## Surviving known limitations (disclosed in-paper, unchanged)
Tier-1 generation campaign; 88-row scale / binomial noise; single-expert validation;
83/792 truncated answers scored as-is; no frontier >7B baseline; no precision-trap or
cross-jurisdictional probes; Zenodo DOI TODO (user-side); Q059–Q061 gold ambiguity
(recommend resolving before camera-ready — its rows remain in the scored set).

## Verification
Final build re-inspected page-by-page by the W2 lane (image-capable): see
`laneW2_writing/FINDINGS.md` §9. Invariants: 6 pp, 0 undefined, 0 overfull >3pt.

## Round-1 delta
All 15 round-1 findings re-checked: 12 FIXED (5 re-verified in text this round), 3
NOTE-level residuals confirmed still-note-level (F13 unfalsifiable-gap phrasing retained
with the four verified VN citations; F15 CSV-under-review is a source comment only; F12
Zenodo DOI remains user-side).
