def generate_insights(monthly_sales, growth_rate, df):
    insights = []

    # ------------------------------------------------
    # SAFE GROWTH INSIGHT
    # ------------------------------------------------
    valid_growth = growth_rate.dropna()

    if len(valid_growth) == 0:
        insights.append(
            "ℹ️ Not enough historical data to calculate growth trends."
        )
    else:
        latest_growth = valid_growth.iloc[-1]

        if latest_growth > 0:
            insights.append(
                f"📈 Revenue increased by {latest_growth:.2f}% in the latest period."
            )
        else:
            insights.append(
                f"📉 Revenue decreased by {abs(latest_growth):.2f}% in the latest period."
            )

    # ------------------------------------------------
    # BEST MONTH INSIGHT
    # ------------------------------------------------
    if not monthly_sales.empty:
        best_month = monthly_sales.idxmax().strftime("%B %Y")
        insights.append(f"🏆 Best performing month: {best_month}.")

    # ------------------------------------------------
    # CATEGORY & REGION DRIVER
    # ------------------------------------------------
    if "revenue" not in df.columns:
        df = df.copy()
        df["revenue"] = df["quantity"] * df["price"]

    if "category" in df.columns and "region" in df.columns:
        top_category = df.groupby("category")["revenue"].sum().idxmax()
        top_region = df.groupby("region")["revenue"].sum().idxmax()

        insights.append(
            f"💡 Top revenue driver: {top_category} category in {top_region} region."
        )

    return insights
