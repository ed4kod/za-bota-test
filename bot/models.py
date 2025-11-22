from sqlalchemy import Column, Integer, String, func, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MessageModel(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, index=True, primary_key=True)
    session_id = Column(String, index=True)
    user_id = Column(Integer, index=True)
    role = Column(String)
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserModel(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, index=True, primary_key=True)
    session_id = Column(String, index=True)
