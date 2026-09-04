# 🔌 Chương 1: MCP – Kết Nối Agent Với Thế Giới Bên Ngoài

---

## 🧩 1.1. Vấn Đề Cốt Lõi Của Agent: N × M Integration Complexity

> [!NOTE]
> **LLM thuần túy chỉ hoạt động theo chu trình đóng kín:** $$\text{Input} \longrightarrow \text{LLM} \longrightarrow \text{Output}$$

- **Hạn chế:** LLM hiểu ngữ nghĩa của câu lệnh *"Kiểm tra lịch của tôi ngày mai"*, nhưng bản thân nó không có quyền truy cập hay trạng thái thực thi trên Google Calendar, Database, File System hay Internal API.
- **Nhu cầu:** Để trở thành một *Autonomous / Action Agent*, LLM bắt buộc phải có khả năng tương tác với hệ thống bên ngoài.

#### ⚠️ Nghịch lý $N \times M$:
- Nếu có $N$ ứng dụng AI (Claude Desktop, Cursor, Custom Agent, Slackbot) và $M$ công cụ / nguồn dữ liệu (Postgres, GitHub, Slack, Google Calendar).
- Việc tích hợp theo cách truyền thống đòi hỏi viết mã riêng cho từng cặp: **tổng số connector cần duy trì là $N \times M$**.
- **Hệ quả:** Chi phí bảo trì cực lớn, dễ gãy vỡ khi API thay đổi, và không thể tái sử dụng tool giữa các ứng dụng AI khác nhau.

```text
[ Truyền thống: N x M ]
App 1 \  /--- Tool A (DB)
App 2 --X---- Tool B (Calendar)
App 3 /  \--- Tool C (GitHub)
(Cần viết 3 x 3 = 9 connectors riêng)
```

---

## 🔌 1.2. MCP Là Gì? Chuẩn "USB-C" Cho AI

**Model Context Protocol (MCP)** là giao thức chuẩn mở (*open standard*) định nghĩa cách thức an toàn, thống nhất để ứng dụng AI (*Host/Client*) kết nối với các nguồn dữ liệu và công cụ bên ngoài (*Server*).

> [!TIP]
> **Tư duy cốt lõi (USB Analogy):** Thay vì mỗi thiết bị điện tử phải dùng một loại cáp sạc độc quyền, thế giới chuẩn hóa bằng cổng **USB-C**. MCP đóng vai trò là "cổng USB-C" cho thế giới AI:
> - Phía Client (Ứng dụng AI) chỉ cần hỗ trợ MCP một lần duy nhất.
> - Phía Server (Công cụ/Dữ liệu) chỉ cần phơi bày giao diện chuẩn MCP một lần duy nhất.
> - **Độ phức tạp giảm từ $N \times M$ xuống còn $N + M$.**

```text
[ Chuẩn MCP: N + M ]
App 1 \                         /--- MCP Server A (DB)
App 2 --- [MCP Client Protocol] ---- MCP Server B (Calendar)
App 3 /                         \--- MCP Server C (GitHub)
```

---

## 🏛️ 1.3. Kiến Trúc MCP Client & MCP Server

Hệ thống MCP phân chia trách nhiệm rõ ràng giữa hai thành phần:

#### 📱 MCP Client (Phía ứng dụng AI)
- Tích hợp trực tiếp bên trong AI Host App (ví dụ: Claude Desktop, IDE, chatbot framework).
- Quản lý kết nối, khám phá danh sách capabilities (hỏi Server: *"Bạn hỗ trợ những tool/resource/prompt nào?"*).
- Chuyển ngữ cảnh (*context*) từ Server vào prompt cho LLM, đồng thời gửi yêu cầu thực thi công cụ từ LLM xuống Server.

#### 🛠️ MCP Server (Phía công cụ & dữ liệu)
- Đóng gói các logic nghiệp vụ cụ thể kết nối tới DB, API bên thứ ba, hay Local Files.
- Chịu trách nhiệm thực thi an toàn các hành vi được yêu cầu và trả kết quả chuẩn hóa về Client.

---

## 📦 1.4. Ba Primitives Cốt Lõi Của MCP

MCP chuẩn hóa ba dạng thành phần mà một Server có thể cung cấp:

| Primitive | Bản chất | Chiều tương tác | Ví dụ trong Hệ thống Học tập |
| :--- | :--- | :--- | :--- |
| **📄 Resource** | Dữ liệu, tài liệu, file nhị phân | **Read-only** *(Agent đọc context)* | Đọc file giáo trình PDF, thông tin lớp học, cấu trúc bài giảng |
| **💬 Prompt** | Mẫu prompt (*template*) dựng sẵn | **Workflow** *(Định hướng hành vi)* | Template tạo đề thi trắc nghiệm, template giải thích bài tập theo Socratic method |
| **⚡ Tool** | Hàm thực thi hành động | **Executable** *(Agent gọi hàm có tác dụng phụ)* | `create_quiz()`, `get_student_progress()`, `save_score()` |

> [!IMPORTANT]
> **Nguyên tắc phân định then chốt:**
> - **Resource** là dữ liệu nạp vào để tăng cường tri thức (*Context*).
> - **Tool** là hành động tạo ra thay đổi trạng thái hoặc truy vấn động (*Action / Execution*).

---

## 🚀 1.5. Cơ Chế Transport (Truyền Tải Thông Điệp)

Client và Server giao tiếp qua chuẩn định dạng **JSON-RPC 2.0** thông qua hai phương thức transport chính:

