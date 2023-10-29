import asyncio

from app.data.currency import get_currency
from app.db.engine import session
from app.db.querysets.querysets import UserQuerySet
from app.telegram.bot import bot


async def check_and_send_notification():
    users = UserQuerySet(session).get_users_with_notification()
    currency = get_currency()

    for user in users:
        await bot.send_message(user.chat_id, f"""
    1 {currency.get('base')} = {currency.get('rate')} {currency.get('convert')} 
    \n дата и время запроса: {currency.get('datetime')} CRON!!!""")


asyncio.run(check_and_send_notification())
