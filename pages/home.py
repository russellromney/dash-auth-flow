import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

layout = dbc.Row(
    dbc.Col(
        [
            dcc.Location(id='home-url',refresh=True),
            html.H1('Home page'),
            html.Br(),

            html.H5('Welcome to the home page!')
        ],
        width=6
    )

)