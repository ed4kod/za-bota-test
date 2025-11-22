import uuid

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.schemas import CreateMessage, CreateUser
from bot.services.gpt import send_to_gpt
from bot.services.messages import save_message, get_history, get_user, add_user

router = Router()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Новый запрос', )]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


@router.message(Command('start'))
async def start(message: Message):
    await add_user(CreateUser(user_id=message.from_user.id, session_id=str(uuid.uuid4())))
    await message.answer(
        '👋 Привет-привет! Я твой персональный ChatGPT 🤖.\n\n'
        'Здесь пока пусто, но ты можешь написать что угодно, и я с тобой поболтаю.\n\n'
        'Если захочешь сбросить контекст или начать с чистого листа — жми кнопку «Новый запрос» ⬇️',
        reply_markup=main_kb
    )


@router.message(Command('help'))
async def start(message: Message):
    await add_user(CreateUser(user_id=message.from_user.id, session_id=str(uuid.uuid4())))
    await message.answer(
        'ℹ️ Я твой собеседник и помогаю обсуждать любые темы.\n\n'
        '💡 Чтобы сбросить текущий контекст и начать заново, используй кнопку «Новый запрос».\n'
        ' Просто напиши мне сообщение, и я отвечу!',
        reply_markup=main_kb
    )


@router.message(lambda message: message.text not in ['Новый запрос'])
async def handle_message(message: Message):
    user_id = message.from_user.id
    user_info = await get_user(user_id)
    await save_message(
        CreateMessage(session_id=user_info.session_id, user_id=user_id, content=message.text, role='user'))
    history_records = await get_history(session_id=user_info.session_id)
    reply = await send_to_gpt(history_records)
    await save_message(
        CreateMessage(session_id=user_info.session_id, user_id=user_id, content=message.text, role='assistant'))
    try:
        await message.reply(reply, parse_mode=ParseMode.MARKDOWN_V2)
    except TelegramBadRequest:
        await message.reply(reply)


@router.message(lambda m: m.text == 'Новый запрос')
async def handle_new_request(message: Message):
    await add_user(CreateUser(user_id=message.from_user.id, session_id=str(uuid.uuid4())))
    await message.answer(
        '🆕 Новый запрос активирован! Контекст очищен, можем начинать с чистого листа.\n\n'
        'Напиши что-нибудь, и я с радостью отвечу! 😎',
        reply_markup=main_kb
    )
