from dash import register_page, dcc
from flask_login import current_user, logout_user

from utils.auth import protected

register_page(__name__, path="/logout")


@protected
def layout():
    if current_user.is_authenticated:
        logout_user()
    return dcc.Location(id="redirect-logout-to-login", pathname="/login")
