# backend/app/routes/auth.py
import os
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.schemas import LoginRequest, Token, UserInfo

router = APIRouter(prefix="/auth", tags=["auth"])

# ─── CONFIG ─────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "churnguard-secret-key-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8 hours

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Simple hardcoded users (extend with DB later)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "analyst": {"password": "analyst123", "role": "analyst"},
}


# ─── HELPERS ────────────────────────────────────────────────────────
def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInfo:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role", "analyst")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return UserInfo(username=username, role=role)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ─── ROUTES ─────────────────────────────────────────────────────────
@router.post("/login", response_model=Token)
def login(request: LoginRequest):
    user = USERS.get(request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token({"sub": request.username, "role": user["role"]})
    return Token(access_token=token)


@router.get("/me", response_model=UserInfo)
def get_me(current_user: UserInfo = Depends(get_current_user)):
    return current_user