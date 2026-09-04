"""
Experiment: 03_embedding_test.py
Kiểm thử và so sánh biểu diễn Embedding Vectors giữa các từ ngữ.
"""

import sys
from pathlib import Path

# Thêm thư mục rag-learning vào sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from compare_vectors import VectorWordComparator


def main():
    comparator = VectorWordComparator()

    test_pairs = [
        ("king", "queen"),
        ("chó", "mèo"),
        ("học máy", "trí tuệ nhân tạo"),
        ("bàn phím", "bát phở"),
    ]

    print("=== EXPERIMENT 03: EMBEDDING & COSINE SIMILARITY TEST ===")
    for w1, w2 in test_pairs:
        comparator.print_result(w1, w2)


if __name__ == "__main__":
    main()
