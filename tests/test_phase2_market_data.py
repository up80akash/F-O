from app.brokers.base import BrokerInterface
from app.brokers.upstox import UpstoxBroker
from app.market_data.service import MarketDataService


def test_broker_interface_is_abstract() -> None:
    assert hasattr(BrokerInterface, "get_quote")
    assert hasattr(BrokerInterface, "get_option_chain")


def test_upstox_config_is_detected() -> None:
    broker = UpstoxBroker()
    assert broker.name == "upstox"
    assert broker.is_configured is False


def test_market_data_service_instruments() -> None:
    service = MarketDataService()
    instruments = service.get_supported_instruments()
    assert "NIFTY" in instruments
    assert "BANKNIFTY" in instruments
    assert "NIFTY 50" in instruments
