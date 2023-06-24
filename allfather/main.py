import asyncio

import uvicorn

from allfather.api.router import app as fastapi_app
from allfather.telegram.client import application as telegram_bot


def main():
    asyncio.run(start())


async def start():
    server = uvicorn.Server(
        uvicorn.Config(
            fastapi_app,
            host="0.0.0.0",
        )
    )
    async with telegram_bot:
        await telegram_bot.start()
        await telegram_bot.updater.start_polling()
        await server.serve()
        await telegram_bot.updater.stop()
        await telegram_bot.stop()


if __name__ == "__main__":
    main()
