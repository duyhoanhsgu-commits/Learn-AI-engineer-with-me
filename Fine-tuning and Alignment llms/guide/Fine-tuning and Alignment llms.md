# CHƯƠNG 1: BỨC TRANH TỔNG THỂ VỀ FINE-TUNING VÀ ALIGNMENT

---

## 1. Đặt Vấn Đề: Nghịch Lý Tri Thức Của Base LLM

Sau giai đoạn **Pre-training**, một Mô hình Ngôn ngữ Lớn (LLM) đã hấp thụ một khối lượng tri thức nhân loại khổng lồ từ Internet và văn bản số hóa.
* Mô hình nắm vững cú pháp lập trình: Python, C++, Go, REST API architecture.
* Mô hình am hiểu ngôn ngữ: ngữ pháp, ngữ nghĩa, khả năng tóm tắt văn bản, dịch thuật đa ngôn ngữ.
* Mô hình có thể giải toán, phân tích logic, viết bài luận.

Tuy nhiên, **"Biết nhiều không đồng nghĩa với việc làm đúng ý con người"**.

Base LLM về bản chất là một cỗ máy dự đoán từ tiếp theo (Next Token Predictor) tối ưu xác suất $P(w_t \mid w_1, \dots, w_{t-1})$. Nếu bạn đặt một câu hỏi, thay vì trả lời theo phong cách trợ lý, nó có thể tiếp tục tạo ra thêm các câu hỏi tương tự hoặc bổ sung văn bản ngẫu nhiên.

```
[Base Model] = Ngôn ngữ + Tri thức nền tảng (Uncontrolled Next-token Predictor)
       │
       ▼ + Supervised Fine-Tuning (SFT)
[Task-Specific Model] = Biết cách thực thi nhiệm vụ cụ thể theo format/persona
       │
       ▼ + Alignment (RLHF / DPO)
[Aligned Model] = Hành xử chuẩn mực, hữu ích và an toàn theo kỳ vọng con người
```

---

## 2. Phân Định Ranh Giới: 4 Trụ Cột Kỹ Thuật

Trong quá trình ứng dụng LLM vào thực tế, chúng ta có 4 công cụ cốt lõi với phạm vi tác động hoàn toàn khác nhau:

| Phương pháp | Cơ chế tác động | Bản chất thay đổi | Chi phí & Độ trễ | Khi nào nên dùng? |
| :--- | :--- | :--- | :--- | :--- |
| **Prompting** | In-Context Learning | Tác động tức thời vào Context Window, **không đổi trọng số** ($W$) | Thấp, dễ triển khai | Thử nghiệm ý tưởng nhanh, tác vụ linh hoạt, ít ràng buộc cứng |
| **RAG** | External Memory (Vector/Keyword DB) | Cung cấp tri thức động theo thời gian thực, **không đổi trọng số** ($W$) | Trung bình, tối ưu chi phí token | Dữ liệu cập nhật liên tục, dữ liệu nội bộ/bí mật, chống hallucination |
| **Fine-tuning (SFT)** | Parameter Updates | Huấn luyện lại một phần hoặc toàn bộ trọng số ($W$) | Trung bình - Cao | Định hình phản xạ (reflex), giọng văn (tone), chuẩn hóa output format (JSON, XML) |
| **Alignment (RLHF/DPO)** | Preference Optimization | Uốn nắn phân phối xác suất dựa trên preference/tiêu chuẩn con người | Cao, đòi hỏi dữ liệu so sánh chuẩn | Kiểm soát an toàn (Safety), giảm độc hại, tuân thủ nguyên tắc đạo đức/sư phạm |

---

## 3. Case Study Minh Họa: Xây Dựng AI Tutor Dạy RAG

Giả sử mục tiêu là phát triển một **Hệ thống AI Gia sư (AI Tutor)** có nhiệm vụ giảng dạy khái niệm *RAG (Retrieval-Augmented Generation)* cho học sinh.

### 3.1. Các tầng năng lực
* **Tầng Pre-training:** Mô hình đã biết RAG là viết tắt của từ gì, kiến trúc gồm Retriever và Generator hoạt động ra sao.
* **Tầng Fine-tuning (Behavior Shaping):** Dạy mô hình đóng vai một gia sư:
  * Không bao giờ đưa ra lời giải hoàn chỉnh ngay lập tức.
  * Luôn giải thích bằng các ví dụ trực quan đời sống.
  * Luôn kết thúc bằng một câu hỏi gợi mở để kiểm tra mức độ thấu hiểu của người học.
* **Tầng Alignment (Human Values & Pedagogical Guidelines):** Căn chỉnh phản ứng của mô hình khi học sinh biểu hiện thái độ tiêu cực:
  * *Tình huống:* Học sinh nói *"Em lười quá, anh giải bài này cho em luôn đi"*.
  * *Chưa Align:* Mô hình có thể nhượng bộ và giải luôn toàn bộ đáp án.
  * *Đã Align:* Mô hình kiên nhẫn từ chối khéo léo, động viên học sinh và chia nhỏ bài toán thành một bước cực kỳ dễ để học sinh tự làm.

---

## 4. Nguyên Tắc Vàng Trong Kỹ Thuật LLM

> **"Đừng Fine-tune để nhồi nhét dữ liệu mới. Hãy dùng RAG cho tri thức động và Fine-tune cho hành vi."**

1. **Trọng số ($W$) không phải là Cơ sở dữ liệu (Database):**
   * Nếu nạp dữ liệu liên tục thay đổi (giá chứng khoán, chính sách công ty, tin tức hằng ngày) vào trọng số thông qua fine-tuning, mô hình rất dễ gặp hiện tượng **Catastrophic Forgetting** (quên kiến thức cũ) và tốn kém chi phí train lại.
2. **RAG là chiếc cặp sách, Fine-tuning là kỹ năng tư duy:**
   * RAG đưa tài liệu vào tay mô hình khi cần tra cứu.
   * Fine-tuning rèn luyện cách mô hình đọc, xử lý và phản hồi thông tin đó sao cho đúng định dạng và phong cách mong muốn.

