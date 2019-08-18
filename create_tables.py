from utilities.config import engine
from utilities.auth import (
    User,
    PasswordChange,
    add_user,
    change_user,
    del_user,
    show_users,
    user_exists
)


# engine is open to sqlite///users.db

def create_user_table(model,engine):
    model.metadata.create_all(engine)

def create_password_change_table(model,engine):
    model.metadata.create_all(engine)


# create the tables
create_user_table(User,engine)
create_password_change_table(PasswordChange,engine)


# add a test user to the database
first = 'test'
last = 'test'
email = 'test@test.com'
password = 'test'
add_user(first,last,password,email,engine)


# show that the users exists
show_users(engine)

# confirm that user exists
print(user_exists(email,engine))


