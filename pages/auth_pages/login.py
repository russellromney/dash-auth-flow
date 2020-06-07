import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import no_update

from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
import time

from server import app, User


success_alert = dbc.Alert(
    'Logged in successfully. Taking you home!',
    color='success',
    dismissable=True
)
failure_alert = dbc.Alert(
    'Login unsuccessful. Try again.',
    color='danger',
    dismissable=True
)
already_login_alert = dbc.Alert(
    'User already logged in. Taking you home!',
    color='warning',
    dismissable=True
)


def layout():
    return dbc.Row(
        dbc.Col(
            [
                dcc.Location(id='login-url',refresh=True,pathname='/login'),
                html.Div(id='login-trigger',style=dict(display='none')),
                html.Div(id='login-alert'),
                dbc.FormGroup(
                    [
                        dbc.Alert('Try test@test.com / test', color='info',dismissable=True),
                        html.Br(),

                        dbc.Input(id='login-email',autoFocus=True),
                        dbc.FormText('Email'),
                        
                        html.Br(),
                        dbc.Input(id='login-password',type='password'),
                        dbc.FormText('Password'),
                        
                        html.Br(),
                        dbc.Button('Submit',color='primary',id='login-button'),
                        #dbc.FormText(id='output-state')
                        
                        html.Br(),
                        html.Br(),
                        dcc.Link('Register',href='/register'),
                        html.Br(),
                        dcc.Link('Forgot Password',href='/forgot')
                    ]
                )
            ],
            width=6
        )
    )



@app.callback(
    [Output('login-url', 'pathname'),
     Output('login-alert', 'children')],
    [Input('login-button', 'n_clicks')],
    [State('login-email', 'value'),
     State('login-password', 'value')]
)
def login_success(n_clicks, email, password):
    '''
    logs in the user
    '''
    if n_clicks > 0:
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)

                return '/home',success_alert
            else:
                return no_update,failure_alert
        else:
            return no_update,failure_alert
    else:
        return no_update,''