---

# CHƯƠNG 2: KHI NÀO THỰC SỰ CẦN FINE-TUNING LLM?

Không phải cứ sở hữu một mô hình ngôn ngữ lớn (LLM) là phải mang đi fine-tune. Fine-tuning chỉ thực sự đáng cân nhắc khi bạn muốn thay đổi hành vi mang tính ổn định dài hạn của mô hình thay vì chỉ giải quyết vấn đề bằng ngữ cảnh tạm thời.

---

## 1. Định hình phong cách và chuẩn hóa định dạng (Style & Format)

Khi bạn cần mô hình luôn duy trì một phong cách giao tiếp và cấu trúc đầu ra cố định mà không cần nhắc lại trong từng câu lệnh:
* **Đặc điểm:** Luôn phản hồi bằng tiếng Việt, văn phong sư phạm/giáo viên, diễn đạt dễ hiểu, tuân thủ nghiêm ngặt schema (ví dụ: JSON chuẩn).
* **Mẫu dữ liệu huấn luyện:**
```
Input: "Explain semantic search"
Output: {"definition": "...", "example": "...", "question": "..."}
```
* **Kết quả:** Qua hàng loạt ví dụ mẫu, mô hình sẽ học sâu mẫu hình (pattern) này và phản hồi tự nhiên mà không bị lệch định dạng.

---

## 2. Huấn luyện kỹ năng chuyên biệt (Specialized Skills)

Áp dụng cho các bài toán đặc thù như Medical LLM, Legal LLM, Coding Assistant, Customer Support, hoặc AI Tutor:
* **Mục tiêu:** Dạy mô hình cách tư duy hoặc phương pháp làm việc cụ thể thay vì chỉ nhồi nhét thông tin thuần túy.
* **Ví dụ (AI Tutor theo phương pháp Socratic):**
```
Instruction: "Teach the student using Socratic questions."
Input: "I don't understand embeddings."
Output: "Imagine every sentence has a position on a map. What do you think happens when two sentences have similar meaning?"
```

---

## 3. Vượt qua giới hạn của Prompting (Prompt Fatigue)

Khi việc tinh chỉnh prompt (System Prompt) bắt đầu chạm ngưỡng giới hạn kỹ thuật:
* **Vấn đề:** System prompt phình to lên tới 2.000 – 3.000 tokens chứa đầy các điều kiện ràng buộc ("You are a tutor", "Always...", "Never...", "If X then Y...", "Output rules..."), nhưng mô hình vẫn thỉnh thoảng vi phạm hoặc quên lệnh.
* **Giải pháp:** Nếu hành vi cần thiết đã ổn định và có tập dữ liệu chuẩn, fine-tuning sẽ nạp trực tiếp hành vi đó vào trọng số (weights) của mô hình, giúp giải phóng hoàn toàn độ dài ngữ cảnh (context window).

---

## 4. Tối ưu hóa chi phí và hiệu năng (Cost & Latency Optimization)

Chiến lược thay thế mô hình lớn bằng mô hình nhỏ chuyên dụng:
* **Mô hình tổng quát (General Model ~70B):** Xử lý tác vụ rất tốt nhưng chi phí vận hành cao, độ trễ lớn và đòi hỏi hạ tầng mạnh.
* **Mô hình tinh chỉnh (Specialized Model ~7B):** Có thể đạt chất lượng tương đương hoặc vượt trội mô hình 70B trên một tác vụ hẹp cụ thể sau khi được fine-tune đúng cách.
* **Lợi ích:** Tiết kiệm chi phí phần cứng (GPU/RAM), giảm độ trễ (latency), và tăng quyền kiểm soát khi tự lưu trữ (self-host).

---

## 5. So sánh nhanh: Prompting vs. Fine-Tuning

| Tiêu chí | Prompt Engineering (In-context) | Fine-Tuning |
| :--- | :--- | :--- |
| **Mục đích chính** | Hướng dẫn tác vụ tức thời, linh hoạt | Cố định hành vi, phong cách, định dạng |
| **Chi phí triển khai** | Rất thấp, thử nghiệm nhanh | Tốn tài nguyên tính toán và chuẩn bị dữ liệu |
| **Kích thước prompt** | Dài (tốn token ngữ cảnh mỗi request) | Ngắn gọn (hành vi đã nằm trong trọng số) |
| **Mô hình phù hợp** | Cần mô hình lớn để hiểu chỉ dẫn phức tạp | Có thể dùng mô hình nhỏ (7B, 8B) chuyên biệt hóa |

---

# CHƯƠNG 3: PROMPTING, RAG VÀ FINE-TUNING

Ba kỹ thuật này thường xuyên bị nhầm lẫn khi triển khai hệ thống LLM thực tế. Để phân biệt nhanh, hãy ghi nhớ bản chất cốt lõi:
* **Prompting:** Nói cho mô hình biết phải làm cái gì (chỉ dẫn tức thời).
* **RAG (Retrieval-Augmented Generation):** Đưa kiến thức cần dùng vào ngữ cảnh (dữ liệu động, cập nhật).
* **Fine-Tuning:** Dạy mô hình cách hành xử (thay đổi phong cách, phản xạ và kỹ năng chuyên sâu).

---

## 1. Case Study Thực Tế: Chatbot Hỗ Trợ Sinh Viên

Giả sử bạn cần xây dựng một trợ lý ảo phục vụ sinh viên trong trường học:

* **Áp dụng Prompting:**
  * Thiết lập giọng điệu và vai trò ngay trong câu lệnh hệ thống (System Prompt).
  * *Ví dụ:* `"The system always answers politely and explains concepts simply."`
