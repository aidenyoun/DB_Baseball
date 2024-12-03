from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, Request, Form, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload
from app.db.dependencies import get_db
from app.db.models import Board, Post
from app.db.dependencies import require_login
from app.session import get_current_user

from app.db.schemas import PostCreate, PostUpdate, PostOut

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

# 1. 게시글 작성 페이지 (Create) - Place this route before the dynamic route
@router.get("/create", response_class=HTMLResponse)
async def create_post_page(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_login)
):
    boards = db.query(Board).all()
    return templates.TemplateResponse("/community/community_create.html", {"request": request, "boards": boards})

# 2. 게시글 작성 처리 (POST)
@router.post("/create", response_class=HTMLResponse)
async def create_post(
    request: Request,
    response: Response,
    board_id: int = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    user_id = get_current_user(request)
    if not user_id:
        # Redirect to login page if user is not authenticated
        return templates.TemplateResponse("/users/login.html", {"request": request})

    new_post = Post(board_id=board_id, title=title, content=content, user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return templates.TemplateResponse("/community/post_detail.html", {"request": request, "post": new_post})

# 3. 전체 게시글 조회
@router.get("/", response_class=HTMLResponse)
def get_all_posts(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).options(joinedload(Post.author), joinedload(Post.board)).all()
    boards = db.query(Board).all()
    return templates.TemplateResponse(
        "community/community.html",
        {"request": request, "posts": posts, "boards": boards, "selected_board": "All"}
    )

# 4. 게시글 상세 조회
@router.get("/post/{post_id}", response_class=HTMLResponse)
def get_post_detail(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(Post).options(joinedload(Post.author), joinedload(Post.board)).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    return templates.TemplateResponse(
        "/community/post_detail.html",
        {"request": request, "post": post}
    )

# 5. 특정 게시판의 게시글 목록 조회
@router.get("/{board_id}", response_class=HTMLResponse)
def get_posts_by_board(board_id: int, request: Request, db: Session = Depends(get_db)):
    posts = (
        db.query(Post)
        .options(joinedload(Post.author), joinedload(Post.board))
        .filter(Post.board_id == board_id)
        .all()
    )
    board = db.query(Board).filter(Board.board_id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found.")
    boards = db.query(Board).all()
    return templates.TemplateResponse(
        "/community/community.html",
        {
            "request": request,
            "posts": posts,
            "boards": boards,
            "selected_board": board.league,
        }
    )
