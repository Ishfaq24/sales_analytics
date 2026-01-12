import sys
import os
import json
import pandas as pd
import streamlit as st

# --------------------------------------------------
# Fix Python path
# --------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.engine import run_engine
from app.config import CONFIG
from analytics.decisions import executive_decision_engine
from analytics.forecasting import smart_forecast
from analytics.alerts import generate_alerts
from app.report_store import save_report, load_reports

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Sales Intelligence Platform",
    layout="wide"
)

st.title("📊 Sales Intelligence Platform")
st.caption("Enterprise-grade, schema-adaptive sales analytics")

# --------------------------------------------------
# File Upload
# --------------------------------------------------
st.sidebar.header("📁 Upload Data")

sales_file = st.sidebar.file_uploader("Sales CSV", type="csv")
customers_file = st.sidebar.file_uploader("Customers CSV", type="csv")
products_file = st.sidebar.file_uploader("Products CSV", type="csv")

if not (sales_file and customers_file and products_file):
    st.info("👈 Upload all three CSV files to begin")
    st.stop()

# --------------------------------------------------
# Load & Merge Data
# --------------------------------------------------
sales = pd.read_csv(sales_file)
customers = pd.read_csv(customers_file)
products = pd.read_csv(products_file)

df = (
    sales
    .merge(customers, on="customer_id", how="left")
    .merge(products, on="product_id", how="left")
)

df["order_date"] = pd.to_datetime(df.get("order_date"), errors="coerce")

# --------------------------------------------------
# SCHEMA NORMALIZATION
# --------------------------------------------------

# ---- CATEGORY ----
if "category" not in df.columns:
    st.error("❌ Required column `category` not found.")
    st.stop()

# ---- REGION (DERIVE IF MISSING) ----
if "region" not in df.columns:
    if "country" in df.columns:
        df["region"] = df["country"]
        st.info("ℹ️ Region not found. Using `country`.")
    elif "city" in df.columns:
        df["region"] = df["city"]
        st.info("ℹ️ Region not found. Using `city`.")
    else:
        df["region"] = "Unknown"
        st.warning("⚠ No geographic column found. Using `Unknown`.")

# ---- CUSTOMER NAME NORMALIZATION ----
def find_customer_name_column(df):
    candidates = [
        "customer_name",
        "name",
        "full_name",
        "username",
        "email"
    ]
    for col in candidates:
        if col in df.columns:
            return col
    return None

customer_name_col = find_customer_name_column(df)

if customer_name_col is None:
    df["customer_name"] = "Unknown Customer"
    st.warning("⚠ No customer name column found. Using 'Unknown Customer'.")
else:
    if customer_name_col != "customer_name":
        df = df.rename(columns={customer_name_col: "customer_name"})

# ---- REVENUE NORMALIZATION ----
if "price" not in df.columns:
    if "unit_price" in df.columns:
        df["price"] = df["unit_price"]
    else:
        df["price"] = 0

if "quantity" not in df.columns:
    df["quantity"] = 1

if "total_amount" in df.columns:
    df["revenue"] = df["total_amount"]
else:
    df["revenue"] = df["quantity"] * df["price"]

# --------------------------------------------------
# Filters
# --------------------------------------------------
st.sidebar.header("🎛️ Filters")

regions = ["All"] + sorted(df["region"].dropna().unique().tolist())
categories = ["All"] + sorted(df["category"].dropna().unique().tolist())

selected_region = st.sidebar.selectbox("Region", regions)
selected_category = st.sidebar.selectbox("Category", categories)

min_date = df["order_date"].min()
max_date = df["order_date"].max()

date_range = st.sidebar.date_input(
    "Order Date Range",
    [min_date, max_date]
)

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------
filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

filtered_df = filtered_df[
    (filtered_df["order_date"] >= pd.to_datetime(date_range[0])) &
    (filtered_df["order_date"] <= pd.to_datetime(date_range[1]))
]

