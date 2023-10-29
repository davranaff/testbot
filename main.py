import asyncio

from app.telegram.bot import bot

asyncio.run(bot.polling())
