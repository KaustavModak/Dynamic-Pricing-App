from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os

router = APIRouter()

class LoginRequest(BaseModel):
    id: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    try:
        # Correct path to users.json
        file_path = os.path.join("data", "users.json")
        with open(file_path, "r") as f:
            users = json.load(f)
        
        for user in users:
            if user["user_id"] == request.id and user["password"] == request.password:
                return {
                    "message": "Login successful!",
                    "state": user["state"],
                    "location_zone": user["location_zone"]
                }

        raise HTTPException(status_code=401, detail="Invalid credentials")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
