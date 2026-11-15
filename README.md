# RegRAG-VN

A benchmark and evaluation framework for Vietnamese banking and payment regulation. It measures how faithfully small language models (at most 7B parameters) answer regulatory questions under retrieval-augmented generation, scoring citations at article (*Điều*) and clause (*Khoản*) level and abstention on questions the corpus cannot answer.

The corpus is QA-driven. The instruments ingested are exactly those the benchmark questions cite, and a coverage invariant requires every retained question's verbatim gold passage to match an ingested chunk. Ground truth is verifiably present in the retrieval corpus rather than assumed.

Companion paper: "Citation-Level Unfaithfulness of Small Language Models on Vietnamese Banking Regulation: A Provenance-Guarded RAG Benchmark" (IEEE-RIVF 2026); `paper/main.pdf` ships in this deposit.

## Authors

Dinh Thi Lan Huong, Nguyen Huy Hoang, Nguyen Thang Phuc, Vu Duc Thanh, Nguyen Khac Duy Ngoc (Hanoi University of Science and Technology), Thanh Phuong Nguyen (University of L'Aquila).

## Contents

| Path | Contents |
|---|---|
| `data/gold/` | 88 curated questions (64 answerable, 24 unanswerable probes), the canonical JSON derived from them, the citation-override table and its findings document |
| `data/raw_legal/` | Ingested legal texts, redistributed as downloaded, with the URL-to-instrument manifest (`DOC_MANIFEST.json`) and source-verification notes |
| `data/processed_chunks/` | The two-tier corpus: 3,703 chunked Tier-2 provisions and the 64-passage Tier-1 fixture |
| `data/eval/` | The full 792-row generation campaign log (3 models x 3 retrieval modes x 88 questions), retrieval-recall logs and the computed table inputs |
| `data/human/` | The 50-response scorer-validation set and its instructions |
| `regrag/`, `scripts/`, `tests/` | Library, pipeline scripts and tests |
| `paper/` | Manuscript source and PDF |

## Quickstart

```bash
python3 -m venv --system-site-packages .venv
.venv/bin/pip install -r requirements.txt

# canonical load from the trusted QA CSV, with a coverage report
.venv/bin/python scripts/load_qa_csv.py --report

# Tier-1 fixture (64 verbatim gold passages)
.venv/bin/python scripts/build_tier1_corpus.py

# Tier-2 ingestion from data/raw_legal/ (dry run lists what is missing)
.venv/bin/python scripts/build_corpus_chunks.py --dry-run

# regenerate every CSV-derived artifact (idempotent)
.venv/bin/python scripts/regenerate.py

# retrieval recall on Tier 2 (Table III of the paper)
.venv/bin/python scripts/eval_bm25_recall.py --retriever bm25

# Tables I and II from the shipped campaign log
.venv/bin/python scripts/compute_tables.py --out data/eval/tables_recomputed.json

# tests (stdlib unittest)
.venv/bin/python -m unittest discover -s tests -q
```

The dense (BGE-M3) retrieval arm needs a GPU. Generation and embedding both ran on a single RTX 3090 with 4-bit NF4 weights, float16 compute and greedy decoding.

## Provenance discipline

Every chunk, retrieved result, generation and evaluation record carries two tags. `corpus_source` names the tier (`tier1_passages` or `tier2_full`); `retriever_backend` names the backend (`bm25-rank_bm25+pyvi`, `BAAI/bge-m3`, or `DEGRADED:<reason>`). Aggregation refuses rows whose backend is unverified, degraded or mismatched. The guard exists because a silent fallback once produced a plausible-looking dense-retrieval column from a mock; without it an entire experimental condition could be fabricated without warning.

The generation campaign ran on the Tier-1 fixture, whose passage pool contains every gold passage; the paper discloses this as an upper-bound conditioning. Retrieval quality is measured on the full Tier-2 corpus.

## Data corrections

Three gold citations (Q059, Q060, Q061) were corrected after the campaign was scored. `data/gold/citation_overrides.json` pins the corrected values; `data/gold/TT61_TRIPLE_FINDINGS.md` records the evidence. The paper's printed numbers were recomputed from the shipped campaign log under the corrected gold.

## License

CC-BY-4.0. The ingested legal texts under `data/raw_legal/` are redistributed unmodified from official Vietnamese government publications and remain under their original terms.