# --------------------------------------------------
# Run Analytics Engine
# --------------------------------------------------
results = run_engine(
    {
        "sales": filtered_df[
            ["order_id", "order_date", "customer_id", "product_id", "quantity", "price"]
        ],
        "customers": filtered_df[
            ["customer_id", "customer_name", "region", "signup_date"]
        ].rename(columns={"customer_name": "name"}).drop_duplicates(),
        "products": filtered_df[
            ["product_id", "product_name", "category"]
        ].drop_duplicates(),
    },
    CONFIG
)

# --------------------------------------------------
# Executive Decision Engine
# --------------------------------------------------
executive = executive_decision_engine(
    filtered_df,
    results["monthly_sales"],
    results["growth"]
)
# --------------------------------------------------
# ADVANCED FORECASTING & ALERTS
# --------------------------------------------------
forecast_df, model_used = smart_forecast(results["monthly_sales"])
alerts = generate_alerts(results["monthly_sales"], forecast_df)

st.markdown("---")
st.subheader("🔮 Sales Forecast & Alerts")

st.caption(f"Forecasting model used: **{model_used}**")

st.line_chart(
    pd.concat(
        [
            results["monthly_sales"].rename("Actual"),
            forecast_df["forecast"].rename("Forecast"),
        ],
        axis=1,
    )
)

with st.expander("📊 Forecast Details"):
    st.dataframe(forecast_df)

# --------------------------------------------------
# KPIs
# --------------------------------------------------
st.subheader("📈 Key Performance Indicators")

c1, c2 = st.columns(2)
c1.metric("Total Revenue", f"{results['kpis']['total_revenue']}")
c2.metric("Avg Order Value", f"{results['kpis']['avg_order_value']:.2f}")

# --------------------------------------------------
# Insights
# --------------------------------------------------
st.subheader("💡 Business Insights")

context = f"(Region: {selected_region}, Category: {selected_category})"
for insight in results["insights"]:
    st.success(f"{insight} {context}")

# --------------------------------------------------
# Export Section
# --------------------------------------------------
st.subheader("📤 Export Reports")

col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(
        "⬇️ Filtered Data (CSV)",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_sales_data.csv",
        mime="text/csv",
    )

with col2:
    kpi_payload = {
        "total_revenue": float(results["kpis"]["total_revenue"]),
        "average_order_value": float(results["kpis"]["avg_order_value"]),
    }
    st.download_button(
        "⬇️ KPI Summary (JSON)",
        data=json.dumps(kpi_payload, indent=4),
        file_name="kpi_summary.json",
        mime="application/json",
    )

with col3:
    st.download_button(
        "⬇️ Insights (TXT)",
        data="\n".join(results["insights"]),
        file_name="business_insights.txt",
        mime="text/plain",
    )

# --------------------------------------------------
# Executive Summary
# --------------------------------------------------
st.markdown("---")
st.subheader("🧠 Executive Decision Summary")

health = executive["health_score"]

if health >= 75:
    st.success(f"🟢 Business Health: {health}/100 (Strong)")
elif health >= 50:
    st.warning(f"🟡 Business Health: {health}/100 (Moderate)")
else:
    st.error(f"🔴 Business Health: {health}/100 (At Risk)")

st.markdown("### ⚠ Risks")
if executive["risks"]:
    for r in executive["risks"]:
        st.warning(r)
else:
    st.success("No major risks detected.")

st.markdown("### 💡 Recommendations")
for rec in executive["recommendations"]:
    st.info(rec)


# --------------------------------------------------
# SAVE REPORT (PRODUCT FEATURE)
# --------------------------------------------------
st.markdown("---")
st.subheader("💾 Save This Report")

report_name = st.text_input("Report name", "Monthly Sales Overview")

if st.button("💾 Save Report"):
    report_payload = {
        "name": report_name,
        "filters": {
            "region": selected_region,
            "category": selected_category,
            "date_range": [str(date_range[0]), str(date_range[1])]
        },
        "kpis": {
            "total_revenue": float(results["kpis"]["total_revenue"]),
            "avg_order_value": float(results["kpis"]["avg_order_value"])
        },
        "health_score": executive["health_score"],
        "insights": results["insights"]
    }

    save_report(report_payload)
    st.success("✅ Report saved successfully!")



# --------------------------------------------------
# Data Preview
# --------------------------------------------------
with st.expander("🔍 View Filtered Data"):
    st.dataframe(filtered_df)
