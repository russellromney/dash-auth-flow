import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, no_update, register_page, callback
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash

from models.user import User
from utilities.auth import redirect_authenticated, unprotected

register_page(__name__, path="/login")

@unprotected
@redirect_authenticated
def layout():
    return dbc.Row(
        dbc.Col(
            [
                html.Div(id="login-url"),
                dbc.Row(
                    dbc.Col(
                        [
                            dbc.Alert(
                                "Try test@test.com / test",
                                color="info",
                                dismissable=True,
                            ),
                            html.Br(),
                            dbc.Input(id="login-email", autoFocus=True),
                            dbc.FormText("Email"),
                            html.Br(),
                            dbc.Input(
                                id="login-password", type="password", debounce=True
                            ),
                            dbc.FormText("Password"),
                            html.Br(),
                            dbc.Button(
                                "Submit", color="primary", id="login-button", n_clicks=0
                            ),
                            # dbc.FormText(id='output-state')
                            html.Br(),
                            html.Br(),
                            dcc.Link("Register", href="/register"),
                            html.Br(),
                            dcc.Link("Forgot Password", href="/forgot"),
                        ]
                    )
                ),
            ],
            width=6,
        )
    )


@callback(
    Output("login-url", "children"),
    Input("login-button", "n_clicks"),
    Input("login-password", "value"),
    State("login-email", "value"),
)
def login_success(n_clicks, password, email):
    """
    logs in the user
    """
    if password is not None or n_clicks > 0:
        user = User.from_email(email)
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return dcc.Location(id="redirect-login-to-home", pathname="/home")
        return no_update
    else:
        return no_update
