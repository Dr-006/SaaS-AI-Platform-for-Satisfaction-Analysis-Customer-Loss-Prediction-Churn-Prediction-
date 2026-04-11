# # backend/app/routes/churn.py
from fastapi import APIRouter
from app.schemas import ChurnRequest
from app.services.churn_service import predict_churn

router = APIRouter(prefix="/churn", tags=["churn"])


@router.post("/predict")
def churn_prediction(request: ChurnRequest):
    data = request.dict()

    # ❌ only remove API-only fields
    data.pop("feedback_text", None)

    return predict_churn(data)