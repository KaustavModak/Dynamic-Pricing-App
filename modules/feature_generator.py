import pandas as pd
import numpy as np
from datetime import datetime
import os

# 📁 File Paths
META_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "full_retail_meta_dataset.csv"))
SALES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "sales_data.csv"))
HOLIDAY_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "holiday_calendar.csv"))  # optional

# 🧮 AMP (Average Market Price) Calculator
def compute_amp(sales_df, product_name, category, state, zone):
    filtered = sales_df[
        (sales_df["product_name"] == product_name) &
        (sales_df["category"] == category) &
        (sales_df["state"] == state) &
        (sales_df["location_zone"] == zone)
    ]
    if not filtered.empty:
        return round(filtered["discounted_price"].mean(), 2)
    return np.nan

# ⏳ Expiry Score (0.0 if expired, else normalized days left)
def compute_expiry_score(row, current_date=None):
    if current_date is None:
        current_date = datetime.today().date()
    expiry = pd.to_datetime(row["expiry_date"]).date()
    mfg = pd.to_datetime(row["manufacturing_date"]).date()
    total_shelf_life = (expiry - mfg).days
    days_left = (expiry - current_date).days
    if days_left <= 0:
        return 0.0
    return round(days_left / total_shelf_life, 2)

# 🎉 Holiday Score (if you have one)
def get_holiday_score(state, date):
    return 0.8  # Placeholder or fetch from your holiday calendar module

# 🛠️ Feature builder
def build_features(state, location_zone):
    meta = pd.read_csv(META_PATH)
    sales = pd.read_csv(SALES_PATH)

    filtered = meta[
        (meta["state"] == state) & (meta["location_zone"] == location_zone)
    ].copy()

    if filtered.empty:
        return []

    enriched_rows = []

    for _, row in filtered.iterrows():
        amp = compute_amp(sales, row["product_name"], row["category"], row["state"], row["location_zone"])
        expiry_score = compute_expiry_score(row)
        holiday_score = get_holiday_score(row["state"], datetime.today().date())

        enriched = {
            "mrp": row["mrp"],
            "brand_reputation_score": row["brand_reputation_score"],
            "expiry_score": expiry_score,
            "holiday_score": holiday_score,
            "inventory_level": row["inventory_level"],
            "amp": amp,
            "location_zone": row["location_zone"],
            "product_name": row["product_name"],
            "category": row["category"],
            "state": row["state"]
        }
        enriched_rows.append(enriched)

    return enriched_rows
