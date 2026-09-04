# 🚀 Learn AI Engineer With Me

Kho lưu trữ tài liệu, kiến thức và dự án thực hành trên lộ trình trở thành **AI Engineer** toàn diện (từ nền tảng lý thuyết, kiến trúc Agent, fine-tuning/alignment đến thiết kế sản phẩm và vận hành hệ thống production đáng tin cậy).

---

## 📚 Danh mục tài liệu & Đường dẫn bài học (.md)

Bảng tổng hợp toàn bộ các đường dẫn tài liệu học tập Markdown trong kho lưu trữ:

### 1. Nền Tảng AI & Large Language Models
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **Foundation AI & LLM (Toàn diện)** | [Foundation ai and llm.md](Foundation%20AI%20&%20LLM/guide/Foundation%20ai%20and%20llm.md) | Cẩm nang kiến trúc hệ thống AI 13 bước: Problem Discovery, Rule vs AI, Automation vs Augmentation, Reward Design, Precision & Recall, 3 Cấp độ kiến trúc (Workflow vs Agent), Tokenization & Attention, Pre-training & RLHF, ReAct & Function Calling, Hybrid Routing & Retrieval, Citation, RAG Triad, Probabilistic Design, Fallback/HITL, Observability, Golden Dataset, LLM-as-a-Judge. |

---

### 2. Chuyên Đề RAG (Retrieval-Augmented Generation) & Semantic Search
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **Tổng quan RAG** | [rag-learning/README.md](rag-learning/README.md) | Giới thiệu RAG, kiến trúc 2 luồng và cấu trúc dự án. |
| **Giáo trình RAG toàn diện** | [rag-learning/guide/ALL_RAG.md](rag-learning/guide/ALL_RAG.md) | **5 chương** lý thuyết, toán học và kỹ thuật RAG: <br>• *Chương 1:* Foundation & Evolution (Embedding, Dense Space, Cosine Similarity, Vector DB).<br>• *Chương 2:* Offline Ingestion (Parsing, OCR, Chunking, Metadata).<br>• *Chương 3:* Online Retrieval (Query Transformation, Hybrid Search, Reranking).<br>• *Chương 4:* Graph RAG & Advanced Architectures (Self-RAG, CRAG, Agentic RAG).<br>• *Chương 5:* Evaluation & Operationalization (RAG Triad, RAGAS, Latency & Cost). |
| **Tổng quan Semantic Search** | [senatic-search/README.md](senatic-search/README.md) | Giới thiệu dự án Semantic Search và cách vận hành. |
| **Báo cáo nghiên cứu (Paper)** | [senatic-search/guide/paper.md](senatic-search/guide/paper.md) | Nghiên cứu chi tiết: *How Computers Search by Meaning*, Vector Embeddings & Similarity. |
| **Hiểu sâu về Embeddings** | [senatic-search/guide/01_understanding_embeddings.md](senatic-search/guide/01_understanding_embeddings.md) | Bản chất biểu diễn vector của từ và câu. |
| **Độ tương đồng Vector** | [senatic-search/guide/02_vector_similarity.md](senatic-search/guide/02_vector_similarity.md) | Các thuật toán đo khoảng cách vector trong không gian đa chiều. |

---

### 3. Kiến Trúc Agentic AI (Agentic Architectures)
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **Kiến trúc Agentic AI toàn tập** | [Agent-arc/guide/agent-arc.md](Agent-arc/guide/agent-arc.md) | **8 chương** chuyên sâu về kiến trúc Agent:<br>• *Chương 1:* Tổng thể Agentic AI & Phân tầng phát triển.<br>• *Chương 2:* ReAct Framework, Autonomy Levels, Agentic Fit (R-T-D-H).<br>• *Chương 3:* Agentic Workflow Patterns (Chaining, Routing, Parallelization, Orchestrator-Workers, Evaluator-Optimizer).<br>• *Chương 4:* Multi-Agent Systems (Divide & Conquer, Specialization, Debate, Parallel Research).<br>• *Chương 5:* Advanced Architectures (Plan-Act-Verify, Reflection, Skill Accumulation).<br>• *Chương 6:* LangGraph & Orchestration (StateGraph, Checkpoints, HITL).<br>• *Chương 7:* Memory Systems (Short-term, Long-term, Episodic vs Semantic).<br>• *Chương 8:* Guardrails, Sandboxing & Deep Research Agent Architecture. |

---

