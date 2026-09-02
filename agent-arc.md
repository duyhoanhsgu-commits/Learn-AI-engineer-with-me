# 🧠 Multi-Agent Systems & Agentic Architectures

---

## 🌐 1. Bức tranh tổng thể

### 🧩 1.1. Tổng quan về Agentic AI

> [!NOTE]
> **Agentic AI** không đơn thuần là một LLM có khả năng gọi công cụ (*Tool Calling*). Đây là một **hệ thống kỹ thuật hoàn chỉnh** tích hợp khả năng suy luận, lưu trữ trạng thái, điều phối và kiểm soát an toàn.

```text
                        USER
                           │
                           ▼
                    ┌─────────────┐
                    │Agent/Router │
                    └──────┬──────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
        Reasoning        Memory         Tools
            │              │              │
            └──────────────┼──────────────┘
                           ▼
                     Orchestration
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Agents       Environment      RAG
             │
             └─────────────┬─────────────┘
                           ▼
                     Verification
                           │
                           ▼
                      Guardrails
                           │
                           ▼
                       Evaluation
                           │
                           ▼
                         OUTPUT
```

> [!IMPORTANT]
> **Công thức định danh Agentic AI:**
> $$\text{Agentic AI} = \text{Model} + \text{Reasoning} + \text{Tools} + \text{State} + \text{Memory} + \text{Planning} + \text{Orchestration} + \text{Control} + \text{Evaluation}$$

---

### 🏗️ 1.2. Vị trí của Multi-Agent trong Kiến trúc Tổng thể

📌 **Multi-Agent chỉ là một phần của hệ thống:** Không phải mọi bài toán phức tạp đều bắt buộc phải triển khai nhiều agent.

> [!TIP]
> **Quy tắc phân tầng phát triển (*Progressive Complexity*):**
> Luôn bắt đầu từ kiến trúc đơn giản nhất và chỉ nâng cấp khi hệ thống hiện tại không còn đáp ứng được yêu cầu về chất lượng hoặc khả năng mở rộng:
> $$\text{Single LLM} \longrightarrow \text{Workflow (Deterministic)} \longrightarrow \text{Single Agent (Tool Use)} \longrightarrow \text{Multi-Agent System}$$

#### 📊 Bảng so sánh các tầng kiến trúc

| Tầng kiến trúc | Bản chất | Khi nào áp dụng? |
| :--- | :--- | :--- |
| **🟢 1. Single LLM** | Prompt trực tiếp, zero-shot / few-shot | Tóm tắt, dịch thuật, biến đổi định dạng, hỏi đáp đơn giản |
| **🔵 2. Workflow** | Chuỗi xử lý cố định (DAG, State Machine) | Quy trình kinh doanh xác định rõ các bước và nhánh rẽ |
| **🟡 3. Single Agent** | Vòng lặp ReAct, tự chủ chọn tool | Bài toán tra cứu động, cần tự quyết định công cụ |
| **🟣 4. Multi-Agent** | Nhiều role chuyên biệt tương tác với nhau | Nhiệm vụ đa miền, cần cơ chế phản biện, review chéo |

> [!WARNING]
> **Nguyên tắc kỹ thuật cốt lõi:** *"Chỉ tăng độ phức tạp khi tầng trước không còn đáp ứng được yêu cầu."*
> Tránh bẫy **Over-engineering** khiến hệ thống tăng độ trễ, tốn chi phí token và gây khó khăn khi debug.

---

## 🎯 2. Learning trong Agentic AI — Bản chất, Vận hành & Định vị Bài toán

### ⚡ 2.1. Phân cấp Khả năng Tự quyết: Rule-based $\rightarrow$ Chatbot $\rightarrow$ Agent

Hệ thống xử lý thông tin được chia thành 3 cấp độ tăng dần về tính tự chủ (*Autonomy*):

```text
[ Cấp 1: Rule-based ] ──► [ Cấp 2: Standard Chatbot ] ──► [ Cấp 3: AI Agent ]
 (Deterministic Rules)         (Direct Generation)          (Dynamic Goal-Seeking)
```

#### 🔹 2.1.1. Rule-based System (Hệ thống quy tắc cố định)

- **Luồng xử lý:** $$\text{Input} \longrightarrow \text{Rule} \longrightarrow \text{Action} \longrightarrow \text{Output}$$
- **Ví dụ:** Nếu `intent == "weather"` $\rightarrow$ gọi Weather API; nếu `intent == "booking"` $\rightarrow$ kích hoạt Booking Flow.
- **Đặc điểm:** Tất định (*Deterministic*), phản hồi nhanh, chi phí tính toán tối thiểu, dễ viết kiểm thử.
- **Hạn chế:** Chỉ xử lý được các trường hợp ngoại lệ mà kỹ sư đã dự đoán và cấu hình từ trước.

#### 🔹 2.1.2. Standard Chatbot (Mô hình hội thoại thụ động)

- **Luồng xử lý:** $$\text{User Prompt} \longrightarrow \text{LLM Reasoning} \longrightarrow \text{Answer}$$
- **Ví dụ:** Người dùng yêu cầu *"Explain RAG"* $\rightarrow$ LLM suy luận và xuất ra định nghĩa *"RAG stands for Retrieval-Augmented Generation..."*.
- **Đặc điểm:** Xử lý ngôn ngữ tự nhiên tốt nhưng mang tính thụ động, chỉ biến đổi văn bản đầu vào thành văn bản đầu ra mà chưa có khả năng trực tiếp tương tác hay thay đổi môi trường bên ngoài.

#### 🔹 2.1.3. AI Agent (Hệ thống hướng mục tiêu chủ động)

- **Luồng xử lý:** $$\text{Goal} \longrightarrow \text{Understand} \longrightarrow \text{Reason} \longrightarrow \text{Tool / Action} \longrightarrow \text{Observe} \longrightarrow \text{Decide Next Step} \longrightarrow \text{Final Output}$$
- **Ví dụ:** *"Nghiên cứu bài báo Attention Is All You Need và tóm tắt đóng góp chính"*.
- **Chuỗi hành động tự sinh:** $\text{Search Paper} \rightarrow \text{Find Original Source} \rightarrow \text{Read PDF} \rightarrow \text{Extract Architecture} \rightarrow \text{Analyze Attention Mechanics} \rightarrow \text{Compare Claims} \rightarrow \text{Write Report} \rightarrow \text{Verify Citation}$.

> [!NOTE]
> **Bản chất cốt lõi của Agentic Behavior:** Mô hình không cần biết toàn bộ đường đi ngay từ đầu. Nó quan sát kết quả trung gian từ môi trường để tự điều chỉnh và quyết định bước tiếp theo.

---

### 🔄 2.2. Mô hình Nền tảng: ReAct Framework (Reasoning + Acting)

ReAct kết hợp chặt chẽ giữa khả năng suy luận logic (*Reasoning*) và hành động gọi công cụ (*Acting*).

```text
┌────────────────────────────────────────────────────────┐
▼                                                        │
[ State: S_t ] ──► [ Reason ] ──► [ Action: A_t ] ──► [ Observation: O_t ] ──► [ State: S_{t+1} ]
                                                         │
                                                         └── (Đạt mục tiêu) ──► [ Final Answer ]
```

> [!IMPORTANT]
> **Chuỗi trạng thái toán học:** Quá trình thực thi diễn ra theo chuỗi liên tục:
> $$(S_t, A_t, O_t) \longrightarrow S_{t+1}$$
> - $S_t$: Trạng thái ngữ cảnh tại bước $t$.
> - $A_t$: Hành động cụ thể được model lựa chọn thực thi.
> - $O_t$: Dữ liệu quan sát thu được từ môi trường sau khi chạy $A_t$.
> - $S_{t+1}$: Trạng thái cập nhật mới sau khi tích lũy quan sát $O_t$.

#### 💡 Ví dụ luồng ReAct: *"Tìm và so sánh 3 phương pháp Retrieval trong RAG"*

1. **Goal:** Cần tài liệu so sánh retrieval.
2. **Action 1:** `search_papers(query="RAG retrieval methods comparison")`
3. **Observation 1:** Tìm thấy 10 bài báo; cần thông tin chi tiết về kiến trúc.
4. **Action 2:** `read_paper(id="paper_01")`
5. **Observation 2:** Đã trích xuất phần Retrieval; cần dữ liệu định lượng để so sánh.
6. **Action 3:** `compile_comparison_matrix(data=...)`
7. **Observation 3:** Hoàn tất bảng số liệu $\rightarrow$ Xuất **Final Answer**.

---

### 📐 2.3. Khung Đánh giá Bài toán: Agentic Fit Framework

Không phải tác vụ nào cũng cần đến Agent. Sử dụng bộ khung 4 chiều **R-T-D-H** để đánh giá tính khả thi:

