from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from bot.config import db_config

Base = declarative_base()

database_url = URL.create(
    drivername='postgresql+asyncpg',
    username=db_config.username,
    password=db_config.password,
    host=db_config.host,
    database=db_config.database,
    port=db_config.port
)

engine = create_async_engine(database_url, echo=db_config.echo)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
)
