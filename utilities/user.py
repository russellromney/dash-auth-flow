from logzero import logger
from werkzeug.security import generate_password_hash
from sqlmodel import select

from models.user import User
from utilities.config import get_session


def add_user(first: str, last: str, password: str, email: str) -> bool:
    hashed_password = generate_password_hash(password, method="sha256")

    with get_session() as session:
        this = User(first=first, last=last, email=email, password=hashed_password)
        session.add(this)
        session.commit()
    return True


def show_users():
    with get_session() as session:
        out = session.exec(select(User)).all()
    for row in out:
        logger.info(row.dict())


def change_password(email: str, password: str) -> bool:
    """
    Change user password. Just changes the password;
    does NOT handle password change email functionality.
    """
    if not User.from_email(email):
        return False

    this = User.from_email(email)
    hashed_password = generate_password_hash(password, method="sha256")
    this.password = hashed_password
    with get_session() as session:
        session.add(this)
        session.commit()
    return True