| Yếu tố | Mức độ Thấp (Low Fit) | Mức độ Cao (High Fit) |
| :--- | :--- | :--- |
| **🧠 Reasoning** *(Mức độ suy luận)* | Phép tính cố định ($2 + 2$), phân loại nhị phân cơ bản. | Nghiên cứu tài liệu, đối chiếu mâu thuẫn dữ liệu, tổng hợp luận điểm đa chiều. |
| **🛠️ Tools** *(Tương tác môi trường)* | Không dùng tool hoặc chỉ đọc context cố định có sẵn. | Tương tác liên tục với Web Search, Database, GitHub API, Calendar, Python Sandbox, Vector DB. |
| **🎲 Decision** *(Quyền tự quyết bước tiếp theo)* | Luồng tĩnh, rẽ nhánh cố định (`if-else` biết trước). | Phân tích kết quả trung gian để chọn: tìm kiếm tiếp, tính toán lại, hỏi người dùng, gọi sub-agent, hoặc dừng lại. |
| **⏳ Horizon** *(Độ dài chuỗi hành động)* | Ngắn (Dịch 1 câu, tóm tắt 1 đoạn văn). | Dài (Thu thập báo cáo tài chính $\rightarrow$ phân tích đối thủ $\rightarrow$ quét rủi ro $\rightarrow$ xác thực nguồn $\rightarrow$ xuất báo cáo). |

> [!TIP]
> **Công thức Agentic Fit Index:**
> $$\text{Khả năng phù hợp với Agent} \propto \text{Reasoning} + \text{Tools} + \text{Decision} + \text{Horizon}$$

---

### 🔄 2.4. Chuyển dịch Tư duy: Model-Centric vs. System-Centric

Sự khác biệt mang tính bước ngoặt giữa kỹ thuật Prompt truyền thống và Kỹ thuật Hệ thống Agentic AI:

```text
[ Model-Centric ]
User Prompt ──────────► [ Big Foundation Model ] ──────────► Response

[ System-Centric ]
                         ┌───────────────────────────────────────────────────────────┐
                         │ Orchestrator / State Machine                              │
User Request ──► Guardrails ──► [ LLM ] ◄──► [ Memory ] ◄──► [ Tools / RAG ] ──► Guardrails ──► Output
                         │       ▲                                                   │
                         │       └──────── Tracing / Observability / Eval ───────────┘
```

| Góc nhìn | Tư duy Cũ (Model-Centric) | Tư duy Mới (System-Centric) |
| :--- | :--- | :--- |
| **Cấu trúc** | $\text{Prompt} \rightarrow \text{LLM} \rightarrow \text{Output}$ | Đặt LLM làm nhân xử lý suy luận bên trong một hệ sinh thái tích hợp (*Orchestrator, Tools, Memory, RAG, Verification, Guardrails, Observability*). |
| **Câu hỏi trọng tâm** | *"Model nào có điểm benchmark cao nhất, thông minh nhất?"* | *"Hệ thống tổng thể có giải quyết được bài toán một cách chính xác, an toàn, ổn định, độ trễ thấp với chi phí tối ưu hay không?"* |

---

## 🛠️ 3. Các Mẫu Thiết Kế Quy Trình (Agentic Workflow Patterns)

### 🚀 3.1. Bản chất của Agentic Workflows

> [!NOTE]
> Trước khi xây dựng một hệ thống Agent phức tạp, kỹ sư cần nắm vững cách tổ chức luồng xử lý (*workflow orchestration*). Không phải bài toán nào cũng cần thả cho LLM tự do hành động; việc áp dụng đúng mẫu thiết kế giúp **kiểm soát chi phí**, **giảm độ trễ** và **triệt tiêu lỗi suy diễn**.

**5 mẫu hình cốt lõi gồm:**
1. **Prompt Chaining** (Chuỗi mệnh lệnh tuần tự)
2. **Routing** (Bộ định tuyến luồng)
3. **Parallelization** (Xử lý song song: Sectioning & Voting)
4. **Orchestrator-Workers** (Điều phối - Thực thi động)
5. **Evaluator-Optimizer** (Tự đánh giá & Tối ưu)

---

### ⚙️ 3.2. Chi tiết 5 Mẫu Thiết Kế Cốt Lõi

#### 🔗 Pattern 1: Prompt Chaining (Chuỗi Mệnh Lệnh Tuần Tự)

Tác vụ phức tạp được chia nhỏ thành một chuỗi các bước tuần tự, đầu ra của bước trước là đầu vào của bước sau.

```text
[ Input ] ──► [ LLM 1 ] ──► [ LLM 2 ] ──► [ LLM 3 ] ──► [ Output ]
```

- **Ví dụ luồng xử lý văn bản:** $$\text{Document} \longrightarrow \text{Summarize} \longrightarrow \text{Extract Concepts} \longrightarrow \text{Generate Questions} \longrightarrow \text{Generate Answers}$$
- **Đặc tính kỹ thuật:** Đường đi hoàn toàn cố định và biết trước (*deterministic pipeline*). Không cần Agent tự chủ để tránh lãng phí tài nguyên.

---

#### 🔀 Pattern 2: Routing (Bộ Định Tuyến Luồng)

Router phân tích câu hỏi người dùng và quyết định chuyển hướng (*dispatch*) yêu cầu đến module chuyên trách phù hợp.

```text
                             ┌──► [ RAG Agent / Research ]
                             │
[ User Prompt ] ──► [ Router ] ┼──► [ Coding Agent ]
                             │
                             └──► [ Booking Workflow ]
```

- **Cơ chế Router:** Có thể dùng Rule-based (regex, keyword) hoặc LLM Classifier xuất dữ liệu có cấu trúc (*Structured Outputs*):
  ```json
  {
    "intent": "research",
    "confidence": 0.94
  }
  ```
- **Quy tắc điều phối:**
  - Nếu `intent == "research"` $\longrightarrow$ Gọi RAG Agent.
  - Nếu `intent == "code"` $\longrightarrow$ Gọi Coding Agent.
  - Nếu `intent == "booking"` $\longrightarrow$ Kích hoạt Booking Workflow.
- **Trường hợp áp dụng:** Hệ thống lớn có nhiều năng lực độc lập (*capabilities*), tránh việc nhồi nhét tất cả tool vào một LLM duy nhất.

---

#### ⚡ Pattern 3: Parallelization (Xử Lý Song Song)

Chia các tác vụ độc lập để chạy đồng thời nhằm tối ưu hóa thời gian xử lý và độ chính xác.

```text
[ Sequential: Tuần tự ]
Task A (10s) ──► Task B (10s) ──► Task C (10s)  ===>  Tổng Latency ≈ 30s

[ Parallel: Song song ]
                 ┌──► Task A (8s)  ──┐
[ Orchestrator ] ┼──► Task B (12s) ──┼──► [ Aggregator ]  ===>  Tổng Latency ≈ max(A, B, C) ≈ 12s
                 └──► Task C (10s) ──┘
```

Mẫu này chia thành 2 biến thể chính:

##### 🧩 3.2.1. Sectioning (Chia nhỏ theo chiều rộng)
- **Bản chất:** Tách một bài toán lớn thành các khía cạnh phân tích độc lập, sau đó tổng hợp lại (*Synthesis*).
- **Ví dụ:** Một bài toán nghiên cứu tổng hợp được chia song song cho: Module khai thác Memory, Module gọi Tool, Module phân tích Planning $\longrightarrow$ Ghép lại ở bước Synthesis.
- **Lợi ích:** Tăng độ bao phủ (*Coverage*), giảm tải ngữ cảnh cho từng lần gọi.

##### 🗳️ 3.2.2. Voting / Self-Consistency (Bỏ phiếu số đông)
- **Bản chất:** Cho nhiều mô hình hoặc nhiều agent giải quyết cùng một bài toán một cách độc lập, sau đó tổng hợp kết quả theo nguyên tắc đa số.
- **Ví dụ:** Cùng một câu hỏi toán, Agent A trả về $\sin(x)$, Agent B trả về $\sin(x)$, Agent C trả về $\cos(x) \longrightarrow$ Kết quả cuối cùng chọn $\sin(x)$.
- **Lợi ích:** Tăng tính xác thực (*Verification*), giảm thiểu rủi ro ảo giác ngẫu nhiên.

---

#### 🎼 Pattern 4: Orchestrator-Workers (Điều Phối - Thực Thi Động)

Mẫu hình nâng cao của Parallelization. Khác với Sectioning cố định bằng code, Orchestrator là một LLM có quyền tự quyết định chia nhỏ bài toán theo cách nó muốn.

```text
                       ┌──► Worker 1 (Dynamic Task A) ──┐
                       │                                │
[ Goal ] ──► [ Orchestrator ] ──┼──► Worker 2 (Dynamic Task B) ──┼──► [ Synthesis ] ──► [ Final Output ]
  (LLM)                │                                │
                       └──► Worker 3 (Dynamic Task C) ──┘
```

