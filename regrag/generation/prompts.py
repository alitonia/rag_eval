"""Prompt templates for Closed-book and RAG generation on Vietnamese banking regulations."""

from typing import List
from regrag.models import RetrievedResult


SYSTEM_PROMPT_VI = (
    "Bạn là chuyên gia tư vấn pháp lý chuyên sâu về các quy định ngân hàng, "
    "thanh toán điện tử và nghiệp vụ thẻ của Ngân hàng Nhà nước Việt Nam. "
    "Nhiệm vụ của bạn là trả lời chính xác, trung thực dựa trên các văn bản pháp luật hiện hành."
)

ABSTENTION_KEYPHRASE = "THÔNG TIN KHÔNG CÓ TRONG TÀI LIỆU"


def build_closed_book_prompt(question: str) -> str:
    """Prompt for closed-book condition."""
    return f"""{SYSTEM_PROMPT_VI}

Câu hỏi: {question}

Yêu cầu:
1. Trả lời chính xác nội dung câu hỏi.
2. Nêu rõ căn cứ pháp lý nếu biết (Tên văn bản, Điều, Khoản).
3. Nếu bạn không chắc chắn hoặc quy định pháp luật không quy định, hãy trả lời chính xác: "{ABSTENTION_KEYPHRASE}". Không được suy diễn hoặc tạo ra căn cứ pháp lý không có thật.

Trả lời:"""


def build_rag_prompt(question: str, retrieved_results: List[RetrievedResult]) -> str:
    """Prompt for RAG condition with context chunks."""
    context_blocks = []
    for i, res in enumerate(retrieved_results, 1):
        context_blocks.append(
            f"--- Tài liệu tham khảo [{i}] ---\n{res.chunk.formatted_context()}"
        )
    context_str = "\n\n".join(context_blocks)

    return f"""{SYSTEM_PROMPT_VI}

Dưới đây là các đoạn trích từ quy định pháp luật của Ngân hàng Nhà nước Việt Nam:

{context_str}

---
Câu hỏi: {question}

Yêu cầu nghiêm ngặt:
1. Chỉ sử dụng thông tin trong các đoạn trích trên để trả lời.
2. Phải trích dẫn cụ thể căn cứ pháp lý (Tên văn bản/Thông tư, Điều, Khoản) hỗ trợ cho câu trả lời.
3. Nếu các đoạn trích trên KHÔNG chứa đủ thông tin để trả lời câu hỏi, bạn PHẢI trả lời: "{ABSTENTION_KEYPHRASE}". Tuyệt đối không tự suy đoán thông tin ngoài văn bản.

Trả lời:"""
