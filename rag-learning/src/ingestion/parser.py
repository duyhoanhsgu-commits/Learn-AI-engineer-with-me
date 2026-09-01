from bs4 import BeautifulSoup

# Dữ liệu HTML thô giả lập (như tải từ web về)
raw_html = """
<html>
    <head><title>Báo cáo AI 2026</title></head>
    <body>
        <nav><a href="#">Trang chủ</a> | <a href="#">Liên hệ</a></nav>
        <div class="ads">Quảng cáo: Mua sắm ngay!</div>
        
        <main>
            <h1>Tổng Quan Về Parsing Trong RAG</h1>
            <p>Parsing là bước bóc tách dữ liệu thô đưa về văn bản sạch.</p>
            <p>Nếu parsing kém, dữ liệu đầu vào sẽ bị biến dạng (Garbage In, Garbage Out).</p>
        </main>
        
        <footer>Copyright 2026 Company Inc.</footer>
        <script>console.log("analytics");</script>
    </body>
</html>
"""

def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Loại bỏ các thẻ rác không chứa nội dung tri thức
    for element in soup(["script", "style", "nav", "footer", "div"]):
        if "ads" in element.get("class", []):
            element.decompose()
        elif element.name in ["script", "style", "nav", "footer"]:
            element.decompose()
            
    # 2. Trích xuất tiêu đề và nội dung văn bản chính
    title = soup.title.string if soup.title else ""
    main_text = soup.get_text(separator="\n", strip=True)
    
    return {
        "title": title,
        "clean_text": main_text
    }

# Kết quả bóc tách
parsed_result = parse_html(raw_html)
print(f"--- TIÊU ĐỀ: {parsed_result['title']} ---")
print(parsed_result["clean_text"])
