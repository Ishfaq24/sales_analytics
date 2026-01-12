def time_series_analysis(df):
    df = df.set_index('order_date')

    # FIX: use 'ME' instead of 'M'
    monthly_sales = df['revenue'].resample('ME').sum()
    growth_rate = monthly_sales.pct_change() * 100

    best_month = monthly_sales.idxmax()
    worst_month = monthly_sales.idxmin()

    return monthly_sales, growth_rate, best_month, worst_month
