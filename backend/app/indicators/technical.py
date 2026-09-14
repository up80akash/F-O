from __future__ import annotations


def calculate_ema(values: list[float], period: int = 14) -> list[float]:
    if not values:
        return []
    if period <= 0:
        raise ValueError("period must be positive")
    multiplier = 2 / (period + 1)
    ema_values: list[float] = []
    prev = float(values[0])
    for value in values:
        prev = (float(value) - prev) * multiplier + prev
        ema_values.append(prev)
    return ema_values


def calculate_rsi(values: list[float], period: int = 14) -> float:
    if not values:
        return 50.0
    if len(values) <= 1:
        return 50.0

    deltas = [float(values[i]) - float(values[i - 1]) for i in range(1, len(values))]
    gains = [max(delta, 0.0) for delta in deltas]
    losses = [abs(min(delta, 0.0)) for delta in deltas]

    avg_gain = sum(gains[:period]) / max(period, 1)
    avg_loss = sum(losses[:period]) / max(period, 1)

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def calculate_macd(values: list[float], fast: int = 12, slow: int = 26, signal: int = 9) -> dict[str, list[float]]:
    if not values:
        return {"macd_line": [], "signal_line": [], "histogram": []}

    fast_ema = calculate_ema(values, fast)
    slow_ema = calculate_ema(values, slow)
    macd_line = [fast_val - slow_val for fast_val, slow_val in zip(fast_ema, slow_ema)]
    signal_line = calculate_ema(macd_line, signal)
    histogram = [macd - signal for macd, signal in zip(macd_line, signal_line)]
    return {"macd_line": macd_line, "signal_line": signal_line, "histogram": histogram}


def calculate_atr(highs: list[float], lows: list[float], closes: list[float]) -> float:
    if not (highs and lows and closes):
        return 0.0
    if len(highs) != len(lows) or len(highs) != len(closes):
        raise ValueError("highs, lows, and closes must have the same length")

    tr_values = []
    for i in range(len(highs)):
        true_range = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]) if i > 0 else 0.0,
            abs(lows[i] - closes[i - 1]) if i > 0 else 0.0,
        )
        tr_values.append(true_range)

    if not tr_values:
        return 0.0

    return sum(tr_values) / len(tr_values)
