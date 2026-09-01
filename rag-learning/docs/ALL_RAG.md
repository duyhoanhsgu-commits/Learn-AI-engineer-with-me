# TỔNG QUAN KIẾN THỨC RAG & CHƯƠNG 1: FOUNDATION & EVOLUTION

---

## 📌 Chương I. CẤU TRÚC BÀI HỌC RAG 

Toàn bộ lộ trình bài học RAG (Retrieval-Augmented Generation) được tổ chức thành 5 chương chính:

| STT | Tên chương | Tên tiếng Anh | Nội dung chính |
| :--- | :--- | :--- | :--- |
| **01** | **Kiến thức nền tảng & Tiến hóa** | *Foundation & Evolution* | Cơ chế Semantic Search, bản chất Embedding, Dense Vector Space, Vector Database và Cosine Similarity. |
| **02** | **Quy trình nạp dữ liệu Offline** | *Offline Pipeline Ingestion* | Xử lý dữ liệu thô, chunking, trích xuất metadata, embedding và nạp vào vector database. |
| **03** | **Quy trình truy xuất Online** | *Online Pipeline Retrieval* | Truy vấn người dùng, embedding câu hỏi, tìm kiếm tương đồng (similarity search), reranking và ghép context vào prompt. |
| **04** | **Graph RAG & Kiến trúc nâng cao** | *Graph RAG & Advanced Architecture* | Kết hợp đồ thị tri thức (Knowledge Graph) với RAG, Multi-query, HyDE, Self-RAG, Agentic RAG. |
| **05** | **Đánh giá & Vận hành thực tế** | *Evaluation & Operationalization* | Các chỉ số đánh giá RAG (Ragas, TruLens), tối ưu độ trễ, chi phí, giám sát và triển khai production. |

---

## 🧠 CHƯƠNG II: FOUNDATION & EVOLUTION

Chương này giải quyết 3 câu hỏi cốt lõi:
1. **Tại sao Semantic Search (Tìm kiếm ngữ nghĩa) lại hoạt động?**
2. **Bản chất của Embedding là gì?**
3. **Vector Database tìm các vector gần nhau bằng cách nào?**

---

### 1: EMBEDDING NATURE & VECTOR SPACE

#### a. Bản chất của Embedding & Không gian Vector Dày Đặc (Dense Vector Space)

##### i. Định nghĩa Embedding
- **Embedding** là quá trình chuyển đổi mọi dạng thông tin (văn bản, hình ảnh, âm thanh, video...) thành một **vector số thực nhiều chiều**.
- Ví dụ: Từ `"dog"` sau khi đi qua Embedding Model sẽ trở thành một vector gồm 768 chiều (hoặc 1.536 chiều). Mỗi chiều mang một giá trị số thực thường dao động trong khoảng `[-1, 1]`.

##### ii. So sánh Dense Vector vs. Sparse Representation (One-hot)

| Tiêu chí | One-hot / Sparse Vector | Dense Vector |
| :--- | :--- | :--- |
| **Kích thước vector** | Phụ thuộc vào kích thước tập từ vựng (ví dụ: 10.000 từ $\rightarrow$ 10.000 chiều). | Cố định theo mô hình (ví dụ: 768 hoặc 1.536 chiều). |
| **Phân bổ giá trị** | Đa số là số `0`, chỉ có một vị trí mang giá trị `1` (thưa thớt). | Hầu hết mọi chiều đều chứa giá trị thực khác nhau (dày đặc). |
| **Hiệu năng lưu trữ** | Cực kỳ tốn bộ nhớ và không gian lưu trữ. | Tối ưu không gian, nén thông tin hiệu quả. |
| **Khả năng biểu diễn ngữ nghĩa** | Không biểu diễn được mối quan hệ hay ngữ nghĩa giữa các từ. | Học và biểu diễn được ngữ nghĩa sâu sắc của từ/câu. |

##### iii. Trực quan hóa không gian đa chiều
- Không gian vector thực tế có hàng trăm, hàng nghìn chiều (768D, 1536D) vượt quá khả năng hình dung trực quan của con người (vốn quen với 2D/3D).
- Khi quy chiếu về không gian 2D để trực quan hóa:
  - Các khái niệm có liên quan/tương đồng sẽ **tự động phân cụm gần nhau**.
  - *Ví dụ 1:* `"cat"` và `"dog"` sẽ nằm gần nhau trong cụm **Animal/Pet** (cùng là động vật 4 chân, có lông, được nuôi làm thú cưng).
  - *Ví dụ 2:* `"Database"` và `"SQL"` sẽ nằm trong cụm lưu trữ dữ liệu.

---

#### b. Độ tương đồng ngữ nghĩa (Semantic Similarity)

##### i. Vấn đề của tìm kiếm từ khóa truyền thống (Keyword / Lexical Search)
- Nếu người dùng hỏi: *"Ô tô là gì?"*
- Trong tài liệu lại dùng từ: *"Xe hơi là phương tiện..."*
- **Hệ thống truyền thống (Keyword Match):** Thất bại vì không khớp từ khóa `"ô tô"` với `"xe hơi"`.

##### ii. Giải pháp với Semantic Similarity
- Embedding Model ánh xạ cả hai từ `"ô tô"` và `"xe hơi"` vào các vị trí vector rất gần nhau trong không gian vector.
- Máy tính không cần khớp từng ký tự mà hiểu được **ý nghĩa ngữ cảnh**.
- 👉 **Semantic Similarity chính là "trái tim" và nền tảng cốt lõi của bước Retrieval trong RAG.**

---

#### c. Độ tương đồng Cosine (Cosine Similarity)

Để đo lường xem hai vector có "gần nhau" hay tương đồng về mặt ngữ nghĩa hay không, hệ thống sử dụng các phép đo khoảng cách/góc, phổ biến nhất là **Cosine Similarity**.

##### i. Công thức toán học
$$\text{Cosine Similarity}(\vec{A}, \vec{B}) = \cos(\theta) = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$

*Trong đó:*
- $\vec{A} \cdot \vec{B}$: Tích vô hướng (dot product) của hai vector.
- $\|\vec{A}\|, \|\vec{B}\|$: Độ dài (chuẩn Euclidean) của từng vector.
- Công thức này áp dụng đồng nhất từ không gian 2 chiều, 3 chiều cho đến hàng nghìn chiều.

##### ii. Ý nghĩa của giá trị Cosine Similarity
- **Gần $1$ (Góc $\theta \to 0^\circ$):** Hai vector cùng hướng $\rightarrow$ Hai đoạn văn bản cực kỳ tương đồng về ngữ nghĩa.
- **Gần $0$ (Góc $\theta \to 90^\circ$):** Hai vector trực giao $\rightarrow$ Không có mối liên hệ ngữ nghĩa.
- **Gần $-1$ (Góc $\theta \to 180^\circ$):** Hai vector ngược hướng $\rightarrow$ Mang ý nghĩa trái ngược nhau hoặc hoàn toàn không liên quan.

---

### 2.HISTORICAL SHIFT – SỰ CHUYỂN DỊCH LỊCH SỬ TỪ TÌM KIẾM THEO CHỮ SANG THEO Ý NGHĨA

#### a. Tổng quan về Historical Shift

Sự phát triển của hệ thống tìm kiếm và truy xuất thông tin (Information Retrieval) đã trải qua bước chuyển dịch cốt lõi:
- **Quá khứ (Lexical Matching):** Tìm kiếm dựa trên so khớp từ khóa (*keyword match*) bề mặt chữ.
- **Hiện tại (Semantic Search):** Tìm kiếm dựa trên ngữ nghĩa và ngữ cảnh thông qua vector embedding.
- **Thực tế sản phẩm (Hybrid Search):** Kết hợp sức mạnh của cả hai phương pháp để tối ưu hóa độ chính xác.

---

#### b. Các thuật toán Lexical Matching truyền thống

##### i. Giới hạn của Lexical Search
- **Từ đồng nghĩa (Synonyms):** Không thể nhận diện các từ khác ký tự nhưng cùng ý nghĩa (ví dụ: *"ô tô"* vs. *"xe hơi"*).
- **Từ đa nghĩa (Polysemy):** Không hiểu ngữ cảnh sử dụng khiến kết quả trả về bị loãng hoặc sai lệch.
- **Tính đa dạng ngôn ngữ:** Rào cản lớn với ngôn ngữ phong phú, tiếng địa phương hoặc biến thể từ ngữ.

##### ii. Thuật toán TF-IDF (Term Frequency - Inverse Document Frequency)
Đánh giá mức độ quan trọng của một từ $t$ trong một tài liệu $d$ thuộc tập văn bản $D$:
- **TF (Term Frequency):** Đo lường tần suất xuất hiện của từ trong tài liệu. Từ xuất hiện càng nhiều trong tài liệu thì càng quan trọng.
- **IDF (Inverse Document Frequency):** Giảm trọng số của các từ xuất hiện quá phổ biến ở mọi tài liệu, vì chúng ít có giá trị phân loại.
- **Vấn đề Stop Words:** Các từ xuất hiện liên tục nhưng không mang nhiều giá trị ngữ nghĩa (ví dụ: *"là"*, *"một"*, *"của"*...). Cần phải lọc bỏ stop words để tránh làm sai lệch kết quả tính toán.

##### iii. Thuật toán BM25 (Best Matching 25)
Là thuật toán xếp hạng (*ranking algorithm*) rất phổ biến trong truy xuất thông tin, phát triển dựa trên nền tảng của lexical matching nhưng cải tiến vượt trội hơn TF-IDF.

**3 yếu tố cốt lõi của BM25:**
- **Term Frequency (Tần suất từ):** Tần suất xuất hiện của từ khóa (có hiện tượng bão hòa tần suất - *term frequency saturation*).
- **Document Length (Độ dài tài liệu):** Chuẩn hóa theo độ dài để tránh thiên vị các tài liệu quá dài.
- **Keyword Importance (Mức độ quan trọng của từ khóa):** Trọng số IDF của từ khóa truy vấn.

**Thế mạnh tuyệt đối của BM25:**
BM25 cực kỳ mạnh trong việc khớp chính xác (*exact match*) các định danh cụ thể mà embedding thường xử lý kém:
- Mã sản phẩm / SKU
- API name / Function name
- Mã lỗi (*Error codes*) / Stack traces (ví dụ: `"error connection reset"`)
- Thuật ngữ pháp lý (*Legal terms*)
- Tên riêng (*Proper nouns*)

---

#### c. Vector Embedding & Bước nhảy Semantic Search

- **Cơ chế:** Ánh xạ từ ngữ/câu vào không gian vector nhiều chiều (*dense vector space*). Các từ khác nhau về mặt chữ nhưng tương đồng về ngữ nghĩa (như *"ô tô"* và *"xe hơi"*) sẽ được đặt tại các tọa độ rất gần nhau.
- **Giải quyết triệt để:** Bẫy từ đồng nghĩa và từ đa nghĩa của phương pháp lexical matching.

---

#### d. So sánh: Lexical Search vs. Vector Search

