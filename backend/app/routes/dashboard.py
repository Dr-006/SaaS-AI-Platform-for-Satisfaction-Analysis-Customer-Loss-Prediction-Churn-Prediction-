# backend/app/routes/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas import DashboardStats
from app.models import Prediction, Feedback
from app.database import SessionLocal

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import pandas as pd
from pathlib import Path
from app.services import churn_service

@router.get("/stats", response_model=DashboardStats)
def get_stats(db: Session = Depends(get_db)):
    # ─── Live DB KPIs ───
    total = db.query(Prediction).count()
    churn_count = db.query(Prediction).filter(Prediction.prediction == 1).count()
    no_churn_count = total - churn_count
    churn_rate = round(churn_count / total, 4) if total > 0 else 0.0

    total_feedbacks = db.query(Feedback).count()
    avg_sentiment_result = db.query(func.avg(Feedback.sentiment_score)).scalar()
    avg_sentiment = round(float(avg_sentiment_result), 4) if avg_sentiment_result is not None else 0.5
    
    # Calcul du score de satisfaction client (0-100)
    # Conversion du sentiment score (-1 à 1) en pourcentage (0-100)
    customer_satisfaction_score = round((avg_sentiment + 1) * 50, 1)
    
    # Détermination du niveau de satisfaction
    if customer_satisfaction_score >= 70:
        satisfaction_level = "Élevé"
    elif customer_satisfaction_score >= 50:
        satisfaction_level = "Moyen"
    else:
        satisfaction_level = "Faible"

    # Risk Distribution from LIVE DB
    high_count = db.query(Prediction).filter(Prediction.probability >= 0.65).count()
    med_count = db.query(Prediction).filter((Prediction.probability >= 0.35) & (Prediction.probability < 0.65)).count()
    low_count = db.query(Prediction).filter(Prediction.probability < 0.35).count()
    
    risk_distribution = []
    if total > 0:
        risk_distribution = [
            {"name": "HIGH", "value": round((high_count/total)*100, 1)},
            {"name": "MEDIUM", "value": round((med_count/total)*100, 1)},
            {"name": "LOW", "value": round((low_count/total)*100, 1)}
        ]

    # ─── ML Feature Importances ───
    feature_importance = []
    churn_service.load_models()
    if churn_service.model is not None and hasattr(churn_service.model, "feature_importances_"):
        imps = churn_service.model.feature_importances_
        feats = churn_service.features
        # Zip, sort, top 5
        feat_imp = sorted(zip(feats, imps), key=lambda x: x[1], reverse=True)[:5]
        feature_importance = [{"name": str(f), "value": round(float(i), 3)} for f, i in feat_imp]

    # ─── Dataset Distributions (Insights) ───
    contract_data = []
    tenure_data = []
    try:
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        csv_path = base_dir / "data" / "processed" / "churn_with_sentiment.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            # Filter to churned clients to see their distribution
            churn_df = df[df["Churn"] == "Yes"] if "Churn" in df.columns else df
            
            if "Contract" in churn_df.columns:
                c_counts = churn_df["Contract"].value_counts(normalize=True) * 100
                contract_data = [{"name": str(k), "value": round(float(v), 1)} for k, v in c_counts.items()]
            
            if "tenure" in churn_df.columns:
                bins = [-1, 12, 24, 36, 48, 60, 100]
                labels = ["0-12", "13-24", "25-36", "37-48", "49-60", "60+"]
                churn_df["t_group"] = pd.cut(churn_df["tenure"], bins=bins, labels=labels)
                t_counts = churn_df["t_group"].value_counts(normalize=True) * 100
                tenure_data = [{"name": f"{k} mois", "value": round(float(v), 1)} for k, v in t_counts.items() if v > 0]
    except Exception as e:
        print(f"Error reading dataset: {e}")

    return DashboardStats(
        total_predictions=total,
        churn_count=churn_count,
        no_churn_count=no_churn_count,
        churn_rate=churn_rate,
        total_feedbacks=total_feedbacks,
        avg_sentiment=avg_sentiment,
        customer_satisfaction_score=customer_satisfaction_score,
        satisfaction_level=satisfaction_level,
        
        global_churn_rate=churn_rate,
        total_analyzed=total,
        high_risk_count=high_count,
        medium_risk_count=med_count,
        low_risk_count=low_count,
        churn_by_contract=contract_data,
        churn_by_tenure=tenure_data,
        feature_importance=feature_importance,
        risk_distribution=risk_distribution
    )