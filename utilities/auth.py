from typing import Callable
from dash import dcc, page_registry
from flask import current_app
from flask_login import current_user
from logzero import logger
import traceback
from sqlmodel import select
import random
from mailjet_rest import Client
from datetime import datetime, timedelta

from models.password_change import PasswordChange
from models.user import User
from utilities.config import get_session, config
from utilities.user import change_password


def unprotected(f: Callable) -> Callable:
    """Used in conjunction with Dash Pages and `protect_layouts`.
    Decorates a Dash page layout function and explicitly
    allows any user to access the layout function output.

    @unprotected
    def layout():
        return html.Div(...)
    """
    f.is_protected = False
    return f


def protected(f: Callable) -> Callable:
    """Used in conjunction with Dash Pages and `protect_layouts`.
    Decorates a Dash page layout function and explicitly
    requires a user to be authenticated to access the layout function output.

    NOTE: Must be the first/outermost decorator.

    @protected
    @other_decorator
    def layout():
        return html.Div(...)
    """
    f.is_protected = True
    return f


def _protect_layout(f: Callable) -> Callable:
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            return dcc.Location(
                id="redirect-unauthenticated-user-to-login",
                pathname=current_app.login_manager.login_view,
            )
        return f(*args, **kwargs)

    return wrapped


def redirect_authenticated(pathname: str) -> Callable:
    """
    If the user is authenticated, redirect them to the provided page pathname.
    """

    def wrapper(f: Callable):
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated:
                return dcc.Location(
                    id="redirect-authenticated-user-to-path",
                    pathname=pathname,
                )
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def protect_layouts(default: bool = True):
    """
    Call this after defining the global dash.Dash object.
    Protect any explicitly protected views and *don't* protect any  explicitly unprotected views.
    Otherwise, protect all or none according to the `default`.
    """
    for page in page_registry.values():
        if hasattr(page["layout"], "is_protected"):
            if bool(getattr(page["layout"], "is_protected")) == False:
                continue
            else:
                page["layout"] = _protect_layout(page["layout"])
        elif default == True:
            page["layout"] = _protect_layout(page["layout"])


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
                    "From": {"Email": config.get("FROM_EMAIL"), "Name": "My App"},
                    "To": [
                        {
                            "Email": email,
                            "Name": user.first,
                        }
                    ],
                    "Subject": "Greetings from Dash-Auth-Flow.",
                    "TextPart": "My App password reset code",
                    "HTMLPart": f"<p>Dear {user.first},<p> <p>Your My App password reset code is: <strong>{key}</strong>",
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
