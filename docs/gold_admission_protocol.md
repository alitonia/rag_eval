# Gold-Admission Protocol (RegRAG-VN sequel)

Status: AGREED with the authors, 2026-10-08. This document defines how a row may
enter benchmark gold. It binds every script, lane, and session touching the
dataset until superseded in writing.

## Task-definition rule (read first)

Tier B gold is **authority-cited**: the provision an official decision or reply
cited for the factual situation. It is a documentary fact, mechanically checkable.
It is distinct from "governing provision" (a human judgment). The paper must
describe gold exactly this way. Headline results are computed on BOTH the strict
authored core (Tier C) and the authority-anchored set (Tier A+B); agreement or
disagreement between the two is itself a reported result.

## Tier A — zero-human gold

A row is admissible without any human pass when its label is a structural or
official-by-construction fact:

1. **Án lệ (official precedents).** The precedent's dispositive citations on its
   published fact pattern. Upstream is curated and anonymized; privacy scrubbing
   is inherited, none added.
2. **Version-pinned lookups.** Provision text at a pinned date, checked against
   the corpus `effective_date`/`status`/consolidated-version columns.
3. **Multi-hop chains.** Composed from mirror `parent_acts`/`citations` links,
   each link verified by string match in the corpus.

## Tier B — authority-anchored, dual-model verified, human-audited

Sources: công văn exchanges (mirror `citations` field, 120k+ docs), fetched court
judgments, consultation-track harvests.

Admission requires ALL of:

1. **Mechanical guards** (LLM-free): coverage invariant pass; version guard
   (cited text must exist in the version effective at the anchor document's
   date); citation-extractor agreement with the harvester.
2. **Dual-model consensus**: harvester and verifier are DIFFERENT model
   families; both must agree the provision answers the question and is
   substantive (not procedural boilerplate, not a cross-reference mention).
3. **Confidence triage**: high-confidence consensus auto-admits; disagreement or
   low confidence goes to the human adjudication queue.

Prohibited admissions: rows whose anchor document cites boilerplate only;
"refer to our earlier letter" non-answers; provisions cited in preamble-style
mentions where the substantive content sits elsewhere (unless the preamble is
the answer); any row failing a guard "on average" — guards are per-row.

## Tier C — human-authored core (small, kept)

Precision traps and cross-jurisdiction probes: gold is a judgment call, so
humans author/verify. Traps are mined automatically (numeric diffs between
near-duplicate clauses) with LLM pre-screening; humans confirm. Target 60-80
rows.

## Human-audit obligations (non-negotiable)

- Audit slices totalling >=150 Tier-B rows (or 10%, whichever is greater),
  drawn stratified per source; human agreement with the admission verdict is
  reported as kappa/alpha in the paper.
- One named senior arbiter (Prof. Thanh Phuong Nguyen) resolves disagreements.
- The paper claims "authority-anchored, dual-model verified, human-audited".
  It must NEVER claim "expert-verified" or "expert-annotated" for Tier B.

## License and trust gates

- Every consumed dump must have an entry in `data/external_provenance.json`.
- TRUSTED/RESEARCH-ONLY only for benchmark construction; UNTRUSTED is read-only
  until resolved.
- RESEARCH-ONLY rows: usable as gold/evaluation inside the project, excluded
  from any released training bundle.
- UNTRUSTED (CC BY-NC-ND, licenseless mirrors, news corpora): evaluation-only,
  and only after a per-source license reading recorded in the manifest.
- Court judgments: privacy scrubbing before any redistribution; internal use may
  read the raw text.

## Row provenance (per admitted row)

Every admitted gold row carries: source document id + URL, extraction method,
harvester/verifier model ids + verdicts, guard results, audit status
(auto/audited/adjudicated), and license class. Stored alongside the row, never
in a separate unlinked log.

## Human budget

Projected: ~20-30 hours total (audit slices + adjudication + Tier C confirm).
If a step exceeds this, the step is redesigned (better mechanical guards), not
silently skipped.