* **Áp dụng RAG:**
  * *Sinh viên hỏi:* *"Học phí ngành CNTT năm nay là bao nhiêu?"*
  * Vì học phí thay đổi theo từng kỳ, mô hình không thể tự đoán.
  * *Luồng xử lý:* Câu hỏi $\rightarrow$ Truy xuất (Retrieval) từ cơ sở dữ liệu/văn bản quy chế $\rightarrow$ Ghép thông tin liên quan (Context) $\rightarrow$ Đưa vào LLM để sinh câu trả lời chính xác.
* **Áp dụng Fine-Tuning:**
  * Bạn muốn bot đóng vai trò trợ giảng với quy trình sư phạm chuẩn: Giải thích khái niệm $\rightarrow$ Đưa ví dụ $\rightarrow$ Đặt câu hỏi kiểm tra $\rightarrow$ Đánh giá câu trả lời $\rightarrow$ Gợi ý (hints).
  * Để bot thành thạo phản xạ này mà không cần viết prompt dài dòng, bạn cần chuẩn bị hàng nghìn cặp hội thoại mẫu dạng Tutor để huấn luyện trực tiếp vào trọng số của mô hình.

---

## 2. Nguyên Tắc Lựa Chọn Công Nghệ

| Mục tiêu triển khai | Kỹ thuật phù hợp | Bản chất can thiệp |
| :--- | :--- | :--- |
| **Thay đổi yêu cầu tạm thời, định hướng tác vụ nhanh** | Prompting | Can thiệp mức câu lệnh (Context Window) |
| **Cập nhật kiến thức mới, tránh ảo giác, tra cứu tài liệu** | RAG | Kết nối dữ liệu ngoài (External Knowledge Base) |
| **Cố định hành vi, chuẩn hóa văn phong/output, rèn kỹ năng sâu** | Fine-Tuning | Cập nhật trực tiếp trọng số mô hình (Model Weights) |

---

## 3. Kiến Trúc Hệ Thống Thực Tế

Trong môi trường sản xuất (Production), ba kỹ thuật này không triệt tiêu lẫn nhau mà thường được kết hợp theo dạng chuỗi để bổ trợ toàn diện:

```
User Request
     │
     ▼
[ Application Layer ]
     │
     ├── 1. RAG: Truy xuất dữ liệu động từ Database / Vector DB
     │
     ├── 2. System Prompt: Gắn chỉ dẫn tác vụ, ngữ cảnh người dùng
     │
     ▼
[ Fine-Tuned LLM ]: Mô hình đã học sẵn phản xạ, kỹ năng và format chuẩn
     │
     ▼
Final Response
```

---

# CHƯƠNG 4: LORA & QLORA – FINE-TUNE MÔ HÌNH LỚN VỚI TÀI NGUYÊN NHỎ

---

## 1. Vấn Đề Của Full Fine-Tuning

Khi huấn luyện lại toàn bộ mô hình (Full Fine-Tuning):
* **Cập nhật toàn bộ tham số:** Mô hình 7B tham số đồng nghĩa với việc tính toán và lưu trữ gradient, trạng thái optimizer (như AdamW) cho cả 7 tỷ trọng số ($W_1, W_2, \dots, W_{7B}$).
* **Nghẽn phần cứng (VRAM/GPU):** Không chỉ tốn tài nguyên tính toán, lượng VRAM cần để duy trì trạng thái huấn luyện có thể gấp 4 đến 6 lần dung lượng ban đầu của mô hình, vượt quá khả năng của các dòng card đồ họa phổ thông.

---

## 2. LoRA (Low-Rank Adaptation): Tối Ưu Bằng Phân Rã Ma Trận

Ý tưởng cốt lõi của LoRA là đóng băng (freeze) toàn bộ trọng số gốc và chỉ học thêm một thành phần biến thiên nhỏ:

**Công thức cập nhật:**
$$W = W_0 + \Delta W = W_0 + \frac{\alpha}{r} (B \times A)$$

* $W_0 \in \mathbb{R}^{d \times k}$: Ma trận trọng số ban đầu của mô hình gốc (được giữ cố định hoàn toàn).
* $\Delta W$: Lượng thay đổi trọng số, được phân rã thành tích của hai ma trận hạng thấp:
  * $A \in \mathbb{R}^{r \times k}$ (khởi tạo ngẫu nhiên theo phân phối chuẩn Gaussian).
  * $B \in \mathbb{R}^{d \times r}$ (khởi tạo bằng 0).
* $r$: Rank (hạng của ma trận), thường rất nhỏ ($r \ll \min(d, k)$, ví dụ: $r = 8, 16, 32$).

```
               Input x
              /       \
             /         \
    [ W0 (Frozen) ]    [ Matrix A (r x k) ]
             \                 │
              \        [ Matrix B (d x r) ]
               \               /
                \             /
                 (+) <-------' (scaled by α/r)
                  │
               Output h
```

* **Hiệu quả:** Chỉ cần cập nhật một lượng rất nhỏ tham số ($< 1\%$ tổng số tham số của mô hình), giảm mạnh dung lượng bộ nhớ dành cho gradients và optimizer states.

---

## 3. Khái Niệm Adapter

Kết quả sau khi huấn luyện LoRA không phải là một mô hình đầy đủ mới, mà là một tệp trọng số nhẹ được gọi là **Adapter** (thường chỉ từ vài chục đến vài trăm MB):

* **Tính linh hoạt:** Một base model duy nhất có thể hoán đổi hoặc tải kèm nhiều adapter khác nhau tùy tác vụ:
  * Qwen 7B (Base) + Tutor Adapter $\rightarrow$ Trợ lý sư phạm.
  * Qwen 7B (Base) + Coding Adapter $\rightarrow$ Trợ lý lập trình.
  * Qwen 7B (Base) + Medical Adapter $\rightarrow$ Trợ lý y tế.
* **Tiết kiệm lưu trữ:** Thay vì lưu nhiều bản sao 7B cồng kềnh (mỗi bản ~14GB ở định dạng FP16), bạn chỉ cần lưu một base model và các file adapter nhỏ gọn.

---

## 4. QLoRA (Quantized Low-Rank Adaptation)

