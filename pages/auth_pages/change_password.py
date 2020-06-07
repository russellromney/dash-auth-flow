import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import no_update

from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
from sqlalchemy.sql import select

from server import app, User, engine
from utilities.auth import (
    validate_password_key,
    change_password,
)

import time

success_alert = dbc.Alert(
    'Reset successful. Taking you to login!',
    color='success',
)
failure_alert = dbc.Alert(
    'Reset unsuccessful. Are you sure the email and code were correct?',
    color='danger',
)
already_login_alert = dbc.Alert(
    'User already logged in. Taking you to your profile.',
    color='warning'
)

def layout():
    return dbc.Row(
        dbc.Col(
            [
                html.H3('Change Password'),
                dcc.Location(id='change-url',refresh=True),
                html.Div(id='change-trigger',style=dict(display='none')),
                dbc.FormGroup(
                    [
                        html.Div(id='change-alert'),
                        html.Br(),

                        dbc.Input(id='change-email',autoFocus=True),
                        dbc.FormText('Email'),
                        html.Br(),
                        
                        dbc.Input(id='change-key',type='password'),
                        dbc.FormText('Code'),
                        html.Br(),

                        dbc.Input(id='change-password',type='password'),
                        dbc.FormText('New password'),
                        html.Br(),

                        dbc.Input(id='change-confirm',type='password'),
                        dbc.FormText('Confirm new password'),
                        html.Br(),

                        dbc.Button('Submit password change',id='change-button',color='primary'),

                    ]
                )
            ],
            width=6
        )
    )


# function to validate inputs
@app.callback(
    [Output('change-password','valid'),
     Output('change-password','invalid'),
     Output('change-confirm','valid'),
     Output('change-confirm','invalid'),
     Output('change-button','disabled')],
    [Input('change-password','value'),
     Input('change-confirm','value')]
)
def change_validate_inputs(password,confirm):
    password_valid = False
    password_invalid = False
    confirm_valid = False
    confirm_invalid = True
    disabled = True
    
    bad = [None,'']

    if password in bad:
        pass
    elif isinstance(password,str):
        password_valid = True
        password_invalid = False
    
    if confirm in bad:
        pass
    elif confirm==password:
        confirm_valid = True
        confirm_invalid = False
    
    if password_valid and confirm_valid:
        disabled = False

    return (
        password_valid,
        password_invalid,
        confirm_valid,
        confirm_invalid,
        disabled
    )


@app.callback(
    [Output('change-alert','children'),
     Output('change-url','pathname')],
    [Input('change-button','n_clicks')],
    [State('change-email','value'),
     State('change-key','value'),
     State('change-password','value'),
     State('change-confirm','value')]
)
def submit_change(submit,email,key,password,confirm):
    # all inputs have been previously validated
    # validate_password_key(email,key,engine)
    if validate_password_key(email,key,engine):
        print('validate password success')
        # if that returns true, update the user information
        if change_password(email,password,engine):
            return success_alert,'/login' 
        else:
            print('validate password failed - at after change user')
            pass
    else:
        print('validate password failed')
        pass
    return failure_alert, no_update