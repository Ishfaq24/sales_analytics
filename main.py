import pandas as pd

from analytics.cleaning import clean_sales_data
from analytics.kpis import calculate_kpis
from analytics.time_analysis import time_series_analysis
from analytics.insights import generate_insights

# Load data
sales = pd.read_csv("data/sales.csv")
customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")

# Clean
sales = clean_sales_data(sales)

# Merge
df = (
    sales
    .merge(customers, on="customer_id")
    .merge(products, on="product_id")
)

# KPIs
kpis = calculate_kpis(df)

# Time analysis
monthly_sales, growth_rate, best, worst = time_series_analysis(df)

# Insights
insights = generate_insights(monthly_sales, growth_rate, df)

# Output
print("\n📊 KPI SUMMARY")
print("Total Revenue:", kpis["total_revenue"])
print("Average Order Value:", kpis["avg_order_value"])

print("\n🔥 BUSINESS INSIGHTS")
for i in insights:
    print(i)