### 4. Đánh Giá Hệ Thống & Guardrails (RAG Evaluation & Safety)
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **RAG Evaluation & Guardrails** | [Evaluation and guardrails/guide/rag-evaluation.md](Evaluation%20and%20guardrails/guide/rag-evaluation.md) | **7 chương** quy chuẩn đánh giá và an toàn hệ thống AI:<br>• *Chương 1:* Đánh giá hệ thống RAG & Golden Dataset.<br>• *Chương 2:* Core 4 Metrics (Context Recall/Precision, Faithfulness, Relevance).<br>• *Chương 3:* Synthetic Test Dataset & RAGAS Automation.<br>• *Chương 4:* LLM-as-a-Judge, Triệt tiêu Biases & Hybrid Evaluation.<br>• *Chương 5:* 5 Lớp AI Guardrails (Input, Injection, Execution, Output, HITL).<br>• *Chương 6:* Human-in-the-Loop (Ma trận rủi ro 3 cấp & Interrupt Design).<br>• *Chương 7:* Responsible AI, PII Redaction & Production SLA Benchmarking. |

---

### 5. Phát Triển & Chuẩn Hóa AI Agent (Development & Standardization)
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **AI Agent Development & Standardization** | [Ai agent development and standardization/guide/AI Agent Development & Standardization.md](Ai%20agent%20development%20and%20standardization/guide/AI%20Agent%20Development%20%26%20Standardization.md) | **5 chương** chuẩn hóa và phát triển Agent:<br>• *Chương 1:* Model Context Protocol (MCP - Chuẩn USB-C cho AI Agent).<br>• *Chương 2:* Prompt & Context Engineering (RTCF, Few-shot, CoT, ToT, Self-Consistency).<br>• *Chương 3:* Context Management & Tool Design (Trimming, Summarization, ReAct Loop).<br>• *Chương 4:* Multi-Agent Systems & LangGraph Cyclic Workflows.<br>• *Chương 5:* Production Reliability, Tracing, Sandboxing, PII Masking & Complete 5-Layer Architecture. |

---

### 6. Fine-Tuning & Alignment LLMs
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **Fine-Tuning and Alignment LLMs** | [Fine-tuning and Alignment llms/guide/Fine-tuning and Alignment llms.md](Fine-tuning%20and%20Alignment%20llms/guide/Fine-tuning%20and%20Alignment%20llms.md) | **9 chương** chuyên sâu huấn luyện & căn chỉnh LLM:<br>• *Chương 1:* Bức tranh tổng thể về Fine-Tuning & Alignment (Nghịch lý tri thức Base LLM, 4 trụ cột kỹ thuật).<br>• *Chương 2:* Khi nào thực sự cần Fine-Tuning LLM? (Style & Format, Specialized Skills, Prompt Fatigue, Cost & Latency).<br>• *Chương 3:* Prompting, RAG và Fine-Tuning (Case Study Chatbot Sinh Viên, Bảng quy tắc lựa chọn công nghệ, Kiến trúc chuỗi thực tế).<br>• *Chương 4:* LoRA & QLoRA – Fine-Tune với tài nguyên nhỏ (Math decomposition $\Delta W = \frac{\alpha}{r}(B \times A)$, Adapter, 4-bit NF4, Double Quantization, Paged Optimizers).<br>• *Chương 5:* PEFT Pipeline Thực Tế SFT (SFT Dataset Alpaca/ShareGPT, Data Masking `label = -100`, LoraConfig, SFTTrainer code Python).<br>• *Chương 6:* SFT Tốt Nhưng Chưa Đủ – Bước đệm cho RLHF (Imitation Learning vs Human Preference Data).<br>• *Chương 7:* RLHF – Căn chỉnh bằng Human Feedback (4 giai đoạn, Reward Model, PPO, Reward Hacking & $D_{KL}$ penalty).<br>• *Chương 8:* Direct Alignment – DPO, ORPO & SimPO (DPO Loss function, ORPO 1-step, SimPO loại bỏ Reference Model & Phạt thiên vị độ dài).<br>• *Chương 9:* GRPO, RLVR, Constitutional AI & Red Teaming (GRPO Group Relative Rewards, RLVR Verifiable Rewards cho Math/Code, Self-Critique/Revision, Red Teaming, Production Roadmap). |

---

