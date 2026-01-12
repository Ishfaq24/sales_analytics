import json

def report_console(results):
    print("\n📊 KPI SUMMARY")
    print("Total Revenue:", results["kpis"]["total_revenue"])
    print("Average Order Value:", results["kpis"]["avg_order_value"])

    print("\n🔥 BUSINESS INSIGHTS")
    for i in results["insights"]:
        print(i)


def report_json(results, path="storage/reports/report.json"):
    with open(path, "w") as f:
        json.dump(results, f, default=str, indent=4)
