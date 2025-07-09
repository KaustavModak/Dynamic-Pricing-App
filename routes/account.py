from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os

router = APIRouter()

class AccountRequest(BaseModel):
    id: str
    password: str

@router.post("/account")
def get_account_details(request: AccountRequest):
    try:
        # ✅ Corrected path to access users.json OUTSIDE backend
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "users.json")
        )

        with open(file_path, "r") as f:
            users = json.load(f)

        for user in users:
            if user["user_id"] == request.id and user["password"] == request.password:
                return {
                    "user_id": user["user_id"],
                    "state": user["state"],
                    "location_zone": user["location_zone"]
                }

        raise HTTPException(status_code=401, detail="Invalid credentials")

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="users.json file not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
