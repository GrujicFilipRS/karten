from sqlalchemy.orm import Session
from flask_login import login_user
from data.__all_models import User


def register_user(username: str, password: str, db_sess: Session) -> None:
    """
    Registers a new user
    """
    user = User(username=username)
    user.set_password(password)
    db_sess.add(user)
    db_sess.commit()
    login_user(user)
