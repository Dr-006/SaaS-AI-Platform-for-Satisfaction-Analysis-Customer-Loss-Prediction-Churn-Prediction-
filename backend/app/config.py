# # a faire

# DATABASE_URL = "postgresql://admin:password@localhost:5432/ai_saas"


# backend/app/config.py
import os

BASE_DIR = os.path.dirname(__file__)  
# 👉 maintenant BASE_DIR = backend/app

MODEL_PATH = os.path.join(BASE_DIR, "ml", "models")

SENTIMENT_MODEL_PATH = os.path.join(MODEL_PATH, "sentiment_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_PATH, "vectorizer.pkl")

CHURN_MODEL_PATH = os.path.join(MODEL_PATH, "churn_model.pkl")
CHURN_FEATURES_PATH = os.path.join(MODEL_PATH, "churn_features.pkl")