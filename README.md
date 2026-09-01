# 🚀 Learn AI Engineer With Me

Kho lưu trữ tài liệu, kiến thức và dự án thực hành trên lộ trình trở thành **AI Engineer** toàn diện (từ nền tảng lý thuyết đến triển khai hệ thống production).

---

## 📚 Danh mục tài liệu & Đường dẫn bài học (.md)

Bảng tổng hợp toàn bộ các đường dẫn tài liệu học tập Markdown trong kho lưu trữ:

### 1. Nền tảng AI & Large Language Models
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **Foundation AI & LLM (Toàn diện)** | [Foundation ai and llm.md](Foundation%20AI%20&%20LLM/Foundation%20ai%20and%20llm.md) | Cẩm nang kiến trúc hệ thống AI 13 bước: Problem Discovery, Rule vs AI, Automation vs Augmentation, Reward Design, Precision & Recall, 3 Cấp độ kiến trúc (Workflow vs Agent), Tokenization & Attention, Pre-training & RLHF, ReAct & Function Calling, Hybrid Routing & Retrieval, Citation, RAG Triad, Probabilistic Design, Fallback/HITL, Observability, Golden Dataset, LLM-as-a-Judge. |

---

### 2. Chuyên đề RAG (Retrieval-Augmented Generation)
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **Tổng quan RAG** | [rag-learning/README.md](rag-learning/README.md) | Giới thiệu RAG, kiến trúc 2 luồng và cấu trúc dự án. |
| **Giáo trình RAG toàn diện** | [rag-learning/docs/ALL_RAG.md](rag-learning/docs/ALL_RAG.md) | Toàn bộ 5 chương lý thuyết, toán học và kỹ thuật RAG: |
| ↳ *Chương 1* | [ALL_RAG.md #Chương 1](rag-learning/docs/ALL_RAG.md#chương-ii-foundation--evolution) | *Foundation & Evolution (Embedding, Dense Space, Cosine Similarity, Vector DB Internals).* |
| ↳ *Chương 2* | [ALL_RAG.md #Chương 2](rag-learning/docs/ALL_RAG.md#chương-iii-offline-pipeline-ingestion--data-extraction) | *Offline Pipeline Ingestion (Parsing, OCR, Chunking Strategies, Metadata Enrichment).* |
| ↳ *Chương 3* | [ALL_RAG.md #Chương 3](rag-learning/docs/ALL_RAG.md#chương-iv-online-pipeline-retrieval) | *Online Pipeline Retrieval (Query Transformation, Hybrid Search, Reranking, Context).* |
| ↳ *Chương 4* | [ALL_RAG.md #Chương 4](rag-learning/docs/ALL_RAG.md#chương-v-graph-rag--advanced-architectures) | *Graph RAG & Advanced Architectures (Self-RAG, CRAG, Agentic RAG).* |
| ↳ *Chương 5* | [ALL_RAG.md #Chương 5](rag-learning/docs/ALL_RAG.md#chương-vi-evaluation--operationalization) | *Evaluation & Operationalization (RAG Triad, Ragas, TruLens, Latency & Cost Optimization).* |

---

### 3. Chuyên đề Semantic Search (Tìm kiếm ngữ nghĩa)
| Tài liệu | Đường dẫn (.md) | Nội dung |
| :--- | :--- | :--- |
| **Tổng quan Semantic Search** | [senatic-search/README.md](senatic-search/README.md) | Giới thiệu dự án Semantic Search và cách vận hành. |
| **Báo cáo nghiên cứu (Paper)** | [senatic-search/guides/paper.md](senatic-search/guides/paper.md) | Nghiên cứu chi tiết: *How Computers Search by Meaning*, Vector Embeddings & Similarity. |
| **Hiểu sâu về Embeddings** | [senatic-search/guides/01_understanding_embeddings.md](senatic-search/guides/01_understanding_embeddings.md) | Bản chất biểu diễn vector của từ và câu. |
| **Độ tương đồng Vector** | [senatic-search/guides/02_vector_similarity.md](senatic-search/guides/02_vector_similarity.md) | Các thuật toán đo khoảng cách vector trong không gian đa chiều. |

---

## 🧭 Lộ trình phát triển tiếp theo (Roadmap)

- [ ] **AI Agents & Multi-Agent Systems:** Tool Use, Function Calling, ReAct, CrewAI, LangGraph.
- [ ] **LLM Fine-tuning & Optimization:** PEFT, LoRA, QLoRA, DPO, RLHF.
- [ ] **Multimodal AI:** Vision-Language Models (VLM), Audio/Video AI.
- [ ] **LLMOps & Serving:** vLLM, Ollama, TensorRT-LLM, Tracing/Observability.

---

## 📂 Cấu trúc Repository

```
Learn-AI-engineer-with-me/
├── Foundation AI & LLM/  # Kiến thức nền tảng AI, Deep Learning & LLMs
│   └── README.md         # Giáo trình nền tảng AI & LLM
├── rag-learning/         # Chuyên đề RAG từ lý thuyết đến triển khai
│   ├── docs/             # Giáo trình chi tiết (ALL_RAG.md)
│   ├── src/              # Mã nguồn pipeline RAG
│   └── README.md         # Giới thiệu & mục lục RAG
├── senatic-search/       # Chuyên đề Semantic Search & Vector Similarity
│   ├── guides/           # Tài liệu hướng dẫn & Paper nghiên cứu
│   ├── src/              # Mã nguồn tìm kiếm ngữ nghĩa
│   └── README.md         # Giới thiệu Semantic Search
└── README.md             # Tổng quan repository & trích xuất đường dẫn học
```
