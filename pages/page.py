import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html, no_update, register_page, callback
import time

register_page(__name__, path="/page")


def layout():
    # if current_user.is_authenticated:
    return dbc.Row(
        dbc.Col(
            [
                html.H1("page"),
                html.Br(),
                html.H5("Welcome to this page!"),
                html.Br(),
                html.P(
                    "Below is an iframe of another website that loads after 1 second:"
                ),
                html.Div(id="page-test-trigger"),
                dcc.Loading(
                    html.Iframe(
                        id="page-test", style=dict(height="500px", width="100%")
                    ),
                    id="page-loading",
                    type="circle",
                    style=dict(width="100%"),
                ),
            ],
            width=10,
        )
    )


@callback(Output("page-test", "src"), Input("page-test-trigger", "children"))
def page_div_update(trigger):
    """
    updates iframe with example.com
    """
    time.sleep(1)
    return "https://example.cypress.io/"
