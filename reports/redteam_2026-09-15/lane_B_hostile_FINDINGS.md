# Red-team B — hostile Review #2 findings — RegRAG-VN (IEEE-RIVF 2026), paper/main.tex

Severity: BLOCKER = could drive rejection; WARN = will draw reviewer criticism; NOTE = cosmetic.
Every quote grep-verified against the live file, 2026-09-15. 15 findings, most severe first.

---

## F1 [BLOCKER] The conclusion attributes the failure to retrieval granularity; the body's own mechanism says the failure is generation-side
- main.tex:267 — "document-level retrieval reaches 90\% recall while article-level retrieval drops below 53\%, establishing that legal RAG is constrained by statutory granularity before generation begins"
- Contracting statements:
  - main.tex:254 — "even with the governing provision inside the retrieved context, 49\% (BM25) and 43\% (dense) of answered rows still cite a wrong or non-covering provision"
  - main.tex:142 — "citations to incorrect instruments or fabricated provisions reflect model generation failures rather than retrieval omissions"
- Attack: "Your headline conclusion pins the binding constraint on article-level retrieval 'before generation begins', but your own RQ2 result — 43–49% mis-citation with the governing article guaranteed inside the prompt — shows generation fails even when retrieval is erased, so the conclusion contradicts the mechanism the body asserts and the numbers it reports."

## F2 [WARN] The abstract presents Tier-1-fixture upper-bound results as the headline without once saying they are Tier-1, and claims provenance 'prevents' fixture data from corrupting results that are computed on the fixture
- main.tex:53 — "Across a $3\times3\times88$ generation campaign on a single GPU, retrieval augmentation with gold evidence in context raises article-level citation F1 from 0.005 (closed-book) to 0.32--0.43"
- main.tex:53 — "preventing degraded or fixture data from silently corrupting benchmark results"
- main.tex:146 — "the gains over closed-book baselines are an empirical upper bound under evidence conditioning"
- Attack: "The two headline numbers in your abstract come from a curated fixture where the gold passage is guaranteed in the pool — disclosed only in Sec V-A — so a reader of the abstract reads 0.32–0.43 as end-to-end RAG performance; the same abstract claims the provenance discipline 'prevents… fixture data from silently corrupting benchmark results' while Tables I–II are built entirely from fixture data."

## F3 [WARN] RQ1's hallucination-'reduction' claim is entangled with refusal: every refused answerable row mechanically lowers the hallucination rate, and the false-refusal metric is never defined or tabulated
- main.tex:251 — "Qwen2.5-7B falsely refuses 25.0\% and 23.4\% of answerable questions under RAG against 0\% closed-book"
- main.tex:157 — "Halluc.\ = hallucination rate over the 64 answerable questions"
- Attack: "With the hallucination denominator fixed at all 64 answerable rows, a model that refuses 16 of them (25%) lowers its hallucination rate purely by not answering, so your claimed RAG reduction is partly an artifact of switching from answering to refusal — and the 'falsely refuses' metric appears in only one prose sentence with no definition in Sec IV-C and no table."

## F4 [WARN] Scorer validation is selectively reported: only the flattering κ (0.39 hallucination) appears; the correctness κ=0.20 / recall 0.167 and abstention κ=0.62 are omitted, and 'net undercount of five' hides 5 false-positive hallucination flags
- main.tex:127 — "Every correctness and abstention call the scorer makes is confirmed by the expert (3/3 and 10/10), but it misses 15 expert-correct answers and 8 expert-judged abstentions, so its positive calls are exact and its rates conservative. Hallucination flags agree with the expert on 70\% of rows ($\kappa = 0.39$ \cite{cohen1960kappa}) with a net undercount of five on this sample"
- Corroboration (data/eval/scorer_validation_2026-09-15.json): "correct" κ=0.204, auto_recall=0.167 (3/18); "abstained" κ=0.615; "hallucinated" fp=5 → precision 0.815.
- Attack: "You report only the kappa that supports 'mild underestimates'; your own released validation file shows the correctness signal — the very thing your validator was built to check — agrees with the expert at κ=0.20 with recall 0.167 (3 of 18 correct answers found), and 'net undercount of five' papers over the five answers your scorer flagged hallucinated that the expert judged clean, all judged by a single expert on 50 rows."

