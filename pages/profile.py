import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import no_update

from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
import time

from server import app, User, engine
from utilities.auth import change_user, change_password


success_alert = dbc.Alert(
    'Changes saved successfully.',
    color='success',
)
failure_alert = dbc.Alert(
    'Unable to save changes.',
    color='danger',
)
login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='warning',
)


def layout():
    return dbc.Row(
        dbc.Col(
            [
                dcc.Location(id='profile-url', refresh=True,    ),
                html.Div(1,id='profile-trigger',style=dict(display='none')),
                
                html.H3('Profile',id='profile-title'),
                html.Div(id='profile-alert'),
                html.Div(id='profile-alert-login'),
                html.Div(id='profile-login-trigger',style=dict(display='none')),
                html.Br(),

                dbc.FormGroup(
                    [
                        # First, first input, and formtext
                        dbc.Label('First:',id='profile-first'),
                        dbc.Input(placeholder='Change first name...',id='profile-first-input'),
                        dbc.FormText(id='profile-first-formtext',color='secondary'),
                        html.Br(),

                        # last, last input, and formtext
                        dbc.Label('Last:',id='profile-last'),
                        dbc.Input(placeholder='Change last name...',id='profile-last-input'),
                        dbc.FormText(id='profile-last-formtext',color='secondary'),
                        html.Br(),

                        # email, formtext
                        dbc.Label('Email:',id='profile-email'),
                        dbc.FormText('Cannot change email',color='secondary'),
                        html.Br(),

                        html.Hr(),
                        html.Br(),

                        # password, input, confirm input
                        dbc.Label('Change password',id='profile-password'),
                        dbc.Input(placeholder='Change password...',id='profile-password-input',type='password'),
                        dbc.FormText('Change password',color='secondary',id='profile-password-input-formtext'),
                        html.Br(),
                        dbc.Input(placeholder='Confirm password...',id='profile-password-confirm',type='password'),
                        dbc.FormText('Confirm password',color='secondary',id='profile-password-confirm-formtext'),
                        html.Br(),
                        
                        html.Hr(),
                        html.Br(),

                        dbc.Button('Save changes',color='primary',id='profile-submit',disabled=True),
                        
                    ] # end formgroup
                )
            ], # end col
            width=6
        )

    )




# function to show profile values
@app.callback(
    [Output('profile-alert-login','children'),
     Output('profile-login-trigger','children')]+\
    [Output('profile-'+x,'children') for x in ['first','last','email']]+\
    [Output('profile-{}-input'.format(x),'value') for x in ['first','last']],
    [Input('profile-trigger','children')]
)
def profile_values(trigger):
    '''
    triggered by loading the change or saving new values

    loads values from user to database
    user must be logged in
    '''
    if not trigger:
        return no_update, no_update, 'First: ', 'Last: ', 'Email:', '', ''
    if current_user.is_authenticated:
        return (
            no_update,
            no_update,
            ['First: ',html.Strong(current_user.first)] ,
            ['Last: ',html.Strong(current_user.last)] ,
            ['Email: ',html.Strong(current_user.email)] ,
            current_user.first ,
            current_user.last
        )
    return login_alert, '/login', 'First: ', 'Last: ', 'Email:', '', ''


# function to validate changes input
@app.callback(
    [Output('profile-'+x,'valid') for x in ['first-input','last-input','password-input','password-confirm']]+\
    [Output('profile-'+x,'invalid') for x in ['first-input','last-input','password-input','password-confirm']]+\
    [Output('profile-'+x,'color') for x in ['-password-input-formtext','-password-confirm-formtext']]+\
    [Output('profile-submit','disabled')],
    [Input('profile-'+x,'value') for x in ['first-input','last-input','password-input','password-confirm']]
)
def profile_validate(first,last,password,confirm):
    disabled = True
    bad = ['',None]
    values = [first,last,password,confirm]
    valids = [False for x in range(4)]
    invalids = [False for x in range(4)]
    colors = ['secondary','secondary']

    # if all are invalid
    if sum([x in bad for x in values])==4:
        return valids+invalids+colors+[disabled]

    # first name
    i = 0
    if first in bad:
        pass
    else:
        if isinstance(first,str):
            valids[i]=True
        else:
            invalids[i]=True
            colors[0] = 'danger'
    
    # last name
    i = 1
    if last in bad:
        pass
    else:
        if isinstance(last,str):
            valids[i]=True
        else:
            invalids[i]=True
            colors[1] = 'danger'

    i = 2
    if password in bad:
        pass
    else:
        if isinstance(password,str):
            valids[i] = True
            i=3
            if confirm == password:
                valids[i] = True
            else:
                invalids[i] = True
        else:
            invalids[i] = True
    
    # if all inputs are either valid or empty, enable the button
    if sum([1 if (v==False and inv==False) or (v==True and inv==False) else 0 for v,inv in zip(valids,invalids)])==4:
        disabled=False

    return valids+invalids+colors+[disabled]


    

# function to save changes
@app.callback(
    [Output('profile-alert','children'),
     Output('profile-trigger','children')],
    [Input('profile-submit','n_clicks')],
    [State('profile-{}-input'.format(x),'value') for x in ['first','last','password']]
)
def profile_save_changes(n_clicks,first,last,password):
    '''
    change profile values to values in inputs

    if password is blank, pull the current password and submit it
    assumes all inputs are valid and checked by validator callback before submitting (enforced by disabling button otherwise)
    '''
    email = current_user.email

    if change_user(first,last,email,engine):
        if password not in ['',None]:
            change_password(email,password,engine)
        return success_alert,1
    
    return failure_alert,0
