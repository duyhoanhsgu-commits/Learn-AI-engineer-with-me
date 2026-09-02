# 🚀 Learn AI Engineer With Me

Kho lưu trữ tài liệu, kiến thức và dự án thực hành trên lộ trình trở thành **AI Engineer** toàn diện (từ nền tảng lý thuyết đến triển khai hệ thống production).

---

## 📚 Danh mục tài liệu & Đường dẫn bài học (.md)

Bảng tổng hợp toàn bộ các đường dẫn tài liệu học tập Markdown trong kho lưu trữ:

### 1. Nền Tảng AI & Large Language Models
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **Foundation AI & LLM (Toàn diện)** | [Foundation ai and llm.md](Foundation%20AI%20&%20LLM/Foundation%20ai%20and%20llm.md) | Cẩm nang kiến trúc hệ thống AI 13 bước: Problem Discovery, Rule vs AI, Automation vs Augmentation, Reward Design, Precision & Recall, 3 Cấp độ kiến trúc (Workflow vs Agent), Tokenization & Attention, Pre-training & RLHF, ReAct & Function Calling, Hybrid Routing & Retrieval, Citation, RAG Triad, Probabilistic Design, Fallback/HITL, Observability, Golden Dataset, LLM-as-a-Judge. |

---

### 2. Chuyên Đề RAG (Retrieval-Augmented Generation) & Semantic Search
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **Tổng quan RAG** | [rag-learning/README.md](rag-learning/README.md) | Giới thiệu RAG, kiến trúc 2 luồng và cấu trúc dự án. |
| **Giáo trình RAG toàn diện** | [rag-learning/docs/ALL_RAG.md](rag-learning/docs/ALL_RAG.md) | **5 chương** lý thuyết, toán học và kỹ thuật RAG: <br>• *Chương 1:* Foundation & Evolution (Embedding, Dense Space, Cosine Similarity, Vector DB).<br>• *Chương 2:* Offline Ingestion (Parsing, OCR, Chunking, Metadata).<br>• *Chương 3:* Online Retrieval (Query Transformation, Hybrid Search, Reranking).<br>• *Chương 4:* Graph RAG & Advanced Architectures (Self-RAG, CRAG, Agentic RAG).<br>• *Chương 5:* Evaluation & Operationalization (RAG Triad, RAGAS, Latency & Cost). |
| **Tổng quan Semantic Search** | [senatic-search/README.md](senatic-search/README.md) | Giới thiệu dự án Semantic Search và cách vận hành. |
| **Báo cáo nghiên cứu (Paper)** | [senatic-search/guides/paper.md](senatic-search/guides/paper.md) | Nghiên cứu chi tiết: *How Computers Search by Meaning*, Vector Embeddings & Similarity. |
| **Hiểu sâu về Embeddings** | [senatic-search/guides/01_understanding_embeddings.md](senatic-search/guides/01_understanding_embeddings.md) | Bản chất biểu diễn vector của từ và câu. |
| **Độ tương đồng Vector** | [senatic-search/guides/02_vector_similarity.md](senatic-search/guides/02_vector_similarity.md) | Các thuật toán đo khoảng cách vector trong không gian đa chiều. |

---

### 3. Kiến Trúc Agentic AI (Agentic Architectures)
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **Kiến trúc Agentic AI toàn tập** | [Agent-arc/agent-arc.md](Agent-arc/agent-arc.md) | **8 chương** chuyên sâu về kiến trúc Agent:<br>• *Chương 1:* Tổng thể Agentic AI & Phân tầng phát triển.<br>• *Chương 2:* ReAct Framework, Autonomy Levels, Agentic Fit (R-T-D-H).<br>• *Chương 3:* Agentic Workflow Patterns (Chaining, Routing, Parallelization, Orchestrator-Workers, Evaluator-Optimizer).<br>• *Chương 4:* Multi-Agent Systems (Divide & Conquer, Specialization, Debate, Parallel Research).<br>• *Chương 5:* Advanced Architectures (Plan-Act-Verify, Reflection, Skill Accumulation).<br>• *Chương 6:* LangGraph & Orchestration (StateGraph, Checkpoints, HITL).<br>• *Chương 7:* Memory Systems (Short-term, Long-term, Episodic vs Semantic).<br>• *Chương 8:* Guardrails, Sandboxing & Deep Research Agent Architecture. |

---

