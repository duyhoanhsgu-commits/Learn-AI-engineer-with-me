"""
Experiment: 07_rerank_test.py
Thực nghiệm kiểm chứng Two-Stage Retrieval:
Giai đoạn 1 (Fast Retrieval): Hybrid Search (Dense Vector + BM25) lấy Top 5 ứng viên.
Giai đoạn 2 (Reranking): Cross-Encoder chắt lọc và sắp xếp lại để đưa Top 2 chuẩn xác nhất vào LLM.
"""

import sys
from pathlib import Path

# Đảm bảo import được module từ rag-learning
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.retrieval.hybrid_search import HybridSearchEngine
from src.retrieval.reranker import CrossEncoderReranker


def main():
    print("=" * 70)
    print("🧪 EXPERIMENT 07: TWO-STAGE RETRIEVAL (HYBRID SEARCH + CROSS-ENCODER)")
    print("=" * 70)

    # 1. Khởi tạo Pipeline
    hybrid_engine = HybridSearchEngine()
    reranker = CrossEncoderReranker()

    # Dữ liệu tài liệu kiểm thử
    documents = [
        {
            "chunk_id": "doc_01",
            "content": "Chính sách nghỉ phép: Nhân viên chính thức được hưởng 12 ngày phép năm và được thanh toán lương đầy đủ.",
            "metadata": {"topic": "leave_policy"},
        },
        {
            "chunk_id": "doc_02",
            "content": "Quy trình xin nghỉ ốm: Nhân viên cần nộp giấy xác nhận của bệnh viện cho phòng Nhân sự trong vòng 48 giờ.",
            "metadata": {"topic": "leave_sick"},
        },
        {
            "chunk_id": "doc_03",
            "content": "Để nộp đơn xin nghỉ phép năm trên cổng thông tin nội bộ, hãy vào mục Nhân sự -> Quản lý ngày nghỉ -> Tạo yêu cầu nghỉ phép mới.",
            "metadata": {"topic": "leave_guide"},
        },
        {
            "chunk_id": "doc_04",
            "content": "Lịch nghỉ lễ Tết Nguyên Đán và các ngày nghỉ lễ theo quy định của nhà nước hàng năm.",
            "metadata": {"topic": "holiday"},
        },
        {
            "chunk_id": "doc_05",
            "content": "Hệ thống cổng thông tin nhân sự bảo trì vào ngày thứ Bảy cuối tuần đầu tiên của tháng.",
            "metadata": {"topic": "system_maintenance"},
        },
    ]

    print("\n📦 Đang nạp và đánh chỉ mục tài liệu...")
    hybrid_engine.index(documents)

    query = "Làm sao để làm thủ tục xin nghỉ phép năm trên hệ thống?"
    print(f"\n🔍 CÂU HỎI TRUY VẤN: '{query}'")

    # Giai đoạn 1: Fast Retrieval (Recall cao, lấy Top 4 ứng viên)
    print("\n--- GIAI ĐOẠN 1: HYBRID SEARCH (DENSE + BM25 + RRF) ---")
    candidates = hybrid_engine.search(query, top_k=4)
    for rank, doc in enumerate(candidates, 1):
        print(f"[{rank}] ID: {doc['chunk_id']} | RRF Score: {doc['rrf_score']:.6f}")
        print(f"    Nội dung: {doc['content'][:80]}...")

    # Giai đoạn 2: Precise Reranking (Precision cao, chắt lọc Top 2 cho LLM)
    print("\n--- GIAI ĐOẠN 2: CROSS-ENCODER RERANKING ---")
    reranked = reranker.rerank(query, candidates, top_k=2)
    for rank, doc in enumerate(reranked, 1):
        print(f"[{rank}] ID: {doc['chunk_id']} | Điểm Rerank: {doc['rerank_score']:+.4f} (Thứ hạng ban đầu: #{doc['original_rank']})")
        print(f"    Nội dung: {doc['content']}")

    print("\n" + "=" * 70)
    print("✅ Hoàn thành thực nghiệm Two-Stage Retrieval với Cross-Encoder!")


if __name__ == "__main__":
    main()
