from datetime import datetime

from sqlalchemy import ForeignKey, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

Base: DeclarativeBase = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: int = Column('id', Integer, primary_key=True)

    username: str = Column('username', String)
    first_name: str = Column('first_name', String, nullable=True)
    last_name: str = Column('last_name', String, nullable=True)
    active: bool = Column('active', Boolean, default=False)
    notification: bool = Column('notification', Boolean, default=False)
    join_date: datetime = Column('join_date', DateTime, default=datetime.now())
    chat_id: int = Column('chat_id', Integer)

    def __init__(self, username, chat_id, active=True, notification=False, first_name=None, last_name=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.chat_id = chat_id
        self.active = active
        self.notification = notification

    def __repr__(self):
        return f'id: {self.id}, username: {self.username}'


class History(Base):
    __tablename__ = 'histories'

    id: int = Column('id', Integer, primary_key=True)

    from_currency: str = Column('from_currency', String)
    amount_from: float = Column('amount_from', Float)
    to_currency: str = Column('to_currency', String)
    amount_to: float = Column('amount_to', Float)
    date: datetime = Column('datetime', DateTime, default=datetime.now())

    user_id: int = Column(Integer, ForeignKey('users.id'))

    def __init__(self, user_id, date, from_currency, amount_from, to_currency, amount_to):
        self.user_id = user_id
        self.from_currency = from_currency
        self.amount_from = amount_from
        self.to_currency = to_currency
        self.amount_to = amount_to
        self.date = date

    def __repr__(self):
        return f"id: {self.id}, user id: {self.user_id}"


class Bot(Base):
    __tablename__ = 'bots'

    id: int = Column('id', Integer, primary_key=True)

    name: str = Column('name', String)
    token: str = Column('token', String)
    active: bool = Column('active', Boolean, default=True)

    def __init__(self, name, token, active):
        self.name = name
        self.token = token
        self.active = active

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'
