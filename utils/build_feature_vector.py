import pandas as pd
import os
from datetime import datetime

from backend.utils.amp import get_amp_for_product
from backend.utils.expiry import get_expiry_score
from backend.utils.holidays import get_holiday_score_for_state
from backend.utils.trending import get_trending_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
META_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'data', 'full_retail_meta_dataset.csv'))

def build_feature_vector(product_name: str, state: str, location_zone: str, today: datetime = None) -> list:
    try:
        df = pd.read_csv(META_PATH)
        row = df[
            (df['product_name'] == product_name) &
            (df['state'] == state) &
            (df['location_zone'] == location_zone)
        ].iloc[0]

        mrp = row['mrp']
        inventory = row['inventory_level']
        brand_score = row['brand_reputation_score']
        amp = get_amp_for_product(product_name, state, location_zone)
        trending_score = get_trending_score(product_name)
        expiry_score = get_expiry_score(row['expiry_date'], today)
        holiday_score = get_holiday_score_for_state(state, today)

        return [
            float(mrp),
            float(inventory),
            float(brand_score),
            float(amp),
            float(trending_score),
            float(expiry_score),
            float(holiday_score)
        ]
    except Exception as e:
        print(f"[Feature Vector Error] {e}")
        return None
