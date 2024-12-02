from fastapi import APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.db.models import User
from app.db.schemas import UserCreate, UserLogin
from passlib.hash import bcrypt

templates = Jinja2Templates(directory="app/templates/home")
router = APIRouter()

@router.get("/community", response_class="HTMLResponse")
async def signup_form(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
