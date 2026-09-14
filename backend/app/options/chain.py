from __future__ import annotations


class OptionChainAnalyzer:
    """Deterministic option-chain summary engine for F&O analysis."""

    def summarize(self, calls: list[dict], puts: list[dict]) -> dict:
        call_oi_total = sum(float(item.get("oi", 0.0)) for item in calls)
        put_oi_total = sum(float(item.get("oi", 0.0)) for item in puts)
        call_oi_change = sum(float(item.get("oi_change", 0.0)) for item in calls)
        put_oi_change = sum(float(item.get("oi_change", 0.0)) for item in puts)

        pcr = 0.0
        if put_oi_total > 0:
            pcr = call_oi_total / put_oi_total
        elif call_oi_total > 0:
            pcr = float("inf")

        return {
            "call_oi_total": call_oi_total,
            "put_oi_total": put_oi_total,
            "call_oi_change": call_oi_change,
            "put_oi_change": put_oi_change,
            "pcr": pcr,
            "max_call_oi": max((float(item.get("oi", 0.0)) for item in calls), default=0.0),
            "max_put_oi": max((float(item.get("oi", 0.0)) for item in puts), default=0.0),
        }
