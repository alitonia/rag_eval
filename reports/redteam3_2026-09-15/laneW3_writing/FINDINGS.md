# Lane W3 Findings

## Build Hygiene
- **PASS**: `main.log` is clean. No undefined citations, no undefined references, no Overfull `\hbox` warnings >3pt, and no "Missing character" warnings for Vietnamese glyphs.

## Diacritics
- **BLOCKER**: Horn diacritics (`ư`, `ơ`) are invisible when followed by another character.
  - *Verbatim text*: `(Thông tư)`, `sửa đổi bởi Nghị định`
  - *Evidence*: Inspected rendered pages 1, 4, and 5. In `(Thông tư)`, the horn on `ư` is completely covered by the closing parenthesis `)`. In the RQ2 quotation (`sửa đổi bởi`), the horns on the `ư` in `sửa` and the `ơ` in `bởi` are overwritten and hidden by the subsequent `a` and `i`. This is because `vnchars.sty` implements `\uhorn` and `\ohorn` with a zero-width `\rlap`, causing the horn tick to collide with whatever immediately follows it.
- **PASS** for hooks (rotated question marks) and dot-below. They render visibly correct at print size without severe collision.

## Prose Quality
- **WARN**: Broken sentence surgery.
  - *Verbatim text*: `sits between at 33--42%`
  - *Evidence*: Section V-C (RQ2), paragraph 1. Leftover words ("between at") from previous edits.
- **WARN**: Inconsistent number formatting.
  - *Verbatim text*: `7{,}000-character context budget` vs. `3,703-chunk Tier-2 corpus`, and `six of 64 questions`.
  - *Evidence*: Section IV-A uses `7{,}000` (which renders exactly as `7,000` in text mode, but implies different LaTeX styling), while Section V-D uses `3,703`. Section V-D also mixes word-and-digit styles (`six of 64`).
- **NOTE**: Run-on sentence feeling slightly LLM-generated.
  - *Verbatim text*: `Citation fidelity remains the critical vulnerability, with 43--49% of RAG answers on answerable questions producing inaccurate or non-governing citations, a rate near 35% even when the source provision reaches the prompt intact, pooled clause accuracy at or below 0.32, and brittle refusal calibration throughout.`
  - *Evidence*: Section VI (Conclusion). This concatenates too many independent metrics into one comma-spliced sentence.

## Abstract Coherence
- **WARN**: The methodology disclosure at the end of the abstract lacks a smooth transition.
  - *Verbatim text*: `...and models frequently emit the refusal sentinel before answering anyway. Finally, a provenance discipline tags corpus tiers and retriever backends...`
  - *Evidence*: Abstract. The text jumps abruptly from RAG failure modes (RQ1/RQ2 findings) to a software engineering/provenance discipline without a bridging clause.

## Tables/Captions
- **PASS**: Table I, II, and III captions remain perfectly accurate. There is no column misalignment, and the caption text does not collide with the top rules.

## Bibliography
- **PASS**: All 28 entries render cleanly. No "in arXiv preprint" artifacts. The `pyvi` and `rank_bm25` entries include the "accessed 2026-09-11" note correctly. There are no missing entry numbers.

## Page-by-page visual
- **PASS**: The layout looks solid across exactly 6 pages. Margins are respected, no lines visibly protrude (confirmed by log check), and there are no glaring orphans/widows in the newly edited paragraphs.

---

### Final Verdict Table
| Category | Status | Worst Finding |
| :--- | :--- | :--- |
| Build Hygiene | PASS | - |
| Diacritics | BLOCKER | Horns on `ư`/`ơ` are covered by subsequent characters due to zero-width `\rlap` in `vnchars.sty` |
| Prose Quality | WARN | Broken sentence surgery (`sits between at 33--42%`) |
| Abstract Coherence | WARN | Abrupt transition to the final provenance sentence |
| Tables/Captions | PASS | - |
| Bibliography | PASS | - |
| Page-by-page visual | PASS | - |

## Horn fix re-verification (v0.3)
- **PASS**: `(Thông tư)` in §I intro. The horn tick on `ư` is now distinctly visible on the top-right shoulder of the `u`, slightly overlapping it as intended, and no longer covered by the closing parenthesis `)`.
- **PASS**: `sửa đổi bởi Nghị định 111/2020/NĐ-CP` in §V-C RQ2 quotation. Both `ử` (in `sửa`) and `ở` (in `bởi`) display their horn ticks perfectly. The ticks are visible, attached correctly to the base letters, and the following characters (`a` and `i`) are safely spaced without any collision. The horns do not render the base letter unreadable. 
- **PASS**: Hooks (ỏ/ủ/ẫ etc.) remain correct, and the document maintains its exact 6-page length without reflow artifacts.

## Final round-4 verification
- **PASS**: Page layout and paragraph reflows. The document remains exactly 6 pages. No visually overfull lines have appeared, and there are no widows or orphans in the heavily reflowed RQ1/RQ2 sections.
- **PASS**: The new RQ2 sentence ("are citation-unfaithful---wrong instrument...") renders cleanly without any odd line breaks around the em-dash or semicolon.
- **PASS**: The chi-square inline math (`$\chi^2{=}10.8/15.3$`) renders correctly with the superscript 2 and no missing glyphs.
- **PASS**: Horn diacritics regression. Both `(Thông tư)` in the introduction and the `sửa đổi bởi Nghị định` quotation in §V-C (formerly §V-B) maintain their correctly rendered, non-colliding horn ticks from the v0.3 fix.
- **PASS**: Bibliography continuity. The self-RAG citation has been successfully removed, leaving 27 contiguous entries with no gaps in the numbering.
- **PASS**: Author block. The first author's email is successfully shortened to `Hoang.NH251325M@sis.hust.edu.vn`. The block occupies exactly three lines with no overflow and renders perfectly.
