import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input,State
from dash import no_update
from flask_login import current_user
import time

from server import app

home_login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)

def layout():
    return dbc.Row(
        dbc.Col(
            [
                dcc.Location(id='home-url',refresh=True),
                html.Div(id='home-login-trigger',style=dict(display='none')),

                html.H1('Home page'),
                html.Br(),

                html.H5('Welcome to the home page!'),
                html.Br(),

                html.Div(id='home-test-trigger'),
                html.Div('before update',id='home-test')
            ],
            width=6
        )
    )

@app.callback(
    Output('home-test','children'),
    [Input('home-test-trigger','children')]
)
def home_test_update(trigger):
    '''
    updates arbitrary value on home page for test
    '''    
    time.sleep(2)
    return html.Div('after the update',style=dict(color='red'))
