from __future__ import annotations


class AIAnalysisService:
    """Validates structured AI market analysis output before it reaches trade logic."""

    required_fields = {
        "market_bias",
        "market_regime",
        "signal",
        "instrument",
        "entry_zone",
        "stop_loss",
        "target",
        "confidence",
        "risk_level",
        "holding_period",
        "reasoning",
        "invalidating_conditions",
        "action",
    }

    allowed_actions = {"BUY", "SELL", "WAIT", "NO TRADE"}
    allowed_signals = {"CALL", "PUT", "NO TRADE"}
    allowed_market_bias = {"BULLISH", "BEARISH", "SIDEWAYS", "UNCERTAIN"}
    allowed_market_regime = {"TRENDING", "SIDEWAYS", "HIGH VOLATILITY", "LOW VOLATILITY", "BREAKOUT", "BREAKDOWN", "UNCERTAIN"}

    def validate_payload(self, payload: dict) -> bool:
        if not isinstance(payload, dict):
            return False

        if not self.required_fields.issubset(payload.keys()):
            return False

        if payload.get("market_bias") not in self.allowed_market_bias:
            return False

        if payload.get("market_regime") not in self.allowed_market_regime:
            return False

        if payload.get("signal") not in self.allowed_signals:
            return False

        if payload.get("action") not in self.allowed_actions:
            return False

        if not isinstance(payload.get("invalidating_conditions"), list):
            return False

        if not isinstance(payload.get("confidence"), (int, float)):
            return False

        if payload.get("confidence") < 0 or payload.get("confidence") > 1:
            return False

        if payload.get("instrument") in (None, ""):
            return False

        return True

    def build_default_no_trade(self, instrument: str = "NIFTY") -> dict:
        return {
            "market_bias": "UNCERTAIN",
            "market_regime": "UNCERTAIN",
            "signal": "NO TRADE",
            "instrument": instrument,
            "entry_zone": "N/A",
            "stop_loss": None,
            "target": None,
            "confidence": 0.0,
            "risk_level": "LOW",
            "holding_period": "N/A",
            "reasoning": "Insufficient or stale market data.",
            "invalidating_conditions": ["missing data", "stale data"],
            "action": "NO TRADE",
        }
