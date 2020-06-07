# dash-auth-flow
Batteries-included authentication flow in [Dash](dash.plot.ly).

This has landing pages and functions to run the entire authentication flow:
- home
- login
- logout
- register
- forgot password
- change password

This uses `flask-login` on the backend, using some code from the very useful [dash-flask-login](https://github.com/RafaelMiquelino/dash-flask-login). Data is held in `users.db`. 

```bash
pip install pipenv
pipenv install --ignore-pipfile
pipenv shell
python create_tables.py # test@test.com / test
python app.py
```

![](example.gif)

---

Notes:

- this uses MailJet as the email API. You need a [free MailJet API key](https://www.mailjet.com/email-api/)
- your send-from email and API key/secret need to be entered in `config/keys.py`
- if you want to use something else, change the `send_password_key` function in `utilities/auth.py`
- add pages in `pages/`.
- the app's basic layout and routing happens in `app.py`
- app is created and auth is built in `server.py`
- config is in `utilities/config.txt` and `utilities/config.py`
