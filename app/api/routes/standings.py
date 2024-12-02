from fastapi import APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.db.models import Standings

templates = Jinja2Templates(directory="app/templates/standings")
router = APIRouter()

# KBO
@router.get("/standings/kbo", response_class="HTMLResponse")
async def standings_kbo(request: Request, db: Session = Depends(get_db)):
    standings = db.query(Standings).filter(Standings.league == "KBO").order_by(Standings.ranking).all()
    return templates.TemplateResponse("standings_kbo.html", {"request": request, "standings": standings, "league": "KBO"})

# MLB
@router.get("/standings/mlb", response_class="HTMLResponse")
async def standings_mlb(request: Request, db: Session = Depends(get_db)):
    standings = db.query(Standings).filter(Standings.league == "MLB").order_by(Standings.division, Standings.ranking).all()
    if not standings:
        print("No standings data found")

    divisions = {}
    for team in standings:
        if team.division not in divisions:
            divisions[team.division] = []
        divisions[team.division].append(team)

    return templates.TemplateResponse("standings_mlb.html", {"request": request, "divisions": divisions, "league": "MLB"})

# NPB
@router.get("/standings/npb", response_class="HTMLResponse")
async def standings_npb(request: Request, db: Session = Depends(get_db)):
    standings = db.query(Standings).filter(Standings.league == "NPB").order_by(Standings.division, Standings.ranking).all()
    if not standings:
        print("No standings data found")

    divisions = {}
    for team in standings:
        if team.division not in divisions:
            divisions[team.division] = []
        divisions[team.division].append(team)

    return templates.TemplateResponse("standings_npb.html", {"request": request, "divisions": divisions, "league": "NPB"})
