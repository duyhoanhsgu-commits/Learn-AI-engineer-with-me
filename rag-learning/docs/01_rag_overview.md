# TỔNG QUAN VỀ KIẾN TRÚC RAG (RETRIEVAL-AUGMENTED GENERATION)

---

## 1. Bản Chất Cốt Lõi Của RAG Là Gì?

**RAG (Retrieval Augmented Generation - Tạo lập tăng cường truy xuất)** là một trong những kiến trúc nền tảng mang tính đột phá để nâng tầm năng lực của Mô hình ngôn ngữ lớn (**LLM**) trong các ứng dụng thực tế.

Về bản chất, RAG đóng vai trò như một **cầu nối thông minh**, giúp LLM mỗi khi trả lời câu hỏi thì biết tự động tra cứu "sách vở" và tài liệu bên ngoài, thay vì chỉ phụ thuộc hoàn toàn vào bộ nhớ tĩnh được huấn luyện sẵn.

---

## 2. Tại Sao Chúng Ta Lại Cần Đến RAG?

Khi một mô hình LLM đứng độc lập một mình, nó sẽ luôn gặp phải **3 giới hạn bẩm sinh**:

1. **Knowledge Cut-off (Điểm dừng tri thức):**
   * LLM chỉ biết dữ liệu đã được huấn luyện cho đến một mốc thời gian nhất định.
   * Các thông tin nội bộ của doanh nghiệp hoặc các sự kiện mới phát sinh hoàn toàn nằm ngoài tầm hiểu biết của nó.
   * Doanh nghiệp cũng không thể mạo hiểm public dữ liệu nội bộ/nhạy cảm lên mạng để LLM học lại từ đầu.
2. **Hallucination (Hiện tượng ảo giác / Tự bịa thông tin):**
   * Bản chất LLM là một cỗ máy đoán từ (token tiếp theo) dựa trên xác suất thống kê.
   * Khi thiếu dữ liệu hoặc không biết câu trả lời, mô hình vẫn tự bịa ra thông tin với văn phong vô cùng tự nhiên và mượt mà. 
   * Điều này xảy ra vì LLM được huấn luyện để trả lời và thuyết phục chúng ta, dù thực tế nó không hề có chủ đích lừa dối.
3. **Context Window (Giới hạn cửa sổ ngữ cảnh):**
   * Ngay cả con người cũng không thể nào chứa toàn bộ ngữ cảnh của cả cuộc đời trong một khoảnh khắc, nhưng con người biết cái nào cần giữ và cái nào không.
   * LLM thì bị giới hạn bởi *Context Window* — ở một thời điểm, nó chỉ có thể nhìn về quá khứ trong một giới hạn độ dài nhất định.

> **Giải pháp từ RAG:** Thay vì bắt mô hình phải học thuộc lòng toàn bộ kiến thức, RAG cung cấp cho LLM một **ngăn tủ sách chuyên biệt**. Lúc này, LLM sẽ dùng đúng thế mạnh cốt lõi của mình là khả năng đọc hiểu và sinh từ (generate token) dựa trên đúng ngữ cảnh đã được cung cấp.

---

## 3. Sơ Đồ Quy Trình Vận Hành Của Hệ Thống RAG

Để đưa RAG vào vận hành thực tế, dữ liệu cần trải qua một quy trình xử lý (**Data Pipeline**) chia làm **2 giai đoạn chính**:

```
[ GIAI ĐOẠN 1: OFFLINE INGESTION ]
Dữ liệu thô (PDF, Excel, HTML...)
   └──> 1. Parse (Trích xuất văn bản)
   └──> 2. Chunking (Cắt nhỏ thành từng đoạn)
   └──> 3. Enrich (Làm giàu & Gán metadata)
   └──> 4. Embedding (Vector hóa ngữ nghĩa)
   └──> 5. Indexing (Lưu vào Vector DB)

[ GIAI ĐOẠN 2: ONLINE SERVING ]
Câu hỏi của người dùng (Query)
   └──> 1. Pre-RAG (Làm sạch, viết lại câu hỏi)
   └──> 2. Retrieval (Truy xuất các chunk gần nhất)
   └──> 3. Augment (Ghép Query + Chunk vào Prompt)
   └──> 4. Generate (LLM đọc context và sinh câu trả lời)
```

---

