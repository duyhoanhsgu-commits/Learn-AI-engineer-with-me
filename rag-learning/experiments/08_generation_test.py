"""
Experiment: 08_generation_test.py
Thực nghiệm kiểm chứng thành phần Augmented Generation (Chữ "G" trong RAG):
1. Nhận các context chunks từ Reranker.
2. Kiểm tra khả năng sinh câu trả lời bám sát tài liệu (Grounded Answer).
3. Kiểm tra cơ chế trích dẫn nguồn minh bạch (Citations).
4. Kiểm tra khả năng từ chối trả lời khi câu hỏi không có trong tài liệu (Anti-Hallucination).
"""

import sys
from pathlib import Path

# Đảm bảo import được module từ rag-learning
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.generation.generator import RAGGenerator
from src.generation.prompt import build_rag_prompt


def main():
    print("=" * 70)
    print("🧪 EXPERIMENT 08: AUGMENTED GENERATION & GROUNDING TEST")
    print("=" * 70)

    generator = RAGGenerator()

    # Tập ngữ cảnh giả lập sau khi đã qua bước Hybrid Search & Reranking
    context_chunks = [
        {
            "chunk_id": "policy_wfh_01",
            "content": "Chính sách WFH: Nhân viên chính thức được làm việc từ xa tối đa 2 ngày mỗi tuần, đăng ký trước 24h qua hệ thống ERP.",
            "metadata": {"source": "hr_portal", "policy_id": "WFH-2024"},
        },
        {
            "chunk_id": "policy_equipment_02",
            "content": "Trang thiết bị làm việc: Công ty cấp 01 máy tính xách tay và trợ cấp 500.000 VNĐ/tháng chi phí internet cho nhân viên WFH.",
            "metadata": {"source": "it_support", "policy_id": "EQP-2024"},
        },
    ]

    # Kịch bản 1: Câu hỏi hợp lệ có trong tài liệu
    q1 = "Nhân viên được làm việc từ xa tối đa mấy ngày một tuần và có được hỗ trợ tiền internet không?"
    print(f"\n1. TRUY VẤN HỢP LỆ: '{q1}'")
    res1 = generator.generate(q1, context_chunks)
    print(f"-> Phản hồi ({res1['model']}):\n{res1['answer']}\n")
    print("-> Nguồn tài liệu được trích dẫn:")
    for s in res1["sources"]:
        print(f"   * {s['source_tag']} Chunk ID: {s['chunk_id']} | Snippet: {s['snippet']}")

    # Kịch bản 2: Câu hỏi hoàn toàn nằm ngoài tài liệu (Kiểm định chống ảo giác)
    q2 = "Công ty có tài trợ học bổng du học Thạc sĩ ở nước ngoài không?"
    print(f"\n2. TRUY VẤN NGOÀI PHẠM VI (UNGROUNDED QUERY): '{q2}'")
    res2 = generator.generate(q2, context_chunks)
    print(f"-> Phản hồi ({res2['model']}):\n{res2['answer']}\n")

    print("=" * 70)
    print("✅ Hoàn thành thực nghiệm Augmented Generation!")


if __name__ == "__main__":
    main()
