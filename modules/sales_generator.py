import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

# --- CONFIG ---
META_PATH = '../data/full_retail_meta_dataset.csv'
SALES_PATH = '../data/sales_data.csv'

def generate_sales():
    meta_df = pd.read_csv(META_PATH)
    sales_data = []

    for _, row in meta_df.iterrows():
        product = row['product_name']
        category = row['category'].lower()
        state = row['state']
        mrp = row['mrp']
        zone = row['location_zone']

        try:
            mfg_date = datetime.strptime(row['manufacturing_date'], '%Y-%m-%d')
            exp_date = datetime.strptime(row['expiry_date'], '%Y-%m-%d')
        except:
            continue  # skip if date is malformed

        # ✅ Category-aware sales count
        if any(word in category for word in ['milk', 'fruit', 'vegetable', 'bread', 'snack', 'oil']):
            num_sales = np.random.choice([15, 20, 25, 30], p=[0.2, 0.3, 0.3, 0.2])
        elif any(word in category for word in ['soap', 'shampoo', 'detergent', 'cleaner', 'paste', 'beverage']):
            num_sales = np.random.choice([10, 12, 15, 18], p=[0.2, 0.3, 0.3, 0.2])
        else:
            num_sales = np.random.choice([5, 6, 7, 10], p=[0.25, 0.25, 0.25, 0.25])

        max_days = (exp_date - mfg_date).days
        if max_days <= 0:
            continue

        for _ in range(num_sales):
            sale_date = mfg_date + timedelta(days=np.random.randint(0, max_days + 1))

            discount_applied = np.random.choice([0, 5, 10, 15, 20], p=[0.3, 0.3, 0.2, 0.15, 0.05])
            discounted_price = round(mrp * (1 - discount_applied / 100), 2)

            base_units = np.random.randint(5, 30)
            multiplier = 1 + (discount_applied / 50)
            units_sold = int(base_units * multiplier)

            sales_data.append([
                product, row['category'], state, zone,
                sale_date.strftime('%Y-%m-%d'),
                mrp, discount_applied, discounted_price, units_sold
            ])

    sales_df = pd.DataFrame(sales_data, columns=[
        'product_name', 'category', 'state', 'location_zone', 'date',
        'mrp', 'discount_applied', 'discounted_price', 'units_sold'
    ])

    os.makedirs(os.path.dirname(SALES_PATH), exist_ok=True)
    sales_df.to_csv(SALES_PATH, index=False)
    print(f"✅ Sales dataset with location zone added saved to: {SALES_PATH}")

if __name__ == '__main__':
    generate_sales()
