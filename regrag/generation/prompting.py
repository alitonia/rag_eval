"""Chat-message assembly on top of the repo's sanctioned prompt templates.

``regrag/generation/prompts.py`` builds a single prompt *string* that already
embeds ``SYSTEM_PROMPT_VI``. This module wraps those builders into the
``messages`` list a chat model needs, without re-wording a single character of
them - the prompt text stays exactly what the rest of the repo assumes, which
matters for reproducibility and because the abstention wording is shared with
``regrag/evaluation/metrics.py``.

Consequence, stated plainly: the messages list has ONE user turn and no separate
system turn, because the system persona is already inside the builder's output.
Duplicating it as a system message would send the persona twice.
"""

from __future__ import annotations

from typing import Dict, List, Sequence

from regrag.generation.prompts import build_closed_book_prompt, build_rag_prompt
from regrag.models import GoldQuestion, RetrievedResult

CLOSED_BOOK = "closed_book"
RAG_MODES = ("rag_bm25", "rag_dense")


def build_messages(
    question_text: str,
    retrieval_mode: str,
    retrieved: Sequence[RetrievedResult] = (),
) -> List[Dict[str, str]]:
    """Render the chat messages for one (question, mode) cell."""
    if retrieval_mode == CLOSED_BOOK:
        content = build_closed_book_prompt(question_text)
    elif retrieval_mode in RAG_MODES:
        content = build_rag_prompt(question_text, list(retrieved))
    else:
        raise ValueError(
            f"Unknown retrieval mode {retrieval_mode!r}. Expected one of "
            f"{(CLOSED_BOOK,) + RAG_MODES}."
        )
    return [{"role": "user", "content": content}]


def messages_from_question(
    q: GoldQuestion,
    retrieval_mode: str,
    retrieved: Sequence[RetrievedResult] = (),
) -> List[Dict[str, str]]:
    return build_messages(q.question, retrieval_mode, retrieved)


def messages_to_prompt_field(messages: Sequence[Dict[str, str]], marker: str) -> str:
    """Serialise messages into ``GenerationResult.prompt``.

    The marker prefixes the payload so a reader can always tell whether the
    string is the literal token sequence the model consumed or a client-side
    rendering of the request. A vLLM row CANNOT carry the literal string: the
    server applies its tokenizer's chat template and never returns it. Writing
    the messages there unmarked would imply a fidelity the row does not have.
    """
    import json

    body = json.dumps(list(messages), ensure_ascii=False)
    return f"{marker}\n{body}"
