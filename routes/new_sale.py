from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import os
from datetime import datetime

router = APIRouter()

SALES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'sales_data.csv'))
META_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'full_retail_meta_dataset.csv'))

class SaleRequest(BaseModel):
    product_name: str
    category: str
    state: str
    location_zone: str
    date: str = Field(..., example="2025-07-04")
    mrp: float
    discount_applied: float
    units_sold: int

@router.post("/new_sale")
def add_new_sale(sale: SaleRequest):
    try:
        # 🔍 Check if product exists in metadata
        meta_df = pd.read_csv(META_PATH)
        match = meta_df[
            (meta_df["product_name"] == sale.product_name) &
            (meta_df["state"] == sale.state) &
            (meta_df["location_zone"] == sale.location_zone)
        ]

        if match.empty:
            raise HTTPException(
                status_code=400,
                detail="Product does not exist in this state and location_zone. Please register the product first via /new_product."
            )

        # 📅 Validate date format
        try:
            datetime.strptime(sale.date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

        # ✅ Validate discount
        if sale.discount_applied > sale.mrp:
            raise HTTPException(status_code=400, detail="Discount applied cannot exceed MRP.")

        # 💰 Auto-compute discounted price
        discounted_price = round(sale.mrp - sale.discount_applied, 2)

        # 📝 Build sale row
        sale_dict = sale.dict()
        sale_dict["discounted_price"] = discounted_price
        sale_df = pd.DataFrame([sale_dict])

        # 📌 Append to file
        if os.path.exists(SALES_PATH):
            existing_df = pd.read_csv(SALES_PATH)
            updated_df = pd.concat([existing_df, sale_df], ignore_index=True)
        else:
            updated_df = sale_df

        updated_df.to_csv(SALES_PATH, index=False)
        return {"message": "✅ Sale entry successfully added."}

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Required file not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