1. **Local Transport (`stdio`):**
   - MCP Server chạy như một process con (*subprocess*) của Host Application trên cùng một máy tính.
   - Trao đổi dữ liệu qua Standard Input/Output. Cực kỳ nhanh, an toàn cho file local và terminal tool.
2. **Remote Transport (`HTTP with SSE / WebSockets`):**
   - MCP Server triển khai trên cloud hoặc mạng nội bộ.
   - Sử dụng Server-Sent Events (SSE) cho streaming và HTTP POST cho client-to-server request. Phù hợp cho enterprise APIs và remote microservices.

---

## 🔄 1.6. Luồng Dữ Liệu Tổng Thể (End-to-End Flow)

```text
[User]
  │ (1) "Lấy điểm của sinh viên A và lưu vào file báo cáo"
  ▼
[AI App / LLM]
  │ (2) Quyết định cần gọi tool 'get_score' & 'save_report'
  ▼
[MCP Client]
  │ (3) Gửi JSON-RPC Request (Tool Call) qua Transport (stdio / SSE)
  ▼
[MCP Server]
  │ (4) Dispatch logic đến Tool / Resource / Prompt tương ứng
  ▼
[External System] (Database, LMS, Local File System, Third-party APIs)
```

---

## 🎯 2. Prompt & Context Engineering – Định Hình Tư Duy Cho Agent

> [!NOTE]
> Một Agent dù được trang bị 50 công cụ (*Tools*) hiện đại qua MCP vẫn sẽ hoạt động kém hiệu quả nếu LLM:
> 1. Không nhận diện được khi nào cần dùng tool.
> 2. Nhầm lẫn tool nào phù hợp nhất cho nhiệm vụ.
> 3. Thiếu ngữ cảnh (*context*) để truyền tham số chính xác.
> 4. Trả ra định dạng kết quả (*format*) khiến hệ thống tiếp theo không thể phân tích cú pháp (*parse error*).

📌 **Prompt & Context Engineering** đóng vai trò là **hệ điều hành nhận thức**, chuyển hóa LLM từ một mô hình tạo văn bản thuần túy thành một Agent có năng lực lập luận, định hướng và điều phối công cụ.

---

### 📋 2.1. Cấu Trúc Chuẩn RTCF (Role – Task – Context – Format)

Để xây dựng System Prompt hay Tool-use Prompt chuẩn mực, khung làm việc **RTCF** (hoặc AICF Framework) giúp bao quát toàn bộ thông tin nền tảng mà LLM cần:

| Thành phần | Câu hỏi cốt lõi | Ý nghĩa & Vai trò | Minh họa thực tế |
| :--- | :--- | :--- | :--- |
| **👤 Role** | *Bạn là ai?* | Thiết lập hệ quy chiếu, phong cách giao tiếp, phạm vi quyền hạn và chuyên môn | *"Bạn là AI Tutor chuyên dạy Toán THPT với phong cách gợi mở, kiên nhẫn."* |
| **🎯 Task** | *Cần làm gì?* | Xác định rõ ràng mục tiêu hành động đơn lẻ hoặc chuỗi hành động cần hoàn thành | *"Hãy giải thích trực quan khái niệm đạo hàm."* |
| **📌 Context** | *Đang biết gì?* | Cung cấp ràng buộc nền tảng, trạng thái người dùng, lịch sử trò chuyện hoặc data truy xuất | *"Học sinh lớp 11; đã nắm vững hàm số bậc nhất và bậc hai nhưng chưa học giới hạn (limit)."* |
| **📐 Format** | *Trả lời như thế nào?* | Quy định cấu trúc đầu ra để hiển thị trực quan hoặc cho parser đọc (JSON / Markdown) | *"1 đoạn giải thích trực quan ngắn $\rightarrow$ 1 ví dụ thực tế đời sống $\rightarrow$ 1 câu hỏi tương tác kiểm tra."* |

---

### 🎯 2.2. Few-Shot Prompting: Định Hình Pattern và Ràng Buộc Output

Thay vì chỉ mô tả nhiệm vụ bằng văn bản thuần túy (*Zero-shot*), **Few-shot Prompting** cung cấp sẵn 2 – 5 cặp mẫu (*Input, Output*).

- **Cơ chế:** LLM học theo cơ chế nhận diện mẫu (*In-context Pattern Matching*) để căn chỉnh chính xác nhãn phân loại hoặc định dạng dữ liệu đầu ra.
- **Ứng dụng điển hình trong Agent:** Phân loại ý định (*Intent Classification*) để routing đến đúng Tool / Sub-agent.

```text
[System Prompt Example]
Phân loại yêu cầu của người dùng vào đúng nhãn quy định.

Ví dụ 1:
Input: "Tôi muốn đặt phòng khách sạn tại Đà Nẵng cuối tuần này"
Output: {"intent": "book_room"}

Ví dụ 2:
Input: "Pass wifi của khách sạn là gì thế?"
Output: {"intent": "hotel_qa"}

Ví dụ 3:
Input: "Có phòng đôi nào trống từ ngày mai không?"
Output: {"intent": "book_room"}

Input: [Nội dung người dùng nhập vào]
Output:
```

---

### 🔗 2.3. Chain of Thought (CoT): Phân Rã Bài Toán và Suy Luận Từng Bước

Đối với các nhiệm vụ phức tạp, việc ép LLM đưa ra câu trả lời ngay lập tức (*Direct Answering*) thường dẫn đến ảo giác (*hallucination*) hoặc bỏ sót bước logic.

