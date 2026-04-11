# # backend/app/services/sentiment_service.py



import joblib
from app.config import SENTIMENT_MODEL_PATH, VECTORIZER_PATH
from app.ml.sentiment import preprocessing, inference

vectorizer = None
model = None


def load_models():
    global vectorizer, model
    if vectorizer is None or model is None:
        vectorizer = joblib.load(VECTORIZER_PATH)
        model = joblib.load(SENTIMENT_MODEL_PATH)


def get_sentiment_score(text: str) -> float:
    load_models()

    clean = preprocessing.preprocess(text)
    vect = vectorizer.transform([clean])
    prediction = inference.predict(model, vect)

    label = prediction[0]

    mapping = {
        "negative": 0.0,
        "neutral": 0.5,
        "positive": 1.0
    }

    return mapping.get(label, 0.5)