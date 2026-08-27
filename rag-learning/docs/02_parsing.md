# TỔNG QUAN VỀ PARSING TRONG HỆ THỐNG RAG: BƯỚC ĐẦU QUYẾT ĐỊNH TRẦN CHẤT LƯỢNG

---

## 1. Bản Chất Của Parsing Là Gì?

Như chúng ta đã tìm hiểu ở phần kiến trúc tổng quan của RAG, **Parsing (Bóc tách & Phân tích cú pháp dữ liệu)** chính là bước đầu tiên và quan trọng nhất trong giai đoạn **Offline Ingestion Pipeline**.

Hiểu một cách đơn giản: **Parsing** là quá trình phân tích, trích xuất và chuyển đổi các tài liệu thô đa định dạng (PDF, Word, Excel, HTML, ảnh quét...) thành dạng **văn bản sạch (clean text)**, giữ nguyên được cấu trúc bảng biểu, tiêu đề và hình ảnh để máy tính và các mô hình AI có thể đọc hiểu chính xác.

---

## 2. Vì Sao Parsing Quyết Định "Trần Chất Lượng" (Quality Ceiling) Của Hệ Thống AI?

Trong xử lý ngôn ngữ tự nhiên (NLP) và RAG, bước bóc tách dữ liệu quyết định trực tiếp đến giới hạn chất lượng cao nhất của toàn bộ hệ thống hạ nguồn.

Hệ thống RAG **không bao giờ có thể tìm kiếm và trả lời tốt hơn chất lượng của dữ liệu thô đầu vào**. Ở đây, quy luật tối thượng luôn được áp dụng:
$$\textbf{Garbage In} \implies \textbf{Garbage Out} \quad \text{(Rác vào thì Rác ra)}$$

### Hiểm họa "Rò rỉ dữ liệu ngầm" (Silent Data Loss):
Bản chất của các bước phía sau (như **Embedding**) là bắt buộc phải tạo ra output. Bất kể đoạn text đầu vào có méo mó, mất nghĩa hay bị đảo lộn thế nào, mô hình embedding vẫn sẽ cắm đầu vector hóa và LLM vẫn sẽ sinh token. 

Khi Parsing hoạt động kém, hệ thống **hoàn toàn không quăng lỗi (crash)**, khiến lập trình viên cực kỳ khó phát hiện. Các lỗi ngầm kinh điển bao gồm:

1. **Đọc sai thứ tự logic (Reading Order):**
   * *Ví dụ:* Một trang PDF tài liệu nghiên cứu chia làm 2 hoặc 3 cột. Bộ parser thông thường đọc theo thứ tự quét ngang từ trái sang phải qua từng dòng, làm trộn lẫn nội dung của cột 1 sang cột 2 thành một chuỗi chữ vô nghĩa.
2. **Phá hủy cấu trúc bảng biểu (Table Flattening):**
   * Biến các bảng số liệu tài chính, báo cáo doanh thu phức tạp thành một chuỗi văn bản nằm ngang, khiến LLM mất hoàn toàn liên kết dòng - cột và không thể tra cứu số liệu.
3. **Lỗi font chữ tiếng Việt (Encoding Error):**
   * Chuyển đổi các ký tự có dấu tiếng Việt thành chuỗi ký tự rác toán học hoặc các ô vuông `[?]` vô nghĩa.
4. **Bỏ sót thông tin phụ trợ quan trọng:**
   * Làm rơi mất tiêu đề phân cấp (*headings*), ghi chú chân trang (*footnotes*), chú thích biểu đồ (*captions*) hoặc công thức tính toán.

---

## 3. Giải Pháp Bóc Tách Chuẩn Cho Từng Định Dạng Dữ Liệu

Để tránh biến dữ liệu thành "rác", quy trình bóc tách phải được thiết kế riêng biệt cho từng loại định dạng tệp:

```
[ DỮ LIỆU ĐẦU VÀO ]
 ├── 1. Native PDF (Text-based) ──> Parser nhận diện Layout (PyMuPDF, Marker, LlamaParse)
 ├── 2. Scanned PDF / Ảnh     ──> OCR + Vision-Language Model (VLM: GPT-4o, MinerU)
 ├── 3. Excel / CSV           ──> Chuyển đổi thành Markdown Table / JSON Schema
 └── 4. Web Page (HTML)       ──> Bộ lọc chuyên dụng (Trafilatura, BeautifulSoup)
```

---

### A. Đối với tài liệu PDF (Định dạng khó nhằn nhất)
* **PDF bản gốc (Text-based PDF):**
  * Không chỉ dùng các thư viện trích xuất thô thông thường (`PyPDF`, `PyMuPDF`) vì dễ đọc sai thứ tự cột.
  * Nên kết hợp các bộ parser nhận diện bố cục (**Layout-aware Parsers** như *Marker*, *LlamaParse*, *Unstructured*) để giữ nguyên cây phân cấp tiêu đề (H1, H2, H3) và thứ tự cột.
* **PDF quét (Scanned PDF / Dạng ảnh chụp):**
  * Bắt buộc phải kết hợp nhận diện ký tự quang học (**OCR**) cùng các mô hình thị giác ngôn ngữ (**VLM - Vision-Language Models** như GPT-4o, Gemini, MinerU) để bóc tách cả chữ, bảng biểu và sơ đồ.

### B. Đối với bảng tính Excel / CSV (Spreadsheets)
* **Tuyệt đối không ép bảng về dạng text thô (flat raw text):**
* Dữ liệu bảng phải được chuyển đổi thành cấu trúc trung gian có tọa độ dòng/cột rõ ràng như **Markdown Table** hoặc **JSON Object**. Điều này giúp LLM hiểu được tiêu đề cột tương ứng với giá trị từng ô.

### C. Đối với trang web (HTML)
* Sử dụng các bộ lọc chuyên dụng (như `Trafilatura`, `BeautifulSoup`) để loại bỏ toàn bộ các thành phần rác: thanh menu, điều hướng (navbar), chân trang (footer), quảng cáo (ads), mã CSS/JS rườm rà.
* Chỉ giữ lại nội dung cốt lõi của bài viết (*main content*).

---

## 4. Các Điểm Cần Lưu Ý Nâng Cao Trong Thực Tế

1. **Xử lý Hình ảnh & Sơ đồ kỹ thuật:**
   * Sử dụng VLM để tự động sinh văn bản mô tả (*Image Captioning*) cho biểu đồ, sơ đồ quy trình, biến hình ảnh thành ngữ cảnh mà LLM đọc được.
2. **Lưu vết nguồn tài liệu (Page-level Lineage & Metadata):**
   * Ở bước Parsing, cần ghi nhận số trang (`page_number`), tên file và vị trí tọa độ của đoạn văn. Đây là dữ liệu cực kỳ quan trọng để sau này hệ thống có thể **trích dẫn chính xác nguồn (Citation)** cho người dùng.