- **Phân rã vấn đề (*Problem Decomposition*):** Thay vì xử lý nguyên khối câu hỏi *"Hãy tìm tài liệu về RAG và so sánh với Vector Search và Hybrid Search"*, Agent tự động lập kế hoạch phân rã:
  - **Sub-goal 1:** Truy vấn định nghĩa và cơ chế hoạt động của RAG.
  - **Sub-goal 2:** Truy vấn cơ chế hoạt động của Vector Search thuần túy.
  - **Sub-goal 3:** Truy vấn cơ chế hoạt động của Hybrid Search (*Keyword + Dense Vector*).
  - **Sub-goal 4:** Tổng hợp, đối chiếu ưu / nhược điểm trong bài toán triển khai thực tế.
- **Tư duy tường minh (*Explicit Reasoning*):** Buộc mô hình tạo ra chuỗi suy nghĩ (`<thought>` hoặc scratchpad) trước khi đưa ra quyết định gọi Tool hoặc gửi phản hồi cuối cùng.

```text
[User Goal]
    │
    ▼
[Decomposition] ──► Step 1: Query RAG concepts
    │           ──► Step 2: Query Vector Search vs Hybrid Search
    │           ──► Step 3: Compare metrics (Recall, Latency, Cost)
    ▼
[Synthesis]     ──► Final Structured Answer
```

---

### 🌲 2.4. Tree of Thoughts (ToT): Khám Phá Đa Hướng và Đánh Giá Đường Đi

Khi một bài toán có nhiều hướng tiếp cận khác nhau và không thể xác định hướng đi tối ưu chỉ qua một luồng tuyến tính, **Tree of Thoughts** cho phép Agent rẽ nhánh, duyệt các không gian nghiệm (*Search Space*) và quay lui (*Backtracking*) khi cần.

#### ⚙️ Cơ chế hoạt động:
1. **Branching (Sinh nhánh):** Từ trạng thái ban đầu, sinh ra nhiều phương án giải quyết (Solution A, B, C).
2. **Evaluation (Đánh giá):** Tự chấm điểm tính khả thi, độ tin cậy của từng nhánh.
3. **Selection (Chọn lọc):** Chọn nhánh điểm cao nhất để đào sâu tiếp hoặc phối hợp các nhánh.

#### 💡 Ví dụ trong Research Agent:
- **Vấn đề:** *"Tìm bằng chứng đánh giá hiệu quả của mô hình Transformer trên ảnh y tế."*
  - **Nhánh A:** Tìm kiếm bài báo khoa học trên ArXiv / PubMed.
  - **Nhánh B:** Tìm kiếm tài liệu kỹ thuật / báo cáo từ các lab nghiên cứu lớn.
  - **Nhánh C:** Rà soát kho mã nguồn mở và benchmarks trên GitHub.
- **Đánh giá & Tổng hợp:** Đối chiếu chéo (*Cross-verification*) giữa các nguồn trước khi kết luận.

```text
                   [Research Question]
                     /      |      \
                    /       |       \
          [Branch A]    [Branch B]   [Branch C]
         (ArXiv/Papers) (Tech Blogs)  (GitHub/Codes)
              \             |             /
               \───► [Cross-Evaluate] ◄──/
                            │
                     [Final Report]
```

---

### 🗳️ 2.5. Self-Consistency: Khử Nhiễu Suy Luận Bằng Đa Số Phiếu (Majority Voting)

Cơ chế lấy mẫu (*sampling*) của LLM có tính ngẫu nhiên (dựa trên `temperature`). Một lần suy luận đơn lẻ có thể vô tình chọn phải một bước sai trong chuỗi logic.

#### ⚙️ Cơ chế Self-Consistency:
- Cho LLM chạy song song nhiều đường suy luận CoT độc lập (ví dụ $k = 3$ hoặc $k = 5$ candidates: Path A, Path B, Path C).
- Mỗi path tự sinh ra lập luận và đáp số tương ứng.
- **Bộ đánh giá (*Evaluator*)** hoặc cơ chế **bỏ phiếu theo số đông (*Majority Vote*)** sẽ chọn kết quả có tần suất xuất hiện cao nhất và nhất quán nhất.

```text
                 [Complex Question]
               /         |         \
              ▼          ▼          ▼
          [Path A]    [Path B]   [Path C]
           CoT 1       CoT 2      CoT 3
             │           │          │
         Answer X    Answer Y   Answer X
              \          |         /
               ▼         ▼        ▼
              [Evaluator / Voting]
                         │
                         ▼
                   [Answer X] (Đa số)
```

#### 📈 Cân nhắc kỹ thuật (Trade-off Matrix)

| Tiêu chí | Single Prompt (CoT) | Self-Consistency (ToT / Multi-candidate) |
| :--- | :--- | :--- |
| **🎯 Độ chính xác (Accuracy)** | Khá – Tốt cho bài toán rõ ràng | **Rất cao** – Khử nhiễu và ảo giác vượt trội |
| **⚡ Độ trễ (Latency)** | **Thấp** ($1\times$) | Cao ($3\times - 5\times$) |
| **💸 Chi phí Token (Cost)** | **Tiết kiệm** | Tăng tuyến tính theo số lượng nhánh / candidate |
| **📌 Phù hợp cho** | Chatbot thông thường, workflow đơn giản | Bài toán logic toán học, research, trích xuất tài liệu pháp lý / y tế |

---

## 🧠 3. Context Management – Trái Tim Vận Hành Của Agent Thực Sự

> [!NOTE]
> Khác biệt cốt lõi giữa một chatbot thông thường và một AI Agent nằm ở năng lực khép kín chu trình:
> $$\text{Lập kế hoạch (Plan)} \longrightarrow \text{Hành động (Act)} \longrightarrow \text{Quan sát (Observe)} \longrightarrow \text{Quyết định tiếp theo (Decide)}$$

