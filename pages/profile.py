import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, no_update, register_page, callback
from flask_login import current_user

from utilities.auth import change_password
from utilities.config import get_session
from models.user import User

register_page(__name__, path="/profile")

success_alert = dbc.Alert(
    "Changes saved successfully.",
    color="success",
)
failure_alert = dbc.Alert(
    "Unable to save changes.",
    color="danger",
)


def layout():
    return dbc.Row(
        dbc.Col(
            [
                html.Div(1, id="profile-trigger", style=dict(display="none")),
                html.H3("Profile", id="profile-title"),
                html.Div(id="profile-alert"),
                html.Div(id="profile-alert-login"),
                html.Div(id="profile-login-trigger", style=dict(display="none")),
                html.Br(),
                dbc.Row(
                    dbc.Col(
                        [
                            # First, first input, and formtext
                            dbc.Label("First:", id="profile-first"),
                            dbc.Input(
                                placeholder="Change first name...",
                                id="profile-first-input",
                            ),
                            dbc.FormText(
                                id="profile-first-formtext", color="secondary"
                            ),
                            html.Br(),
                            # last, last input, and formtext
                            dbc.Label("Last:", id="profile-last"),
                            dbc.Input(
                                placeholder="Change last name...",
                                id="profile-last-input",
                            ),
                            dbc.FormText(id="profile-last-formtext", color="secondary"),
                            html.Br(),
                            # email, formtext
                            dbc.Label("Email:", id="profile-email"),
                            dbc.FormText("Cannot change email", color="secondary"),
                            html.Br(),
                            html.Hr(),
                            html.Br(),
                            # password, input, confirm input
                            dbc.Label("Change password", id="profile-password"),
                            dbc.Input(
                                placeholder="Change password...",
                                id="profile-password-input",
                                type="password",
                            ),
                            dbc.FormText(
                                "Change password",
                                color="secondary",
                                id="profile-password-input-formtext",
                            ),
                            html.Br(),
                            dbc.Input(
                                placeholder="Confirm password...",
                                id="profile-password-confirm",
                                type="password",
                            ),
                            dbc.FormText(
                                "Confirm password",
                                color="secondary",
                                id="profile-password-confirm-formtext",
                            ),
                            html.Br(),
                            html.Hr(),
                            html.Br(),
                            dbc.Button(
                                "Save changes",
                                color="primary",
                                id="profile-submit",
                                disabled=True,
                            ),
                        ]
                    )
                ),
            ],  # end col
            width=6,
        )
    )


# function to show profile values
@callback(
    Output("profile-first", "children"),
    Output("profile-last", "children"),
    Output("profile-email", "children"),
    Output("profile-first-input", "value"),
    Output("profile-last-input", "value"),
    Input("profile-trigger", "children"),
)
def profile_values(trigger):
    """
    triggered by loading the change or saving new values

    loads values from user to database
    user must be logged in
    """
    if not trigger:
        return "First: ", "Last: ", "Email:", "", ""
    if current_user.is_authenticated:
        return (
            ["First: ", html.Strong(current_user.first)],
            ["Last: ", html.Strong(current_user.last)],
            ["Email: ", html.Strong(current_user.email)],
            current_user.first,
            current_user.last,
        )
    return "First: ", "Last: ", "Email:", "", ""


# function to validate changes input
@callback(
    Output("profile-first-input", "valid"),
    Output("profile-last-input", "valid"),
    Output("profile-password-input", "valid"),
    Output("profile-password-confirm", "valid"),
    Output("profile-first-input", "invalid"),
    Output("profile-last-input", "invalid"),
    Output("profile-password-input", "invalid"),
    Output("profile-password-confirm", "invalid"),
    Output("profile-password-input-formtext", "color"),
    Output("profile-password-confirm-formtext", "color"),
    Output("profile-submit", "disabled"),
    Input("profile-first-input", "value"),
    Input("profile-last-input", "value"),
    Input("profile-password-input", "value"),
    Input("profile-password-confirm", "value"),
)
def profile_validate(first, last, password, confirm):
    disabled = True
    bad = ["", None]
    values = [first, last, password, confirm]
    valids = [False for x in range(4)]
    invalids = [False for x in range(4)]
    colors = ["secondary", "secondary"]

    # if all are invalid
    if sum([x in bad for x in values]) == 4:
        return valids + invalids + colors + [disabled]

    # first name
    i = 0
    if first in bad:
        pass
    else:
        if isinstance(first, str):
            valids[i] = True
        else:
            invalids[i] = True
            colors[0] = "danger"

    # last name
    i = 1
    if last in bad:
        pass
    else:
        if isinstance(last, str):
            valids[i] = True
        else:
            invalids[i] = True
            colors[1] = "danger"

    i = 2
    if password in bad:
        pass
    else:
        if isinstance(password, str):
            valids[i] = True
            i = 3
            if confirm == password:
                valids[i] = True
            else:
                invalids[i] = True
        else:
            invalids[i] = True

    # if all inputs are either valid or empty, enable the button
    if (
        sum(
            [
                1
                if (v == False and inv == False) or (v == True and inv == False)
                else 0
                for v, inv in zip(valids, invalids)
            ]
        )
        == 4
    ):
        disabled = False

    return valids + invalids + colors + [disabled]


# function to save changes
@callback(
    Output("profile-alert", "children"),
    Output("profile-trigger", "children"),
    Input("profile-submit", "n_clicks"),
    State("profile-first-input", "value"),
    State("profile-last-input", "value"),
    State("profile-password-input", "value"),
    prevent_initial_call=True,
)
def profile_save_changes(n_clicks, first, last, password):
    """
    change profile values to values in inputs

    if password is blank, pull the current password and submit it
    assumes all inputs are valid and checked by validator callback before submitting (enforced by disabling button otherwise)
    """
    email = current_user.email

    user = User.from_email(email)
    if not user:
        return failure_alert, 0
    user.first = first
    user.last = last
    user.email = email
    with get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)

    if password not in ["", None]:
        change_password(user.email, password)

    return success_alert, 1
