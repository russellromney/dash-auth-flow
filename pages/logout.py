import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import no_update

from flask_login import logout_user, current_user

import time


from server import app

success_alert = dbc.Alert(
    'Logged out. Taking you to home.',
    color='success',
    dismissable=False
)
failure_alert = dbc.Alert(
    'Not logged in. Taking you to login.',
    color='danger',
    dismissable=False
)

layout = dbc.Row(
    dbc.Col(
        [
            dcc.Location(id='logout-url', refresh=True),
            html.Div(id='logout-hidden-url',style=dict(display='none')),
            html.Div(id='logout-trigger',style=dict(display='none')),
            html.Div(id='logout-message'),
            dbc.Button('Logout',id='logout-button',color='danger',block=True,size='lg')
        ],
        width=6
    )
)

@app.callback(
    [Output('logout-hidden-url','children'),
     Output('logout-message','children')],
    [Input('logout-button','n_clicks'),
     Input('logout-trigger','children')]
)
def logout_card(n_clicks,c):
    print(n_clicks)
    if n_clicks==0 or n_clicks is None:
        if not current_user.is_authenticated:
            return '/login',failure_alert
        else:
            return no_update,no_update
    if current_user.is_authenticated:
            logout_user()
            return '/home',success_alert
    else:
        return '/login',failure_alert

@app.callback(
    Output('logout-url','pathname'),
    [Input('logout-hidden-url','children')]
)
def logout_wait_and_reload(url):
    if url is None or url=='':
        return no_update
    time.sleep(1.5)
    return url
