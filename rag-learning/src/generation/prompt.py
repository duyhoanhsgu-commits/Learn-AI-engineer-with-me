"""
Module: src/generation/prompt.py
Mục đích: Chuẩn hóa cấu trúc Prompt cho khâu Augmented Generation (Chữ "G" trong RAG).
Công thức:
   Final Prompt = System Instruction + Retrieved Context (có đánh số & metadata) + User Query
"""

from typing import Any, Dict, List, Optional, Tuple

DEFAULT_SYSTEM_INSTRUCTION = (
    "Bạn là một trợ lý AI thông minh, trung thực và chính xác.\n"
    "Nhiệm vụ của bạn là trả lời câu hỏi của người dùng CHỈ DỰA TRÊN các đoạn tài liệu tham khảo (Context) được cung cấp dưới đây.\n"
    "NGUYÊN TẮC CỐT LÕI:\n"
    "1. Tính Căn Cứ (Grounding): Tuyệt đối không tự suy diễn hoặc bịa đặt thông tin nằm ngoài Context.\n"
    "2. Từ Chối Trung Thực: Nếu Context không chứa đủ thông tin để trả lời câu hỏi, bạn PHẢI trả lời rõ: "
    "'Xin lỗi, tài liệu được cung cấp không có thông tin về vấn đề này.'\n"
    "3. Trích Dẫn Nguồn (Citations): Cuối mỗi luận điểm quan trọng, hãy ghi rõ nguồn tham khảo dạng [Nguồn 1], [Nguồn 2] tương ứng với tài liệu đã dùng."
)


def format_context_blocks(context_chunks: List[Dict[str, Any]]) -> str:
    """
    Định dạng danh sách các chunk thành khối ngữ cảnh có cấu trúc:
    --- [Nguồn 1: doc_id | title] ---
    Nội dung chunk...
    """
    if not context_chunks:
        return "(Không có tài liệu tham khảo nào được cung cấp)"

    blocks = []
    for idx, chunk in enumerate(context_chunks, 1):
        doc_id = chunk.get("chunk_id") or chunk.get("id", f"doc_{idx}")
        meta = chunk.get("metadata", {})
        meta_str = f" | {meta}" if meta else ""
        content = chunk.get("content") or chunk.get("text", "")

        block = f"--- [Nguồn {idx} | ID: {doc_id}{meta_str}] ---\n{content.strip()}"
        blocks.append(block)

    return "\n\n".join(blocks)


def build_rag_prompt(
    query: str,
    context_chunks: List[Dict[str, Any]],
    system_instruction: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Xây dựng cặp tin nhắn (system_prompt, user_prompt) chuẩn cho các API Chat Completion.
    """
    system_prompt = system_instruction or DEFAULT_SYSTEM_INSTRUCTION
    context_text = format_context_blocks(context_chunks)

    user_prompt = (
        f"Dưới đây là các tài liệu ngữ cảnh được trích xuất:\n\n"
        f"{context_text}\n\n"
        f"==================================================\n"
        f"CÂU HỎI CỦA NGƯỜI DÙNG: {query}\n"
        f"CÂU TRẢ LỜI CỦA BẠN:"
    )

    return system_prompt, user_prompt


if __name__ == "__main__":
    sample_chunks = [
        {
            "chunk_id": "c101",
            "content": "Chính sách làm việc từ xa: Nhân viên được đăng ký WFH tối đa 2 ngày/tuần sau khi thử việc.",
            "metadata": {"dept": "HR", "version": "2024"},
        },
        {
            "chunk_id": "c102",
            "content": "Thời gian làm việc tiêu chuẩn từ 8h30 đến 17h30 từ thứ Hai đến thứ Sáu.",
            "metadata": {"dept": "HR"},
        },
    ]

    sys_p, usr_p = build_rag_prompt("Quy định làm việc tại nhà như thế nào?", sample_chunks)
    print("=== SYSTEM PROMPT ===")
    print(sys_p)
    print("\n=== USER PROMPT ===")
    print(usr_p)
