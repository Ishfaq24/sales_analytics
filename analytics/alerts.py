def generate_alerts(monthly_sales, forecast_df):
    alerts = []

    recent_growth = monthly_sales.pct_change().iloc[-1]

    if recent_growth < -0.1:
        alerts.append(
            "🚨 Sales dropped more than 10% in the last month."
        )

    last_actual = monthly_sales.iloc[-1]
    next_forecast = forecast_df["forecast"].iloc[0]

    if next_forecast < last_actual:
        alerts.append(
            "⚠ Forecast indicates a potential decline next month."
        )

    if not alerts:
        alerts.append("✅ No immediate sales risks detected.")

    return alerts
