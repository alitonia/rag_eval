"""Importer for bank_qa_data - QA.csv into standardized GoldQuestion JSON schema."""

import os
import sys
import csv
import json
import re
from dataclasses import asdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from regrag.models import GoldQuestion
from regrag.evaluation.citation import extract_citations


def import_qa_csv(csv_path: str, output_path: str) -> None:
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    questions = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            q_text = row.get("question", "").strip()
            ans_text = row.get("answer", "").strip()
            ctx_text = row.get("text_contains_answer_in_the_doc", "").strip()
            author = row.get("author", "").strip()
            doc_link = row.get("doc_link", "").strip()

            if not q_text:
                continue

            # Extract citations from answer and supporting context
            citations = extract_citations(ans_text + " " + ctx_text)

            gold_q = GoldQuestion(
                id=f"Q{i:03d}",
                question=q_text,
                is_answerable=True,
                gold_doc_ids=[doc_link] if doc_link else [],
                gold_citations=citations,
                reference_answer=ans_text,
                category="factual",
            )
            q_dict = asdict(gold_q)
            q_dict["author"] = author
            q_dict["ground_truth_context"] = ctx_text
            questions.append(q_dict)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"Successfully imported {len(questions)} questions from {csv_path} to {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Import QA CSV into standardized GoldQuestion JSON")
    parser.add_argument(
        "--csv",
        default=os.path.join(os.path.dirname(__file__), "..", "data", "gold", "bank_qa_data.csv"),
        help="Path to the QA CSV file",
    )
    parser.add_argument(
        "--out",
        default=os.path.join(os.path.dirname(__file__), "..", "data", "gold", "questions_in_progress.json"),
        help="Output path for JSON",
    )
    args = parser.parse_args()

    import_qa_csv(os.path.abspath(args.csv), os.path.abspath(args.out))
