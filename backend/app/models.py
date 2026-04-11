# backend/app/models.py
from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    profession = Column(String)

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    sentiment_score = Column(Float)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True)
    probability = Column(Float)
    prediction = Column(Integer)