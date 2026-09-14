from app.risk.engine import RiskEngine
from app.strategies.engine import StrategyEngine, DecisionEngine


def test_strategy_engine_generates_call_when_conditions_align() -> None:
    engine = StrategyEngine()
    signal = engine.generate_signal(
        {
            "trend": "BULLISH",
            "ema_9": 101.5,
            "ema_20": 99.0,
            "rsi": 62,
            "vwap": 100.0,
            "pcr": 1.2,
            "volume_ratio": 1.3,
            "market_regime": "TRENDING",
        }
    )
    assert signal["signal"] == "CALL"
    assert signal["score"] >= 0.6


def test_strategy_engine_prefers_no_trade_on_conflict() -> None:
    engine = StrategyEngine()
    signal = engine.generate_signal(
        {
            "trend": "BULLISH",
            "ema_9": 100.0,
            "ema_20": 101.0,
            "rsi": 50,
            "vwap": 105.0,
            "pcr": 0.9,
            "volume_ratio": 0.8,
            "market_regime": "SIDEWAYS",
        }
    )
    assert signal["signal"] == "NO TRADE"


def test_risk_engine_blocks_trade_when_loss_limit_exceeded() -> None:
    risk = RiskEngine()
    result = risk.validate_trade(
        {
            "signal": "CALL",
            "stop_loss": 100.0,
            "target": 110.0,
            "risk_per_trade": 0.02,
            "position_size": 15000,
            "market_fresh": True,
            "live_trading_enabled": False,
        },
        daily_loss=5000,
        max_daily_loss=4000,
    )
    assert result["approved"] is False
    assert result["decision"] == "NO TRADE"


def test_decision_engine_combines_ai_strategy_and_risk() -> None:
    engine = DecisionEngine()
    decision = engine.decide(
        ai_signal={"signal": "CALL", "action": "WAIT"},
        strategy_signal={"signal": "CALL", "score": 0.72},
        risk_result={"approved": True, "decision": "APPROVED"},
        market_fresh=True,
    )
    assert decision["final_decision"] == "BUY"
