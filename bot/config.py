from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    token: str

    class Config:
        env_prefix = 'BOT_'


class DBConfig(BaseSettings):
    host: str = 'localhost'
    port: int = 5432
    database: str = 'bot_db'
    username: str = 'postgres'
    password: str = 'postgres'
    echo: bool = True
    driver: str = 'postgresql+asyncpg'

    class Config:
        env_prefix = 'DB_'


class AIConfig(BaseSettings):
    api_key: str
    base_url: str | None = None

    class Config:
        env_prefix = 'AI_'


db_config = DBConfig()
bot_config = BotConfig()
ai_config = AIConfig()
