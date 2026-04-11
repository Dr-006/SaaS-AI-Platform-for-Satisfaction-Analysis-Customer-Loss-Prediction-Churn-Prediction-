# # backend/app/services/churn_service.py

import joblib
import pandas as pd
from pathlib import Path
from app.ml.churn import inference as churn_inf


# PATHS
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "models" / "churn_model.pkl"
FEATURES_PATH = BASE_DIR / "ml" / "models" / "churn_features.pkl"


# CACHE

model = None
features = None


#  LOAD MODELS
def load_models():
    global model, features

    if model is None or features is None:
        model = joblib.load(MODEL_PATH)
        features = joblib.load(FEATURES_PATH)



# CLEAN TYPES (IMPORTANT FIX XGBOOST / SKLEARN)

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # conversion numérique SAFE
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    if "MonthlyCharges" in df.columns:
        df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce")

    if "tenure" in df.columns:
        df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce")

    # inutile pour le modèle
    df.drop(columns=["customerID"], inplace=True, errors="ignore")

    return df



#  PREPROCESS
def preprocess(df: pd.DataFrame, features) -> pd.DataFrame:
    df = df.copy()

    # 1. clean types
    df = clean(df)

    # 2. remove AI features (PAS dans training)
    ai_cols = [
        "sentiment_score",
        "sentiment_binary",
        "sentiment_intensity",
        "tenure_sentiment",
        "feedback_text"
    ]
    df.drop(columns=ai_cols, inplace=True, errors="ignore")

    # 3. encoding (same training behavior)
    df = pd.get_dummies(df)

    # 4. alignement STRICT avec features training
    df = df.reindex(columns=features, fill_value=0)

    return df


# PREDICTION

def predict_churn(input_data: dict):

    load_models()

    df = pd.DataFrame([input_data])

    df = clean(df)

    X = preprocess(df, features)

    proba = model.predict_proba(X)

    return {
        "prediction": int(proba[0][1] > 0.4),
        "probability": float(proba[0][1])
    }


# STATUS
def is_loaded():
    return model is not None and features is not None









