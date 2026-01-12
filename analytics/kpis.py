import numpy as np

def calculate_kpis(df):
    # Revenue column
    df['revenue'] = df['quantity'] * df['price']

    total_revenue = np.sum(df['revenue'])
    avg_order_value = np.mean(df['revenue'])

    top_products = (
        df.groupby('product_name')['revenue']
        .sum()
        .sort_values(ascending=False)
    )

    top_customers = (
        df.groupby('name')['revenue']
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "total_revenue": total_revenue,
        "avg_order_value": avg_order_value,
        "top_products": top_products,
        "top_customers": top_customers
    }
