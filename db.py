import pyrebase
from key_db import config

import firebase_admin
from firebase_admin import credentials, firestore


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

cred = credentials.Certificate("key_db.json")
firebase_admin.initialize_app(cred)
database = firestore.client()
users = database.collection("users")



### PAYMENT (firebase_admin)
def check_user_payment(user_id):
    print("\n\n\n[DB] check_user_payment\n[DB] user_id: " + user_id + "\n\n\n")
    return users.document(user_id).get().to_dict()["paid"]

def create_user(user_id, paid):
    print("\n\n\n[DB] create_user\n[DB] user_id: " + user_id + "\n[DB] paid: " + str(paid) + "\n\n\n")
    users.document(user_id).set({"paid": paid})

def update_user(user_id, paid):
    print("\n\n\n[DB] update_user\n[DB] user_id: " + user_id + "\n[DB] paid: " + str(paid) + "\n\n\n")
    users.document(user_id).update({"paid": paid})


### AUTH (pyrebase)
def sign_up(email, password):
    print("\n\n\n[DB] sign_up\n[DB] email: " + email + "\n[DB] password: " + password + "\n\n\n")
    uid = auth.create_user_with_email_and_password(email, password)["localId"]
    create_user(uid, False)
    return uid


def sign_in(email, password):
    print("\n\n\n[DB] sign_in\n[DB] email: " + email + "\n[DB] password: " + password + "\n\n\n")
    return auth.sign_in_with_email_and_password(email, password)["localId"]
