from logzero import logger
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, register_page, callback
import dash
from application import app
from flask_login import current_user

register_page(__name__, path="/")


header = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Dash Auth Flow", href="/home"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Home", href="/home")),
                    dbc.NavItem(dbc.NavLink("Page", href="/page")),
                    dbc.NavItem(dbc.NavLink(id="user-name", href="/profile")),
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
        dcc.Location(id="base-url", refresh=True),
    ]
)


@callback(Output("user-name", "children"), Input("base-url", "pathname"))
def profile_link(_):
    """
    returns a navbar link to the user profile if the user is authenticated
    """
    if current_user.is_authenticated:
        return html.Div(current_user.first)
    else:
        return ""


@callback(
    Output("user-action", "children"),
    Output("user-action", "href"),
    Input("base-url", "pathname"),
)
def user_logout(_):
    """
    returns a navbar link to /logout or /login, respectively, if the user is authenticated or not
    """

    if current_user.is_authenticated:
        out = "Logout", "/logout"
    else:
        out = "Login", "/login"
    logger.info("user_logout " + str(out))
    return out


if __name__ == "__main__":
    app.run_server(debug=True)
