from telegram.ext import ApplicationBuilder, CommandHandler

from allfather.config import TELEGRAM_BOT_TOKEN
from allfather.telegram.handler import start

application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
