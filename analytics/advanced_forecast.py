import pandas as pd
import numpy as np

from statsmodels.tsa.arima.model import ARIMA


def arima_forecast(monthly_sales, periods=3):
    """
    Advanced ARIMA forecasting with full safety.
    Returns None if ARIMA cannot be applied.
    """

    # Clean input
    series = monthly_sales.dropna()

    # ARIMA needs enough data
    if len(series) < 6:
        return None

    try:
        # Simple ARIMA(1,1,1) – safe default
        model = ARIMA(series, order=(1, 1, 1))
        model_fit = model.fit()

        forecast = model_fit.forecast(steps=periods)

        index = pd.date_range(
            start=series.index[-1],
            periods=periods + 1,
            freq="ME"
        )[1:]

        forecast_df = pd.DataFrame(
            {
                "forecast": forecast.values,
                "lower_bound": forecast.values * 0.9,
                "upper_bound": forecast.values * 1.1,
            },
            index=index
        )

        return forecast_df

    except Exception:
        # Any ARIMA failure → graceful fallback
        return None