Agent không thể suy luận chính xác nếu bị "ngộp" thông tin hoặc context window bị phân mảnh. **Quản lý ngữ cảnh (Context Management)** chính là kiến trúc hạ tầng quyết định Agent có chạy ổn định, tiết kiệm chi phí và đạt độ chính xác cao trong thực tế hay không.

---

### ⚖️ 3.1. Nghịch Lý Context Window và Dynamic Context Injection

Dù các LLM hiện đại hỗ trợ context window lên đến hàng trăm nghìn hay hàng triệu token, việc nhồi nhét toàn bộ dữ liệu (100 tài liệu PDF, lịch sử học tập, profile, 500 tin nhắn chat) trực tiếp vào model sẽ dẫn đến 3 vấn đề nghiêm trọng:

1. **Hiện tượng "Lost in the Middle":** LLM chú ý tốt ở đầu và cuối context, dễ bỏ qua thông tin quan trọng nằm ở giữa.
2. **Chi phí & Độ trễ (Cost & Latency):** Thời gian sinh token (*Time to First Token - TTFT*) và chi phí API tăng tuyến tính theo kích thước prompt.
3. **Tăng rủi ro Hallucination:** Quá nhiều thông tin nhiễu khiến mô hình kích hoạt các vector tri thức không liên quan.

#### 💡 Giải pháp: Dynamic Context Injection (Bơm ngữ cảnh động)
Thay vì nạp tĩnh toàn bộ tri thức, hệ thống sử dụng một lớp trung gian **Context Manager** đóng vai trò bộ lọc:

```text
[User Request] 
      │
      ▼
[Context Manager] ◄── Filter / Retrieval (RAG, Cache, Memory Store)
      │
      ▼ (Chỉ trích xuất Relevant Context thực sự cần thiết)
    [LLM]
```

- **Ví dụ luồng RAG:** Khi người dùng hỏi *"Attention mechanism hoạt động như thế nào?"*:
  1. Câu hỏi được vector hóa thành embedding vector.
  2. Vector Search truy vấn trong cơ sở dữ liệu để lọc ra 3–5 chunks tài liệu có độ tương đồng cao nhất.
  3. Context Manager chỉ tiêm các chunks này kèm System Prompt vào LLM để sinh câu trả lời.

---

### ✂️ 3.2. Context Trimming & Window Budgeting

Khi một phiên làm việc kéo dài hàng trăm lượt trao đổi (từ Message 1 đến Message 200+), việc gửi toàn bộ chuỗi hội thoại là lãng phí và phản tác dụng.

Chiến lược **Context Trimming** thiết lập một ngân sách token (*Token Budget*) và tái cấu trúc payload gửi đến LLM theo các tầng ưu tiên:

```text
┌─────────────────────────────────────────────────────────┐
│ System Prompt & Role Definition (Bất biến)              │
├─────────────────────────────────────────────────────────┤
│ Core User Profile & Long-term Memory (Cố định, ngắn gọn)│
├─────────────────────────────────────────────────────────┤
│ Conversation Summary (Tóm tắt nén từ Msg 1 -> N-10)     │
├─────────────────────────────────────────────────────────┤
│ Retrieved Documents / Tool Outputs (Dynamic Injection)  │
├─────────────────────────────────────────────────────────┤
│ Sliding Window: 10 tin nhắn gần nhất (Raw history)      │
└─────────────────────────────────────────────────────────┘
```

> [!TIP]
> **Lợi ích:** Kỹ thuật này đảm bảo ngữ cảnh của Agent vừa duy trì được tính liên tục cục bộ (*Local Coherence qua Sliding Window*), vừa giữ được sợi dây kết nối toàn cục (*Global Context qua Memory & Summary*).

---

### 📝 3.3. Conversation Summarization (Tóm Tắt Nén Ngữ Cảnh)

Tóm tắt không chỉ đơn giản là rút gọn văn bản, mà là quá trình chắt lọc trạng thái nhận thức và mục tiêu của người dùng (*State Extraction*).

- **Dữ liệu thô (100 messages):** Lịch sử trao đổi dài dòng qua nhiều ngày về việc xây dựng hệ thống hỏi đáp tài liệu.
- **Nén ngữ cảnh có cấu trúc (Structured State Summary):**
  - **Chủ đề đang xử lý:** Kiến trúc RAG cho môi trường production.
  - **Kiến thức người dùng đã nắm vững:** Embedding, Vector Database.
  - **Lỗ hổng / Khái niệm đang gặp khó khăn:** Re-ranking, Hybrid Search (*Keyword + Dense Vector*).
  - **Mục tiêu cuối cùng:** Triển khai pipeline RAG hoàn chỉnh đạt độ chính xác cao.

> [!IMPORTANT]
> Agent sử dụng bản tóm tắt trạng thái này làm background context cho các lượt tương tác tiếp theo, loại bỏ hoàn toàn các câu chat chào hỏi, tin nhắn thừa thãi.

---

### 🔄 3.4. Tool Calling & Vòng Lặp Agent Loop

**Tool Calling** là bước ngoặt biến mô hình ngôn ngữ từ "người trò chuyện" thành "thực thể hành động". Khi cần dữ liệu thực tế, LLM không suy đoán mà phát sinh một cấu trúc lệnh gọi hàm (*Function Call*).

#### 🔁 Bản chất chu trình Agent Loop (ReAct Pattern)
Chu trình vận hành theo vòng lặp 4 bước: $\text{Request} \longrightarrow \text{Thought/Analysis} \longrightarrow \text{Action (Tool Call)} \longrightarrow \text{Observation}$.

