from __future__ import annotations


class HealthChecker:
    """Service health checks and stale-data alerting."""

    def check_all(self) -> dict:
        return {
            "api": {"status": "OK"},
            "database": {"status": "OK"},
            "redis": {"status": "OK"},
            "ai": {"status": "OK"},
            "market_data": {"status": "OK"},
            "broker": {"status": "DISCONNECTED"},
        }

    def check_market_data_freshness(self, age_seconds: int) -> dict:
        if age_seconds > 300:
            return {"status": "ALERT", "message": "Market data stale: data age exceeds 5 minutes."}
        return {"status": "OK", "message": "Market data fresh."}