| Tiêu chí | Lexical Search (BM25 / TF-IDF) | Vector Search (Embedding) |
| :--- | :--- | :--- |
| **Cơ chế hoạt động** | So khớp chính xác từ khóa / ký tự | So khớp khoảng cách ngữ nghĩa trong không gian vector |
| **Xử lý từ đồng nghĩa** | Rất kém ("xe hơi" $\neq$ "ô tô") | Rất tốt ("xe hơi" $\approx$ "ô tô") |
| **Dữ liệu đặc thù** | Vượt trội với mã lỗi, tên hàm, mã SKU, tên riêng | Dễ nhầm lẫn hoặc bỏ sót exact keyword |
| **Chi phí tính toán** | Thấp, tốc độ truy xuất cực nhanh | Cao hơn (cần GPU/mô hình embedding & vector DB) |

---

### 3. VECTOR STORE INTERNALS – BÊN TRONG VECTOR DATABASE

#### a. Tổng quan về Vector Store Internals

Để tìm kiếm vector trong cơ sở dữ liệu hàng triệu đến hàng tỷ vector, **Vector Database** không thể dùng các phương pháp quét tuần tự truyền thống mà bắt buộc phải dựa vào các kỹ thuật **lập chỉ mục (indexing)** và **nén vector** chuyên sâu.

#### b. Các kỹ thuật Lập chỉ mục & Nén Vector (Vector Indexing & Compression)

##### i. ANN (Approximate Nearest Neighbor) – Tìm kiếm láng giềng gần đúng
- **Vấn đề của Brute-force (KNN / Vét cạn):**
  - So sánh vector truy vấn $Q$ với toàn bộ $N$ vector trong cơ sở dữ liệu (độ phức tạp $O(N \cdot d)$).
  - Cho độ chính xác tuyệt đối (100% Exact Recall), nhưng độ trễ (*latency*) cực kỳ cao, bất khả thi khi dữ liệu lên tới hàng triệu/hàng tỷ vector.
- **Nguyên lý của ANN:**
  - Chấp nhận sự đánh đổi (*trade-off*): không cần tìm ra vector láng giềng chính xác 100%, chỉ cần tìm ra vector "đủ gần/đủ tốt" với tốc độ cực nhanh (thường ở mức vài mili-giây).
  - **Cốt lõi:** Cân bằng tối ưu giữa **Speed (Tốc độ)** và **Recall / Accuracy (Độ chính xác)**.

##### ii. HNSW (Hierarchical Navigable Small World) – Đồ thị phân tầng
Là một trong những thuật toán lập chỉ mục dạng đồ thị phổ biến và mạnh mẽ nhất trong các Vector DB hiện đại (*Milvus*, *Qdrant*, *Pinecone*, *pgvector*...):
- **Cấu trúc:** Xây dựng đồ thị dạng nhiều tầng (*hierarchical multi-layer graph*), tương tự cấu trúc dữ liệu Skip-List nhưng dành cho đồ thị:
  - **Top Level (Tầng cao nhất):** Ít node, các liên kết nối xa (*long-range links*) $\rightarrow$ Dò tìm nhanh vùng/cụm tổng quát chứa vector $Q$.
  - **Mid Levels (Tầng trung gian):** Mật độ node tăng dần $\rightarrow$ Thu hẹp phạm vi tìm kiếm.
  - **Bottom Level / Level 0 (Tầng đáy):** Chứa toàn bộ vector với các liên kết chi tiết $\rightarrow$ Tinh chỉnh (*refine*) và xác định chính xác các nearest neighbors.
- **Ưu điểm:** Tốc độ tìm kiếm cực nhanh ($O(\log N)$), độ bao phủ (*recall*) rất cao.

```text
[Level 2 - Top]      (A) -----------------------------> (D)
                      |                                  |
[Level 1 - Mid]      (A) ---------> (B) -------> (D) -> (F)
                      |              |            |      |
[Level 0 - Bottom]   (A)-(B)-(C)-(D)-(E)-(F)-(G)-(H)-(I)
```

##### iii. IVF (Inverted File Index) – Phân cụm không gian
- **Nguyên lý:** Phân chia toàn bộ không gian vector thành $K$ cụm (*clusters*) bằng thuật toán phân cụm (ví dụ: K-Means) và xác định tâm cụm (*centroid*).
- **Quy trình truy vấn:**
  1. So sánh vector $Q$ với các tâm cụm để tìm ra cụm gần nhất (*nearest centroid*).
  2. Chỉ tìm kiếm các vector nằm bên trong cụm (hoặc một vài cụm) đã chọn, bỏ qua hoàn toàn các cụm còn lại.
  3. Giúp thu hẹp không gian tìm kiếm từ quy mô toàn cục xuống phạm vi cục bộ.
- **Sự đánh đổi (Trade-off):**
  - Tìm kiếm nhiều cụm (`nprobe` cao): Recall cao $\rightarrow$ Tăng Latency (chạy chậm hơn).
  - Tìm kiếm ít cụm (`nprobe` thấp): Latency thấp (chạy rất nhanh) $\rightarrow$ Dễ bỏ sót tài liệu liên quan nằm ở biên cụm.

##### iv. PQ (Product Quantization) – Kỹ thuật nén & Lượng tử hóa
- **Bài toán tài nguyên:**
  - Giả sử 1 vector có $768$ chiều $\times 4 \text{ bytes (Float32)} = 3.072 \text{ bytes/vector}$.
  - Với $100.000.000$ vector $\rightarrow$ Tốn hơn $300\text{ GB}$ RAM/Disk (chưa tính chỉ mục đồ thị).
- **Nguyên lý của PQ:**
  - Chia vector gốc có độ dài $D$ thành $M$ sub-vectors nhỏ hơn.
  - Thực hiện lượng tử hóa (*quantization*): Mỗi sub-vector được ánh xạ về một mã đại diện ngắn gọn (*centroid code trong codebook*).
- **Kết quả:**
  - Giảm mạnh dung lượng bộ nhớ RAM và Disk (nén từ Float32 xuống còn vài bytes).
  - Tăng tốc độ tính khoảng cách trực tiếp trên dữ liệu nén.
- **Đánh đổi:** Giảm nhẹ độ chính xác do mất mát thông tin trong quá trình nén.

#### c. Bảng so sánh các kỹ thuật Vector Index & Compression

| Kỹ thuật | Cơ chế cốt lõi | Ưu điểm nổi bật | Điểm đánh đổi (Trade-off) |
| :--- | :--- | :--- | :--- |
| **ANN** | Tìm kiếm gần đúng | Giảm độ phức tạp thời gian so với Brute-force | Mất tính chính xác tuyệt đối (100% Recall) |
| **HNSW** | Đồ thị phân tầng đa lớp | Tốc độ truy vấn siêu nhanh, Recall cao | Tốn nhiều RAM để lưu trữ cấu trúc đồ thị |
| **IVF** | Phân cụm không gian (Voronoi Cells) | Giảm số lượng vector cần quét | Dễ miss dữ liệu nếu cấu hình số cụm quét (`nprobe`) quá nhỏ |
| **PQ** | Chia nhỏ vector & lượng tử hóa | Nén dung lượng bộ nhớ cực lớn, tăng tốc tính toán | Mất mát độ chính xác (Precision) do nén số thực |

---

## 🎯 4. TỔNG KẾT TOÀN BỘ CHƯƠNG 1: FOUNDATION & EVOLUTION

Chương 1 đã thiết lập toàn bộ nền tảng lý thuyết và kỹ thuật bên dưới của RAG qua 3 trụ cột:

```text
                      FOUNDATION & EVOLUTION
                                │
   ┌────────────────────────────┼────────────────────────────┐
   ▼                            ▼                            ▼
1.1 EMBEDDING NATURE         1.2 HISTORICAL SHIFT        1.3 VECTOR STORE INTERNALS
- Dense Vector Space         - Lexical Search (BM25)      - ANN: Trade-off Speed/Recall
- Sparse vs Dense            - Semantic (Vector Search)   - HNSW: Hierarchical Graph
- Cosine Similarity          - Hybrid Search (BM25 + Vec) - IVF: Clustering & PQ: Compression
```

1. **Embedding & Semantic Similarity (1.1):** Bản chất của việc đưa dữ liệu thực tế về không gian dense vector đa chiều và dùng phép đo góc Cosine Similarity để biểu diễn mức độ tương đồng ngữ nghĩa.
2. **Sự chuyển dịch lịch sử (1.2):** Từ tìm kiếm theo chữ (*Lexical Search* - TF-IDF, BM25) sang tìm kiếm theo nghĩa (*Vector Search*), và hội tụ ở **Hybrid Search** trong thực tế production để xử lý đồng thời cả từ đồng nghĩa lẫn mã lỗi, tên riêng, SKU.
3. **Bên trong Vector Database (1.3):** Cơ chế vận hành của **ANN** cùng các giải pháp đồ thị phân tầng (**HNSW**), phân cụm (**IVF**) và nén vector (**PQ**) nhằm cân bằng tối ưu bài toán **Tốc độ – Độ chính xác – Dung lượng bộ nhớ**.

> **Chuyển tiếp:** Toàn bộ nền tảng Chương 1 đã hoàn thiện. Dưới đây là chi tiết **Chương 2: Offline Pipeline Ingestion** (*Data Extraction*, *Chunking strategies*, *Metadata Enrichment*, *Embedding & Index Building*).

---

## ⚙️ Chương III. OFFLINE PIPELINE INGESTION & DATA EXTRACTION

---

### 1. Tổng quan về Offline Pipeline Ingestion

#### a. Bản chất của Ingestion Pipeline
- **Offline Pipeline Ingestion** là toàn bộ quy trình tiếp nhận, xử lý, băm nhỏ và lập chỉ mục tài liệu **trước khi người dùng đưa ra câu hỏi**.
- **Nguyên lý cốt lõi:** *"Garbage In, Garbage Out"* – Dù LLM có thông minh hay context window lớn đến đâu (ví dụ: 1 triệu tokens), việc nạp thẳng tài liệu thô khổng lồ vào prompt sẽ dẫn đến:
  - Chi phí tính toán / token cực kỳ đắt đỏ.
  - Hiện tượng mất thông tin ở giữa văn bản (*Lost in the Middle*).
  - Ảo giác (*Hallucination*) do context bị loãng hoặc nhiễu.
- 👉 **Nếu Ingestion Pipeline xử lý sai ngữ cảnh (context), downstream của RAG chắc chắn sẽ trả về kết quả sai, bất kể LLM mạnh đến mức nào.**

---

#### b. Sơ đồ luồng (Mindmap / Pipeline Flow)

```text
[Tài liệu thô] (PDF, DOCX, HTML, PPTX, Scan...)
      │
      ▼
 1. EXTRACTION (Multi-format Parsing, OCR)
      │
      ▼
 2. CHUNKING (Cắt nhỏ văn bản có cấu trúc)
      │
      ▼
 3. METADATA ENRICHMENT (Bổ sung Page, Heading, Title...)
      │
      ▼
 4. EMBEDDING GENERATION (Chuyển Chunk thành Dense Vector)
      │
      ▼
 5. VECTOR INDEXING (Lưu trữ vào Vector Database & Index: HNSW, IVF...)
```

---

### 2. DATA EXTRACTION (TRÍCH XUẤT DỮ LIỆU)

Mục tiêu chính: Chuyển đổi các tài liệu đa định dạng thô thành một biểu diễn thống nhất (*unified representation*) có cấu trúc rõ ràng mà hệ thống RAG có thể xử lý hiệu quả.

---

#### a. Multi-format Parsing (Phân tích đa định dạng)

