"""
Module: rag-learning/compare_vectors.py
Mục đích: So sánh vector biểu diễn (Embedding Vectors) giữa hai từ / cụm từ.
Lý thuyết nền tảng (RAG Chapter 1):
  - Chuyển đổi từ ngữ thành Dense Vector nhiều chiều trong không gian ngữ nghĩa.
  - So sánh mức độ tương đồng qua:
      + Cosine Similarity: Góc giữa 2 vector [-1, 1] (Càng gần 1 càng giống nhau).
      + Euclidean Distance (L2): Khoảng cách thẳng giữa 2 đầu mút vector.
      + Dot Product: Tích vô hướng (nếu vector đã chuẩn hóa thì bằng Cosine).
"""

import math
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
from dotenv import load_dotenv

# Tìm và nạp .env từ root
root_dir = Path(__file__).resolve().parent.parent
env_path = root_dir / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


class VectorWordComparator:
    """So sánh biểu diễn vector của hai từ trong không gian đa chiều."""
    # Phải chọn mô hình phù hợp. vì dụ kiểm tra xem mô hình đó có xử lý được tiếng việt hay ko 
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model_name = model_name
        self._model = None
        self._mode = "uninitialized"

    def _load_model(self):
        """Khởi tạo mô hình Embedding (ưu tiên SentenceTransformers, fallback sang Offline Vector)."""
        if self._model is not None:
            return

        try:
            from sentence_transformers import SentenceTransformer

            print(f"⏳ Đang tải mô hình SentenceTransformer ('{self.model_name}')...")
            self._model = SentenceTransformer(self.model_name)
            self._mode = f"SentenceTransformer ({self.model_name})"
            print("✅ Mô hình đã sẵn sàng!")
        except Exception as e:
            print(f"ℹ️ Không thể tải online model ({e}). Sử dụng chế độ Offline Semantic Vector.")
            self._mode = "Offline Deterministic Embedding"

    def get_vector(self, text: str) -> np.ndarray:
        """Tạo vector nhúng cho một từ hoặc cụm từ."""
        self._load_model()

        if self._model is not None:
            # Model SentenceTransformer trả về vector 384 chiều
            embedding = self._model.encode(text, normalize_embeddings=True)
            return np.array(embedding, dtype=np.float32)

        # Fallback Vector Generator nếu không có model / offline
        return self._offline_embedding(text)

    def _offline_embedding(self, text: str, dim: int = 128) -> np.ndarray:
        """Tạo vector giả lập dựa trên n-gram và ngữ nghĩa để test offline."""
        import hashlib

        vector = np.zeros(dim, dtype=np.float32)
        text_clean = text.lower().strip()

        # Băm toàn bộ từ
        base_hash = int(hashlib.md5(text_clean.encode("utf-8")).hexdigest(), 16)
        vector[base_hash % dim] += 2.0

        # Băm từng ký tự / n-gram để giữ tính tương quan hình thái
        for i in range(len(text_clean)):
            idx = (base_hash + ord(text_clean[i]) * 31 + i) % dim
            vector[idx] += 1.0

        # Chuẩn hóa vector đơn vị L2 (L2 Norm = 1.0)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector

    @staticmethod
    def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
        """Tính Cosine Similarity giữa 2 vector: cos(θ) = (v1 · v2) / (||v1|| * ||v2||)."""
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(v1, v2) / (norm1 * norm2))

    @staticmethod
    def euclidean_distance(v1: np.ndarray, v2: np.ndarray) -> float:
        """Tính khoảng cách Euclidean (L2 Distance): ||v1 - v2||_2."""
        return float(np.linalg.norm(v1 - v2))

    @staticmethod
    def evaluate_similarity(score: float) -> str:
        """Diễn giải ý nghĩa của điểm Cosine Similarity."""
        if score >= 0.85:
            return "🟢 Rất tương đồng (Đồng nghĩa / Cùng khái niệm chặt chẽ)"
        elif score >= 0.60:
            return "🟡 Tương đồng khá (Cùng chủ đề / Trường từ vựng liên quan)"
        elif score >= 0.35:
            return "🟠 Có liên quan nhẹ (Khác nhóm nhưng chung ngữ cảnh xa)"
        else:
            return "🔴 Khác biệt / Không liên quan (Ngữ nghĩa cách xa nhau)"

    def compare(self, word1: str, word2: str) -> Dict[str, Any]:
        """Thực hiện so sánh chi tiết vector giữa hai từ."""
        v1 = self.get_vector(word1)
        v2 = self.get_vector(word2)

        cosine = self.cosine_similarity(v1, v2)
        euclidean = self.euclidean_distance(v1, v2)
        dot_prod = float(np.dot(v1, v2))

        return {
            "word1": word1,
            "word2": word2,
            "dimension": len(v1),
            "vector1_sample": v1[:5].tolist(),  # 5 chiều đầu tiên
            "vector2_sample": v2[:5].tolist(),
            "cosine_similarity": cosine,
            "euclidean_distance": euclidean,
            "dot_product": dot_prod,
            "assessment": self.evaluate_similarity(cosine),
            "engine": self._mode,
        }

    def print_result(self, word1: str, word2: str) -> None:
        """In kết quả so sánh đẹp mắt dạng bảng."""
        res = self.compare(word1, word2)

        print("\n" + "=" * 65)
        print(f"🔬 SO SÁNH VECTOR: 「{word1}」 ⟷ 「{word2}」")
        print("=" * 65)
        print(f"⚙️  Mô hình Vector: {res['engine']}")
        print(f"📐 Số chiều (Dimensions): {res['dimension']} chiều")
        print(f"🔹 Vector 1 ('{word1}') [5 chiều đầu]: {[round(x, 4) for x in res['vector1_sample']]}...")
        print(f"🔹 Vector 2 ('{word2}') [5 chiều đầu]: {[round(x, 4) for x in res['vector2_sample']]}...")
        print("-" * 65)
        print("📊 CÁC CHỈ SỐ TOÁN HỌC:")
        print(f"   1. Cosine Similarity : {res['cosine_similarity']:+.4f}  (Thang đo: [-1.0 đến +1.0])")
        print(f"   2. Euclidean Distance: {res['euclidean_distance']:.4f}   (Khoảng cách L2)")
        print(f"   3. Dot Product       : {res['dot_product']:+.4f}")
        print("-" * 65)
        print(f"🎯 Đánh giá ngữ nghĩa  : {res['assessment']}")
        print("=" * 65)


