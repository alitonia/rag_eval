"""Dense vector index for legal chunks using multilingual embeddings."""

from typing import List, Optional
from regrag.models import LegalChunk, RetrievedResult

try:
    from sentence_transformers import SentenceTransformer
    import torch
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False


class DenseIndex:
    """Dense embedding index supporting BGE-M3 and multilingual models."""

    def __init__(
        self,
        chunks: List[LegalChunk],
        model_name: str = "BAAI/bge-m3",
        device: Optional[str] = None,
    ) -> None:
        self.chunks = chunks
        self.model_name = model_name
        self.device = device or ("cuda" if HAS_SENTENCE_TRANSFORMERS and torch.cuda.is_available() else "cpu")
        self._model = None
        self._embeddings = None

    def build(self) -> None:
        """Encode all chunks into dense embeddings."""
        if not HAS_SENTENCE_TRANSFORMERS or not self.chunks:
            return

        self._model = SentenceTransformer(self.model_name, device=self.device)
        texts = [chunk.formatted_context() for chunk in self.chunks]
        self._embeddings = self._model.encode(
            texts,
            convert_to_tensor=True,
            show_progress_bar=False,
            normalize_embeddings=True,
        )

    def search(self, query: str, top_k: int = 3) -> List[RetrievedResult]:
        """Retrieve top_k chunks by cosine similarity."""
        if not HAS_SENTENCE_TRANSFORMERS or self._model is None or self._embeddings is None:
            # Fallback mock for non-GPU/test environments
            return [
                RetrievedResult(chunk=chunk, score=1.0 / (i + 1), rank=i + 1)
                for i, chunk in enumerate(self.chunks[:top_k])
            ]

        import torch
        query_emb = self._model.encode(
            query, convert_to_tensor=True, normalize_embeddings=True
        )
        scores = torch.matmul(self._embeddings, query_emb).cpu().tolist()
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