```text
                 [User Request]
                       │
                       ▼
            ┌──► [Thought / Phân tích]
            │          │
            │          ├─► Cần gọi Tool? ──► [NO] ──► [Answer User]
            │          │
            │          └─► [YES]
            │                │
            │                ▼
            │        [Action: Gọi Tool]
            │          (JSON payload)
            │                │
            │                ▼
            │     [Thực thi qua MCP/API]
            │                │
            │                ▼
            └──── [Observation: Kết quả trả về]
                   (Đã đủ thông tin chưa?)
```

#### ⚙️ Xử lý chuỗi hành động phức tạp (Multi-Action Flow)
Một yêu cầu người dùng có thể kích hoạt nhiều tool tuần tự trước khi ra được câu trả lời:
- **Yêu cầu:** *"Xem mai tôi rảnh lúc nào và đặt lịch họp với An."*
  - **Action 1:** `get_calendar(date="tomorrow")` $\longrightarrow$ **Observation 1:** Rảnh lúc 14:00 - 16:00.
  - **Action 2:** `find_contact(name="An")` $\longrightarrow$ **Observation 2:** Email: `an@company.com`.
  - **Action 3:** `create_event(attendees=["an@company.com"], start="14:00")` $\longrightarrow$ **Observation 3:** Tạo sự kiện thành công.
  - **Final Answer:** *"Tôi đã đặt lịch họp với An vào lúc 14:00 ngày mai."*

---

### 🛠️ 3.5. Nguyên Tắc Thiết Kế Tool (Tool Design Principles)

LLM "nhìn" thế giới công cụ thông qua tên hàm (*Function Name*), mô tả (*Description*), và sơ đồ tham số (*Parameter Schema*). Thiết kế tool kém là nguyên nhân hàng đầu khiến Agent gọi sai hoặc sinh ảo giác tham số.

| Tiêu chí | ❌ Thiết kế kém (Anti-pattern) | ✅ Thiết kế chuẩn (Best Practice) | Lý do kỹ thuật |
| :--- | :--- | :--- | :--- |
| **🏷️ Đặt tên (Naming)** | `run()`, `handle_data()`, `process_input()` | `search_document()`, `get_student_profile()`, `create_quiz()` | Tên mang tính mô tả hành động cụ thể giúp LLM ánh xạ đúng ngữ nghĩa (*Semantic Mapping*). |
| **📥 Tham số (Parameters)** | `execute(a, b, c, mode)` | `get_student_profile(student_id: int)`<br>`search_document(query: str, top_k: int = 5)` | Đặt tên tham số rõ nghĩa, có kiểu dữ liệu (*Type hinting*) và giá trị mặc định rõ ràng. |
| **📖 Mô tả (Docstring)** | Trống hoặc mô tả sơ sài: *"Hàm xử lý quiz"* | *"Tạo bài kiểm tra trắc nghiệm dựa trên mã môn học và số lượng câu hỏi yêu cầu."* | Mô tả là hướng dẫn sử dụng trực tiếp cho LLM; giải thích rõ khi nào nên dùng và không nên dùng tool. |
| **🎯 Phạm vi trách nhiệm** | Một tool làm mọi việc: `manage_all(action="quiz_or_db")` | Tách biệt theo đơn nhiệm: `create_quiz()`, `query_database()` | Tuân thủ đơn nhiệm (*Single Responsibility*) giúp LLM không chọn nhầm tham số. |

---

## 🌐 4. Multi-Agent Systems & LangGraph – Khi Một Agent Không Còn Đủ

> [!NOTE]
> Khi phạm vi bài toán mở rộng, việc nhồi nhét mọi năng lực vào một **"siêu Agent" (Monolithic Agent)** duy nhất sẽ nhanh chóng chạm ngưỡng giới hạn kỹ thuật. Chuyển đổi sang kiến trúc **Multi-Agent** và sử dụng các framework quản lý luồng có trạng thái như **LangGraph** là bước tiến tất yếu để đưa hệ thống vào môi trường sản xuất.

---

### 💥 4.1. Sự Sụp Đổ Của Monolithic Agent & Nguyên Lý Chuyên Môn Hóa

Một Agent ôm đồm mọi vai trò (*Research, Tool call, Quiz generation, RAG, Memory, Planning, Long-form Writing*) sẽ đối mặt với các điểm nghẽn nghiêm trọng:

1. **Context Overload & Phân mảnh chú ý:** System prompt phình to, chứa hàng chục mô tả công cụ khiến LLM bị nhiễu và dễ chọn sai tool (*Tool Confusion*).
2. **Khó khăn trong kiểm thử & Debug:** Khi một bước trong chuỗi xử lý bị lỗi, rất khó xác định nguyên nhân do prompt, do retrieval, hay do logic suy luận.
3. **Bất khả thi khi scale team:** Nhiều kỹ sư cùng tinh chỉnh trên một prompt khổng lồ dễ gây xung đột hành vi (*Regression*).

#### 💡 Giải pháp: Specialization (Chuyên môn hóa)
Chia nhỏ hệ thống thành một mạng lưới gồm các Agent chuyên biệt, mỗi Agent sở hữu:
- Một System Prompt ngắn gọn, tập trung cao độ vào một miền trách nhiệm.
- Một tập hợp nhỏ các Tools liên quan trực tiếp.
- Ngữ cảnh cô đọng, giảm thiểu tiêu tốn token.

---

### 🤝 4.2. Các Mô Hình Cộng Tác Multi-Agent (Multi-Agent Patterns)

