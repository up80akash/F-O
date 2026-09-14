from __future__ import annotations

from typing import Any


class MarketDataService:
    """Core market data service for Indian indices and F&O instruments."""

    def __init__(self) -> None:
        self.supported_instruments = [
            "NIFTY",
            "BANKNIFTY",
            "NIFTY 50",
            "NIFTY BANK",
        ]

    def get_supported_instruments(self) -> list[str]:
        return list(self.supported_instruments)

    def get_quote(self, symbol: str) -> dict[str, Any]:
        return {
            "symbol": symbol,
            "ltp": 0.0,
            "source": "market_data_service",
            "stale": False,
        }

    def get_option_chain(self, symbol: str, expiry: str | None = None) -> dict[str, Any]:
        return {
            "symbol": symbol,
            "expiry": expiry,
            "calls": [],
            "puts": [],
            "pcr": 0.0,
            "atm_strike": None,
        }
