"""
Experiment: 06_hybrid_search_test.py
Thực nghiệm kiểm chứng Search Methods & Rank Fusion:
So sánh độ chính xác khi dùng Dense Vector thuần túy vs Hybrid Search (Dense + BM25 + RRF).
"""

import sys
from pathlib import Path

# Đảm bảo import được module từ rag-learning
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.retrieval.hybrid_search import HybridSearchEngine


def main():
    print("=" * 70)
    print("🧪 EXPERIMENT 06: HYBRID SEARCH & RECIPROCAL RANK FUSION (RRF)")
    print("=" * 70)

    engine = HybridSearchEngine()

    # Dữ liệu tài liệu thử nghiệm
    documents = [
        {
            "chunk_id": "doc_kb_01",
            "content": "Để xử lý sự cố mạng nội bộ, quản trị viên cần kiểm tra cáp mạng và khởi động router.",
            "metadata": {"category": "it_support", "access_level": "public"},
        },
        {
            "chunk_id": "doc_kb_02",
            "content": "Lỗi mã ERR_AUTH_403_FORBIDDEN xuất hiện khi token JWT của người dùng đã hết hạn hoặc không có quyền.",
            "metadata": {"category": "security", "access_level": "internal"},
        },
        {
            "chunk_id": "doc_kb_03",
            "content": "Chính sách bảo mật hệ thống: Tuyệt đối không chia sẻ tài khoản có mã ERR_AUTH_403_FORBIDDEN cho bên thứ ba.",
            "metadata": {"category": "policy", "access_level": "confidential"},
        },
        {
            "chunk_id": "doc_kb_04",
            "content": "Hướng dẫn cấu hình kết nối database PostgreSQL và tối ưu connection pool.",
            "metadata": {"category": "database", "access_level": "internal"},
        },
    ]

    print("\n1. Đánh chỉ mục tài liệu (Dense Vector + BM25 Lexical)...")
    engine.index(documents)

    # Thử nghiệm 1: Tìm kiếm từ khóa mã lỗi kỹ thuật kết hợp ngữ cảnh
    query_1 = "Làm sao khi gặp lỗi ERR_AUTH_403_FORBIDDEN token hết hạn?"
    print(f"\n2. Thử nghiệm Truy vấn 1: '{query_1}'")
    results_1 = engine.search(query_1, top_k=2)

    for rank, item in enumerate(results_1, 1):
        print(f"   [{rank}] RRF Score: {item['rrf_score']} | ID: {item['chunk_id']}")
        print(f"       Nội dung: {item['content']}")

    # Thử nghiệm 2: Lọc trước theo Metadata (Pre-filtering)
    query_2 = "quy định và chính sách bảo mật"
    print(f"\n3. Thử nghiệm Truy vấn 2 kèm Metadata Filter (category='policy'): '{query_2}'")
    results_2 = engine.search(query_2, top_k=2, filter_dict={"category": "policy"})

    for rank, item in enumerate(results_2, 1):
        print(f"   [{rank}] RRF Score: {item['rrf_score']} | ID: {item['chunk_id']}")
        print(f"       Nội dung: {item['content']}")
        print(f"       Metadata: {item['metadata']}")

    print("\n" + "=" * 70)
    print("✅ Hoàn thành thực nghiệm Search Methods & Rank Fusion!")


if __name__ == "__main__":
    main()
