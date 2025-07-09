import pandas as pd
import os
from datetime import datetime, timedelta

# --- CONFIG ---
META_PATH = '../data/full_retail_meta_dataset.csv'
NEW_PRODUCTS_PATH = '../data/new_products.csv'  # User submits new products here


def load_existing_metadata():
    if os.path.exists(META_PATH):
        return pd.read_csv(META_PATH)
    else:
        return pd.DataFrame(columns=[
            'product_name', 'category', 'mrp', 'manufacturing_date', 'expiry_date',
            'location_zone', 'state', 'inventory_level'
        ])


def process_new_products(df_new):
    today = datetime.today()
    processed = []

    for _, row in df_new.iterrows():
        try:
            product_name = row['product_name']
            category = row['category']
            mrp = float(row['mrp'])
            location_zone = row['location_zone']
            state = row['state']
            inventory = int(row['inventory_level'])

            # Handle missing manufacturing/expiry dates
            if 'manufacturing_date' in row and pd.notna(row['manufacturing_date']):
                mfg_date = datetime.strptime(row['manufacturing_date'], '%Y-%m-%d')
            else:
                mfg_date = today - timedelta(days=int(row.get('age', 5)))

            if 'expiry_date' in row and pd.notna(row['expiry_date']):
                exp_date = datetime.strptime(row['expiry_date'], '%Y-%m-%d')
            else:
                exp_date = mfg_date + timedelta(days=int(row.get('shelf_life', 30)))

            processed.append([
                product_name, category, mrp,
                mfg_date.strftime('%Y-%m-%d'),
                exp_date.strftime('%Y-%m-%d'),
                location_zone, state, inventory
            ])

        except Exception as e:
            print(f"[⚠️ Skipped Row] {row.to_dict()} → {e}")

    return pd.DataFrame(processed, columns=[
        'product_name', 'category', 'mrp', 'manufacturing_date', 'expiry_date',
        'location_zone', 'state', 'inventory_level'
    ])


def update_metadata():
    if not os.path.exists(NEW_PRODUCTS_PATH):
        print("❌ No new_products.csv found.")
        return

    df_meta = load_existing_metadata()
    df_new = pd.read_csv(NEW_PRODUCTS_PATH)
    df_new_processed = process_new_products(df_new)

    combined = pd.concat([df_meta, df_new_processed], ignore_index=True)
    combined.drop_duplicates(subset=['product_name', 'state', 'location_zone'], keep='last', inplace=True)

    os.makedirs(os.path.dirname(META_PATH), exist_ok=True)
    combined.to_csv(META_PATH, index=False)
    print(f"✅ Updated metadata saved to {META_PATH} | +{len(df_new_processed)} new/updated rows")


if __name__ == '__main__':
    update_metadata()