#### 👔 4.2.1. Supervisor – Worker (Quản lý và Thực thi)
Một Agent đầu nào đóng vai trò **Supervisor** (*Router / Orchestrator*) tiếp nhận yêu cầu từ người dùng, phân tích ý định và ủy quyền công việc cho các **Worker** chuyên trách:

```text
                      [User Request]
                            │
                            ▼
                    [Supervisor Agent]
                     (Route & Delegate)
                     /      │       \
                    /       │        \
                   ▼        ▼         ▼
           [Research Agent] [Tutor Agent] [Quiz Agent]
           - search_doc     - explain     - generate_quiz
           - summarize      - track_gap   - grade_answer
```

- **Ví dụ điều phối:**
  - *User:* `"Tôi chưa hiểu Attention Mechanism"` $\longrightarrow$ Supervisor chuyển việc cho **Tutor Agent** để giải thích và đặt câu hỏi gợi mở.
  - *User:* `"Nghiên cứu các kiến trúc RAG mới nhất"` $\longrightarrow$ Supervisor chuyển việc cho **Research Agent** để tìm kiếm và tổng hợp tài liệu.

#### 🔗 4.2.2. Sequential Pipeline (Xử lý tuần tự)
Áp dụng cho các bài toán phức tạp đòi hỏi độ sâu và tính xác thực cao (như *Deep Research, Code Generation & Audit*):

```text
[Start] ──► [Research Agent] ──► [Analysis Agent] ──► [Writer Agent] ──► [Fact-check Agent] ──► [End]
               (Thu thập)            (Phân tích)           (Soạn thảo)          (Hậu kiểm)
```
- Từng Agent hoàn thành một giai đoạn, đóng gói kết quả và bàn giao cho Agent tiếp theo làm đầu vào.

#### ⚡ 4.2.3. Parallel Execution (Thực thi song song)
Khi một bài toán lớn có thể phân rã thành các nhiệm vụ con độc lập, các Agent chạy đồng thời để tối ưu hóa thời gian phản hồi (*giảm Latency*):

```text
                        [User Query]
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
     [Search Agent A] [Search Agent B] [Search Agent C]
      (ArXiv Papers)   (Tech Blogs)     (GitHub Repos)
            └────────────────┬────────────────┘
                             │
                             ▼
                    [Synthesizer Agent]
                   (Tổng hợp & Chốt đáp án)
```

---

### 🔄 4.3. LangGraph: Quản Lý Luồng Trạng Thái và Chu Trình Lặp

Khi luồng làm việc của Agent trở nên phức tạp, các pipeline dạng DAG (*Directed Acyclic Graph*) truyền thống không còn đáp ứng được. **LangGraph** mô hình hóa hệ thống Agent dưới dạng một đồ thị có trạng thái (**Stateful Graph**) với 3 thành phần cốt lõi:

1. **State (Trạng thái trung tâm):** Cấu trúc dữ liệu dùng chung (*schema*) lưu trữ toàn bộ ngữ cảnh, tin nhắn, và kết quả trung gian giữa các nút.
2. **Nodes (Nút xử lý):** Đại diện cho các tác vụ cụ thể — có thể là một hàm Python, một LLM call, hoặc một Agent con. Mỗi Node nhận State hiện tại, xử lý và trả về phần cập nhật cho State.
3. **Edges (Cạnh điều hướng):**
   - **Normal Edge:** Nối trực tiếp từ Node A sang Node B.
   - **Conditional Edge:** Nút rẽ nhánh dựa trên logic điều kiện (ví dụ: đánh giá chất lượng câu trả lời để quyết định đi tiếp hay quay lại).

#### 🔁 Sức mạnh của Cyclic Workflow (Vòng lặp tự sửa sai)
Điểm vượt trội của LangGraph so với pipeline tĩnh nằm ở khả năng quay lui (*looping / cycles*) để tự đánh giá và hoàn thiện kết quả:

```text
                   [Start]
                      │
                      ▼
                  [Router]
                      │
                      ▼
                 [Retrieve]
                      │
                      ▼
                 [Generate]
                      │
                      ▼
                [Evaluate] ◄──────────────┐
                 /       \                │
           (Good)         (Not good)      │
             /             \              │
            ▼               ▼             │
          [End]     [Rewrite Query] ──────┘
                     (Retrieve lại)
```

- **Generate:** Sinh bản nháp hoặc câu trả lời ban đầu.
- **Evaluate (Evaluator Node):** Đánh giá xem câu trả lời có đạt yêu cầu hay tài liệu truy xuất có đủ thông tin không.
- **Looping:**
  - *Nếu Đạt (Good):* Kết thúc luồng (`[End]`) và trả kết quả cho người dùng.
  - *Nếu Chưa đạt (Not good):* Không dừng lại hay trả kết quả lỗi, mà chuyển hướng sang bước viết lại truy vấn (`[Rewrite Query]`), tìm kiếm lại ngữ cảnh và lặp lại chu trình cho đến khi đạt chất lượng.

---

### 📊 4.4. So Sánh Tổng Quan Kiến Trúc

| Tiêu chí | Monolithic Agent | Multi-Agent (Supervisor/Pipeline) | LangGraph Workflow |
| :--- | :--- | :--- | :--- |
| **🎮 Cơ chế điều khiển** | 1 LLM điều phối tất cả | LLM Supervisor phân việc | Đồ thị State Machine kết hợp Code & LLM |
| **🧠 Quản lý ngữ cảnh** | Dễ tràn Context Window | Tách biệt theo từng Agent con | Quản lý tập trung qua Shared State Schema |
| **🔁 Khả năng lặp lại** | Hạn chế, dễ lặp vô tận | Phụ thuộc prompt | Rất mạnh, kiểm soát chặt bằng Conditional Edges |
| **🛡️ Độ tin cậy** | Thấp trên tác vụ phức tạp | Trung bình - Khá | **Cao**, dễ test từng Node độc lập |

