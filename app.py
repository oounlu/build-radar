from flask import Flask, request, jsonify, render_template, redirect, session
from generate import generate_feature_request
import json
import os
import stripe
import db



app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "2689"

DOMAIN_URL = os.environ["DOMAIN_URL"]



### STRIPE
stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
    "endpoint_secret": os.environ["STRIPE_ENDPOINT_SECRET"],
}
stripe.api_key = stripe_keys["secret_key"]


@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


@app.route("/create-checkout-session")
def create_checkout_session():
    stripe.api_key = stripe_keys["secret_key"]

    try:
        checkout_session = stripe.checkout.Session.create(
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
        user_id = event["id"]
        db.create_user(user_id, True)
        # TODO

    return "Success", 200







### STRIPE RESPONSE
@app.route("/success")
def success():
    return redirect("/?success=true")

@app.route("/cancel")
def cancel():
    return redirect("/?success=false")









### ROUTES
@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")


@app.route("/index", methods=["GET", "POST"])
def generate():
    has_paid = db.check_user_payment_status() # TODO
    print(has_paid)

    success = request.args.get("success", "none")

    if request.method == "POST":
        description = request.form.get("description")
        features = json.dumps([request.form.get("feature-1"), request.form.get("feature-2"), request.form.get("feature-3")], indent=4)
        output = generate_feature_request(description, features, request.form.get("feature-number"))

        return render_template("index.html", output=output, success=success)

    return render_template("index.html", success="true")