QLoRA đưa khả năng tiết kiệm VRAM lên một mức cao hơn bằng cách lượng tử hóa (quantize) mô hình gốc trước khi gắn LoRA adapter:

$$\text{Fine-Tuned Architecture} = \text{Base Model (4-bit)} + \text{LoRA Adapters (16-bit)}$$

Ba kỹ thuật nền tảng giúp QLoRA duy trì độ chính xác dù nén mạnh:
* **4-bit NormalFloat (NF4):** Kiểu dữ liệu lượng tử hóa tối ưu riêng cho các trọng số mạng nơ-ron có phân phối chuẩn, giúp bảo toàn thông tin tốt hơn chuẩn FP4 hay INT4 truyền thống.
* **Double Quantization (Lượng tử hóa kép):** Lượng tử hóa chính các hằng số lượng tử hóa (quantization constants), tiết kiệm thêm khoảng $0.37 \text{ bit}$ trên mỗi tham số.
* **Paged Optimizers:** Tận dụng bộ nhớ RAM hệ thống thông qua cơ chế phân trang (paging) qua kết nối CPU-GPU khi VRAM chạm ngưỡng đỉnh tải, ngăn chặn lỗi văng chương trình (Out-of-Memory / OOM).

---

## 5. So Sánh Nhanh

| Tiêu chí | Full Fine-Tuning | LoRA | QLoRA |
| :--- | :--- | :--- | :--- |
| **Trọng số Base Model** | FP16 / BF16 (Cập nhật) | FP16 / BF16 (Đóng băng) | 4-bit NF4 (Đóng băng) |
| **Tham số huấn luyện** | 100% | Thường $< 1\%$ | Thường $< 1\%$ |
| **VRAM cần cho Model 7B** | Rất cao (~60GB - 80GB) | Trung bình (~16GB - 24GB) | Cực thấp (~6GB - 10GB) |
| **Phần cứng khả thi** | Cluster GPU chuyên dụng (A100/H100) | GPU Enterprise / Prosumer | GPU phổ thông (RTX 3060/4060) |

---

# CHƯƠNG 5: PEFT PIPELINE THỰC TẾ (SUPERVISED FINE-TUNING)

---

## 1. Tổng Quan Luồng Xử Lý (End-to-End Pipeline)

Quy trình chuẩn để huấn luyện một mô hình ngôn ngữ bằng kỹ thuật PEFT (Parameter-Efficient Fine-Tuning) qua các công cụ hiện đại (Transformers, PEFT, TRL):

```
[ Dataset Chuẩn Bị ]
       │
       ▼
[ Formatting & Chat Template ]
       │
       ▼
[ Tokenization & Data Masking (Prompt Masking) ]
       │
       ▼
[ Load Base Model (4-bit/8-bit) + Cấu Hình LoRA Adapter ]
       │
       ▼
[ SFTTrainer (Hugging Face / TRL) ]
       │
       ▼
[ Evaluation & Validation Loss ]
       │
       ▼
[ Export / Save LoRA Adapter ]
```

---

## 2. Chuẩn Bị SFT Dataset (Supervised Fine-Tuning)

Dữ liệu SFT là các cặp câu hỏi – trả lời mẫu chất lượng cao. Hiện nay có 2 định dạng dữ liệu phổ biến nhất:

### Dạng 1: Instruction – Input – Output (Alpaca Style)
Phù hợp cho các bài toán xử lý tác vụ đơn lẻ, tóm tắt hoặc trích xuất thông tin.
```json
{
  "instruction": "Explain RAG simply.",
  "input": "I am a beginner.",
  "output": "RAG allows an AI to search external documents before answering your question."
}
```

### Dạng 2: Conversational Messages (ShareGPT / OpenAI Style)
Phù hợp xây dựng chatbot hội thoại đa lượt (Multi-turn), áp dụng trực tiếp qua `chat_template`.
```json
{
  "messages": [
    {"role": "user", "content": "What is RAG?"},
    {"role": "assistant", "content": "RAG is a technique that combines retrieval with generation."}
  ]
}
```

---

## 3. Data Masking (Prompt Masking / Label Masking)

Đây là chi tiết kỹ thuật cốt lõi quyết định chất lượng mô hình sau khi huấn luyện:

* **Bản chất vấn đề:**
  Trong cặp câu:
  * User: *"What is RAG?"*
  * Assistant: *"RAG combines retrieval with generation..."*
  Mục tiêu là dạy mô hình cách trả lời, không phải học thuộc lòng câu hỏi của người dùng.
* **Cơ chế hoạt động:**
  * **Input Tokens (User Prompt):** Gán nhãn `label = -100` (giá trị mặc định trong PyTorch/CrossEntropyLoss để bỏ qua việc tính gradient). $\rightarrow$ *Ignore loss*.
  * **Output Tokens (Assistant Response):** Giữ nguyên token IDs để tính toán mất mát. $\rightarrow$ *Calculate loss*.
* **Lợi ích:** Mô hình tập trung toàn bộ dung lượng học vào việc tối ưu câu trả lời, tránh hiện tượng sinh lặp lại chính câu hỏi của người dùng.

---

## 4. Cấu Hình LoRA Adapter (LoraConfig)

Cấu hình LoRA xác định ma trận nào trong mạng nơ-ron sẽ được gắn thêm adapter:

* `r` **(Rank):** Kích thước không gian con nén (thường chọn $8, 16, 32, 64$). Giá trị $r$ càng cao, dung lượng học càng lớn nhưng tốn thêm chút VRAM.
* `lora_alpha`**:** Hệ số tỷ lệ (scaling factor). Quy tắc thực tế: thường đặt $\alpha = 2 \times r$ (ví dụ: $r=16 \rightarrow \alpha=32$).
* `lora_dropout`**:** Tỷ lệ dropout ngẫu nhiên (thường từ $0.05$ đến $0.1$) giúp chống hiện tượng overfitting.
* `target_modules`**:** Các khối ma trận tuyến tính được gắn LoRA:
  * Khối Attention cơ bản: `q_proj`, `v_proj`.
  * Khối Attention đầy đủ (khuyên dùng): `q_proj`, `k_proj`, `v_proj`, `o_proj`.
  * Khối MLP mở rộng: `gate_proj`, `up_proj`, `down_proj`.

