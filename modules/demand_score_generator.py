import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

def compute_demand_score(input_path='../data/sales_data.csv', output_path='../data/sales_data.csv'):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"❌ Input file not found: {input_path}")

    df = pd.read_csv(input_path)

    # Remove old demand_score if it exists
    if 'demand_score' in df.columns:
        df.drop(columns=['demand_score'], inplace=True)

    # Ensure required columns exist
    if 'product_name' not in df.columns or 'units_sold' not in df.columns:
        raise ValueError("❌ Missing required columns: 'product_name' or 'units_sold'.")

    # Compute total demand per product
    demand_df = df.groupby('product_name')['units_sold'].sum().reset_index()
    demand_df.columns = ['product_name', 'total_units_sold']

    # Normalize demand
    scaler = MinMaxScaler()
    demand_df['demand_score'] = scaler.fit_transform(demand_df[['total_units_sold']]).round(2)

    # Merge into sales data
    df = df.merge(demand_df[['product_name', 'demand_score']], on='product_name', how='left')

    # Save updated data
    df.to_csv(output_path, index=False)
    print(f"✅ Demand scores added and saved to: {output_path}")

# Run if executed directly
if __name__ == '__main__':
    compute_demand_score()
