from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Quote:
    symbol: str
    exchange: str = "NSE"
    ltp: float = 0.0
    bid: float | None = None
    ask: float | None = None
    volume: int = 0
    timestamp: str | None = None
    stale: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class OptionChainSnapshot:
    symbol: str
    expiry: str | None = None
    calls: list[dict[str, Any]] = field(default_factory=list)
    puts: list[dict[str, Any]] = field(default_factory=list)
    pcr: float = 0.0
    atm_strike: float | None = None
    timestamp: str | None = None
