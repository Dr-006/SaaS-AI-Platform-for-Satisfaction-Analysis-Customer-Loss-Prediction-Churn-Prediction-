# backend/app/routes/dashboard.py
from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
def dashboard():
    return {"message": "Dashboard data"}