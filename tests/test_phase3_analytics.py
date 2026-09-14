from app.indicators.technical import calculate_ema, calculate_macd, calculate_rsi, calculate_atr
from app.market_regime import classify_market_regime
from app.options.chain import OptionChainAnalyzer


def test_ema_calculation() -> None:
    values = [10, 12, 15, 17, 20]
    ema = calculate_ema(values, period=3)
    assert ema[-1] > 0
    assert len(ema) == len(values)


def test_rsi_bounds() -> None:
    values = [10, 11, 12, 11, 13, 15, 16, 14, 17, 18]
    rsi = calculate_rsi(values)
    assert 0 <= rsi <= 100


def test_macd_and_atr_values() -> None:
    closes = [100, 101, 102, 101, 103, 105, 104]
    highs = [101, 102, 103, 102, 104, 106, 105]
    lows = [99, 100, 101, 99, 101, 103, 102]
    macd = calculate_macd(closes)
    atr = calculate_atr(highs, lows, closes)
    assert macd["macd_line"][-1] is not None
    assert atr >= 0


def test_option_chain_summary() -> None:
    analyzer = OptionChainAnalyzer()
    summary = analyzer.summarize(
        calls=[{"oi": 1200, "oi_change": 100, "volume": 300, "iv": 18.3}, {"oi": 800, "oi_change": -50, "volume": 200, "iv": 17.1}],
        puts=[{"oi": 1400, "oi_change": 110, "volume": 280, "iv": 19.2}, {"oi": 900, "oi_change": -40, "volume": 220, "iv": 18.7}],
    )
    assert summary["pcr"] > 0
    assert summary["call_oi_total"] > 0
    assert summary["put_oi_total"] > 0


def test_market_regime_classification() -> None:
    result = classify_market_regime(ema_9=101.0, ema_20=99.0, rsi=62, price_above_vwap=True)
    assert result in {"BULLISH", "SIDEWAYS", "BEARISH", "UNCERTAIN"}
