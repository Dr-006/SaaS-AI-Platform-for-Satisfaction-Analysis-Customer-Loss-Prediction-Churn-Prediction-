
# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import churn, feedback, dashboard, auth, clients
from app.database import Base, engine



#  LIFESPAN 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

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
    title="ChurnGuard API",
    description="ML-powered churn prediction & sentiment analysis platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173","http://localhost:3030"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ROUTES

app.include_router(auth.router)
app.include_router(churn.router)
app.include_router(feedback.router)
app.include_router(dashboard.router)
app.include_router(clients.router)



# HEALTH CHECK

@app.get("/")
def home():
    return {
        "message": "AI SaaS Platform is running 🚀",
        "status": "healthy"
    }