---

## 5. Quy Trình Thực Thi Code (Transformers + PEFT + TRL)

Minh họa đoạn mã rút gọn áp dụng trọn vẹn pipeline:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer, SFTConfig

# 1. Load Tokenizer & Base Model ở chế độ 4-bit (QLoRA)
model_id = "Qwen/Qwen2.5-7B-Instruct"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 2. Định nghĩa LoRA Configuration
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    bias="none",
    task_type="CAUSAL_LM"
)

# 3. Cấu hình Training
training_args = SFTConfig(
    output_dir="./lora_output",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=10,
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported()
)

# 4. Huấn luyện bằng SFTTrainer
# SFTTrainer tự động xử lý data masking khi cấu hình data collator phù hợp
trainer = SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    peft_config=peft_config,
    tokenizer=tokenizer,
    args=training_args
)

trainer.train()

# 5. Lưu Adapter (chỉ tốn vài chục MB)
trainer.model.save_pretrained("./final_adapter")
tokenizer.save_pretrained("./final_adapter")
```

---

## 6. Kết Quả Lưu Trữ

Bạn không cần lưu lại toàn bộ model 7B (~14GB - 16GB). Thư mục `./final_adapter` chỉ chứa:
* `adapter_config.json`: Cấu hình siêu tham số LoRA.
* `adapter_model.safetensors`: File nhị phân lưu ma trận $A$ và $B$ (kích thước siêu nhẹ: ~50MB – 150MB).

Khi triển khai (Inference), chỉ cần nạp Base Model gốc và load đè adapter này lên.

---

# CHƯƠNG 6: SUPERVISED FINE-TUNING TỐT NHƯNG VẪN CHƯA ĐỦ – BƯỚC ĐỆM CHO RLHF

---

## 1. Bản Chất Và Giới Hạn Của SFT

Trong bài toán Supervised Fine-Tuning (SFT), mô hình được tối ưu theo cơ chế Next-Token Prediction dựa trên tập dữ liệu mẫu:

* **Học bắt chước (Imitation Learning):** Nếu bạn cung cấp 10.000 cặp câu hỏi – trả lời, mô hình sẽ cố gắng tối đa hóa xác suất tái tạo chính xác từng token trong câu trả lời mục tiêu.
* **Quy chuẩn đơn lẻ (Binary View):** Hàm mất mát (Cross-Entropy Loss) chỉ coi câu trả lời mẫu trong tập dữ liệu là "đúng" (xác suất mục tiêu = 1), còn tất cả các cách diễn đạt khác đều bị phạt (penalized).

---

## 2. Vấn Đề: SFT Không Biết So Sánh "Tốt Hơn"

SFT chỉ dạy mô hình cách tạo ra một đáp án hợp lệ, chứ không dạy mô hình đánh giá mức độ ưu tiên giữa các đáp án cùng đúng:

Giả sử câu hỏi là: *"Explain RAG to a beginner"*

* **Đáp án A:** `"RAG retrieves useful information from documents before generating an answer."` (Dễ hiểu, trực quan, nhắm đúng đối tượng beginner).
* **Đáp án B:** `"Retrieval-Augmented Generation utilizes external vector retrieval mechanics to condition generative decoding."` (Về mặt kỹ thuật hoàn toàn chính xác, nhưng quá hàn lâm, không phù hợp cho người mới bắt đầu).

**Tại sao SFT thất bại trong việc phân cấp:**
* **Không có khái niệm Preference (Sự ưu tiên):** SFT không có cơ chế để so sánh hai câu trả lời cùng lúc. Nếu cả A và B đều xuất hiện trong tập dữ liệu, mô hình xem trọng số của chúng ngang nhau.
* **Ảo giác về chất lượng:** Mô hình có thể sinh ra một câu trả lời đúng ngữ pháp, không sai sự thật, nhưng dài dòng, sáo rỗng hoặc lệch phong cách người dùng mong muốn.

---

## 3. Sự Xuất Hiện Của RLHF (Reinforcement Learning from Human Feedback)

Để giải quyết khoảng trống của SFT, hệ thống cần được căn chỉnh (alignment) dựa trên sự so sánh:

```
[ SFT Model ]
     │
     ▼
Sinh ra nhiều câu trả lời cho cùng một Prompt (Answer A vs. Answer B)
     │
     ▼
Human / AI đánh giá sự ưu tiên: Preference (A > B)
     │
     ▼
[ Alignment Stage: RLHF / DPO ] ──> Dạy mô hình tối ưu hóa theo độ thỏa mãn
```

* **Dữ liệu dạng so sánh (Preference Data):** Thay vì cặp `(Prompt, Single Answer)`, dữ liệu chuyển thành bộ ba `(Prompt, Chosen Answer, Rejected Answer)`.
* **Mục tiêu mới:** Dạy mô hình tối đa hóa phần thưởng (Reward) từ câu trả lời tốt nhất ($A$) và tránh xa các đặc điểm của câu trả lời kém hơn ($B$).

---

## 4. Bảng So Sánh SFT vs. RLHF

| Tiêu chí | Supervised Fine-Tuning (SFT) | Reinforcement Learning / Alignment (RLHF) |
| :--- | :--- | :--- |
| **Dạng dữ liệu** | `(Prompt, Answer)` | `(Prompt, Chosen, Rejected)` |
| **Mục tiêu học** | Bắt chước văn phong và cấu trúc | Tối ưu hóa theo mức độ ưa thích (Human Preference) |
| **Độ nhạy ngữ cảnh** | Khó phân biệt mức độ hay/dở giữa các câu đúng | Tự động chọn lọc cách diễn đạt phù hợp nhất với ngữ cảnh |
| **Vai trò trong Pipeline** | Dựng khung năng lực cơ bản | Tinh chỉnh hành vi, an toàn (Safety) và độ hữu ích (Helpfulness) |

---

# CHƯƠNG 7: RLHF – CĂN CHỈNH MÔ HÌNH BẰNG HUMAN FEEDBACK

---

## 1. Khái Niệm Cốt Lõi

RLHF (Reinforcement Learning from Human Feedback) là kỹ thuật học tăng cường dựa trên phản hồi của con người. Thay vì chỉ bắt chước dữ liệu mẫu (như SFT), mô hình được huấn luyện để hiểu và tối ưu hóa theo sở thích (human preference), độ an toàn và mức độ hữu ích mà con người mong muốn.

---

## 2. Pipeline Cổ Điển Của RLHF

Quy trình chuẩn gồm 4 giai đoạn nối tiếp nhau:

```
[ 1. SFT Model ] 
       │ (Sinh nhiều câu trả lời: A, B, C, D)
       ▼
