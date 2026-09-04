"""
Module: src/retrieval/hybrid_search.py
Mục đích: Triển khai Search Methods & Rank Fusion trong RAG:
   1. Dense Vector Search (Ngữ nghĩa dựa trên Embedding)
   2. BM25 Search (Từ khóa chính xác / Mã định danh / Thuật ngữ)
   3. Reciprocal Rank Fusion (RRF) (Hợp nhất thứ hạng không phụ thuộc thang điểm)
   4. Metadata Filtering (Lọc trước theo thuộc tính / phân quyền)
"""

import math
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

# Đảm bảo import được module trong rag-learning khi chạy trực tiếp file
rag_dir = Path(__file__).resolve().parent.parent.parent
if str(rag_dir) not in sys.path:
    sys.path.insert(0, str(rag_dir))

try:
    from src.vectorstore.vector_store import SimpleVectorStore
except ImportError:
    from vectorstore.vector_store import SimpleVectorStore


# =====================================================================
# 1. BM25 RETRIEVER (TÌM KIẾM THEO TỪ KHÓA CHUẨN XÁC)
# =====================================================================
class BM25Retriever:
    """Thuật toán BM25 (Best Matching 25) thuần Python, phục vụ Lexical Search."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = 0
        self.avg_doc_len = 0.0
        self.doc_lens: List[int] = []
        self.doc_freqs: Dict[str, int] = {}  # Số tài liệu chứa từ t
        self.doc_term_counts: List[Dict[str, int]] = []  # Tần suất từ trong từng doc

    def _tokenize(self, text: str) -> List[str]:
        return [w.lower() for w in re.findall(r"\w+", text)]

    def fit(self, documents: List[str]) -> None:
        """Huấn luyện thống kê TF, DF và độ dài tài liệu trung bình."""
        self.corpus_size = len(documents)
        if self.corpus_size == 0:
            return

        self.doc_lens = []
        self.doc_freqs = {}
        self.doc_term_counts = []

        total_words = 0
        for doc in documents:
            tokens = self._tokenize(doc)
            self.doc_lens.append(len(tokens))
            total_words += len(tokens)

            term_counts: Dict[str, int] = {}
            for t in tokens:
                term_counts[t] = term_counts.get(t, 0) + 1
            self.doc_term_counts.append(term_counts)

            for t in set(tokens):
                self.doc_freqs[t] = self.doc_freqs.get(t, 0) + 1

        self.avg_doc_len = total_words / self.corpus_size if self.corpus_size > 0 else 1.0

    def get_scores(self, query: str) -> List[float]:
        """Tính điểm BM25 cho tất cả các tài liệu trong tập."""
        query_tokens = self._tokenize(query)
        scores = [0.0] * self.corpus_size

        for token in query_tokens:
            if token not in self.doc_freqs:
                continue

            # Tính IDF theo công thức chuẩn BM25
            df = self.doc_freqs[token]
            idf = math.log((self.corpus_size - df + 0.5) / (df + 0.5) + 1.0)

            for doc_idx, term_counts in enumerate(self.doc_term_counts):
                tf = term_counts.get(token, 0)
                if tf == 0:
                    continue
                doc_len = self.doc_lens[doc_idx]
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                scores[doc_idx] += idf * (numerator / denominator)

        return scores


# =====================================================================
# 2. RECIPROCAL RANK FUSION (RRF)
# =====================================================================
def reciprocal_rank_fusion(
    ranked_lists: List[List[str]],
    k: int = 60,
) -> List[Tuple[str, float]]:
    """
    Thuật toán RRF:
       RRF_score(d) = SUM( 1 / (k + rank_m(d)) )
    - ranked_lists: Danh sách các ID tài liệu đã được sắp xếp từ các bộ tìm kiếm.
    - k: Hằng số làm mượt xếp hạng (mặc định = 60 theo tiêu chuẩn công nghiệp).
    """
    rrf_scores: Dict[str, float] = {}

    for doc_list in ranked_lists:
        for rank, doc_id in enumerate(doc_list, start=1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    # Sắp xếp giảm dần theo điểm RRF
    sorted_ranks = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_ranks


# =====================================================================
# 3. HYBRID SEARCH ENGINE (DENSE + BM25 + RRF)
# =====================================================================
class HybridSearchEngine:
    """Hệ thống tìm kiếm kết hợp hoàn chỉnh: Dense Vector + BM25 + RRF."""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.vector_store = SimpleVectorStore(model_name=model_name)
        self.bm25 = BM25Retriever()
        self.documents: List[Dict[str, Any]] = []

    def index(self, chunks: List[Dict[str, Any]]) -> None:
        """Đánh chỉ mục đồng thời cho cả Dense Vector Store và BM25."""
        self.documents = chunks
        self.vector_store.add_documents(chunks)

        # Huấn luyện BM25 trên nội dung text của các chunk
        corpus_texts = [c.get("content", "") for c in chunks]
        self.bm25.fit(corpus_texts)
        print("✅ Đã hoàn tất Indexing cho cả Dense Vector và BM25!")

    def search(
        self,
        query: str,
        top_k: int = 3,
        filter_dict: Optional[Dict[str, Any]] = None,
        rrf_k: int = 60,
    ) -> List[Dict[str, Any]]:
        """
        Thực thi Hybrid Search:
        1. Lọc trước theo metadata (nếu có).
        2. Chạy Dense Vector Search.
        3. Chạy BM25 Lexical Search.
        4. Hợp nhất kết quả bằng Reciprocal Rank Fusion (RRF).
        """
        if not self.documents:
            return []

        # Áp dụng Metadata Pre-filtering
        valid_indices = []
        for idx, doc in enumerate(self.documents):
            meta = doc.get("metadata", {})
            if filter_dict:
                if all(meta.get(k) == v for k, v in filter_dict.items()):
                    valid_indices.append(idx)
            else:
                valid_indices.append(idx)

        if not valid_indices:
            return []

        # 1. Dense Vector Search (Lấy danh sách ID đã xếp hạng)
        dense_results = self.vector_store.search(query, top_k=len(self.documents), filter_dict=filter_dict)
        dense_ranked_ids = [item["id"] for item in dense_results]

        # 2. BM25 Search (Lấy danh sách ID đã xếp hạng)
        bm25_all_scores = self.bm25.get_scores(query)
        bm25_filtered = [(self.documents[idx]["chunk_id"], bm25_all_scores[idx]) for idx in valid_indices]
        # Sắp xếp giảm dần theo điểm BM25
        bm25_filtered.sort(key=lambda x: x[1], reverse=True)
        bm25_ranked_ids = [doc_id for doc_id, score in bm25_filtered if score > 0]

        # 3. Hợp nhất bằng RRF
        fused_rankings = reciprocal_rank_fusion([dense_ranked_ids, bm25_ranked_ids], k=rrf_k)

        # 4. Gom dữ liệu kết quả hoàn chỉnh
        doc_lookup = {d["chunk_id"]: d for d in self.documents}
        final_results = []

        for doc_id, rrf_score in fused_rankings[:top_k]:
            doc_data = doc_lookup.get(doc_id, {})
            final_results.append({
                "chunk_id": doc_id,
                "rrf_score": round(rrf_score, 6),
                "content": doc_data.get("content", ""),
                "metadata": doc_data.get("metadata", {}),
            })

        return final_results


if __name__ == "__main__":
    print("=== DEMO HYBRID SEARCH & RANK FUSION (RRF) ===")

    # Dữ liệu kiểm thử: vừa có ngữ nghĩa tự nhiên, vừa có mã lỗi kỹ thuật
    sample_dataset = [
        {
            "chunk_id": "doc_01",
            "content": "Lỗi ERR_502_GATEWAY_TIMEOUT xảy ra khi máy chủ trung gian không nhận được phản hồi kịp thời.",
            "metadata": {"type": "technical", "system": "gateway"},
        },
        {
            "chunk_id": "doc_02",
            "content": "Để khắc phục sự cố mạng và kết nối chậm, hãy kiểm tra proxy và khởi động lại dịch vụ.",
            "metadata": {"type": "guide", "system": "network"},
        },
        {
            "chunk_id": "doc_03",
            "content": "Chính sách bảo mật quy định mã lỗi ERR_502_GATEWAY_TIMEOUT phải được ghi log đầy đủ.",
            "metadata": {"type": "policy", "system": "gateway"},
        },
    ]

    engine = HybridSearchEngine()
    engine.index(sample_dataset)

    # Thử nghiệm truy vấn kết hợp: Mã lỗi cụ thể (cần BM25) + Diễn đạt tự nhiên (cần Vector)
    test_query = "Nguyên nhân gây ra lỗi ERR_502_GATEWAY_TIMEOUT là gì?"
    print(f"\n🔍 Truy vấn: '{test_query}'")

    results = engine.search(test_query, top_k=2)
    for rank, item in enumerate(results, 1):
        print(f"\n[{rank}] Điểm RRF: {item['rrf_score']} | ID: {item['chunk_id']}")
        print(f"    Nội dung: {item['content']}")
        print(f"    Metadata: {item['metadata']}")