def run_demo():
    """Chạy các cặp từ mẫu để quan sát sự khác biệt không gian vector."""
    comparator = VectorWordComparator()

    sample_pairs = [
        ("ô tô", "xe hơi"),        # Đồng nghĩa Tiếng Việt (Xe cộ)
        ("vua", "hoàng đế"),       # Rất tương đồng (Synonyms)
        ("chó", "mèo"),            # Cùng trường nghĩa động vật
        ("bác sĩ", "bệnh viện"),   # Liên quan ngữ cảnh
        ("máy tính", "quả chuối"),  # Hoàn toàn không liên quan
    ]

    print("\n🚀 CHẠY THỬ NGHIỆM CÁC CẶP TỪ TIÊU BIỂU:")
    for w1, w2 in sample_pairs:
        comparator.print_result(w1, w2)


def interactive_loop():
    """Cho phép người dùng tự gõ 2 từ bất kỳ để so sánh."""
    comparator = VectorWordComparator()

    print("\n" + "=" * 65)
    print("⌨️  CHẾ ĐỘ TƯƠNG TÁC: NHẬP 2 TỪ ĐỂ SO SÁNH VECTOR")
    print("💡 Gõ 'exit', 'quit' hoặc 'q' để dừng chương trình.")
    print("=" * 65)

    while True:
        try:
            w1 = input("\n👉 Nhập từ thứ nhất: ").strip()
            if w1.lower() in ("exit", "quit", "q"):
                break
            if not w1:
                continue

            w2 = input("👉 Nhập từ thứ hai : ").strip()
            if w2.lower() in ("exit", "quit", "q"):
                break
            if not w2:
                continue

            comparator.print_result(w1, w2)

        except (KeyboardInterrupt, EOFError):
            break

    print("\n👋 Đã kết thúc chương trình so sánh vector.")


if __name__ == "__main__":
    # Nếu truyền tham số dòng lệnh: python compare_vectors.py <từ1> <từ2>
    if len(sys.argv) == 3:
        comp = VectorWordComparator()
        comp.print_result(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] == "--interactive":
        interactive_loop()
    else:
        # Mặc định chạy demo rồi mở interactive loop
        run_demo()
        interactive_loop()
