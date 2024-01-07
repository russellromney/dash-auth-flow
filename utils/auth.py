from typing import Callable
from dash import dcc, page_registry, _callback
from dash.exceptions import PreventUpdate
from flask import current_app
from flask_login import current_user


def redirect_authenticated(pathname: str) -> Callable:
    """
    If the user is authenticated, redirect them to the provided page pathname.
    """

    def wrapper(f: Callable):
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated:
                return dcc.Location(
                    id="redirect-authenticated-user-to-path",
                    pathname=pathname,
                )
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def unprotected(f: Callable) -> Callable:
    """
    Explicitly allows any User to access the layout function or callback function output.
    Decorates a Dash page layout function or callback function.
    Used in conjunction with Dash Pages and Flask Login.

    IMPORTANT NOTE: 
        For a layout function, this must be the first/outermost.
        For a callback, this must be the decorator directly after `dash.callback`.

    ###### FOR LAYOUTS
    @unprotected
    @other_decorator
    def layout():
        return html.Div(...)


    ###### FOR CALLBACKS
    @unprotected
    @callback
    def do_stuff(Output(...), Input(...)):
        return 1
    """
    f.is_protected = False
    return f


def protected(f: Callable) -> Callable:
    """
    Explicitly requires a user to be authenticated to access the layout function or callback function output.
    Decorates a Dash page layout function or callback function.
    Used in conjunction with Dash Pages and Flask Login.

    IMPORTANT NOTE: 
        For a layout function, this must be the first/outermost.
        For a callback, this must be the decorator directly after `dash.callback`.

    ###### FOR LAYOUTS
    @protected
    @other_decorator
    def layout():
        return html.Div(...)


    ###### FOR CALLBACKS
    @callback(Output(...), Input(...))
    @protected
    def do_stuff():
        return 1
    """
    f.is_protected = True
    return f


def _protect_layout(f: Callable) -> Callable:
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            return dcc.Location(
                id="redirect-unauthenticated-user-to-login",
                pathname=current_app.login_manager.login_view,
            )
        return f(*args, **kwargs)

    return wrapped


def protect_layouts(default: bool = True):
    """
    Call this after defining the global dash.Dash object.
    Protect any explicitly protected views and *do not* protect any explicitly unprotected views.
    Otherwise, protect all or none according to the `default`.
    """
    for page in page_registry.values():
        if hasattr(page["layout"], "is_protected"):
            if bool(getattr(page["layout"], "is_protected")) == False:
                continue
            else:
                page["layout"] = _protect_layout(page["layout"])
        elif default == True:
            page["layout"] = _protect_layout(page["layout"])


def _protect_callback(f: Callable) -> Callable:
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            # print("_protect_callback PROTECTED", f)
            raise PreventUpdate
        return f(*args, **kwargs)

    return wrapped


def protect_callbacks(default: bool = True):
    for key, value in _callback.GLOBAL_CALLBACK_MAP.items():
        if hasattr(value["callback"], "is_protected"):
            if bool(getattr(value["callback"], "is_protected")) == False:
                continue
            else:
                # print("PROTECTING CALLBACK", key)
                value["callback"] = value["callback"] = _protect_callback(
                    value["callback"]
                )
        elif default == True:
            # print("PROTECTING CALLBACK", key)
            value["callback"] = _protect_callback(value["callback"])


def protect_app(default: bool = True):
    """
    Protect Dash pages and callbacks from unauthorized access according to a global default.

    Works in conjunction with Dash Pages and Flask Login.
    Is NOT compatible with Dash 1.x, only 2.x+.
    Any views/layouts that are not defined with Dash Pages <WILL NOT BE PROTECTED>

    Otherwise, protect all or none according to the `default` (True = protected, False = unprotected).

    Call this after defining the global dash.Dash object and just before where
    the app is imported to run it, or run explicitly (i.e. locally).
    """
    protect_callbacks(default)
    protect_layouts(default)