### 7. AI Product Management & Human-in-the-Loop UX
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **AI Product & UX Management** | [AI Product and UX Management/guide/AI Product and UX Management.md](AI%20Product%20and%20UX%20Management/guide/AI%20Product%20and%20UX%20Management.md) | **6 chương** quản trị sản phẩm AI & thiết kế HITL UX:<br>• *Chương 1:* Dịch chuyển tư duy & Cải tiến Scrum trong dự án AI (Từ Task sang Giả thuyết, Sprint Planning/Refinement/Review).<br>• *Chương 2:* Thử nghiệm MVE First & Công cụ Low-code/No-code PoC (MVE vs MVP, Feasibility Risk, Playgrounds/Flowise/Streamlit).<br>• *Chương 3:* Quản trị Stakeholder, ROI & Pitch Deck (Expectation Gap, mô hình tài chính ROI 3-6-12 tháng, Pitch Deck 6 slides).<br>• *Chương 4:* Rủi ro Full Autonomy & 5 Mô hình HITL Interaction (Approval, Editing, Escalation, Co-Pilot, Audit).<br>• *Chương 5:* Cơ chế Định tuyến theo Độ tự tin & Interrupts (Confidence Routing High/Medium/Low, Tiêu chí ngắt luồng khẩn cấp).<br>• *Chương 6:* Vòng lặp phản hồi, Audit Trails & UX Best Practices (Explicit/Implicit Feedback, Audit Log cấu trúc, 5 nguyên tắc chống Alert Fatigue). |

---

### 8. Vận Hành Hệ Thống Production Đáng Tin Cậy (Reliable AI Systems)
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **Reliable AI Agent Production Systems** | [Reliable ai agent production systems/guide/Reliable ai agent production systems.md](Reliable%20ai%20agent%20production%20systems/guide/Reliable%20ai%20agent%20production%20systems.md) | **8 chương** hạ tầng & vận hành Agent Production đáng tin cậy:<br>• *Chương 1:* Từ BI Pipeline sang RAG/Agent Corpus & 4 Giai đoạn Data Pipeline (Fail Loudly vs Fail Silently, Ingestion, Transformation, Storage, Serving).<br>• *Chương 2:* Kiểm soát chất lượng dữ liệu & 5 Trụ cột Data Observability (Data Contracts, Quality Gates, Sơ đồ dịch chuyển lỗi, 5 trụ cột Observability).<br>• *Chương 3:* Dockerization & Đặc tính hạ tầng của Agent (Environment Parity, Multi-stage Dockerfile, `uv`, Non-root User).<br>• *Chương 4:* Thách thức vận hành & Lựa chọn hạ tầng Cloud (Long-running, Stateful, Cost Overflow, Timeout & Serverless/PaaS/VPS/Managed Runtimes).<br>• *Chương 5:* 4 Trụ cột AI Observability & Cảnh báo P99 Latency (Metrics, Logs, Traces Waterfall, Continuous Eval & P99 Analysis).<br>• *Chương 6:* Structured Logging & Công cụ LLM Observability (JSON Format, Correlation ID, PII Redaction, Langfuse/LangSmith/Arize Phoenix/Helicone).<br>• *Chương 7:* Các dạng sự cố & Cơ chế cầu dao cảnh báo Circuit Breaker (Infinite Loops, API Outage, Sơ đồ 3 trạng thái CLOSED/OPEN/HALF-OPEN).<br>• *Chương 8:* Chuỗi dự phòng Fallback Chain & Semantic Caching (Model Fallback, Graceful Degradation, Cache ngữ nghĩa & Stale responses warning). |

---

## 🧭 Lộ trình phát triển tiếp theo (Roadmap)

- [x] **Foundation AI & LLM Systems:** LLM Mechanics, Probabilistic Design, Fallback & HITL.
- [x] **RAG & Vector Search:** Offline Ingestion, Hybrid Search, Graph RAG, Reranking & Evaluation.
- [x] **Agentic AI & Multi-Agent Systems:** ReAct, Workflow Patterns, Specialization, LangGraph StateGraph.
- [x] **Evaluation, Guardrails & Responsible AI:** Golden Dataset, RAGAS, LLM-as-a-Judge, 5-Layer Guardrails, SLA Benchmarking.
- [x] **AI Agent Development & MCP Standardization:** Model Context Protocol (MCP), Context Management, Tool Design Principles.
- [x] **LLM Fine-Tuning & Alignment:** PEFT, LoRA, QLoRA, SFT Pipeline, RLHF, DPO, ORPO, SimPO, GRPO, RLVR, Constitutional AI.
- [x] **AI Product Management & HITL UX:** MVE First, Scrum for AI, ROI Model, 5 HITL Interaction Patterns, Confidence Routing.
- [x] **Reliable AI Production Systems:** Data Observability, Dockerization, Long-running Cloud Runtimes, P99 Latency Tracing, Circuit Breakers & Semantic Caching.
- [ ] **Multimodal AI:** Vision-Language Models (VLM), Audio/Video AI.
- [ ] **High-Performance LLM Serving & Inference Engines:** vLLM, Ollama, TensorRT-LLM, DeepSpeed.