---

## 🚀 5. Production, Reliability & Security – Đưa Agent Ra Thực Tế

### 💸 5.1. Cân Bằng Cost & Latency (Chi Phí & Độ Trễ)

Trong một kiến trúc Agentic Workflow:
- Một câu hỏi đơn giản của người dùng có thể kích hoạt chuỗi: $\text{Router LLM} \longrightarrow \text{Research LLM} \longrightarrow \text{Tool Evaluator LLM} \longrightarrow \text{Writer LLM}$.
- Một lượt tương tác đơn lẻ tốn từ 4–5 lượt gọi API, tiêu thụ hàng nghìn tokens với độ trễ cộng dồn lên tới hàng chục giây.
- **Quy mô Production:** 1.000 users đồng thời sẽ khiến chi phí API bùng nổ theo cấp số nhân và hệ thống đối mặt với nghẽn cổ chai (*rate limit / timeout*).

#### 💡 Giải pháp kỹ thuật:
1. **Model Tiering (Phân tầng mô hình):** Dùng model nhỏ, rẻ, nhanh (ví dụ: *Haiku, GPT-4o-mini, Flash*) cho các tác vụ phân loại/router, trích xuất tham số; chỉ dùng model lớn (*Opus, GPT-4o, Sonnet*) cho bước lập luận phức tạp và tổng hợp cuối cùng.
2. **Semantic Caching:** Cache kết quả của các truy vấn / tool call tương đồng để tránh gọi lại LLM.
3. **Streaming & Async Execution:** Stream kết quả từng phần về UI để giảm cảm giác chờ đợi của người dùng (giảm *Perceived Latency*).

---

### 👁️ 5.2. Observability & Tracing (Khả Năng Quan Sát & Truy Vết)

Không thể sửa lỗi nếu không biết Agent đang suy luận điều gì bên trong "hộp đen". Hệ thống production bắt buộc phải gắn `Request ID` và lưu vết toàn diện (*End-to-End Tracing*) qua các nền tảng như LangSmith, Arize Phoenix hoặc OpenTelemetry:

```text
[Trace Log: Request ID #1800291]
├── Router Node: Phân loại intent -> "deep_research" (Latency: 0.8s, Cost: $0.0002)
├── Tool Call: search_documents("Attention mechanism", top_k=8) (Latency: 1.2s)
├── Reranker Node: Lọc 8 docs -> Top 3 docs phù hợp (Latency: 0.3s)
├── LLM Generation: 1,240 tokens (Latency: 3.2s, Cost: $0.006)
└── Status: 200 OK | Total Latency: 5.5s | Total Cost: $0.0062
```

> [!TIP]
> **Phân tích nguyên nhân gốc (Root Cause Analysis):** Khi người dùng phàn nàn Agent trả lời sai, kỹ sư truy vết ngược cây execution: *Do Router phân loại nhầm? Do Retrieval lấy sai chunk? Hay do LLM ảo giác dù context đúng?*

---

### 🗄️ 5.3. State Inspection & Long-term Persistence

Agent không thể xem như stateless server thông thường mà cần cơ chế lưu giữ trạng thái:

#### 🔍 5.3.1. State Inspection (Soi trạng thái)
Định nghĩa cấu trúc Schema tường minh để debug khi Agent gặp lỗi logic:

```json
{
  "user_id": "usr_9981",
  "current_topic": "Attention Mechanism",
  "knowledge_level": "Intermediate",
  "weak_points": ["Re-ranking", "Self-Attention vs Cross-Attention"],
  "retrieved_doc_ids": ["doc_12", "doc_88"]
}
```

#### 🧠 5.3.2. Long-term Persistence (Ký ức dài hạn)
- Agent xuất sắc không quên ngữ cảnh sau khi phiên kết thúc.
- Lưu trạng thái người dùng vào Database / Vector Store.
- Hôm sau người dùng quay lại, Agent tải lại State cũ và chào đón tự nhiên: *"Hôm trước chúng ta đã nắm vững Self-Attention, hôm nay bạn có muốn đi tiếp phần Cross-Attention không?"*.

---

### 🧪 5.4. Automated Evaluation & Harness Engineering

> [!WARNING]
> Đừng bao giờ test Agent bằng cách "chat thử 5 câu rồi release". Mọi thay đổi trong Prompt, Code hay Model đều có thể tạo ra lỗi tiềm ẩn (*Regression*).

#### 🎯 Evaluation Benchmark
Xây dựng tập dữ liệu kiểm thử vàng (*Golden Dataset*) gồm hàng trăm test cases:
- **Input:** Câu hỏi hoặc tình huống edge-case.
- **Expected Behavior:** Tool nào bắt buộc phải gọi, schema tham số là gì, câu trả lời mong đợi ra sao.

#### 📈 Bộ chỉ số đo lường (Eval Metrics)

| Chỉ số | Mục tiêu kiểm tra | Ngưỡng an toàn khuyến nghị |
| :--- | :--- | :--- |
| **🎯 Intent Accuracy** | Tỷ lệ nhận diện đúng mục đích người dùng | $> 95\%$ |
| **🛠️ Tool Selection Accuracy** | Tỷ lệ chọn đúng công cụ và điền đúng tham số | $> 92\%$ |
| **🛡️ Groundedness (Faithfulness)** | Câu trả lời có bám sát context truy xuất, không bịa đặt | $> 90\%$ |
| **🎯 Answer Relevance** | Mức độ bám sát trọng tâm câu hỏi của người dùng | $> 90\%$ |

