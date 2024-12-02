import uvicorn
from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api.routes import users,community,standings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

router = APIRouter()
app.include_router(community.router, prefix="/community", tags=["Community"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(standings.router, tags=["standings"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/", response_class="HTMLResponse")
async def root(request: Request):
    return templates.TemplateResponse("intro.html", {"request": request})
