from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

# User 스키마
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    user_id: int
    username: str
    email: str
    join_date: date

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Post 스키마
class PostCreate(BaseModel):
    board_id: int
    title: str
    content: str

class PostOut(BaseModel):
    post_id: int
    board_id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Comment 스키마
class CommentCreate(BaseModel):
    post_id: int
    content: str

class CommentOut(BaseModel):
    comment_id: int
    post_id: int
    user_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

# Vote 스키마
class VoteCreate(BaseModel):
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    vote_type: str

class VoteOut(BaseModel):
    vote_id: int
    user_id: int
    post_id: Optional[int]
    comment_id: Optional[int]
    vote_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class StandingsBase(BaseModel):
    league: str
    team_name: str
    games_played: int
    wins: int
    losses: int
    ties: Optional[int] = 0
    win_rate: float
    rank: int
    division: str

class StandingsInDB(StandingsBase):
    id: int
    last_updated: Optional[str]

    class Config:
        orm_mode = True