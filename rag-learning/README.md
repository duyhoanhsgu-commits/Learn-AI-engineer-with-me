# 📚 RAG (Retrieval-Augmented Generation) Learning Hub

Mô-đun học tập và thực hành xây dựng hệ thống **RAG (Retrieval-Augmented Generation)** từ nền tảng đến production.

---

## 🎯 1. RAG là gì?

**RAG (Retrieval-Augmented Generation)** là kiến trúc kết hợp giữa **truy xuất thông tin (Retrieval)** từ cơ sở tri thức bên ngoài và **mô hình ngôn ngữ lớn (Generation)** để tạo câu trả lời chính xác, cập nhật theo thời gian thực và hạn chế tối đa hiện tượng ảo giác (hallucination).

```
[Dữ liệu thô] ──> [Offline Ingestion Pipeline] ──> [Vector Database]
                                                         │
[Câu hỏi]     ──> [Online Retrieval Pipeline]  ──────────┴──> [LLM] ──> [Câu trả lời]
```

---

## 📖 2. Trích dẫn bài học (Course Index)

Chi tiết toàn bộ lý thuyết chuyên sâu, công thức toán và phân tích kỹ thuật được trình bày tại tài liệu [guide/ALL_RAG.md](guide/ALL_RAG.md):

| STT | Chương | Trích dẫn tài liệu | Mô tả tóm tắt |
| :--- | :--- | :--- | :--- |
| **01** | **Foundation & Evolution** | [Chương 1](guide/ALL_RAG.md#chương-ii-foundation--evolution) | Bản chất Embedding, Dense Vector Space, Cosine Similarity và cơ chế Vector DB. |
| **02** | **Offline Pipeline Ingestion** | [Chương 2](guide/ALL_RAG.md#chương-iii-offline-pipeline-ingestion--data-extraction) | Quy trình nạp dữ liệu: Parsing, OCR, chiến lược Chunking và Metadata Enrichment. |
| **03** | **Online Pipeline Retrieval** | [Chương 3](guide/ALL_RAG.md#chương-iv-online-pipeline-retrieval) | Quy trình truy xuất: Query Transformation, Hybrid Search, Reranking và Context Selection. |
| **04** | **Graph RAG & Advanced Architectures** | [Chương 4](guide/ALL_RAG.md#chương-v-graph-rag--advanced-architectures) | Các kiến trúc nâng cao: Graph RAG, Multi-query, HyDE, Self-RAG, Agentic RAG. |
| **05** | **Evaluation & Operationalization** | [Chương 5](guide/ALL_RAG.md#chương-vi-evaluation--operationalization) | Đánh giá chất lượng RAG (Ragas, TruLens), tối ưu latency, chi phí và vận hành production. |

---

## 📂 3. Cấu trúc thư mục

```
rag-learning/
├── guide/
│   ├── ALL_RAG.md          # Chi tiết nội dung bài học 5 chương
│   └── RAG Mind Map.png    # Sơ đồ tư duy RAG
├── src/                    # Mã nguồn triển khai pipeline RAG
├── experiments/            # Thử nghiệm chunking, embedding, retrieval
├── tests/                  # Kiểm thử unit test & benchmark
└── README.md               # Giới thiệu & mục lục RAG
```
