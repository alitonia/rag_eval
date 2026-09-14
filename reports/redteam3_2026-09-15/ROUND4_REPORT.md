# Round-4 Red-Team & Audit — RegRAG-VN (IEEE-RIVF 2026, EDAS N35414) — 2026-09-15

Fourth hardening cycle, run on deadline day against commit `86473c4` (unpushed at cycle
start). Protocol: three parallel adversarial lanes + main-thread zero-trust adjudication
(every quantitative claim re-derived from repo data before any edit) + fix cycle + rebuild.

## Lanes

| Lane | Model | Scope | Output |
|---|---|---|---|
| H3 hostile | deepseek-flash | fresh Review-#2 charges, fix-regression hunt, script-logic audit | `laneH3_hostile/FINDINGS.md` (0 BLOCKER / 3 WARN / 6 NOTE + 15 pre-empted) |
| N3 numeric | glm-flash | every number vs ground truth + script re-runs | `laneN3_numeric/FINDINGS.md` (47 VERIFIED / 3 MISMATCH, one root cause / 5 w/ observation) |
| W3 writing/visual | gemini-pro | build, typography, diacritics, bibliography, prose | `laneW3_writing/FINDINGS.md` (1 BLOCKER / 2 WARN / 1 NOTE; horn-fix re-verification PASS; final gate PASS pending) |

## Adjudicated verdicts (main thread; every claim independently re-derived)

### N3-M1 — conditioning split ignored `rag_context_dropped_ranks` — CONFIRMED, FIXED (the round's critical catch)
15 answerable rows carry the gold chunk at retrieval rank 3 with that rank in
`rag_context_dropped_ranks` (context budget never packed it); the round-3 script bucketed
them INTACT because it only read `truncated_ranks`. For 6 rows (Q008 BM25 ×3, Q039 dense ×3)
the gold text is entirely absent from the final prompt — "arrives intact" was false for them.
9 further rows (Q034, Q060) show gold text via a duplicate passage at a clipped rank.
Fixed at the root: `scripts/compute_conditioned_rates.py` now classifies at prompt level
(gold-head-in-final-prompt check; dropped ranks honoured). Corrected cells (sanity gate
unchanged: 94/192, 83/192):
- INTACT 19/57 (33.3%) BM25, 29/84 (34.5%) dense — pooled 48/141 = 34.0%
- TRUNCATED 17/39 (43.6%) BM25, 18/54 (33.3%) dense
- ABSENT 58/96 (60.4%) BM25, 36/54 (66.7%) dense
- χ² intact-vs-absent 10.5 / 13.6 (intact-vs-clipped 1.04 / 0.02, i.e. noise)
- absent/intact ratios 1.81× / 1.93× — "roughly doubles" survives
Paper: RQ2 split sentence, abstract "about 35%"→"about 34%", conclusion "near 35%"→"near 34%",
RQ1 refusal-concentration count 20→21 (absent bucket gained Q008 rows). §III-B's 33/64 and
47/64 are retrieval-level (top-3 chunk-id) claims and remain true; the script now prints both
semantics (prompt-visible: 32/64, 46/64).

### W3-BLOCKER — horn glyph collision — CONFIRMED, FIXED (vnchars v0.3)
v0.2 built ơ/ư with a protruding zero-width `\rlap`, so the horn tick extended into the next
glyph's box ("tư)", "sử+a", "b+ơ+i"). v0.3 tucks the tick inside the base letter's advance
width (`o\kern-.14em\rlap{tick}\kern.14em`): zero net width (no page reflow), no neighbour
contact. Visual re-verification by the W3 lane at ≥400 dpi: PASS on all flagged spots, hooks
unchanged, 6 pages intact.

### H3-W1 — headline described the union as cite-only — CONFIRMED, FIXED
"43–49% … cite an incorrect instrument or non-governing provision" counts the 4-type
unfaithfulness union; UNCITED_ASSERTION rows (no citation at all) are inside it. Re-derived
cite-only (WI∪NC): 79/192 = 41% BM25, 66/192 = 34% dense. Fixes: abstract and conclusion now
say "fail citation-level checking" / "citation-unfaithful"; RQ2 spells out the four types and
adds "wrong or non-covering citations alone account for 41% and 34%".

### H3-W2 — "state the sentinel" false under the paper's own definition — CONFIRMED, FIXED
Of the 80 hedged-then-answered closed-book answerable rows: 0 contain the §III-C sentinel
"Không có trong kho văn bản"; 65 contain the prompted keyphrase verbatim; 15 match only soft
paraphrase templates. Also §III-C's sentinel (gold target) and §IV-B's prompted string are
two different strings, both previously called "the sentinel". Fixes: RQ2 sentence now
"open with refusal language yet answer anyway (65 reproduce the keyphrase verbatim, 15 only
paraphrase it); a keyphrase scorer would credit the verbatim kind"; "sentinel" now reserved
for the gold-target string; §IV-B/§IV-C/Q008 example use "keyphrase".

