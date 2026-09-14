from __future__ import annotations


class RiskEngine:
    """Deterministic trade gatekeeper for the platform."""

    def validate_trade(self, trade: dict, daily_loss: float = 0.0, max_daily_loss: float = 0.0) -> dict:
        signal = trade.get("signal")
        stop_loss = trade.get("stop_loss")
        target = trade.get("target")
        risk_per_trade = float(trade.get("risk_per_trade", 0.0) or 0.0)
        position_size = float(trade.get("position_size", 0.0) or 0.0)
        market_fresh = bool(trade.get("market_fresh", False))
        live_trading_enabled = bool(trade.get("live_trading_enabled", False))

        if daily_loss >= max_daily_loss and max_daily_loss > 0:
            return {"approved": False, "decision": "NO TRADE", "reason": "daily loss limit reached"}

        if not market_fresh:
            return {"approved": False, "decision": "NO TRADE", "reason": "stale market data"}

        if not live_trading_enabled and trade.get("signal") in {"CALL", "PUT"}:
            return {"approved": True, "decision": "APPROVED", "reason": "paper trading default"}

        if signal not in {"CALL", "PUT"}:
            return {"approved": False, "decision": "NO TRADE", "reason": "invalid signal"}

        if stop_loss is None or target is None:
            return {"approved": False, "decision": "NO TRADE", "reason": "stop loss or target missing"}

        if risk_per_trade <= 0 or position_size <= 0:
            return {"approved": False, "decision": "NO TRADE", "reason": "risk or position invalid"}

        return {"approved": True, "decision": "APPROVED", "reason": "risk checks passed"}
