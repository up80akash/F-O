from __future__ import annotations


class ChatService:
    """Simple text-command router with a strict read-vs-trading separation."""

    def classify_command(self, message: str) -> str:
        text = message.strip().lower()
        trading_keywords = {"buy", "sell", "trade", "paper trade", "run paper trade", "place order"}
        if any(keyword in text for keyword in trading_keywords):
            return "TRADING"
        return "READ"

    def handle(self, message: str) -> dict:
        classified = self.classify_command(message)
        if classified == "TRADING":
            return {
                "status": "blocked",
                "reason": "TRADING commands must pass strategy, risk, and validation checks before execution.",
            }
        return {
            "status": "ok",
            "response": f"Read-only analysis for: {message}",
            "category": "READ",
        }
