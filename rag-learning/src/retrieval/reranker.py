"""
Module: src/retrieval/reranker.py
Mục đích: Triển khai Re-ranking với Cross-Encoder trong RAG:
   1. Nhận danh sách ứng viên (Candidates) từ bước Retrieval (Top 10 - 50).
   2. Ghép cặp trực tiếp (Query, Document) đưa qua mô hình Cross-Encoder để tính All-to-All Cross-Attention.
   3. Sắp xếp lại theo điểm số liên quan thực tế và chắt lọc ra Top-K tinh túy nhất (Top 3 - 5) cho LLM.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Đảm bảo import được module trong rag-learning
rag_dir = Path(__file__).resolve().parent.parent.parent
if str(rag_dir) not in sys.path:
    sys.path.insert(0, str(rag_dir))


class CrossEncoderReranker:
    """Mô hình Re-ranking sử dụng Cross-Encoder để đánh giá tương quan ngữ nghĩa sâu."""

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self._model = None

    def _get_model(self):
        """Khởi tạo Cross-Encoder model (Lazy Loading)."""
        if self._model is None:
            try:
                from sentence_transformers import CrossEncoder

                print(f"🔄 Đang tải mô hình Cross-Encoder: {self.model_name}...")
                self._model = CrossEncoder(self.model_name)
                print("✅ Tải Cross-Encoder thành công!")
            except Exception as e:
                print(f"⚠️ Không thể tải mô hình Cross-Encoder online ({e}). Chuyển sang chế độ Fallback heuristic.")
                self._model = None
        return self._model

    def _fallback_score(self, query: str, text: str) -> float:
        """Thuật toán dự phòng tính điểm tương quan ngữ nghĩa đơn giản nếu offline."""
        q_words = set(query.lower().split())
        t_words = text.lower().split()
        if not q_words or not t_words:
            return 0.0
        match_count = sum(1 for w in t_words if w in q_words)
        return match_count / (len(q_words) + len(set(t_words)))

    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Thực hiện Reranking cho danh sách tài liệu ứng viên:
        - Input: Danh sách documents (mỗi doc có 'content' hoặc 'text', 'chunk_id'...)
        - Output: Top-K documents đã được tái xếp hạng kèm theo `rerank_score` và `original_rank`.
        """
        if not documents:
            return []

        # Chuẩn bị danh sách cặp (Query, Doc Content)
        pairs: List[List[str]] = []
        doc_contents: List[str] = []

        for doc in documents:
            content = doc.get("content") or doc.get("text") or ""
            pairs.append([query, content])
            doc_contents.append(content)

        model = self._get_model()

        if model is not None:
            # Dự đoán điểm relevance với Cross-Encoder
            # Model trả về raw logits (điểm số càng cao càng liên quan)
            scores = model.predict(pairs)
        else:
            # Fallback scoring
            scores = [self._fallback_score(query, text) for text in doc_contents]

        # Ghép điểm và thông tin xếp hạng ban đầu
        scored_docs: List[Dict[str, Any]] = []
        for orig_rank, (doc, score) in enumerate(zip(documents, scores), start=1):
            doc_copy = dict(doc)
            doc_copy["original_rank"] = orig_rank
            doc_copy["rerank_score"] = float(score)
            scored_docs.append(doc_copy)

        # Sắp xếp giảm dần theo điểm Rerank
        scored_docs.sort(key=lambda item: item["rerank_score"], reverse=True)

        return scored_docs[:top_k]


if __name__ == "__main__":
    print("=" * 65)
    print("=== DEMO RERANKING VỚI CROSS-ENCODER ===")
    print("=" * 65)

    reranker = CrossEncoderReranker()

    test_query = "Làm thế nào để đổi mật khẩu tài khoản người dùng?"

    # Giả lập danh sách Top Candidates trả về từ bước Retrieval (có cả tài liệu liên quan thật và tài liệu chứa từ khóa gây nhiễu)
    retrieved_candidates = [
        {
            "chunk_id": "doc_01",
            "content": "Chính sách mật khẩu: Người dùng phải đặt mật khẩu tối thiểu 8 ký tự bao gồm chữ hoa và số.",
            "metadata": {"section": "policy"},
        },
        {
            "chunk_id": "doc_02",
            "content": "Các bước đổi mật khẩu: Vào Cài đặt cá nhân -> Chọn Bảo mật -> Nhập mật khẩu cũ và xác nhận mật khẩu mới.",
            "metadata": {"section": "guide"},
        },
        {
            "chunk_id": "doc_03",
            "content": "Tài khoản người dùng bị khóa khi đăng nhập sai mật khẩu quá 5 lần liên tiếp.",
            "metadata": {"section": "troubleshoot"},
        },
    ]

    print(f"\n🔍 Câu hỏi truy vấn: '{test_query}'")
    print(f"📦 Số lượng ứng viên từ Retrieval: {len(retrieved_candidates)}")

    reranked_results = reranker.rerank(test_query, retrieved_candidates, top_k=3)

    print("\n📊 BẢNG XẾP HẠNG SAU KHI QUA CROSS-ENCODER:")
    for new_rank, item in enumerate(reranked_results, 1):
        print(f"\n[{new_rank}] ID: {item['chunk_id']} | Điểm Rerank: {item['rerank_score']:+.4f} (Thứ hạng cũ: #{item['original_rank']})")
        print(f"    Nội dung: {item['content']}")
