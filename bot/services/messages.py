from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert

from bot.database import AsyncSessionLocal
from bot.models import MessageModel, UserModel
from bot.schemas import CreateMessage, Message, User, CreateUser


async def add_user(user: CreateUser):
    async with AsyncSessionLocal() as session:
        query = (
            insert(UserModel)
            .values(user.model_dump())
            .on_conflict_do_update(
                index_elements=[UserModel.user_id],
                set_={'session_id': user.session_id}
            )
            .returning(UserModel)
        )
        result = await session.execute(query)
        user = User.model_validate(result.scalar_one())
        await session.commit()
        return user


async def save_message(message: CreateMessage):
    async with AsyncSessionLocal() as session:
        query = insert(MessageModel).values(message.model_dump()).returning(MessageModel)
        result = await session.execute(query)
        message = Message.model_validate(result.scalar_one())
        await session.commit()
        return message


async def get_user(user_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.user_id == user_id)
        )
        obj = result.scalar_one_or_none()
        return User.model_validate(obj) if obj else None


async def get_history(session_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(MessageModel)
            .where(MessageModel.session_id == session_id)
            .order_by(MessageModel.created_at)
        )
        messages = result.scalars().all()
        return [Message.model_validate(msg) for msg in messages]


async def clear_history(user_id: int):
    async with AsyncSessionLocal() as session:
        await session.execute(
            delete(MessageModel).where(MessageModel.user_id == user_id)
        )
        await session.commit()
