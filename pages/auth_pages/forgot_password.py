import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, no_update, callback, register_page
from flask_login import current_user
from models.user import User

from utilities.auth import redirect_authenticated, send_password_key, unprotected

register_page(__name__, path="/forgot")

success_alert = dbc.Alert(
    "Reset successful. Taking you to change password.",
    color="success",
)
failure_alert = dbc.Alert(
    "Reset unsuccessful. Are you sure that email was correct?",
    color="danger",
)


@unprotected
@redirect_authenticated("/home")
def layout():
    return dbc.Row(
        dbc.Col(
            [
                html.H3("Forgot Password"),
                html.Div(id="forgot-redirect"),
                dbc.Row(
                    dbc.Col(
                        [
                            html.Div(id="forgot-alert"),
                            html.Br(),
                            dbc.FormText("Email"),
                            dbc.Input(id="forgot-email", autoFocus=True),
                            html.Br(),
                            dbc.Button(
                                "Submit email to receive code",
                                id="forgot-button",
                                color="primary",
                            ),
                        ]
                    )
                ),
            ],
            width=6,
        )
    )


@callback(
    Output("forgot-alert", "children"),
    Output("forgot-redirect", "children"),
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
        return success_alert, dcc.Location(
            id="redirect-forgot-to-change", pathname="/change"
        )
    else:
        return failure_alert, no_update
