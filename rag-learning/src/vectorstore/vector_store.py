"""
Module: src/vectorstore/vector_store.py
Mục đích: Triển khai Vector Indexing và Tìm kiếm tương đồng ngữ nghĩa (Vector Search).
Cấu trúc bản ghi:
   {
       "id": chunk_id,
       "vector": np.ndarray (Dense Vector),
       "text": chunk_content,
       "metadata": dict (doc_title, section, access_level, ...)
   }
Hỗ trợ:
   - Vector Indexing (Đánh chỉ mục vector tự động).
   - Metadata Pre-filtering (Lọc theo metadata trước khi tìm kiếm).
   - Cosine Similarity Search (Tìm top_k kết quả phù hợp nhất).
   - Lưu trữ / Nạp index từ file đĩa (Persistence).
"""

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import numpy as np


class SimpleVectorStore:
    """Kho lưu trữ vector đơn giản, hỗ trợ đánh chỉ mục và tìm kiếm ngữ nghĩa."""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model_name = model_name
        self._model = None
        self.records: List[Dict[str, Any]] = []

    def _get_model(self):
        """Khởi tạo embedding model một lần duy nhất."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except Exception:
                self._model = None
        return self._model

    def embed_text(self, text: str) -> np.ndarray:
        """Tạo vector embedding chuẩn hóa (L2 normalized) cho văn bản."""
        model = self._get_model()
        if model is not None:
            vec = model.encode(text, normalize_embeddings=True)
            return np.array(vec, dtype=np.float32)

        # Fallback offline embedding nếu không có thư viện/internet
        import hashlib
        dim = 128
        vec = np.zeros(dim, dtype=np.float32)
        words = text.lower().split()
        for w in words:
            idx = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16) % dim
            vec[idx] += 1.0
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    def add_documents(self, chunks: List[Dict[str, Any]]) -> None:
        """
        Vector Indexing:
        1. Lấy nội dung text (hoặc contextual_text nếu có).
        2. Sinh vector embedding.
        3. Lưu trữ bản ghi hoàn chỉnh: {id, vector, text, metadata}.
        """
        print(f"📦 Đang đánh chỉ mục (Indexing) cho {len(chunks)} chunk dữ liệu...")

        for idx, chunk in enumerate(chunks):
            chunk_id = chunk.get("chunk_id", f"chunk_{len(self.records) + 1:04d}")
            text_to_embed = chunk.get("contextual_text") or chunk.get("content", "")
            raw_content = chunk.get("content", "")
            meta = chunk.get("metadata", {})

            # Sinh vector embedding
            vector = self.embed_text(text_to_embed)

            record = {
                "id": chunk_id,
                "vector": vector,
                "text": raw_content,
                "metadata": meta,
            }
            self.records.append(record)

        print(f"✅ Đã đánh chỉ mục thành công! Tổng số bản ghi trong kho: {len(self.records)}")

    def search(
        self,
        query: str,
        top_k: int = 3,
        filter_dict: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Tìm kiếm vector kết hợp lọc Metadata (Pre-filtering):
        1. Tạo vector cho câu hỏi truy vấn.
        2. Lọc các bản ghi thỏa mãn điều kiện metadata (nếu có).
        3. Tính Cosine Similarity và trả về top_k văn bản phù hợp nhất.
        """
        if not self.records:
            return []

        # 1. Tạo embedding cho câu truy vấn
        query_vec = self.embed_text(query)

        # 2. Lọc theo metadata (Pre-filtering)
        candidate_records = self.records
        if filter_dict:
            candidate_records = [
                r for r in candidate_records
                if all(r["metadata"].get(k) == v for k, v in filter_dict.items())
            ]

        if not candidate_records:
            return []

        # 3. Tính Cosine Similarity
        results = []
        for r in candidate_records:
            doc_vec = r["vector"]
            # Vì vector đã được normalize L2 nên tích vô hướng chính là Cosine Similarity
            score = float(np.dot(query_vec, doc_vec))
            results.append({
                "id": r["id"],
                "score": round(score, 4),
                "text": r["text"],
                "metadata": r["metadata"],
            })

        # Sắp xếp giảm dần theo điểm số
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def save_to_file(self, filepath: str) -> None:
        """Lưu toàn bộ index và metadata ra file JSON."""
        serializable = []
        for r in self.records:
            serializable.append({
                "id": r["id"],
                "vector": r["vector"].tolist(),
                "text": r["text"],
                "metadata": r["metadata"],
            })
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"💾 Đã lưu vector index vào: {filepath}")

    def load_from_file(self, filepath: str) -> None:
        """Nạp vector index từ file JSON."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Không tìm thấy file index: {filepath}")

        data = json.loads(path.read_text(encoding="utf-8"))
        self.records = []
        for item in data:
            self.records.append({
                "id": item["id"],
                "vector": np.array(item["vector"], dtype=np.float32),
                "text": item["text"],
                "metadata": item["metadata"],
            })
        print(f"📥 Đã nạp thành công {len(self.records)} bản ghi từ {filepath}")


if __name__ == "__main__":
    print("=== DEMO VECTOR INDEXING & SEARCH ===")

    store = SimpleVectorStore()

    # Dữ liệu chunk mẫu đã qua bước Parsing & Metadata Enrichment
    sample_chunks = [
        {
            "chunk_id": "rag_c001",
            "content": "RAG kết hợp cơ sở tri thức bên ngoài để giúp LLM trả lời chính xác, giảm thiểu ảo giác.",
            "metadata": {"doc_id": "rag_intro", "section": "Khái niệm", "access_level": "public"},
        },
        {
            "chunk_id": "rag_c002",
            "content": "Cosine Similarity đo lường góc giữa hai vector để xác định mức độ tương đồng ngữ nghĩa.",
            "metadata": {"doc_id": "rag_math", "section": "Toán học", "access_level": "public"},
        },
        {
            "chunk_id": "rag_c003",
            "content": "Quy định bảo mật nội bộ nghiêm cấm chia sẻ khóa bí mật API ra bên ngoài.",
            "metadata": {"doc_id": "security_policy", "section": "Bảo mật", "access_level": "admin"},
        },
    ]

    # Bước 1: Vector Indexing (Đánh chỉ mục)
    store.add_documents(sample_chunks)

    # Bước 2: Tìm kiếm ngữ nghĩa (Vector Search)
    query = "Làm sao để đo độ tương đồng giữa hai văn bản?"
    print(f"\n🔍 Truy vấn: '{query}'")
    matches = store.search(query, top_k=2)

    for i, res in enumerate(matches, 1):
        print(f"\n[{i}] Điểm Cosine: {res['score']:+.4f} | ID: {res['id']}")
        print(f"    Nội dung : {res['text']}")
        print(f"    Mục      : {res['metadata'].get('section')} (Quyền: {res['metadata'].get('access_level')})")

    # Bước 3: Tìm kiếm có lọc Metadata (Pre-filtering theo access_level='admin')
    print("\n" + "-" * 60)
    print("🔒 Tìm kiếm với bộ lọc quyền truy cập: access_level = 'admin'")
    admin_matches = store.search("chính sách bảo mật", top_k=2, filter_dict={"access_level": "admin"})
    for res in admin_matches:
        print(f"-> Điểm: {res['score']:+.4f} | ID: {res['id']} | Nội dung: {res['text']}")
