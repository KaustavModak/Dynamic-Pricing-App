from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import os

router = APIRouter()

class ProductDeleteRequest(BaseModel):
    product_name: str
    state: str
    location_zone: str

@router.delete("/delete_product")
def delete_product(req: ProductDeleteRequest):
    try:
        meta_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "full_retail_meta_dataset.csv")
        )

        if not os.path.exists(meta_path):
            raise HTTPException(status_code=500, detail="Metadata CSV not found.")

        df = pd.read_csv(meta_path)

        # 🔍 Find matching row
        mask = (
            (df["product_name"] == req.product_name) &
            (df["state"] == req.state) &
            (df["location_zone"] == req.location_zone)
        )

        if not mask.any():
            raise HTTPException(status_code=404, detail="Product not found in the specified region.")

        # ❌ Delete row
        df = df[~mask]
        df.to_csv(meta_path, index=False)

        return {"message": "🗑️ Product deleted successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
