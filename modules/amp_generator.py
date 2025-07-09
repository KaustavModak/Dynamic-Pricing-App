import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

# --- CONFIG ---
META_PATH = '../data/full_retail_meta_dataset.csv'
SALES_PATH = '../data/sales_data.csv'
AMP_OUTPUT_PATH = '../data/sales_data.csv'


def generate_amp():
    sales_df = pd.read_csv(SALES_PATH)
    meta_df = pd.read_csv(META_PATH)

    # Merge to get inventory_level for each product-state-zone
    merged = pd.merge(sales_df, meta_df, on=['product_name', 'category', 'state'], how='left')

    # Drop rows with missing inventory
    merged = merged.dropna(subset=['inventory_level'])

    # Calculate AMP based on units sold vs. inventory usage
    def compute_amp(group):
        total_units_sold = group['units_sold'].sum()
        total_inventory = group['inventory_level'].iloc[0]  # inventory is constant per group
        usage_ratio = total_units_sold / total_inventory if total_inventory > 0 else 0

        base_amp = (group['discounted_price'] * group['units_sold']).sum() / total_units_sold if total_units_sold > 0 else group['mrp'].mean()
        amp_score = base_amp * (0.7 + 0.3 * usage_ratio)  # emphasize better usage of inventory
        return round(amp_score, 2)

    amp_df = merged.groupby(['product_name', 'state', 'location_zone']).apply(compute_amp).reset_index()
    amp_df.columns = ['product_name', 'state', 'location_zone', 'amp']

    os.makedirs(os.path.dirname(AMP_OUTPUT_PATH), exist_ok=True)
    amp_df.to_csv(AMP_OUTPUT_PATH, index=False)
    print(f"✅ AMP dataset saved to: {AMP_OUTPUT_PATH}")


if __name__ == '__main__':
    generate_amp()