- **Thực tế dữ liệu đầu vào:** Rất đa dạng gồm `PDF`, `DOCX`, `HTML`, `Markdown`, `TXT`, `JSON`, `CSV`, `PPTX`...
- **Yêu cầu của một Parser chất lượng cao:**
  - Không đơn thuần là trích xuất text thuần túy (*plain text*).
  - Phải bảo toàn được **cấu trúc ngữ nghĩa (Semantic Structure)** của tài liệu:
    - Tiêu đề / Phân cấp đề mục (`Headings`, `Sections`).
    - Đoạn văn (`Paragraphs`).
    - Bảng biểu dữ liệu (`Tables`).
    - Danh sách liệt kê (`Lists`, `Bullet points`).
    - Chú thích trang, số trang (`Page numbers`).
    - Tách bạch và định danh được hình ảnh, sơ đồ (`Images`, `Figures`).

---

#### b. OCR for Scanned Documents (OCR cho tài liệu quét)

##### i. Vấn đề thực tế & Giải pháp
- **Vấn đề thực tế:** Nhiều tài liệu PDF thực chất là tập hợp các hình ảnh quét (*scanned images/pages*) chứ không chứa text kỹ thuật số (*selectable text*).
- **Giải pháp:** Sử dụng **OCR (Optical Character Recognition - Nhận dạng ký tự quang học)** để trích xuất văn bản từ hình ảnh tài liệu.

##### ii. Hiệu ứng dây chuyền sai lệch (Error Propagation Pipeline)
Trong kiến trúc RAG, sai sót từ bước đầu tiên sẽ kéo theo sự sụp đổ của toàn bộ hệ thống:

```text
[OCR Error] (Trích xuất sai chữ, thiếu ký tự)
     │
     ▼
[Chunking Error] (Cắt sai đoạn, rách nghĩa câu)
     │
     ▼
[Embedding Error] (Vector bị lệch tọa độ ngữ nghĩa)
     │
     ▼
[Retrieval Error] (Tìm kiếm sai/bỏ sót tài liệu chuẩn)
     │
     ▼
[Answer Error] (LLM sinh câu trả lời sai hoặc ảo giác)
```

> ⚠️ **Kết luận:** RAG là một hệ thống **End-to-End Information Retrieval & Pipeline**, độ chính xác của câu trả lời cuối cùng phụ thuộc mật thiết vào chất lượng xử lý dữ liệu ở từng mắt xích, chứ không đơn thuần chỉ phụ thuộc vào LLM.

---

### 3. CHUNKING STRATEGIES & TRADE-OFFS (CHIẾN LƯỢC BĂM NHỎ TÀI LIỆU)

#### a. Bản chất của Chunking trong RAG

- **Chunking** là quá trình phân rã một tài liệu lớn thành các phân đoạn nhỏ hơn (gọi là *chunk*).
- **Mối liên hệ với Vector Search:**
  - Mỗi chunk đại diện cho một vector embedding trong cơ sở dữ liệu.
  - Khi người dùng truy vấn, hệ thống tính độ tương đồng giữa câu hỏi và từng chunk để kéo về ngữ cảnh (*context*) phù hợp nhất nạp vào LLM.
- **Tầm quan trọng:** Chunking quyết định trực tiếp chất lượng ngữ cảnh đưa vào LLM.
  - Nếu chunk quá dài $\rightarrow$ nhiễu thông tin.
  - Nếu chunk quá ngắn hoặc bị cắt rách nghĩa $\rightarrow$ mất thông tin cốt lõi, dẫn đến LLM trả lời sai hoặc xuất hiện ảo giác (*hallucination*).

---

#### b. 3 chiến lược Chunking phổ biến

```text
                        CHUNKING STRATEGIES
                                │
    ┌───────────────────────────┼───────────────────────────┐
    ▼                           ▼                           ▼
1. FIXED-SIZE WITH OVERLAP  2. SEMANTIC CHUNKING     3. STRUCTURE-AWARE CHUNKING
- Chia theo kích thước cố định - Chia theo dịch chuyển ngữ nghĩa - Chia theo cấu trúc văn bản
- Thêm vùng gối đầu (overlap)  - Đo cosine similarity câu   - Giữ nguyên heading/hierarchy
```

##### i. Fixed-size Chunking with Overlap (Chia kích thước cố định có gối đầu)
- **Cơ chế hoạt động:**
  - Chia tài liệu thành các khối có số lượng token/ký tự cố định (ví dụ: `chunk_size` = 500 tokens).
  - **Vấn đề của Fixed-size thuần túy:** Thường cắt ngang xương câu, làm gãy ngữ cảnh hoặc tách rời cụm từ quan trọng ở ranh giới (*boundary*).
  - **Giải pháp bổ sung Overlap (Gối đầu):** Cho phép chunk tiếp theo chứa một phần nội dung cuối của chunk trước (ví dụ: `overlap` = 100 tokens).
    - Chunk 1: Token $1 \rightarrow 500$
    - Chunk 2: Token $401 \rightarrow 900$ (chứa 100 token đệm từ Chunk 1)
    - Chunk 3: Token $801 \rightarrow 1300$ (chứa 100 token đệm từ Chunk 2)

```text
[------------- Chunk 1 (1 - 500) -------------]
                           [============= 100 overlap =============]
                           [------------- Chunk 2 (401 - 900) -------------]
                                                      [============= 100 overlap =============]
                                                      [------------- Chunk 3 (801 - 1300) -------------]
```

- **Đánh giá:**
  - **Ưu điểm:** Cực kỳ đơn giản, tốc độ thực thi nhanh, tài nguyên tính toán thấp, dễ triển khai làm baseline ban đầu. Giữ được liên kết ngữ cảnh tại các điểm giao cắt.
  - **Nhược điểm:** Hoàn toàn mù mờ trước cấu trúc logic của tài liệu (vẫn có thể cắt đứt một bảng dữ liệu hoặc một đoạn văn bản tự nhiên).

##### ii. Semantic Chunking (Băm nhỏ theo ngữ nghĩa)
- **Cơ chế hoạt động:**
  - Không ép buộc độ dài cố định theo số lượng token mà phân tách dựa trên sự chuyển đổi chủ đề/ý nghĩa (*semantic shift*).
  - **Cách thức:**
    1. Tách văn bản thành từng câu đơn lẻ.
    2. Tạo embedding cho từng câu và đo độ tương đồng Cosine Similarity giữa các câu liền kề.
    3. Khi khoảng cách ngữ nghĩa giữa hai câu vượt ngưỡng (*threshold drop* $\rightarrow$ xuất hiện chủ đề/khái niệm mới), hệ thống sẽ đặt điểm cắt chunk (*chunk boundary*).
- **Đánh giá:**
  - **Ưu điểm:** Tính liên kết và mạch lạc ngữ nghĩa (*chunk coherence*) cực kỳ cao, đảm bảo mỗi chunk là một khối ý nghĩa hoàn chỉnh.
  - **Nhược điểm:**
    - Chi phí tính toán rất lớn (phải chạy embedding cho từng câu trong tài liệu offline).
    - Khó tinh chỉnh tham số (ngưỡng tương đồng tối ưu khác nhau tùy theo từng loại tài liệu).
    - Không phải lúc nào cũng vượt trội hơn fixed-size trong các tác vụ tổng quát.

##### iii. Structure-Aware Chunking (Băm nhỏ nhận biết cấu trúc)
- **Cơ chế hoạt động:**
  - Tận dụng cấu trúc phân cấp tự nhiên của văn bản làm ranh giới phân tách: Tiêu đề chương (`H1`), mục (`H2`), tiểu mục (`H3`), đoạn văn (`Paragraph`), hoặc bảng biểu (`Table`).
  - **Kèm Metadata:** Mỗi chunk được gắn kèm thông tin ngữ cảnh về vị trí của nó trong tài liệu.
  - *Ví dụ:* Chunk Content: `"..."` đi kèm Metadata: `{Chapter: "RAG Overview", Section: "Embeddings", Page: 12}`.
- **Ứng dụng thực tế & Đánh giá:**
  - Đặc biệt tối ưu cho các loại tài liệu có bố cục rõ ràng: Giáo trình (*Textbooks*), Sách hướng dẫn kỹ thuật (*Manuals*), Hợp đồng pháp lý (*Contracts*), Chính sách / Quy chế (*Policies*).
  - **Ưu điểm:** Giúp mô hình retrieval tìm kiếm cực kỳ chuẩn xác cả về mặt vị trí văn bản lẫn nội dung chi tiết.

---

#### c. Bảng so sánh các chiến lược Chunking

| Tiêu chí | Fixed-size with Overlap | Semantic Chunking | Structure-Aware Chunking |
| :--- | :--- | :--- | :--- |
| **Tiêu chí cắt chunk** | Độ dài token cố định | Độ tương đồng ngữ nghĩa giữa các câu | Phân cấp tiêu đề (H1, H2, H3), cấu trúc văn bản |
| **Chi phí tính toán** | Thấp nhất | Rất cao (yêu cầu embedding từng câu) | Trung bình (cần parser nhận diện DOM/Markdown) |
| **Độ mạch lạc ngữ nghĩa** | Trung bình | Rất cao | Cao |
| **Duy trì cấu trúc tài liệu** | Kém | Kém | Xuất sắc |
| **Trường hợp sử dụng phù hợp** | Dữ liệu văn bản tự do, baseline ban đầu | Tài liệu chuyển đổi ý linh hoạt, nghiên cứu sâu | Sách giáo khoa, hợp đồng, tài liệu kỹ thuật, chính sách |

### 4. METADATA ENRICHMENT (LÀM GIÀU DỮ LIỆU METADATA)
#### a. Bản chất của Metadata Enrichment
Trong các hệ thống RAG thực tế, một chunk không bao giờ nên chỉ là một chuỗi văn bản thô (*plain text*).
- Nếu chỉ lưu text và vector embedding, hệ thống sẽ mất toàn bộ ngữ cảnh nguồn gốc của đoạn văn bản đó.
- Bước **Metadata Enrichment** biến mỗi chunk thành một đối tượng dữ liệu có cấu trúc hoàn chỉnh (thường là định dạng JSON hoặc Document Object).
---
#### b. Cấu trúc một Chunk được làm giàu (Enriched Chunk)
Thay vì chỉ lưu trữ nội dung text, một chunk hoàn chỉnh sẽ đi kèm tập thuộc tính metadata chi tiết:
```json
{
  "content": "Retrieval-Augmented Generation (RAG) kết hợp sức mạnh truy xuất của retrieval với khả năng sinh ngôn ngữ của LLM...",
  "metadata": {
    "doc_id": "rag_handbook_v1",
    "doc_title": "RAG Comprehensive Guide",
    "page": 12,
    "chapter": "Retrieval Pipeline",
    "section": "Hybrid Search Mechanics",
    "author": "Huân",
    "created_at": "2026-08-30",
    "access_level": "student",
    "chunk_id": "chunk_0142"
  }
}
```
---
#### c. 6 Vai trò cốt lõi của Metadata trong RAG
```text
                       CÁC ỨNG DỤNG CỦA METADATA
                                  │
      ┌──────────────┬────────────┼────────────┬──────────────┐
      ▼              ▼            ▼            ▼              ▼
1. FILTERING   2. CITATION   3. ACCESS   4. RETRIEVABILITY  5. DEBUGGING
(Pre-filtering) (Trích dẫn)   CONTROL     & RERANKING       & MONITORING
```
##### i. Metadata Filtering (Lọc trước khi truy xuất – Pre-filtering)
- **Bài toán:** Người dùng hỏi: *"Trong tài liệu bài giảng Lecture 08, kỹ thuật RAG được triển khai như thế nào?"*
- **Cơ chế:** Thay vì tìm kiếm vector trên toàn bộ cơ sở dữ liệu hàng triệu chunks (dễ bị nhiễu bởi các bài giảng khác), hệ thống áp dụng bộ lọc metadata:
  $$\text{Filter: } \{\text{doc\_title}: \text{"Lecture 08"}\} \longrightarrow \text{Thực hiện Vector Search trong tập con}$$
