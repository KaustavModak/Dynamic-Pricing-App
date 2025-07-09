import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
import numpy as np
from datetime import datetime

from backend.utils.holidays import get_holiday_score_for_state
from backend.utils.expiry import get_expiry_score

# --- CONFIG ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
META_PATH = os.path.join(BASE_DIR, 'data', 'full_retail_meta_dataset.csv')
SALES_PATH = os.path.join(BASE_DIR, 'data', 'sales_data.csv')
OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'training_data.csv')

def generate_training_data():
    # Load data
    meta_df = pd.read_csv(META_PATH)
    sales_df = pd.read_csv(SALES_PATH)

    # Merge on multiple keys
    merged = pd.merge(
        sales_df,
        meta_df,
        on=['product_name', 'category', 'state', 'location_zone', 'mrp'],
        how='left'
    )

    # Convert to datetime
    merged['date'] = pd.to_datetime(merged['date'], errors='coerce')
    merged['expiry_date'] = pd.to_datetime(merged['expiry_date'], errors='coerce')

    # Drop invalid dates
    merged = merged.dropna(subset=['date', 'expiry_date'])

    # ✅ Add expiry score
    merged['expiry_score'] = merged.apply(
        lambda row: get_expiry_score(row['expiry_date'], row['date']), axis=1
    )

    # ✅ Add holiday score
    merged['holiday_score'] = merged.apply(
        lambda row: get_holiday_score_for_state(row['state'], row['date']), axis=1
    )

    # ✅ Amplify scores
    merged['holiday_score'] *= 1.5

    # ✅ Compute AMP
    def compute_amp(group):
        total_units = group['units_sold'].sum()
        if total_units == 0:
            return pd.Series({'amp': group['mrp'].mean()})
        revenue = (group['discounted_price'] * group['units_sold']).sum()
        return pd.Series({'amp': round(revenue / total_units, 2)})

    amp_df = merged.groupby(['product_name', 'state', 'location_zone']).apply(compute_amp).reset_index()
    merged = pd.merge(merged, amp_df, on=['product_name', 'state', 'location_zone'], how='left')

    # ✅ Define location zone factor
    def location_zone_factor(zone):
        if zone == 'Tier-1':
            return 0.02
        elif zone == 'Tier-2':
            return 0.01
        elif zone == 'Tier-3':
            return -0.01
        return 0

    # ✅ Compute raw price using all influencing factors
    merged['raw_price'] = merged.apply(
        lambda row: row['amp'] * (
            1
            + 0.03 * row['holiday_score']
            - 0.04 * row['expiry_score']
            + 0.02 * row['brand_reputation_score']
            + location_zone_factor(row['location_zone'])
        ),
        axis=1
    )

    # ✅ Clamp final price between amp and mrp
    merged['final_price'] = merged.apply(
        lambda row: round(min(max(row['raw_price'], row['amp']), row['mrp']), 2),
        axis=1
    )

    # Final cleaned DataFrame
    final_df = merged[[ 
        'product_name', 'category', 'mrp', 'amp',
        'brand_reputation_score', 'expiry_score',
        'holiday_score', 'inventory_level',
        'location_zone', 'final_price'
    ]].drop_duplicates()

    # Save
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    final_df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Training dataset saved to {OUTPUT_PATH}")

if __name__ == '__main__':
    generate_training_data()
