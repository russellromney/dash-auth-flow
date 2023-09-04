from logzero import logger
import traceback
from sqlmodel import select
import random
from mailjet_rest import Client
from datetime import datetime, timedelta

from models.password_change import PasswordChange
from models.user import User
from utils.config import get_session, config
from utils.user import change_password


def send_password_key(email, firstname):
    """
    ensure email exists
    create random 6-number password key
    send email with Twilio Sendgrid containing that password key
    return True if that all worked
    return False if one step fails
    """

    # make sure email exists
    user = User.from_email(email)
    if not user:
        return False

    # generate a random key and send it to the user's email
    key = "".join([random.choice("1234567890") for x in range(6)])
    try:
        mailjet = Client(
            auth=(config.get("MAILJET_API_KEY"), config.get("MAILJET_API_SECRET")),
            version="v3.1",
        )
        data = {
            "Messages": [
                {
                    "From": {
                        "Email": config.get("FROM_EMAIL"),
                        "Name": config["APP_NAME"],
                    },
                    "To": [
                        {
                            "Email": email,
                            "Name": user.first,
                        }
                    ],
                    "Subject": "Greetings from Dash-Auth-Flow.",
                    "TextPart": f"{config['APP_NAME']} password reset code",
                    "HTMLPart": f"<p>Dear {user.first},<p> <p>Your {config['APP_NAME']} password reset code is: <strong>{key}</strong>",
                    "CustomID": "AppGettingStartedTest",
                }
            ]
        }
        result = mailjet.send.create(data=data)
        if result.status_code != 200:
            logger.info(f"Mailjet returned a non-200 status: {result.status_code}")
            logger.info(result.json())
            return False
    except Exception as e:
        traceback.print_exc(e)
        return False

    # store that key in the password_key table
    with get_session() as session:
        change = PasswordChange(email=email, password_key=key, timestamp=datetime.now())
        session.add(change)
        session.commit()
        session.refresh(change)

    # change their current password to a random string
    # first, get first and last name
    random_password = "".join([random.choice("1234567890") for x in range(15)])
    res = change_password(email, random_password)
    if res:
        return True
    return False


def validate_password_key(email: str, key: str) -> bool:
    # email exists
    if not User.from_email(email):
        return False

    # there is entry matching key and email
    with get_session() as session:
        out = session.exec(
            select(PasswordChange)
            .where(PasswordChange.email == email)
            .where(PasswordChange.password_key == key)
        ).all()
    if out:
        if (out[0].timestamp - (datetime.now() - timedelta(1))).days < 1:
            return True
    return False
