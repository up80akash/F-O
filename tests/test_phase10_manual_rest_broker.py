import httpx

from app.brokers.rest import ManualRestBroker


def test_manual_rest_broker_reads_configured_quote() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/quote/NIFTY"
        assert request.headers["authorization"] == "Bearer test-token"
        return httpx.Response(200, json={"symbol": "NIFTY", "ltp": 22500.0})

    broker = ManualRestBroker(
        base_url="https://broker.example.test",
        access_token="test-token",
        enabled=True,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    assert broker.get_quote("NIFTY")["ltp"] == 22500.0


def test_manual_rest_broker_rejects_orders_in_paper_mode() -> None:
    broker = ManualRestBroker(
        base_url="https://broker.example.test",
        access_token="test-token",
        enabled=True,
        trading_mode="PAPER",
        live_trading_enabled=False,
        client=httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(500))),
    )

    result = broker.place_order({"symbol": "NIFTY", "quantity": 1})

    assert result["status"] == "rejected"
    assert result["reason"] == "live-trading-disabled"


def test_manual_rest_broker_is_disabled_without_configuration() -> None:
    broker = ManualRestBroker()

    assert broker.get_quote("NIFTY")["status"] == "disabled"
    assert broker.is_configured is False
