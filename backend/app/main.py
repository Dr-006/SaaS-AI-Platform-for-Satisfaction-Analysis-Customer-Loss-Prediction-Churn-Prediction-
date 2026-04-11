
# backend/app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import churn, feedback, dashboard, auth



#  LIFESPAN 
@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.services import sentiment_service, churn_service

    services = [
        ("sentiment", sentiment_service),
        ("churn", churn_service),
    ]

    for name, service in services:
        try:
            service.load_models()
            print(f"✅ {name} model loaded")
        except Exception as e:
            print(f"❌ {name} failed: {e}")

    yield  # 👉 app running here

    print("🛑 Shutting down...")


# APP INIT

app = FastAPI(
    title="AI SaaS Platform API",
    lifespan=lifespan
)



# ROUTES

app.include_router(churn.router)
app.include_router(feedback.router)
app.include_router(dashboard.router)
app.include_router(auth.router)



# HEALTH CHECK

@app.get("/")
def home():
    return {
        "message": "AI SaaS Platform is running 🚀",
        "status": "healthy"
    }