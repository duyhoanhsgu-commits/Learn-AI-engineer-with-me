"""
Module: src/generation/generator.py
Mục đích: Triển khai thành phần Augmented Generation (Chữ "G" trong RAG):
   1. Nhận câu hỏi (Query) và các đoạn ngữ cảnh (Context Chunks từ Retrieval/Reranker).
   2. Tạo Prompt có cấu trúc chuẩn hóa, ràng buộc chống ảo giác và yêu cầu trích dẫn.
   3. Gửi tới LLM để sinh câu trả lời có căn cứ xác thực (Grounded Answer).
   4. Hỗ trợ chế độ Offline Fallback trích xuất thông tin nếu chưa cấu hình API Key.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

# Đảm bảo import được module trong rag-learning và nạp file .env từ root
current_file = Path(__file__).resolve()
rag_dir = current_file.parent.parent.parent       # .../rag-learning
project_root = rag_dir.parent                    # .../Learn AI

# Tìm và nạp file .env
for candidate in [project_root / ".env", rag_dir / ".env"]:
    if candidate.exists():
        load_dotenv(dotenv_path=candidate)
        break
else:
    load_dotenv()

if str(rag_dir) not in sys.path:
    sys.path.insert(0, str(rag_dir))

from src.generation.prompt import build_rag_prompt


class RAGGenerator:
    """Bộ sinh câu trả lời tăng cường ngữ cảnh (Augmented Generator)."""

    def __init__(self, model_name: Optional[str] = None, temperature: float = 0.2):
        self.model_name = model_name or os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.temperature = temperature
        self.api_key = os.getenv("OPENAI_API_KEY")

    def _call_llm_api(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Gọi LLM qua OpenAI API nếu có API key hợp lệ."""
        if not self.api_key or not self.api_key.strip():
            return None
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self.temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"⚠️ Gọi API LLM không thành công ({e}). Chuyển sang mô phỏng sinh có căn cứ.")
            return None

    STOPWORDS = {
        "cho", "có", "không", "của", "được", "trong", "các", "về", "làm", "những",
        "thì", "là", "và", "như", "theo", "này", "đó", "gì", "nào", "sao", "để", "với",
        "bằng", "hoặc", "tại", "từ", "ra", "vào", "ai", "bao", "nhiêu"
    }

    def _fallback_grounded_answer(
        self, query: str, context_chunks: List[Dict[str, Any]]
    ) -> str:
        """
        Bộ sinh câu trả lời ngoại tuyến (Offline Heuristic Generator):
        Tuân thủ nguyên tắc Grounding:
        - Lọc bỏ stop words để lấy các từ khóa thực chất (meaningful key terms).
        - Quét tìm câu trả lời trực tiếp trong context chunks.
        - Nếu không tìm thấy thông tin trùng khớp, kiên quyết từ chối thay vì bịa đặt.
        """
        if not context_chunks:
            return "Xin lỗi, tài liệu được cung cấp không có thông tin về vấn đề này."

        raw_terms = [w.lower().strip("?,.!") for w in query.split()]
        key_terms = [w for w in raw_terms if len(w) > 1 and w not in self.STOPWORDS]

        if not key_terms:
            return "Xin lỗi, tài liệu được cung cấp không có thông tin về vấn đề này."

        matched_sentences = []

        for idx, chunk in enumerate(context_chunks, 1):
            content = chunk.get("content") or chunk.get("text", "")
            sentences = [s.strip() for s in content.split(".") if s.strip()]
            for s in sentences:
                s_lower = s.lower()
                # Phải khớp ít nhất 2 từ khóa quan trọng hoặc >= 40% số từ khóa câu hỏi
                matches = sum(1 for term in key_terms if term in s_lower)
                if matches >= 2 and (matches / len(key_terms) >= 0.3):
                    matched_sentences.append(f"{s}. [Nguồn {idx}]")

        if matched_sentences:
            unique_sentences = list(dict.fromkeys(matched_sentences))
            return "Dựa trên tài liệu tham khảo:\n" + " ".join(unique_sentences)

        return "Xin lỗi, tài liệu được cung cấp không có thông tin về vấn đề này."

    def generate(
        self,
        query: str,
        context_chunks: List[Dict[str, Any]],
        system_instruction: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Quy trình Augmented Generation:
        1. Xây dựng prompt chuẩn hóa.
        2. Sinh câu trả lời từ LLM (hoặc Fallback Grounded Engine).
        3. Đóng gói kết quả kèm danh sách trích dẫn nguồn (Sources / Citations).
        """
        system_prompt, user_prompt = build_rag_prompt(
            query=query,
            context_chunks=context_chunks,
            system_instruction=system_instruction,
        )

        is_offline = False
        answer = self._call_llm_api(system_prompt, user_prompt)

        if answer is None:
            is_offline = True
            answer = self._fallback_grounded_answer(query, context_chunks)

        # Xây dựng danh sách nguồn tham khảo minh bạch
        sources = []
        for idx, chunk in enumerate(context_chunks, 1):
            doc_id = chunk.get("chunk_id") or chunk.get("id", f"doc_{idx}")
            content = chunk.get("content") or chunk.get("text", "")
            snippet = content[:100] + ("..." if len(content) > 100 else "")
            sources.append({
                "source_tag": f"[Nguồn {idx}]",
                "chunk_id": doc_id,
                "snippet": snippet,
                "metadata": chunk.get("metadata", {}),
            })

        return {
            "query": query,
            "answer": answer,
            "sources": sources,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "model": self.model_name if not is_offline else "Offline-Grounded-Heuristic",
            "is_offline_fallback": is_offline,
        }


if __name__ == "__main__":
    print("=" * 65)
    print("=== DEMO AUGMENTED GENERATION (CHỮ 'G' TRONG RAG) ===")
    print("=" * 65)

    generator = RAGGenerator()

    # Dữ liệu context đã qua Retrieval & Rerank
    relevant_contexts = [
        {
            "chunk_id": "hr_doc_01",
            "content": "Chính sách nghỉ ốm: Nhân viên được nghỉ tối đa 30 ngày/năm và hưởng 75% mức lương theo quy định BHXH.",
            "metadata": {"title": "Sổ tay nhân sự", "chapter": "Quyền lợi"},
        },
        {
            "chunk_id": "hr_doc_02",
            "content": "Để làm thủ tục hưởng trợ cấp ốm đau, người lao động phải nộp giấy ra viện hoặc giấy chứng nhận nghỉ việc hưởng BHXH cho phòng nhân sự trong 3 ngày.",
            "metadata": {"title": "Quy trình nhân sự", "chapter": "Thủ tục"},
        },
    ]

    # Trường hợp 1: Câu hỏi có trong context
    test_q1 = "Chế độ nghỉ ốm của nhân viên được bao nhiêu ngày và hưởng bao nhiêu lương?"
    print(f"\n🔍 [TRƯỜNG HỢP 1 - CÂU HỎI CÓ TRONG CONTEXT]: '{test_q1}'")
    res1 = generator.generate(test_q1, relevant_contexts)
    print(f"\n💡 CÂU TRẢ LỜI ({res1['model']}):")
    print(res1["answer"])
    print("\n📚 NGUỒN TRÍCH DẪN (CITATIONS):")
    for s in res1["sources"]:
        print(f"   {s['source_tag']} ID: {s['chunk_id']} | Snippet: {s['snippet']}")

    # Trường hợp 2: Câu hỏi KHÔNG có trong context (Kiểm tra tính Grounding / Không ảo giác)
    test_q2 = "Công ty có hỗ trợ kinh phí mua xe ô tô cho nhân viên không?"
    print(f"\n\n🔍 [TRƯỜNG HỢP 2 - CÂU HỎI NGOÀI CONTEXT]: '{test_q2}'")
    res2 = generator.generate(test_q2, relevant_contexts)
    print(f"\n💡 CÂU TRẢ LỜI ({res2['model']}):")
    print(res2["answer"])