- **Cơ chế vận hành:** Orchestrator tự động:
  1. Phân tích Goal và quyết định cần chia thành bao nhiêu sub-tasks.
  2. Khởi tạo số lượng worker tương ứng.
  3. Giao việc cụ thể cho từng worker.
  4. Thu thập toàn bộ kết quả trung gian để tổng hợp thành câu trả lời cuối cùng.
- **Ví dụ (Research Agent Architecture):** Orchestrator tự động phân rã thành: Worker 1 (Short-term memory), Worker 2 (Long-term memory), Worker 3 (Episodic memory), Worker 4 (Frameworks), Worker 5 (Evaluation) $\longrightarrow$ Synthesis.
- **Điểm khác biệt cốt lõi:** Quá trình phân rã (*Task Decomposition*) diễn ra động (*Dynamic*) dựa trên ngữ cảnh thực tế, không bị trói buộc bởi luồng code cứng.

---

#### 🔄 Pattern 5: Evaluator-Optimizer (Tự Đánh Giá & Tối Ưu)

Mô hình vòng lặp gồm một Agent đóng vai trò tạo nội dung (*Generator*) và một Agent đóng vai trò kiểm duyệt (*Evaluator*).

```text
                      ┌────────────────────────────────────────┐
                      ▼                                        │ Fail (Kèm Feedback)
[ Prompt ] ──► [ Generator ] ──► Draft ──► [ Evaluator ] ──────┤
                                                │
                                                └── Pass (Score ≥ Threshold) ──► [ Finish / Output ]
```

- **Ví dụ luồng viết bài báo (Article Writing):**
  1. Generator viết bản nháp Article v1.
  2. Evaluator chấm điểm chất lượng theo Rubrics: $\text{Groundedness} = 0.72, \text{Citation} = 0.80, \text{Completeness} = 0.61$.
  3. Điểm chưa đạt yêu cầu $\longrightarrow$ Evaluator xuất Feedback chi tiết.
  4. Generator đọc Feedback và sinh bản nháp cải tiến Article v2.

> [!IMPORTANT]
> **Điều kiện dừng bắt buộc (*Termination Criteria*):**
> Vòng lặp phải dừng lại khi thỏa mãn một trong hai điều kiện:
> 1. **Chất lượng đạt chuẩn:** $\text{Score} \ge \text{Threshold}$
> 2. **Chạm giới hạn vòng lặp:** $\text{Iteration} \ge \text{Max Iterations}$

> [!WARNING]
> **Quy tắc an toàn:** Luôn thiết lập giới hạn `max_iterations` (thường từ 2 – 3 vòng) để triệt tiêu nguy cơ rơi vào vòng lặp vô tận (*Infinite Loop*) làm cạn kiệt ngân sách token và tăng vọt độ trễ.

---

### 📊 3.3. Bảng Tổng Hợp So Sánh 5 Mẫu Thiết Kế

| Mẫu thiết kế | Quyết định đường đi | Độ phức tạp | Tác động chính |
| :--- | :--- | :--- | :--- |
| **🔗 Prompt Chaining** | Tuyến tính, cố định | 🟢 Thấp | Tách nhỏ bài toán phức tạp thành các bước dễ quản lý |
| **🔀 Routing** | Phân nhánh dựa trên ý định | 🟢 Thấp – Vừa | Giảm tải token, điều phối chính xác chuyên môn |
| **⚡ Parallelization** | Đồng thời (Sectioning / Voting) | 🟡 Vừa | Giảm độ trễ tổng thể, tăng độ tin cậy kết quả |
| **🎼 Orchestrator-Workers** | LLM tự phân rã động | 🔴 Cao | Giải quyết các tác vụ mở, phạm vi thay đổi linh hoạt |
| **🔄 Evaluator-Optimizer** | Vòng lặp phản hồi có điều kiện | 🔴 Cao | Tối đa hóa chất lượng đầu ra, tự sửa sai (*Self-correction*) |

---

## 🤝 4. Hệ Thống Đa Tác Tử (Multi-Agent Systems - MAS)

### 🎯 4.1. Tại sao cần nhiều Agent? — Nguyên lý Chia để trị (Divide and Conquer)

Khi hệ thống phát triển đủ lớn, nếu dồn toàn bộ tác vụ cho một Agent duy nhất (*Single Agent*), hệ thống sẽ gặp các điểm nghẽn nghiêm trọng:
- **Prompt bloat:** System prompt quá dài, dễ khiến mô hình mất tập trung (*lost-in-the-middle*).
- **Quá tải công cụ (*Tool saturation*):** Cung cấp hàng chục tools cùng lúc làm giảm độ chính xác khi chọn hàm (*Function Calling accuracy*).
- **Ô nhiễm ngữ cảnh (*Context contamination*):** Trộn lẫn kết quả tìm kiếm thô, mã lỗi thực thi và văn bản phân tích trong cùng một context window.
- **Khó cô lập lỗi:** Khi kết quả sai, rất khó debug xem lỗi do khâu tìm kiếm, tính toán hay khâu hành văn.

```text
[ Vấn đề của Single Agent ]
User Goal ──► [ Single God Agent ] ──► (Gánh: Search + Read + Analyze + Calculate + Fact-check + Write)
              └── Rủi ro: Prompt quá dài, Tool quá nhiều, Dễ lú, Debug cực khó

[ Giải pháp Chia để trị (Multi-Agent) ]
User Goal ──► [ Manager / Orchestrator ]
                     ├──► Researcher  (Chỉ Search, Read)    ── [ Context & Tools hẹp ]
                     ├──► Analyst     (Chỉ Code, Calculate) ── [ Context & Tools hẹp ]
                     └──► Writer      (Chỉ Tổng hợp, Báo cáo) ── [ Không cần external tools ]
```

> [!NOTE]
> **Nguyên tắc cốt lõi:** Mỗi Agent chỉ nhận đúng tập Context tối thiểu và bộ Tools thực sự cần thiết để hoàn thành nhiệm vụ được giao.

---

### 🛠️ 4.2. Chuyên môn hóa (Specialization)

Mỗi Agent đảm nhận một vai trò duy nhất (*Single Responsibility Principle*), được trang bị System Prompt chuyên sâu và bộ công cụ riêng biệt.

#### 💡 Case Study: Đội ngũ Kỹ sư Phần mềm (Software Engineering Team)

| Agent Role | Trách nhiệm chính | Bộ Tools được cấp | Lợi ích đạt được |
| :--- | :--- | :--- | :--- |
| **💻 Developer** | Hiện thực hóa mã nguồn (*Implement code*) | `code_repository`, `code_editor`, `compiler` | Prompt ngắn gọn, tập trung cú pháp và logic thuật toán. |
| **🧪 Tester** | Chạy kiểm thử tự động, bắt lỗi (*Test & QA*) | `pytest_runner`, `test_database`, `log_viewer` | Không bị phân tâm bởi việc viết code tính năng, chỉ soi lỗi. |
| **🔍 Reviewer** | Thẩm định chuẩn mực code (*Code Inspection*) | `pr_diff_reader`, `static_code_analyzer` | Đảm bảo tính bảo mật, hiệu năng và kiến trúc chuẩn. |

> [!IMPORTANT]
> **Công thức tối ưu hiệu năng:**
> $$\text{Prompt nhỏ hơn} + \text{Tool ít hơn} + \text{Context sạch hơn} \Longrightarrow \text{Độ chính xác cao hơn, Dễ debug hơn}$$

---

### ⚖️ 4.3. Mẫu Phản biện & Đánh giá (Pro, Con & Judge / Debate Pattern)

Áp dụng cơ chế tranh biện đa chiều nhằm tối ưu hóa các quyết định phức tạp, hạn chế góc nhìn phiến diện hoặc thiên vị (*confirmation bias*) của một mô hình đơn lẻ.

```text
                     ┌──► [ Pro Agent / Advocate ]   (Phân tích mặt lợi, cơ hội) ──┐
[ Question / Dilemma ]┤                                                             ├──► [ Judge Agent ] ──► [ Final Decision ]
                     └──► [ Opponent / Critic Agent ] (Bóc tách rủi ro, nhược điểm) ──┘
```

#### 📌 Ví dụ thực tế: *"Doanh nghiệp có nên triển khai GraphRAG thay cho Vector RAG truyền thống?"*
- **Pro Agent:** Chỉ ra lợi thế vượt trội của GraphRAG trong việc nối kết các thực thể quan hệ xa (*multi-hop reasoning*) và tính giải thích rõ ràng.
- **Opponent Agent:** Cảnh báo về chi phí xây dựng Knowledge Graph cực lớn, độ trễ truy vấn cao và sự phức tạp khi bảo trì pipeline.
- **Judge Agent:** Đọc toàn bộ lập luận của hai bên, cân đối với nguồn lực hiện tại của doanh nghiệp để đưa ra kết luận cuối cùng.

> [!TIP]
> **Trường hợp áp dụng:** Ra quyết định kiến trúc (*Architectural Decisions*), Tư duy phản biện (*Critical Thinking*), Đánh giá rủi ro (*Risk Assessment*), Thẩm định thông tin (*Fact-checking Verification*).

