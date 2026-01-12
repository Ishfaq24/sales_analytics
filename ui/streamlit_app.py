import streamlit as st
import pandas as pd

import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.engine import run_engine
from app.config import CONFIG
# ---- Streamlit App ----

st.set_page_config(
    page_title="Sales Intelligence Platform",
    layout="wide"
)

st.title("📊 Sales & Business Intelligence Platform")
st.caption("Upload your data → Get instant insights")

# ---- File Upload ----
st.sidebar.header("📁 Upload Data")

sales_file = st.sidebar.file_uploader("Upload Sales CSV", type="csv")
customers_file = st.sidebar.file_uploader("Upload Customers CSV", type="csv")
products_file = st.sidebar.file_uploader("Upload Products CSV", type="csv")

if sales_file and customers_file and products_file:
    data = {
        "sales": pd.read_csv(sales_file),
        "customers": pd.read_csv(customers_file),
        "products": pd.read_csv(products_file),
    }

    results = run_engine(data, CONFIG)

    # ---- KPIs ----
    st.subheader("📈 Key Performance Indicators")

    col1, col2 = st.columns(2)
    col1.metric("Total Revenue", f"{results['kpis']['total_revenue']}")
    col2.metric("Avg Order Value", f"{results['kpis']['avg_order_value']:.2f}")

    # ---- Monthly Sales Chart ----
    st.subheader("⏱ Monthly Revenue Trend")
    st.line_chart(results["monthly_sales"])

    # ---- Growth ----
    st.subheader("📊 Growth Rate (%)")
    st.bar_chart(results["growth"])

    # ---- Insights ----
    st.subheader("💡 Automated Business Insights")
    for insight in results["insights"]:
        st.success(insight)

    # ---- Data Preview ----
    with st.expander("🔍 View Raw Data"):
        st.dataframe(data["sales"])

else:
    st.info("👈 Upload all three CSV files to start analysis")
