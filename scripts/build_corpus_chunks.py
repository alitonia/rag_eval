"""Script to ingest raw legal texts and produce structured clause-level JSON chunks."""

import os
import sys
import json
from dataclasses import asdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from regrag.corpus.parser import LegalDocumentParser

DOCS_MAP = {
    "18_2024_TT_NHNN.txt": {
        "doc_id": "18/2024/TT-NHNN",
        "doc_title": "Thông tư quy định về hoạt động thẻ ngân hàng",
    }
}

def main():
    raw_dir = "data/raw_legal"
    output_path = "data/processed_chunks/corpus_chunks.json"
    os.makedirs("data/processed_chunks", exist_ok=True)

    all_chunks = []
    for filename, meta in DOCS_MAP.items():
        filepath = os.path.join(raw_dir, filename)
        if not os.path.exists(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()

        parser = LegalDocumentParser(doc_id=meta["doc_id"], doc_title=meta["doc_title"])
        chunks = parser.parse(raw_text)
        print(f"Parsed {len(chunks)} clause-level chunks from {filename} ({meta['doc_id']}).")
        all_chunks.extend(chunks)

    serialized = [asdict(c) for c in all_chunks]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serialized, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(all_chunks)} total chunks to {output_path}")

if __name__ == "__main__":
    main()