---

### ⚡ 4.4. Nghiên cứu Song song (Parallel Multi-Agent Research)

Khi cần tổng hợp thông tin từ nhiều thực thể độc lập, mô hình phân tán các Sub-agent chạy song song giúp mở rộng độ phủ và giảm thiểu thời gian chờ.

```text
                       ┌──► Researcher A (Khảo sát LangGraph) ──┐
                       │                                        │
[ Request: So sánh ] ──┼──► Researcher B (Khảo sát CrewAI)    ──┼──► [ Analyst / Synthesis ] ──► [ Final Report ]
                       │                                        │
                       └──► Researcher C (Khảo sát AutoGen)   ──┘
```

- **Cơ chế:** Manager tạo ra 3 Agent chạy độc lập cùng lúc để đào sâu từng framework, sau đó Analyst tổng hợp các báo cáo con thành một bảng so sánh toàn diện.
- **Lợi ích kép:**
  - **Tăng Coverage (Độ bao phủ):** Mỗi agent có đủ context window để đọc sâu tài liệu của từng thư viện.
  - **Giảm Latency (Độ trễ):** Thời gian thu thập thông tin tính theo $\max(T_A, T_B, T_C)$ thay vì $T_A + T_B + T_C$.

---

### 🔄 4.5. Vòng lặp Phản hồi Khép kín (Closed Feedback Loop)

Hệ thống Agentic không hoạt động theo kiểu một chiều $\text{Input} \longrightarrow \text{Output}$, mà vận hành dựa trên cơ chế tự sửa sai qua thực nghiệm:

$$\text{Plan} \longrightarrow \text{Execute} \longrightarrow \text{Evaluate} \longrightarrow \begin{cases} \text{Đạt chuẩn (Pass)} & \longrightarrow \text{Finish} \\ \text{Lỗi (Fail)} & \longrightarrow \text{Improve Plan} \longrightarrow \text{Execute lại} \end{cases}$$

```text
                   ┌────────────────────────────────────────────────────────┐
                   ▼                                                        │
[ Generate Code ] ──► [ Run Pytest ] ──► [ 5 Tests Failed ] ──► [ Analyze Failure & Modify ]
                                               │
                                               └──► (0 Tests Failed) ──► [ Finish / Merge PR ]
```

- **Ví dụ Coding Agent:**
  1. Generator sinh mã nguồn.
  2. Executor chạy kiểm thử tự động $\longrightarrow$ phát hiện 5 test case bị fail.
  3. Evaluator/Analyst phân tích nguyên nhân lỗi dựa trên stack trace và logs.
  4. Generator viết lại mã nguồn dựa trên phản hồi $\longrightarrow$ Chạy lại kiểm thử cho đến khi pass toàn bộ.

---

### ⚠️ 4.6. Khi nào KHÔNG NÊN dùng Multi-Agent? (Anti-patterns & Hidden Costs)

> [!CAUTION]
> **Multi-Agent không phải là "viên đạn bạc".** Việc lạm dụng Multi-Agent mà không có lý do kiến trúc rõ ràng sẽ tạo ra gánh nặng lớn:

```text
[ Anti-Pattern: Over-engineering ]
User: "Tóm tắt file PDF này" 
  └── Rơi vào ma trận: Router ──► Planner ──► Researcher ──► RAG Agent ──► Analyst ──► Writer ──► Retriever 
      (Lãng phí tài nguyên khủng khiếp)
```

#### 💸 Các chi phí ẩn và rủi ro:
- **Token Cost bùng nổ:** Dữ liệu context phải đóng gói, truyền qua lại giữa các Agent ($A \rightarrow B \rightarrow C$) làm nhân số lượng token lên nhiều lần.
- **Độ trễ tăng cao (*Latency Spike*):** Mỗi bước handoff giữa các Agent đều tốn thời gian mạng và thời gian chờ model suy luận.
- **Giao tiếp cồng kềnh (*Coordination Overhead*):** Tốn logic xử lý định dạng trao đổi, phân giải tranh chấp khi các Agent đưa ra ý kiến mâu thuẫn (*Conflicting Decisions*).
- **Mất mát ngữ cảnh (*Context Loss*):** Qua nhiều tầng tóm tắt và chuyển tiếp giữa các Agent, thông tin chi tiết ban đầu rất dễ bị biến dạng hoặc rơi rụng.
- **Nhiều điểm lỗi hơn (*Cascading Failure*):** Càng nhiều Agent in chuỗi, xác suất một mắt xích gặp lỗi, rơi vào vòng lặp hoặc sinh ảo giác càng lớn.

> [!WARNING]
> **Quy tắc thiết kế bất biến:**
> Nếu một bài toán có thể giải quyết tốt bằng Prompting đơn lẻ, một chuỗi Workflow tĩnh hoặc Single Agent với vài tools, **tuyệt đối không dùng Multi-Agent**. Chỉ sử dụng Multi-Agent khi cần giải quyết một điểm nghẽn cụ thể về phân tách trách nhiệm, context window hoặc chuyên môn hóa sâu.

---

## 🚀 5. Kiến Trúc Agent Nâng Cao (Advanced Agent Architectures)

### 📋 5.1. Mẫu Kiến trúc Plan — Act — Verify

Trong khi ReAct đưa ra quyết định ngắn hạn theo kiểu phản xạ từng bước đơn lẻ (*step-by-step reaction*), mẫu hình Plan — Act — Verify tiếp cận bài toán bằng việc lập chiến lược tổng thể từ trước:

```text
                  ┌──────────────────────────────────────────────────┐
                  ▼                                                  │ No (Re-plan / Bổ sung)
[ Goal ] ──► [ Plan ] ──► [ Act ] ──► [ Output ] ──► [ Verify ] ─────┤
             (1, 2, 3, 4)  (Thực thi)                 (Kiểm định)    │
                                                                     └── Yes ──► [ Finish ]
```

#### 💡 Case Study Nghiên cứu:
- **Goal:** Nghiên cứu kiến trúc mô hình Transformer.
- **Initial Plan:**
  1. Tìm bài báo gốc (*Attention Is All You Need*).
  2. Định danh các thành phần kiến trúc cốt lõi.
  3. Bóc tách cơ chế Scaled Dot-Product và Multi-Head Attention.
  4. Phân tích đóng góp khoa học chính.
  5. Đối chiếu, so sánh với các mô hình tuần tự trước đó (RNN, LSTM).
- **Act:** Agent tiến hành thực thi và tạo bản báo cáo tổng hợp.
- **Verify:** Bộ kiểm định rà soát nội dung và phát hiện: *"Luận điểm 4 (Claim 4) không có trích dẫn minh chứng thực tế"*.
- **Re-plan / Dynamic Adjustment:** Kế hoạch không phải là bất biến. Verifier điều phối lại Planner chèn thêm một nhiệm vụ phụ: *"Tìm kiếm tài liệu minh chứng cho Claim 4"* trước khi xuất bản kết quả cuối cùng.

---

### 🔍 5.2. Phân biệt: Verification vs. Reflection

Hai cơ chế đánh giá này vận hành ở hai tầng trừu tượng khác nhau:

```text
[ Quá trình thực thi (Process / Strategy) ] ──────────► [ Kết quả đầu ra (Result / Output) ]
                     ▲                                                    ▲
                     │                                                    │
            [ Reflection soi vào ]                               [ Verification soi vào ]
      "Tại sao cách làm chưa hiệu quả?"                        "Kết quả này có đúng không?"
```

| Tiêu chí | Verification (Kiểm định) | Reflection (Phản tỉnh / Tự chiêm nghiệm) |
| :--- | :--- | :--- |
| **Đối tượng soi chiếu** | Kết quả (*Result / Output*) | Quy trình & Chiến lược (*Process / Strategy*) |
| **Câu hỏi cốt lõi** | *"Kết quả đầu ra có chính xác và hợp lệ không?"* | *"Tại sao chiến lược vừa rồi thất bại hoặc kém tối ưu?"* |
| **Ví dụ thực tế** | Kiểm tra xem bài viết có chứa câu khẳng định nào thiếu nguồn dẫn chứng (*unsupported claim*) hay không. | Phân tích thất bại: *"Lần trước tìm kiếm từ khóa chung chung dẫn đến quá nhiều kết quả rác. Lần tới cần trích xuất tên tác giả và năm trước khi search."* |
| **Hành động tiếp theo** | Duyệt qua (*Pass*) hoặc Từ chối (*Fail*). | Cập nhật lại heuristic, chiến lược hoặc tinh chỉnh prompt cho lần chạy sau. |

> [!NOTE]
> **Quy tắc ngắn gọn:** **Verification** kiểm tra kết quả, còn **Reflection** mổ xẻ quy trình.

---

### 📚 5.3. Tích lũy Kỹ năng (Skill Accumulation)

