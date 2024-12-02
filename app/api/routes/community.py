from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload
from app.db.dependencies import get_db
from app.db.models import Board, Post
from app.db.schemas import PostCreate, PostUpdate, PostOut

templates = Jinja2Templates(directory="app/templates/community")
router = APIRouter()

# 전체 게시글 조회
@router.get("/", response_class=HTMLResponse)
def get_all_posts(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).options(joinedload(Post.author)).all()
    boards = db.query(Board).all()
    return templates.TemplateResponse(
        "community.html",
        {"request": request, "posts": posts, "boards": boards, "selected_board": "All"}
    )

# 특정 게시판의 게시글 목록 조회
@router.get("/{board_id}", response_class=HTMLResponse)
def get_posts_by_board(board_id: int, request: Request, db: Session = Depends(get_db)):
    posts = (
        db.query(Post)
        .options(joinedload(Post.author))
        .filter(Post.board_id == board_id)
        .all()
    )
    board = db.query(Board).filter(Board.board_id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found.")
    boards = db.query(Board).all()
    return templates.TemplateResponse(
        "community.html",
        {
            "request": request,
            "posts": posts,
            "boards": boards,
            "selected_board": board.league,
        }
    )

# 게시글 상세 조회
@router.get("/post/{post_id}", response_class=HTMLResponse)
def get_post_detail(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    return templates.TemplateResponse(
        "post_detail.html",
        {"request": request, "post": post}
    )