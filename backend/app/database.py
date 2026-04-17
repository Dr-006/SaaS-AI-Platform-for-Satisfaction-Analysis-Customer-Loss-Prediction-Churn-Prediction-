# backend/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Changez "churn_guard" en "DATABASE_URL" (convention standard)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Soufiane12%40@localhost:5432/ai_saas")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()