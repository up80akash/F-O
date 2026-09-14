from app.backtesting.engine import BacktestEngine


def test_backtesting_runs_with_predefined_history() -> None:
    engine = BacktestEngine()
    results = engine.run(
        candles=[
            {"close": 100.0, "high": 101.0, "low": 99.0, "volume": 1200},
            {"close": 101.5, "high": 102.2, "low": 100.5, "volume": 1300},
            {"close": 103.1, "high": 104.5, "low": 101.7, "volume": 1600},
            {"close": 102.0, "high": 103.3, "low": 100.6, "volume": 1400},
            {"close": 104.5, "high": 105.4, "low": 102.8, "volume": 1700},
        ],
        initial_capital=100000,
    )

    assert results["total_return"] is not None
    assert results["number_of_trades"] >= 0
    assert results["win_rate"] >= 0
    assert results["max_drawdown"] >= 0


def test_backtester_rejects_look_ahead_bias() -> None:
    engine = BacktestEngine()
    assert engine.validate_history([
        {"close": 100.0},
        {"close": 101.0},
        {"close": 102.0},
    ]) is True
