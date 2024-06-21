from flask import Flask, request, jsonify, render_template, redirect, session, url_for, send_from_directory
from generate import generate_feature_request
import json
import os
import stripe
import db
from key_db import config



app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.environ["FLASK_SECRET_KEY"]




### STRIPE KEYS
stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
    "endpoint_secret": os.environ["STRIPE_ENDPOINT_SECRET"],
}
stripe.api_key = stripe_keys["secret_key"]









### MAIN APP ROUTES
@app.route("/")
def landing():
    try:
        return render_template("landing.html", signed_in=session["uid"], payed=db.check_user_payment(session["uid"]))
    except KeyError:
        return render_template("landing.html", signed_in=False, payed=False)


@app.route("/generate", methods=["GET", "POST"])
def generate():
    try:
        if db.check_user_payment(session["uid"]) == None:
            return redirect("/")
    except:
        return redirect("/")

    if request.method == "POST":
        description = request.form.get("description")
        features = json.dumps(request.form.get("features"))
        feature_number = request.form.get("feature-number")
        print(description, features, feature_number)
        output = generate_feature_request(description, features, feature_number)
        return render_template("generate.html", output=output)
    return render_template("generate.html")















### ACCOUNT ROUTES
@app.route("/login", methods=["POST", "GET"])
def login():
    error = request.args.get("error")
    if session.get("uid"):
        return redirect("/")
    return render_template("login.html", firebase_config=config, error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/delete_account")
def delete_account():
    try:
        db.delete_user(session["id_token"])
    except:
        session.clear()
        return redirect("/login?error=credential_too_old")
    session.clear()
    return redirect("/")


@app.route("/token-signin", methods=["POST"])
def token_signin():
    id_token = request.form["idToken"]
    decoded_token = db.decode_token(id_token)["user_id"]
    session["uid"] = decoded_token
    session["id_token"] = id_token
    return redirect("/generate")


















### STRIPE
@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


@app.route("/create-checkout-session")
def create_checkout_session():
    stripe.api_key = stripe_keys["secret_key"]

    try:
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=session["uid"],
            success_url=request.host_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.referrer,
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": "BuildRadar One-Time Payment",
                        },
                        "unit_amount": 100,
                    },
                    "quantity": 1,
                }
            ]
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )
    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400
    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session_with_user = event["data"]["object"]
        user_id = session_with_user.get("client_reference_id")
        db.update_payment(user_id, True)
    return "Success", 200


@app.route("/success")
def success():
    return redirect("/?success=true")