import uvicorn
import os
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api.routes import base, users, posts
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# app.include_router(base.router, tags=["Base"])
app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(posts.router, prefix="/posts", tags=["Posts"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요한 도메인을 명시하거나 "*"로 모두 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)