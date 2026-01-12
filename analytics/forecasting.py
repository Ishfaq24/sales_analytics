import numpy as np
import pandas as pd


def forecast_sales(monthly_sales, periods=3):
    """
    Robust sales forecasting with graceful degradation.
    Uses trend projection if possible, otherwise falls back
    to last-value / rolling mean forecast.
    """

    # -------------------------------
    # CLEAN INPUT
    # -------------------------------
    series = monthly_sales.dropna()

    # If not enough data → fallback
    if len(series) < 2:
        last_value = series.iloc[-1] if len(series) == 1 else 0

        forecast = np.full(periods, last_value)
        lower = forecast * 0.9
        upper = forecast * 1.1

        index = pd.date_range(
            start=monthly_sales.index[-1] if len(monthly_sales) else pd.Timestamp.today(),
            periods=periods + 1,
            freq="ME"
        )[1:]

        return pd.DataFrame(
            {
                "forecast": forecast,
                "lower_bound": lower,
                "upper_bound": upper,
            },
            index=index,
        )

    # -------------------------------
    # TRY LINEAR TREND
    # -------------------------------
    try:
        y = series.values.astype(float)
        x = np.arange(len(y))

        # Check variance (critical)
        if np.std(y) == 0:
            raise ValueError("Zero variance in data")

        m, c = np.polyfit(x, y, 1)

        future_x = np.arange(len(y), len(y) + periods)
        forecast = m * future_x + c

    except Exception:
        # -------------------------------
        # FALLBACK: ROLLING MEAN
        # -------------------------------
        rolling_mean = series.rolling(window=3, min_periods=1).mean().iloc[-1]
        forecast = np.full(periods, rolling_mean)

    # -------------------------------
    # CONFIDENCE BANDS
    # -------------------------------
    lower = forecast * 0.85
    upper = forecast * 1.15

    index = pd.date_range(
        start=series.index[-1],
        periods=periods + 1,
        freq="ME"
    )[1:]

    return pd.DataFrame(
        {
            "forecast": forecast,
            "lower_bound": lower,
            "upper_bound": upper,
        },
        index=index,
    )
