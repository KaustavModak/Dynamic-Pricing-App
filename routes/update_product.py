from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import pandas as pd
import os
from datetime import datetime

# 📦 Custom util to recompute brand reputation dynamically
from backend.utils.brand import get_brand_reputation_score

router = APIRouter()

class ProductUpdateRequest(BaseModel):
    product_name: str
    category: str
    state: str
    location_zone: str
    mrp: Optional[float] = None
    expiry_date: Optional[str] = None  # YYYY-MM-DD
    inventory_level: Optional[int] = None
    manufacturing_date: Optional[str] = Field(default=None, pattern=r"\d{4}-\d{2}-\d{2}")

@router.put("/update_product")
def update_product(update: ProductUpdateRequest):
    try:
        meta_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "full_retail_meta_dataset.csv")
        )

        if not os.path.exists(meta_path):
            raise HTTPException(status_code=500, detail="Metadata CSV not found.")

        df = pd.read_csv(meta_path)

        # 🔍 Match row to update
        mask = (
            (df["product_name"] == update.product_name) &
            (df["category"] == update.category) &
            (df["state"] == update.state) &
            (df["location_zone"] == update.location_zone)
        )

        if not mask.any():
            raise HTTPException(status_code=404, detail="Product not found in this region.")

        # 🧠 Preserve manufacturing_date if not provided
        if update.manufacturing_date:
            mfg_date = update.manufacturing_date
        else:
            mfg_date = df.loc[mask, "manufacturing_date"].values[0]

        # 🎯 Compute updated brand reputation
        brand_score = get_brand_reputation_score(update.product_name)

        # 🛠️ Update values
        df.loc[mask, "mrp"] = update.mrp if update.mrp is not None else df.loc[mask, "mrp"]
        df.loc[mask, "expiry_date"] = update.expiry_date if update.expiry_date else df.loc[mask, "expiry_date"]
        df.loc[mask, "inventory_level"] = update.inventory_level if update.inventory_level is not None else df.loc[mask, "inventory_level"]
        df.loc[mask, "manufacturing_date"] = mfg_date
        df.loc[mask, "brand_reputation_score"] = brand_score

        df.to_csv(meta_path, index=False)

        return {"message": "✅ Product updated successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
