# 🎯 I. Xác định bài toán (Problem Discovery)

Tài liệu hướng dẫn tư duy tiếp cận, phương pháp luận Double Diamond, Human-Centered Design và cấu trúc chuẩn của một Problem Statement trong việc thiết kế giải pháp AI.

---

## 1. Tư duy tiếp cận bài toán AI

### Đừng bắt đầu bằng việc lựa chọn công nghệ:
- **Tránh đặt câu hỏi:** Dùng LLM nào? Có cần Agent không? Dùng LangGraph hay LangChain?
- **Hãy bắt đầu bằng:** Người dùng đang gặp vấn đề gì và AI có thực sự cần thiết không?

---

## 2. Mô hình Double Diamond trong thiết kế giải pháp AI

```
          [ Diamond 1: Vấn đề ]              [ Diamond 2: Giải pháp ]
       Discover  ───>   Define           Develop    ───>   Deliver
      (Mở rộng)        (Thu hẹp)        (Mở rộng)         (Thu hẹp)
```

### Diamond 1: Discover & Define (Khám phá & Xác định vấn đề)

- **Discover (Khám phá):**
  - Quan sát người dùng, phỏng vấn, thu thập pain points.
  - Phân tích workflow hiện tại để tìm bottleneck (điểm nghẽn).
  - Nhận diện các tác vụ tốn nhiều thời gian hoặc dễ mắc sai sót.

- **Define (Xác định):**
  - Thu hẹp thông tin thành một Problem Statement rõ ràng.
  - **Ví dụ đúng:** *"Tutor phải đọc hàng trăm câu trả lời của học sinh mỗi ngày nên thời gian chấm bài quá lâu."*
  - **Ví dụ sai:** *"Tôi muốn xây một AI chấm bài."* (Lỗi: nhảy thẳng vào Solution khi chưa đào sâu Problem).

### Diamond 2: Develop & Deliver (Phát triển & Chuyển giao)

- **Quy trình triển khai:**
$$\text{Generate Idea} \longrightarrow \text{Prototype} \longrightarrow \text{Test with User} \longrightarrow \text{Measure} \longrightarrow \text{Iterate} \longrightarrow \text{Production}$$

---

## 3. Quy trình Human-Centered Design (Ví dụ: Hệ thống EdTech)

| Giai đoạn | Hành động cụ thể |
| :--- | :--- |
| **Observation** | Nhận thấy Tutor mất quá nhiều thời gian để chấm bài thủ công. |
| **Ideation** | Đề xuất giải pháp dùng AI chấm bài trắc nghiệm (MCQ) và câu trả lời ngắn (short answer). |
| **Prototype** | Xây dựng dịch vụ thử nghiệm AI grading service. |
| **Test** | Cho AI chấm thử 200 bài đã có sẵn kết quả chấm từ Tutor. |
| **Measure** | Đánh giá, so sánh độ chính xác và thời gian giữa AI với Tutor. |
| **Iteration** | Tinh chỉnh lại Rubric, System Prompt hoặc Model dựa trên sai lệch thực tế. |

---

## 4. Cấu trúc một Problem Statement chuẩn

Một Problem Statement chất lượng cao cần đáp ứng đủ **6 yếu tố cốt lõi**:

1. **Actor:** Đối tượng chịu tác động chính (ai gặp vấn đề?).
2. **Workflow:** Quy trình làm việc hiện tại.
3. **Bottleneck:** Điểm nghẽn gây lãng phí tài nguyên/thời gian.
4. **Impact:** Tác động tiêu cực trực tiếp đến trải nghiệm hoặc vận hành.
5. **Metric:** Chỉ số đo lường hiệu quả kỳ vọng.
6. **Boundary:** Giới hạn phạm vi hoạt động của AI.

### Ví dụ chuẩn:
> *"**Tutor (Actor)** đang **chấm thủ công (Workflow)** câu trắc nghiệm và câu trả lời ngắn, khiến **thời gian phản hồi cho học sinh bị kéo dài (Bottleneck & Impact)**. Cần một hệ thống giúp **giảm ít nhất 70% khối lượng công việc chấm bài (Metric)**, nhưng **tuyệt đối không cho AI quyết định điểm đối với các bài tự luận dài (Boundary)**."*

### ⚠️ Nguyên tắc về Boundary
> **AI Engineer giỏi không chỉ biết xác định AI làm được gì, mà quan trọng hơn là phải thiết lập rõ ràng AI không được phép làm gì.**

---

# 🧠 II. Định vị AI & Lựa chọn giải pháp (AI Positioning & Solution Selection)

## 1. Nguyên tắc cốt lõi: Có thực sự cần AI không?
- Chỉ đặt câu hỏi về giải pháp công nghệ sau khi đã xác định rõ Problem Statement.
- **Đừng lạm dụng AI cho mọi bài toán.**
- Nếu logic xác định được bằng luật rõ ràng, luôn ưu tiên các giải pháp lập trình truyền thống để tối ưu chi phí, độ trễ và độ tin cậy.

---

## 2. Khi nào KHÔNG dùng AI? (Rule-based & Heuristic)
Sử dụng hệ thống dựa trên quy tắc (Rule-based) hoặc thuật toán kinh nghiệm (Heuristic) khi bài toán có **logic đóng, rõ ràng và tất định (deterministic)**:
- **Tính điểm MCQ:** Đối chiếu đáp án học sinh chọn với đáp án chuẩn ($A, B, C, D$).
- **Kiểm tra deadline:** So sánh `current_timestamp > deadline_timestamp`.
- **Phân quyền người dùng (Role-based Permission):** Kiểm tra `user.role == 'admin'` hoặc quyền truy cập tài nguyên.
- **Validate form:** Kiểm tra định dạng email, độ dài mật khẩu, số điện thoại, trường bắt buộc.
- **Quản lý trạng thái booking:** Chuyển đổi trạng thái đơn hàng/đặt chỗ ($\text{Pending} \rightarrow \text{Confirmed} \rightarrow \text{Completed}$).

---

## 3. Khi nào BẮT BUỘC / NÊN dùng AI?
AI (đặc biệt là LLM / Machine Learning) phát huy tối đa giá trị khi dữ liệu và yêu cầu có các đặc tính sau:
- **Tính mờ (Fuzzy):** Không có ranh giới đúng/sai nhị phân tuyệt đối; kết quả phụ thuộc vào ngữ cảnh hoặc cảm nhận.
- **Ngữ nghĩa & Ngôn ngữ (Semantic / Language-based):** Cần hiểu ý định (intent), sắc thái biểu cảm, cấu trúc câu tự nhiên thay vì chỉ khớp từ khóa (keyword matching).
- **Xác suất (Probabilistic):** Kết quả mang tính suy luận thống kê dựa trên không gian mẫu rộng lớn.
- **Không thể vét cạn bằng Rule-based:** Số lượng trường hợp ngoại lệ (edge cases) quá lớn để viết `if-else`.

### Ví dụ điển hình:
- **Yêu cầu:** *"Giải thích lực hấp dẫn hoạt động như thế nào?"*
- **Đặc điểm:** Có vô số cách diễn đạt đúng (giải thích cho trẻ em, giải thích theo cơ học cổ điển Newton, hoặc giải thích theo độ cong không-thời gian của Einstein).
- **Kết luận:** Dùng biểu diễn ngữ nghĩa (Semantic) và mô hình ngôn ngữ phù hợp hơn nhiều so với việc cố gắng viết hàng nghìn luật `if-else` cứng nhắc.

---

## 4. Bảng đối chiếu: Rule-based vs. AI

| Tiêu chí | Rule-based / Heuristics | AI / LLM Solutions |
| :--- | :--- | :--- |
| **Logic bài toán** | Tất định (Deterministic), rõ ràng, cố định | Xác suất (Probabilistic), có tính mờ (Fuzzy) |
| **Dữ liệu đầu vào** | Cấu trúc chuẩn, ranh giới rõ ràng | Ngôn ngữ tự nhiên, hình ảnh, đa ngữ nghĩa |
| **Khả năng mở rộng rule** | Phức tạp dần và dễ gãy khi thêm edge case | Tự tổng quát hóa theo ngữ cảnh đào tạo/prompt |
| **Độ trễ & Chi phí** | Cực thấp, tài nguyên tính toán tối thiểu | Cao hơn, cần hạ tầng suy luận chuyên biệt |

