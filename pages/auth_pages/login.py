import time
import uuid
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, no_update, register_page, callback
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash

from models.user import User
from utils.auth import redirect_authenticated, unprotected
from utils.config import config

register_page(__name__, path="/login")


@unprotected
@redirect_authenticated(config["HOME_PATH"])
def layout():
    return dbc.Row(
        dbc.Col(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            html.Div(id="login-alert"),
                            dbc.Alert(
                                "Try test@test.com / test",
                                color="info",
                                dismissable=True,
                            ),
                            html.Br(),
                            dbc.FormText("Email"),
                            dbc.Input(id="login-email", autoFocus=True),
                            html.Br(),
                            dbc.FormText("Password"),
                            dbc.Input(
                                id="login-password", type="password", debounce=True
                            ),
                            html.Br(),
                            dbc.Button(
                                "Submit", color="primary", id="login-button", n_clicks=0
                            ),
                            dcc.Loading(
                                [
                                    html.Div(
                                        id="login-trigger", style=dict(display="none")
                                    ),
                                    html.Div(id="login-redirect"),
                                ],
                                id=uuid.uuid4().hex,
                            ),
                            html.Br(),
                            html.Br(),
                            dcc.Link("Register", href="/register"),
                            html.Br(),
                            dcc.Link("Forgot Password", href="/forgot"),
                        ]
                    )
                ),
            ],
            className="auth-page",
        )
    )


success_alert = dbc.Alert("Logged in. Taking you to home.", color="success")
failure_alert = dbc.Alert(
    "Login failed. Check your email and password.",
    color="danger",
    dismissable=True,
    duration=3000,
)


@callback(
    Output("login-trigger", "children"),
    Output("login-alert", "children"),
    Input("login-button", "n_clicks"),
    Input("login-password", "value"),
    State("login-email", "value"),
    prevent_initial_call=True,
)
def login_success(n_clicks, password, email):
    if not n_clicks:
        return no_update
    if password is not None:
        user = User.from_email(email)
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return 1, success_alert
        return no_update, failure_alert
    return no_update


@callback(
    Output("login-redirect", "children"),
    Output("url", "pathname", allow_duplicate=True),
    Input("login-trigger", "children"),
    prevent_initial_call=True,
)
def login_redirect(trigger):
    if trigger:
        time.sleep(2)
        return "", config["HOME_PATH"]
    return no_update, no_update
