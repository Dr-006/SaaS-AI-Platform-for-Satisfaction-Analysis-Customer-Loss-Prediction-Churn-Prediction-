# backend/app/routes/feedback.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import FeedbackRequest, FeedbackResponse
from app.models import Feedback
from app.database import SessionLocal
from app.services import sentiment_service

router = APIRouter(prefix="/feedback", tags=["feedback"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=FeedbackResponse)
def submit_feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    try:
        score = sentiment_service.get_sentiment_score(request.text)
    except Exception:
        score = 0.5  # fallback neutral

    if score < 0.35:
        label = "negative"
    elif score > 0.65:
        label = "positive"
    else:
        label = "neutral"

    fb = Feedback(
        text=request.text,
        sentiment_score=score,
        sentiment_label=label,
        customer_id=request.customer_id,
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)

    return FeedbackResponse(
        id=fb.id,
        text=fb.text,
        sentiment_score=fb.sentiment_score,
        sentiment_label=fb.sentiment_label,
    )


@router.get("/", response_model=list[FeedbackResponse])
def list_feedbacks(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).order_by(Feedback.id.desc()).offset(skip).limit(limit).all()
    return [
        FeedbackResponse(
            id=f.id,
            text=f.text,
            sentiment_score=f.sentiment_score or 0.5,
            sentiment_label=f.sentiment_label or "neutral",
        )
        for f in feedbacks
    ]