## F5 [WARN] The only formal definition of the hallucination metric scopes it to closed-book, yet Table I and RQ1 report it for RAG modes
- main.tex:125 — "(ii)~\emph{hallucination rate}, identifying statements that contradict statutory text or introduce unsupported assertions in closed-book mode"
- main.tex:157 — "Halluc.\ = hallucination rate over the 64 answerable questions" (caption covering RAG rows 0.344/0.313/…)
- Attack: "Your metric definition limits hallucination to closed-book mode, but Table I and the entire RQ1 subsection deploy the same rate for RAG-BM25/RAG-Dense rows; either the definition is wrong or the RAG numbers measure something else you never define."

## F6 [WARN] 'Identical answers in only 45 of 264' is incompatible with 'trivially perfect… indistinguishable' and 'sole experimental variable' if the top-3 sets match — but if they differ, the difference is content, not 'prompt ordering'
- main.tex:147 — "the two configurations yield identical answers in only 45 of 264 shared instances"
- main.tex:103 — "retrieval recall on it is trivially perfect and sparse and dense retrievers are indistinguishable"
- main.tex:119 — "the top-3 retrieved passages are concatenated into the prompt with identical formatting, isolating retrieval representation as the sole experimental variable"
- Attack: "If both retrievers place the same gold chunk in an identically formatted prompt, greedy decoding should reproduce answers far more than 45/264 times; if the filler chunks differ, generation differences are retrieval-content differences mislabelled 'prompt ordering' — you never report the two arms' top-3 set overlap to arbitrate which."

## F7 [WARN] The 63-verbatim + 1-annex + 1-transferred arithmetic does not reconcile with 64 answerable rows as written
- main.tex:99 — "63 of the 64 passages consist of verbatim article text substituted under a guarded repair procedure… Of the remaining rows, one cites a \emph{Phụ lục} annex rather than a numbered article and is retained as an annotator summary, while another whose governing instrument is absent was transferred to the unanswerable probe arm"
- Attack: "63 substituted plus one annex row already exhausts the 64, so 'another row was transferred to the probe arm' implies a 65th answerable row that the 88-row count never accounts for; as written the sentence invites the reading that the transferred row is inside the 64, making the counts sum to 65."

## F8 [WARN] 10.5% of answers (83/792) are truncated at the 512-token cap and scored as-is, with no analysis of how truncation interacts with citation/abstention scoring
- main.tex:138 — "709 answers finish naturally and 83 hit the token cap and are analysed as generated"
- Attack: "A truncated answer that never reaches its citation scores as no-citation and a truncation before the refusal sentinel misreads as a refusal, so Table II's closed-book 0.005 F1 and the abstention column depend on how the 83 capped answers split across cells — a distribution you never report."

## F9 [WARN] The conclusion converts recall@3 into unqualified 'recall', and the "≥0.7 retrieval gate" is asserted with no definition or precedent
- main.tex:267 — "document-level retrieval reaches 90\% recall while article-level retrieval drops below 53\%"
- main.tex:259 — "passing the $\geq 0.7$ retrieval gate"
- Attack: "Table III's 90.6%/52.4% are recall at k=3, yet the conclusion states them as unqualified recall; the ≥0.7 gate appears once in prose with no derivation, citation, or statement of what failing it would have changed."