- **Lợi ích:** Tăng độ chính xác (*Precision*) vượt trội, giảm độ trễ (*latency*) và hạn chế tối đa tài liệu nhiễu.
##### ii. Citation & Grounding (Trích dẫn nguồn gốc chính xác)
- Giúp LLM có thể trích dẫn chính xác vị trí thông tin để người dùng kiểm chứng.
- *Ví dụ câu trả lời của LLM:* `"RAG bao gồm 5 chương chính (Nguồn: Tài liệu RAG Handbook, Chương Retrieval, Trang 12)"`.
- Tạo sự tin tưởng (*Trustworthiness*) và loại bỏ ảo giác (*Hallucination*).
##### iii. Access Control (Kiểm soát quyền truy cập & Bảo mật)
- Trong môi trường doanh nghiệp hoặc trường học, các nhóm người dùng khác nhau có quyền hạn khác nhau (`access_level`: `public`, `student`, `lecturer`, `admin`).
- Hệ thống tự động lọc ra các chunk mà người dùng hiện tại có quyền xem, ngăn ngừa rò rỉ dữ liệu mật.
##### iv. Tăng cường khả năng truy xuất (Retrievability & Context Injection)
- Bổ sung tiêu đề tài liệu (`doc_title`) và tiêu đề mục (`section`) vào phần đầu của chunk text trước khi tạo embedding:
  $$\text{Input Embedding} = \text{"[Document: RAG Guide > Section: Retrieval] "} + \text{Chunk Content}$$
- Giúp chunk giữ được ngữ cảnh bao quát, tránh trường hợp vector bị mồ côi (*orphan chunks*) khi nội dung bên trong quá ngắn hoặc dùng nhiều đại từ thay thế.
##### v. Reranking & Hybrid Scoring
Dùng metadata để điều chỉnh trọng số xếp hạng kết quả:
- Ưu tiên tài liệu mới phát hành gần đây (`created_at`).
- Ưu tiên tài liệu chính thống của tác giả/bộ phận chuyên môn (`author`).
##### vi. Debugging & Tracing (Kiểm tra & Vận hành hệ thống)
Khi LLM đưa ra câu trả lời sai hoặc chất lượng kém, kỹ sư RAG có thể dễ dàng kiểm tra ngược lại:
- Chunk nào đã được lấy về? (`chunk_id`, `doc_id`)
- Vị trí nằm ở trang bao nhiêu? (`page`)
- Phân đoạn đó thuộc phần nào của tài liệu? (`section`, `chapter`)
---
#### d. Tổng kết mối quan hệ: Chunking vs. Metadata Enrichment
| Tiêu chí | Chunking (2.2) | Metadata Enrichment (2.3) |
| :--- | :--- | :--- |
| **Bản chất** | Chia nhỏ tài liệu thành các đoạn vừa vặn về mặt kích thước / ngữ nghĩa. | Gắn thêm thông tin ngữ cảnh, vị trí, quyền hạn và xuất xứ vào từng đoạn. |
| **Mục tiêu** | Đảm bảo kích thước context phù hợp cho Embedding & LLM. | Đảm bảo khả năng lọc chính xác, truy vết nguồn gốc và bảo mật dữ liệu. |
| **Triển khai thực tế** | Thường được gộp chung trong quá trình phân tích văn bản (Parser sinh ra cả text chunk lẫn metadata). |

---

### 5. VECTOR INDEXING & HOÀN THIỆN OFFLINE INGESTION PIPELINE

#### a. Cơ chế hoạt động của Vector Indexing

Sau khi tài liệu đã được băm nhỏ thành từng chunk và bổ sung metadata, hệ thống thực hiện bước cuối cùng trong Offline Pipeline:

```text
[Chunk Text & Metadata] ──► [Embedding Model] ──► [Dense Vector: (0.12, 0.44, -0.21, ...)]
                                                              │
                                                              ▼
                                                 [Lưu vào Vector Database]
```

- **Sinh Vector (Embedding Generation):** Từng chunk văn bản đi qua mô hình Embedding (ví dụ: `text-embedding-3-small`, `bge-m3`...) để chuyển đổi thành một Dense Vector nhiều chiều.
  - *Ví dụ:* Chunk `chunk_001` có nội dung `"RAG combined retrieval..."` $\longrightarrow$ Vector: `[0.12, 0.44, -0.21, ...]`.
- **Lưu trữ có cấu trúc (Vector Storage):** Dữ liệu không chỉ lưu mỗi vector mà lưu một bản ghi tổng hợp chứa 4 trường thông tin cốt lõi.

---

#### b. Cấu trúc bản ghi trong Vector Database

Mỗi bản ghi được lưu trữ dưới dạng một Document Object / JSON hoàn chỉnh:

```json
{
  "id": "chunk_001",
  "vector": [0.12, 0.44, -0.21, 0.08, 0.51],
  "text": "Retrieval-Augmented Generation (RAG) combined retrieval...",
  "metadata": {
    "doc_id": "rag_book",
    "page": 2,
    "chapter": "Retrieval",
    "access_level": "student"
  }
}
```

- **`id`:** Định danh duy nhất của chunk trong hệ thống (`chunk_001`).
- **`vector`:** Tọa độ biểu diễn ngữ nghĩa trong không gian đa chiều, phục vụ cho thuật toán tìm kiếm tương đồng (ANN / HNSW / IVF).
- **`text`:** Đoạn văn bản gốc để LLM đọc và tổng hợp câu trả lời khi được tìm thấy.
- **`metadata`:** Dữ liệu ngữ cảnh phục vụ việc lọc (*filtering*), kiểm soát quyền (*access control*), và trích dẫn (*citation*).

---

## 🎯6. TỔNG KẾT TOÀN BỘ CHƯƠNG 2: OFFLINE PIPELINE INGESTION

Chu trình xử lý dữ liệu ngoại tuyến khép lại với 4 mắt xích hoàn chỉnh:

```text
[Tài liệu thô]
      │
      ▼
 2.1 Extraction          : Trích xuất nội dung đa định dạng & xử lý OCR
      │
      ▼
 2.2 Chunking            : Cắt nhỏ tài liệu (Fixed-size, Semantic, Structure-aware)
      │
      ▼
 2.3 Metadata Enrichment : Gắn thuộc tính cấu trúc (Page, Section, Access Level)
      │
      ▼
 2.4 Vector Indexing     : Tạo Dense Vector & lưu đồng bộ (ID, Vector, Text, Metadata)
      │
      ▼
[Vector Database sẵn sàng phục vụ Online Retrieval]
```

1. **Extraction (2.1):** Trích xuất văn bản sạch từ PDF, Word, HTML, Excel, ảnh quét (OCR) bảo toàn cấu trúc ngữ nghĩa.
2. **Chunking (2.2):** Phân rã văn bản thành các khối thích hợp (Fixed-size overlap, Semantic, Structure-aware) tối ưu cho Embedding & Context Window.
3. **Metadata Enrichment (2.3):** Làm giàu dữ liệu với các thẻ ngữ cảnh (`page`, `section`, `access_level`) hỗ trợ Pre-filtering, Citation và Security.
4. **Vector Indexing (2.4):** Chuyển đổi chunk thành Dense Vector và lưu trữ đồng bộ bản ghi 4 trường (`id`, `vector`, `text`, `metadata`) vào Vector Database.

> **Chuyển tiếp:** Toàn bộ Offline Pipeline Ingestion đã hoàn tất. Tiếp theo là **Chương 3: Online Pipeline Retrieval & Serving** (*Query Rewriting*, *Similarity Search*, *Reranking*, *Context Augmentation & Generation*).

---

## 🔍CHƯƠNG IV: ONLINE PIPELINE RETRIEVAL & SERVING

---

### 1. Tổng quan về Online Pipeline (RAG Runtime)

#### a. Bản chất của Online Pipeline
- Khác với Ingestion Pipeline diễn ra offline, **Online Pipeline Retrieval** (thường được gọi là *RAG Runtime*) là chuỗi xử lý diễn ra theo thời gian thực ngay khi người dùng gửi câu hỏi.
- **Mục tiêu:** Nhận diện ý định câu hỏi, tìm kiếm đúng ngữ cảnh liên quan nhất trong Vector Database, và hỗ trợ LLM tổng hợp câu trả lời chính xác, đáng tin cậy.

---

#### b. Sơ đồ luồng Runtime (Pipeline Flow)

```text
[User Query]
     │
     ▼
 1. PRE-RETRIEVAL (Query Rewriting, Multi-query)
     │
     ▼
 2. SEARCH / RETRIEVAL (Dense / Sparse / Hybrid Search)
     │
     ▼
 3. RERANK (Re-scoring & Cross-Encoder)
     │
     ▼
 4. PROMPT SYNTHESIS & LLM (Ghép context & sinh câu trả lời)
     │
     ▼
[Answer / Final Output]
```

---

### 2. PRE-RETRIEVAL (TIỀN TRUY XUẤT)

#### a. Mục tiêu cốt lõi
Không dùng trực tiếp câu hỏi thô của người dùng để search ngay lập tức, mà tối ưu hóa câu hỏi trước để tăng tỷ lệ tìm trúng tài liệu liên quan.

---

#### b. Query Rewriting (Viết lại truy vấn)

##### i. Vấn đề thực tế
- Người dùng thường hỏi các câu mơ hồ, chứa đại từ thay thế (*"nó"*, *"cái này"*, *"thuật toán đó"*) hoặc phụ thuộc chặt chẽ vào lịch sử trò chuyện phía trước.
- *Ví dụ:*
  - Lịch sử hội thoại trước: Đang bàn về thuật toán HNSW.
  - Câu hỏi hiện tại của người dùng: *"Nó hoạt động kiểu gì?"*
  - Nếu tìm kiếm bằng vector ngay: Hệ thống sẽ không thể hiểu từ *"nó"* là gì, dẫn đến kết quả truy xuất hoàn toàn sai lệch.

##### ii. Cơ chế giải quyết
Sử dụng một mô hình ngôn ngữ nhỏ/nhanh để phân tích lịch sử hội thoại và sinh ra một **Standalone Search Query (Truy vấn độc lập)**:

$$\text{Conversation History} + \text{Current Raw Query} \xrightarrow{\quad\text{LLM}\quad} \text{Standalone Query}$$

- **Kết quả sau khi Rewrite:** `"How does HNSW vector search work?"` (đầy đủ chủ ngữ, ngữ cảnh và từ khóa kỹ thuật).
- 👉 Cực kỳ quan trọng đối với các hệ thống **Conversational RAG (Chatbot hỏi đáp nhiều lượt)**.

---

#### c. Multi-query Generation (Sinh đa truy vấn)