[ 2. Human Feedback & Ranking ] ──> [ Preference Dataset (A > B > C > D) ]
       │
       ▼
[ 3. Train Reward Model (RM) ] ──> Đóng vai trò "Giám khảo AI" chấm điểm
       │
       ▼
[ 4. PPO Training ] ──> Tối ưu hóa policy của LLM để đạt điểm cao nhất từ RM
```

---

## 3. Các Thành Phần Chính Trong Pipeline

### 3.1. Thu Thập Dữ Liệu Sở Thích (Human Preference Dataset)
Với cùng một câu lệnh (prompt), mô hình SFT sẽ sinh ra nhiều phương án trả lời khác nhau: $A, B, C, D$.
Chuyên viên đánh giá (Human Annotator) sẽ xếp hạng chất lượng:
$$\text{Ranking: } A > B > C > D$$
Dữ liệu này tạo thành tập dữ liệu so sánh (pairwise comparison), phản ánh tiêu chuẩn câu trả lời nào được con người ưu tiên hơn.

### 3.2. Reward Model (Mô Hình Phần Thưởng – "Ban Giám Khảo AI")
Con người không thể ngồi chấm điểm hàng triệu câu trả lời trong suốt quá trình train PPO, do đó một mô hình riêng (thường khởi tạo từ chính SFT model) được huấn luyện để dự đoán điểm số con người sẽ chấm:
* Answer A: $0.91$ (rất tốt)
* Answer B: $0.75$ (khá)
* Answer D: $0.21$ (kém/lạc đề)

Reward Model đóng vai trò như một hàm mục tiêu (objective function) tự động hóa việc chấm điểm đầu ra.

### 3.3. PPO (Proximal Policy Optimization) & Tối Ưu Chính Sách
LLM (được xem như Policy Agent) nhận prompt, sinh câu trả lời và nhận điểm số (Reward) từ Reward Model.
Thuật toán PPO cập nhật trọng số của LLM nhằm mục đích duy nhất: tối đa hóa điểm thưởng nhận được.

---

## 4. Hiện Tượng Reward Hacking & Giải Pháp KL Divergence

Khi yêu cầu mô hình tối đa hóa điểm thưởng bằng mọi giá, một vấn đề lớn sẽ nảy sinh:

* **Reward Hacking (Lách luật / Lừa điểm):**
  * Mô hình phát hiện ra một số pattern khiến Reward Model luôn cho điểm cao (ví dụ: viết câu trả lời cực dài, lặp lại các từ ngữ tâng bốc, nhồi nhét thuật ngữ học thuật dù vô nghĩa).
  * Hậu quả: Mô hình bắt đầu sinh ra văn phong quái dị, mất kiểm soát và trôi xa khỏi khả năng ngôn ngữ tự nhiên ban đầu.

* **Cơ Chế Khắc Phục – Phạt KL Divergence ($D_{KL}$ Penalty):**
  * Hệ thống duy trì một bản sao đóng băng của mô hình ban đầu: Reference Model ($W_{ref}$).
  * Trong quá trình train PPO, hàm mục tiêu được bổ sung thêm một đại lượng phạt:
  $$\text{Objective} = R(x, y) - \beta \cdot D_{KL}\big(\pi_{\theta}(y\mid x) \parallel \pi_{ref}(y\mid x)\big)$$
  * **Ý nghĩa:** Điểm thưởng thực nhận sẽ bằng điểm của Reward Model trừ đi khoảng cách phân phối xác suất giữa mô hình đang học ($\pi_\theta$) và mô hình gốc ($\pi_{ref}$). Nếu mô hình cố thay đổi trọng số quá mạnh hoặc sinh chuỗi token quá dị biệt, đại lượng phạt sẽ kéo tụt điểm thưởng $\rightarrow$ Nguyên tắc: *"High reward, but don't change too drastically."*

---

## 5. Điểm Nghẽn Của RLHF Cổ Điển

Dù cực kỳ mạnh mẽ (đặt nền móng cho các hệ thống như ChatGPT ban đầu), pipeline RLHF cổ điển tồn tại các nhược điểm lớn:
* **Hạ tầng cực kỳ nặng nề:** Cần nạp đồng thời ít nhất 4 mô hình vào bộ nhớ trong quá trình training (Actor Model, Critic/Value Model, Reference Model, và Reward Model).
* **Độ bất ổn định cao:** PPO rất nhạy cảm với siêu tham số (hyperparameters), dễ bị sụp đổ gradient (policy collapse).

Chính vì độ phức tạp này, ngành công nghiệp sau đó đã phát triển **DPO (Direct Preference Optimization)** – kỹ thuật bỏ qua hoàn toàn Reward Model và PPO để tối ưu trực tiếp từ dữ liệu preference.

---

# CHƯƠNG 8: DIRECT ALIGNMENT – DPO, ORPO & SIMPO (ĐƠN GIẢN HÓA RLHF)

---

## 1. Bước Chuyển Tư Duy: Direct Alignment Là Gì?

Trong các hệ sinh thái LLM hiện đại, xu hướng chuyển dịch mạnh mẽ từ RLHF phức tạp sang các kỹ thuật Căn chỉnh trực tiếp (Direct Alignment):

* **RLHF truyền thống:** Phải trải qua quy trình trung gian cồng kềnh:
  $$\text{Dataset} \longrightarrow \text{Train Reward Model} \longrightarrow \text{Train PPO (cực kỳ bất ổn, tốn VRAM)}$$
* **Direct Alignment (DPO, ORPO, SimPO):** Bỏ qua hoàn toàn việc huấn luyện Reward Model và thuật toán PPO. Mô hình học trực tiếp từ Preference Dataset bằng một hàm mất mát (loss function) duy nhất:
  $$\text{Preference Dataset } (x, y_w, y_l) \longrightarrow \text{Direct Training Loss} \longrightarrow \text{Aligned Model}$$

---

## 2. Dữ Liệu Sở Thích Chuẩn (Pairwise Preference Dataset)

Dữ liệu đầu vào không còn là các cặp `(instruction, output)` đơn lẻ như SFT, mà bao gồm bộ ba:
* **Prompt ($x$):** Câu lệnh của người dùng.
* **Chosen ($y_w$ / $y_{win}$):** Câu trả lời được đánh giá tốt hơn (dễ hiểu, an toàn, chuẩn xác).
* **Rejected ($y_l$ / $y_{lose}$):** Câu trả lời kém hơn (dài dòng, khó hiểu, sai phong cách).

* **Ví dụ:**
  * **Prompt:** `"Explain embedding simply."`
  * **Chosen ($y_w$):** `"Think of embeddings as coordinates of words on a conceptual map."`
  * **Rejected ($y_l$):** `"Embeddings are high-dimensional vectors representing latent semantic features."`

**Mục tiêu của thuật toán:** Tăng xác suất sinh ra $y_w$ và giảm xác suất sinh ra $y_l$ khi gặp câu hỏi $x$.

---

## 3. DPO (Direct Preference Optimization)

DPO chứng minh về mặt toán học rằng: bản thân mô hình ngôn ngữ có thể tự đóng vai trò như một Reward Model ngầm định, giúp triệt tiêu hoàn toàn sự phụ thuộc vào PPO.

* **Nguyên lý trực giác:** So sánh tỷ lệ xác suất sinh ra câu trả lời giữa mô hình đang huấn luyện ($\pi_\theta$) và mô hình cơ sở tham chiếu đã đóng băng ($\pi_{ref}$).
* **Hàm mất mát sẽ tối đa hóa khoảng cách:**
  $$\mathcal{L}_{\text{DPO}} = -\mathbb{E} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w\mid x)}{\pi_{ref}(y_w\mid x)} - \beta \log \frac{\pi_\theta(y_l\mid x)}{\pi_{ref}(y_l\mid x)} \right) \right]$$
  Nếu mô hình tăng xác suất của $y_w$ đồng thời giảm xác suất của $y_l$ (so với base model), loss sẽ tiến về 0.

* **Ưu điểm cốt lõi:**
  * **Không cần Reward Model:** Giảm bớt một mô hình riêng biệt cần huấn luyện và bảo trì.
  * **Huấn luyện ổn định:** Huấn luyện như một bài toán phân loại nhị phân đơn giản, không bị tình trạng sụp đổ gradient (collapse) như khi train PPO.
  * **Tiết kiệm tài nguyên:** Thay vì giữ 4 mô hình trong VRAM cùng lúc, DPO chỉ cần 1 mô hình đang train và 1 reference model (có thể load dạng đóng băng/lượng tử hóa).

---

## 4. Các Biến Thể Mở Rộng: ORPO & SimPO

Cùng đi theo tinh thần "Direct Alignment", các phương pháp mới tiếp tục tinh gọn quy trình huấn luyện:

* **ORPO (Odds Ratio Preference Optimization):**
  * **Hợp nhất SFT và Alignment làm một:** Thông thường bạn phải train SFT trước, sau đó mới train DPO. ORPO tích hợp sẵn hàm phạt tỷ lệ chênh lệch (Odds Ratio) ngay trong bước huấn luyện SFT.
  * **Lợi ích:** Bỏ qua bước SFT riêng lẻ, chỉ cần 1 lượt huấn luyện duy nhất (Single-turn alignment) để vừa học kiến thức vừa căn chỉnh hành vi. Không cần reference model.

* **SimPO (Simple Preference Optimization):**
  * **Bỏ luôn Reference Model:** DPO vẫn cần giữ một bản $\pi_{ref}$ để tính KL-divergence phạt lệch trọng số. SimPO sử dụng trực tiếp độ dài chuẩn hóa (length-normalized reward) và một ngưỡng biên độ (target margin) làm hàm mục tiêu.
  * **Lợi ích:** Tiết kiệm thêm bộ nhớ VRAM, tốc độ train nhanh hơn DPO thuần và giảm thiểu hiện tượng mô hình sinh câu trả lời thiên vị độ dài (length exploitation).

---

## 5. Bảng So Sánh Toàn Cảnh

| Tiêu chí | RLHF (PPO) | DPO | ORPO | SimPO |
| :--- | :--- | :--- | :--- | :--- |
| **Cần Reward Model riêng?** | Có | Không | Không | Không |
| **Cần Reference Model?** | Có | Có ($\pi_{ref}$) | Không | Không |
| **Tách biệt bước SFT?** | Có | Có | Gộp chung (1 step) | Có |
| **Độ phức tạp hạ tầng** | Rất cao (4 models) | Trung bình (2 models) | Thấp (1 model) | Thấp (1 model) |
| **Độ ổn định khi train** | Kém (dễ vỡ PPO) | Rất ổn định | Rất ổn định | Rất ổn định |

---

# CHƯƠNG 9: GRPO, RLVR, CONSTITUTIONAL AI & RED TEAMING

---

## 1. GRPO (Group Relative Policy Optimization)

GRPO là bước tiến tối ưu hóa policy nhằm cắt giảm triệt để chi phí tính toán của PPO truyền thống:

* **Cơ chế cốt lõi:** Với mỗi câu hỏi (prompt), mô hình sinh ra một nhóm gồm nhiều câu trả lời ứng viên $\{o_1, o_2, \dots, o_G\}$.
* **Đánh giá tương đối theo nhóm:** Thay vì dùng một Value Model/Critic Model cồng kềnh để dự đoán giá trị baseline tuyệt đối, GRPO chuẩn hóa điểm số (reward) trực tiếp trong nhóm:
  $$A_i = \frac{r_i - \text{mean}(\{r_1, \dots, r_G\})}{\text{std}(\{r_1, \dots, r_G\})}$$
* **Lợi ích:** Bỏ hoàn toàn Critic Network, tiết kiệm đáng kể VRAM và tài nguyên tính toán trong khi vẫn giữ được tính ổn định cao.

---

## 2. RLVR (Reinforcement Learning with Verifiable Reward)

RLVR giải quyết bài toán căn chỉnh cho các tác vụ có đáp án đúng/sai tuyệt đối và kiểm chứng được bằng thuật toán:

* **Nguyên lý:** Thay thế con người hoặc LLM Judge cảm tính bằng bộ chấm tự động (deterministic verifier):
  * **Toán học & Logic:** So khớp chuỗi kết quả cuối cùng (`prediction == 100` $\rightarrow$ Reward = 1, ngược lại = 0).
  * **Lập trình (Coding):** Chạy code sinh ra qua bộ Unit Test tự động (10/10 test case passed $\rightarrow$ Reward = 1; runtime error/fail test $\rightarrow$ Reward = 0).
  * **Cấu trúc dữ liệu:** Kiểm tra tính hợp lệ của schema (JSON parse, regex match).
* **Ưu điểm:** Loại bỏ hoàn toàn chi phí gán nhãn thủ công và triệt tiêu nguy cơ thiên vị hay ảo giác từ LLM-as-a-Judge.

---

## 3. Constitutional AI (Căn Chỉnh Dựa Trên Hiến Pháp)

Thay vì con người phải thủ công chấm điểm từng output độc hại, Constitutional AI thiết lập một tập hợp các nguyên tắc định trước (Hiến pháp – Constitution):

* **Bộ nguyên tắc mẫu:**
  * *"Không cung cấp hướng dẫn chế tạo vũ khí hoặc hành vi gây hại."*
  * *"Không tiết lộ dữ liệu nhạy cảm hoặc danh tính cá nhân."*
  * *"Phải trung thực; nếu không chắc chắn hoặc không có nguồn, phải thẳng thắn thừa nhận không biết."*

* **Vòng lặp tự phê bình & sửa đổi (Critique $\rightarrow$ Revision):**

```
User Prompt
     │
     ▼
