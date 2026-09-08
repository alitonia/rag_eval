"""Sparse BM25 Index with Vietnamese word segmentation support."""

import re
from typing import List, Tuple
from regrag.models import LegalChunk, RetrievedResult

# Optional import of pyvi for Vietnamese word segmentation
try:
    from pyvi import ViTokenizer
    HAS_PYVI = True
except ImportError:
    HAS_PYVI = False

try:
    from rank_bm25 import BM25Okapi
    HAS_RANK_BM25 = True
except ImportError:
    HAS_RANK_BM25 = False


def tokenize_vietnamese(text: str) -> List[str]:
    """Tokenize Vietnamese text with compound word handling."""
    text_clean = text.lower()
    text_clean = re.sub(r"[^\w\s]", " ", text_clean)
    if HAS_PYVI:
        segmented = ViTokenizer.tokenize(text_clean)
        return segmented.split()
    return text_clean.split()


class BM25Index:
    """BM25 index wrapper for legal chunks."""

    def __init__(self, chunks: List[LegalChunk]) -> None:
        self.chunks = chunks
        self.corpus_tokens = [
            tokenize_vietnamese(chunk.formatted_context()) for chunk in chunks
        ]
        if HAS_RANK_BM25 and self.corpus_tokens:
            self._bm25 = BM25Okapi(self.corpus_tokens)
        else:
            self._bm25 = None

    def search(self, query: str, top_k: int = 3) -> List[RetrievedResult]:
        """Retrieve top_k chunks matching the query using BM25."""
        if not self.chunks:
            return []

        query_tokens = tokenize_vietnamese(query)
        if self._bm25:
            scores = self._bm25.get_scores(query_tokens)
            ranked_indices = sorted(
                range(len(scores)), key=lambda i: scores[i], reverse=True
            )[:top_k]
            return [
                RetrievedResult(
                    chunk=self.chunks[idx],
                    score=float(scores[idx]),
                    rank=rank + 1,
                )
                for rank, idx in enumerate(ranked_indices)
            ]

        # Simple term overlap fallback if rank_bm25 is not installed
        q_set = set(query_tokens)
        scored = []
        for idx, tokens in enumerate(self.corpus_tokens):
            overlap = len(q_set.intersection(set(tokens)))
            scored.append((idx, float(overlap)))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [
            RetrievedResult(
                chunk=self.chunks[idx],
                score=score,
                rank=rank + 1,
            )
            for rank, (idx, score) in enumerate(scored[:top_k])
        ]
