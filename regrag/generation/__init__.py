"""Generation package for prompt construction and model interaction."""

from regrag.generation.prompts import (
    build_closed_book_prompt,
    build_rag_prompt,
    ABSTENTION_KEYPHRASE,
)

__all__ = [
    "build_closed_book_prompt",
    "build_rag_prompt",
    "ABSTENTION_KEYPHRASE",
]
