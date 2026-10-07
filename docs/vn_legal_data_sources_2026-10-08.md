# Vietnamese legal data sources — probe results (2026-10-08)

Probed for the RegRAG-VN Q1 sequel (benchmark expansion + real-world validation slice).
All facts below verified live on 2026-10-08 by direct fetch unless marked otherwise.

## Verified usable now

### 1. Zalo AI Challenge 2021 legal text retrieval
- HF mirror: https://huggingface.co/datasets/GreenNode/zalo-ai-legal-text-retrieval-vn (MIT license)
- Also Kaggle mirror: kaggle.com/datasets/hariwh0/zaloai2021-legal-text-retrieval
- Original portal challenge.zalo.ai requires account login (user would fetch manually)
- 60,701 unique legal documents (~83.5 MB text, avg 1.36k chars, max 253k), 818 queries (788 unique),
  793 qrels, avg 1.006 relevant docs/query (max 2). Relevance is document-level, sparse.
- HF parquet viewer is broken ("Parquet magic bytes not found") — download files directly, not via viewer.

### 2. ALQAC 2024 QA dump ("ViLQA")
- HF: https://huggingface.co/datasets/huyhuy123/ViLQA — open, NOT gated
- 43,588 rows, CSV, fields: ID, ID1, Question, Answer, idx
- Free-text answers "extracted and summarized from legal documents"; Vietnamese regulations as of Aug 2024
- License: research purposes only, commercial use requires author contact
- Tied to: Pham et al., "Top 2 at ALQAC 2024: LLMs for Legal Question Answering" (Int. J. of Asian Language Processing)
- NOTE: no article-level gold columns in this dump; answers must be citation-harvested (our regex machinery) if article gold is needed

### 3. ViBidLQA (bidding-law QA)
- HF: https://huggingface.co/datasets/ntphuc149/ViBidLQA_v1 ; repo github.com/ntphuc149/ViLQA (MIT)
- LLM-synthesized questions from Vietnamese bidding law, validated by legal-domain experts (KSE 2024 paper:
  "Vietnamese Legal Question Answering: An Experimental Study", Nguyen Thu Ha, Truong-Phuc Nguyen et al.)
- Same recipe as our planned provision-first authoring; candidate extra-domain source (bidding law)

## Verified NOT released

### 4. VLQA (arXiv 2507.19995) — the closest to our "consultations as gold" idea
- 3,129 real citizen questions from Vietnamese legal-consultation platforms
- Article-level gold (Law_id + Article_id, e.g. "38/2019/QH14, Article 8")
- Corpus: 59,636 articles from 2,162 documents, 27 domains
- Split 7:1:2 train/val/test
- Paper says "The dataset and source code will be publicly released soon." — NO public repo found on
  GitHub or HuggingFace as of 2026-10-08 (searched both). Preprint is CC BY-NC-SA 4.0.
- Authors: Tan-Minh Nguyen, Hoang-Trung Nguyen, Trong-Khoi Dao, Xuan-Hieu Phan, Ha-Thanh Nguyen, Thi-Hai-Yen Vuong
- Our paper already cites it as nguyen2025vlqa. Worth emailing the authors for pre-release access.

### 5. VLegal-Bench (arXiv 2512.14554, CMC-OpenAI)
- HF org CMC-OPENAI exists (verified) with model CMC-AI-Legal-32B, but ZERO public datasets.
  The "VLegal-Bench" collection holds only the paper + the model. GitHub link in search results 404s.
- 10,450 expert-verified samples claimed in paper; data not obtainable as of 2026-10-08.

## Download + audit results (2026-10-08, scripts/audit_external_datasets.py)

All three downloaded to data/external/ (gitignored, 167 MB total). Full report:
reports/external_data_audit_2026-10-08.md. Headlines:

