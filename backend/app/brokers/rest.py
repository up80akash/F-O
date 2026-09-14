from __future__ import annotations

from typing import Any
from urllib.parse import quote

import httpx

from app.brokers.base import BrokerInterface


class ManualRestBroker(BrokerInterface):
    """Configurable REST broker adapter with a paper-first execution gate."""

    name = "manual-rest"

    def __init__(
        self,
        base_url: str = "",
        access_token: str = "",
        enabled: bool = False,
        auth_header: str = "Authorization",
        auth_scheme: str = "Bearer",
        timeout_seconds: float = 10.0,
        trading_mode: str = "PAPER",
        live_trading_enabled: bool = False,
        endpoints: dict[str, str] | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token
        self.enabled = enabled
        self.auth_header = auth_header
        self.auth_scheme = auth_scheme
        self.trading_mode = trading_mode.upper()
        self.live_trading_enabled = live_trading_enabled
        self.endpoints = {
            "quote": "/quote/{symbol}",
            "quotes": "/quotes",
            "option_chain": "/option-chain",
            "positions": "/positions",
            "orders": "/orders",
            "order": "/orders/{order_id}",
            "order_status": "/orders/{order_id}",
            "instruments": "/instruments",
            **(endpoints or {}),
        }
        self.client = client or httpx.Client(timeout=timeout_seconds)
        self.is_configured = bool(self.enabled and self.base_url)

    def status(self) -> dict[str, Any]:
        return {
            "broker": self.name,
            "configured": self.is_configured,
            "trading_mode": self.trading_mode,
            "live_execution_allowed": self._can_execute_live_trade(),
        }

    def _can_execute_live_trade(self) -> bool:
        return self.live_trading_enabled and self.trading_mode == "LIVE"

    def _headers(self) -> dict[str, str]:
        if not self.access_token:
            return {}
        value = f"{self.auth_scheme} {self.access_token}".strip()
        return {self.auth_header: value}

    def _path(self, key: str, **values: str) -> str:
        path = self.endpoints[key]
        for name, value in values.items():
            path = path.replace("{" + name + "}", quote(value, safe=""))
        return path

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        if not self.is_configured:
            return {"status": "disabled", "reason": "manual-rest-broker-not-configured"}
        try:
            response = self.client.request(
                method,
                f"{self.base_url}{path}",
                headers=self._headers(),
                **kwargs,
            )
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, ValueError) as error:
            return {
                "status": "error",
                "reason": "broker-request-failed",
                "detail": str(error),
            }

    @staticmethod
    def _as_list(payload: Any) -> list[dict[str, Any]]:
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict) and isinstance(payload.get("data"), list):
            return payload["data"]
        return []

    def get_quote(self, symbol: str) -> dict[str, Any]:
        payload = self._request("GET", self._path("quote", symbol=symbol))
        return payload if isinstance(payload, dict) else {"status": "error", "reason": "invalid-quote-response"}

    def get_quotes(self, symbols: list[str]) -> list[dict[str, Any]]:
        return self._as_list(self._request("GET", self._path("quotes"), params={"symbols": ",".join(symbols)}))

    def get_option_chain(self, symbol: str, expiry: str | None = None) -> dict[str, Any]:
        params = {"symbol": symbol}
        if expiry:
            params["expiry"] = expiry
        payload = self._request("GET", self._path("option_chain"), params=params)
        return payload if isinstance(payload, dict) else {"status": "error", "reason": "invalid-option-chain-response"}

    def get_positions(self) -> list[dict[str, Any]]:
        return self._as_list(self._request("GET", self._path("positions")))

    def get_orders(self) -> list[dict[str, Any]]:
        return self._as_list(self._request("GET", self._path("orders")))

    def place_order(self, order: dict[str, Any]) -> dict[str, Any]:
        if not self._can_execute_live_trade():
            return {"status": "rejected", "reason": "live-trading-disabled", "order": order}
        payload = self._request("POST", self._path("orders"), json=order)
        return payload if isinstance(payload, dict) else {"status": "error", "reason": "invalid-order-response"}

    def modify_order(self, order_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        if not self._can_execute_live_trade():
            return {"status": "rejected", "reason": "live-trading-disabled", "order_id": order_id}
        payload = self._request("PATCH", self._path("order", order_id=order_id), json=updates)
        return payload if isinstance(payload, dict) else {"status": "error", "reason": "invalid-order-response"}

    def cancel_order(self, order_id: str) -> dict[str, Any]:
        if not self._can_execute_live_trade():
            return {"status": "rejected", "reason": "live-trading-disabled", "order_id": order_id}
        payload = self._request("DELETE", self._path("order", order_id=order_id))
        return payload if isinstance(payload, dict) else {"status": "error", "reason": "invalid-order-response"}

    def get_order_status(self, order_id: str) -> dict[str, Any]:
        payload = self._request("GET", self._path("order_status", order_id=order_id))
        return payload if isinstance(payload, dict) else {"status": "error", "reason": "invalid-order-response"}

    def get_instruments(self) -> list[dict[str, Any]]:
        return self._as_list(self._request("GET", self._path("instruments")))
