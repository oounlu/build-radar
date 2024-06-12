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



### STRIPE KEYS
stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
    "endpoint_secret": os.environ["STRIPE_ENDPOINT_SECRET"],
}
stripe.api_key = stripe_keys["secret_key"]

















### ROUTES
@app.route("/")
def landing():
    try:
        return render_template("landing.html", signed_in=bool(session.get("uid")), payed=db.check_user_payment(session["uid"]))
    except:
        return render_template("landing.html", signed_in=False, payed=False)

 
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            uid = db.sign_in(email, password)
            session["uid"] = uid
            return redirect("/")
        except:
            return redirect("/login?error=true")

    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            uid = db.sign_up(email, password)
            session["uid"] = uid
            return redirect("/")
        except Exception as e:
            print(e)
            return redirect("/signup?error=true")

    return render_template("signup.html")


@app.route("/index", methods=["GET", "POST"])
def generate():
    has_paid = db.check_user_payment(session["uid"])

    if not has_paid:
        return redirect("/")

    success = request.args.get("success", "none")

    if request.method == "POST":
        description = request.form.get("description")
        features = json.dumps() # TODO: fetch the features dynamically
        output = generate_feature_request(description, features, request.form.get("feature-number"))

        return render_template("index.html", output=output, success=success)

    return render_template("index.html", success="true")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
























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
        db.update_user(user_id, True)

    return "Success", 200


@app.route("/success")
def success():
    return redirect("/?success=true")