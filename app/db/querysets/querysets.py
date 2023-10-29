from sqlalchemy.orm import Session

from app.db.models import User, History


class BaseQueryset:

    def __init__(self, session: Session):
        self.session = session


class UserQuerySet(BaseQueryset):

    def __init__(self, session: Session):
        super().__init__(session)
        self._model = User
        self._query = self.session.query(User)

    def get(self, username: str) -> User:
        return self._query.filter(self._model.username == username).first()

    def create(self, **kwargs):
        if self.get(kwargs.get('username')):
            return False

        user = User(
            username=kwargs.get("username"),
            first_name=kwargs.get("first_name"),
            last_name=kwargs.get("last_name"),
            chat_id=kwargs.get("chat_id")
        )

        self.session.add(user)
        self.session.commit()
        return True

    def delete(self, **kwargs):
        user = self.get(kwargs.get('username'))
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def history(self, username: str) -> list[History]:
        user = self.get(username)
        if user:
            return self.session.query(History).filter(History.user_id == user.id)
        return False

    def create_history(self, **kwargs):
        history = History(
            user_id=self.get(kwargs.get('username')).id,
            from_currency=kwargs.get("from_currency"),
            amount_from=kwargs.get("amount_from"),
            to_currency=kwargs.get("to_currency"),
            amount_to=kwargs.get("amount_to"),
            date=kwargs.get("date")
        )

        self.session.add(history)
        self.session.commit()

        return True

    def create_notification(self, username):
        try:
            user = self.get(username)
            user.notification = True
            self.session.add(user)
            self.session.commit()
            return True
        except:
            return False

    def get_users_with_notification(self):
        return self._query.filter(User.notification == True)