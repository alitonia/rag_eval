"""Citation extraction and verification for Vietnamese legal text."""

import re
from typing import List, Dict, Any, Tuple


# Regex patterns for Vietnamese legal citations
CIRCULAR_PATTERN = re.compile(
    r"(?:Thông\s*tư|TT|Nghị\s*định|NĐ)\s*(?:số)?\s*(\d+[\/\-]\d+[\/\-][A-ZĐa-zđ\d\-]+)",
    re.IGNORECASE,
)
ARTICLE_PATTERN = re.compile(r"Điều\s*(\d+)", re.IGNORECASE)
CLAUSE_PATTERN = re.compile(r"Khoản\s*(\d+)", re.IGNORECASE)


def extract_citations(text: str) -> List[Dict[str, Any]]:
    """Extract circular/decree, article, and clause citations from generated text."""
    citations: List[Dict[str, Any]] = []

    # Find all mentioned legal documents
    docs = CIRCULAR_PATTERN.findall(text)
    articles = ARTICLE_PATTERN.findall(text)
    clauses = CLAUSE_PATTERN.findall(text)

    # If document and article are present, build structured citation objects
    if articles:
        for art in articles:
            doc_id = docs[0] if docs else "UNKNOWN"
            clause_id = clauses[0] if clauses else None
            citations.append({
                "doc_id": doc_id,
                "article_id": art,
                "clause_id": clause_id,
            })
    return citations


def compute_citation_precision_recall(
    predicted_citations: List[Dict[str, Any]],
    gold_citations: List[Dict[str, Any]],
) -> Tuple[float, float]:
    """Compute citation precision and recall at the Article / Điều level."""
    if not gold_citations:
        # If no gold citation was required (e.g. unanswerable question)
        if not predicted_citations:
            return 1.0, 1.0
        return 0.0, 1.0

    if not predicted_citations:
        return 0.0, 0.0

    def to_key(c: Dict[str, Any]) -> Tuple[str, str]:
        doc = str(c.get("doc_id", "")).strip().upper()
        art = str(c.get("article_id", "")).strip()
        return doc, art

    pred_keys = set(to_key(c) for c in predicted_citations)
    gold_keys = set(to_key(c) for c in gold_citations)

    # Check matches (allowing article-only match if doc is UNKNOWN in pred)
    true_positives = 0
    for p_doc, p_art in pred_keys:
        for g_doc, g_art in gold_keys:
            if p_art == g_art:
                if p_doc == "UNKNOWN" or p_doc == g_doc or p_doc in g_doc or g_doc in p_doc:
                    true_positives += 1
                    break

    precision = true_positives / len(pred_keys) if pred_keys else 0.0
    recall = true_positives / len(gold_keys) if gold_keys else 0.0
    return min(1.0, precision), min(1.0, recall)