---

### 🛡️ 5.5. Security & Safety: HITL, Sandboxing & PII Masking

Agent sở hữu khả năng thực thi hành động (*Action-taking*), do đó nguy cơ an ninh cao hơn chatbot truyền thống gấp nhiều lần.

#### ⚖️ 5.5.1. Phân tầng Rủi ro & Human-in-the-Loop (HITL)

| Cấp độ rủi ro | Hành động mẫu | Cơ chế xử lý |
| :--- | :--- | :--- |
| **🟢 Low Risk** | Tìm kiếm tài liệu, giải thích bài, đọc dữ liệu | Agent tự động $100\%$ |
| **🟡 Medium Risk** | Chấm bài tự động, gửi email thông báo lớp học | Agent xử lý + Bộ lọc Validation / Threshold (Confidence $< 0.9 \rightarrow$ đẩy người duyệt) |
| **🔴 High Risk** | Xóa database, chuyển khoản $> 10.000\$$ | **Bắt buộc Human Approval (HITL)** (Tạm dừng execution graph, chờ con người ấn Approve trên dashboard mới chạy tiếp) |

#### 📦 5.5.2. Code Execution Sandboxing
- Nếu Agent có năng lực sinh và chạy code (*Python interpreter*): Tuyệt đối không chạy trực tiếp trên Production Server.
- Bắt buộc chạy trong Sandbox cô lập (Docker container dùng một lần, Firecracker MicroVM, gVisor).
- **Cấu hình nghiêm ngặt:** Giới hạn CPU/RAM (ví dụ tối đa 512MB), ngắt quyền truy cập Internet ra ngoài, cấm can thiệp file hệ thống nhạy cảm.

#### 🔒 5.5.3. PII Masking (Khử định danh thông tin cá nhân)
Trước khi gửi prompt ra các LLM API bên ngoài, hệ thống phải chạy qua lớp lọc Regex/NER để làm mờ dữ liệu cá nhân:
- **Raw:** *"Tôi là Nguyễn Văn A, CCCD: 079123456789, sđt: 0901234567"*
- **Masked:** *"Tôi là `[NAME_1]`, CCCD: `[ID_1]`, sđt: `[PHONE_1]`"*
- Khi LLM trả lời, bộ giải mã nội bộ (*De-masker*) mới chuyển ngược lại thông tin cho người dùng.

---

### 🏛️ 5.6. Bức Tranh Tổng Thể: Hệ Thống AI Agent Hoàn Chỉnh (5 Chương)

Sơ đồ kiến trúc hoàn chỉnh tích hợp toàn bộ tri thức của 5 chương:

```text
                            [USER]
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. INGESTION & CONTEXT ENGINEERING (Chương 2)                │
│    - PII Masking & Security Check                           │
│    - RTCF Prompt Structure (Role - Task - Context - Format) │
│    - Few-shot Routing & Dynamic Context Injection           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. CORE AGENT ENGINE (Chương 3 & 4)                          │
│    - Planning & Reasoning: CoT / ToT                        │
│    - State & Memory: Persistent History + Active State      │
│    - Routing Architecture:                                  │
│         ├── Single Agent ReAct Loop (Chương 3)              │
│         └── Multi-Agent / LangGraph Cyclic Graph (Chương 4) │
└──────────────────────────────┬──────────────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
       [Low/Med Risk Actions]         [High Risk Actions]
                │                             │
                │                             ▼
                │                    [Human-in-the-Loop]
                │                    (Chờ con người duyệt)
                │                             │
                └──────────────┬──────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. STANDARDIZED INTEGRATION LAYER (Chương 1)                 │
│    - Protocol: Model Context Protocol (MCP Client)          │
│    - JSON-RPC Transport (stdio / SSE)                       │
│    - Primitives: Resources | Prompts | Tools                │
└──────────────────────────────┬──────────────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
    [MCP Server: RAG]   [MCP Server: APIs]   [MCP Server: Sandbox]
    - Vector Search     - Internal CRM/ERP   - Isolated Code Exec
    - Docs Chunks       - Payment Gateway    - Resource Constrained
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. OBSERVATION & EVALUATION (Chương 3 & 4)                   │
│    - Parse Tool Result / Observation                        │
│    - Evaluate: Đủ dữ liệu chưa? (Cycle Loop nếu chưa đạt)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
                            [ANSWER]
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. PRODUCTION, RELIABILITY & MONITORING (Chương 5)          │
│    - Tracing & Logs (LangSmith/OpenTelemetry)               │
│    - Token Cost & Latency Optimization                      │
│    - Automated Evals: Groundedness, Faithfulness, Accuracy  │
└──────────────────────────────┴──────────────────────────────┘
```

> [!NOTE]
> **Tóm tắt hành trình 5 chương:**
> - **Chương 1:** Chuẩn hóa giao tiếp (MCP - USB-C cho AI).
> - **Chương 2:** Định hình tư duy (Prompt & Context Engineering).
> - **Chương 3:** Tối ưu ngữ cảnh & công cụ (Context Management & Tool Design).
> - **Chương 4:** Mở rộng phối hợp (Multi-Agent Systems & LangGraph).
> - **Chương 5:** Đảm bảo vận hành an toàn & tin cậy ở quy mô sản xuất (Production, Reliability & Security).




