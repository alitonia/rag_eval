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

## Round-3 sweep results (2026-10-08 evening, scripts/discover_hf_github_legal.py)

Systematic catalog sweep (10 HF keyword queries + 6 GitHub queries): **98 unique HF
datasets, 26 GitHub repos**. Full listings in reports/ (rerun the script to regenerate).

### Downloaded this round (data/external/, all gitignored)
- **tmquan/thuvienphapluat-vn-vbpl** — CC-BY-4.0, 121 parquet shards: thuvienphapluat
  legal-DOCUMENT corpus, refreshed 2026-09-16. The corpus-expansion backbone.
- **tmquan/thuvienphapluat-vn-hdpl** — license:other — "Hỏi đáp pháp luật" consultation
  Q&A dumps (the user's consultation-idea source, pre-scraped) + embeddings/analytics.
- **tmquan/thuvienphapluat-vn-tnpl** — license:other — "Tình huống pháp luật" case/situation dump.
- **phuocsang/hoidap-thuvienphapluat-200k** — MIT — ~200k thuvienphapluat consultation Q&A pairs.
- **VietTung04/alqac_2025** — ungated mirror of ALQAC 2025 task data: trắc_nghiệm (MCQ),
  tự_luận (essay), đúng_sai (true/false). License unstated on mirror; canonical source is
  the GATED nguyenlab/ALQAC repo (access request required).
- **FinnPham52/vietnamese-legal-claim-verification** — evidence_passages.jsonl +
  verifier train/val jsonl: Vietnamese legal CLAIM VERIFICATION data (trains the
  citation-verification loop of the sequel).
- **hieunguyen1053/vlegal-bench** (GitHub clone, 10.7 MB) — THE VLegal-Bench data
  (absent from HF org CMC-OPENAI): 22 tasks in 5 categories, each folder has task
  .jsonl with ground truth + prompt files. Includes 1.4 Article Recall and 3.1
  Article/Clause Prediction (article/clause-level tasks) and 3.3 Multi-hop Graph
  Reasoning. LICENSE.txt is custom (inspect before any redistribution).

### Verified non-hits / false friends
- **yyyyifan/VLQA** (HF) is a VISUAL-QA dataset (diagram counting; arXiv 2410.00193) —
  acronym collision with the legal VLQA. The legal VLQA (arXiv 2507.19995) remains unreleased.
- **nguyenlab/ALQAC** (HF) is gated: "Access denied. This repository requires approval."
- **ansvn/congbobanan/anle.toaan.gov.vn** — all DNS-fail from this machine; user browser
  fetch required for the judgment/precedent corpus.
- **vbpl.vn** IS reachable with a browser UA (HTTP 200 after 308 redirect, 80 KB portal page);
  api.vbpl.vn does not resolve. Official-metadata channel for the sequel's instrument
  expansion is open (gentle scraping, 20-40 s gaps, per scrape-slowly rule).

### Other notable sweep finds (not downloaded yet, vet before use)
- mlalab/VNLegalText (GitHub, 23 MB) — legal reference/relation extraction dataset
  (cross-reference structure = multi-hop gold ingredient)
- rusano-knn/VietLegalQA (GitHub, 19 MB) — unsupervised cloze-to-natural pipeline,
  113k QA pairs over Vietnamese legal texts
- dthn-anna/ViLegalNLI, thakpl/ViLegalNLI (GitHub) — Vietnamese legal NLI,
  9,600+ premise-hypothesis pairs from 3,000+ documents (groundedness/verification adjacent)
- saladnga/Vietnamese-Legal-Code-Crawler-Semantic-Search — "PhapDien" crawler + vector DB
- noname002/GreenNode-Vietnamese-Law-hn-mined-v2-deduped-10gram — hard negatives mined
  from the GreenNode/Zalo corpus (reranker training material for the sequel)
- niits/vietnamese-legal-ocr — OCR corpus for legal documents
- hdv2709/Vietnamese_Legal_Traffic_Judge_Prediction_QA — traffic judge-prediction QA
- hirine/dataset-van-ban-phap-luat-381K-samples — 381k-sample legal document dump
- th1nhng0/vietnamese-legal-documents — the most-downloaded VN legal corpus (1,320 dl)

### Additional sweep entries worth noting (full-listing tail, 2026-10-08)
- VietTung04/alqac2025-reasoning-trace — reasoning traces for ALQAC 2025 (verification-loop training data)
- GreenNode/Vietnamese-Law-hn-mined-v2 — OFFICIAL hard-negative set mined from the Zalo/GreenNode
  corpus (reranker training material; supersedes the noname002 mirror copy)
- headintheclouds6453/vlsp2025-vietnamese_legal_documents_revision — VLSP 2025 shared-task corpus
- jasong03/vov_phapluat, jasong03/nhandan_phapluat, myduy/vnexpress_plain_text_phap_luat —
  Vietnamese legal-news corpora (real-world phrasing pool for probe arms)

### 7. VLegal-Bench data (hieunguyen1053/vlegal-bench GitHub clone) — verified contents
- 23 jsonl files (22 tasks), 77 MB on disk. LICENSE: **CC BY-NC-ND 4.0** (CMC-OpenAI
  Dataset License Agreement): research use + sharing unmodified OK; NO derivative
  works, NO commercial use, NO redistribution under our name.
  => Sequel consequence: we may EVALUATE models on VLegal-Bench and cite it, but its
  rows must never be merged into our released bundle nor used to build published
  derived training data.
- Task format is MULTIPLE-CHOICE, not generative. Verified samples:
  - 1.4 Article Recall: given a provision locator ("Điểm a Khoản 1 Điều 1 Nghị định
    113/2007/NĐ-CP"), pick the content it defines (4 options).
  - 3.1 Article/Clause Prediction: given a legal question, pick which of four
    (Khoản, Điều, Nghị định) locators governs it — our citation-prediction task in
    MCQ form; directly comparable to RQ2/RQ3 with the generative-vs-MCQ caveat.

### 8. News/official-answer corpora (verified open, 2026-10-08) — user's "government answers in news" idea
- jasong03/vov_phapluat — VOV legal-section news, single parquet, NO license stated
- jasong03/nhandan_phapluat — Nhân Dân legal-section news, single parquet, NO license stated
- myduy/vnexpress_plain_text_phap_luat — VnExpress legal news plain text, 9 jsonl parts, NO license stated
- hdv2709/Vietnamese_Legal_Traffic_Judge_Prediction_QA — Apache-2.0, case-derived judge-prediction QA (traffic domain)
- Not downloaded yet (news corpora are paraphrase-pool material; check provenance/ToS before use)

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
