import asyncio
import logging
import sys
from os import getenv

import google.generativeai as genai
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

TOKEN = getenv("BOT_TOKEN")
genai.configure(api_key=getenv("GOOGLE_API_KEY"))

dp = Dispatcher()
gemini = genai.GenerativeModel("gemini-1.0-pro-latest")
messages: genai.types.ContentsType = []


async def bot_referred(message: Message) -> bool:
    if message.bot is None:
        return False
    bot = await message.bot.me()
    if (
        message.reply_to_message is not None
        and message.reply_to_message.from_user is not None
        and message.reply_to_message.from_user.username == bot.username
    ):
        return True
    if message.text is not None and f"@{bot.username}" in message.text:
        return True
    return False


@dp.message(bot_referred)
async def on_mention(message: Message) -> None:
    if message.from_user is None:
        return
    global messages
    parts = []
    if message.text is not None and len(message.text) > 0:
        parts.append(f"{message.from_user.full_name}: {message.text}")
    messages.append({"role": "user", "parts": parts})
    response = await gemini.generate_content_async(messages)
    messages.append({"role": "model", "parts": response.parts})
    await message.reply(response.text)


async def start_polling() -> None:
    if TOKEN is None:
        raise Exception("BOT_TOKEN is missing from environment")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    messages.extend(
        [
            {
                "role": "user",
                "parts": [
                    f"""
                    System Prompt: You are a telegram bot whose name is {await bot.get_my_name()}.
                    The messages you receive will be prefixed by the user's display name.
                    """
                ],
            },
            {
                "role": "model",
                "parts": ["Understood"],
            },
        ]
    )
    await dp.start_polling(bot)


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start_polling())


if __name__ == "__main__":
    main()
