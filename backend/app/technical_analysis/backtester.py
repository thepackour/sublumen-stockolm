from __future__ import annotations

from math import sqrt

import pandas as pd


def run_backtest(
    signals: pd.DataFrame,
    initial_capital: float,
    commission_rate: float = 0.00015,
    slippage_rate: float = 0.0005,
) -> dict:
    """Run a long-only, all-in backtest with next-session-open execution."""
    if initial_capital <= 0:
        raise ValueError("initial_capital은 0보다 커야 합니다.")
    if not 0 <= commission_rate < 1 or not 0 <= slippage_rate < 1:
        raise ValueError("수수료율과 슬리피지는 0 이상 1 미만이어야 합니다.")
    if signals.empty:
        raise ValueError("백테스트할 가격 데이터가 없습니다.")

    cash = float(initial_capital)
    shares = 0
    entry_cost = 0.0
    trades: list[dict] = []
    completed_returns: list[float] = []
    equity_values: list[float] = []

    for index, (date, row) in enumerate(signals.iterrows()):
        if index > 0:
            prior_signal = signals.iloc[index - 1]["signal"]
            open_price = float(row["open"])
            if prior_signal == "BUY" and shares == 0:
                fill_price = open_price * (1 + slippage_rate)
                cost_per_share = fill_price * (1 + commission_rate)
                quantity = int(cash // cost_per_share)
                if quantity > 0:
                    entry_cost = quantity * cost_per_share
                    cash -= entry_cost
                    shares = quantity
                    trades.append({
                        "signal_date": _date_string(signals.index[index - 1]),
                        "execution_date": _date_string(date),
                        "side": "BUY",
                        "price": round(fill_price, 4),
                        "quantity": quantity,
                    })
            elif prior_signal == "SELL" and shares > 0:
                fill_price = open_price * (1 - slippage_rate)
                proceeds = shares * fill_price * (1 - commission_rate)
                completed_returns.append((proceeds - entry_cost) / entry_cost)
                trades.append({
                    "signal_date": _date_string(signals.index[index - 1]),
                    "execution_date": _date_string(date),
                    "side": "SELL",
                    "price": round(fill_price, 4),
                    "quantity": shares,
                })
                cash += proceeds
                shares = 0
                entry_cost = 0.0

        equity_values.append(cash + shares * float(row["close"]))

    equity = pd.Series(equity_values, index=signals.index, dtype=float)
    daily_returns = equity.pct_change().dropna()
    return_rate = (equity.iloc[-1] / initial_capital - 1) * 100
    running_peak = equity.cummax()
    max_drawdown = ((equity / running_peak) - 1).min() * 100
    volatility = daily_returns.std(ddof=0)
    sharpe_ratio = 0.0
    if volatility and not pd.isna(volatility):
        sharpe_ratio = float(daily_returns.mean() / volatility * sqrt(252))

    elapsed_days = max((signals.index[-1] - signals.index[0]).days, 1)
    cagr = ((equity.iloc[-1] / initial_capital) ** (365 / elapsed_days) - 1) * 100
    benchmark_return = (
        float(signals["close"].iloc[-1] / signals["close"].iloc[0] - 1) * 100
    )
    wins = sum(result > 0 for result in completed_returns)

    return {
        "initial_capital": round(initial_capital, 2),
        "final_value": round(float(equity.iloc[-1]), 2),
        "return_rate": round(float(return_rate), 2),
        "buy_and_hold_return_rate": round(benchmark_return, 2),
        "cagr": round(float(cagr), 2),
        "max_drawdown": round(float(max_drawdown), 2),
        "sharpe_ratio": round(sharpe_ratio, 4),
        "trade_count": len(completed_returns),
        "win_rate": round(wins / len(completed_returns) * 100, 2) if completed_returns else 0.0,
        "open_position": shares > 0,
        "trades": trades,
        "equity_curve": [
            {"date": _date_string(date), "value": round(float(value), 2)}
            for date, value in equity.items()
        ],
    }


def _date_string(value) -> str:
    return value.date().isoformat() if hasattr(value, "date") else str(value)
