import pyrebase
from key_db import config


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()


### PAYMENT
def check_user_payment(user_id):
    print("\n\n\n[DB] check_user_payment\n[DB] user_id: " + user_id + "\n\n\n")
    return database.child("users").child(user_id).get().val()["paid"]

def create_user(user_id, paid):
    print("\n\n\n[DB] create_user\n[DB] user_id: " + user_id + "\n[DB] paid: " + str(paid) + "\n\n\n")
    database.child("users").child(user_id).set({"paid": paid})

def update_user(user_id, paid):
    print("\n\n\n[DB] update_user\n[DB] user_id: " + user_id + "\n[DB] paid: " + str(paid) + "\n\n\n")
    database.child("users").child(user_id).update({"paid": paid})


### AUTH
def sign_up(email, password):
    print("\n\n\n[DB] sign_up\n[DB] email: " + email + "\n[DB] password: " + password + "\n\n\n")
    return auth.create_user_with_email_and_password(email, password)

def sign_in(email, password):
    print("\n\n\n[DB] sign_in\n[DB] email: " + email + "\n[DB] password: " + password + "\n\n\n")
    return auth.sign_in_with_email_and_password(email, password)
