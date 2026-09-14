from __future__ import annotations


class StrategyEngine:
    """Deterministic intraday directional strategy for NIFTY-style data."""

    def generate_signal(self, market: dict) -> dict:
        score = 0.0
        trend = market.get("trend", "SIDEWAYS")
        ema_9 = float(market.get("ema_9", 0.0) or 0.0)
        ema_20 = float(market.get("ema_20", 0.0) or 0.0)
        rsi = float(market.get("rsi", 50.0) or 50.0)
        vwap = float(market.get("vwap", 0.0) or 0.0)
        pcr = float(market.get("pcr", 1.0) or 1.0)
        volume_ratio = float(market.get("volume_ratio", 1.0) or 1.0)
        market_regime = market.get("market_regime", "SIDEWAYS")

        if trend == "BULLISH":
            score += 0.25
        elif trend == "BEARISH":
            score -= 0.25

        if ema_9 > ema_20:
            score += 0.25
        else:
            score -= 0.25

        if 55 <= rsi <= 70:
            score += 0.15
        elif 30 <= rsi <= 45:
            score -= 0.15

        if vwap and ema_9 > vwap:
            score += 0.15
        elif vwap and ema_9 < vwap:
            score -= 0.15

        if pcr > 1.0:
            score += 0.10
        elif pcr < 0.9:
            score -= 0.10

        if volume_ratio > 1.1:
            score += 0.10
        elif volume_ratio < 0.9:
            score -= 0.10

        if market_regime in {"TRENDING", "BREAKOUT"}:
            score += 0.10
        elif market_regime in {"SIDEWAYS", "UNCERTAIN"}:
            score -= 0.10

        normalized = max(0.0, min(1.0, (score + 0.7) / 1.4))

        if normalized >= 0.6 and market_regime not in {"SIDEWAYS", "UNCERTAIN"}:
            signal = "CALL" if trend != "BEARISH" else "PUT"
            return {"signal": signal, "score": round(normalized, 2), "decision": "APPROVED"}

        return {"signal": "NO TRADE", "score": round(normalized, 2), "decision": "NO TRADE"}


class DecisionEngine:
    """Combines AI signal, strategy signal, and risk approval into a final trade decision."""

    def decide(self, ai_signal: dict, strategy_signal: dict, risk_result: dict, market_fresh: bool) -> dict:
        if not market_fresh:
            return {"final_decision": "NO TRADE", "reason": "market data stale"}

        if ai_signal.get("action") == "NO TRADE":
            return {"final_decision": "NO TRADE", "reason": "AI requested no action"}

        if strategy_signal.get("signal") == "NO TRADE":
            return {"final_decision": "NO TRADE", "reason": "strategy no-trade"}

        if risk_result.get("approved") is not True:
            return {"final_decision": "NO TRADE", "reason": "risk not approved"}

        if strategy_signal.get("signal") == "CALL":
            return {"final_decision": "BUY", "reason": "risk approved with bullish bias"}

        if strategy_signal.get("signal") == "PUT":
            return {"final_decision": "SELL", "reason": "risk approved with bearish bias"}

        return {"final_decision": "NO TRADE", "reason": "decision engine default no-trade"}
