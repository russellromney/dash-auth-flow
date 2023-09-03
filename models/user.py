from __future__ import annotations
from typing import Self, Union
from flask_login import UserMixin
from sqlmodel import SQLModel, Field, select
import sqlalchemy
import uuid

from utilities.config import get_session


class AuthUser(UserMixin):
    # this is for Flask-Login to work correctly
    # https://github.com/tiangolo/sqlmodel/issues/476
    # https://github.com/tiangolo/sqlmodel/pull/256#issuecomment-1112188647 (link from the first thread)
    __config__ = None


class User(SQLModel, AuthUser, table=True):
    __tablename__ = "dash_user"

    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    first: str
    last: str
    email: str
    password: str

    @classmethod
    def from_id(cls, id: str) -> Union[User, None]:
        with get_session() as session:
            return session.get(User, id)

    @classmethod
    def from_email(cls, email: str) -> Union[User, None]:
        with get_session() as session:
            try:
                return session.exec(select(User).where(User.email == email)).one()
            except sqlalchemy.exc.NoResultFound:
                return None
