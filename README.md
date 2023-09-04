# dash-auth-flow

Batteries-included authentication flow in [Dash](dash.plot.ly) with Dash Pages.

This has landing pages and functions to run the entire authentication flow:

- home
- login
- logout
- register
- forgot password
- change password

This uses `flask-login` on the backend, taking some inspiration from the very useful [dash-flask-login](https://github.com/RafaelMiquelino/dash-flask-login). Data is held in `users.db`.

```shell
# with plain virtualenv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python create_tables.py # test@test.com / test
python app.py

# with pipenv
pip install pipenv
pipenv install --ignore-pipfile
pipenv shell
python create_tables.py # test@test.com / test
python app.py

# either: deactivate virtual environment
deactivate
```

![](example.gif)

## Notes:

- this uses MailJet as the email API. You need a [free MailJet API key](https://www.mailjet.com/email-api/)
- your send-from email and API key/secret need to be entered in `.env`
- if you want to use a different email provider, change the `send_password_key` function in `utilities/auth.py`
- add pages in `pages/`. Make sure to register the page at a path with `register_page(__name__, pathname="/path")`
- the app's basic layout and routing happens in `app.py`
- app is created and auth is built in `server.py`
- config is in `utilities/config.txt` and `utilities/config.py`

## Deploying to fly.io or Heroku

I've provided a `Procfile` for Heroku, there are many resources for Heroku deployment.

My preferred host is [Fly.io](https://fly.io). I've included a `Dockerfile`, `.dockerignore`, and `fly.toml` for an example.

```shell
# first time
fly launch

# after any change, deploy an updated version with
fly deploy
```
