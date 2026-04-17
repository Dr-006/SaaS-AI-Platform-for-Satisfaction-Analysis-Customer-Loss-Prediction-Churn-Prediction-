# backend/app/schemas.py
from pydantic import BaseModel
from typing import Optional, List


# ─── CHURN ───────────────────────────────────────────────
class ChurnRequest(BaseModel):
    gender: Optional[str] = None
    SeniorCitizen: Optional[int] = None
    Partner: Optional[str] = None
    Dependents: Optional[str] = None
    tenure: Optional[int] = None
    PhoneService: Optional[str] = None
    MultipleLines: Optional[str] = None
    InternetService: Optional[str] = None
    OnlineSecurity: Optional[str] = None
    OnlineBackup: Optional[str] = None
    DeviceProtection: Optional[str] = None
    TechSupport: Optional[str] = None
    StreamingTV: Optional[str] = None
    StreamingMovies: Optional[str] = None
    Contract: Optional[str] = None
    PaperlessBilling: Optional[str] = None
    PaymentMethod: Optional[str] = None
    MonthlyCharges: Optional[float] = None
    TotalCharges: Optional[str] = None
    feedback_text: Optional[str] = None


class ChurnResponse(BaseModel):
    prediction: int
    probability: float
    risk_level: str  # "low" | "medium" | "high"


# ─── FEEDBACK ────────────────────────────────────────────
class FeedbackRequest(BaseModel):
    text: str
    customer_id: Optional[int] = None


class FeedbackResponse(BaseModel):
    id: int
    text: str
    sentiment_score: float
    sentiment_label: str  # "negative" | "neutral" | "positive"


# ─── AUTH ────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInfo(BaseModel):
    username: str
    role: str


# ─── DASHBOARD ───────────────────────────────────────────
class ChartItem(BaseModel):
    name: str
    value: float

class DashboardStats(BaseModel):
    total_predictions: int
    churn_count: int
    no_churn_count: int
    churn_rate: float
    total_feedbacks: int
    avg_sentiment: float
    customer_satisfaction_score: float  # Score de satisfaction (0-100)
    satisfaction_level: str  # "Faible" | "Moyen" | "Élevé"
    global_churn_rate: float
    total_analyzed: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    churn_by_contract: List[ChartItem]
    churn_by_tenure: List[ChartItem]
    feature_importance: List[ChartItem]
    risk_distribution: List[ChartItem]


# ─── CLIENT ──────────────────────────────────────────────
class ClientCreate(BaseModel):
    name: str
    email: Optional[str] = None
    tenure: Optional[int] = None
    monthly_charges: Optional[float] = None


class ClientOut(BaseModel):
    id: int
    name: str
    email: Optional[str]
    tenure: Optional[int]
    monthly_charges: Optional[float]
    churn_probability: Optional[float]
    churn_prediction: Optional[int]

    class Config:
        from_attributes = True