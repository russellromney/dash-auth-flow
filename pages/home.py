import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html, no_update, register_page, callback
import time


register_page(__name__, path="/home")


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
                    type="circle",
                    style=dict(width="100%"),
                ),
            ],
            width=10,
        )
    )


@callback(Output("home-test", "children"), Input("home-test-trigger", "children"))
def home_div_update(trigger):
    """
    updates arbitrary value on home page for test
    """
    time.sleep(1)
    return html.Div("after the update", style=dict(color="red"))
