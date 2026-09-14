from __future__ import annotations


def classify_market_regime(
    ema_9: float | None = None,
    ema_20: float | None = None,
    rsi: float | None = None,
    price_above_vwap: bool | None = None,
) -> str:
    if ema_9 is None and ema_20 is None and rsi is None and price_above_vwap is None:
        return "UNCERTAIN"

    bullish_score = 0
    bearish_score = 0

    if ema_9 is not None and ema_20 is not None:
        if ema_9 > ema_20:
            bullish_score += 1
        elif ema_9 < ema_20:
            bearish_score += 1

    if rsi is not None:
        if rsi > 70:
            bearish_score += 1
        elif rsi < 30:
            bullish_score += 1
        elif rsi >= 55:
            bullish_score += 1
        elif rsi <= 45:
            bearish_score += 1

    if price_above_vwap is True:
        bullish_score += 1
    elif price_above_vwap is False:
        bearish_score += 1

    if bullish_score > bearish_score:
        return "BULLISH"
    if bearish_score > bullish_score:
        return "BEARISH"
    return "SIDEWAYS"
