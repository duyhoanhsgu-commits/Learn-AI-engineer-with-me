"""
Module: src/ingestion/chunker.py
Mục đích: Triển khai 3 chiến lược Chunking cốt lõi trong RAG:
   1. Fixed-size Chunking with Overlap (Kích thước cố định có gối đầu)
   2. Semantic Chunking (Băm nhỏ theo độ tương đồng ngữ nghĩa)
   3. Structure-Aware Chunking (Băm nhỏ theo phân cấp tiêu đề Markdown)
"""

import math
import re
from typing import Any, Callable, Dict, List, Optional


# =====================================================================
# 1. FIXED-SIZE CHUNKING WITH OVERLAP
# =====================================================================
def fixed_size_chunking(
    text: str,
    chunk_size: int = 150,
    chunk_overlap: int = 30,
) -> List[Dict[str, Any]]:
    """
    Chiến lược 1: Chia văn bản thành các khối có số từ cố định, kèm phần gối đầu.
    - chunk_size: Số từ trong mỗi chunk.
    - chunk_overlap: Số từ đệm lặp lại giữa 2 chunk liền kề để không rách ngữ cảnh.
    """
    words = text.split()
    if not words:
        return []

    if chunk_size <= chunk_overlap:
        raise ValueError("chunk_size phải lớn hơn chunk_overlap!")

    chunks: List[Dict[str, Any]] = []
    step = chunk_size - chunk_overlap
    idx = 0

    for i in range(0, len(words), step):
        chunk_words = words[i : i + chunk_size]
        chunk_text = " ".join(chunk_words)

        chunks.append({
            "chunk_id": idx,
            "strategy": "fixed_size_overlap",
            "content": chunk_text,
            "metadata": {
                "word_count": len(chunk_words),
                "start_word_idx": i,
                "end_word_idx": i + len(chunk_words),
            },
        })
        idx += 1

        # Nếu đã duyệt đến hết danh sách từ
        if i + chunk_size >= len(words):
            break

    return chunks


# =====================================================================
# 2. SEMANTIC CHUNKING
# =====================================================================
def _simple_similarity(s1: str, s2: str) -> float:
    """Tính độ tương đồng từ vựng/Jaccard nhẹ nhàng khi chạy offline."""
    w1 = set(s1.lower().split())
    w2 = set(s2.lower().split())
    if not w1 or not w2:
        return 0.0
    return len(w1 & w2) / len(w1 | w2)


