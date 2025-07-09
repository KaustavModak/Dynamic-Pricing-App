from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
from datetime import datetime

# 💡 Import brand reputation utils
from backend.utils.brand import get_brand_reputation_score

router = APIRouter()

class NewProduct(BaseModel):
    product_name: str
    category: str
    mrp: float
    manufacturing_date: str  # Format: YYYY-MM-DD
    expiry_date: str         # Format: YYYY-MM-DD
    location_zone: str
    state: str
    inventory_level: int

@router.post("/new_product")
def add_new_product(product: NewProduct):
    try:
        meta_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "full_retail_meta_dataset.csv")
        )

        if not os.path.exists(meta_path):
            raise HTTPException(status_code=500, detail="Metadata CSV not found.")

        df = pd.read_csv(meta_path)

        # ✅ Check for existing product in same region
        duplicate = df[
            (df["product_name"] == product.product_name) &
            (df["state"] == product.state) &
            (df["location_zone"] == product.location_zone)
        ]

        if not duplicate.empty:
            raise HTTPException(status_code=400, detail="Product already exists in this region.")

        # 🔍 Compute brand reputation dynamically
        brand_score = get_brand_reputation_score(product.product_name)

        # ✅ Convert new entry to DataFrame row
        new_row = pd.DataFrame([{
            "product_name": product.product_name,
            "category": product.category,
            "mrp": product.mrp,
            "manufacturing_date": product.manufacturing_date,
            "expiry_date": product.expiry_date,
            "location_zone": product.location_zone,
            "state": product.state,
            "inventory_level": product.inventory_level,
            "brand_reputation_score": brand_score
        }])

        # ✅ Concatenate instead of append
        updated_df = pd.concat([df, new_row], ignore_index=True)
        updated_df.to_csv(meta_path, index=False)

        return {"message": "✅ Product added successfully with brand reputation!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