Agent không nhất thiết phải suy luận mọi thứ lại từ đầu (*from scratch*) cho các tác vụ lặp lại. Thay vào đó, nó tích lũy một thư viện kỹ năng tái sử dụng được (*Skill Library*).

```text
                      ┌──► [ Skill: Research Paper ]
                      ├──► [ Skill: Analyze GitHub Repo ]
[ Task Mới ] ──► [ Skill Retrieval ] ┼──► [ Skill: Debug FastAPI ] ──► [ Load Context & Run ]
                      ├──► [ Skill: Write Unit Test ]
                      └──► [ Skill: Generate Architecture ]
```

#### 📦 Cấu trúc một Skill chuẩn đóng gói:
- **Instructions / System Prompt:** Hướng dẫn chi tiết cách tư duy chuyên môn.
- **Workflow:** Quy trình từng bước chuẩn hóa.
- **Dedicated Tools:** Danh sách các công cụ chuyên biệt gán với kỹ năng đó.
- **Few-shot Examples:** Các mẫu input-output chuẩn mực để mô hình noi theo.
- **Constraints & Guardrails:** Giới hạn những điều cấm kỵ khi thực thi.

📌 Khi gặp bài toán mới, Agent chỉ cần thực hiện **Skill Retrieval** để nạp gói kỹ năng phù hợp vào Context, tiết kiệm đáng kể thời gian suy luận và hạn chế lỗi ngẫu nhiên.

---

### 🧬 5.4. Cơ chế Tự tiến hóa (Self-Evolution Agent) & An toàn Vận hành

#### 🔄 Vòng lặp học tập từ kinh nghiệm:
$$\text{Experience} \longrightarrow \text{Evaluation} \longrightarrow \text{Reflection} \longrightarrow \text{Extract Strategy} \longrightarrow \text{Store Skill} \longrightarrow \text{Apply to Future Tasks}$$

*Ví dụ:* Sau 100 phiên xử lý, hệ thống gom nhật ký (*logs*), phân tích các chiến lược xử lý thành công, đúc kết thành các pattern tối ưu hơn và đề xuất cập nhật chiến lược nghiên cứu mới.

#### 🛡️ Ranh giới an toàn trong Môi trường Production:

> [!CAUTION]
> Tuyệt đối **không cho phép Agent tự động sửa đổi mã nguồn/prompt** rồi tự triển khai trực tiếp (*Self-modifying & Auto-deploy*) lên hệ thống đang chạy.

```text
[ Nghiệm thu Nguy hiểm (Anti-Pattern) ]
Agent rút kinh nghiệm ──► Tự sửa Prompt/Code ──► Auto Deploy Production (Rủi ro sập hệ thống / Drift)

[ Pipeline Tiến hóa An toàn (Production Standard) ]
Agent rút kinh nghiệm ──► Đề xuất (Proposal) ──► Offline Evaluation ──► Human Approval ──► CI/CD Deploy
```

---

### ⚙️ 5.5. Kỹ thuật Ngữ cảnh (Context Engineering)

Point cốt lõi của Agentic AI không chỉ dừng lại ở việc viết prompt thật dài, mà nằm ở câu hỏi: *"Mô hình đang nhìn thấy chính xác những thông tin gì tại thời điểm đưa ra quyết định?"*

#### 🧩 5.5.1. Bức tranh Context đầy đủ
Context thực tế được cấu thành từ nhiều mảnh ghép:
1. **System Instruction** (Vai trò, quy tắc cốt lõi).
2. **User Request** (Mục tiêu ban đầu).
3. **Conversation Memory** (Lịch sử hội thoại liên quan).
4. **Retrieved Documents** (Tài liệu từ RAG).
5. **Tool Execution Results** (Dữ liệu trả về từ API/Database).
6. **Current Plan & Current State** (Vị trí hiện tại trong kế hoạch tổng).
7. **Prior Errors & Retries** (Mã lỗi từ lần thử trước).
8. **Handoff Data from Other Agents** (Dữ liệu bàn giao từ agent khác).

#### ⚠️ 5.5.2. Sai lầm kinh điển: "Nhồi nhét tất cả vào một Context" (*Everything into Context*)
- **Hậu quả:** Gây loãng thông tin (*Needle in a Haystack / Lost-in-the-middle*), tăng chi phí token, tăng độ trễ và khiến mô hình dễ bị nhầm lẫn giữa các vai trò.

#### 🔒 5.5.3. Thiết kế Context tinh gọn theo vai trò (Role-based Context Isolation)
Mỗi Agent chỉ nhận đúng dữ liệu nó cần, không đọc toàn bộ lịch sử thô:

```text
[ User Request + Background ]
               │
               ▼
┌───────────────────────────────┐
│ Researcher Context            │ ──► Mục tiêu nghiên cứu + Search tools + Yêu cầu nguồn
└──────────────┬────────────────┘
               │ (Chỉ bàn giao kết quả tóm tắt / Findings)
               ▼
┌───────────────────────────────┐
│ Writer Context                │ ──► Dữ liệu tóm tắt từ Researcher + Văn phong báo cáo
└──────────────┬────────────────┘
               │ (Chỉ bàn giao bản thảo / Draft)
               ▼
┌───────────────────────────────┐
│ Evaluator Context             │ ──► Tiêu chuẩn nghiệm thu (Rubric) + Bản thảo + Bằng chứng gốc
└───────────────────────────────┘
```

| Agent Role | Context được cấp | Thông tin bị lược bỏ |
| :--- | :--- | :--- |
| **🔍 Researcher** | Goal nghiên cứu, công cụ search, tiêu chuẩn dữ liệu | Lịch sử chat cá nhân của user, các quy định về văn phong |
| **✍️ Writer** | Kết quả tổng hợp (*findings*) từ Researcher, template báo cáo | Toàn bộ log tìm kiếm thô, các link web hỏng đã thử |
| **🔎 Evaluator** | Bản draft, rubric chấm điểm, danh sách trích dẫn gốc | Các bước suy luận trung gian của Researcher và Writer |

---

## 🕸️ 6. LangGraph & Agent Orchestration

### 🎯 6.1. Mục tiêu cốt lõi của Chương 6

> [!NOTE]
> Nếu từ **Chương 1 đến Chương 5** tập trung giải quyết câu hỏi thiết kế Agent như thế nào về mặt lý thuyết, thì **Chương 6** giải quyết bài toán kỹ thuật thực thi: Làm thế nào để biến kiến trúc Agent thành một workflow có trạng thái (*State*), khả năng lập kế hoạch (*Plan*), vòng lặp (*Loop*), khả năng lưu trữ phục hồi (*Persistence*) và có sự tham gia kiểm duyệt của con người (*Human-in-the-Loop*)?

---

### 🧩 6.2. Các Thành phần Cốt lõi của StateGraph

Mọi workflow trong LangGraph đều được mô hình hóa dưới dạng một đồ thị trạng thái (*StateGraph*) gồm 4 trụ cột:

```text
[ START ] ──► [ Router Node ] ──► [ Researcher Node ] ──► [ Generator Node ] ──► [ Evaluator Node ]
                                         ▲                                               │
                                         │                    (Score < 0.8: Fail)        ▼
                                         └────────────────────────────────────── [ Conditional Edge ]
                                                                                         │ (Score ≥ 0.8: Pass)
                                                                                         ▼
                                                                                      [ END ]
```

#### 📦 6.2.1. State (Trạng thái dùng chung)
- **Khái niệm:** Nguồn chân lý duy nhất (*Single Source of Truth*) lưu trữ toàn bộ dữ liệu luân chuyển trong suốt vòng đời của workflow.
- **Cấu trúc dữ liệu:** Thường được biểu diễn bằng `TypedDict` hoặc `Pydantic BaseModel` trong Python:

```python
from typing import Annotated, List, TypedDict
import operator

class AgentState(TypedDict):
    query: str
    plan: List[str]
    messages: List[str]
    documents: Annotated[List[str], operator.add]  # Dùng Reducer nối danh sách
    tool_results: dict
    answer: str
    score: float
    retry_count: int
```

📌 **Quy tắc vận hành:** Mỗi Node khi chạy sẽ đọc `AgentState` hiện tại và chỉ trả về phần dữ liệu cần cập nhật (*State Update*).

#### ⚙️ 6.2.2. Node (Đơn vị thực thi)
- **Khái niệm:** Một Node là một đơn vị xử lý độc lập nhận vào `State` và trả về một phần `State` mới.
- **Hình thức triển khai:** Một Node có thể là:
  - Một hàm Python thuần túy (*pure function*).
  - Một lời gọi LLM (*LLM invocation*).
  - Một lời gọi công cụ ngoại vi (*Tool call*).
  - Một `Subgraph` hoàn chỉnh (cho phép lồng ghép Multi-Agent dạng đồ thị con vào đồ thị chính).
- **Các Node phổ biến:** `RouterNode`, `PlannerNode`, `ResearcherNode`, `RAGNode`, `WriterNode`, `EvaluatorNode`.

