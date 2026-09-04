"""
Module: src/retrieval/pre_retrieval.py
Mục đích: Xử lý tiền truy xuất (Pre-retrieval) nhằm tối ưu hóa câu hỏi của người dùng:
   1. Query Rewriting: Chuyển câu hỏi mơ hồ/chứa đại từ thay thế thành Standalone Query.
   2. Multi-query Generation: Phân rã 1 câu hỏi thành nhiều biến thể để tăng độ phủ (Recall).
   3. Synonym Expansion: Bổ sung từ đồng nghĩa để tránh điểm mù từ khóa.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Nạp biến môi trường từ root
root_dir = Path(__file__).resolve().parent.parent.parent
env_path = root_dir / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


class PreRetrievalProcessor:
    """Bộ xử lý tiền truy xuất cho câu hỏi người dùng trước khi tìm kiếm vector."""

    # Bảng tra cứu từ đồng nghĩa thông dụng trong lĩnh vực AI/RAG
    SYNONYM_MAP = {
        "ô tô": ["xe hơi", "phương tiện giao thông"],
        "xe hơi": ["ô tô", "phương tiện 4 bánh"],
        "llm": ["mô hình ngôn ngữ lớn", "large language model"],
        "rag": ["retrieval augmented generation", "truy xuất tăng cường"],
        "hallucination": ["ảo giác", "thông tin bịa đặt"],
        "embedding": ["vector nhúng", "dense vector"],
    }

    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")

    def _call_llm(self, prompt: str) -> Optional[str]:
        """Gọi OpenAI nếu có API Key hợp lệ."""
        if not self.api_key or not self.api_key.strip():
            return None
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            resp = client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return None

    # =====================================================================
    # 1. QUERY REWRITING (VIẾT LẠI TRUY VẤN ĐỘC LẬP)
    # =====================================================================
    def rewrite_query(
        self,
        query: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Phân tích lịch sử hội thoại để loại bỏ đại từ mập mờ ("nó", "cái này", "phương pháp đó")
        và tạo thành câu truy vấn độc lập (Standalone Query).
        """
        if not conversation_history:
            return query.strip()

        # 1. Thử gọi LLM nếu có API Key
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
        prompt = (
            f"Dựa vào lịch sử hội thoại sau đây:\n{history_text}\n\n"
            f"Người dùng vừa hỏi: '{query}'\n"
            f"Hãy viết lại câu hỏi trên thành một câu truy vấn tìm kiếm độc lập (Standalone Search Query), "
            f"thay thế các đại từ (nó, cái đó, công nghệ này...) bằng chủ ngữ thực sự. Chỉ trả về câu đã viết lại, không giải thích."
        )
        llm_output = self._call_llm(prompt)
        if llm_output:
            return llm_output.strip('"\' ')

        # 2. Fallback Heuristic (Quy tắc nhận diện ngữ cảnh đơn giản khi offline)
        last_turn = conversation_history[-1].get("content", "")
        # Trích xuất các thực thể hoặc danh từ viết hoa / ngoặc kép từ câu trước
        subject_match = re.search(r'([A-Z][a-zA-Z0-9_\-]+|"[^"]+"|[A-ZÀ-Ỵ][a-zà-ỹ\s]+)', last_turn)
        subject = subject_match.group(0).strip('"') if subject_match else ""

        pronouns = ["nó", "cái này", "cái đó", "công nghệ này", "thuật toán đó", "phương pháp này"]
        rewritten = query
        if subject:
            for p in pronouns:
                if p in rewritten.lower():
                    # Thay thế đại từ bằng chủ ngữ từ câu trước
                    rewritten = re.sub(rf"\b{p}\b", subject, rewritten, flags=re.IGNORECASE)

        return rewritten.strip()

    # =====================================================================
    # 2. MULTI-QUERY GENERATION (SINH ĐA TRUY VẤN)
    # =====================================================================
    def generate_multi_queries(self, query: str, num_queries: int = 3) -> List[str]:
        """
        Phân rã câu hỏi gốc thành nhiều biến thể với góc nhìn khác nhau
        để tăng tỷ lệ tìm trúng tài liệu (tối đa hóa Recall).
        """
        queries = [query.strip()]

        # 1. Thử gọi LLM nếu có API key
        prompt = (
            f"Hãy tạo {num_queries - 1} câu hỏi biến thể có cùng ý nghĩa nhưng dùng các từ khóa khác nhau "
            f"cho câu hỏi sau: '{query}'.\n"
            f"Mỗi câu hỏi trên 1 dòng, không đánh số thứ tự."
        )
        llm_output = self._call_llm(prompt)
        if llm_output:
            lines = [line.strip("- •0123456789. ") for line in llm_output.splitlines() if line.strip()]
            queries.extend(lines[: num_queries - 1])
            return queries

        # 2. Fallback Heuristic (Tạo câu biến thể dạng quy tắc)
        q_lower = query.lower()
        if "là gì" in q_lower or "khái niệm" in q_lower:
            queries.append(f"Định nghĩa và nguyên lý hoạt động của {re.sub(r'(là gì|khái niệm)', '', query).strip(' ?')}")
            queries.append(f"Đặc điểm cốt lõi của {re.sub(r'(là gì|khái niệm)', '', query).strip(' ?')}")
        elif "như thế nào" in q_lower or "làm sao" in q_lower:
            queries.append(f"Cơ chế và các bước thực hiện {re.sub(r'(như thế nào|làm sao)', '', query).strip(' ?')}")
            queries.append(f"Hướng dẫn chi tiết về {re.sub(r'(như thế nào|làm sao)', '', query).strip(' ?')}")
        else:
            queries.append(f"Tổng quan và kiến trúc {query.strip(' ?')}")
            queries.append(f"Hướng dẫn thực hành {query.strip(' ?')}")

        return queries[:num_queries]

    # =====================================================================
    # 3. SYNONYM EXPANSION (MỞ RỘNG TỪ ĐỒNG NGHĨA)
    # =====================================================================
    def expand_synonyms(self, query: str) -> str:
        """Bổ sung các từ đồng nghĩa phổ biến vào câu truy vấn."""
        expanded_terms = []
        for term, synonyms in self.SYNONYM_MAP.items():
            if term in query.lower():
                expanded_terms.extend(synonyms)

        if expanded_terms:
            return f"{query} (Từ khóa mở rộng: {', '.join(set(expanded_terms))})"
        return query


