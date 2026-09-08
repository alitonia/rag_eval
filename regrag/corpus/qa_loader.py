"""Loader from the trusted QA CSV to canonical GoldQuestion objects.

This is the single place the CSV is interpreted, so that a revised CSV (review
is still in flight) regenerates every downstream artifact identically. Nothing
else in the codebase should call csv.DictReader on the gold file.

Design is driven by four measured properties of the CSV:
  * 64/64 passages name an ``Điều``  -> article-level gold always derivable
  * 24/64 passages contain "Khoản N"  -> clause-level gold is optional
  * only 5/64 preserve line-initial clause numbering -> never rely on layout
  * only 2/64 passages name their instrument -> doc_id must come from doc_link
"""

import csv
import os
from typing import Dict, List, Optional, Tuple

from regrag.models import GoldQuestion
from regrag.corpus.canonical import (
    canonicalize_doc_id,
    extract_article_id,
    extract_article_title,
    extract_gold_citation,
    load_manifest,
    manifest_path,
    prefer_passage_named_doc,
    split_urls,
)

REQUIRED_COLUMNS = ("question", "answer", "text_contains_answer_in_the_doc", "doc_link")


def _row_id(raw_id: str, index: int) -> str:
    """Stable question id from the CSV `ID` column, falling back to row order."""
    raw = (raw_id or "").strip()
    if raw.isdigit():
        return f"Q{int(raw):03d}"
    if raw:
        return raw
    return f"Q{index:03d}"


def load_gold_questions(
    csv_path: str,
    manifest: Optional[Dict[str, str]] = None,
    repo_root: Optional[str] = None,
) -> List[GoldQuestion]:
    """Parse the QA CSV into canonical GoldQuestion objects.

    Every row with a non-empty question is kept. Rows whose instrument cannot be
    resolved are NOT dropped - they are retained with an ``UNRESOLVED:`` doc_id
    so the coverage report can name them instead of silently shrinking the
    benchmark.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"QA CSV not found: {csv_path}")

    if manifest is None:
        root = repo_root or os.path.abspath(
            os.path.join(os.path.dirname(csv_path), "..", "..")
        )
        manifest = load_manifest(manifest_path(root))

    questions: List[GoldQuestion] = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"QA CSV missing required column(s): {missing}")

        for i, row in enumerate(reader, 1):
            q_text = (row.get("question") or "").strip()
            if not q_text:
                continue

            passage = (row.get("text_contains_answer_in_the_doc") or "").strip()
            answer = (row.get("answer") or "").strip()
            urls = split_urls(row.get("doc_link") or "")

            doc_ids: List[str] = []
            confidences: List[str] = []
            for u in urls:
                doc_id, conf = canonicalize_doc_id(u, manifest)
                if doc_id not in doc_ids:
                    doc_ids.append(doc_id)
                    confidences.append(conf)

            # Primary doc_id drives the gold citation. URL order is not evidence,
            # so when the passage itself names one of the candidates, prefer that.
            named = prefer_passage_named_doc(passage, doc_ids)
            if named and doc_ids and doc_ids[0] != named:
                doc_ids = [named] + [d for d in doc_ids if d != named]
            primary = doc_ids[0] if doc_ids else "UNRESOLVED:empty"
            citation = extract_gold_citation(passage, primary)

            if named:
                confidence = "passage-named"
            elif len(doc_ids) > 1:
                confidence = "ambiguous-multi-url"
            else:
                confidence = confidences[0] if confidences else "unresolved"

            questions.append(
                GoldQuestion(
                    id=_row_id(row.get("ID", ""), i),
                    question=q_text,
                    is_answerable=True,
                    gold_doc_ids=doc_ids,
                    gold_citations=[citation] if citation else [],
                    reference_answer=answer,
                    category="factual",
                    gold_passage=passage,
                    source_urls=urls,
                    doc_id_confidence=confidence,
                    author=(row.get("author") or "").strip(),
                )
            )

    return questions


def coverage_report(questions: List[GoldQuestion]) -> Dict[str, object]:
    """Summarise what the CSV can and cannot support, without touching a corpus."""
    n = len(questions)
    resolved = [q for q in questions if q.doc_ids_resolved]
    by_conf: Dict[str, int] = {}
    for q in questions:
        by_conf[q.doc_id_confidence] = by_conf.get(q.doc_id_confidence, 0) + 1
    return {
        "questions": n,
        "doc_ids_resolved": len(resolved),
        "doc_ids_unresolved": n - len(resolved),
        "by_confidence": by_conf,
        "with_article_gold": sum(
            1 for q in questions if q.gold_citations and q.gold_citations[0].get("article_id")
        ),
        "with_clause_gold": sum(
            1 for q in questions if q.gold_citations and q.gold_citations[0].get("clause_id")
        ),
        "empty_passage": sum(1 for q in questions if not q.gold_passage),
        "distinct_doc_ids": sorted({d for q in resolved for d in q.gold_doc_ids}),
        "unresolved_rows": [
            {"id": q.id, "urls": q.source_urls, "doc_ids": q.gold_doc_ids}
            for q in questions
            if not q.doc_ids_resolved
        ],
    }


def load_and_report(
    csv_path: str, repo_root: Optional[str] = None
) -> Tuple[List[GoldQuestion], Dict[str, object]]:
    qs = load_gold_questions(csv_path, repo_root=repo_root)
    return qs, coverage_report(qs)
