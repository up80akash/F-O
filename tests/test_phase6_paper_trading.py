from app.paper_trading.engine import PaperTradingEngine
from app.risk.engine import RiskEngine


def test_paper_trade_simulates_fill_and_pnl() -> None:
    engine = PaperTradingEngine()
    result = engine.execute_order(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 50,
            "price": 22000,
            "stop_loss": 21900,
            "target": 22150,
            "strategy_score": 0.7,
        }
    )
    assert result["status"] in {"FILLED", "PARTIAL"}
    assert result["pnl"] is not None
    assert result["trade_id"]


def test_risk_engine_rejects_trade_when_loss_limit_hit() -> None:
    risk = RiskEngine()
    result = risk.validate_trade(
        {"signal": "CALL", "stop_loss": 100.0, "target": 110.0, "risk_per_trade": 0.02, "position_size": 5000, "market_fresh": True, "live_trading_enabled": False},
        daily_loss=8000,
        max_daily_loss=5000,
    )
    assert result["approved"] is False


def test_paper_engine_keeps_same_record_schema_as_live() -> None:
    engine = PaperTradingEngine()
    order = engine.execute_order({"symbol": "BANKNIFTY", "side": "BUY", "quantity": 25, "price": 49000, "stop_loss": 48850, "target": 49350, "strategy_score": 0.6})
    required = {"trade_id", "status", "symbol", "side", "quantity", "price", "pnl", "fees", "stop_loss", "target"}
    assert required.issubset(order.keys())
