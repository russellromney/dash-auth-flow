from logzero import logger
import time
from dash import register_page, dcc, html, Input, Output, no_update, callback
from flask_login import current_user, logout_user

from utils.auth import protected
from utils.config import config

register_page(__name__, path="/logout")


@protected
def layout():
    if current_user.is_authenticated:
        logout_user()
    return dcc.Location(id="redirect-logout-to-login", pathname="/login")