---

# ⚡ III. Tự động hóa vs. Hỗ trợ con người (Automation vs. Augmentation)

## 1. Bản chất của sự phân tách (Distinction)
Việc phân định rõ giữa **Automation** và **Augmentation** quyết định trực tiếp đến kiến trúc hệ thống, trải nghiệm người dùng (UX) và mức độ rủi ro khi triển khai AI vào thực tế.

- **Automation (Tự động hóa hoàn toàn):** AI thay thế con người thực hiện toàn bộ tác vụ từ đầu đến cuối (*Human-out-of-the-loop*).
- **Augmentation (Hỗ trợ / Tăng cường năng lực):** AI đóng vai trò trợ lý, xử lý phần thô hoặc gợi ý quyết định để con người kiểm duyệt và chốt kết quả cuối cùng (*Human-in-the-loop*).

---

## 2. So sánh chi tiết qua ví dụ chấm bài

```
[ Automation Workflow ]
Input: Bài thi ──> AI chấm & đối chiếu ──> Chốt điểm và lưu hệ thống

[ Augmentation Workflow ]
Input: Bài thi ──> AI phân tích & gợi ý điểm/nhận xét ──> Tutor kiểm duyệt ──> Chốt điểm chính thức
```

### a. Automation (Tự động hóa)
Áp dụng cho các tác vụ lặp lại, có độ chính xác cao hoặc rủi ro sai sót thấp:
- **MCQ Grading:** Hệ thống tự động so khớp đáp án chuẩn và ghi nhận điểm số 100% tự động.
- **Short Answer Grading (kèm ngưỡng tin cậy):**

$$\text{Input: Short Answer} \longrightarrow \text{LLM Evaluation} \longrightarrow \text{Confidence} \ge 0.96 \longrightarrow \text{Auto Grade}$$

*(Nếu độ tự tin của model vượt ngưỡng an toàn, hệ thống tự động cho phép chốt điểm; ngược lại chuyển sang Tutor kiểm duyệt).*

### b. Augmentation (Hỗ trợ con người)
Áp dụng cho các tác vụ phức tạp, giàu ngữ nghĩa, mang tính chủ quan hoặc có tác động lớn:
- **Long Essay Evaluation:**

$$\text{Input: Long Essay} \longrightarrow \text{AI phân tích luận điểm} \longrightarrow \text{Gợi ý điểm \& Feedback} \longrightarrow \text{Tutor đánh giá lại} \longrightarrow \text{Quyết định cuối cùng}$$

---

## 3. Bảng phân định Automation vs. Augmentation

| Tiêu chí | Automation (Tự động hóa) | Augmentation (Hỗ trợ con người) |
| :--- | :--- | :--- |
| **Vai trò của AI** | Người thực thi chính (*Doer*) | Trợ lý hỗ trợ ra quyết định (*Advisor / Co-pilot*) |
| **Vai trò con người** | Giám sát ngẫu nhiên / xử lý ngoại lệ | Người kiểm duyệt và chịu trách nhiệm cuối cùng |
| **Phù hợp với** | Logic rõ ràng, tác vụ chuẩn hóa, rủi ro thấp | Đánh giá đa chiều, sáng tạo, ngữ cảnh phức tạp |
| **Quy trình điển hình** | Chấm trắc nghiệm, phân loại spam, trích xuất dữ liệu form | Chấm bài tự luận, chẩn đoán y khoa sơ bộ, thẩm định hồ sơ vay |

---

## 4. Nguyên tắc cốt lõi khi thiết kế hệ thống AI
- **Quy tắc vàng:** Đối với các quyết định quan trọng (*High-stakes decisions*), AI luôn nên đóng vai trò là **Augmentation** thay vì Automation.
- **Tính chịu trách nhiệm:** Con người phải luôn là chốt chặn cuối cùng chịu trách nhiệm về mặt đạo đức, pháp lý và tính công bằng của quyết định.

---

# 🎯 IV. Thiết kế hàm mục tiêu / Phần thưởng (Reward Function & Objective Design)

## 1. Bản chất của Reward Function trong AI System
Một hệ thống AI không chỉ cần hoạt động được mà kỹ sư còn phải định nghĩa rõ ràng: *"Thế nào là một đầu ra tốt?"*.

- **Reward Function (Hàm mục tiêu / Hàm thưởng):** Bộ tiêu chuẩn và công thức định lượng dùng để đánh giá mức độ hiệu quả, dẫn hướng hành vi của mô hình và toàn bộ hệ thống.
- **Rủi ro:** Nếu không định nghĩa chính xác những gì cần tối ưu và những gì cần triệt tiêu, hệ thống sẽ phát triển theo các hành vi lệch lạc (*misaligned behavior*).

---

## 2. Công thức tư duy thiết kế Reward đa chiều (Objective Reward Design)

Trong một hệ thống phức tạp (ví dụ: AI Tutor), hàm mục tiêu phải cân bằng giữa các yếu tố giá trị gia tăng $(+)$ và các hình phạt / rủi ro $(-)$:

$$\text{Reward} = \underbrace{\Big( \text{Correctness} + \text{Groundedness} + \text{Learning Improvement} + \text{User Satisfaction} \Big)}_{\text{Giá trị mong muốn (+) }} - \underbrace{\Big( \text{Hallucination} + \text{Unsafe Response} \Big)}_{\text{Rủi ro \& Hình phạt (-)}}$$

### Chi tiết các thành phần:
- **Answer Correctness (+):** Tính chính xác về mặt kiến thức, khái niệm và giải thuật.
- **Groundedness (+):** Mức độ bám sát tài liệu nguồn, giáo trình (đặc biệt quan trọng trong kiến trúc RAG).
- **Learning Improvement (+):** Tác động thực tế đến sự tiến bộ của người học (học sinh có hiểu bài hơn sau tương tác không).
- **User Satisfaction (+):** Trải nghiệm người dùng, độ tự nhiên và hữu ích trong phản hồi.
- **Hallucination Penalty (-):** Phạt nặng khi AI bịa đặt thông tin không có trong tài liệu.
- **Unsafe Response Penalty (-):** Phạt triệt để nếu vi phạm an toàn thông tin, đạo đức hoặc ranh giới cho phép.

---

## 3. Cạm bẫy: Tối ưu hóa trên một chỉ số duy nhất (Single Metric Trap)

Lỗi phổ biến nhất khi thiết kế hệ thống AI là chỉ tập trung tối ưu hóa một metric duy nhất (dẫn đến hệ quả của Định luật Goodhart - *"When a measure becomes a target, it ceases to be a good measure"*).

### Ví dụ điển hình: Tối ưu hóa Engagement (Thời gian tương tác)
- **Hành vi sai lệch:** Nếu chỉ thưởng cho AI khi giữ chân người dùng lâu, AI Tutor sẽ có xu hướng trả lời vòng vo, đưa thêm câu hỏi phụ không cần thiết, hoặc làm người dùng bối rối để kéo dài phiên học.
- **Hậu quả:** Metric engagement tăng vọt nhưng Learning Improvement bằng 0 (học sinh tốn nhiều thời gian mà không học được gì).

---

## 4. Bảng đối chiếu: Single Metric vs. Multi-objective Reward Design

