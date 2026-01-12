def generate_insights(monthly_sales, growth_rate, df):
    insights = []

    latest_growth = growth_rate.dropna().iloc[-1]

    if latest_growth > 0:
        insights.append(
            f"📈 Revenue increased by {latest_growth:.2f}% in the latest month."
        )
    else:
        insights.append(
            f"📉 Revenue decreased by {abs(latest_growth):.2f}% in the latest month."
        )

    best_month = monthly_sales.idxmax().strftime('%B %Y')
    insights.append(f"🏆 Best performing month was {best_month}.")

    top_category = (
        df.groupby('category')['revenue']
        .sum()
        .idxmax()
    )

    top_region = (
        df.groupby('region')['revenue']
        .sum()
        .idxmax()
    )

    insights.append(
        f"💡 Top revenue driver: {top_category} category in {top_region} region."
    )

    return insights
