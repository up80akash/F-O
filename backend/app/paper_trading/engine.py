from __future__ import annotations

import uuid


class PaperTradingEngine:
    """Paper trading engine that simulates fills, slippage, fees, and P&L."""

    def execute_order(self, order: dict) -> dict:
        quantity = int(order.get("quantity", 0) or 0)
        price = float(order.get("price", 0.0) or 0.0)
        stop_loss = float(order.get("stop_loss", 0.0) or 0.0)
        target = float(order.get("target", 0.0) or 0.0)
        strategy_score = float(order.get("strategy_score", 0.0) or 0.0)

        if quantity <= 0 or price <= 0:
            return {
                "trade_id": str(uuid.uuid4()),
                "status": "REJECTED",
                "symbol": order.get("symbol", "UNKNOWN"),
                "side": order.get("side", "BUY"),
                "quantity": quantity,
                "price": price,
                "pnl": 0.0,
                "fees": 0.0,
                "stop_loss": stop_loss,
                "target": target,
                "strategy_score": strategy_score,
            }

        slippage = max(0.0, price * 0.0005)
        fill_price = price + slippage if order.get("side") == "BUY" else price - slippage
        brokerage = max(0.0, quantity * price * 0.0001)
        fees = brokerage + 25.0

        pnl = (target - fill_price) * quantity if order.get("side") == "BUY" else (fill_price - target) * quantity
        if pnl == 0:
            pnl = (stop_loss - fill_price) * quantity if order.get("side") == "BUY" else (fill_price - stop_loss) * quantity

        return {
            "trade_id": str(uuid.uuid4()),
            "status": "FILLED",
            "symbol": order.get("symbol", "UNKNOWN"),
            "side": order.get("side", "BUY"),
            "quantity": quantity,
            "price": fill_price,
            "pnl": round(pnl, 2),
            "fees": round(fees, 2),
            "stop_loss": stop_loss,
            "target": target,
            "strategy_score": strategy_score,
        }
