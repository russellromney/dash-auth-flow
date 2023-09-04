import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, register_page, callback
import dash
from application import app, server
from flask_login import current_user
from utils.config import config

header = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Dash Auth Flow", href=config["HOME_PATH"]),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Home", href=config["HOME_PATH"])),
                    dbc.NavItem(dbc.NavLink("Page", href="/page")),
                    dbc.NavItem(dbc.NavLink(id="user-name-nav", href="/profile")),
                    dbc.NavItem(dbc.NavLink("Login", id="user-action", href="/login")),
                ]
            ),
        ]
    ),
    className="mb-5",
)


app.layout = html.Div(
    [
        header,
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
def profile_link(_, __):
    """
    Returns a navbar link to the user profile if the user is authenticated
    """
    if current_user.is_authenticated:
        return html.Div(current_user.first)
    else:
        return ""


@callback(
    Output("user-action", "children"),
    Output("user-action", "href"),
    Input("url", "pathname"),
)
def user_logout(_):
    """
    returns a navbar link to /logout or /login, respectively, if the user is authenticated or not
    """
    if current_user.is_authenticated:
        out = "Logout", "/logout"
    else:
        out = "Login", "/login"
    return out


if __name__ == "__main__":
    app.run_server(debug=True)
