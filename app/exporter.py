import json

def export_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def export_kpis(kpis):
    clean_kpis = {
        "total_revenue": kpis["total_revenue"],
        "average_order_value": kpis["avg_order_value"],
    }
    return json.dumps(clean_kpis, indent=4)

def export_insights(insights):
    return "\n".join(insights)
