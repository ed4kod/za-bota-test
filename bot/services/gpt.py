import asyncio

from openai import OpenAI

from bot import config
from bot.const import system_prompt
from bot.schemas import Message

client = OpenAI(
    base_url=config.ai_config.base_url,
    api_key=config.ai_config.api_key,
)


async def send_to_gpt(history_messages: list[Message]) -> str:
    instructions = [{'role': 'system', 'content': system_prompt}]
    history = [{'role': message.role, 'content': message.content} for message in history_messages]
    loop = asyncio.get_running_loop()
    print('Отправка GPT...')

    response = await loop.run_in_executor(
        None,
        lambda: client.chat.completions.create(
            model='openai/gpt-oss-20b',
            messages=instructions + history
        )
    )

    print('Получен ответ от GPT...')
    return response.choices[0].message.content[:4096]
