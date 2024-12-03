from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.db.models import User
from app.db.schemas import UserCreate, UserLogin
from app.session import create_session, clear_session

from passlib.hash import bcrypt

templates = Jinja2Templates(directory="app/templates/users")
router = APIRouter()

@router.get("/signup", response_class="HTMLResponse")
async def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/login", response_class="HTMLResponse")
async def signup_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# @router.post("/login")
#     create_session(response, user.user_id)


@router.post("/login")
def login_user(login_data: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    if not bcrypt.verify(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid Password")

    create_session(response, user.user_id)

    return {"message": "Login successful", "username": user.username}


@router.get("/logout")
def logout_user(response: Response, request: Request):
    clear_session(response)
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/mypage", response_class="HTMLResponse")
async def signup_form(request: Request):
    return templates.TemplateResponse("mypage.html", {"request": request})
