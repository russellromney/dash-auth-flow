import uuid
from logzero import logger
from flask import current_app
from sqlmodel import SQLModel, select
from models.user import User

from application import server
from utilities.config import get_session
from utilities.user import add_user, show_users


def main():
    """
    Create all the tables in the current SQLModel metadata. 

    Clear the tables. 
    Re-create the test values.
    """
    # engine is open to sqlite///users.db (or whatever is in the .env files)
    SQLModel.metadata.create_all(current_app.engine)

    # add a test user to the database
    users = [
        dict(
            first="test",
            last="test",
            email="test@test.com",
            password="test",
        )
    ]
    with get_session() as session:
        # delete existing users
        logger.info("DELETING USERS")
        existing = session.exec(select(User)).all()
        i = 0
        for x in existing:
            session.delete(x)
            i += 1
        session.commit()
        logger.info(f"DELETED {i} USERS")

        # add new users
        logger.info("ADDING USERS")
        i = 0
        for vals in users:
            add_user(**vals)
            i += 1
        session.commit()
        logger.info(f"ADDED {i} USERS")

    # show that the users exists
    logger.info("USERS ARE:")
    show_users()

    # confirm that user exists
    assert User.from_email(users[0]["email"])
    logger.info(f"DONE")


if __name__ == "__main__":
    with server.app_context():
        main()