##### i. Cơ chế hoạt động
Một câu hỏi có thể được diễn đạt dưới nhiều góc độ và từ ngữ khác nhau. Hệ thống dùng LLM để phân rã câu hỏi gốc thành $N$ biến thể truy vấn có cùng ý nghĩa nhưng tiếp cận ở các khía cạnh từ khóa khác nhau:

```text
                  [User Query: "How does RAG reduce hallucination?"]
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
            [Question 1]            [Question 2]            [Question 3]
      "How does retrieval-     "Why does external context "How does RAG ground
       grounding reduce LLM     improve factual accuracy   model response?"
          hallucination?"               in RAG?"
                    │                    │                    │
                    ▼                    ▼                    ▼
               [Retrieval]          [Retrieval]          [Retrieval]
                    └────────────────────┬────────────────────┘
                                         ▼
                                  [Merge Results]
```

##### ii. Đánh giá & Điểm đánh đổi (Trade-off)
- **Ưu điểm:** Tăng mạnh độ bao phủ (Recall $\uparrow$), hạn chế tối đa nguy cơ bỏ sót tài liệu do câu hỏi ban đầu dùng từ khóa lệch góc nhìn.
- **Nhược điểm & Đánh đổi:**
  - **Độ trễ tăng (Latency $\uparrow$):** Phải chờ LLM sinh truy vấn và thực hiện nhiều lượt search song song.
  - **Chi phí tăng (Cost $\uparrow$):** Tốn thêm token để LLM rewrite câu hỏi và tăng số lượng request vào Vector DB.
  - **Độ nhiễu tăng (Noise $\uparrow$):** Lấy về nhiều tài liệu hơn cũng đồng nghĩa với việc dễ kéo theo các đoạn context không thực sự liên quan.

---

#### d. Bảng tổng hợp các kỹ thuật Pre-retrieval

| Kỹ thuật | Đầu vào | Đầu ra | Mục đích chính |
| :--- | :--- | :--- | :--- |
| **Query Rewriting** | Câu hỏi thô + Lịch sử hội thoại | 1 câu truy vấn độc lập (*Standalone Query*) | Giải quyết câu hỏi thiếu ngữ cảnh, chứa đại từ thay thế trong Chatbot |
| **Multi-query Generation** | 1 câu hỏi của người dùng | Nhiều biến thể câu hỏi (*Multiple Sub-queries*) | Mở rộng góc độ tìm kiếm để tối đa hóa Recall |

---

### 3. SEARCH METHODS & RANK FUSION (PHƯƠNG PHÁP TÌM KIẾM & HỢP NHẤT)

#### a. Tổng quan về Search Methods trong RAG Runtime

Sau bước tiền xử lý câu hỏi (Pre-retrieval), hệ thống thực hiện giai đoạn **Search / Retrieval** để truy xuất các đoạn văn bản có liên quan nhất. Để đảm bảo độ mạnh mẽ (*robustness*) trong môi trường thực tế, hệ thống không chỉ dùng tìm kiếm vector đơn lẻ mà kết hợp 3 kỹ thuật cốt lõi:

```text
                      SEARCH & RETRIEVAL PIPELINE
                                  │
      ┌───────────────────────────┼───────────────────────────┐
      ▼                           ▼                           ▼
1. METADATA FILTERING     2. HYBRID SEARCH           3. RRF SCORING
(Thu hẹp & Cô lập)         (Dense Vector + BM25)      (Hợp nhất thứ hạng)
```

---

#### b. Đi sâu vào các phương pháp tìm kiếm

##### i. Metadata Filtering (Lọc dữ liệu theo thuộc tính & Bảo mật)
- **Vấn đề không gian dữ liệu lớn & Đa người dùng:**
  - Giả sử một hệ thống Vector Database lưu trữ: 3.000 courses, 100 users, và 10.000 documents.
  - Nếu người dùng đang thao tác trong không gian `space_id = "ABC123"`, hệ thống không thể tìm kiếm trên toàn bộ cơ sở dữ liệu rồi hy vọng phép đo độ tương đồng vector tự động lọc ra đúng vùng dữ liệu.
- **Vai trò cốt lõi:**
  - **Data Isolation & Security Design:** Bắt buộc lọc cứng điều kiện trước (*pre-filter*) để đảm bảo tính cô lập và bảo mật dữ liệu giữa các người dùng hoặc tổ chức.
  - **Cải thiện độ liên quan (Relevance):** Thu hẹp không gian tìm kiếm, loại bỏ hoàn toàn các tài liệu nhiễu nằm ngoài phạm vi truy vấn.
  - **Các trường filter phổ biến:** `space_id`, `user_id`, `document_id`, `course_date`, `language`, `category`, `access_level`.

##### ii. Hybrid Search (Tìm kiếm kết hợp: Vector + Keyword)
Là tiêu chuẩn vàng (*de facto standard*) trong các hệ thống Production RAG để khắc phục nhược điểm của từng phương pháp đơn lẻ:

$$\text{Hybrid Search} = \text{Dense Vector Search (Semantic)} + \text{BM25 Search (Lexical)}$$

```text
                   [User Query / Standalone Query]
                                  │
         ┌────────────────────────┴────────────────────────┐
         ▼                                                 ▼
[Dense Vector Search]                             [BM25 Keyword Search]
• Bắt trọn ngữ cảnh ngữ nghĩa (Meaning)           • Khớp chính xác từ khóa (Exact Keyword)
• Xử lý từ đồng nghĩa (Synonyms)                  • Mã định danh, Mã lỗi, SKU (IDs, Codes)
• Hiểu ngôn ngữ tự nhiên linh hoạt                 • Tên riêng, Thuật ngữ chuyên ngành (Names, Terms)
         │                                                 │
         └────────────────────────┬────────────────────────┘
                                  ▼
                         [Fusion / Hợp nhất]
```

- **Sự bù trừ hoàn hảo:** Khi người dùng hỏi câu hỏi kết hợp cả thuật ngữ kỹ thuật/mã định danh cụ thể lẫn diễn đạt tự nhiên, Hybrid Search đảm bảo không bị mất dấu từ khóa cứng mà vẫn bắt đúng ý định câu hỏi.

##### iii. RRF (Reciprocal Rank Fusion) Scoring – Thuật toán hợp nhất thứ hạng
- **Vấn đề khi kết hợp điểm số thô (Raw Score):**
  - Dense Vector Search trả về điểm Cosine Similarity (hoặc Dot Product) thường dao động trong khoảng $[0, 1]$ hoặc $[-1, 1]$.
  - BM25 trả về điểm số không bị chặn trên ($[0, +\infty)$), phụ thuộc vào tần suất từ và độ dài tài liệu.
  - 👉 **Không thể cộng hoặc so sánh trực tiếp raw scores của hai hệ thống này với nhau.**
- **Nguyên lý của RRF:**
  - RRF giải quyết bằng cách: Bỏ qua giá trị điểm thô và chỉ sử dụng **vị trí thứ hạng (rank)** của tài liệu trong từng danh sách kết quả trả về.
  - **Công thức toán học:**
    $$RRF(d) = \sum_{m \in M} \frac{1}{k + \text{rank}_m(d)}$$
    - *Trong đó:*
      - $M$: Tập hợp các hệ thống tìm kiếm (ở đây gồm Dense Search và BM25).
      - $\text{rank}_m(d)$: Vị trí thứ hạng của tài liệu $d$ trong hệ thống tìm kiếm $m$ (vị trí bắt đầu từ $1, 2, 3...$).
      - $k$: Hằng số làm mượt (thường mặc định $k = 60$) để giảm sự chênh lệch quá lớn giữa các thứ hạng đầu.
- **Cơ chế ưu tiên của RRF:** Một tài liệu $d$ nếu xuất hiện ở thứ hạng cao trong đồng thời cả hai hệ thống (ví dụ: tài liệu $A$ và $C$ đều nằm trong Top đầu của cả Vector Search và BM25) thì sẽ nhận được điểm $RRF(d)$ rất cao và được ưu tiên đẩy lên vị trí cao nhất.

---

#### c. Bảng tổng hợp các thành phần trong Phần 3.2

| Thành phần | Đầu vào | Chức năng chính | Kết quả đầu ra |
| :--- | :--- | :--- | :--- |
| **Metadata Filtering** | Bộ lọc điều kiện (`space_id`, `role`...) | Phân vùng dữ liệu, bảo mật, cô lập phạm vi tìm kiếm | Không gian vector thu hẹp hợp lệ |
| **Dense Vector Search** | Vector câu hỏi truy vấn | Tìm kiếm theo độ tương đồng ngữ nghĩa | Danh sách tài liệu xếp theo Cosine Similarity |
| **BM25 Search** | Chuỗi từ khóa truy vấn | Tìm kiếm theo khớp chính xác từ khóa, ID, mã code | Danh sách tài liệu xếp theo điểm BM25 |
| **RRF Scoring** | Các bảng xếp hạng kết quả riêng lẻ | Chuẩn hóa và hợp nhất dựa trên vị trí thứ tự | Một bảng xếp hạng kết quả cuối cùng đã được tối ưu |

---

### 4. RERANKING VỚI CROSS-ENCODER

#### a. Lý do cần Rerank
- Sau bước Retrieval (3.1 - 3.2), hệ thống có thể thu về tập ứng viên khoảng 20 tài liệu (Top 20 Candidates).
- Không nên nạp toàn bộ 20 tài liệu này vào LLM vì sẽ gây ra:
  - Chi phí token tăng cao.
  - Độ trễ (*latency*) phản hồi chậm.
  - Hiện tượng loãng ngữ cảnh (*Context Dilution*) và làm giảm chất lượng câu trả lời của LLM.

---

#### b. Mô hình Two-stage Pipeline

```text
[User Query]
     │
     ▼
[3.1 - 3.2: Retrieval Pipeline] ──► Thu được tập ứng viên rộng (Ví dụ: Top 20 Candidates)
     │
     ▼
[3.3: Cross-Encoder Reranker]   ──► Chắt lọc & sắp xếp lại (Ví dụ: Top 3 - 5 Chunks)
     │
     ▼
[3.4: Augmented Generation]     ──► Ghép Context + Prompt đưa vào LLM sinh câu trả lời
     │
     ▼
[3.5: Post-RAG Guardrails]      ──► Rà soát an toàn, tính xác thực & trích dẫn
     │
     ▼
[Final Verified Answer]
```

Cơ chế xử lý 2 giai đoạn (Two-stage Pipeline):

$$\text{Query} \xrightarrow{\quad\text{Fast Retrieval (Ưu tiên Speed / Recall)}\quad} \text{Top 20} \xrightarrow{\quad\text{Cross-Encoder (Ưu tiên Precision)}\quad} \text{Top 3 - 5} \xrightarrow{\quad} \text{LLM}$$

---

#### c. Cơ chế hoạt động của Cross-Encoder
- **Đánh giá trực tiếp & đồng thời:** Đánh giá cặp `(Query, Document)` cùng lúc qua các lớp Transformer chú ý chéo (*cross-attention*), thay vì sinh embedding độc lập cho từng phần như Bi-Encoder.
- **Độ chính xác vượt trội:** Cho độ tương quan ngữ nghĩa chính xác hơn hẳn Bi-Encoder, dù tốc độ tính toán chậm hơn.
- **Phân công vai trò:**
  - **Vector Search / Hybrid Search:** Đảm nhận khâu *Candidate Generation* (sinh tập ứng viên nhanh với Recall cao).
  - **Cross-Encoder Reranker:** Đảm nhận khâu *Candidate Refinement* (tinh chỉnh, chọn lọc và sắp xếp lại với Precision cao).