| Tiêu chí | Single Metric Optimization | Multi-objective Reward Design |
| :--- | :--- | :--- |
| **Tiêu điểm** | Tối ưu 1 chỉ số duy nhất (ví dụ: Session duration, Clicks) | Cân bằng giữa hiệu quả sử dụng, độ chính xác và an toàn |
| **Rủi ro** | Dễ bị "hack" mục tiêu (Goodhart's Law), hành vi tiêu cực | Hệ thống ổn định, phát triển theo đúng giá trị cốt lõi |
| **Độ phức tạp** | Đơn giản, dễ đo nhưng sai lệch thực tế | Cần thiết lập bộ tiêu chuẩn đánh giá (Evaluation Rubric) đa chiều |

---

# 📊 V. Precision và Recall trong Đánh giá Hệ thống AI

## 1. Nền tảng: Ma trận nhầm lẫn (Confusion Matrix)
Để hiểu rõ Precision và Recall, cần nắm 4 thành phần cơ bản của Confusion Matrix:

- **True Positive ($TP$):** AI dự đoán Đúng/Có liên quan, và thực tế nó **Thực sự Đúng**.
- **False Positive ($FP$):** AI dự đoán Đúng/Có liên quan, nhưng thực tế nó **Sai/Không liên quan** (*Báo động giả*).
- **False Negative ($FN$):** AI bỏ qua hoặc đoán Sai, nhưng thực tế nó **Là cái Đúng cần tìm** (*Bỏ sót*).
- **True Negative ($TN$):** AI dự đoán Sai/Không liên quan, và thực tế nó **Thực sự Không liên quan**.

---

## 2. Định nghĩa & Công thức

```
                      Tổng các mẫu AI dự đoán là Positive (TP + FP)
                                   ┌───────────────┐
                                   │  TP  │   FP   │
                                   └───────────────┘
                                      ▲
           Precision = TP / (TP + FP) │ "AI nói đúng bao nhiêu cái thực sự đúng?"
                                      │
─────────────────────────────────────────────────────────────────────────────────
                                      │
           Recall    = TP / (TP + FN) │ "AI tìm được bao nhiêu cái cần tìm?"
                                      ▼
                                   ┌───────────────┐
                                   │  TP  │   FN   │
                                   └───────────────┘
                      Tổng các mẫu Thực tế là Positive (TP + FN)
```

### a. Precision (Độ chính xác)
Trong số tất cả những kết quả mà AI trả về, có bao nhiêu phần trăm là thực sự đúng?

$$\text{Precision} = \frac{TP}{TP + FP}$$

- **Ý nghĩa:** Đo lường mức độ "đáng tin" của câu trả lời do AI đưa ra.
- **Tập trung vào:** Giảm thiểu $FP$ (không đưa ra thông tin rác / kết quả sai lệch).

### b. Recall (Độ phủ / Độ thu hồi)
Trong số tất cả những kết quả đúng thực tế đang tồn tại, AI đã bắt được bao nhiêu phần trăm?

$$\text{Recall} = \frac{TP}{TP + FN}$$

- **Ý nghĩa:** Đo lường khả năng "không bỏ sót" mục tiêu của hệ thống.
- **Tập trung vào:** Giảm thiểu $FN$ (tránh việc bỏ qua tài liệu quan trọng).

---

## 3. Ví dụ thực tế: Hệ thống Information Retrieval (RAG / Search)

- **Thực tế:** Có tổng cộng $100$ đoạn tài liệu thực sự liên quan đến câu hỏi ($TP + FN = 100$).
- **Hệ thống truy xuất:** Lấy về $20$ đoạn văn bản ($TP + FP = 20$).
- **Kết quả đối chiếu:** Trong $20$ đoạn lấy về, có $15$ đoạn thực sự đúng ($TP = 15$) và $5$ đoạn sai/không liên quan ($FP = 5$).

$$\text{Precision} = \frac{15}{20} = 75\%$$

$$\text{Recall} = \frac{15}{100} = 15\%$$

> **Nhận xét:** Precision ở mức khá tốt ($75\%$), nhưng Recall cực kỳ tệ ($15\%$) vì hệ thống đã bỏ sót đến $85$ đoạn thông tin quan trọng ($FN = 85$).

---

## 4. Ứng dụng trong kiến trúc Retrieval & Reranker

Mối quan hệ đánh đổi (**Trade-off**) giữa Precision và Recall là lý do các hệ thống Search / RAG hiện đại sử dụng kiến trúc 2 giai đoạn (**Two-stage Retrieval**):

```
[ Toàn bộ Corpus (Hàng triệu docs) ]
               │
               ▼  Giai đoạn 1: First-stage Retrieval (BM25, Vector Search)
     [ High Recall ] ──> Lấy rộng (Top 50 - 100 docs) để gom hết cái đúng, chấp nhận lẫn rác (FP cao)
               │
               ▼  Giai đoạn 2: Reranker (Cross-Encoder / ColBERT)
   [ High Precision ] ──> Lọc kỹ & sắp xếp lại, đẩy tài liệu chuẩn nhất lên Top 3 - 5
               │
               ▼
      [ LLM Generation ]
```

- **Giai đoạn 1 (Retrieval - Ưu tiên High Recall):** Quét qua không gian dữ liệu khổng lồ với tốc độ cao, lấy về số lượng lớn tài liệu nhằm đảm bảo **không bỏ sót** thông tin quan trọng.
- **Giai đoạn 2 (Reranker - Ưu tiên High Precision):** Sử dụng mô hình chuyên sâu hơn để xếp hạng lại tập tài liệu nhỏ vừa lấy về, loại bỏ kết quả nhiễu ($FP$) và giữ lại các đoạn có độ chính xác cao nhất đưa vào Context của LLM.

---

# 🏗️ VI. Phân cấp kỹ thuật trong Xây dựng Hệ thống AI (Architectural Levels)

## 1. Bản chất của 3 cấp độ kiến trúc
Hệ thống kỹ thuật được chia thành **3 cấp độ (Levels)** dựa trên mức độ tự chủ (*Autonomy*) và tính tất định (*Determinism*) của luồng xử lý:

```
[ Cấp 1: Rule / Script ]  ───►  [ Cấp 2: Workflow / Graph ]  ───►  [ Cấp 3: Agentic System ]
  (Cố định, tất định)             (Phân nhánh có cấu trúc)           (Tự chủ ra quyết định)
```

---

## 2. Chi tiết 3 cấp độ kiến trúc

### a. Cấp 1: Rule / Script (Quy tắc & Kịch bản cố định)
- **Luồng xử lý:**
$$\text{Input} \longrightarrow \text{Rule / Logic} \longrightarrow \text{Output}$$
- **Đặc điểm:** Hoàn toàn tất định (deterministic), tuyến tính, không có yếu tố bất định hay xác suất.
- **Phù hợp cho:**
  - Data validation (kiểm tra định dạng email, phone).
  - Role-based permissions (phân quyền truy cập tài nguyên).
  - Business logic cố định (tính thuế, áp mã giảm giá).

### b. Cấp 2: Workflow (Quy trình tuần tự & Phân nhánh có cấu trúc)
- **Luồng xử lý:**
$$\text{Input} \longrightarrow \text{Step A} \longrightarrow \text{Step B} \longrightarrow \text{Decision} \longrightarrow \text{Step C} \text{ hoặc } \text{Step D}$$
- **Cơ chế:** Thường triển khai dưới dạng State Machine, DAG (Directed Acyclic Graph) hoặc Graph (ví dụ: LangGraph, Temporal, Airflow).
- **Ví dụ thực tế (Xử lý tài liệu PDF):**
$$\text{Upload PDF} \longrightarrow \text{Parse text} \longrightarrow \text{Extract embeddings} \longrightarrow \text{Store to Vector DB} \longrightarrow \text{System Ready}$$
- **⚠️ Lưu ý quan trọng:** Luồng này xử lý nhiều bước phức tạp nhưng hoàn toàn do Developer định nghĩa trước toàn bộ đường đi $\rightarrow$ **Không cần và không nên dùng Agent.**

### c. Cấp 3: Agent (Hệ thống Tự chủ / Vòng lặp Suy luận)
- **Luồng xử lý (ReAct Loop):**
$$\text{Goal} \longrightarrow \text{Reason} \longrightarrow \text{Choose Tool} \longrightarrow \text{Execute \& Observe} \longrightarrow \text{Reason tiếp} \longrightarrow \text{Choose Next Action}$$
- **Đặc điểm:** Áp dụng khi đường đi và số lượng bước thực thi không thể xác định trước tại thời điểm viết code.
- **Cơ chế:** Mô hình AI (LLM) được trao quyền tự quan sát kết quả trả về của môi trường/công cụ để quyết định hành động tiếp theo cho đến khi đạt được mục tiêu (*Goal*).

---

## 3. Phân định cốt lõi: Workflow vs. Agent

| Tiêu chí | Cấp 2: Workflow | Cấp 3: Agent |
| :--- | :--- | :--- |
| **Quyền quyết định đường đi** | Developer quyết định toàn bộ logic và nhánh rẽ từ trước | AI Model có quyền tự quyết định một phần hoặc toàn bộ đường đi |
| **Tính dự đoán (Determinism)** | Cao, dễ debug, kiểm soát hoàn toàn flow | Thấp hơn, linh hoạt xử lý bài toán mở, khó debug |
| **Chi phí & Độ trễ** | Tối ưu, ổn định | Tốn nhiều token và vòng gọi lặp (*multi-step loops*) |
| **Công cụ tham khảo** | LangChain (Chains), LangGraph (StateGraph), Airflow | LangGraph (Agentic loops), AutoGen, CrewAI |

---

# 🔬 VII & VIII. Cơ chế cốt lõi của LLM — Tokenization, Embedding & Attention Mechanism

## 1. Phần 7: Tokenization & Embedding (Cách LLM nhìn nhận ngôn ngữ)
LLM không trực tiếp đọc hay hiểu văn bản dưới dạng ký tự chữ cái thông thường. Quy trình biến đổi văn bản đầu vào thành dữ liệu toán học diễn ra qua 3 bước:

```
[ Raw Text ] ──► [ Tokenizer ] ──► [ Token IDs ] ──► [ Embedding Matrix ] ──► [ Dense Vectors ]
```

- **Tokenization:** Văn bản thô được phân tách thành các mảnh nhỏ gọi là **Tokens** (từ vựng, cụm ký tự hoặc âm tiết).
  - *Ví dụ:* `"I love artificial intelligence"` $\longrightarrow$ `["I", " love", " artificial", " intelligence"]`
- **Token IDs (Số hóa):** Mỗi token được ánh xạ sang một ID số nguyên tương ứng trong bảng từ vựng (*Vocabulary*).
  - *Ví dụ:* `[40, 1842, 10598, 4438]`
- **Embedding Lookup:** Mỗi Token ID được chuyển đổi thành một vector toán học nhiều chiều (**Dense Vector**), lưu giữ tọa độ ngữ nghĩa của từ trong không gian vector đa chiều.

---

## 2. Phần 8: Cơ chế Attention — Nền tảng kiến trúc Transformer
Cơ chế **Self-Attention** cho phép mỗi token trong câu tính toán mối quan hệ và mức độ liên quan đối với toàn bộ các token còn lại trong cùng văn bản.

### Ví dụ về giải quyết nhập nhằng ngữ nghĩa (Coreference Resolution):
> **Câu:** *"The animal didn't cross the street because it was tired."*
> 
> **Nhiệm vụ của Attention:** Giúp mô hình xác định đại từ **"it"** đang liên kết chặt chẽ nhất với **"animal"** (thay vì *"street"*).

---

## 3. Bản chất của bộ 3 Vector: Query, Key, Value ($Q, K, V$)

Tại mỗi tầng của Transformer, mỗi token embedding được chiếu thành 3 vector độc lập:

| Vector | Vai trò | Câu hỏi đại diện |
| :--- | :--- | :--- |
| **Query ($Q$)** | Đi tìm kiếm ngữ cảnh | *"Tôi đang tìm kiếm những thông tin/thuộc tính gì?"* |
| **Key ($K$)** | Nhãn định danh nội dung | *"Tôi đang lưu trữ những thông tin/đặc điểm gì?"* |
| **Value ($V$)** | Nội dung thông tin thực tế | *"Nội dung giá trị thực sự của tôi là gì?"* |

---

## 4. Công thức Scaled Dot-Product Attention

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$

### Quy trình tính toán từng bước:
1. **Tích vô hướng ($Q \times K^T$):** Lấy vector Query của token hiện tại nhân với Key của tất cả các token khác để tính độ tương đồng (*Attention Score*).
2. **Chia tỷ lệ ($\sqrt{d_k}$):** Chia cho căn bậc hai của số chiều vector Key ($d_k$) để ổn định độ lớn gradient khi đạo hàm (tránh tràn số).
3. **Chuẩn hóa Softmax:** Chuyển đổi các điểm số thành phân phối xác suất có tổng bằng $1$ (trọng số chú ý - *Attention Weights*).
4. **Tổng hợp có trọng số ($\times V$):** Lấy các trọng số vừa chuẩn hóa nhân với vector Value ($V$) tương ứng để tạo ra vector đại diện mới giàu ngữ cảnh cho token.

---

# 🚀 IX & X. Vòng đời huấn luyện LLM — Pre-training, SFT & Preference Alignment (RLHF)

## 1. Tổng quan quy trình huấn luyện LLM hiện đại
Một mô hình ngôn ngữ lớn (LLM) để trở thành một trợ lý AI hữu ích cần trải qua 3 giai đoạn chính:

```
[ Raw Text Data ] ──► [ Pre-training ] ──► [ Base Model ] 
                                                   │
                                                   ▼
[ Instruction Data ] ──► [ Supervised Fine-Tuning (SFT) ] ──► [ SFT Model ]
                                                                    │
                                                                    ▼
[ Preference Data ] ──► [ Alignment / RLHF ] ──► [ Aligned Assistant Model ]
```

---

## 2. Phần 9: Pre-training (Huấn luyện tiền kỳ)

### a. Bản chất toán học: Next-Token Prediction
Ở giai đoạn Pre-training, LLM được huấn luyện trên hàng nghìn tỷ token văn bản phi cấu trúc (web, sách, mã nguồn) với mục tiêu tự hồi quy duy nhất: **Dự đoán xác suất của token tiếp theo dựa trên chuỗi token đã có phía trước**.

$$P(x_1, x_2, \dots, x_T) = \prod_{t=1}^{T} P(x_t \mid x_1, x_2, \dots, x_{t-1})$$

**Ví dụ:**
- **Input:** `"The capital of France is..."`
- **Model tính toán phân phối xác suất trên toàn bộ từ điển:**
  - `"Paris"`: $0.99$
  - `"London"`: $0.02$
  - `"Berlin"`: $0.01$

### b. Góc nhìn Kỹ sư AI: Vì sao LLM bị Hallucination?
- **LLM là Probabilistic Text Generator (bộ sinh văn bản dựa trên xác suất)**, hoàn toàn không phải là Database chứa dữ liệu có cấu trúc hay công cụ truy vấn thông tin tuyệt đối.
- Model ghép các token tiếp theo sao cho câu nghe trôi chảy và hợp lý nhất về mặt thống kê. Do đó, model có thể viết ra một câu cực kỳ tự nhiên, ngữ pháp hoàn hảo nhưng nội dung bên trong hoàn toàn sai sự thật (**Hallucination**).

---

## 3. Phần 10: Post-Training (SFT & Preference Alignment)

### a. SFT (Supervised Fine-Tuning — Tinh chỉnh có giám sát)
Sau giai đoạn Pre-training, Base Model chỉ biết tự động viết tiếp câu chứ chưa biết đóng vai trò làm trợ lý để trả lời câu hỏi. SFT huấn luyện mô hình trên tập dữ liệu dạng cặp `(Instruction/Prompt, Desired Response)`.

- **Ví dụ mẫu dữ liệu SFT:**
  - **Instruction:** `"Explain RAG"`
  - **Target Response:** `"RAG stands for Retrieval-Augmented Generation. It is an architecture that combines information retrieval with text generation..."`
- **Mục đích:** Dạy model nhận diện mệnh lệnh của người dùng và sinh câu trả lời theo đúng định dạng mong muốn.

### b. Preference Alignment / RLHF (Căn chỉnh theo ý định con người)
Dù đã qua SFT, mô hình vẫn có thể sinh câu trả lời dài dòng, độc hại hoặc không đúng ý người dùng. **RLHF (Reinforcement Learning from Human Feedback)** giúp model học được "sở thích" (*preference*) của con người:

1. Cho model sinh ra nhiều câu trả lời khác nhau ($A$ và $B$) cho cùng một câu hỏi.
2. Con người (hoặc mô hình chấm điểm AI) đánh giá: Chọn **Response A** (*Upvote/Like*) và từ chối **Response B** (*Downvote/Dislike*).
3. Sử dụng thuật toán học tăng cường (hoặc các phương pháp trực tiếp như **DPO**, **KTO**) để hướng mô hình ưu tiên sinh ra các phản hồi tương tự như $A$.

---

## 4. Bảng đúc kết tư duy cốt lõi

| Giai đoạn | Vai trò cốt lõi | Dữ liệu đầu vào | Output |
| :--- | :--- | :--- | :--- |
| **Pre-training** | Tạo ra năng lực (*Knowledge & Reasoning capabilities*) | Hàng nghìn tỷ tokens văn bản thô | **Base Model** |
| **Post-training (SFT + RLHF)** | Điều chỉnh hành vi (*Behavior, Safety, Style, Instruction-following*) | Cặp Instruction-Response & Preference pairs | **Production-ready Assistant** |

> 💡 **Quy tắc vàng:** *"Pre-training creates capabilities, post-training steers behavior."* (Pre-training tạo ra tri thức và năng lực suy luận, còn Post-training định hình phong cách, sự an toàn và hành vi tương tác).

---

# 🤖 XII, XIII & XIV. Kiến trúc AI Agent, Khung ReAct & Function Calling

## 1. Phần 12: Cấu trúc tổng quan của mô hình AI Agent
Một hệ thống AI Agent hoàn chỉnh hoạt động dựa trên một **vòng lặp kín gồm 6 thành phần cốt lõi**:

```
                  ┌───────────────────────────────┐
                  ▼                               │
[ Goal ] ──► [ Reasoning ] ──► [ Tool / Action ] ──┤
                  ▲                               │
                  │        [ Memory ]             │
                  │             ▲                 │
                  └────── [ Observation ] ◄───────┘
```

- **Goal:** Mục tiêu người dùng yêu cầu agent hoàn thành.
- **Reasoning:** Quá trình phân tích trạng thái hiện tại và lập kế hoạch bước tiếp theo.
- **Tool & Action:** Chọn và thực thi công cụ tương ứng (*Search, Calculator, Database API...*).
- **Observation:** Tiếp nhận và phân tích kết quả trả về từ môi trường/công cụ.
- **Memory:** Bộ nhớ ngắn hạn (lịch sử hội thoại/vết suy luận) và dài hạn (vector context).

### Ví dụ luồng xử lý: *"Tìm tài liệu RAG và tóm tắt cho tôi"*
1. **Understand Request:** Phân tích yêu cầu $\rightarrow$ xác định cần tìm tài liệu về RAG.
2. **Action (Search):** Gọi công cụ tìm kiếm trong cơ sở dữ liệu.
3. **Observation (Read Document):** Đọc nội dung các tài liệu vừa lấy về.
4. **Decision:** Kiểm tra xem thông tin đã đủ chưa?
   - *Nếu chưa đủ:* Thực hiện truy vấn lại với từ khóa khác.
   - *Nếu đã đủ:* Tổng hợp kiến thức và sinh câu trả lời tóm tắt cho người dùng.

---

## 2. Phần 13: ReAct Framework (Reasoning + Acting)
ReAct là mô hình kết hợp giữa **Suy luận (Reasoning)** và **Hành động (Acting)**, cho phép LLM vừa "nghĩ" vừa "làm" và tự hiệu chỉnh thông qua kết quả quan sát được.

### Chu trình chuẩn của ReAct:
$$\text{Reasoning} \longrightarrow \text{Action} \longrightarrow \text{Observation} \longrightarrow \text{Reasoning} \longrightarrow \text{Action} \longrightarrow \dots \longrightarrow \text{Final Answer}$$

### Ví dụ phân tích từng bước:
- **Goal:** *"Doanh thu quý gần nhất của Apple là bao nhiêu?"*
- **Thought / Reasoning 1:** Cần tra cứu báo cáo tài chính mới nhất của Apple.
- **Action 1:** `search_web(query="Apple latest quarterly revenue report")`
- **Observation 1:** Tìm thấy thông cáo báo chí tài chính từ CEO/CFO của Apple.
- **Thought / Reasoning 2:** Đã có tài liệu, cần đọc đúng số liệu doanh thu tổng.
- **Action 2:** `read_document(url="apple_q3_report.pdf")`
- **Observation 2:** Tìm thấy thông tin `Revenue = $85.8B`.
- **Final Answer:** Doanh thu quý gần nhất của Apple đạt 85.8 tỷ USD.

> 💡 **Tư duy kỹ thuật:** Điểm mấu chốt của ReAct không phải là cố in toàn bộ chuỗi suy nghĩ (*Thought/Reasoning*) ra giao diện cho người dùng thấy, mà là thiết lập kiến trúc cho phép model tự suy luận, gọi công cụ, quan sát phản hồi và ra quyết định tiếp theo.

---

## 3. Phần 14: Function Calling & Bảo mật Hệ thống (Tool Security)
**LLM chỉ là bộ xử lý văn bản, nó không thể và tuyệt đối không bao giờ được phép trực tiếp kết nối hay thực thi truy vấn vào Database.**

### 3.1. Cấu trúc của một Tool Schema
Mọi công cụ cung cấp cho LLM phải được định nghĩa tường minh bằng Schema (thường là JSON Schema):

```json
{
  "name": "search_knowledge_base",
  "description": "Truy vấn các tài liệu kỹ thuật nội bộ theo từ khóa",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Từ khóa tìm kiếm"
      },
      "top_k": {
        "type": "integer",
        "description": "Số lượng văn bản cần trả về",
        "default": 3
      }
    },
    "required": ["query"]
  }
}
```

### 3.2. Luồng thực thi Function Calling chuẩn bảo mật

```
[ User Prompt ] ──► [ LLM ] ──► Sinh ra Tool Call (JSON: Name & Params)
                                      │
                                      ▼
                        [ Backend Application Layer ]
                        ├── Step 1: Input Validation & Sanitization
                        ├── Step 2: Role-based Permission Check
                        └── Step 3: Execute DB API / External Tool
                                      │
                                      ▼
                    [ Tool Result / Data Output ]
                                      │
                                      ▼
[ Final Response ] ◄── [ LLM ] ◄──────┘ (Gửi dữ liệu thô về cho LLM tổng hợp)
```

---

## 4. Bảng nguyên tắc bảo mật: LLM vs. Database

| Tiêu chuẩn | Thực hành SAI (Nguy hiểm) | Thực hành ĐÚNG (Bảo mật) |
| :--- | :--- | :--- |
| **Quyền truy cập DB** | Cho LLM chạy trực tiếp raw SQL query vào database. | LLM chỉ sinh cấu trúc tham số gọi hàm (*Function arguments*). |
| **Kiểm soát logic** | Tin tưởng tuyệt đối tham số do LLM tạo ra. | Backend kiểm tra kiểu dữ liệu (*Validation*), giới hạn quyền (*Permission*) trước khi query. |
| **Rủi ro phòng ngừa** | SQL Injection, rò rỉ toàn bộ bảng dữ liệu nhạy cảm. | Giới hạn phạm vi thao tác trong từng API endpoint cụ thể. |

---

# 🌐 XV — XXII. Kiến trúc Hybrid Routing và Kỹ thuật Retrieval Nâng cao trong RAG

## 1. Phần 15: Mô hình Kết hợp (Hybrid Pattern & Semantic Router)

Trong môi trường Production, việc áp dụng cơ chế Agent cho toàn bộ mọi request (*"Agent Everything"*) là một lỗi thiết kế nghiêm trọng, dẫn đến độ trễ cao, chi phí token lớn và khó kiểm soát lỗi. Kiến trúc chuẩn mực sử dụng một **Bộ điều hướng (Router)** để phân luồng request:

```
                                  ┌──► [ Flow 1: Simple Chat / FAQ ] ──► (LLM Direct / Cache)
                                  │
[ User Request ] ──► [ Router ] ──┼──► [ Flow 2: Structured Workflow ] ──► (Deterministic State Machine)
                                  │
                                  └──► [ Flow 3: Agentic Loop ] ────────► (ReAct / Dynamic Tools)
```

### Tiêu chí phân luồng tại Router:
Bộ định tuyến (Router) đánh giá **Query Intent** (ý định), **Complexity** (độ phức tạp) và **Risk Level** (mức độ rủi ro) để chọn nhánh xử lý tối ưu:

| Nhánh xử lý | Trường hợp sử dụng | Ví dụ luồng thực thi |
| :--- | :--- | :--- |
| **Flow 1: Simple Chat** | Hỏi đáp FAQ, chào hỏi xã giao, tra cứu thông tin đơn giản. | Trả lời trực tiếp từ Prompt Cache hoặc Context ngắn gọn. |
| **Flow 2: Workflow Task** | Quy trình kinh doanh xác định, logic tuần tự cố định. | **Quy trình Booking:** Thu thập info $\rightarrow$ Kiểm tra phòng trống $\rightarrow$ Chọn dịch vụ $\rightarrow$ Xác nhận thanh toán. |
| **Flow 3: Agent Task** | Nghiên cứu mở, nhiều bước cần lập kế hoạch (*planning*), không xác định trước số bước. | **Báo cáo phân tích:** Tự động tìm kiếm web, đọc nhiều nguồn, so sánh số liệu và tổng hợp báo cáo. |

---

## 2. Phần 16 — 20: Tổng quan RAG Ingestion Pipeline

Quy trình nạp dữ liệu cơ bản cho hệ thống RAG (*chi tiết đào sâu tại [rag-learning/docs/ALL_RAG.md](../rag-learning/docs/ALL_RAG.md)*):

```
[ Raw Documents ] ──► [ Parsing & Cleaning ] ──► [ Chunking ] ──► [ Embedding Model ] ──► [ Vector Database ]
```

- **Phần 16 (RAG Indexing):** Khâu lập chỉ mục toàn bộ tài liệu nguồn để phục vụ việc tìm kiếm nhanh chóng.
- **Phần 17 (Parsing):** Trích xuất văn bản thô, bảng biểu và cấu trúc từ các định dạng file đa dạng (*PDF, Docx, HTML, Markdown*).
- **Phần 18 (Chunking):** Cắt tài liệu thành các đoạn nhỏ có kích thước tối ưu (*Chunk size & Chunk overlap*).
- **Phần 19 (Embedding):** Biến đổi các đoạn text chunk thành các vector đặc trưng trong không gian ngữ nghĩa nhiều chiều.
- **Phần 20 (Vector Database):** Lưu trữ vector embedding kèm metadata (*Pinecone, Qdrant, Milvus, pgvector*) để phục vụ phép tìm kiếm tương đồng (*Cosine Similarity / Dot Product*).

---

## 3. Phần 21: Mở rộng truy vấn (Query Expansion)

Người dùng thường đặt câu hỏi rất ngắn hoặc thiếu từ khóa chuyên môn, khiến hệ thống tìm kiếm vector bỏ sót tài liệu quan trọng (**Low Recall**).

```
                      ┌──► Sub-query 1: "Transformer architecture overview"
                      │
[ Original Query: ] ──┼──► Sub-query 2: "Self-attention mechanism explained"
"Transformer hoạt     │
 động như thế nào?"   ├──► Sub-query 3: "Encoder-Decoder structure"
                      │
                      └──► Sub-query 4: "Multi-head attention role"
```

- **Cơ chế:** Dùng LLM viết lại câu hỏi gốc thành nhiều câu hỏi phụ (*Sub-queries*) hoặc bổ sung các khái niệm kỹ thuật liên quan.
- **Mục tiêu cốt lõi:** Tăng **Recall** lên tối đa trong giai đoạn First-stage Retrieval bằng cách bao phủ nhiều góc nhìn ngữ nghĩa khác nhau của vấn đề.

---

## 4. Phần 22: Kỹ thuật HyDE (Hypothetical Document Embeddings)

### a. Vấn đề khoảng cách ngữ nghĩa (Semantic Gap)
- Câu hỏi (*Query*) và Đoạn tài liệu chứa câu trả lời (*Document*) thường có cấu trúc ngữ pháp và phong cách viết hoàn toàn khác nhau.
- *Ví dụ:* Câu hỏi là câu nghi vấn ngắn, còn tài liệu là một đoạn phân tích dài chứa nhiều thuật ngữ học thuật $\rightarrow$ Độ tương đồng vector trực tiếp giữa câu hỏi và tài liệu có thể không cao.

### b. Giải pháp của HyDE
Thay vì đem câu hỏi thô đi embedding, HyDE sử dụng LLM để sinh ra một **tài liệu giả định (Hypothetical Answer)** trước khi tìm kiếm:

```
[ User Query ] ──► [ LLM Generation ] ──► [ Hypothetical Answer ] ──► [ Embedding ] ──► [ Vector Search ]
```

### c. Ví dụ quy trình thực thi:
1. **Câu hỏi người dùng:** *"Tại sao hệ thống RAG lại bị ảo giác (hallucination)?"*
2. **LLM sinh đoạn trả lời giả định:** *"RAG hallucination xảy ra do context retrieval không chính xác, context window quá dài làm loãng thông tin, hoặc model bị xung đột giữa parametric memory và external context..."*
   *(Dù thông tin này có thể chưa chuẩn 100%, nhưng phong cách và từ vựng của nó rất giống tài liệu kỹ thuật).*
3. **Thực thi:** Lấy vector của đoạn giả định này để truy vấn trong Vector Database $\rightarrow$ Kết quả tìm kiếm chính xác và sát ngữ cảnh hơn nhiều so với việc chỉ dùng câu hỏi gốc.

---

# 🔗 XXIII, XXV & XXVI. Hybrid Retrieval, In-Context Grounding & Citation trong RAG

## 1. Phần 23: Hybrid Retrieval & Reciprocal Rank Fusion (RRF)

Không có phương pháp tìm kiếm đơn lẻ nào là hoàn hảo. Hệ thống Retrieval chuẩn Production luôn kết hợp giữa **Dense Vector Search** và **Sparse Search (BM25)**:

- **Vector Search (Dense):** Rất mạnh về tìm kiếm theo ngữ nghĩa (*semantic context*), hiểu các từ đồng nghĩa và ý định ngầm.
- **BM25 (Sparse):** Rất mạnh về khớp từ khóa chính xác (*exact keyword matching*), mã định danh (*SKU, ID, tên riêng, thuật ngữ kỹ thuật*).

```
               ┌──► Vector Search (Top K) ──┐
[ User Query ] ┤                            ├──► [ Reciprocal Rank Fusion (RRF) ] ──► [ Cross-Encoder Reranker ]
               └──► BM25 Search (Top K) ────┘
```

### a. Thuật toán Reciprocal Rank Fusion (RRF)
RRF kết hợp thứ hạng của tài liệu từ các bảng xếp hạng khác nhau mà không cần chuẩn hóa điểm số tương đồng:

$$RRF\_Score(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

*(Trong đó $r_m(d)$ là thứ hạng của tài liệu $d$ trong hệ thống tìm kiếm $m$, và $k$ là hằng số làm mịn, thường chọn $k = 60$).*

### b. Pattern kinh điển: Retrieval vs. Reranker
- **Retrieval (Dense + Sparse):** Ưu tiên **Tốc độ (Speed)** và **Recall** $\rightarrow$ Quét nhanh hàng triệu tài liệu để lấy ra ứng viên tiềm năng (*Top 50 - 100*).
- **Cross-Encoder Reranker:** Ưu tiên **Độ chính xác (Accuracy)** và **Precision** $\rightarrow$ Đưa cả `(Query, Document)` vào mô hình để cùng nhau chấm điểm mức độ liên quan (*in-context relevance*), chính xác vượt trội so với phép đo cosine similarity độc lập.

---

## 2. Phần 25: In-Context Grounding & Chiến lược Chống Ảo giác (Anti-Hallucination)

Để buộc LLM chỉ trả lời dựa trên tài liệu được cung cấp, System Prompt cần định nghĩa rõ ràng logic giới hạn thông tin:

> **System Prompt Logic:**
> *"Answer the question ONLY using the supplied context below. If the context does not contain enough information to answer the question, state clearly that the information cannot be found. Do not assume or extrapolate from outside knowledge."*

### Vì sao chỉ dùng Prompt là KHÔNG ĐỦ?
Prompting chỉ giảm thiểu một phần xác suất sinh ảo giác. Để triệt tiêu hallucination ở cấp độ hệ thống, cần thiết lập một **chiến lược phòng thủ đa lớp (Defense-in-depth)**:

```
[ 1. High-Precision Retrieval ] ──► [ 2. Strict Reranking ] ──► [ 3. Guardrail Prompt ] ──► [ 4. Strict Citations ] ──► [ 5. Automated Eval & Feedback ]
```

1. **Retrieval & Reranking:** Đảm bảo Context đưa vào sạch, đúng trọng tâm và không chứa thông tin nhiễu.
2. **Prompt Enforcement:** Ràng buộc chặt chẽ phạm vi sinh câu trả lời.
3. **Citation & Attributions:** Buộc model phải trích xuất nguồn cụ thể cho từng khẳng định.
4. **Evaluation & Feedback:** Dùng LLM-as-a-judge kiểm tra chỉ số Faithfulness và Groundedness trước khi hiển thị cho người dùng.

---

## 3. Phần 26: Trích dẫn nguồn dữ liệu (Citation Architecture)

Citation không đơn thuần là ghi chú thêm ở cuối câu, mà là một thành phần kỹ thuật cốt lõi trong toàn bộ RAG pipeline.

### 3.1. Quản lý Metadata xuyên suốt Pipeline
Trong suốt quá trình Ingestion và Retrieval, mỗi đoạn văn bản (*chunk*) bắt buộc phải gắn liền với metadata:

```json
{
  "chunk_id": "chk_89412",
  "document_name": "Q3_Financial_Report.pdf",
  "page_number": 14,
  "section_title": "Operating Expenses & Revenue",
  "source_url": "https://internal.corp/reports/q3.pdf"
}
```

### 3.2. Định dạng đầu ra của LLM kèm Citation
Model được hướng dẫn trích dẫn nguyên văn (*quote*) kèm ID nguồn:
> *"Doanh thu quý 3 đạt 85.8 tỷ USD, tăng 5% so với cùng kỳ năm trước **[Doc: Q3_Financial_Report.pdf, Page: 14]**."*

---

## 4. Giá trị cốt lõi của Citation trong Hệ thống AI

| Vai trò | Giá trị mang lại |
| :--- | :--- |
| **User Verification** | Người dùng có thể nhấp trực tiếp vào trích dẫn để đọc lại trang gốc, tự kiểm chứng thông tin. |
| **System Debugging** | Kỹ sư dễ dàng truy vết xem câu trả lời sai là do Retrieval kéo nhầm chunk hay do LLM tự suy diễn sai. |
| **Metric Evaluation** | Tự động hóa việc chấm điểm độ bám sát tài liệu (*Groundedness / Faithfulness Score*). |
| **Trust & Compliance** | Tăng mức độ tin cậy của sản phẩm, đáp ứng các tiêu chuẩn khắt khe về mặt pháp lý và dữ liệu doanh nghiệp. |

---

# 📈 XXIX, XXX & PRD. Đánh giá RAG, Thiết kế Xác suất & Chuyển dịch từ Prototype sang Product

## 1. Phần 30: Khung đánh giá RAG (RAG Triad Evaluation)

Để đo lường và xác định chính xác điểm nghẽn gây lỗi trong pipeline RAG, hệ thống cần được đánh giá qua 3 trục của **RAG Triad**:

```
                       [ Question / Query ]
                           /          \
  (Answer Relevance)      /            \  (Context Relevance)
                         /              \
                        ▼                ▼
                 [ Answer ] ◄──────── [ Context ]
                           (Groundedness / Faithfulness)
```

### 1.1. Context Relevance (Độ liên quan của ngữ cảnh)
- **Câu hỏi kiểm tra:** *Tài liệu truy xuất được (Context) có thực sự liên quan đến câu hỏi của người dùng không?*
- **Nếu chỉ số thấp (Lỗi tại tầng Retrieval):**
  - Chiến lược Chunking chưa tối ưu (quá dài/quá ngắn, mất ngữ cảnh).
  - Mô hình Embedding không đủ mạnh hoặc không phù hợp miền dữ liệu.
  - Khâu Query Processing / Expansion chưa tốt.
  - Bộ lọc Reranker xếp hạng sai thứ tự.

### 1.2. Groundedness / Faithfulness (Độ trung thực / Bám sát tài liệu)
- **Câu hỏi kiểm tra:** *Câu trả lời (Answer) có thực sự được chứng minh và hỗ trợ bởi Context cung cấp hay không?*
- **Nếu chỉ số thấp (Lỗi tại tầng Generation):**
  - Model bị Hallucination (bịa đặt thông tin ngoài context).
  - System Prompt chưa đủ chặt chẽ trong việc cấm suy diễn tự do.
  - Context bị nhiễu (*Noise*), dẫn đến xung đột thông tin khiến LLM bị hiểu sai.

### 1.3. Answer Relevance (Độ liên quan của câu trả lời)
- **Câu hỏi kiểm tra:** *Câu trả lời có đi đúng trọng tâm và giải quyết trực tiếp câu hỏi ban đầu không?*
- **Nếu chỉ số thấp:**
  - Khâu Query Understanding hiểu sai ý định (*Intent*) của người dùng.
  - Prompt Generation khiến câu trả lời dài dòng, lan man hoặc lệch trọng tâm.

---

## 2. Phần 29: Tư duy thiết kế hệ thống theo xác suất (Probabilistic Design)

Sự khác biệt căn bản giữa phần mềm truyền thống và hệ thống AI:
- **Phần mềm truyền thống (Deterministic):** $\text{Input } A \longrightarrow \text{Output } B \text{ (100\% cố định)}$
- **Hệ thống AI / LLM (Probabilistic):**
$$\text{Input } A \longrightarrow \begin{cases} \text{Output } B & (80\%) \\ \text{Output } C & (15\%) \\ \text{Output } D & (5\%) \end{cases}$$

> 💡 **Tư duy cốt lõi:** Kỹ sư AI bắt buộc phải thiết kế hệ thống dự phòng cho sự bất định (**Design for Uncertainty**).

```
                           ┌──► Confidence > 90% ──► [ Tự động thực thi (Auto Action) ]
                           │
[ AI Prediction / Output ] ┼──► 60% ≤ Conf ≤ 90% ──► [ Hỏi lại để làm rõ (Clarification) ]
                           │
                           └──► Confidence < 60% ──► [ Chuyển người duyệt (Human-in-the-loop) ]
```

- **$\text{Confidence Score} > 0.90$:** Tự động thực thi hành động (*Automation*).
- **$0.60 \le \text{Confidence Score} \le 0.90$:** Yêu cầu người dùng xác nhận hoặc làm rõ ý định (*Ask clarification / Active prompt*).
- **$\text{Confidence Score} < 0.60$:** Chuyển luồng sang cho chuyên viên xử lý thủ công (*Human review / Fallback*).

---

## 3. Khung PRD cho AI Product: Chuyển từ Prototype sang Product

Một bản demo/prototype chạy được trên notebook không đồng nghĩa với một sản phẩm thương mại. Trước khi đưa vào sản xuất, bản **PRD (Product Requirements Document)** của dự án AI phải chứng minh được **4 trụ cột**:

| Trụ cột | Tiêu chí đánh giá | Câu hỏi cốt lõi |
| :--- | :--- | :--- |
| **Value** | Giá trị thực tế | Sản phẩm giải quyết bài toán gì? Giúp tiết kiệm bao nhiêu chi phí/thời gian cho người dùng? |
| **Usability** | Khả năng sử dụng | Giao diện và trải nghiệm (UX) xử lý độ trễ (*latency*) và lỗi xác suất của AI có mượt mà không? Người dùng có sẵn sàng dùng hàng ngày không? |
| **Feasibility** | Tính khả thi kỹ thuật | Model hiện tại có đáp ứng được yêu cầu về Latency, Compute Cost, chất lượng dữ liệu (*Data Quality*) và hạ tầng phần cứng không? |
| **Viability** | Tính bền vững kinh doanh | Chi phí token/hạ tầng vận hành có nhỏ hơn doanh thu/giá trị mang lại không? Có rủi ro pháp lý hay vi phạm đạo đức/bản quyền không? |

---

# 🛡️ XXXI & XXXII. Fallback, Human-in-the-Loop, Observability & Evaluation Dataset

## 1. Phần 31: Fallback & Giảm tải mềm (Graceful Degradation)

Hệ thống AI không được phép làm sập toàn bộ ứng dụng khi một thành phần gặp sự cố. **Graceful Degradation** là cơ chế tự động chuyển dịch qua các tầng dự phòng có độ phức tạp thấp hơn:

```
[ Complex Agent Loop ] ──(Lỗi / Timeout)──► [ RAG Pipeline ] ──(Retrieval Fail)──► [ Keyword Search (BM25) ] ──(Không tìm thấy)──► [ Safe Fallback Message + Handoff ]
```

### Ví dụ luồng Fallback đa tầng:
1. **Tầng 1 (Agent):** Gọi Agent tra cứu đa bước. Nếu quá timeout $\rightarrow$ Chuyển xuống Tầng 2.
2. **Tầng 2 (RAG):** Truy xuất Vector DB lấy context. Nếu Vector DB lỗi hoặc score quá thấp $\rightarrow$ Chuyển xuống Tầng 3.
3. **Tầng 3 (Rule/Keyword Search):** Tìm kiếm từ khóa truyền thống để lấy thông tin cơ bản.
4. **Tầng 4 (Safe Fallback):** Trả về thông báo an toàn: *"Hiện tại tôi chưa tìm thấy thông tin chính xác về phần này, bạn có muốn kết nối với tư vấn viên/tutor không?"*.

---

## 2. Mô hình Phê duyệt: Human-in-the-Loop (HITL)

Áp dụng mô hình **AI Propose $\rightarrow$ Human Review $\rightarrow$ Execute** cho các tác vụ quan trọng:

```
[ AI phân tích ] ──► [ Đánh giá Rủi ro & Độ tin cậy ]
                           │
                           ├──► [ Low Risk & High Confidence ] ──► [ Auto Execute ]
                           │
                           └──► [ High Risk / Low Confidence ] ──► [ Chuyển Human Review ]
                                                                           │
                                                                           ├── Approve (Duyệt)
                                                                           ├── Edit (Sửa)
                                                                           └── Reject (Hủy)
```

> ⚠️ **Lĩnh vực bắt buộc áp dụng HITL:** Y tế, Giáo dục (chấm điểm quyết định), Tài chính, Pháp lý, và các tác vụ có tính phá hủy (*Destructive actions* như xóa dữ liệu, thực hiện giao dịch chuyển tiền).

---

## 3. Phần 32: Giám sát Hệ thống (Observability & Tracing)

Không có Observability, kỹ sư hoàn toàn không thể debug một hệ thống AI trên Production.

### Cấu trúc dữ liệu một Trace Log chuẩn:
Khi người dùng báo lỗi (*"AI trả lời sai/ngu"*), hệ thống phải truy vết được chi tiết qua Request ID:

```json
{
  "request_id": "req_9981a_2026",
  "user_id": "usr_404",
  "user_query": "Giải thích quy tắc tính điểm bài thi tự luận",
  "detected_intent": "exam_grading_policy",
  "retrieval_trace": {
    "retrieved_chunks": ["chunk_12", "chunk_88"],
    "similarity_scores": [0.89, 0.42],
    "reranker_scores": [0.95, 0.12]
  },
  "prompt_payload": {
    "system_prompt_version": "v2.4.1",
    "injected_context_tokens": 1240
  },
  "execution_metrics": {
    "model_name": "gpt-4o-mini",
    "tool_calls": ["search_policy_db"],
    "latency_ms": 1450,
    "total_tokens": 1580
  },
  "output_response": "...",
  "user_feedback": "negative_thumbs_down",
  "error_type": null
}
```

---

## 4. Tập dữ liệu Đánh giá Chuẩn (Golden Evaluation Dataset)

**Golden Dataset** đóng vai trò như *Unit Test / Integration Test* cho hệ thống AI, giúp kiểm soát chất lượng (**Regression Testing**) mỗi khi cập nhật Prompt, Model, Chunk size hay Embedding.

### Cấu trúc một Test Case chuẩn (Quy mô: 100 – 500 cases):

| Trường thông tin | Ý nghĩa | Ví dụ kiểm thử |
| :--- | :--- | :--- |
| **Question** | Câu hỏi đầu vào | *"Điểm thi cuối kỳ dưới 4.0 có được thi lại không?"* |
| **Expected Intent** | Ý định cần nhận diện | `query_retake_policy` |
| **Expected Context** | Nguồn tài liệu bắt buộc phải trích | `[Handbook_2026.pdf, Section 4.2]` |
| **Expected Answer / Rubric** | Nội dung đúng trọng tâm | Phải nêu rõ sinh viên được thi lại tối đa 1 lần nếu vắng có phép. |
| **Allowed Tools** | Công cụ được phép gọi | `policy_search_api` |
| **Forbidden Behaviors** | Hành vi cấm (Guardrails) | Không được tự ý đưa ra ngoại lệ ngoài quy chế; không phán xét. |

> 💡 **Nguyên tắc triển khai:** Bất kỳ thay đổi nào về Prompt, Model, Reranker hay Chunking đều phải chạy qua bộ Golden Dataset để đo lại các chỉ số (*Groundedness, Latency, Accuracy*) trước khi Deploy Production.

---

# 🎓 XXXIV & XXXV. LLM-as-a-Judge, Vòng lặp Cải tiến Liên tục & Bản đồ Tư duy Kiến trúc AI Hoàn chỉnh

## 1. Phần 34: Đánh giá bằng LLM-as-a-Judge

Sử dụng một mô hình ngôn ngữ mạnh hơn (hoặc được tối ưu riêng cho việc chấm điểm) để tự động đánh giá đầu ra của hệ thống AI theo các tiêu chí và thang đo định lượng (*Rubrics*):

```
[ Question + Context + Generated Answer ] ──► [ LLM Judge ] ──► Chấm điểm: Groundedness (0.96), Relevance (0.94)
```

### Nguyên tắc triển khai:
1. **Không coi LLM-as-a-Judge là chân lý tuyệt đối (*Ground Truth*):** LLM Judge vẫn có thể mắc lỗi tự thiên vị (*Self-enhancement bias*), nhạy cảm với thứ tự đáp án (*Position bias*) hoặc bị ảo giác.
2. **Mô hình đánh giá 3 lớp (Tri-tier Evaluation):**

$$\text{Chất lượng đánh giá} = \text{Automated Metrics (ROUGE, BLEU, Exact Match)} + \text{LLM Judge} + \text{Human Expert Evaluation}$$

---

## 2. Phần 35: Vòng lặp Cải tiến Liên tục (Continuous Improvement Loop)

Trong kỹ thuật AI, quy trình triển khai không bao giờ kết thúc ở bước đóng gói và phát hành (*Build $\rightarrow$ Deploy $\rightarrow$ Done*). Hệ thống thực tế vận hành theo một chu trình khép kín:

$$\text{Production} \longrightarrow \text{Observability / Logs} \longrightarrow \text{User Feedback \& Errors} \longrightarrow \text{Update Golden Dataset} \longrightarrow \text{Improve System} \longrightarrow \text{Re-deploy}$$

---

## 3. Bản đồ Tư duy Kiến trúc AI Toàn diện (The Full Mindmap)

Dưới đây là khung quy trình **13 bước chuẩn hóa** từ khâu khám phá bài toán đến vận hành sản xuất:

```
1. DISCOVER
   └── What is the real problem? (Phỏng vấn, tìm pain points, workflow bottlenecks)
   ↓
2. DEFINE
   └── Problem Statement: Actor | Workflow | Bottleneck | Metric | Boundary
   ↓
3. DECIDE
   └── Does this actually need AI? (Fuzzy vs. Deterministic | Semantic vs. Rule-based)
   ↓
4. SELECT ARCHITECTURE
   ├── Level 1: Rule / Script (Validation, permissions, fixed business logic)
   ├── Level 2: Structured Workflow (State Machine, DAG, fixed pipelines)
   └── Level 3: Agentic System (Dynamic goals, unpredictable paths)
   ↓
5. BUILD AI FOUNDATION
   └── Core Mechanics: Tokenization → Embeddings → Self-Attention → Pre-training → SFT / RLHF
   ↓
6. BUILD KNOWLEDGE (Ingestion)
   └── Parsing → Chunking Strategy → Metadata Tagging → Embedding → Vector DB
   ↓
7. RETRIEVE
   └── Query Expansion / HyDE → Hybrid Search (Dense + BM25) → RRF → Cross-Encoder Rerank
   ↓
8. REASON / ACT
   └── LLM Reasoning → Tool Calling (Schema validation) → ReAct Loops → Memory Store
   ↓
9. GENERATE
   └── In-Context Grounding → Citations (Doc/Page/Chunk ID) → Graceful Degradation / Fallback
   ↓
10. CONTROL & SAFETY
    └── Guardrails → Confidence Thresholds → Human-in-the-Loop (HITL) → Security Permissions
    ↓
11. EVALUATE
    └── RAG Triad: Context Relevance | Groundedness / Faithfulness | Answer Relevance
    ↓
12. OBSERVE
    └── Trace Logs (Request ID, Chunks, Prompts, Latency, Token Usage, User Feedback)
    ↓
13. IMPROVE (Continuous Feedback Loop)
    └── Golden Dataset Expansion → LLM-as-a-Judge → Human Review → Regression Testing
    │
    └───────────────────────────── ↺ (Vòng lặp tiếp diễn liên tục)
```
