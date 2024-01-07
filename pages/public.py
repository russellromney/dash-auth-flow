import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html, no_update, register_page, callback
import time
from utils.auth import unprotected

register_page(__name__, path="/public")


@unprotected
def layout():
    return dbc.Row(
        dbc.Col(
            [
                html.H1("Public"),
                html.Br(),
                html.H5("This public page can be viewed by anyone!"),
                html.Br(),
                html.P(
                    "Below is an iframe of another website that loads after 1 second:"
                ),
                html.Div(id="public-test-trigger"),
                dcc.Loading(
                    html.Iframe(
                        id="public-test", style=dict(height="500px", width="100%")
                    ),
                    id="public-loading",
                    style=dict(width="100%"),
                ),
            ],
            className="public-content",
        )
    )


@unprotected
@callback(Output("public-test", "src"), Input("public-test-trigger", "children"))
def public_div_update(_):
    """
    updates iframe with example.com
    """
    time.sleep(1)
    return "https://example.cypress.io/"
