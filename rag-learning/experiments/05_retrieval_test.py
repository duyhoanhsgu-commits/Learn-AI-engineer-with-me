"""
Experiment: 05_retrieval_test.py
Thực nghiệm Pre-retrieval: Rewrite câu hỏi mơ hồ và tìm kiếm tài liệu tương ứng.
"""

import sys
from pathlib import Path

# Thêm thư mục rag-learning vào sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.retrieval.pre_retrieval import PreRetrievalProcessor
from src.vectorstore.vector_store import SimpleVectorStore


def main():
    print("=" * 65)
    print("🧪 EXPERIMENT 05: PRE-RETRIEVAL & SEARCH PIPELINE TEST")
    print("=" * 65)

    processor = PreRetrievalProcessor()
    store = SimpleVectorStore()

    # Tạo kho dữ liệu mẫu
    documents = [
        {"chunk_id": "c1", "content": "Thuật toán HNSW xây dựng đồ thị nhiều tầng giúp tìm kiếm láng giềng gần nhất cực nhanh."},
        {"chunk_id": "c2", "content": "RAG kết hợp cơ sở tri thức giúp LLM hạn chế ảo giác và nâng cao độ chính xác."},
        {"chunk_id": "c3", "content": "Chính sách nghỉ phép của công ty quy định mỗi nhân viên có 12 ngày phép năm."},
    ]
    store.add_documents(documents)

    # Tình huống: Người dùng đang chat và hỏi câu mơ hồ
    conversation = [
        {"role": "user", "content": "HNSW là gì?"},
        {"role": "assistant", "content": "HNSW là cấu trúc đồ thị vector ANN."},
    ]
    ambiguous_query = "Nó có ưu điểm gì so với tìm kiếm truyền thống?"

    print(f"\n1. Câu hỏi gốc của người dùng: '{ambiguous_query}'")
    rewritten_query = processor.rewrite_query(ambiguous_query, conversation_history=conversation)
    print(f"2. Sau Pre-retrieval (Rewrite): '{rewritten_query}'")

    print("\n3. Kết quả tìm kiếm trong Vector Store:")
    results = store.search(rewritten_query, top_k=1)
    for r in results:
        print(f"-> Điểm: {r['score']:+.4f} | ID: {r['id']} | Nội dung: {r['text']}")

    print("\n" + "=" * 65)
    print("✅ Hoàn thành thực nghiệm Pre-Retrieval!")


if __name__ == "__main__":
    main()
