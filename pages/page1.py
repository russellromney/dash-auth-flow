import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input,State
from dash import no_update
import random
from flask_login import current_user
import time
from functools import wraps

from server import app

login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)

location = dcc.Location(id='page1-url',refresh=True)

def layout():
    #if current_user.is_authenticated:
    return dbc.Row(
        dbc.Col(
            [
                location,
                html.Div(id='page1-login-trigger'),

                html.H1('Page1'),
                html.Br(),

                html.H5('Welcome to Page1!'),
                html.Br(),

                html.Div(id='page1-test-trigger'),
                dcc.Loading(html.Iframe(id='page1-test',style=dict(height='500px',width='100%')),id='page1-loading')
            ],
            width=6
        )

    )


@app.callback(
    Output('page1-test','src'),
    [Input('page1-test-trigger','children')]
)
def page1_test_update(trigger):
    '''
    updates iframe with example.com
    '''    
    time.sleep(2)
    return 'http://example.com/'

