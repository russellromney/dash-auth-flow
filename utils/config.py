import sqlalchemy
from sqlmodel import Session, create_engine
from flask import current_app
from dotenv import dotenv_values

# Load a config dictionary from the dotenv file.
config = dotenv_values(".env")


def make_engine() -> sqlalchemy.engine.Engine:
    return create_engine(config["SQLALCHEMY_DATABASE_URI"])


def get_session() -> Session:
    return Session(current_app.engine)