---

### 5. AUGMENTED GENERATION (CHỮ "G" TRONG RAG)

#### a. Cơ chế hoạt động
Sau khi chọn ra Top 3 - 5 ngữ cảnh chất lượng nhất từ bước Reranking, hệ thống ghép nối câu hỏi của người dùng, context vừa trích xuất và câu lệnh điều khiển (*System Instruction*) để LLM sinh câu trả lời có căn cứ thực tế (*grounded answer*).

---

#### b. Cấu trúc Prompt chuẩn hóa

$$\text{Final Prompt} = \text{System Instruction} + \text{Retrieved Context} + \text{User Query}$$

```text
System: Answer using only the provided context. If the answer cannot be found, say that the information is unavailable.

Context:
- [Chunk 1: HNSW multi-layer skip list mechanics...]
- [Chunk 2: HNSW beam search configuration...]

Question: How does HNSW vector search work?
```

---

### 6. POST-RAG GUARDRAILS (HÀNG RÀO AN TOÀN & KIỂM ĐỊNH SAU SINH)

#### a. Bản chất & Vị trí triển khai
Sau khi LLM tạo ra câu trả lời thô (*raw answer*), hệ thống chuyển qua các lớp kiểm định an toàn trước khi trả kết quả cuối cùng cho người dùng.

> **Lưu ý triển khai:** Guardrails có thể được bố trí ở nhiều vị trí trong hệ thống (như Input Guardrails kiểm tra prompt đầu vào). Khái niệm Post-RAG Guardrails chỉ vị trí triển khai phổ biến và quan trọng nhất ở đầu ra để kiểm soát chất lượng phản hồi.

---

#### b. 4 Lớp kiểm định an toàn

```text
[LLM Raw Answer]
       │
       ▼
 1. Grounding Checker (Kiểm tra câu trả lời có bám sát context không, loại bỏ ảo giác)
       │
       ▼
 2. Policy Checker (Kiểm tra vi phạm chính sách nội dung, ngôn từ độc hại)
       │
       ▼
 3. PII Checker (Phát hiện & ẩn thông tin định danh cá nhân: Số điện thoại, Email, CCCD...)
       │
       ▼
 4. Citation Checker (Kiểm tra trích dẫn nguồn có tương ứng và chính xác với chunks đã dùng không)
       │
       ▼
[Final Verified Answer]
```

##### i. Grounding Checker
Kiểm tra câu trả lời có căn cứ từ tập context hay không; phát hiện và chặn các chi tiết ảo giác (*hallucination*) do LLM tự bịa ra.

##### ii. Policy Checker
Rà soát vi phạm chính sách an toàn nội dung, ngôn từ thù hận, hoặc các chủ đề cấm của doanh nghiệp/tổ chức.

##### iii. PII Checker (Personally Identifiable Information)
Phát hiện và ẩn/mã hóa các thông tin định danh cá nhân nhạy cảm (*Số điện thoại, Email, Số CMND/CCCD, Thẻ tín dụng*).

##### iv. Citation Checker
Đảm bảo các trích dẫn nguồn (*citations*) nằm đúng phân đoạn chunk đã được truy xuất và không bị dẫn sai địa chỉ.

---

## 🎯7. TỔNG KẾT TOÀN BỘ CHƯƠNG 3: ONLINE PIPELINE RETRIEVAL & SERVING

| Bước | Thành phần | Trọng tâm tối ưu | Kết quả đầu ra |
| :--- | :--- | :--- | :--- |
| **3.1** | **Pre-retrieval** | Tối ưu hóa câu hỏi (Rewrite, Multi-query) | Standalone Query / Sub-queries |
| **3.2** | **Search & Rank Fusion** | Thu hẹp phạm vi (Filter) & Tìm kiếm kết hợp (Hybrid + RRF) | Top 20 Candidates |
| **3.3** | **Cross-Encoder Reranker** | Độ chính xác (*Precision*) & Độ liên quan sâu | Top 3 - 5 Chunks tinh hoa |
| **3.4** | **Augmented Generation** | Khóa chặt LLM vào Context (*Grounding*) | Câu trả lời thô từ LLM |
| **3.5** | **Post-RAG Guardrails** | An toàn, bảo mật dữ liệu & chống ảo giác | Câu trả lời hoàn chỉnh đã qua kiểm định |

> **Chuyển tiếp:** Toàn bộ Online Pipeline Retrieval & Serving đã hoàn thiện. Tiếp theo là **Chương 4: Graph RAG & Kiến trúc nâng cao** (*Knowledge Graph Integration*, *Multi-query*, *HyDE*, *Self-RAG*, *Agentic RAG*).


--

## 🌐 CHƯƠNG 4: GRAPHRAG & ADVANCED ARCHITECTURES

---

### 1. Tổng quan về Kiến trúc RAG nâng cao

Trong các bài toán thực tế phức tạp, kiến trúc RAG nâng cao thường được xây dựng dựa trên **3 trụ cột cốt lõi**:

- **Knowledge Graphs (Đồ thị tri thức):** Biểu diễn các thực thể và mối quan hệ phức tạp để phục vụ suy luận toàn cục và đa bước.
- **Vector Models (Mô hình Vector):** Tìm kiếm ngữ nghĩa cục bộ dựa trên độ tương đồng không gian.
- **Agentic RAG (RAG dạng tác tử):** Hệ thống LLM tự định tuyến, lập kế hoạch và gọi công cụ linh hoạt.

---

### 2. KNOWLEDGE GRAPH TRONG RAG

#### a. Bản chất sự khác biệt: Vector Search vs. Graph-based Search
- **Vector Search thuần túy:** Trả lời câu hỏi *"Đoạn text nào có nội dung/ngữ nghĩa tương đồng với câu hỏi của người dùng?"*.
- **Graph-based Search:** Trả lời câu hỏi *"Các thực thể (entities) kết nối và tương tác với nhau như thế nào qua các mối quan hệ (relationships)?"*.

---

#### b. Thành phần cấu tạo: Nodes, Edges & Triples

Đồ thị tri thức lưu trữ thông tin dưới dạng bộ ba quan hệ (**Triples**):

$$\text{Triple} = (\text{Subject}, \text{Predicate}, \text{Object}) = (\text{Thực thể nguồn}, \text{Mối quan hệ}, \text{Thực thể đích})$$

- **Nodes (Đỉnh / Thực thể):** Biểu diễn con người, tổ chức, sản phẩm, khái niệm (ví dụ: `OpenAI`, `GPT-4`).
- **Edges (Cạnh / Quan hệ):** Đường nối có hướng mô tả bản chất liên kết giữa hai thực thể.
- **Ví dụ Triple:**
  $$\text{(OpenAI)} \xrightarrow{\quad\text{developed}\quad} \text{(GPT-4)}$$
  - *Subject:* `OpenAI`
  - *Predicate:* `developed` (phát triển)
  - *Object:* `GPT-4`

---

#### c. Suy luận toàn cục: Local Search vs. Global Search (Global Context Reasoning)

| Tiêu chí | Local Search (Vector Search truyền thống) | Global Search (GraphRAG / Community Summaries) |
| :--- | :--- | :--- |
| **Dạng câu hỏi tối ưu** | Câu hỏi cụ thể, khu biệt (*"HNSW là gì?"*, *"Hạn mức bảo hiểm là bao nhiêu?"*) | Câu hỏi tổng hợp, bao quát (*"Những chủ đề chính xuất hiện xuyên suốt toàn bộ tập tài liệu là gì?"*) |
| **Cơ chế hoạt động** | Truy xuất các chunk có độ tương đồng vector cao nhất với câu hỏi | Gom cụm đồ thị (*Community Detection*) $\to$ Tạo bản tóm tắt cụm (*Community Summaries*) để suy luận ở cấp độ vĩ mô |
| **Hạn chế** | Dễ bỏ sót các mẫu hình phân tán rải rác ở hàng trăm tài liệu khác nhau | Chi phí trích xuất thực thể và dựng đồ thị ban đầu cao hơn |

---

#### d. Giải thích chuyên sâu: Multi-hop Search & Reasoning (Truy xuất đa chặng)

##### i. Vấn đề cốt lõi: Tại sao Vector Search đơn thuần gặp khó khăn?
Vector Search chỉ tính khoảng cách ngữ nghĩa giữa **câu hỏi của người dùng** và **từng đoạn văn bản đơn lẻ**. Trong các câu hỏi logic đa bước, câu trả lời nằm ở **chuỗi liên kết bắc cầu** giữa nhiều tài liệu độc lập:

- **Tài liệu 1:** *"Alice làm việc tại Công ty A."*
- **Tài liệu 2:** *"Công ty A đã hoàn tất việc mua lại Công ty B vào năm ngoái."*
- **Tài liệu 3:** *"Công ty B là đơn vị trực tiếp phát triển Sản phẩm X."*

*Nếu người dùng hỏi:* *"Sản phẩm nào được phát triển bởi công ty được mua lại bởi công ty mà Alice đang làm việc?"*

- **Cách Vector Search thất bại:** 
  - Câu hỏi chứa các từ khóa `"Alice"`, `"công ty mua lại"`, `"phản hồi sản phẩm"`.
  - Khi embed câu hỏi, vector truy vấn sẽ tìm kiếm những đoạn chứa cả `"Alice"` lẫn `"Sản phẩm"`.
  - **Tài liệu 3** chứa đáp án `"Sản phẩm X"` nhưng hoàn toàn **không nhắc đến `"Alice"` hay `"Công ty A"`**, dẫn đến điểm tương đồng ngữ nghĩa giữa câu hỏi và Tài liệu 3 cực thấp $\rightarrow$ Vector Search bỏ sót Tài liệu 3.

##### ii. Cách Knowledge Graph giải quyết (Graph Traversal)
Knowledge Graph chuyển đổi các liên kết rời rạc thành một chuỗi đường đi trên đồ thị (*Graph Path*):

```text
(Alice) ──[works_at]──► (Công ty A) ──[acquired]──► (Công ty B) ──[developed]──► (Sản phẩm X)
```

1. **Khởi tạo (Entity Linking):** Xác định thực thể gốc từ câu hỏi: `Alice`.
2. **Chặng 1 (Hop 1):** Truy vấn quan hệ `works_at` $\to$ Thu được `Công ty A`.
3. **Chặng 2 (Hop 2):** Truy vấn quan hệ `acquired` $\to$ Thu được `Công ty B`.
4. **Chặng 3 (Hop 3):** Truy vấn quan hệ `developed` $\to$ Thu được kết quả chính xác: `Sản phẩm X`.

👉 **Kết luận:** GraphRAG cho phép hệ thống "bước" (*hop*) qua từng nút quan hệ để kết nối các mảnh tri thức rải rác một cách chính xác tuyệt đối.

---

### 3.SOTA GRAPH-RAG MODELS (CÁC MÔ HÌNH GRAPHRAG TIÊN TIẾN)

