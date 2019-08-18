# index page
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from flask import redirect
from server import app, server
from flask_login import logout_user, current_user

from pages import (
    login,
    logout,
    register,
    home,
    profile,
    change_password,
    forgot_password    
)


header = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("My App", href="/home"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink(id='user-name',href='/profile')),
                    dbc.NavItem(dbc.NavLink("Home", href="/home")),
                    dbc.NavItem(dbc.NavLink('Login',id='user-action',href='Login'))
                ]
            )
        ]
    ),
    className="mb-5",
)



app.layout = html.Div(
    [
        header,
        html.Div(
            [
                dbc.Container(
                    id='page-content'
                )
            ]
        ),
        dcc.Location(id='url', refresh=False),
    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def router(pathname):
    if pathname == '/home' or pathname== '/':
        return home.layout
    elif pathname == '/profile':
        return profile.layout
    elif pathname == '/login':
        return login.layout
    elif pathname == '/logout':
        return logout.layout
    elif pathname =='/register':
        return register.layout
    elif pathname == '/change':
        return change_password.layout
    elif pathname == '/forgot':
        return forgot_password.layout
    #elif pathname == '/app/home':
    #elif pathname == '/app/investment':
    # elif pathname == '/app/user':
    else:
        return '404'


@app.callback(
    Output('user-name', 'children'),
    [Input('page-content', 'children')])
def cur_user(input1):
    if current_user.is_authenticated:
        return html.Div(current_user.first)
    else:
        return ''


@app.callback(
    [Output('user-action', 'children'),
     Output('user-action','href')],
    [Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return 'Logout', '/logout'
    else:
        return 'Login', '/login'





if __name__ == '__main__':
    app.run_server(debug=True)
