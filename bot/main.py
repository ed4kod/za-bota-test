import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot import config
from bot.handlers.messages import router as message_router

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=config.bot_config.token)
    dp = Dispatcher()
    dp.include_router(message_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
