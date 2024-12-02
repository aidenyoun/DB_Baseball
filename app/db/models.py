from sqlalchemy import Column, Integer, String, Text, Enum, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    join_date = Column(Date, server_default=func.current_date())

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class Board(Base):
    __tablename__ = "Board"
    board_id = Column(Integer, primary_key=True, index=True)
    league = Column(String(50), nullable=False)
    team = Column(String(50))
    description = Column(Text)

    posts = relationship("Post", back_populates="board")

class Post(Base):
    __tablename__ = "Post"
    post_id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, ForeignKey("Board.board_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default="CURRENT_TIMESTAMP")
    updated_at = Column(DateTime, default="CURRENT_TIMESTAMP")

    board = relationship("Board", back_populates="posts")
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "Comment"
    comment_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("Post.post_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default="CURRENT_TIMESTAMP")

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")

class Vote(Base):
    __tablename__ = "Vote"
    vote_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    post_id = Column(Integer, ForeignKey("Post.post_id"), nullable=True)
    comment_id = Column(Integer, ForeignKey("Comment.comment_id"), nullable=True)
    vote_type = Column(Enum("upvote", "downvote"), nullable=False)
    created_at = Column(DateTime, default="CURRENT_TIMESTAMP")

class GameResult(Base):
    __tablename__ = "GameResult"
    game_id = Column(Integer, primary_key=True, index=True)
    league = Column(String(50), nullable=False)
    home_team = Column(String(50), nullable=False)
    away_team = Column(String(50), nullable=False)
    home_score = Column(Integer, nullable=False)
    away_score = Column(Integer, nullable=False)
    game_date = Column(Date, nullable=False)
