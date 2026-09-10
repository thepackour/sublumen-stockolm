from __future__ import annotations

import pandas as pd


def simple_moving_average(series: pd.Series, window: int) -> pd.Series:
    """Return a simple moving average after a complete window is available."""
    return series.rolling(window=window, min_periods=window).mean()


def relative_strength_index(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Wilder's RSI, including stable values for flat price series."""
    delta = series.diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)
    average_gain = gains.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()
    average_loss = losses.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()

    relative_strength = average_gain / average_loss
    rsi = 100 - (100 / (1 + relative_strength))
    rsi = rsi.mask((average_loss == 0) & (average_gain > 0), 100.0)
    rsi = rsi.mask((average_loss == 0) & (average_gain == 0), 50.0)
    return rsi


def bollinger_bands(
    series: pd.Series,
    window: int = 20,
    standard_deviations: float = 2.0,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    middle = simple_moving_average(series, window)
    deviation = series.rolling(window=window, min_periods=window).std(ddof=0)
    upper = middle + standard_deviations * deviation
    lower = middle - standard_deviations * deviation
    return middle, upper, lower