if __name__ == "__main__":
    processor = PreRetrievalProcessor()

    print("=== DEMO PRE-RETRIEVAL PROCESSING ===")

    # 1. Test Query Rewriting (Phân giải đại từ từ lịch sử)
    history = [
        {"role": "user", "content": "Thuật toán HNSW là gì?"},
        {"role": "assistant", "content": "HNSW (Hierarchical Navigable Small World) là đồ thị tìm kiếm láng giềng gần nhất xấp xỉ."},
    ]
    raw_query = "Nó hoạt động kiểu gì và có ưu điểm gì?"
    rewritten = processor.rewrite_query(raw_query, conversation_history=history)

    print("\n[1] QUERY REWRITING:")
    print(f"Câu hỏi thô của user : '{raw_query}'")
    print(f"Lịch sử trước đó      : Bàn về '{history[0]['content']}'")
    print(f"-> Câu hỏi sau Rewrite: '{rewritten}'")

    # 2. Test Multi-query Generation (Sinh đa biến thể)
    topic_query = "Làm sao để RAG giảm thiểu ảo giác?"
    multi_queries = processor.generate_multi_queries(topic_query, num_queries=3)

    print("\n[2] MULTI-QUERY GENERATION:")
    print(f"Câu hỏi gốc: '{topic_query}'")
    print("Các biến thể tìm kiếm:")
    for i, q in enumerate(multi_queries, 1):
        print(f"   ({i}) {q}")

    # 3. Test Synonym Expansion
    sample_q = "Tôi muốn tìm hiểu về mô hình ô tô tự hành"
    expanded_q = processor.expand_synonyms(sample_q)
    print("\n[3] SYNONYM EXPANSION:")
    print(f"Gốc    : '{sample_q}'")
    print(f"Mở rộng: '{expanded_q}'")
