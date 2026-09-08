"""Automated metric extraction for generated model answers.

WARNING: Metrics in this module (particularly correctness_score, hallucinated,
abstained, and abstained_correctly) are heuristic PLACEHOLDERS pending the research
team's final scorer implementation. They must NOT be reported as publishable numbers
in benchmark results or paper tables. All records are tagged with metric_status='placeholder'.
"""

from typing import Dict, Any, List
from regrag.models import EvaluationRecord, GenerationResult, GoldQuestion
from regrag.provenance import CORPUS_UNSET
from regrag.generation.prompts import ABSTENTION_KEYPHRASE
from regrag.evaluation.citation import (
    extract_citations,
    compute_citation_precision_recall,
)


def evaluate_response(
    gen: GenerationResult,
    gold: GoldQuestion,
) -> EvaluationRecord:
    """Evaluate a single generated model response against the gold benchmark question."""
    answer_text = gen.answer_text.strip()

    # Check abstention
    abstained = (
        ABSTENTION_KEYPHRASE.lower() in answer_text.lower()
        or "không có trong tài liệu" in answer_text.lower()
        or "không tìm thấy thông tin" in answer_text.lower()
    )

    # For unanswerable questions, abstaining is correct
    if not gold.is_answerable:
        abstained_correctly = abstained
        hallucinated = not abstained
        correctness = 2.0 if abstained_correctly else 0.0
        prec, rec = (1.0, 1.0) if abstained else (0.0, 0.0)
    else:
        abstained_correctly = False
        # Extract citations from response
        extracted = extract_citations(answer_text)
        prec, rec = compute_citation_precision_recall(extracted, gold.gold_citations)

        # Baseline heuristic for correctness and hallucination
        hallucinated = False
        if abstained:
            correctness = 0.0
        else:
            # If citations match and non-empty
            if rec > 0.0:
                correctness = 2.0 if prec >= 0.5 else 1.0
            else:
                correctness = 0.5
                hallucinated = True if len(extracted) > 0 else False

    return EvaluationRecord(
        question_id=gold.id,
        model_name=gen.model_name,
        retrieval_mode=gen.retrieval_mode,
        is_answerable=gold.is_answerable,
        citation_precision=prec,
        citation_recall=rec,
        abstained=abstained,
        abstained_correctly=abstained_correctly,
        correctness_score=correctness,
        hallucinated=hallucinated,
        corpus_source=getattr(gen, "corpus_source", CORPUS_UNSET),
        retriever_backend=getattr(gen, "retriever_backend", CORPUS_UNSET),
        metric_status="placeholder",
        placeholder_fields=[
            "correctness_score",
            "hallucinated",
            "abstained",
            "abstained_correctly",
        ],
    )
