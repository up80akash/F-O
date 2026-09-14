from fastapi import APIRouter

from app.brokers.upstox import UpstoxBroker
from app.market_data.service import MarketDataService
from app.trading.control import TradingControl
from app.config import get_settings

router = APIRouter(prefix="/api", tags=["market"])


@router.get("/market/health")
def market_health() -> dict:
    return {
        "status": "ok",
        "mode": "PAPER",
        "broker": UpstoxBroker().name,
        "supported_instruments": MarketDataService().get_supported_instruments(),
    }


@router.get("/market/instruments")
def market_instruments() -> dict:
    return {"instruments": MarketDataService().get_supported_instruments()}


@router.get("/trading/status")
def trading_status() -> dict:
    settings = get_settings()
    return TradingControl(
        live_trading_enabled=settings.live_trading_enabled,
        trading_mode=settings.trading_mode,
    ).status()
