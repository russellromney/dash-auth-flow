import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html, no_update, register_page, callback
import time
from utils.config import config


register_page(__name__, path=config["HOME_PATH"])


def layout():
    return dbc.Row(
        dbc.Col(
            [
                html.H1("Home page"),
                html.Br(),
                html.H5("Welcome to the home page!"),
                html.Br(),
                html.P(
                    "The section below is updated after a callback that takes 1 second!"
                ),
                html.Div(id="home-test-trigger"),
                dcc.Loading(
                    html.Div("before update", id="home-test"),
                    id="loading-home-test-trigger",
                    style=dict(width="100%"),
                ),
            ],
            className="page-content",
        ),
    )


@callback(Output("home-test", "children"), Input("home-test-trigger", "children"))
def home_div_update(_):
    """Updates arbitrary value on home page as example of callback."""
    time.sleep(1)
    return html.Div("after the update", style=dict(color="red"))
