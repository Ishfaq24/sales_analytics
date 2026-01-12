import pandas as pd

def clean_sales_data(sales_df):
    # Remove duplicates
    sales_df = sales_df.drop_duplicates()

    # Convert date column
    sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])

    # Fix invalid values
    sales_df['quantity'] = sales_df['quantity'].clip(lower=1)
    sales_df['price'] = sales_df['price'].clip(lower=0)

    # Handle missing values
    sales_df.fillna(0, inplace=True)

    return sales_df