---

## 📂 Cấu trúc Repository

```
Learn-AI-engineer-with-me/
├── .gitignore                                  # Quản lý bỏ qua cache, venv, secrets
├── .env.example                                # Mẫu cấu hình API keys và môi trường
├── requirements.txt                            # Thư viện dùng chung toàn bộ repo
├── Agent-arc/                                  # Chuyên đề Kiến trúc Agentic AI
│   ├── guide/                                  # Giáo trình & sơ đồ kiến trúc
│   │   ├── agent-arc.md                        # Giáo trình 8 chương Agentic Architectures
│   │   └── agent arc.png                       # Sơ đồ tổng quan kiến trúc Agent
│   ├── agent/                                  # Module triển khai Agent & Router
│   ├── rag/                                    # Module RAG
│   ├── llm/                                    # Client kết nối LLM
│   └── app.py                                  # Điểm khởi chạy ứng dụng
├── AI Product and UX Management/               # Chuyên đề Quản trị Sản phẩm AI & HITL UX
│   └── guide/
│       ├── AI Product and UX Management.md     # Giáo trình 6 chương Product Management & HITL UX
│       └── AI Product and UX Management.png    # Sơ đồ tổng quan HITL UX & Product Workflow
├── Ai agent development and standardization/  # Chuyên đề Phát triển & Chuẩn hóa AI Agent
│   └── guide/
│       ├── AI Agent Development & Standardization.md # Giáo trình 5 chương MCP & Agent Development
│       └── Ai agent development and standardization.png # Sơ đồ tổng quan hệ thống Agent
├── Evaluation and guardrails/                  # Chuyên đề Đánh giá hệ thống & Guardrails
│   └── guide/
│       ├── rag-evaluation.md                   # Giáo trình 7 chương RAG Evaluation & Safety
│       └── Evaluation and guardrails.png       # Sơ đồ 5 lớp Guardrails & Benchmark
├── Fine-tuning and Alignment llms/             # Chuyên đề Huấn luyện & Căn chỉnh LLMs
│   └── guide/
│       ├── Fine-tuning and Alignment llms.md   # Giáo trình 9 chương Fine-Tuning & Alignment
│       └── Fine-tuning and Alignment llms.png  # Sơ đồ tổng quan Fine-Tuning & Alignment Pipeline
├── Foundation AI & LLM/                        # Kiến thức nền tảng AI, Deep Learning & LLMs
│   └── guide/
│       ├── Foundation ai and llm.md            # Cẩm nang 13 bước nền tảng AI & LLM
│       └── foundationAI and llm.png            # Sơ đồ nền tảng Foundation AI
├── rag-learning/                               # Chuyên đề RAG từ lý thuyết đến triển khai
│   ├── guide/                                  # Giáo trình & Mind Map RAG
│   │   ├── ALL_RAG.md                          # Giáo trình 5 chương RAG toàn diện
│   │   └── RAG Mind Map.png                    # Sơ đồ tư duy RAG
│   ├── src/                                    # Mã nguồn pipeline RAG
│   ├── experiments/                            # Thử nghiệm chunking, embedding, retrieval
│   ├── tests/                                  # Kiểm thử unit test & benchmark
│   └── README.md                               # Giới thiệu & mục lục RAG
├── Reliable ai agent production systems/       # Chuyên đề Vận hành hệ thống Production đáng tin cậy
│   └── guide/
│       ├── Reliable ai agent production systems.md # Giáo trình 8 chương Production Systems & Reliability
│       └── Reliable ai agent production systems.png # Sơ đồ tổng quan Data Observability & Circuit Breakers
├── senatic-search/                             # Chuyên đề Semantic Search & Vector Similarity
│   ├── guide/                                  # Tài liệu hướng dẫn & Paper nghiên cứu
│   │   ├── paper.md
│   │   ├── 01_understanding_embeddings.md
│   │   └── 02_vector_similarity.md
│   ├── src/                                    # Mã nguồn tìm kiếm ngữ nghĩa
│   └── README.md                               # Giới thiệu Semantic Search
└── README.md                                   # Tổng quan repository & Trích xuất đường dẫn học tập
```
