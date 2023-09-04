# external imports
import dash_bootstrap_components as dbc
import dash
from flask import Flask, request, current_app
from flask_login import LoginManager
import sqlalchemy

# local imports
from models.user import User
from utils.auth import protect_layouts
from utils.config import get_session, make_engine


def create_app():
    server = Flask(__name__)
    app = dash.Dash(
        __name__,
        server=server,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        # prevent_initial_callbacks=True,
        use_pages=True,
        suppress_callback_exceptions=True,
        title="Dash Auth Flow",
        update_title=None,
    )

    # app.css.config.serve_locally = True
    # app.scripts.config.serve_locally = True

    # config
    server.config.update(
        SECRET_KEY="make this key random or hard to guess",
    )

    server.engine = make_engine()

    # Setup the LoginManager for the server
    login_manager = LoginManager()
    login_manager.init_app(server)
    login_manager.login_view = "/login"

    # callback to reload the user object
    @login_manager.user_loader
    def load_user(user_id):
        with get_session() as session:
            return session.get(User, user_id)

    return app, server


app, server = create_app()
protect_layouts(default=True)