#### 🔀 6.2.3. Edge & Conditional Edge (Cạnh điều hướng)
- **Edge cố định (*Normal Edge*):** Đường đi xác định 1-1 không đổi (ví dụ: `START` $\rightarrow$ `RouterNode`, hoặc `RetryNode` $\rightarrow$ `GeneratorNode`).
- **Conditional Edge (*Cạnh rẽ nhánh có điều kiện*):** Dựa trên dữ liệu trong `State` để quyết định Node tiếp theo.
  - *Ví dụ:* `EvaluatorNode` kiểm tra `score`:
    - Nếu $\text{score} \ge 0.8$ $\longrightarrow$ Điều hướng về `END`.
    - Nếu $\text{score} < 0.8$ $\longrightarrow$ Tăng `retry_count` và quay về `ResearcherNode` hoặc `RewriteNode`.

> [!IMPORTANT]
> **Bản chất kiến trúc:** Hành vi tự chủ của Agent (*Agentic Behavior*) xuất hiện phần lớn nhờ vào **Conditional Routing & Loops** thay vì logic tuyến tính một chiều.

---

### 🔄 6.3. Reducer: Xử lý Cập nhật Trạng thái Song song

Khi nhiều Node chạy song song (*Parallel Nodes*) hoặc một Node ghi thêm dữ liệu vào một danh sách, nếu không có Reducer thì dữ liệu mới sẽ ghi đè hoàn toàn (*Overwrite*) dữ liệu cũ.

```text
[ Không có Reducer ]
Worker A trả về: [Doc 1] ──► State['documents'] = [Doc 1]
Worker B trả về: [Doc 2] ──► State['documents'] = [Doc 2]  (Mất Doc 1!)

[ Có Reducer (operator.add) ]
Worker A trả về: [Doc 1] ──┐
                           ├──► Reducer: old_docs + new_docs ──► State['documents'] = [Doc 1, Doc 2]
Worker B trả về: [Doc 2] ──┘
```

> [!TIP]
> **Cơ chế Reducer:** Reducer định nghĩa cách gộp dữ liệu cũ và dữ liệu mới:
> $$\text{State}_{\text{new}} = \text{Reducer}(\text{State}_{\text{old}}, \text{Update})$$
> *Cú pháp:* `Annotated[List[str], operator.add]` biến trường `documents` thành dạng nối mảng (*append/extend*) thay vì thay thế.

---

### 💾 6.4. Persistency, Checkpoint & Time Travel

Trong môi trường Production, các tác vụ nghiên cứu sâu, viết mã nguồn hoặc phê duyệt có thể kéo dài hàng giờ. Hệ thống không thể chỉ giữ trạng thái trong bộ nhớ RAM tạm thời.

```text
[ Step 1 ] ──► [ Step 2 ] ──► [ Step 3: Lưu Checkpoint ] ──► (Hệ thống sập / Timeout)
                                         │
                                         └──► [ Phục hồi từ Checkpoint Step 3 ] ──► [ Step 4 ] ──► [ Step 5 ]
```

#### 📍 6.4.1. Checkpoint & Persistence (Lưu trữ trạng thái)
- Sau mỗi bước thực thi (*Superstep*), LangGraph tự động serialize toàn bộ `State` và lưu vào cơ sở dữ liệu bền vững (`PostgreSQL`, `Redis`, `SqliteSaver`) thông qua `thread_id`.
- **Lợi ích:**
  - **Chống sập hệ thống:** Nếu API bên thứ ba bị timeout ở Step 4, hệ thống resume trực tiếp từ Step 3 mà không cần chạy lại từ đầu Step 1.
  - Tối ưu hóa chi phí token và thời gian chờ của người dùng.

#### ⏳ 6.4.2. Time Travel (Du hành thời gian trong đồ thị)
Nhờ có lịch sử Checkpoint ($S_0, S_1, S_2, S_3$), nhà phát triển có thể:
- Quay ngược lại trạng thái quá khứ bất kỳ (ví dụ: $S_1$).
- Tinh chỉnh trực tiếp dữ liệu state hoặc đổi System Prompt.
- Rẽ nhánh chạy thử nghiệm chiến lược mới ($S_1 \rightarrow \text{Strategy B} \rightarrow S_4 \rightarrow S_5$).
- **Ứng dụng:** Debug trực tiếp trên Production, phân tích nguyên nhân lỗi (*root cause analysis*), can thiệp sửa đổi dữ liệu trung gian và đánh giá đối chiếu (A/B Testing).

---

### 👤 6.5. Human-in-the-Loop (HITL)

Không phải hành động nào của Agent cũng được phép tự động kích hoạt. HITL biến con người thành một nút chặn có thẩm quyền phê duyệt trong đồ thị.

```text
[ Agent đề xuất Action ] ──► [ Breakpoint / Interrupt ] ──► Chờ con người:
                                                                 ├── Approve ──► Resume luồng
                                                                 ├── Reject  ──► Rollback / Hủy
                                                                 └── Edit    ──► Sửa payload rồi Resume
```

- **Cơ chế:** Sử dụng `interrupt_before` hoặc `interrupt_after` tại các Node nhạy cảm.

> [!WARNING]
> **Các tác vụ bắt buộc áp dụng HITL:**
> - Gửi email hàng loạt cho khách hàng.
> - Chuyển tiền hoặc thực hiện giao dịch tài chính.
> - Xóa file, drop bảng dữ liệu hoặc sửa đổi dữ liệu nhạy cảm.
> - Triển khai code lên môi trường Production.
> - Xác nhận booking / hóa đơn dịch vụ.

---

### 🛡️ 6.6. Cơ chế Phục hồi Lỗi trên Production (Error Recovery & Graceful Fallback)

Kỹ sư Agentic AI chuyên nghiệp luôn giả định rằng: **Mọi công cụ ngoại vi và model đều có xác suất fail.**

```text
[ Gọi Tool / Vector Search ] ──► Lỗi / Timeout
                                       │
                                       ├── Lần 1: Retry (Exponential Backoff)
                                       ├── Lần 2: Retry
                                       └── Vẫn lỗi ──► [ Kích hoạt Fallback ]
                                                             │
                                                             ├── Chuyển sang BM25 / Keyword Search
                                                             ├── Đổi sang Backup Model (LLM Fallback)
                                                             └── Báo cáo an toàn & Chuyển chuyên viên
```

| Chiến lược | Kỹ thuật triển khai | Mục đích |
| :--- | :--- | :--- |
| **🔄 Retry with Backoff** | Thử lại 2 – 3 lần với khoảng thời gian chờ tăng dần | Xử lý lỗi nghẽn mạng tạm thời (*Network Glitch / Rate Limit*). |
| **🛠️ Fallback Tool** | Vector Search hỏng $\longrightarrow$ chuyển sang BM25 / Keyword Search | Đảm bảo hệ thống vẫn trả được kết quả thay thế chấp nhận được. |
| **🤖 Fallback Model** | Claude/GPT-4o timeout $\longrightarrow$ gọi model dự phòng (như Gemini/Local LLM) | Đảm bảo tính sẵn sàng cao (*High Availability*). |
| **👤 Human Escalation** | Dừng luồng an toàn, thông báo cho người dùng và tạo vé hỗ trợ | Ngăn chặn việc sinh dữ liệu sai hoặc làm gián đoạn trải nghiệm người dùng. |

---

## 🧠 7. Hệ Thống Bộ Nhớ Cho LLM (Memory Systems for LLM)

### 💡 7.1. Bản chất & Hiểu lầm lớn nhất về Trí nhớ của LLM

> [!CAUTION]
> **Hiểu lầm phổ biến:** Nghĩ rằng LLM có khả năng tự ghi nhớ thông tin sau mỗi lượt trò chuyện.
> **Thực tế:** LLM bản chất là **Stateless (phi trạng thái)**. Mỗi lần gọi API về cơ bản chỉ là một hàm suy luận đơn lẻ:
> $$\text{Input (Prompt)} \longrightarrow \text{Model (Inference)} \longrightarrow \text{Output (Response)}$$

📌 **Cơ chế ghi nhớ thực sự:** Muốn mô hình "nhớ" được ngữ cảnh quá khứ, hệ thống bên ngoài (*Memory System*) bắt buộc phải truy xuất các thông tin liên quan từ cơ sở dữ liệu và **nhồi lại vào trong Context Window** của lượt inference hiện tại.

```text
[ Quan niệm sai ]
User: "Tên tôi là Huấn" ──► LLM tự lưu vào não ──► Lượt sau tự nhớ

[ Kiến trúc đúng ]
User: "Tên tôi là Huấn" ──► Lưu DB
                             │
User: "Tôi tên là gì?"  ──► Retrieval từ DB ("Tên user là Huấn") ──► Ghép vào Prompt ──► LLM trả lời: "Huấn"
```

---

### ⚖️ 7.2. Phân biệt: Context Window vs. Memory System

