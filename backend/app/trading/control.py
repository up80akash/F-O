from __future__ import annotations


class TradingControl:
    """Safety gate that enforces paper-trading defaults and explicit opt-in for live execution."""

    def __init__(self, live_trading_enabled: bool = False, trading_mode: str = "PAPER") -> None:
        self.live_trading_enabled = bool(live_trading_enabled)
        self.trading_mode = str(trading_mode or "PAPER").upper()

    def can_execute_live_trade(self) -> bool:
        return self.live_trading_enabled and self.trading_mode == "LIVE"

    def status(self) -> dict:
        execution_allowed = self.can_execute_live_trade()
        return {
            "mode": self.trading_mode,
            "live_trading_enabled": self.live_trading_enabled,
            "execution_allowed": execution_allowed,
            "policy": "PAPER ONLY unless explicit live opt-in is enabled",
        }
