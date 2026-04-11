# backend/app/routes/feedback.py
from fastapi import APIRouter

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.get("/")
def get_feedback():
    return {"message": "Feedback endpoint"}