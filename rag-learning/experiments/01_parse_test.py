"""
Experiment: 01_parse_test.py
Thực nghiệm bóc tách dữ liệu đa định dạng (HTML, Markdown, TXT, JSON).
"""

import sys
from pathlib import Path

# Thêm thư mục rag-learning vào sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.ingestion.parser import parse_html, parse_json, parse_markdown, parse_txt


def main():
    print("=" * 60)
    print("🧪 EXPERIMENT 01: PARSING MULTI-FORMAT DATA")
    print("=" * 60)

    # 1. Test Markdown
    md_content = """# Hướng Dẫn Kỹ Thuật RAG
## 1. Giới Thiệu
RAG là viết tắt của Retrieval-Augmented Generation.
## 2. Các Bước Thực Hiện
- Parsing tài liệu
- Chunking
- Embedding
"""
    res_md = parse_markdown(md_content, filename="guide.md")
    print("\n[1] TEST PARSE MARKDOWN:")
    print(f"Tiêu đề : {res_md['title']}")
    print(f"Đề mục  : {res_md['metadata']['sections']}")
    print(f"Số từ   : {res_md['metadata']['word_count']}")

    # 2. Test HTML (Loại bỏ rác script, style, ads)
    html_content = """<html><head><title>Trang Sản Phẩm</title></head><body>
    <div class="ads">Khuyến mãi cực sốc!</div>
    <h1>Thông tin sản phẩm</h1>
    <p>Sản phẩm AI hỗ trợ doanh nghiệp tự động hóa.</p>
    <script>alert('spam');</script>
    </body></html>"""
    res_html = parse_html(html_content, filename="product.html")
    print("\n[2] TEST PARSE HTML (Lọc sạch rác):")
    print(f"Tiêu đề : {res_html['title']}")
    print(f"Nội dung: {res_html['content']}")

    print("\n" + "=" * 60)
    print("✅ Hoàn thành thực nghiệm Parsing!")


if __name__ == "__main__":
    main()
