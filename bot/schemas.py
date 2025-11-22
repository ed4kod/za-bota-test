from datetime import datetime

from pydantic import BaseModel


class Base(BaseModel):
    class Config:
        from_attributes = True


class Message(Base):
    user_id: int
    content: str
    created_at: datetime
    role: str


class User(Base):
    user_id: int
    session_id: str


class CreateUser(User):
    user_id: int
    session_id: str


class CreateMessage(Base):
    session_id: str
    user_id: int
    content: str
    role: str
