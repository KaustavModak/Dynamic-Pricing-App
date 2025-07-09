import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SALES_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'data', 'sales_data.csv'))

def get_amp_for_product(product_name: str, state: str, location_zone: str) -> float:
    try:
        df = pd.read_csv(SALES_PATH)
        filtered = df[
            (df['product_name'] == product_name) &
            (df['state'] == state)
        ]
        if filtered.empty:
            return 0.0

        total_units = filtered['units_sold'].sum()
        if total_units == 0:
            return filtered['mrp'].mean()

        amp = (filtered['discounted_price'] * filtered['units_sold']).sum() / total_units
        return round(amp, 2)
    except Exception as e:
        print(f"[AMP Error] {e}")
        return 0.0
