from __future__ import annotations

from typing import Any

from app.brokers.base import BrokerInterface


class UpstoxBroker(BrokerInterface):
    """Upstox broker adapter placeholder for Phase 2."""

    name = "upstox"

    def __init__(self) -> None:
        self.access_token = None
        self.client_id = None
        self.client_secret = None
        self.is_configured = False

    def get_quote(self, symbol: str) -> dict[str, Any]:
        return {"symbol": symbol, "ltp": 0.0, "source": self.name}

    def get_quotes(self, symbols: list[str]) -> list[dict[str, Any]]:
        return [self.get_quote(symbol) for symbol in symbols]

    def get_option_chain(self, symbol: str, expiry: str | None = None) -> dict[str, Any]:
        return {"symbol": symbol, "expiry": expiry, "calls": [], "puts": [], "source": self.name}

    def get_positions(self) -> list[dict[str, Any]]:
        return []

    def get_orders(self) -> list[dict[str, Any]]:
        return []

    def place_order(self, order: dict[str, Any]) -> dict[str, Any]:
        return {"status": "rejected", "reason": "upstox-not-configured", "order": order}

    def modify_order(self, order_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        return {"status": "not_implemented", "order_id": order_id, "updates": updates}

    def cancel_order(self, order_id: str) -> dict[str, Any]:
        return {"status": "not_implemented", "order_id": order_id}

    def get_order_status(self, order_id: str) -> dict[str, Any]:
        return {"status": "unknown", "order_id": order_id}

    def get_instruments(self) -> list[dict[str, Any]]:
        return []
