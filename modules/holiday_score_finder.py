import os
import pandas as pd
from datetime import datetime

# ✅ Clean absolute path to holidays.csv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOLIDAY_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'data', 'holidays.csv'))
WINDOW_DAYS = 7

def get_holiday_score_for_state(state: str, today: datetime = None) -> int:
    today = today or datetime.today()
    try:
        df_holidays = pd.read_csv(HOLIDAY_PATH)
        df_holidays['date'] = pd.to_datetime(df_holidays['date'], errors='coerce')

        relevant = df_holidays[df_holidays['state'].str.lower().isin([state.lower(), 'national'])]
        for _, row in relevant.iterrows():
            if pd.isna(row['date']):
                continue
            if abs((row['date'] - today).days) <= WINDOW_DAYS:
                return 10
        return 0
    except Exception as e:
        print(f"[Holiday Score Error] {e}")
        return 0
