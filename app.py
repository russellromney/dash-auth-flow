import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, callback
import dash
from application import app, server
from flask_login import current_user
from utils.config import config
from utils.auth import protect_app, unprotected


header = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand(
                [
                    html.Img(src="/assets/favicon.ico", height="30px"),
                    html.Span("Dash Auth Flow", style=dict(marginLeft="10px")),
                ],
                href=config["HOME_PATH"],
                style=dict(maxWidth="300px"),
            ),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Public", href="/public")),
                    dbc.NavItem(dbc.NavLink("Home", href=config["HOME_PATH"])),
                    dbc.NavItem(dbc.NavLink("Page", href="/page")),
                    dbc.NavItem(
                        dbc.NavLink(
                            html.Span(id="user-name-nav"),
                            href="/profile",
                        )
                    ),
                    dbc.NavItem(dbc.NavLink("Login", id="user-action", href="/login")),
                ],
            ),
        ],
    ),
    # className="mb-5",
    color="dark",
    dark=True,
)


app.layout = html.Div(
    [
        header,
        html.Br(),
        dbc.Container(dash.page_container),
        dcc.Location(id="url", refresh=True),
        html.Div(id="profile-trigger", style=dict(display="none")),
    ]
)


@callback(
    Output("user-name-nav", "children"),
    Input("url", "pathname"),
    Input("profile-trigger", "children"),
)
@unprotected
def profile_link(_, __):
    """
    Returns a navbar link to the user profile if the user is authenticated
    """
    if current_user.is_authenticated:
        return [
            html.I(className="bi bi-person-circle", style=dict(marginRight="5px")),
            current_user.first,
        ]
    else:
        return ""


@callback(
    Output("user-action", "children"),
    Output("user-action", "href"),
    Input("url", "pathname"),
)
@unprotected
def user_logout_or_login(_):
    """
    returns a navbar link to /logout or /login, respectively, if the user is authenticated or not
    """
    if current_user.is_authenticated:
        out = "Logout", "/logout"
    else:
        out = "Login", "/login"
    return out


protect_app(default=True)
if __name__ == "__main__":
    app.run_server(debug=True)
