# backend/app/routes/churn.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import ChurnRequest, ChurnResponse
from app.services.churn_service import predict_churn
from app.models import Prediction
from app.database import SessionLocal

router = APIRouter(prefix="/churn", tags=["churn"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/predict", response_model=ChurnResponse)
def churn_prediction(request: ChurnRequest, db: Session = Depends(get_db)):
    data = request.dict()
    data.pop("feedback_text", None)

    result = predict_churn(data)

    # Persist prediction to DB
    pred = Prediction(probability=result["probability"], prediction=result["prediction"])
    db.add(pred)
    db.commit()

    # Risk level label
    prob = result["probability"]
    if prob < 0.35:
        risk = "low"
    elif prob < 0.65:
        risk = "medium"
    else:
        risk = "high"

    return ChurnResponse(
        prediction=result["prediction"],
        probability=result["probability"],
        risk_level=risk,
    )