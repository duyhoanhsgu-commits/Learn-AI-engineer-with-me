"""
Module: src/ingestion/metadata.py
Mục đích: Làm giàu dữ liệu Metadata (Metadata Enrichment) cho các Chunk trong RAG.
Biến mỗi chunk văn bản thô thành một đối tượng tri thức có ngữ cảnh, nguồn gốc,
quyền hạn và hỗ trợ Contextual Retrieval (ngăn ngừa orphan chunks).
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


def enrich_chunk(
    chunk: Dict[str, Any],
    doc_metadata: Dict[str, Any],
    chunk_index: int,
    total_chunks: int,
) -> Dict[str, Any]:
    """
    Làm giàu một chunk riêng lẻ với thông tin nguồn, vị trí và quyền truy cập.
    """
    doc_id = doc_metadata.get("doc_id", "doc_unknown")
    doc_title = doc_metadata.get("doc_title", "Tài liệu không tên")
    section = chunk.get("header") or doc_metadata.get("section", "Chung")
    content = chunk.get("content", "").strip()

    # 1. Định danh duy nhất cho chunk
    chunk_id = f"{doc_id}_c{chunk_index:04d}"

    # 2. Xây dựng bộ metadata hoàn chỉnh
    enriched_metadata = {
        # Định danh & Nguồn gốc (Provenance)
        "chunk_id": chunk_id,
        "doc_id": doc_id,
        "doc_title": doc_title,
        "source_file": doc_metadata.get("source_file", ""),
        "author": doc_metadata.get("author", "Hệ thống"),
        "created_at": doc_metadata.get("created_at", datetime.now().strftime("%Y-%m-%d")),
        
        # Ngữ cảnh cấu trúc (Structure)
        "section": section,
        "chunk_index": chunk_index,
        "total_chunks": total_chunks,
        "strategy": chunk.get("strategy", "unknown"),
        
        # Thống kê văn bản
        "char_count": len(content),
        "word_count": len(content.split()),
        
        # Phân quyền & Lọc (Access Control & Filtering)
        "access_level": doc_metadata.get("access_level", "public"),
        "category": doc_metadata.get("category", "general"),
    }

    # 3. Context Injection (Tạo văn bản có ngữ cảnh dùng riêng để Embed vector)
    # Giúp chunk không bị mồ côi (orphan chunk) khi đứng một mình
    contextual_text = f"[Tài liệu: {doc_title} | Mục: {section}]\n{content}"

    return {
        "chunk_id": chunk_id,
        "content": content,
        "contextual_text": contextual_text,
        "metadata": enriched_metadata,
    }


def enrich_document_chunks(
    chunks: List[Dict[str, Any]],
    doc_metadata: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Làm giàu hàng loạt danh sách các chunk của một tài liệu.
    """
    total = len(chunks)
    enriched_list = []

    for idx, c in enumerate(chunks):
        enriched = enrich_chunk(
            chunk=c,
            doc_metadata=doc_metadata,
            chunk_index=idx + 1,
            total_chunks=total,
        )
        enriched_list.append(enriched)

    return enriched_list


if __name__ == "__main__":
    print("=== DEMO METADATA ENRICHMENT ===")

    # Giả lập metadata của tài liệu gốc
    doc_info = {
        "doc_id": "rag_tutorial_2026",
        "doc_title": "Giáo trình RAG Toàn diện",
        "source_file": "ALL_RAG.md",
        "author": "AI Team",
        "access_level": "student",
        "category": "Education",
    }

    # Giả lập 2 chunk thô thu được từ bước chunking
    raw_chunks = [
        {
            "header": "Chương 1: Foundation & Evolution",
            "strategy": "structure_aware",
            "content": "Cosine Similarity đo góc giữa hai vector để xác định mức độ tương đồng ngữ nghĩa.",
        },
        {
            "header": "Chương 2: Ingestion Pipeline",
            "strategy": "structure_aware",
            "content": "Metadata Enrichment bổ sung thông tin xuất xứ và phân quyền vào từng chunk.",
        },
    ]

    # Thực hiện làm giàu metadata
    enriched_results = enrich_document_chunks(raw_chunks, doc_info)

    for item in enriched_results:
        print("\n" + "-" * 60)
        print(f"📌 CHUNK ID: {item['chunk_id']}")
        print(f"📄 Nội dung: {item['content']}")
        print(f"🏷️  Contextual Text (Dùng để Embed):")
        print(f"   {item['contextual_text']}")
        print("📊 Metadata đính kèm:")
        for k, v in item["metadata"].items():
            print(f"   - {k}: {v}")
