import time
import uuid
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, no_update, callback, register_page
from models.user import User

from utils.auth import redirect_authenticated, unprotected
from utils.pw import send_password_key
from utils.config import config

register_page(__name__, path="/forgot")


@unprotected
@redirect_authenticated(config["HOME_PATH"])
def layout():
    return dbc.Row(
        dbc.Col(
            [
                html.H3("Forgot Password"),
                dbc.Row(
                    dbc.Col(
                        [
                            html.Div(id="forgot-alert"),
                            html.Br(),
                            dbc.FormText("Email"),
                            dbc.Input(id="forgot-email", autoFocus=True),
                            html.Br(),
                            dcc.Loading(
                                [
                                    html.Div(
                                        id="forgot-trigger", style=dict(display="none")
                                    ),
                                    html.Div(id="forgot-redirect"),
                                ],
                                id=uuid.uuid4().hex,
                            ),
                            dbc.Button(
                                "Submit email to receive code",
                                id="forgot-button",
                                color="primary",
                            ),
                        ]
                    )
                ),
            ],
            className="auth-page",
        )
    )


success_alert = dbc.Alert(
    "Reset successful. Taking you to change password.",
    color="success",
)
failure_alert = dbc.Alert(
    "Reset unsuccessful. Are you sure that email was correct?",
    color="danger",
    dismissable=True,
    duration=config["ALERT_DELAY"],
)


@callback(
    Output("forgot-alert", "children"),
    Output("forgot-trigger", "children"),
    Input("forgot-button", "n_clicks"),
    State("forgot-email", "value"),
    prevent_initial_call=True,
)
def forgot_submit(_, email):
    # get first name
    user = User.from_email(email)
    if not user:
        return failure_alert, no_update

    # if it does, send password reset and save info
    if send_password_key(email, user.first):
        return success_alert, 1
    else:
        return failure_alert, no_update


@callback(
    Output("url", "pathname", allow_duplicate=True),
    Output("forgot-redirect", "children"),
    Input("forgot-trigger", "children"),
    prevent_initial_call=True,
)
def forgot_redirect(trigger):
    if trigger:
        time.sleep(config["TRANSITION_DELAY"])
        return "/change", ""
    return no_update, no_update