- **Zalo 2021 is 4x bigger than the HF card stated**: the MTEB test subset showed
  818 queries / 793 qrels, but the full dump holds **3,298 queries with 3,298 qrels**
  (train+test jsonl). Corpus = 61,425 docs, fields (_id, title, text), and the docs are
  ARTICLE units (titles like "Điều 1. Phạm vi áp dụng"). Citation-harvest on 500 sampled
  docs: **500/500 yield (document, article) pairs** through regrag extraction — so
  Zalo qrels are effectively article-level gold pending doc->instrument normalization.
- **ALQAC harvest: 84%** (36,716 of 43,588 answers) yield an (instrument, article)
  pair through regrag extraction. Examples land right in our banking core
  ("...ngân hàng hợp tác xã..." -> 32/2024/QH15 Điều 200; loan-form question ->
  39/2016/TT-NHNN Điều 23). These are candidate gold pending human verification.
- **ViBidLQA**: 3,013 rows (train 1928 / val 482 / test 603), fields (question,
  context, answer), MRC format, contexts are Bidding Law 22/2023/QH15 + decree
  provisions. Apache-2.0. Domain-generalization arm material.
- **Contamination: 0/88** of our benchmark questions appear (exact match) in either
  ALQAC or Zalo queries. Near-duplicate check still owed before any training use.
- Licenses as stated on cards: Zalo mirror MIT; ALQAC research-purposes-only
  (commercial use barred, author contact required); ViBidLQA Apache-2.0. Note the
  Zalo corpus itself is thuvienphapluat-derived, so redistribution in a released
  benchmark needs the same "redistributed as downloaded" treatment as raw_legal.

## Round-2 dig results (2026-10-08, later)

### 6. VLSP Legal Team QA dump — thangvip/vietnamese-legal-qa (HF)
- 9,715 documents x 3 generated QA pairs = 29,145 pairs; fields (doc_name, doc_type_name,
  article_content, generated_qa_pairs{question, answer, question_type, difficulty}, generation_time)
- question_type taxonomy: factual / interpretation / analytical / application; difficulty easy/medium/hard
  — a published precedent for typed-question benchmarks (supports our multi-hop/numeric/trap taxonomy)
- All questions LLM-GENERATED from articles (VLSP Legal Team, 2024) — not human gold, not consultations.
  License vague: "appropriate license for Vietnamese legal documents".

### 7. Court portals — UNREACHABLE from this machine (DNS/connection failure, HTTP 000)
- ansvn.toaan.gov.vn, congbobanan.toaan.gov.vn (judgment publication), anle.toaan.gov.vn (precedents)
- All fail instantly at connection level, same pattern as other blocked .vn hosts. USER ACTION AVAILABLE:
  open these three URLs in a browser and save pages/exports; per established workflow the user fetches
  what CLI cannot. The judgment corpus would feed version-pinned questions + the real-dispute slice.

### 8. duyet/vietnamese-legal-documents-dataset (GitHub)
- Exists but tiny (60 KB, 13 stars, NO license file) — a small scraper dump, not a corpus-scale source.

### ALQAC 2025
- Not yet probed in this round (successor shared task; check NTCIR-18/ALQAC 2025 site for task data).

## Open probes not yet done
- Court judgment portal + án lệ precedent collection (ansvn.toaan.gov.vn family): volumes, structure,
  privacy-scrubbing state — candidate source for version-pinned questions and a real-dispute slice
- thuvienphapluat Q&A section layout/licensing (bot-walled; user fetches manually per established workflow)
- SBV published agency replies (công văn answers) as a small high-precision (question, provision) source
- ALQAC 2025 (successor task) data availability
- Zalo corpus vs VLQA corpus overlap (both appear thuvienphapluat-derived)

## Fit to the sequel plan (q1-sequel-planning memory)
- Real-world question track: ALQAC dump (43.6k, downloadable today) + own consultation mining (VLQA recipe)
- External retrieval validation: Zalo qrels on GreenNode mirror
- Domain-generalization arm: ViBidLQA (bidding) if license/quality checks pass
- Version-pinned + real-dispute instruments: judgment portals (probe pending)
