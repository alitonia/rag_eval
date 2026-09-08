"""Regex-based parser for Vietnamese legal circulars and decrees.

Segments legal texts into granular Khoản (Clause) units while retaining parent
metadata (Document ID, Title, Chapter, Article ID, Article Title).
"""

import re
from typing import List, Optional
from regrag.models import LegalChunk


class LegalDocumentParser:
    """Parses structured Vietnamese legal documents (Thông tư, Nghị định)."""

    # Matches "Chương I. NHỮNG QUY ĐỊNH CHUNG" or similar
    CHAPTER_REGEX = re.compile(r"^(Chương\s+[IVXLCDM\d]+)[\.\:\s]*(.*)$", re.IGNORECASE | re.MULTILINE)

    # Matches "Điều 15. Hạn mức giao dịch thẻ"
    ARTICLE_REGEX = re.compile(r"^Điều\s+(\d+)[\.\:\s]+([^\n\r]+)", re.IGNORECASE | re.MULTILINE)

    # Matches numbered clauses at start of line: "1. ", "2. ", etc.
    CLAUSE_REGEX = re.compile(r"^(\d+)\.\s+", re.MULTILINE)

    def __init__(self, doc_id: str, doc_title: str) -> None:
        self.doc_id = doc_id
        self.doc_title = doc_title

    def parse(self, raw_text: str) -> List[LegalChunk]:
        """Parse raw text of a circular into a list of LegalChunk objects."""
        chunks: List[LegalChunk] = []
        lines = raw_text.splitlines()

        current_chapter: Optional[str] = None
        current_article_id: Optional[str] = None
        current_article_title: str = ""
        current_clause_id: Optional[str] = None
        current_clause_lines: List[str] = []

        def flush_clause():
            nonlocal current_clause_lines, current_clause_id
            if current_article_id and current_clause_lines:
                clause_text = "\n".join(current_clause_lines).strip()
                if clause_text:
                    chunk_id = f"{self.doc_id}_D{current_article_id}"
                    if current_clause_id:
                        chunk_id += f"_K{current_clause_id}"
                    else:
                        chunk_id += "_Kall"

                    chunk = LegalChunk(
                        chunk_id=chunk_id,
                        doc_id=self.doc_id,
                        doc_title=self.doc_title,
                        chapter=current_chapter,
                        article_id=current_article_id,
                        article_title=current_article_title,
                        clause_id=current_clause_id,
                        text=clause_text,
                    )
                    chunks.append(chunk)
            current_clause_lines = []

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Check Chapter
            chap_match = self.CHAPTER_REGEX.match(line_str)
            if chap_match:
                current_chapter = f"{chap_match.group(1)}: {chap_match.group(2).strip()}"
                continue

            # Check Article
            art_match = self.ARTICLE_REGEX.match(line_str)
            if art_match:
                flush_clause()
                current_article_id = art_match.group(1)
                current_article_title = art_match.group(2).strip()
                current_clause_id = None
                continue

            # Check Clause if within an Article
            if current_article_id:
                clause_match = self.CLAUSE_REGEX.match(line_str)
                if clause_match:
                    flush_clause()
                    current_clause_id = clause_match.group(1)
                    current_clause_lines.append(line_str)
                else:
                    current_clause_lines.append(line_str)

        flush_clause()
        return chunks