### 4. Đánh Giá Hệ Thống & Guardrails (RAG Evaluation & Safety)
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **RAG Evaluation & Guardrails** | [Evaluation and guardrails/rag-evaluation.md](Evaluation%20and%20guardrails/rag-evaluation.md) | **7 chương** quy chuẩn đánh giá và an toàn hệ thống AI:<br>• *Chương 1:* Đánh giá hệ thống RAG & Golden Dataset.<br>• *Chương 2:* Core 4 Metrics (Context Recall/Precision, Faithfulness, Relevance).<br>• *Chương 3:* Synthetic Test Dataset & RAGAS Automation.<br>• *Chương 4:* LLM-as-a-Judge, Triệt tiêu Biases & Hybrid Evaluation.<br>• *Chương 5:* 5 Lớp AI Guardrails (Input, Injection, Execution, Output, HITL).<br>• *Chương 6:* Human-in-the-Loop (Ma trận rủi ro 3 cấp & Interrupt Design).<br>• *Chương 7:* Responsible AI, PII Redaction & Production SLA Benchmarking. |

---

### 5. Phát Triển & Chuẩn Hóa AI Agent (Development & Standardization)
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **AI Agent Development & Standardization** | [Ai agent development and standardization/AI Agent Development & Standardization.md](Ai%20agent%20development%20and%20standardization/AI%20Agent%20Development%20%26%20Standardization.md) | **5 chương** chuẩn hóa và phát triển Agent:<br>• *Chương 1:* Model Context Protocol (MCP - Chuẩn USB-C cho AI Agent).<br>• *Chương 2:* Prompt & Context Engineering (RTCF, Few-shot, CoT, ToT, Self-Consistency).<br>• *Chương 3:* Context Management & Tool Design (Trimming, Summarization, ReAct Loop).<br>• *Chương 4:* Multi-Agent Systems & LangGraph Cyclic Workflows.<br>• *Chương 5:* Production Reliability, Tracing, Sandboxing, PII Masking & Complete 5-Layer Architecture. |

---

## 🧭 Lộ trình phát triển tiếp theo (Roadmap)

- [x] **Foundation AI & LLM Systems:** LLM Mechanics, Probabilistic Design, Fallback & HITL.
- [x] **RAG & Vector Search:** Offline Ingestion, Hybrid Search, Graph RAG, Reranking & Evaluation.
- [x] **Agentic AI & Multi-Agent Systems:** ReAct, Workflow Patterns, Specialization, LangGraph StateGraph.
- [x] **Evaluation, Guardrails & Responsible AI:** Golden Dataset, RAGAS, LLM-as-a-Judge, 5-Layer Guardrails, SLA Benchmarking.
- [x] **AI Agent Development & MCP Standardization:** Model Context Protocol (MCP), Context Management, Tool Design Principles.
- [ ] **LLM Fine-tuning & Optimization:** PEFT, LoRA, QLoRA, DPO, RLHF.
- [ ] **Multimodal AI:** Vision-Language Models (VLM), Audio/Video AI.
- [ ] **LLMOps & High-Performance Serving:** vLLM, Ollama, TensorRT-LLM, OpenTelemetry Tracing.

---

## 📂 Cấu trúc Repository

```
Learn-AI-engineer-with-me/
├── Agent-arc/                                  # Chuyên đề Kiến trúc Agentic AI
│   ├── agent-arc.md                            # Giáo trình 8 chương Agentic Architectures
│   └── agent arc.png                           # Sơ đồ tổng quan kiến trúc Agent
├── Ai agent development and standardization/  # Chuyên đề Phát triển & Chuẩn hóa AI Agent
│   ├── AI Agent Development & Standardization.md # Giáo trình 5 chương MCP & Agent Development
│   └── Ai agent development and standardization.png # Sơ đồ tổng quan hệ thống Agent
├── Evaluation and guardrails/                  # Chuyên đề Đánh giá hệ thống & Guardrails
│   ├── rag-evaluation.md                       # Giáo trình 7 chương RAG Evaluation & Safety
│   └── Evaluation and guardrails.png           # Sơ đồ 5 lớp Guardrails & Benchmark
├── Foundation AI & LLM/                        # Kiến thức nền tảng AI, Deep Learning & LLMs
│   └── Foundation ai and llm.md                # Cẩm nang 13 bước nền tảng AI & LLM
├── rag-learning/                               # Chuyên đề RAG từ lý thuyết đến triển khai
│   ├── docs/ALL_RAG.md                         # Giáo trình 5 chương RAG toàn diện
│   ├── src/                                    # Mã nguồn pipeline RAG
│   └── README.md                               # Giới thiệu & mục lục RAG
├── senatic-search/                             # Chuyên đề Semantic Search & Vector Similarity
│   ├── guides/                                 # Tài liệu hướng dẫn & Paper nghiên cứu
│   ├── src/                                    # Mã nguồn tìm kiếm ngữ nghĩa
│   └── README.md                               # Giới thiệu Semantic Search
└── README.md                                   # Tổng quan repository & Trích xuất đường dẫn học tập
```