### Giai Đoạn 1: Offline Ingestion (Nạp dữ liệu & Đánh chỉ mục)
*Đây là giai đoạn cực kỳ quan trọng, quyết định trực tiếp đến sự thành bại của toàn bộ hệ thống RAG.*

* **Bước 1 - Parse (Phân tích cú pháp):** Trích xuất văn bản thô từ các định dạng dữ liệu khó như PDF, Excel, HTML... đưa về dạng văn bản chuẩn mà LLM có khả năng đọc hiểu được.
* **Bước 2 - Chunking (Cắt đoạn):** Cắt nhỏ các văn bản dài thành các đoạn nhỏ (*chunks*) vừa vặn với kích thước ngữ cảnh của mô hình. 
  * *Mục đích:* Giúp LLM định hình rõ đây chính là ngữ cảnh trọng tâm, thay vì phải đọc hết toàn bộ một tài liệu khổng lồ thì nay chỉ cần đọc từng chunk thích hợp để trả lời.
* **Bước 3 - Enrich (Làm giàu dữ liệu):** Tự động bổ sung các siêu dữ liệu (*metadata*) như phiên bản tài liệu, mốc thời gian, hoặc tóm tắt ngắn cho từng chunk để hỗ trợ tìm kiếm nhanh và chính xác hơn.
* **Bước 4 - Embedding (Vector hóa):** Biến đổi từng chunk văn bản thành một dãy số thực (vector đa chiều). 
  * Đây chính là **ngôn ngữ chung của máy học** — cách máy tính nhìn nhận mọi thứ xung quanh và đưa về dạng vector để máy có thể hiểu và tính toán ngữ nghĩa sâu, thay vì chỉ đếm từ trùng khớp máy móc.
* **Bước 5 - Indexing (Lập chỉ mục):** Lưu trữ các vector này cùng metadata liên quan vào một cơ sở dữ liệu chuyên dụng gọi là **Vector Database** để tối ưu hóa tốc độ và khả năng tra cứu.

---

### Giai Đoạn 2: Online Serving (Truy xuất & Trả lời thời gian thực)

* **Bước 1 - Pre-RAG (Tiền xử lý câu hỏi):** Làm sạch câu hỏi của người dùng và viết lại (*Query Rewriting*). Nếu người dùng hỏi gộp nhiều ý, bước này sẽ phân tích và tách câu hỏi ra để query chính xác vào từng chunk.
* **Bước 2 - Retrieval (Truy xuất):** Sử dụng vector của câu hỏi để tra cứu trong Vector DB, truy xuất ra các đoạn chunk có tọa độ vector gần nhất (đo bằng Cosine Similarity hoặc Euclidean).
* **Bước 3 - Augment (Bổ sung ngữ cảnh):** Lấy những đoạn chunk tìm thấy nhồi vào prompt chung với câu hỏi để gửi đến LLM. Lúc này, chunk đóng vai trò là một *Context* (bối cảnh thực tế) để LLM bám vào sinh từ.
* **Bước 4 - Generate (Sinh câu trả lời):** Sau khi LLM đã đọc được cả query và context, nó sẽ sinh token dựa trên chính các chunk tài liệu này. 
  * Ràng buộc này khiến LLM giảm thiểu tối đa cơ hội sinh ra ảo giác (*hallucination*) vì bắt buộc phải dựa vào tài liệu thực tế.
  * *(Lưu ý: Nếu câu trả lời chưa chuẩn thì phần lớn nguyên nhân nằm ở việc khâu Embedding hoặc Retrieval chưa bốc trúng đoạn chunk phù hợp).*

---

## 4. Các Biến Thể RAG Nâng Cao (Advanced RAG)

Trong thực tế triển khai, hệ thống RAG thường được mở rộng với các kỹ thuật chuyên sâu hơn:
* **Hybrid Search:** Kết hợp tìm kiếm ngữ nghĩa (*Dense Vector*) và tìm kiếm từ khóa truyền thống để không bị sót thuật ngữ hoặc mã chuyên ngành.
* **Reranking:** Dùng mô hình chấm điểm chuyên biệt để sắp xếp lại độ ưu tiên của các chunks vừa bốc ra trước khi nạp vào LLM.
* **Graph RAG:** Kết hợp Vector DB với Đồ thị tri thức (*Knowledge Graph*) để nắm bắt các mối liên hệ ngữ cảnh phức tạp xuyên suốt nhiều nguồn tài liệu.