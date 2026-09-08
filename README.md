# RegRAG-VN: Measuring Hallucination and Citation Accuracy of Small Language Models on Vietnamese Banking Regulations with RAG

A benchmark and modular evaluation framework for studying hallucination, citation accuracy, and abstention behavior of small open language models ($\le 7\text{B}$) on Vietnamese banking and payment regulations.

## Authors & Group Members
- Đinh Thị Lan Hương (20261261M)
- Vũ Đức Thành (20261082M)
- Nguyễn Khắc Duy Ngọc (20261206M)
- Nguyễn Huy Hoàng (20251325M)
- Nguyễn Thắng Phúc (20252263M)

## Research Questions
- **RQ1:** How much does retrieval-augmented generation reduce hallucination compared with closed-book answering for small LLMs on Vietnamese regulatory questions?
- **RQ2:** How accurately do models cite the supporting article and clause, and do they abstain when the corpus does not contain the answer?
- **RQ3:** How does sparse retrieval (BM25) compare with dense multilingual-embedding retrieval in this domain?

## Project Architecture
- `corpus/`: Ingestion, cleaning, and regex-based Điều/Khoản/Điểm segmentation for SBV circulars.
- `indexing/`: Sparse (BM25 with Vietnamese word segmentation) and dense (BGE-M3 / multilingual embeddings) indexing.
- `retrieval/`: Query retrieval components with top-$k$ recall evaluation.
- `generation/`: 4-bit quantized inference runners (Colab/local) with closed-book and RAG prompting.
- `evaluation/`: Exact citation parser, abstention classifier, hallucination grader, and inter-annotator agreement metrics.
- `storage/`: Two-persistence-layer architecture (In-Memory vs. JSON/CSV) sharing an identical business logic interface.
- `docs/`: Project plan, experimental protocol, and LaTeX report draft.

## vLLM model serving

The benchmark generation models can be exposed through vLLM's
OpenAI-compatible API. Install vLLM separately in a CUDA environment, then
start one model (recommended for a single GPU):

```bash
python scripts/load_vllm_models.py --list
python scripts/load_vllm_models.py --model qwen-7b --gpu-devices 0
```

To keep all five configured models loaded, assign one CUDA device to each
server. They listen on consecutive ports starting at 8000:

```bash
python scripts/load_vllm_models.py --all --gpu-devices 0,1,2,3,4
```

Additional vLLM arguments may be placed after `--`, for example
`-- --max-model-len 4096 --gpu-memory-utilization 0.85`.
