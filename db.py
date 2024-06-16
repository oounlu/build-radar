from key_db import config
import firebase


### FIREBASE-REST_API
app = firebase.initialize_app(config)
auth = app.auth()
users = app.database()


### PAYMENT
def check_user_payment(uid):
    print("\n\n\n[DB] check_user_payment\n[DB] uid: " + uid + "\n\n\n")
    return users.child(uid).child("paid").get().val()

def update_payment(uid, paid):
    print("\n\n\n[DB] update_payment\n[DB] uid: " + uid + "\n[DB] paid: " + str(paid) + "\n\n\n")
    users.child(uid).update({"paid": paid})


### AUTH
def decode_token(id_token):
    print(auth.verify_id_token(id_token))
    return auth.verify_id_token(id_token)

def delete_user(id_token):
    uid = decode_token(id_token)["user_id"]
    print("\n\n\n[DB] delete_user\n[DB] uid: " + uid + "\n\n\n")
    auth.delete_user_account(id_token)
    try:
        users.child(uid).remove()
    except:
        pass
