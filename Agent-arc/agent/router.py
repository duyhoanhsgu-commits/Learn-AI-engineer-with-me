"""
Module: agent/router.py
Mục đích: Định tuyến dựa trên Embedding (Semantic Router)
Luồng: Input User -> Embedding -> So khớp độ tương đồng Vector -> [RAG hoặc AGENT]
"""

import math
import os
from typing import Dict, List, Literal, Tuple
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


RouteType = Literal["RAG", "AGENT"]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Tính khoảng cách cosine giữa hai vector."""
    if len(vec_a) != len(vec_b) or not vec_a:
        return 0.0
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot_product / (norm_a * norm_b)


class EmbeddingRouter:
    """
    Semantic Router:
    Phân loại câu hỏi của người dùng vào nhánh RAG hoặc AGENT bằng Vector Embedding.
    """

    # Các câu mẫu đại diện cho ý định (Intent Anchors)
    ROUTE_ANCHORS: Dict[RouteType, List[str]] = {
        "RAG": [
            "Tra cứu tài liệu, chính sách, quy định nội bộ",
            "Tìm kiếm thông tin dữ liệu trong văn bản đã lưu",
            "Định nghĩa, khái niệm hoặc thông tin lịch sử từ tài liệu",
            "Tìm kiếm văn bản trong cơ sở dữ liệu tri thức",
            "Tài liệu hướng dẫn này viết gì về chính sách bảo hành?",
        ],
        "AGENT": [
            "Tính toán ngân sách hoặc giải phương trình toán học",
            "Gọi công cụ, thực thi code, gửi email hoặc thao tác API bên ngoài",
            "Lập kế hoạch nhiều bước và phối hợp thực hiện tác vụ phức tạp",
            "Kiểm tra thời tiết hiện tại qua công cụ bên ngoài",
            "Đặt vé máy bay hoặc tạo một file báo cáo tự động",
        ],
    }

    def __init__(self, model_name: str = "text-embedding-3-small"):
        self.model_name = model_name
        self._anchor_embeddings: Dict[RouteType, List[List[float]]] = {}
        self._init_anchors()

    def get_embedding(self, text: str) -> List[float]:
        """
        Tạo embedding vector từ text.
        Ưu tiên dùng OpenAI Embedding nếu có API Key; nếu không có sẽ dùng fallback
        thuật toán băm đặc trưng ngữ nghĩa (semantic feature hashing) để chạy offline.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key.strip():
            try:
                from openai import OpenAI

                client = OpenAI(api_key=api_key)
                response = client.embeddings.create(input=text, model=self.model_name)
                return response.data[0].embedding
            except Exception as e:
                print(f"[Warning] Gọi OpenAI Embedding lỗi ({e}), chuyển sang fallback embedding.")

        # Fallback Offline Feature-based Embedding (không phụ thuộc external API)
        return self._fallback_embedding(text)

    def _fallback_embedding(self, text: str, dim: int = 256) -> List[float]:
        """Tạo vector chuẩn hóa ổn định (deterministic) cho môi trường local/demo."""
        import hashlib
        stop_words = {"và", "của", "là", "gì", "các", "trong", "cho", "với", "được", "này", "để", "có", "một", "những", "the", "is", "a", "an", "and", "or"}
        words = [w.strip("?,.!") for w in text.lower().split() if w.strip("?,.!") not in stop_words and len(w.strip("?,.!")) > 1]
        vector = [0.0] * dim
        for word in words:
            # Dùng md5 để vector luôn cố định qua các lần chạy
            idx = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16) % dim
            vector[idx] += 1.0
        norm = math.sqrt(sum(v * v for v in vector))
        if norm > 0:
            vector = [v / norm for v in vector]
        return vector

    def _init_anchors(self) -> None:
        """Tạo embedding cho các câu mẫu của từng route."""
        for route, examples in self.ROUTE_ANCHORS.items():
            self._anchor_embeddings[route] = [self.get_embedding(ex) for ex in examples]

    def route(self, user_input: str) -> Tuple[RouteType, float, Dict[RouteType, float]]:
        """
        Định tuyến:
        Input User -> Embedding -> Tính điểm tương đồng Cosine với từng Route -> Lựa chọn RAG hoặc AGENT.
        """
        user_vec = self.get_embedding(user_input)

        scores: Dict[RouteType, float] = {}
        for route, anchor_vecs in self._anchor_embeddings.items():
            # Tính điểm tương đồng cao nhất giữa input và các anchors của route
            similarities = [cosine_similarity(user_vec, a_vec) for a_vec in anchor_vecs]
            scores[route] = max(similarities) if similarities else 0.0

        # Chọn route có độ tương đồng lớn nhất
        chosen_route: RouteType = max(scores, key=lambda k: scores[k])
        confidence = scores[chosen_route]

        return chosen_route, confidence, scores
