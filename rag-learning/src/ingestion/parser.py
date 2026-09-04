"""
Module: src/ingestion/parser.py
Mục đích: Bóc tách dữ liệu đa định dạng (Multi-format Parsing) đưa về văn bản sạch (Clean Text).
Hỗ trợ: TXT, Markdown (.md), HTML, JSON.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from bs4 import BeautifulSoup


def parse_txt(text: str, filename: str = "document.txt") -> Dict[str, Any]:
    """Bóc tách file văn bản thuần túy (Plain Text)."""
    clean_text = text.strip()
    lines = [line.strip() for line in clean_text.splitlines() if line.strip()]
    title = lines[0] if lines else "Untitled"

    return {
        "filename": filename,
        "format": "txt",
        "title": title[:100],
        "content": clean_text,
        "metadata": {
            "char_count": len(clean_text),
            "word_count": len(clean_text.split()),
            "line_count": len(lines),
        },
    }


def parse_markdown(md_text: str, filename: str = "document.md") -> Dict[str, Any]:
    """Bóc tách file Markdown: Giữ cấu trúc tiêu đề, trích xuất sections."""
    lines = md_text.splitlines()
    title = "Untitled"
    sections: List[str] = []

    for line in lines:
        stripped = line.strip()
        # Tìm tiêu đề H1 đầu tiên
        if stripped.startswith("# ") and title == "Untitled":
            title = stripped.replace("# ", "").strip()
        elif stripped.startswith(("#", "##", "###")):
            sections.append(stripped.lstrip("#").strip())

    clean_text = md_text.strip()
    return {
        "filename": filename,
        "format": "markdown",
        "title": title,
        "content": clean_text,
        "metadata": {
            "sections": sections,
            "char_count": len(clean_text),
            "word_count": len(clean_text.split()),
        },
    }


def parse_html(html_content: str, filename: str = "document.html") -> Dict[str, Any]:
    """Bóc tách HTML: Loại bỏ tag rác (script, style, nav, footer, ads) và lấy nội dung chính."""
    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Loại bỏ các thẻ không chứa tri thức
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    # Loại bỏ các khối quảng cáo phổ biến
    for tag in soup.find_all(class_=re.compile(r"(ads|advertisement|banner|social)", re.I)):
        tag.decompose()

    # 2. Trích xuất tiêu đề
    title = soup.title.get_text(strip=True) if soup.title else "Untitled HTML"

    # 3. Lấy nội dung văn bản sạch
    clean_text = soup.get_text(separator="\n", strip=True)

    return {
        "filename": filename,
        "format": "html",
        "title": title,
        "content": clean_text,
        "metadata": {
            "char_count": len(clean_text),
            "word_count": len(clean_text.split()),
        },
    }


def parse_json(json_str: str, filename: str = "document.json") -> Dict[str, Any]:
    """Bóc tách JSON: Đọc cấu trúc key-value và chuyển đổi thành văn bản có thể đọc."""
    data = json.loads(json_str)

    # Chuyển đổi json thành văn bản phân cấp dễ hiểu
    def extract_text(obj: Any, prefix: str = "") -> List[str]:
        lines = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_prefix = f"{prefix}.{k}" if prefix else str(k)
                lines.extend(extract_text(v, new_prefix))
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                new_prefix = f"{prefix}[{idx}]"
                lines.extend(extract_text(item, new_prefix))
        else:
            lines.append(f"{prefix}: {obj}")
        return lines

    text_lines = extract_text(data)
    content = "\n".join(text_lines)

    return {
        "filename": filename,
        "format": "json",
        "title": filename,
        "content": content,
        "metadata": {
            "char_count": len(content),
            "word_count": len(content.split()),
        },
    }


def parse_document(file_path: str) -> Dict[str, Any]:
    """Hàm thống nhất: Tự động phát hiện đuôi file và gọi Parser phù hợp."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

    content = path.read_text(encoding="utf-8")
    ext = path.suffix.lower()

    if ext in (".txt", ".text"):
        return parse_txt(content, filename=path.name)
    elif ext in (".md", ".markdown"):
        return parse_markdown(content, filename=path.name)
    elif ext in (".html", ".htm"):
        return parse_html(content, filename=path.name)
    elif ext == ".json":
        return parse_json(content, filename=path.name)
    else:
        # Mặc định coi là plain text
        return parse_txt(content, filename=path.name)


if __name__ == "__main__":
    print("=== DEMO MULTI-FORMAT PARSER ===")

    # 1. Thử nghiệm HTML
    raw_html = """
    <html>
        <head><title>Báo cáo RAG Ingestion 2026</title></head>
        <body>
            <nav><a href="/">Trang chủ</a></nav>
            <div class="ads">Mua ngay khóa học AI!</div>
            <h1>Tổng Quan Về Parsing Trong RAG</h1>
            <p>Parsing là bước bóc tách dữ liệu thô đưa về văn bản sạch.</p>
            <footer>Bản quyền 2026</footer>
        </body>
    </html>
    """
    res_html = parse_html(raw_html)
    print("\n📄 [1. HTML Parsing]:")
    print(f"Tiêu đề: {res_html['title']}")
    print(f"Nội dung:\n{res_html['content']}")

    # 2. Thử nghiệm JSON
    sample_json = json.dumps({
        "tên_dự_án": "RAG Learning",
        "module": "Ingestion",
        "tác_vụ": ["Parsing", "Chunking", "Embedding"],
    }, ensure_ascii=False, indent=2)
    res_json = parse_json(sample_json)
    print("\n📄 [2. JSON Parsing]:")
    print(f"Nội dung:\n{res_json['content']}")
