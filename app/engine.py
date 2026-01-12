from analytics.cleaning import clean_sales_data
from analytics.kpis import calculate_kpis
from analytics.time_analysis import time_series_analysis
from analytics.insights import generate_insights

def run_engine(data, config):
    sales = clean_sales_data(data["sales"])

    df = (
        sales
        .merge(data["customers"], on="customer_id")
        .merge(data["products"], on="product_id")
    )

    kpis = calculate_kpis(df)
    monthly, growth, best, worst = time_series_analysis(df)

    insights = []
    if config["enable_insights"]:
        insights = generate_insights(monthly, growth, df)

    return {
        "kpis": kpis,
        "monthly_sales": monthly,
        "growth": growth,
        "insights": insights
    }