## F10 [WARN] RQ3 reads a 3.2 pp ranking 'reversal' as a finding inside the paper's own declared ~6 pp binomial noise, and asserts a retrieval bottleneck is 'consistent with' RQ2 numbers that were measured with retrieval removed
- main.tex:259 — "reverses the article-level ranking at $k{=}3$ (52.4\% against BM25's 49.2\%)"
- main.tex:259 — "this retrieval bottleneck bounds the citation ceiling of downstream generation, consistent with the mis-citation rates observed in RQ2"
- main.tex:138 — "binomial noise is on the order of six and ten percentage points respectively, so we report point estimates without significance tests and read small differences between cells cautiously"
- Attack: "By your own noise estimate (~6 pp at n=63) a 3.2 pp gap is within chance, so 'reverses the ranking' over-reads the data; and RQ2's 43–49% mis-citation was produced with the governing article guaranteed in the prompt, so a retrieval bottleneck cannot logically be 'consistent with' numbers that exclude retrieval."

## F11 [WARN] Mis-citation counts use a 192-row denominator while the same table's scorable set is 189 (Q036 has no article gold), so the counts are not reproducible from the tables
- main.tex:254 — "102 of 192 answered questions asserting a provision that does not govern the question and 76 citing an instrument other than the governing one"
- main.tex:183 — "P and R are averaged per row over the 189 scorable answerable rows (63 questions $\times$ 3 models; one annex-citing question has no article gold)"
- Attack: "For the annex question there is no gold article, so 'asserting a provision that does not govern the question' is undefined for those rows; the 192-based prose counts and the 189-based table cannot both be right, and the 102/76 counts appear in no table."

## F12 [WARN] The availability section claims a permanent Zenodo DOI 'established at submission' that the source itself marks as an unfilled TODO, and names no repository URL
- main.tex:272 — "The RegRAG-VN benchmark, pipelines, evaluation suites, and full experimental logs are available in our public repository, with a permanent Zenodo archive and DOI established at submission."
- main.tex:270 — "% TODO(results): insert the Zenodo DOI here at submission; the record must be"
- Attack: "No DOI string and no repository URL appear in the manuscript; the immediately preceding source comment says the DOI still has to be inserted, so 'established at submission' is an availability claim a reviewer cannot verify and could reject on reproducibility grounds."

## F13 [NOTE] No empirical comparison against any cited Vietnamese legal resource, and the gap claim is an unfalsifiable 'we did not find one' with no search protocol
- main.tex:88 — "Within these resources we did not find one that couples article-level citation scoring and unanswerable probes with a corpus whose coverage of the governing provisions is verified; that conjunction is the one RegRAG-VN occupies"
- Attack: "You cite VLQA, VLegal-Bench, ViLegalLM, and Nguyen Ba et al. but never run them or report their sizes, so the claimed novelty rests on an undocumented negative search rather than on any measured gap."

## F14 [NOTE] F1 'of the pooled P and R' (micro-style construction) with per-row-averaged P/R is an unusual construction, and per-row multi-citation scoring is never specified
- main.tex:183 — "F1 is the harmonic mean of the pooled P and R"
- Attack: "Pooled harmonic-mean F1 from row-averaged precision/recall is not the macro F1 a reader expects, and nothing in the paper says how an answer citing several articles (one correct) is scored per row."

## F15 [NOTE] The gold CSV the 88-row benchmark rests on is flagged 'still under review' in the source, so the headline row counts are not final
- main.tex:98 — "% camera-ready, the CSV is still under review."
- Attack: "If the gold CSV changes after review, every table changes with it; the paper should either freeze the dataset description or state the review status instead of asserting final counts."

---

## Sections that withstood attack (no finding)
- Related Work: citation-integrity comments are thorough; no invented refs spotted (could not verify online; bib claims two rejected identifiers were replaced, which is a positive practice).
- Table I / Table II arithmetic: internally consistent (709+83=792; pooled-F1 checks out: 2·0.293·0.354/0.647≈0.321; 2·0.399·0.476/0.875≈0.434).
- The Tier-1 disclosure itself (Sec V-A), the probes limitation (no precision-trap, no cross-jurisdiction), and the non-measured inter-annotator agreement (Sec III-D) are honestly stated — the problems above are what the disclosure does NOT control: abstract framing, metric scope, denominator hygiene.