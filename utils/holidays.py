import os
import pandas as pd
from datetime import datetime

# 📂 Path Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOLIDAY_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'data', 'holidays.csv'))
WINDOW_DAYS = 7

# 🗺️ Mapping holiday names to relevant product categories
HOLIDAY_CATEGORY_MAP = {
    "Diwali": ["sweets", "snacks"],
    "Holi": ["sweets", "beverages"],
    "Christmas": ["toys", "sweets"],
    "Independence Day": ["stationery", "snacks"],
    "Republic Day": ["stationery", "snacks"],
    "Makar Sankranti": ["sweets"],
    "Onam": ["sweets"],
    "Ugadi": ["sweets"],
    "Bohag Bihu": ["sweets"],
    "Maha Shivratri": ["snacks"],
    "Good Friday": ["toys"],
    "Children's Day": ["toys"],
}

# 🧠 Generic holiday score (state-only)
def get_generic_holiday_score(state: str, today: datetime = None) -> float:
    today = today or datetime.today()
    if isinstance(today, pd.Timestamp):
        today = today.to_pydatetime()

    try:
        df = pd.read_csv(HOLIDAY_PATH)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        relevant = df[df['state'].str.lower().isin([state.lower(), 'all', 'national'])]

        for _, row in relevant.iterrows():
            if pd.isna(row['date']):
                continue
            delta_days = abs((row['date'] - today).days)
            if delta_days <= WINDOW_DAYS:
                return round((WINDOW_DAYS - delta_days) / WINDOW_DAYS, 2)
        return 0.0
    except Exception as e:
        print(f"[Generic Holiday Score Error] {e}")
        return 0.0

# 🧠 Category-aware holiday score
def get_category_holiday_score(state: str, category: str, today: datetime = None) -> float:
    today = today or datetime.today()
    if isinstance(today, pd.Timestamp):
        today = today.to_pydatetime()

    try:
        df = pd.read_csv(HOLIDAY_PATH)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        relevant = df[df['state'].str.lower().isin([state.lower(), 'all', 'national'])]

        max_score = 0.0
        for _, row in relevant.iterrows():
            if pd.isna(row['date']):
                continue
            delta_days = (row['date'] - today).days
            if 0 <= delta_days <= WINDOW_DAYS:
                base_score = round((WINDOW_DAYS - delta_days) / WINDOW_DAYS, 2)
                boost = 0.2 if category.lower() in HOLIDAY_CATEGORY_MAP.get(row['name'], []) else 0.0
                max_score = max(max_score, min(1.0, base_score + boost))
        return max_score
    except Exception as e:
        print(f"[Category Holiday Score Error] {e}")
        return 0.0
