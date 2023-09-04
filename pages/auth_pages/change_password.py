import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, no_update, callback, register_page
from flask_login import current_user

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
)


@unprotected
@redirect_authenticated("/home")
def layout():
    return dbc.Row(
        dbc.Col(
            [
                html.H3("Change Password"),
                dbc.Row(
                    dbc.Col(
                        [
                            html.Div(id="change-alert"),
                            html.Div(id="change-redirect"),
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
            width=6,
        )
    )


# function to validate inputs
@callback(
    Output("change-password", "valid"),
    Output("change-password", "invalid"),
    Output("change-confirm", "valid"),
    Output("change-confirm", "invalid"),
    Output("change-button", "disabled"),
    Input("change-password", "value"),
    Input("change-confirm", "value"),
    prevent_initial_call=True,
)
def change_validate_inputs(password, confirm):
    password_valid = False
    password_invalid = False
    confirm_valid = False
    confirm_invalid = True
    disabled = True

    bad = [None, ""]

    if password in bad:
        pass
    elif isinstance(password, str):
        password_valid = True
        password_invalid = False

    if confirm in bad:
        pass
    elif confirm == password:
        confirm_valid = True
        confirm_invalid = False

    if password_valid and confirm_valid:
        disabled = False

    return (password_valid, password_invalid, confirm_valid, confirm_invalid, disabled)


@callback(
    Output("change-alert", "children"),
    Output("change-redirect", "pathname"),
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
            return success_alert, dcc.Location(id="redirect-change-to-forgot")
        else:
            pass
    else:
        pass
    return failure_alert, no_update
