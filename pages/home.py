import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input,State
from dash import no_update

from flask_login import current_user
import time

from server import app
from utilities.auth import layout_auth

home_login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)

@layout_auth('auth',
    dbc.Row(
        dbc.Col(
            [
                dcc.Location(id='home-url',refresh=True,pathname='/app/home'),
                html.Div('/login',id='home-login-trigger',style=dict(display='none')),
                html.Div(home_login_alert)
            ]
        )
    )
)
def layout():
    return dbc.Row(
        dbc.Col(
            [
                dcc.Location(id='home-url',refresh=True,pathname='/app/home'),
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




@app.callback(
    Output('home-url','pathname'),
    [Input('home-login-trigger','children')]
)
def home_send_to_login(url):
    '''
    if user isn't logged in, sends to login

    only triggered if user not authenticated
    '''
    if url is None or url=='':
        return no_update
    time.sleep(1.5)
    return url
