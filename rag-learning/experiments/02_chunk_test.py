"""
Experiment: 02_chunk_test.py
Thực nghiệm so sánh 3 chiến lược Chunking trên cùng một tài liệu.
"""

import sys
from pathlib import Path

# Thêm thư mục rag-learning vào sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.ingestion.chunker import (
    fixed_size_chunking,
    semantic_chunking,
    structure_aware_chunking,
)


def main():
    print("=" * 65)
    print("🧪 EXPERIMENT 02: SO SÁNH 3 CHIẾN LƯỢC CHUNKING TRONG RAG")
    print("=" * 65)

    document = """# Kiến Trúc RAG Toàn Diện

## Giới Thiệu
RAG kết hợp cơ sở tri thức bên ngoài với LLM để hạn chế ảo giác. Quá trình này giúp mô hình trả lời chính xác hơn dựa trên tài liệu doanh nghiệp.

## Pipeline Ingestion
Quy trình nạp dữ liệu gồm parsing bóc tách văn bản, chunking phân mảnh tài liệu và embedding tạo vector. Mỗi bước đóng vai trò cốt lõi cho chất lượng tìm kiếm.

## Chiến Lược Chunking
Có 3 chiến lược chunking phổ biến: Fixed-size có overlap, Semantic Chunking theo ngữ nghĩa, và Structure-aware theo cấu trúc tiêu đề.
"""

    print("\n🔹 1. FIXED-SIZE WITH OVERLAP (size=25 từ, overlap=8 từ):")
    c1 = fixed_size_chunking(document, chunk_size=25, chunk_overlap=8)
    print(f"-> Tổng số chunk tạo ra: {len(c1)}")
    for c in c1:
        print(f"   [Chunk {c['chunk_id']}] ({c['metadata']['word_count']} từ): {c['content'][:70]}...")

    print("\n🔹 2. STRUCTURE-AWARE CHUNKING (Theo đề mục Markdown):")
    c2 = structure_aware_chunking(document)
    print(f"-> Tổng số chunk tạo ra: {len(c2)}")
    for c in c2:
        print(f"   [Chunk {c['chunk_id']} | Đề mục: '{c['header']}']: {c['content'][:70]}...")

    print("\n🔹 3. SEMANTIC CHUNKING (Dựa trên dịch chuyển ngữ nghĩa câu):")
    c3 = semantic_chunking(document, similarity_threshold=0.15)
    print(f"-> Tổng số chunk tạo ra: {len(c3)}")
    for c in c3:
        print(f"   [Chunk {c['chunk_id']} | Số câu: {c['metadata']['sentence_count']}]: {c['content'][:70]}...")

    print("\n" + "=" * 65)
    print("✅ Hoàn thành thực nghiệm 3 chiến lược Chunking!")


if __name__ == "__main__":
    main()
