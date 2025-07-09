from datetime import datetime
import pandas as pd
def get_expiry_score(expiry_date, today=None) -> float:
    today = today or datetime.today()
    
    try:
        if isinstance(expiry_date, str):
            expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')
        elif isinstance(expiry_date, pd.Timestamp):
            expiry_date = expiry_date.to_pydatetime()
        
        days_left = (expiry_date - today).days
        if days_left <= 0:
            return 0.0
        elif days_left >= 30:
            return 1.0
        else:
            return round(days_left / 30, 2)
    except Exception as e:
        print(f"[Expiry Score Error] {e}")
        return 0.0
