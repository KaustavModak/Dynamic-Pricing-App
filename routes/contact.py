import os
import sys
from fastapi import APIRouter

# Add root path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
sys.path.append(ROOT_DIR)

router = APIRouter()

@router.get("/contact")
def contact_us():
    return {
        "team": [
            {"name": "Hiya Dutta", "email": "hiyadutta2255@gmail.com"},
            {"name": "Nabaruna Mutsuddi", "email": "mutsuddinabaruna@gmail.com"},
            {"name": "Parambrata Acharjee","email": "parambrataofficial@gmail.com"},
            {"name": "Kaustav Modak", "email": "kaustav.modak29@gmail.com"}
        ],
        "note": "Built as part of Walmart Hackathon for Indian retail market"
    }
