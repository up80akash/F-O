from app.trading.control import TradingControl


def test_live_trading_control_blocks_when_disabled() -> None:
    control = TradingControl(live_trading_enabled=False, trading_mode="PAPER")
    assert control.can_execute_live_trade() is False
    status = control.status()
    assert status["mode"] == "PAPER"
    assert status["live_trading_enabled"] is False
    assert status["execution_allowed"] is False


def test_live_trading_control_allows_when_explicitly_enabled() -> None:
    control = TradingControl(live_trading_enabled=True, trading_mode="LIVE")
    assert control.can_execute_live_trade() is True
    status = control.status()
    assert status["mode"] == "LIVE"
    assert status["live_trading_enabled"] is True
    assert status["execution_allowed"] is True