#### a. Tổng quan về các mô hình SOTA trong GraphRAG
Các mô hình State-of-the-Art (SOTA) hiện đại trong GraphRAG giải quyết các bài toán mà tìm kiếm Naive Top-K Vector truyền thống không thể xử lý tốt:
- **Microsoft GraphRAG:** Khai thác cấu trúc phân cấp cộng đồng (*Community Summaries*) để giải quyết các câu hỏi tổng hợp toàn cục (*Global Sensemaking*).
- **LightRAG (Dual-level Retrieval):** Phân tầng truy xuất kép giữa thực thể chi tiết (*Low-level*) và chủ đề tổng quát (*High-level*).
- **HippoRAG (Bio-inspired Memory):** Mô phỏng cơ chế hồi hải mã (*Hippocampus*) của não bộ để thực hiện liên tưởng tri thức (*Associative Memory Retrieval*).

```text
                     SOTA GRAPHRAG MODELS
                               │
  ┌────────────────────────────┼────────────────────────────┐
  ▼                            ▼                            ▼
1. MICROSOFT GRAPHRAG       2. LIGHTRAG (DUAL-LEVEL)     3. HIPPORAG (BIO-INSPIRED)

Community Detection        - Low-level: Entities/Edges   - Hippocampus mechanics

Hierarchical Summaries     - High-level: Themes/Topics   - Associative memory paths

Global synthesis on corpus - Adapt to query granularity  - Non-parametric continual KG
```

---

#### b. Chi tiết các mô hình SOTA

##### i. Microsoft GraphRAG (Multi-Community Graph Indexing)
- **Quy trình xử lý cốt lõi (Concept Flow):**

$$\text{Raw Documents} \longrightarrow \text{Entity \& Relationship Extraction} \longrightarrow \text{Knowledge Graph} \longrightarrow \text{Community Detection} \longrightarrow \text{Community Summaries}$$

- **Cơ chế Community Detection:** Sử dụng thuật toán phân cụm đồ thị (như *Leiden algorithm*) để chia đồ thị tri thức thành các nhóm/cụm cộng đồng tri thức liên kết chặt chẽ:
  - *Community A:* Cụm chủ đề về LLM, Architecture, Transformers.
  - *Community B:* Cụm chủ đề về Vector Database, Search, HNSW Indexing.
  - *Community C:* Cụm chủ đề về Evaluation, Benchmarks, Ragas.
- **Community Summaries:** LLM tổng hợp tóm tắt nội dung của từng cụm cộng đồng trước ở giai đoạn offline.
- **Điểm mạnh vượt trội (Global Sensemaking):** Vượt trội hoàn toàn so với Naive Top-K Vector Retrieval khi xử lý các câu hỏi vĩ mô trên toàn bộ tập dữ liệu (ví dụ: *"Những thách thức kỹ thuật cốt lõi được thảo luận trong toàn bộ các bài báo là gì?"*).

##### ii. LightRAG (Dual-Level Retrieval – Truy xuất hai tầng)
- **Vấn đề của các truy vấn khác biệt:** Các câu hỏi từ người dùng có mức độ bao quát (*granularity*) rất khác nhau:
  - Có câu hỏi yêu cầu **độ chi tiết cục bộ** (*Specific / Local*): *"Ai là người sáng lập công ty X?"*
  - Có câu hỏi yêu cầu **tầm nhìn bao quát** (*Abstract / Global*): *"Chủ đề chính xuyên suốt tài liệu này là gì?"*
- **Cơ chế Dual-Level (Phân tầng kép):** LightRAG thiết kế luồng truy xuất ở hai cấp độ độc lập nhưng tương hỗ:
  - **Low-level (Tầng cục bộ):** Truy xuất trực tiếp vào các thực thể cụ thể (*Entities*), quan hệ trực tiếp (*Relationships*) và các đoạn trích nhỏ.
  - **High-level (Tầng khái niệm):** Truy xuất vào các khái niệm rộng (*Concepts*), chủ đề lớn (*Themes/Topics*) và mối liên kết trừu tượng.
  - **Cân bằng linh hoạt:** Tự động điều hướng và kết hợp tỷ trọng giữa Low-level và High-level dựa trên bản chất của câu truy vấn.

##### iii. HippoRAG (Bio-inspired Human Memory Architecture)
- **Cảm hứng sinh học từ Hồi hải mã (Hippocampus):** Lấy cảm hứng từ cấu trúc hồi hải mã (*Hippocampus*) trong não người – nơi tiếp nhận trải nghiệm mới, tạo liên kết liên tưởng (*associative indexing*) và kích hoạt vùng vỏ não lưu trữ ký ức dài hạn.
- **Mục tiêu:** Không chỉ tìm các vector "gần nhau" trong không gian tĩnh, mà tìm kiếm thông qua **các liên kết liên tưởng ngữ nghĩa (Associative Relationships)**.
- **Điểm đáng học & Đột phá kỹ thuật:**
  - **Không chỉ là Vector Similarity:** Chuyển dịch từ việc đo khoảng cách hình học đơn thuần sang cơ chế kích hoạt liên tưởng đa chặng (*Associative Activation* / Thuật toán tương tự *Personalized PageRank*).
  - Khi gặp một manh mối truy vấn mới, hệ thống kích hoạt nút thực thể liên quan trên đồ thị và "lan truyền" tín hiệu qua các đường liên kết để tìm ra toàn bộ chuỗi tri thức bắc cầu nằm phân mảnh.

---

#### c. Bảng so sánh các mô hình SOTA GraphRAG

| Tiêu chí | Microsoft GraphRAG | LightRAG | HippoRAG |
| :--- | :--- | :--- | :--- |
| **Cảm hứng thiết kế** | Phân cụm cộng đồng mạng xã hội / Đồ thị phức tạp | Tối ưu hóa truy xuất theo mức độ hạt (*Granularity*) | Cấu trúc bộ nhớ liên tưởng sinh học (Hồi hải mã) |
| **Cơ chế cốt lõi** | Phân tầng cụm (Leiden) & Sinh bản tóm tắt cộng đồng | Tách biệt Low-level (*Entity*) và High-level (*Theme*) | Kích hoạt liên tưởng & lan truyền đồ thị (*Associative Path*) |
| **Thế mạnh lớn nhất** | Khả năng tổng hợp báo cáo vĩ mô toàn tập dữ liệu | Linh hoạt và tối ưu chi phí cho cả câu hỏi hẹp lẫn rộng | Giải quyết xuất sắc các bài toán suy luận liên tưởng phức tạp |

---

### 4. GENTIC RAG & SELF-CORRECTION (RAG TÁC TỬ & CƠ CHẾ TỰ HIỆU CHỈNH)

#### a. Sự dịch chuyển từ Fixed Pipeline sang Decision-Making RAG
Sự phát triển từ hệ thống RAG tĩnh sang RAG thông minh dạng tác tử:
- **Traditional RAG (Fixed Pipeline):** Luồng xử lý cứng nhắc, tuyến tính một chiều:
  $$\text{Query} \longrightarrow \text{Retrieve} \longrightarrow \text{Generate}$$
  - *Hạn chế:* Bắt buộc phải tìm kiếm dù câu hỏi không cần; nếu kết quả tìm kiếm rác/sai thì mô hình vẫn nhồi vào prompt và sinh câu trả lời sai.
- **Agentic RAG (Decision-Making / Dynamic Workflow):** Mô hình chuyển sang cơ chế tự ra quyết định (*Autonomous Decision-Making*), chủ động đánh giá chất lượng tài liệu và tự sửa sai theo thời gian thực (*Self-Correction Loops*).

---

#### b. Cơ chế vận hành của Agentic RAG & Self-Correction

```text
                      [User Query]
                           │
                           ▼
               [Cần Retrieval không?]
                 ├── (Không) ──► [Dùng kiến thức nội tại / LLM Answer]
                 │
                 └── (Có) ─────► [Lập kế hoạch & Query Decomposition]
                                        │
                                        ▼
                                 [Thực hiện Retrieval]
                                        │
                                        ▼
                          [Đánh giá tài liệu: Relevant / Đủ chưa?]
                                 ├── (Không / Thiếu) ──► [Rewrite Query / Dùng Tool khác] ──┐
                                 │                                                           │
                                 │ ◄─────────────────────────────────────────────────────────┘
                                 │
                                 └── (Có / Đủ) ────────► [Generate Answer]
                                                                │
                                                                ▼
                                                        [Verify Grounding]
                                                         ├── (Sai / Ảo giác) ──► [Tự sửa câu trả lời]
                                                         └── (Đúng chuẩn)   ──► [Final Output]
```

---

#### c. Các quyết định tự động của Agent trong Runtime
Một Agentic RAG system sở hữu năng lực điều phối linh hoạt thông qua **7 câu hỏi tự vấn (*Self-Reflection & Routing*)**:

1. **Có cần retrieve không?** (*Do I need retrieval?*): Nhận diện các câu chào hỏi xã giao hoặc suy luận logic thuần túy để không tốn chi phí search database.
2. **Nên truy xuất từ nguồn nào?** (*Which source/tool to query?*): Định tuyến giữa Vector DB, Knowledge Graph, SQL DB, Search API hoặc Calculator.
3. **Câu hỏi có quá phức tạp không?** (*Query Decomposition*): Tự động chia nhỏ câu hỏi phức tạp thành nhiều câu hỏi phụ (*sub-queries*) tuần tự.
4. **Tài liệu tìm về có thực sự liên quan không?** (*Is the retrieved context relevant?*): Đánh giá độ tin cậy và khớp nối của chunks trước khi dùng.
5. **Có cần tìm kiếm lại không?** (*Rewrite & Search again?*): Nếu tài liệu thu được không đạt yêu cầu, tự động viết lại truy vấn để search tiếp vòng mới.
6. **Bằng chứng đã đủ chưa?** (*Is evidence sufficient?*): Nếu chưa đủ dữ liệu để kết luận, kích hoạt tìm kiếm bổ sung (*multi-hop retrieval*).
7. **Câu trả lời có bám sát ngữ cảnh không?** (*Is the answer grounded & hallucination-free?*): Tự đối soát câu trả lời vừa sinh với context trích xuất trước khi trả về cho người dùng.

---

#### d. Bảng so sánh: Traditional RAG vs. Agentic RAG

| Tiêu chí | Traditional RAG (Fixed Pipeline) | Agentic RAG (Self-Correction) |
| :--- | :--- | :--- |
| **Quy trình luồng** | Tuyến tính, cố định 1 chiều | Động, có rẽ nhánh, lặp vòng (*loop*) và tự sửa sai |
| **Tính linh hoạt** | Rất thấp (luôn chạy đúng 1 luồng) | Rất cao (thích ứng theo độ khó của câu hỏi) |
| **Xử lý Retrieval kém** | Chấp nhận context rác $\to$ Dễ sinh ảo giác | Đánh giá lại context $\to$ Viết lại truy vấn & search lại |
| **Khả năng dùng công cụ** | Chỉ truy xuất từ 1 Vector DB cố định | Tự chọn Vector DB, Knowledge Graph, Web Search, Code Tool |
| **Chi phí & Độ trễ** | Thấp và ổn định | Cao hơn (do có bước suy luận, đánh giá và retry) |

---

## 🎯 5. TỔNG KẾT TOÀN BỘ CHƯƠNG 4: GRAPHRAG & ADVANCED ARCHITECTURES