| Tiêu chí | Context Window (Cửa sổ ngữ cảnh) | Memory System (Hệ thống bộ nhớ) |
| :--- | :--- | :--- |
| **Bản chất** | Không gian RAM tạm thời của lượt gọi hiện tại | Kho lưu trữ dữ liệu bền vững bên ngoài (Database / Vector Store) |
| **Phạm vi** | Mô hình nhìn thấy gì ngay tại thời điểm suy luận | Hệ thống đã lưu lại những gì và truy xuất lại khi cần thiết |
| **Độ tồn tại** | Biến mất ngay khi lượt inference kết thúc | Tồn tại xuyên suốt qua nhiều phiên, nhiều ngày, nhiều tháng |
| **Giới hạn** | Giới hạn bởi số lượng token tối đa của model | Gần như không giới hạn dung lượng lưu trữ |

---

### 🗂️ 7.3. Các Phân Loại Bộ Nhớ Cốt Lõi

```text
                              ┌── Short-term Memory (Nội bộ 1 phiên hội thoại)
                              │
[ Hệ Thống Bộ Nhớ (Memory) ] ──┼── Long-term Memory (Xuyên suốt nhiều phiên làm việc)
                              │      │
                              │      ├── Episodic Memory (Kinh nghiệm & Sự kiện: "Chuyện gì đã xảy ra?")
                              │      └── Semantic Memory (Tri thức & Fact: "Tôi biết điều gì?")
                              │
                              └── Profile Memory (Đặc trưng cá nhân hóa: Sở thích, Phong cách)
```

#### 🔹 7.3.1. Short-term Memory (Bộ nhớ ngắn hạn)
- **Phạm vi hoạt động:** Tồn tại trong phiên hội thoại hiện tại (*current conversation thread*).
- **Cơ chế:** Quản lý danh sách các lượt tin nhắn gần nhất (`previous_messages` + `current_message`).
- **Hạn chế:** Nếu một tin nhắn cũ bị đẩy ra khỏi Context Window (do vượt ngưỡng giới hạn token), LLM sẽ hoàn toàn không biết thông tin đó từng tồn tại.

#### 🔹 7.3.2. Long-term Memory (Bộ nhớ dài hạn)
- **Phạm vi hoạt động:** Tồn tại bền vững qua nhiều phiên làm việc khác nhau (*cross-session persistence*).
- **Ứng dụng:** Trích xuất các đặc trưng nền tảng (phong cách giao tiếp, sở thích, thông tin cá nhân hóa, dự án đang theo đuổi) để tái sử dụng ở bất kỳ phiên trò chuyện nào trong tương lai.

#### 🔹 7.3.3. Episodic Memory vs. Semantic Memory

Two critical branches forming long-term memory:

| Đặc tính | Episodic Memory (Bộ nhớ Sự kiện) | Semantic Memory (Bộ nhớ Ngữ nghĩa / Tri thức) |
| :--- | :--- | :--- |
| **Câu hỏi đại diện** | *"Chuyện gì đã xảy ra?" (What happened?)* | *"Tôi biết điều gì?" (What do I know?)* |
| **Nội dung lưu trữ** | Kinh nghiệm, sự kiện, dòng thời gian, hành vi của user | Sự thật (*facts*), tri thức, cấu hình, thông số cố định |
| **Ví dụ thực tế** | • *"User đã hoàn thành bài học X vào tuần trước."*<br>• *"User bị kẹt ở chủ đề Y và thử 3 lần mới qua."*<br>• *"User vừa giải quyết thành công bug logic."* | • *"User thích viết code bằng Python."*<br>• *"Dự án hiện tại sử dụng framework FastAPI."*<br>• *"Hệ thống cơ sở dữ liệu dùng PostgreSQL."* |

---

### ⚙️ 7.4. Pipeline Xử lý Bộ nhớ Chuẩn Production

> [!WARNING]
> **Quy tắc cấm kỵ:** Tuyệt đối không gửi toàn bộ 1000 tin nhắn lịch sử vào LLM trong mỗi request (lãng phí token, tăng độ trễ và làm loãng ngữ cảnh).

```text
[ Tin nhắn mới ] ──► [ Recent Buffer ] ──► [ Summarize & Compress ] ──► [ Extract Facts / Events ] ──► [ Validate & Deduplicate ] ──► [ Persist Store ]
```

1. **Recent Buffer:** Giữ lại $K$ tin nhắn gần nhất để duy trì ngữ cảnh tự nhiên.
2. **Summarize & Compress:** Tóm tắt các khối hội thoại cũ hơn thành các đoạn văn ngắn gọn.
3. **Extract Facts / Events:** Trích xuất các thực thể, sở thích hoặc sự kiện đáng nhớ.
4. **Validate & Deduplicate:** Kiểm tra tính hợp lệ, loại bỏ thông tin trùng lặp hoặc mâu thuẫn với dữ liệu cũ.
5. **Persist Store:** Lưu vào cơ sở dữ liệu chuyên dụng (SQL / NoSQL / Vector DB).

---

### 🏗️ 7.5. Kiến Trúc Bộ Nhớ Hoàn Chỉnh (Memory Architecture Flow)

Sơ đồ điều phối luồng truy xuất và cập nhật bộ nhớ trong một hệ thống Agentic / LLM chuyên nghiệp:

```text
                    USER
                      │
                      ▼
                Current Query
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
    Recent Messages         Memory Retrieval
          │                       │
          │              ┌────────┼────────┐
          │              ▼        ▼        ▼
          │           Semantic Episodic Profile
          │              │        │        │
          └──────────────┼────────┼────────┘
                         ▼
                  Context Builder
                         │
                         ▼
                        LLM
                         │
                         ▼
                      Response
                         │
                         ▼
                  Memory Extractor
                         │
                    Worth saving?
                    ┌────┴────┐
                   NO        YES
                   │          │
                  END      Persist
```

#### 📌 Chi tiết các bước vận hành:
1. **Truy vấn đầu vào:** Người dùng gửi câu hỏi mới (*Current Query*).
2. **Truy xuất song song:**
   - Lấy các tin nhắn gần nhất (*Recent Messages*).
   - Thực hiện `Memory Retrieval` để kéo về các mảnh ghép liên quan từ: `Semantic`, `Episodic` và `Profile Memory`.
3. **Context Builder:** Ghép nối có chọn lọc các thông tin trên thành một Context tối ưu, ngắn gọn và đưa vào LLM.
4. **Sinh phản hồi:** LLM trả lời câu hỏi dựa trên ngữ cảnh đã được cá nhân hóa đầy đủ.
5. **Memory Extractor (Hậu xử lý):** Phân tích xem trong lượt tương tác vừa rồi có thông tin gì mới cần nhớ lâu dài hay không:
   - Nếu không có giá trị (**NO**): Kết thúc luồng (**END**).
   - Nếu có thông tin quan trọng (**YES**): Ghi vào cơ sở dữ liệu bền vững (**Persist**).

---

## 🛡️ 8. Vận hành Thực tế — Guardrails, Grounding, Metrics & Deep Research Architecture

### 🚨 8.1. Rủi ro của Agentic AI & Chuỗi Kiểm soát (Guardrails Pipeline)

> [!CAUTION]
> **Điểm khác biệt chí mạng giữa Chatbot thông thường và AI Agent:**
> - **Chatbot:** Chỉ tạo ra văn bản (*Generate text*).
> - **Agent:** Có khả năng thực thi hành động (*Execute actions* qua tool, API, database).
>
> Do đó, **đầu ra của LLM không bao giờ được mặc định tin tưởng**. Một hệ thống an toàn trên môi trường Production phải thiết lập chuỗi kiểm soát khép kín:

$$\text{User Input} \longrightarrow \text{Input Guard} \longrightarrow \text{Agent} \longrightarrow \text{Tool Permission} \longrightarrow \text{Action Validation} \longrightarrow \text{Tool} \longrightarrow \text{Result Validation} \longrightarrow \text{Output Guard} \longrightarrow \text{User Output}$$

```text
[ User Input ] ──► [ Input Guard ] ──► [ Agent Reasoning ] ──► [ Tool Permission ]
                                                                       │
                                                                       ▼
[ User ] ◄── [ Output Guard ] ◄── [ Result Validation ] ◄── [ Tool Execution ]
```

#### 🛡️ 8.1.1. Input Guardrail
- **Nhiệm vụ:** Ngăn chặn các câu lệnh độc hại hoặc dữ liệu dị dạng tiếp cận trực tiếp vào hệ thống công cụ.
- **Cơ chế kiểm soát:**
  - Phát hiện tấn công tiêm nhiễm câu lệnh (*Prompt Injection Detection*).
  - Kiểm tra vi phạm chính sách (*Policy Check*).
  - Xác thực định dạng đầu vào (*Input Schema Validation*).