def semantic_chunking(
    text: str,
    similarity_threshold: float = 0.4,
    embedding_fn: Optional[Callable[[str], Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Chiến lược 2: Băm nhỏ theo dịch chuyển ngữ nghĩa (Semantic Shift).
    - Tách đoạn thành từng câu.
    - Đo độ tương đồng ngữ nghĩa giữa câu i và câu i+1.
    - Khi điểm tương đồng rớt xuống dưới threshold -> Cắt sang chunk mới.
    """
    # Tách văn bản thành các câu độc lập
    raw_sentences = re.split(r"(?<=[.!?\n])\s+", text.strip())
    sentences = [s.strip() for s in raw_sentences if s.strip()]

    if not sentences:
        return []

    chunks: List[Dict[str, Any]] = []
    current_chunk_sentences: List[str] = [sentences[0]]
    idx = 0

    for i in range(len(sentences) - 1):
        s_current = sentences[i]
        s_next = sentences[i + 1]

        # Tính độ tương đồng giữa câu hiện tại và câu kế tiếp
        if embedding_fn is not None:
            try:
                import numpy as np
                v1 = np.array(embedding_fn(s_current))
                v2 = np.array(embedding_fn(s_next))
                score = float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
            except Exception:
                score = _simple_similarity(s_current, s_next)
        else:
            score = _simple_similarity(s_current, s_next)

        # Nếu độ tương đồng thấp hơn ngưỡng -> Chủ đề thay đổi -> Ngắt chunk
        if score < similarity_threshold:
            chunk_content = " ".join(current_chunk_sentences)
            chunks.append({
                "chunk_id": idx,
                "strategy": "semantic",
                "content": chunk_content,
                "metadata": {
                    "sentence_count": len(current_chunk_sentences),
                    "split_score": round(score, 4),
                },
            })
            idx += 1
            current_chunk_sentences = [s_next]
        else:
            current_chunk_sentences.append(s_next)

    # Thêm chunk cuối cùng còn lại
    if current_chunk_sentences:
        chunk_content = " ".join(current_chunk_sentences)
        chunks.append({
            "chunk_id": idx,
            "strategy": "semantic",
            "content": chunk_content,
            "metadata": {
                "sentence_count": len(current_chunk_sentences),
                "split_score": 1.0,
            },
        })

    return chunks


# =====================================================================
# 3. STRUCTURE-AWARE CHUNKING
# =====================================================================
def structure_aware_chunking(markdown_text: str) -> List[Dict[str, Any]]:
    """
    Chiến lược 3: Băm nhỏ nhận biết cấu trúc văn bản (Headers/Sections).
    - Tách văn bản theo các tiêu đề (#, ##, ###).
    - Giữ lại tiêu đề mẹ và cấp bậc đề mục trong metadata của từng chunk.
    """
    lines = markdown_text.splitlines()
    chunks: List[Dict[str, Any]] = []

    current_header = "Introduction"
    current_level = 1
    current_lines: List[str] = []
    idx = 0

    def save_chunk(header: str, level: int, body_lines: List[str]):
        nonlocal idx
        content = "\n".join(body_lines).strip()
        if content:
            chunks.append({
                "chunk_id": idx,
                "strategy": "structure_aware",
                "header": header,
                "level": level,
                "content": content,
                "metadata": {
                    "line_count": len(body_lines),
                    "char_count": len(content),
                },
            })
            idx += 1

    for line in lines:
        stripped = line.strip()
        match = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if match:
            # Lưu lại khối trước đó nếu có nội dung
            if current_lines:
                save_chunk(current_header, current_level, current_lines)
                current_lines = []

            # Thiết lập header mới
            hashes, title = match.groups()
            current_header = title.strip()
            current_level = len(hashes)
            current_lines.append(stripped)
        else:
            current_lines.append(line)

    # Lưu khối cuối cùng
    if current_lines:
        save_chunk(current_header, current_level, current_lines)

    return chunks


if __name__ == "__main__":
    print("=== TEST 3 CHIẾN LƯỢC CHUNKING ===")

    sample_doc = """# Khái Niệm Về RAG
RAG là viết tắt của Retrieval-Augmented Generation. Đây là một kiến trúc AI đột phá kết hợp tra cứu dữ liệu và mô hình ngôn ngữ lớn.

## 1. Thành Phần Retrieval
Retrieval có nhiệm vụ tra cứu thông tin liên quan từ cơ sở tri thức bên ngoài. Các vector được lưu trong vector database như Chroma hoặc Pinecone.

## 2. Thành Phần Generation
Generation nhận dữ liệu từ Retrieval và ghép vào Prompt. Sau đó LLM sẽ sinh câu trả lời chính xác dựa trên dữ liệu thật.
"""

    print("\n[1] FIXED-SIZE WITH OVERLAP (size=20 words, overlap=5 words):")
    fixed_chunks = fixed_size_chunking(sample_doc, chunk_size=20, chunk_overlap=5)
    for c in fixed_chunks[:2]:
        print(f"  Chunk {c['chunk_id']}: {c['content'][:60]}... ({c['metadata']['word_count']} words)")

    print("\n[2] STRUCTURE-AWARE CHUNKING (Theo đề mục Markdown):")
    struct_chunks = structure_aware_chunking(sample_doc)
    for c in struct_chunks:
        print(f"  Chunk {c['chunk_id']} [{c['header']} - H{c['level']}]: {c['content'][:50]}...")

    print("\n[3] SEMANTIC CHUNKING (Tách theo câu và ngữ cảnh):")
    sem_chunks = semantic_chunking(sample_doc, similarity_threshold=0.2)
    for c in sem_chunks:
        print(f"  Chunk {c['chunk_id']}: {c['content'][:60]}...")
