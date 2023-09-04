import time
import uuid
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, no_update, callback, register_page
from validate_email import validate_email

from utilities.auth import (
    redirect_authenticated,
    unprotected,
    validate_password_key,
    change_password,
)

register_page(__name__, path="/change")

success_alert = dbc.Alert(
    "Reset successful. Taking you to login!",
    color="success",
)
failure_alert = dbc.Alert(
    "Reset unsuccessful. Are you sure the email and code were correct?",
    color="danger",
    dismissable=True,
    duration=3000,
)


@unprotected
@redirect_authenticated("/")
def layout():
    return dbc.Row(
        dbc.Col(
            [
                html.H3("Change Password"),
                dbc.Row(
                    dbc.Col(
                        [
                            html.Div(id="change-alert"),
                            dcc.Loading(
                                [
                                    html.Div(
                                        id="change-trigger", style=dict(display="none")
                                    ),
                                    html.Div(id="change-redirect"),
                                ],
                                id=uuid.uuid4().hex,
                            ),
                            html.Br(),
                            dbc.FormText("Email"),
                            dbc.Input(id="change-email", autoFocus=True),
                            html.Br(),
                            dbc.FormText("Code"),
                            dbc.Input(id="change-key", type="password"),
                            html.Br(),
                            dbc.FormText("New password"),
                            dbc.Input(id="change-password", type="password"),
                            html.Br(),
                            dbc.FormText("Confirm new password"),
                            dbc.Input(id="change-confirm", type="password"),
                            html.Br(),
                            dbc.Button(
                                "Submit password change",
                                id="change-button",
                                color="primary",
                            ),
                        ]
                    )
                ),
            ],
            className="auth-page",
        )
    )


# function to validate inputs
@callback(
    Output("change-password", "valid"),
    Output("change-password", "invalid"),
    Output("change-confirm", "valid"),
    Output("change-confirm", "invalid"),
    Output("change-email", "valid"),
    Output("change-email", "invalid"),
    Output("change-button", "disabled"),
    Input("change-password", "value"),
    Input("change-confirm", "value"),
    Input("change-email", "value"),
    prevent_initial_call=True,
)
def change_validate_inputs(password, confirm, email):
    password_valid = False
    password_invalid = False
    confirm_valid = False
    confirm_invalid = True
    email_valid = False
    email_invalid = True
    disabled = True
    bad = [None, ""]
    if password not in bad and isinstance(password, str):
        password_valid, password_invalid = True, False
    if confirm not in bad and confirm == password:
        confirm_valid, confirm_invalid = True, False
    if email not in bad and validate_email(email):
        email_valid, email_invalid = True, False
    if password_valid and confirm_valid and email_valid:
        disabled = False
    return (
        password_valid,
        password_invalid,
        confirm_valid,
        confirm_invalid,
        email_valid,
        email_invalid,
        disabled,
    )


@callback(
    Output("change-alert", "children"),
    Output("change-trigger", "pathname"),
    Input("change-button", "n_clicks"),
    State("change-email", "value"),
    State("change-key", "value"),
    State("change-password", "value"),
    State("change-confirm", "value"),
    prevent_initial_call=True,
)
def submit_change(submit, email, key, password, confirm):
    # all inputs have been previously validated
    if validate_password_key(email, key):
        # if that returns true, update the user information
        if change_password(email, password):
            return success_alert, 1
    return failure_alert, no_update


@callback(
    Output("url", "pathname", allow_duplicate=True),
    Input("change-trigger", "children"),
    prevent_initial_call=True,
)
def change_redirect(trigger):
    if trigger:
        time.sleep(2)
        return "/forgot"
        return dcc.Location(id="redirect-change-to-forgot", pathname="/forgot")
    return no_update
