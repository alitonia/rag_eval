"""Core data models for RegRAG-VN."""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional


@dataclass
class LegalCitation:
    """Represents a formal citation to a Vietnamese legal provision."""
    doc_id: str             # e.g., "18/2024/TT-NHNN"
    article_id: str         # e.g., "15" (Điều 15)
    clause_id: Optional[str] = None  # e.g., "2" (Khoản 2)
    point_id: Optional[str] = None   # e.g., "a" (Điểm a)

    def to_citation_string(self) -> str:
        parts = []
        if self.point_id:
            parts.append(f"Điểm {self.point_id}")
        if self.clause_id:
            parts.append(f"Khoản {self.clause_id}")
        parts.append(f"Điều {self.article_id}")
        parts.append(self.doc_id)
        return " ".join(parts)


@dataclass
class LegalChunk:
    """A granular chunk of a legal document (segmented at Khoản / Clause level)."""
    chunk_id: str
    doc_id: str             # e.g., "18/2024/TT-NHNN"
    doc_title: str          # Title of the Circular/Decree
    chapter: Optional[str]  # e.g., "Chương II"
    article_id: str         # e.g., "14"
    article_title: str      # e.g., "Hạn mức giao dịch thẻ"
    clause_id: Optional[str] = None
    text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def formatted_context(self) -> str:
        """Context string with legal hierarchical header for retrieval."""
        header = f"[{self.doc_id}] Điều {self.article_id}. {self.article_title}"
        if self.clause_id:
            header += f" (Khoản {self.clause_id})"
        return f"{header}\n{self.text}"


@dataclass
class GoldQuestion:
    """A curated question in the 100-question benchmark set."""
    id: str                 # e.g., "Q001"
    question: str
    is_answerable: bool
    gold_doc_ids: List[str] = field(default_factory=list)
    gold_citations: List[Dict[str, Any]] = field(default_factory=list)
    reference_answer: str = ""
    category: str = "factual"  # "factual", "synthesis", "definition", "unanswerable"


@dataclass
class RetrievedResult:
    """Retrieved document chunk with score and rank."""
    chunk: LegalChunk
    score: float
    rank: int


@dataclass
class GenerationResult:
    """Model output for a given question and retrieval configuration."""
    question_id: str
    model_name: str
    retrieval_mode: str     # "closed_book", "rag_bm25", "rag_dense"
    prompt: str
    raw_response: str
    answer_text: str
    extracted_citations: List[Dict[str, Any]] = field(default_factory=list)
    abstained: bool = False


@dataclass
class EvaluationRecord:
    """Evaluation metrics for a single generation output."""
    question_id: str
    model_name: str
    retrieval_mode: str
    is_answerable: bool
    citation_precision: float = 0.0
    citation_recall: float = 0.0
    abstained: bool = False
    abstained_correctly: bool = False
    correctness_score: float = 0.0  # 0.0, 1.0, 2.0
    hallucinated: bool = False
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
