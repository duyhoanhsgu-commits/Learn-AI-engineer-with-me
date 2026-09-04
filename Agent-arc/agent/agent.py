"""
Module: agent/agent.py
Mục đích: Bộ điều phối luồng thực thi tổng thể
Luồng xử lý:
   User Input
       │
       ▼
   Embedding (Tạo vector đại diện)
       │
       ▼
   Router (So khớp ngữ nghĩa)
       ├───────────────┐
       ▼               ▼
   [ RAG Flow ]   [ AGENT Flow ]
   (Tra cứu doc)   (Tool & Action)
       │               │
       └───────┬───────┘
               ▼
             Output
"""

import sys
from pathlib import Path
from typing import Any, Dict

# Cho phép import module khi chạy trực tiếp file này
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

try:
    from agent.router import EmbeddingRouter, RouteType
except (ImportError, ModuleNotFoundError):
    from router import EmbeddingRouter, RouteType


class AgentOrchestrator:
    """Điều phối luồng xử lý từ User Input -> Embedding -> RAG hoặc Agent."""

    def __init__(self):
        self.router = EmbeddingRouter()

    def handle_rag(self, query: str) -> str:
        """Xử lý tác vụ tra cứu tài liệu tri thức (RAG)."""
        # Đây là điểm kết nối sang module rag/retriever.py và rag/rag.py
        return (
            f"[RAG Engine] Tiếp nhận câu hỏi: '{query}'\n"
            f"-> Thực hiện tra cứu văn bản trong cơ sở tri thức (data/documents/)\n"
            f"-> Trả về câu trả lời có kèm trích dẫn tài liệu."
        )

    def handle_agent(self, query: str) -> str:
        """Xử lý tác vụ suy luận động và gọi công cụ (Agent)."""
        # Đây là điểm kết nối sang LLM Reasoning và Tool Calling
        return (
            f"[Agent Engine] Tiếp nhận yêu cầu: '{query}'\n"
            f"-> Kích hoạt chu trình ReAct (Reasoning + Action)\n"
            f"-> Gọi Tool / API phù hợp và tổng hợp kết quả thực thi."
        )

    def run(self, user_input: str) -> Dict[str, Any]:
        """
        Thực thi toàn bộ luồng:
        Input User -> Embedding -> RAG hoặc Agent -> Response
        """
        print(f"\n{'='*50}")
        print(f"📥 [1. Input User]: {user_input}")

        # Bước 2 & 3: Embedding và Định tuyến qua Semantic Router
        print(f"🔄 [2. Embedding]: Đang chuyển đổi văn bản sang vector...")
        route, confidence, all_scores = self.router.route(user_input)
        print(f"🧭 [3. Router Decision]: Phân loại nhánh -> 【{route}】 (Confidence: {confidence:.2f})")
        print(f"   📊 Chi tiết điểm tương đồng: {all_scores}")

        # Bước 4: Phân nhánh thực thi
        if route == "RAG":
            response = self.handle_rag(user_input)
        else:
            response = self.handle_agent(user_input)

        print(f"📤 [4. Output]:\n{response}")
        print(f"{'='*50}")

        return {
            "query": user_input,
            "route": route,
            "confidence": confidence,
            "scores": all_scores,
            "response": response,
        }


if __name__ == "__main__":
    # Test thử nghiệm luồng trực tiếp
    orchestrator = AgentOrchestrator()

    # Thử nghiệm câu hỏi dành cho RAG
    orchestrator.run("Chính sách hoàn tiền và quy định bảo hành của công ty là gì?")

    # Thử nghiệm câu hỏi dành cho Agent
    orchestrator.run("Hãy tính toán tổng chi phí và gửi email báo cáo cho quản lý.")
