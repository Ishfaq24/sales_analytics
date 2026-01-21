# 📊 Sales Intelligence Platform

An **enterprise-grade Sales & Business Intelligence platform** built with **Python, Pandas, NumPy, Streamlit**, and an optional **AI-powered executive narrative layer**.

This project simulates a **real-world analytics product** used by business teams and leadership to analyze sales data, monitor KPIs, forecast performance, generate insights, and store historical reports.

---

## 🚀 Why This Project Matters

This is **not a basic dashboard**.

It is designed as a **product** with:
- Schema-adaptive data ingestion
- Executive-level analytics
- Predictive forecasting
- Saved report history
- AI-driven decision narratives

The architecture and feature set closely resemble **modern BI / analytics SaaS platforms**.

---

## 🧠 Key Features
https://sales-analytics-ib24.streamlit.app/

### 📥 Data Ingestion
- Upload **Sales**, **Customers**, and **Products** CSV files
- Automatic dataset merging
- Handles messy, real-world data

### 🧹 Schema-Adaptive Normalization
Automatically detects and normalizes:
- `region` (region / country / city fallback)
- `customer_name` (name / email / username fallback)
- `price`, `quantity`, and `revenue`

Prevents crashes due to inconsistent schemas.

---

## 📈 Analytics & KPIs

- Total Revenue
- Average Order Value (AOV)
- Monthly revenue trends
- Growth rate analysis
- Segment-level insights

Built using:
- **Pandas** (`groupby`, `merge`, `resample`)
- **NumPy** (vectorized metrics)

---

## 🔮 Forecasting Engine

### Baseline Forecast
- Robust trend-based forecasting
- Works with limited data

### Advanced Forecasting (ARIMA)
- Automatically applied when sufficient history exists
- Safe fallback when data is insufficient
- Production-stable (no crashes)

---

## 🧠 Executive Decision Engine

Generates:
- **Business Health Score (0–100)**
- Risk detection:
  - Negative growth
  - Revenue concentration
  - High volatility
- Strategic recommendations:
  - Regional focus
  - Category diversification
  - Performance improvements

Designed to mimic **real executive dashboards**.

---

## 🤖 AI Executive Narrative (Optional)

An **LLM-powered intelligence layer** that converts analytics into **CEO-style summaries**.

Example:
> “Revenue growth is driven by Electronics in the South region, though volatility suggests diversification is recommended.”

Features:
- OpenAI-compatible API
- Safe fallback when API key is missing
- Frontend-only integration (no backend dependency)

---

## 💾 Saved Reports & History

- Save reports including:
  - Filters
  - KPIs
  - Insights
  - Health score
- Persistent local storage
- Fault-tolerant handling of empty or corrupted files
- Enables historical analysis and auditing

---

## 📤 Export Capabilities

- Download filtered data (CSV)
- Download KPI summary (JSON)
- Download business insights (TXT)

---

## 🖥️ User Interface

Built using **Streamlit**:
- Interactive filters
- KPI cards
- Forecast charts
- Executive summaries
- Clean, leadership-friendly layout

---

## 🏗️ Project Structure
```text
sales_analytics/
│
├── analytics/
│   ├── forecasting.py        # Baseline forecasting
│   ├── advanced_forecast.py  # ARIMA forecasting
│   ├── decisions.py          # Executive decision engine
│   ├── alerts.py             # Risk & alert detection
│   └── llm_narrative.py      # AI executive summaries
│
├── app/
│   ├── engine.py             # Core analytics engine
│   ├── config.py             # Configurations
│   └── report_store.py       # Saved reports persistence
│
├── ui/
│   └── streamlit_app.py      # Frontend application
│
├── reports/
│   └── reports.json          # Saved report history
│
├── data/
│   ├── sales.csv
│   ├── customers.csv
│   └── products.csv
│
├── README.md
└── requirements.txt
```
# ⚙️ Requirements
```

# ⚙️ Requirements

Python 3.9+

pandas
numpy
streamlit
requests
statsmodels
openai
```
## 📦 Installation
```
git clone https://github.com/ishfaq24/sales_analytics.git
cd sales_analytics
pip install -r requirements.txt


```
