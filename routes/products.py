from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
import pickle
from datetime import datetime
import numpy as np

# 🧩 Custom utils
from backend.utils.amp import get_amp_for_product
from backend.utils.expiry import get_expiry_score
from backend.utils.holidays import get_category_holiday_score

router = APIRouter()

class ProductRequest(BaseModel):
    state: str
    location_zone: str

@router.post("/products")
def get_dynamic_products(user: ProductRequest):
    try:
        # ✅ Load metadata
        meta_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "full_retail_meta_dataset.csv")
        )
        df = pd.read_csv(meta_path)

        # ✅ Filter products
        filtered_df = df[
            (df["state"] == user.state) &
            (df["location_zone"] == user.location_zone)
        ].copy()

        if filtered_df.empty:
            return {"message": "No products available for your region"}

        # 🧠 AMP
        filtered_df["amp"] = filtered_df.apply(
            lambda row: get_amp_for_product(row["product_name"], user.state, user.location_zone),
            axis=1
        )

        # ⏳ Expiry
        today = datetime.now()
        filtered_df["expiry_date"] = pd.to_datetime(filtered_df["expiry_date"], errors="coerce")
        filtered_df["expiry_score"] = filtered_df["expiry_date"].apply(lambda x: get_expiry_score(x, today))
        filtered_df["expiry_days"] = filtered_df["expiry_date"].apply(
            lambda x: max((pd.to_datetime(x) - pd.Timestamp(today)).days, 0)
        )

        # 🎯 Holiday score
        filtered_df["holiday_score"] = filtered_df.apply(
            lambda row: get_category_holiday_score(user.state, row["category"], today),
            axis=1
        )

        # ✅ Load model
        model_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "models", "pricing_model.pkl")
        )
        print("🧠 [DEBUG] Loading model from:", model_path)

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        # 🎯 Features to predict
        features = [
            "amp",
            "inventory_level",
            "mrp",
            "holiday_score",
            "brand_reputation_score",
            "expiry_score",
            "location_zone"
        ]
        X = filtered_df[features].copy()

        # 🔮 Predict prices
        predicted_prices = model.predict(X)
        filtered_df["final_price"] = [
            float(f"{min(price, mrp):.2f}") for price, mrp in zip(predicted_prices, filtered_df["mrp"])
        ]

        # ✅ Final output
        result = filtered_df[[
            "product_name",
            "category",
            "mrp",
            "final_price",
            "inventory_level",
            "expiry_days"
        ]].to_dict(orient="records")

        return {"products": result}

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"File not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
