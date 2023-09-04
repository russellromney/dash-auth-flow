import uuid
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, no_update, register_page, callback
from flask_login import current_user
import time
from validate_email import validate_email
from models.user import User

from utils.auth import redirect_authenticated, unprotected
from utils.user import add_user
from utils.config import config

register_page(__name__, path="/register")


@unprotected
@redirect_authenticated(config["HOME_PATH"])
def layout():
    return dbc.Row(
        dbc.Col(
            [
                html.Div(id="register-alert"),
                dbc.Row(
                    dbc.Col(
                        [
                            dbc.FormText("First"),
                            dbc.Input(id="register-first", autoFocus=True),
                            html.Br(),
                            dbc.FormText("Last"),
                            dbc.Input(id="register-last"),
                            html.Br(),
                            dbc.FormText(
                                "Email", id="register-email-formtext", color="secondary"
                            ),
                            dbc.Input(id="register-email"),
                            html.Br(),
                            dbc.FormText("Password"),
                            dbc.Input(id="register-password", type="password"),
                            html.Br(),
                            dbc.FormText("Confirm password"),
                            dbc.Input(id="register-confirm", type="password"),
                            html.Br(),
                            dbc.Button("Submit", color="primary", id="register-button"),
                            dcc.Loading(
                                [
                                    html.Div(
                                        id="register-trigger",
                                        style=dict(display="none"),
                                    ),
                                    html.Div(id="register-redirect"),
                                ],
                                id=uuid.uuid4().hex,
                            ),
                        ]
                    ),
                ),
            ],
            className="auth-page",
        )
    )


success_alert = dbc.Alert(
    "Registered successfully. Taking you to login.", color="success"
)
failure_alert = dbc.Alert(
    "Registration unsuccessful. Try again.",
    color="danger",
    dismissable=True,
    duration=config["ALERT_DELAY"],
)


@callback(
    Output("register-first", "valid"),
    Output("register-last", "valid"),
    Output("register-email", "valid"),
    Output("register-password", "valid"),
    Output("register-confirm", "valid"),
    Output("register-first", "invalid"),
    Output("register-last", "invalid"),
    Output("register-email", "invalid"),
    Output("register-password", "invalid"),
    Output("register-confirm", "invalid"),
    Output("register-button", "disabled"),
    Output("register-email-formtext", "children"),
    Output("register-email-formtext", "color"),
    Input("register-first", "value"),
    Input("register-last", "value"),
    Input("register-email", "value"),
    Input("register-password", "value"),
    Input("register-confirm", "value"),
    prevent_initial_call=True,
)
def register_validate_inputs(first, last, email, password, confirm):
    """
    validate all inputs
    """

    email_formtext = "Email"
    email_formcolor = "secondary"
    disabled = True
    bad = [None, ""]

    v = {
        k: f
        for k, f in zip(
            ["first", "last", "email", "password", "confirm"],
            [first, last, email, password, confirm],
        )
    }
    # if all the values are empty, leave everything blank and disable button
    if sum([x in bad for x in v.values()]) == 5:
        return [False for x in range(10)] + [disabled, email_formtext, email_formcolor]

    d = {}
    d["valid"] = {x: False for x in ["first", "last", "email", "password", "confirm"]}
    d["invalid"] = {x: False for x in ["first", "last", "email", "password", "confirm"]}

    def validate(x, inst):
        if v[x] in bad:
            pass
        elif not isinstance(v[x], inst):
            d["valid"][x], d["invalid"][x] = False, True
        else:
            d["valid"][x], d["invalid"][x] = True, False

    for k in ["first", "last", "password"]:
        validate(k, str)

    x = "confirm"
    if v[x] in bad:
        pass
    d["valid"][x] = not v[x] in bad and v["password"] == v[x]
    d["invalid"][x] = not v["confirm"]

    # if it's a valid email, check if it already exists
    # if it exists, invalidate it and let the user know
    x = "email"
    if v[x] in bad:
        pass
    else:
        d["valid"][x] = validate_email(v[x])
        d["invalid"][x] = not d["valid"][x]
    if User.from_email(v[x]):
        d["valid"][x] = False
        d["invalid"][x] = True
        email_formcolor = "danger"
        email_formtext = "Email is already registered."

    # if all are valid, enable the button
    if sum(d["valid"].values()) == 5:
        disabled = False

    return [
        *list(d["valid"].values()),
        *list(d["invalid"].values()),
        disabled,
        email_formtext,
        email_formcolor,
    ]


@callback(
    Output("register-alert", "children"),
    Output("register-trigger", "children"),
    Input("register-button", "n_clicks"),
    State("register-first", "value"),
    State("register-last", "value"),
    State("register-email", "value"),
    State("register-password", "value"),
    State("register-confirm", "value"),
    prevent_initial_call=True,
)
def register_success(n_clicks, first, last, email, password, confirm):
    if add_user(first, last, password, email):
        return (
            success_alert,
            1,
        )
    else:
        return failure_alert, no_update


@callback(
    Output("url", "pathname", allow_duplicate=True),
    Output("register-redirect", "children"),
    Input("register-trigger", "children"),
    prevent_initial_call=True,
)
def register_redirect(trigger):
    if trigger:
        if trigger == 1:
            time.sleep(config["TRANSITION_DELAY"])
            return "/login", ""
    return no_update, no_update