### H3-W3 — §III-B misdescribed the corpus chunking — CONFIRMED, FIXED
Delivered Tier-2 corpus: 3,122/3,703 chunk ids are per-clause (`…_D52_K1`); the paper claimed
"chunks are articles (Điều), with clause boundaries preserved inside them". The strict
coverage tier accepts either match direction ≥30 chars, and with clause chunks all 63 matches
are chunk-inside-passage. Fixes: §III-B now "articles are chunked at clause (Khoản)
boundaries—one chunk per clause, short articles single chunks"; invariant sentence now states
the either-direction ≥30-char match with the clause-inside-passage reality; §I wording
adjusted.

### H3 NOTEs — all adjudicated
- N4 ("six of 64" BM25-only): FIXED → "six (BM25) and seven (dense) of 64".
- N5 ("sits between" false for dense): FIXED via rewrite ("falls to about one-third … moves
  to 33–44% … rises to 60–67%") — no ordering claim; also moot after N3-M1 re-bucketing.
- N6 (selection confound, no test): FIXED — χ² parenthetical + "the split is selected by the
  retriever's own ranking".
- N7 (3B "genuine reduction" overstated for BM25 arm): FIXED — "keeps a reduction (…),
  unambiguous only in the dense arm" (Wald CIs overlap on BM25, clear on dense).
- N8 (refusals concentrate in absent cells): FIXED — "21 of the BM25 arm's 28 answerable
  refusals occur where the governing text did not reach the prompt" (dense shows no such
  concentration: 6/19, so the caveat is BM25-scoped).
- N9 (Q006 example selective; "fabricated quotation" unprovable): FIXED — the example now
  adds the second error direction ("and later cites the governing instrument under a wrong
  article (Điều 32)"), and "fabricated statutory quotation" → "a statutory quotation that
  appears nowhere in the ingested corpus" (BLDS 91/2015/QH13 is ingested, 869 chunks; the
  quoted fragment occurs 0 times — corpus-verifiable, no longer unprovable).

### First-author email — user-confirmed defect, FIXED
Author block printed `Hoang.NH20251325M@…` (mechanically derived from the SIS ID by commit
f58a659, whose own message records the real address). User confirmed the correct address is
`Hoang.NH251325M@sis.hust.edu.vn`; applied. Co-author addresses remain flagged in KANBAN as
needing one-glance team confirmation (user-side).

### W3 prose WARNs
- "sits between at 33–42%" surgery artifact: fixed (see N5).
- Abstract transition ("Finally, …provenance…"): fixed by merging into the preceding
  sentence (also reclaimed a line).
- Conclusion comma-splice: partially addressed (duplicate RQ3 tail clause removed); the
  summary sentence keeps its metric list by design.
- Number-format WARN (7{,}000 vs 3,703; "six of 64"): dismissed — renders identically /
  intentional style.

## Page budget
Fix cycle initially pushed the paper to 7 pages (three times). Reclaimed ~12+ lines through:
two compressions of the new parentheticals, dropping the §IV-D generic third vulnerability
example, Table II caption methods detail, §II lost-middle sentence compression, §I pricing
clause, one probe-list example, §V-A intro merge, "Model refusal is similarly brittle"
transition, conclusion's duplicated RQ3 caveat, and dropping the Self-RAG sentence + its bib
entry (renamed `_DISABLED` per refs.bib policy). **Final: exactly 6 pages, 0 undefined, 0
overfull.** All corrected numbers verified to render (19/57, 29/84, 33–44%, 60–67%,
10.5/13.6, about/near 34%, 21 of the BM25 arm's 28).

## Numbers changed this round (all script-derived, none hand-entered)
- Conditioned split (prompt-level): 19/57, 17/39, 58/96 (BM25); 29/84, 18/54, 36/54 (dense)
- χ² 10.5 / 13.6; ratios 1.81× / 1.93×; pooled intact 48/141 = 34.0%
- Cite-only unfaithfulness: 79/192 (41%), 66/192 (34%)
- Hedged split: 65 verbatim / 15 paraphrase of 80
- Refusal concentration: 21/28 (BM25); doc-level misses six (BM25) / seven (dense)
- Q006 RAG answer's second citation: 46/2024/QH15 Điều 32

## Surviving known limitations (disclosed or user-side; unchanged from round 3)
Tier-1 generation campaign; 88-row scale; single-expert validation; 83 truncated answers;
no >7B baseline; no precision-trap/cross-jurisdictional probes; Zenodo DOI (user-side,
TODO in tex); Q059–Q061 gold ambiguity (camera-ready); co-author email confirmation
(user-side); κ 30-question scaffold unfilled (disclosed as not performed).

## Lane verification of the fix cycle
W3 lane re-verified the horn fix at ≥400 dpi (PASS ×3 spots) and ran a final page-by-page
gate over the rebuilt PDF (see `laneW3_writing/FINDINGS.md` final sections). Numeric lane's
corrected cells reproduced by the patched repo script (stdout archived in
`laneN3_numeric/`); the patch itself was re-reviewed on the main thread.