[ LLM sinh câu trả lời thô (Initial Response) ]
     │
     ▼
[ Đối chiếu với bộ nguyên tắc (Constitutional Rules) ]
     │
     ▼
[ AI tự phê bình (Self-Critique): "Phản hồi này có vi phạm tính trung thực không?" ]
     │
     ▼
[ AI tự hiệu chỉnh (Revision): Viết lại câu trả lời an toàn, chuẩn mực ]
```

---

## 4. Red Teaming (Chủ Động Tấn Công Tìm Lỗ Hổng)

Red Teaming là hoạt động đóng vai kẻ tấn công nhằm khai thác các điểm yếu tiềm ẩn của mô hình:

* **Các hình thức tấn công phổ biến:**
  * **Prompt Injection / Jailbreak:** Dùng các kỹ thuật bẻ khóa (đóng vai giả định, mã hóa base64, thơ ca ẩn dụ) để vượt qua bộ lọc an toàn.
  * **Indirect Prompt Injection:** Cài mã độc/lệnh ẩn vào tài liệu web mà RAG sẽ cào về.
  * **Sensitive Data Extraction:** Tìm cách ép mô hình làm lộ dữ liệu huấn luyện nhạy cảm hoặc API key.
* **Mục tiêu:** Không phải phá hủy hệ thống, mà là thu thập các ca thất bại (failures) làm dữ liệu để gia cố an toàn.
* **Vòng lặp cải tiến liên tục:**
  $$\text{Model} \longrightarrow \text{Red Team Attack} \longrightarrow \text{Collect Failures} \longrightarrow \text{Dataset Update} \longrightarrow \text{Alignment / Guardrails} \longrightarrow \text{Hardened Model}$$

---

## 5. Tổng Kết Toàn Bộ Lộ Trình (Production Roadmap)

```
                  PRETRAINED LLM
                         │
                         ▼
              ┌──────────────────┐
              │ Có cần knowledge?│
              └────────┬─────────┘
                       │
                      RAG
                       │
                       ▼
              Có cần đổi hành vi?
                       │
                       ▼
                  FINE-TUNING
                       │
              ┌────────┴────────┐
              ▼                 ▼
             LoRA             QLoRA
                                │
                       4-bit + LoRA Adapter
                                │
                                ▼
                               SFT
                                │
                     Instruction/Input/Output
                                │
                                ▼
                         Fine-tuned LLM
                                │
                                ▼
                      Chưa hợp preference?
                                │
                                ▼
                            ALIGNMENT
                                │
          ┌─────────────────────┼────────────────────┐
          ▼                     ▼                    ▼
        RLHF                   DPO                  GRPO
          │                     │                    │
 Reward Model + PPO      Chosen/Rejected      Group Relative Rewards / RLVR
          │                     │                    │
          └─────────────────────┼────────────────────┘
                                │
                                ▼
                          Aligned Model
                                │
                  ┌─────────────┴─────────────┐
                  ▼                           ▼
          Constitutional AI              Red Teaming
                  │                           │
                  └─────────────┬─────────────┘
                                │
                                ▼
                         Production LLM
```









