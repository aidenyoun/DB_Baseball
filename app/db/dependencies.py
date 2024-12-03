from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from fastapi import Request, HTTPException
from app.session import get_current_user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_login(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id