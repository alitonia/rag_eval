"""Abstract repository interface for persisting benchmark results.

Fulfills the course requirement of having a unified business logic interface
supported by multiple swappable persistence layers.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from regrag.models import EvaluationRecord, GenerationResult


class BenchmarkResultRepository(ABC):
    """Abstract storage interface for RegRAG-VN benchmark results."""

    @abstractmethod
    def save_evaluation(self, record: EvaluationRecord) -> None:
        """Persist an evaluation record."""
        pass

    @abstractmethod
    def get_evaluation(
        self, question_id: str, model_name: str, retrieval_mode: str
    ) -> Optional[EvaluationRecord]:
        """Retrieve an evaluation record by composite key."""
        pass

    @abstractmethod
    def list_evaluations(
        self,
        model_name: Optional[str] = None,
        retrieval_mode: Optional[str] = None,
    ) -> List[EvaluationRecord]:
        """List evaluations matching the optional filter criteria."""
        pass

    @abstractmethod
    def save_generation(self, result: GenerationResult) -> None:
        """Persist a raw generation result."""
        pass

    @abstractmethod
    def list_generations(
        self,
        model_name: Optional[str] = None,
        retrieval_mode: Optional[str] = None,
    ) -> List[GenerationResult]:
        """List raw generations matching the optional filter criteria."""
        pass

    @abstractmethod
    def export_summary(self) -> Dict[str, Any]:
        """Compute and export high-level metric summaries across all conditions."""
        pass