#### 🛡️ 8.1.2. Output Guardrail
- **Nhiệm vụ:** Bảo đảm nội dung phản hồi cho người dùng hoặc payload truyền sang công cụ khác đạt chuẩn an toàn.
- **Cơ chế kiểm soát:**
  - Quét và làm mờ thông tin định danh cá nhân (*PII Masking / Redaction*).
  - Kiểm tra định tuyến (*Routing Check*) và chính sách nội dung (*Policy Check*).
  - Xác thực cấu trúc dữ liệu trả về (*JSON Schema Validation*), đặc biệt tối quan trọng khi output của Agent này là input của Agent/Tool kế tiếp.

---

### 🔒 8.2. Kiểm soát Quyền hạn & Cô lập Thực thi (Control & Sandboxing)

📌 Cả **Capability Control** và **Sandboxing** đều phục vụ một mục tiêu cốt lõi: **Giới hạn tối đa phạm vi ảnh hưởng (*Blast Radius*)** khi Agent gặp lỗi hoặc bị tấn công.

#### 🔑 8.2.1. Kiểm soát quyền hạn (Capability Control & Least Privilege)
- **Nguyên tắc đặc quyền tối thiểu (*Least Privilege*):** Mỗi Agent chỉ được cấp đúng những công cụ phục vụ vai trò của nó.
- **Ví dụ phân định quyền:**
  - `Researcher Agent`: Chỉ được cấp quyền `search_web`, `read_document`, `extract_notes`.
  - *Tuyệt đối không cấp:* `delete_database`, `transfer_money`, `deploy_production`.

#### 📦 8.2.2. Môi trường hộp cát (Sandboxing)
Khi Agent cần thông dịch hoặc thực thi mã lệnh (ví dụ: chạy script Python để phân tích dữ liệu), **tuyệt đối không chạy trực tiếp trên máy chủ Production (*Host System*)**.

Cần thiết lập môi trường Sandbox độc lập với các hàng rào bảo vệ:
- Giới hạn tài nguyên phần cứng (*CPU & Memory Limits*).
- Cô lập hệ thống tệp tin (*Ephemeral Virtual Filesystem*).
- Chặn truy cập mạng không cần thiết (*Network Restrictions*).
- Thiết lập thời gian chờ cưỡng chế (*Strict Execution Timeout*).

---

### 📌 8.3. Xác thực Căn cứ & Ánh xạ Nguồn (Grounding & Citation Mapping)

Grounding không chỉ đơn giản là nhồi tài liệu RAG vào context, mà là quy trình đối chiếu và kiểm tra từng luận điểm (*Claim Verification*):

```text
                   ┌──► Claim 1 ──► Có trong Source A ──► [ Hợp lệ ]
                   │
[ Generated Text ] ┼──► Claim 2 ──► Có trong Source B ──► [ Hợp lệ ]
                   │
                   └──► Claim 4 ──► Không có Evidence  ──► [ Cần xử lý ]
```

> [!TIP]
> **Quy trình xử lý luận điểm thiếu bằng chứng (*Missing Evidence Flow*):**
> $$\text{Claim 4 thiếu bằng chứng} \longrightarrow \text{Tìm kiếm bổ sung (Search again)} \longrightarrow \begin{cases} \text{Tìm thấy (Found)} & \longrightarrow \text{Giữ lại \& gắn Citation} \\ \text{Không tìm thấy (Not Found)} & \longrightarrow \text{Xóa luận điểm / Tuyên bố chưa xác thực} \end{cases}$$

---

### 📊 8.4. Hệ thống Chỉ số Đánh giá Agent trên Production (Metrics Framework)

> [!IMPORTANT]
> **Không đánh giá năng lực của AI Agent bằng trực giác hay cảm tính** (*"thấy chạy thử khá thông minh"*). Hệ thống cần được định lượng qua 5 nhóm chỉ số:

| Nhóm chỉ số | Chỉ số chi tiết | Ý nghĩa đo lường |
| :--- | :--- | :--- |
| **🎯 Quality** | • Task Success Rate<br>• Answer Relevance<br>• Groundedness / Faithfulness<br>• Hallucination Rate<br>• Completeness | Chất lượng nội dung và độ tin cậy của câu trả lời. |
| **🛡️ Reliability** | • Tool Success Rate<br>• Retry Rate<br>• Failure Rate<br>• Recovery Rate | Khả năng tự phục hồi khi gặp lỗi API / mạng. |
| **⚡ Performance** | • Total Latency<br>• Latency từng Node (Router, Planner...)<br>• Tool Latency<br>• Time-to-First-Token (TTFT) | Phát hiện chính xác điểm nghẽn (*bottleneck*) trong đồ thị xử lý. |
| **💸 Cost** | • Input / Output Tokens<br>• Tool Call Tokens<br>• Cost per Successful Task | Chi phí tài chính thực tế trên mỗi nhiệm vụ thành công. |
| **🧠 Behavior** | • Số bước thực thi (*Steps count*)<br>• Số lần gọi tool<br>• Số lần Re-plan<br>• Tỷ lệ cần con người can thiệp (*HITL rate*) | Mức độ phức tạp và tính ổn định trong hành vi suy luận. |

#### 🔍 Phân tích Bottleneck qua Node Latency & Token Usage:
- **Node Latency:** $\text{Router (0.3s)} \rightarrow \text{Planner (0.5s)} \rightarrow \text{Retriever (0.8s)} \rightarrow \text{LLM Generation (2.1s)} \rightarrow \text{Verification (1.0s)} \Longrightarrow \text{Tổng Latency} = 4.7s$ (LLM Generation là bottleneck lớn nhất).
- **Token Cost:** $\text{Planner (2k)} \rightarrow \text{Researcher (8k)} \rightarrow \text{Writer (4k)} \rightarrow \text{Evaluator (7k)} \Longrightarrow \text{Tổng Token} = 17k$ (Đặc biệt trong Multi-Agent, token tăng nhanh do dữ liệu context luân chuyển qua nhiều tầng).

#### 💰 Chỉ số Hiệu quả Kinh tế: Cost per Success
$$\text{Cost per Success} = \frac{\text{Total Cost}}{\text{Successful Tasks}}$$

> [!WARNING]
> **Cảnh báo kiến trúc:** Một hệ thống đạt tỷ lệ thành công $95\%$ nhưng chi phí tốn gấp $10$ lần hệ thống đạt $93\%$ chưa chắc đã là giải pháp tốt trên quy mô kinh doanh lâu dài.

---

### 🏛️ 8.5. Kiến trúc Tổng thể: Deep Research Agent System

Sơ đồ tích hợp toàn diện luồng thực thi trung tâm kết hợp chặt chẽ với 6 hệ thống nền tảng bao quanh:

```text
                                      USER
                                        │
                                        ▼
                                 ┌────────────┐
                                 │ Input Guard│
                                 └──────┬─────┘
                                        ▼
                                 ┌────────────┐
                                 │   Router   │
                                 └──────┬─────┘
                                        ▼
                                 ┌────────────┐
                                 │  Planner   │
                                 └──────┬─────┘
                                        │
                         ┌──────────────┼──────────────┐
                         ▼              ▼              ▼
                   Researcher A   Researcher B   Researcher C
                         │              │              │
                         └──────────────┼──────────────┘
                                        ▼
                                      Writer
                                        │
                                        ▼
                                    Evaluator
                                        │
                                ┌───────┴───────┐
                                ▼               ▼
                               FAIL            PASS
                                │               │
                            Reflection        Verify
                                │               │
                             Replan          Grounding
                                │               │
                             Workers         Citation
                                                │
                                                ▼
                                           Output Guard
                                                │
                                                ▼
                                              USER
```

#### ⚙️ 6 Hệ thống Nền tảng Bao quanh Đồ thị (Core Infra & Controls)

```text
┌──────────────────────────────────────────────────────────┐
│                          STATE                           │
│ plan / docs / messages / results / scores                │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                         MEMORY                           │
│ short-term / long-term / episodic / semantic             │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                       PERSISTENCE                        │
│ checkpoint / resume / time travel                        │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                          HITL                            │
│ interrupt / approve / reject / edit                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                        SECURITY                          │
│ guardrails / permissions / sandbox                       │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                       EVALUATION                         │
│ quality / success / latency / tokens / cost              │
└──────────────────────────────────────────────────────────┘
```

1. **State:** Không gian dữ liệu dùng chung luân chuyển qua từng nút xử lý.
2. **Memory:** Quản lý bối cảnh ngắn hạn và tri thức dài hạn đa phiên của người dùng.
3. **Persistence:** Cơ chế lưu trữ Checkpoint bảo đảm hệ thống có thể tiếp tục chạy sau khi đứt đoạn và hỗ trợ Time Travel debug.
4. **HITL (Human-in-the-Loop):** Điểm chốt chặn can thiệp, kiểm duyệt hoặc chỉnh sửa trước các tác vụ nhạy cảm.
5. **Security:** Hàng rào bảo vệ đa lớp từ Input Guard, Least Privilege đến Sandboxing độc lập.
6. **Evaluation:** Bảng đo lường trực quan toàn diện về chất lượng đầu ra, thời gian xử lý và chi phí kinh tế.







