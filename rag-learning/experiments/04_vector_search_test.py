"""
Experiment: 04_vector_search_test.py
Thực nghiệm Vector Indexing và Semantic Similarity Search kết hợp lọc Metadata.
"""

import sys
from pathlib import Path

# Thêm thư mục rag-learning vào sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.vectorstore.vector_store import SimpleVectorStore


def main():
    print("=" * 65)
    print("🧪 EXPERIMENT 04: VECTOR INDEXING & SEARCH TEST")
    print("=" * 65)

    store = SimpleVectorStore()

    dataset = [
        {
            "chunk_id": "c1",
            "content": "Phở bò và bún chả là những món ăn truyền thống đặc sắc của Hà Nội.",
            "metadata": {"topic": "ẩm thực", "location": "Hà Nội"},
        },
        {
            "chunk_id": "c2",
            "content": "Học máy và học sâu là hai nhánh con quan trọng của trí tuệ nhân tạo.",
            "metadata": {"topic": "công nghệ", "location": "toàn cầu"},
        },
        {
            "chunk_id": "c3",
            "content": "Bánh mì kẹp thịt và cà phê sữa đá rất phổ biến tại Sài Gòn.",
            "metadata": {"topic": "ẩm thực", "location": "Sài Gòn"},
        },
    ]

    # Indexing
    store.add_documents(dataset)

    # Search
    query = "Món ăn ngon miền bắc"
    print(f"\n🔍 Truy vấn: '{query}'")
    results = store.search(query, top_k=2)

    for r in results:
        print(f"-> Điểm: {r['score']:+.4f} | ID: {r['id']} | Chủ đề: {r['metadata']['topic']}")
        print(f"   Văn bản: {r['text']}")

    print("\n" + "=" * 65)
    print("✅ Hoàn thành thực nghiệm Vector Indexing & Search!")


if __name__ == "__main__":
    main()
