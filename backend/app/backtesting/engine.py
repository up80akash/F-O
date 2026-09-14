from __future__ import annotations


class BacktestEngine:
    """Minimal deterministic backtester for a single long/short directional rule."""

    def validate_history(self, candles: list[dict]) -> bool:
        if not candles:
            return False
        for candle in candles:
            if not isinstance(candle, dict):
                return False
            if "close" not in candle:
                return False
        return True

    def run(self, candles: list[dict], initial_capital: float = 100000.0) -> dict:
        if not self.validate_history(candles):
            raise ValueError("candles must contain valid close values")

        capital = float(initial_capital)
        trades = 0
        wins = 0
        losses = 0
        pnl_values = []
        peak = capital
        max_drawdown = 0.0

        for index in range(1, len(candles)):
            prev_close = float(candles[index - 1]["close"])
            curr_close = float(candles[index]["close"])
            if curr_close > prev_close:
                trade_pnl = (curr_close - prev_close) / prev_close * capital
                capital += trade_pnl
                trades += 1
                pnl_values.append(trade_pnl)
                if trade_pnl > 0:
                    wins += 1
                else:
                    losses += 1
                if capital > peak:
                    peak = capital
                drawdown = (peak - capital) / peak if peak > 0 else 0.0
                if drawdown > max_drawdown:
                    max_drawdown = drawdown

        total_return = (capital - initial_capital) / initial_capital if initial_capital else 0.0
        win_rate = (wins / trades) if trades else 0.0
        average_win = sum(p for p in pnl_values if p > 0) / max(wins, 1)
        average_loss = abs(sum(p for p in pnl_values if p < 0)) / max(losses, 1) if losses else 0.0
        profit_factor = (sum(p for p in pnl_values if p > 0) / max(abs(sum(p for p in pnl_values if p < 0)), 1.0)) if pnl_values else 0.0

        return {
            "initial_capital": initial_capital,
            "final_capital": capital,
            "total_return": round(total_return, 4),
            "win_rate": round(win_rate, 4),
            "average_win": round(average_win, 4),
            "average_loss": round(average_loss, 4),
            "profit_factor": round(profit_factor, 4),
            "max_drawdown": round(max_drawdown, 4),
            "maximum_drawdown": round(max_drawdown, 4),
            "number_of_trades": trades,
            "consecutive_losses": 0,
            "sharpe_ratio": 0.0,
            "expectancy": 0.0,
        }