Chương 4 hoàn thiện bức tranh về các kiến trúc RAG hiện đại nhất:
1. **Knowledge Graph Fundamentals (4.1):** Cấu trúc Triples `(Subject, Predicate, Object)`, giải quyết bài toán Global Reasoning và Multi-hop Traversal mà Vector Search đơn lẻ gặp giới hạn.
2. **SOTA GraphRAG Models (4.2):** 
   - *Microsoft GraphRAG:* Phân cụm cộng đồng (*Community Summaries*) phục vụ tổng hợp toàn tập dữ liệu.
   - *LightRAG:* Cân bằng truy xuất hai tầng Low-level (Entities) và High-level (Themes).
   - *HippoRAG:* Kích hoạt liên tưởng bộ nhớ mô phỏng sinh học hồi hải mã (*Hippocampus*).
3. **Agentic RAG & Self-Correction (4.3):** Chuyển dịch từ đường ống cố định sang tác tử tự ra quyết định, tự lập kế hoạch phân rã câu hỏi, đánh giá chất lượng tài liệu và tự hiệu chỉnh vòng lặp.

> **Chuyển tiếp:** Toàn bộ Chương 4 về GraphRAG & Kiến trúc nâng cao đã hoàn tất. Tiếp theo là **Chương 5: Evaluation & Operationalization** (*Ragas*, *TruLens*, *Latency*, *Cost*, *Production Monitoring*).

---

## 📊 CHƯƠNG 5: EVALUATION & OPERATIONALIZATION (ĐÁNH GIÁ & VẬN HÀNH RAG THỰC TẾ)

---

### 1. Tổng quan về Đánh giá và Vận hành

Một sai lầm phổ biến khi triển khai RAG là dừng lại ở mức *"chạy được"* (`PDF + Vector DB + LLM -> It works`), nhưng không đo lường được hệ thống hoạt động tốt đến đâu. Chương 5 cung cấp khung đánh giá và vận hành sản phẩm thông qua **3 trụ cột cốt lõi**:
- **5.1 RAG Assessment Metrics (Bộ ba chỉ số RAG Triad):** Đo lường và định vị chính xác vị trí lỗi.
- **5.2 Quality Control & Observability:** Kiểm soát chất lượng, cây chẩn đoán lỗi (*Error Tree*), giám sát độ trễ và bảo mật dữ liệu (*ACL*, *PII*).
- **5.3 Cost & Latency Management:** Cân bằng bài toán chất lượng, chi phí token và tốc độ phản hồi trong production.

```text
               EVALUATION & OPERATIONALIZATION
                              │
  ┌───────────────────────────┼───────────────────────────┐
  ▼                           ▼                           ▼
5.1 RAG ASSESSMENT METRICS   5.2 QUALITY CONTROL       5.3 COST & LATENCY
(Bộ ba chỉ số RAG Triad)     (Error Tree, ACL, PII)    (Cân bằng Routing)

Context Relevance          - Diagnostic Error Tree   - Simple vs Complex Routing

Faithfulness (Groundedness)- Observability & Logging - Tối ưu token & Latency

Answer Relevance           - Security ACL & Masking  - Cân bằng UX thực tế
```

---

### 2.RAG ASSESSMENT METRICS (BỘ BA CHỈ SỐ RAG TRIAD)

Bộ ba chỉ số cốt lõi tạo thành tam giác đánh giá RAG, đóng vai trò như công cụ chẩn đoán (*diagnostic tool*) để xác định lỗi thuộc về khâu nào:

```text
              [User Question]
                 /        \
                /          \
(Context Relevance)          (Answer Relevance)
              /              \
             ▼                ▼
     [Retrieved Context] ──► [LLM Answer]
       (Faithfulness / Groundedness)
```

#### a. Context Relevance (Độ liên quan của ngữ cảnh)
- **Câu hỏi kiểm tra:** *Các đoạn context trích xuất về có thực sự liên quan đến câu hỏi không?*
- **Ví dụ:** Người dùng hỏi *"HNSW là gì?"*, hệ thống lấy về 3 chunk gồm: `HNSW graph search`, `ANN indexing`, và `Vietnamese cooking recipe`. Chunk thứ 3 hoàn toàn là nhiễu (*noise*).
- **Chẩn đoán:** Nếu chỉ số này thấp $\longrightarrow$ **Lỗi ở khâu Retrieval Pipeline** (Embedding model, chiến lược chunking, query rewrite, metadata filtering hoặc cấu hình Top-K).

#### b. Faithfulness / Groundedness (Tính trung thực / Bám sát ngữ cảnh)
- **Câu hỏi kiểm tra:** *Câu trả lời của LLM có hoàn toàn dựa trên context được cung cấp hay tự ý bịa đặt (ảo giác)?*
- **Ví dụ:** Context chỉ ghi *"HNSW là thuật toán ANN dạng đồ thị"*, nhưng LLM trả lời *"HNSW được phát minh bởi Google vào năm 2010"*. Thông tin về Google/2010 không có trong context $\longrightarrow$ Câu trả lời không faithful.
- **Chẩn đoán:** Nếu chỉ số này thấp $\longrightarrow$ **Lỗi ở khâu Generation** (Prompt chưa đủ chặt, System Instruction thiếu ràng buộc grounding, chất lượng model LLM kém).

#### c. Answer Relevance (Độ liên quan của câu trả lời)
- **Câu hỏi kiểm tra:** *Câu trả lời có trực tiếp giải quyết đúng trọng tâm câu hỏi của người dùng không?*
- **Ví dụ:** Người dùng hỏi *"HNSW hoạt động như thế nào?"*, LLM trả lời *"Vector database rất hữu ích cho các ứng dụng AI hiện đại"*. Dù thông tin đúng về mặt tri thức chung nhưng không trả lời câu hỏi.
- **Chẩn đoán:** Nếu chỉ số này thấp $\longrightarrow$ **Lỗi ở khâu Query Understanding hoặc sinh phản hồi** (LLM không hiểu ý định người dùng, context bị lệch hướng).

---

### 3.QUALITY CONTROL, OBSERVABILITY & SECURITY

#### a. Error Tree (Cây chẩn đoán lỗi)
Thay vì phàn nàn chung chung *"LLM trả lời tệ"*, kỹ sư RAG phân rã theo cây chẩn đoán:

```text
[Wrong / Bad Answer]
├── Retrieval Problem
│    ├── Bad Chunking (Cắt rách câu, mất ý)
│    ├── Bad Embedding (Vector bị lệch ngữ nghĩa)
│    ├── Bad Query (Chưa rewrite, câu hỏi thô thiếu ngữ cảnh)
│    └── Missing / Outdated Data (Tài liệu nguồn bị thiếu hoặc lỗi thời)
├── Reranking Problem (Cross-Encoder loại nhầm tài liệu quan trọng)
└── Generation Problem
     ├── Hallucination (LLM tự suy diễn ngoài context)
     └── Poor System Prompt (Chưa khóa chặt hướng dẫn grounding)
```

#### b. Data Observability & System Latency Breakdown
Để biết điểm nghẽn (*bottleneck*) của hệ thống đang nằm ở đâu, cần ghi log chi tiết từng công đoạn:
- **Các trường bắt buộc log:** `Raw Query`, `Rewritten Query`, `Retrieval Scores`, `Reranker Scores`, `Document Sources`, `Latency từng bước`, `Token Usage`, `Final Answer`, `User Feedback`.
- **Phân bổ thời gian thực tế mẫu:**
  - `User Query Receive`: **30 ms**
  - `Query Rewriting (LLM)`: **300 ms**
  - `Hybrid / Vector Search`: **80 ms**
  - `Cross-Encoder Reranking`: **200 ms**
  - `LLM Generation`: **1.000 ms - 8.000 ms** *(Điểm nghẽn lớn nhất về thời gian)*

#### c. Security: ACL (Access Control List) & PII Masking
- **ACL (Kiểm soát quyền truy cập):** Bắt buộc phải lọc quyền **trước khi tìm kiếm (Pre-filtering)**.
  - *Ví dụ:* Nhân viên bộ phận HR chỉ được tìm tài liệu có metadata `department == "HR"`.
  - *Lưu ý an toàn:* Không bao giờ được phép retrieve toàn bộ dữ liệu công ty rồi mới nạp vào LLM để kiểm tra quyền, vì thông tin mật đã bị lộ vào context.
- **PII Masking (Ẩn thông tin định danh cá nhân):** Nhận diện và che các dữ liệu nhạy cảm (`Tên`, `SĐT`, `Email`, `CCCD/Passport`, `Địa chỉ`).
  - Có thể áp dụng linh hoạt: trước khi indexing, trước khi nạp vào LLM prompt, hoặc trước khi ghi log dữ liệu.

---

### 4. LOAD, COST & LATENCY MANAGEMENT (QUẢN LÝ TẢI, CHI PHÍ & ĐỘ TRỄ)

#### a. Thách thức trong môi trường Production
Một pipeline RAG cực kỳ phức tạp (Multi-query $\to$ Multi-source $\to$ Hybrid Retrieval $\to$ Reranking $\to$ Large LLM $\to$ Multi-guardrails) có thể đạt chất lượng cao, nhưng nếu mất **15 giây/request** và tốn **5 lượt gọi LLM** thì chi phí sẽ bùng nổ khi phục vụ 100.000 người dùng, đồng thời phá hỏng trải nghiệm người dùng (UX).

#### b. Giải pháp Dynamic Query Routing (Định tuyến truy vấn động)

```text
                   [Incoming User Query]
                             │
             [Phân loại độ khó của Query]
               /                       \
    (Câu hỏi đơn giản)              (Câu hỏi phức tạp / Đa bước)
           /                                 \
          ▼                                   ▼
[Lightweight Pipeline]               [Advanced Pipeline]
Vector Search ──► Small LLM          Rewrite ──► Multi-Query ──► Hybrid Search
(Phản hồi nhanh, chi phí thấp)       ──► Graph / Rerank ──► LLM ──► Guardrails
                                     (Độ chính xác sâu, chấp nhận latency cao)
```

---

## 🎯 5. TỔNG KẾT TOÀN BỘ KHÓA HỌC RAG (SUMMARY OF ALL 5 CHAPTERS)

| Chương | Tên chương | Trụ cột cốt lõi & Giá trị đạt được |
| :--- | :--- | :--- |
| **01** | **Foundation & Evolution** | Hiểu bản chất Dense Vector Space, Cosine Similarity, ANN (HNSW, IVF, PQ) và cơ chế Hybrid Search (BM25 + Vector). |
| **02** | **Offline Pipeline Ingestion** | Nắm vững chu trình 4 khâu: Extraction (OCR) $\to$ Chunking (Structure-aware) $\to$ Metadata Enrichment $\to$ Vector Indexing. |
| **03** | **Online Pipeline Retrieval** | Làm chủ luồng Runtime: Pre-retrieval (Rewrite, Multi-query) $\to$ Search & RRF Fusion $\to$ Cross-Encoder Rerank $\to$ Post-RAG Guardrails. |
| **04** | **GraphRAG & Advanced Architectures** | Triển khai Knowledge Graph (Triples, Multi-hop Traversal), SOTA Models (Microsoft GraphRAG, LightRAG, HippoRAG) & Agentic Self-Correction. |
| **05** | **Evaluation & Operationalization** | Làm chủ RAG Triad Metrics (Context Relevance, Faithfulness, Answer Relevance), Cây chẩn đoán lỗi Error Tree, ACL Security & Dynamic Query Routing. |

> 🎉 **Chúc mừng bạn đã hoàn thành toàn bộ Giáo trình RAG Toàn tập từ Nền tảng tới Production!**
