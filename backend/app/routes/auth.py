# backend/app/routes/auth.py
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/")
def auth():
    return {"message": "Auth endpoint"}