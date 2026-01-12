from app.config import CONFIG
from app.loader import load_csv_data
from app.engine import run_engine
from app.reporter import report_console, report_json

data = load_csv_data({
    "sales": "data/sales.csv",
    "customers": "data/customers.csv",
    "products": "data/products.csv"
})

results = run_engine(data, CONFIG)

if CONFIG["report_format"] == "console":
    report_console(results)
elif CONFIG["report_format"] == "json":
    report_json(results)
