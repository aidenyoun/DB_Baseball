from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.dependencies import get_db
from app.db.models import GameResult
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse



router = APIRouter()
templates = Jinja2Templates(directory="app/templates/game_result")

@router.get("/game_result/{league}", response_class=HTMLResponse)
async def game_results(
    request: Request,
    league: str,
    month: int = 3,  # 기본 값은 3월
    db: Session = Depends(get_db)
):
    # 해당 리그와 월에 해당하는 게임 결과를 가져옴
    results = db.query(GameResult).filter(
        GameResult.league == league,
        func.extract('month', GameResult.game_date) == month
    ).order_by(GameResult.game_date).all()

    # 결과를 날짜별로 그룹화
    grouped_results = {}
    for game in results:
        date_str = game.game_date.strftime('%Y년 %m월 %d일')
        if date_str not in grouped_results:
            grouped_results[date_str] = []
        grouped_results[date_str].append(game)

    return templates.TemplateResponse(
        "game_result_"+league+".html",
        {
            "request": request,
            "league": league,
            "grouped_results": grouped_results,
            "month": month
        }
    )

