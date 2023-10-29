from telebot import types
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from app.data.currency import get_currency
from app.db.engine import session
from app.db.querysets.querysets import UserQuerySet

bot = AsyncTeleBot('6560509226:AAHWUBH8QNvrtSkBhgD153nyFIdwWbG9buU')

_CONST_COMMANDS = {
    'subscribe': 'Подписаться',
}


@bot.message_handler(commands=['start'])
async def send_welcome(message: Message):
    markup = types.ReplyKeyboardMarkup()
    subscribe = types.InlineKeyboardButton(text=_CONST_COMMANDS.get('subscribe'), callback_data="subscribe")

    markup.add(subscribe)

    user = UserQuerySet(session).create(
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        chat_id=message.chat.id,
        active=True,
    )

    if not user:
        await bot.send_message(message.chat.id, "Упс! что-то пошло не так!")
        return

    await bot.send_message(message.chat.id, """
        Добро пожаловать!!!\n
        Чтобы узнать курс доллара к рублю,\n пишите команду */rate_usd*\n
        Чтобы просмотреть историю запроса,\n пишите команде */history*
        \n Подписаться на обновление курса валют (каждый час приходит)""", reply_markup=markup)


@bot.message_handler(commands=['rate_usd'])
async def send_rates(message: Message):
    currency = get_currency()

    UserQuerySet(session).create_history(
        username=message.from_user.username,
        from_currency=currency.get("base"),
        amount_from=1,
        to_currency=currency.get("convert"),
        amount_to=currency.get("rate"),
        date=currency.get("datetime")
    )

    await bot.send_message(message.chat.id, f"""
    1 {currency.get('base')} = {currency.get('rate')} {currency.get('convert')} 
    \n дата и время запроса: {currency.get('datetime')}""")


@bot.message_handler(commands=['history'])
async def history(message: Message):
    histories = UserQuerySet(session).history(message.from_user.username)
    text = """Ваша история запросов"""

    for i in histories:
        text += (f'\n---------------\n '
                 f'{i.amount_from} {i.from_currency} = {i.amount_to} {i.to_currency}\n'
                 f'Время запроса: {i.date.strftime("%d/%m/%Y, %H:%M:%S")}')

    await bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: True)
async def echo_message(message: types.Message):
    if message.text == _CONST_COMMANDS.get('subscribe'):
        a = types.ReplyKeyboardRemove()
        await bot.send_message(message.chat.id, "Вы подписались на наши обновление", reply_markup=a)

        UserQuerySet(session).create_notification(username=message.from_user.username)

        return
    await bot.reply_to(message, "Такой команды нету((")
