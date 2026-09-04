"""
Module: agent/rule_base.py
Mục đích: Triển khai Rule-based Agent (Hệ thống Agent dựa trên quy tắc cố định)
Luồng xử lý:
   User Input ──► Rule Matching (Regex/Keywords) ──► Trigger Action ──► Output
"""

import re
from typing import Any, Callable, Dict, List, Optional, Tuple


class RuleBasedAgent:
    """Agent hoạt động dựa trên tập luật (Deterministic Rules) xác định trước."""

    def __init__(self):
        # Bảng quy tắc: (Tên luật, regex pattern, action tương ứng)
        self.rules: List[Tuple[str, str, Callable[[str], str]]] = [
            ("greeting", r"\b(chào|hello|hi|xin chào|hey)\b", self._action_greeting),
            ("weather", r"\b(thời tiết|nhiệt độ|mưa|nắng|dự báo thời tiết)\b", self._action_weather),
            ("calc", r"\b(tính|cộng|trừ|nhân|chia|\+|\-|\*|\/)\b", self._action_calc),
            ("doc_search", r"\b(chính sách|tài liệu|quy định|hướng dẫn|tra cứu|bảo hành)\b", self._action_search_doc),
            ("booking", r"\b(đặt lịch|đặt vé|hẹn|booking|đặt phòng)\b", self._action_booking),
        ]

    def _action_greeting(self, text: str) -> str:
        return "👋 Xin chào! Tôi là Rule-based Agent. Tôi có thể xử lý các tác vụ được lập trình sẵn."

    def _action_weather(self, text: str) -> str:
        return "🌤️ [Action: Call Weather API] Đang tra cứu dữ liệu thời tiết: Trời có mây, nhiệt độ 28°C, độ ẩm 70%."

    def _action_calc(self, text: str) -> str:
        # Trích xuất biểu thức toán học cơ bản (ví dụ: 10 + 20)
        match = re.search(r"(\d+\.?\d*)\s*([\+\-\*\/])\s*(\d+\.?\d*)", text)
        if match:
            num1 = float(match.group(1))
            op = match.group(2)
            num2 = float(match.group(3))
            
            if op == "+":
                res = num1 + num2
            elif op == "-":
                res = num1 - num2
            elif op == "*":
                res = num1 * num2
            elif op == "/":
                res = "Không thể chia cho 0" if num2 == 0 else num1 / num2
            else:
                res = "Không hỗ trợ toán tử"

            return f"🔢 [Action: Calculator] Kết quả phép tính {num1} {op} {num2} = {res}"

        return "🔢 [Action: Calculator] Nhận diện yêu cầu tính toán. Vui lòng nhập phép tính rõ ràng (vd: tính 25 * 4)."

    def _action_search_doc(self, text: str) -> str:
        return "📄 [Action: Doc Search] Khớp từ khóa tài liệu -> Chuyển hướng sang kho tài liệu nội bộ (data/documents/)."

    def _action_booking(self, text: str) -> str:
        return "📅 [Action: Booking Flow] Khớp từ khóa đặt lịch -> Kích hoạt form đăng ký lịch hẹn tự động."

    def _action_fallback(self, text: str) -> str:
        return (
            "⚠️ [Fallback: Không khớp luật]\n"
            "   Hệ thống không tìm thấy quy tắc nào khớp với câu hỏi của bạn.\n"
            "   (Đây là giới hạn của Rule-based: Cần LLM Agent để hiểu ngôn ngữ tự nhiên phức tạp)."
        )

    def process(self, user_input: str) -> Dict[str, Any]:
        """Kiểm tra tuần tự từng luật theo cơ chế if-else / regex."""
        cleaned_input = user_input.strip().lower()

        for rule_name, pattern, action_fn in self.rules:
            if re.search(pattern, cleaned_input):
                output = action_fn(user_input)
                return {
                    "matched_rule": rule_name,
                    "pattern": pattern,
                    "output": output,
                    "status": "MATCHED",
                }

        # Nếu không khớp luật nào
        return {
            "matched_rule": None,
            "pattern": None,
            "output": self._action_fallback(user_input),
            "status": "FALLBACK",
        }


def main():
    agent = RuleBasedAgent()

    print("=" * 60)
    print("🤖 HỆ THỐNG RULE-BASED AGENT (Cấp độ 1: Quy tắc cố định)")
    print("📌 Các luật mẫu được hỗ trợ:")
    print("   1. Chào hỏi: 'xin chào', 'hello'...")
    print("   2. Thời tiết: 'thời tiết hôm nay thế nào', 'nhiệt độ'...")
    print("   3. Tính toán: 'tính 15 + 30', 'tính 50 * 2'...")
    print("   4. Tra cứu: 'chính sách bảo hành', 'tài liệu hướng dẫn'...")
    print("   5. Đặt lịch: 'đặt lịch hẹn', 'booking phòng'...")
    print("\n💡 Gõ 'exit', 'quit' hoặc 'q' để dừng chương trình.")
    print("=" * 60)

    while True:
        try:
            user_input = input("\n👤 Nhập yêu cầu: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit", "q"):
                print("\n👋 Tạm biệt! Đã kết thúc phiên làm việc.")
                break

            result = agent.process(user_input)

            print(f"⚙️  [Luật khớp]: {result['matched_rule']} (Trạng thái: {result['status']})")
            print(f"📤 [Kết quả]:\n{result['output']}")
            print("-" * 60)

        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Tạm biệt! Đã kết thúc phiên làm việc.")
            break


if __name__ == "__main__":
    main()
