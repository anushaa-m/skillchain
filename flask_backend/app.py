from flask import Flask, request, jsonify
import json, os
from hash_utils import generate_hash
import requests
from flask import render_template

app = Flask(__name__)

DB = "database.json"


def read_db():
    if not os.path.exists(DB):
        return []
    with open(DB) as f:
        return json.load(f)


def write_db(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=4)

def send_to_blockchain(hash_value, creator, teammate):

    url = "http://localhost:3000/verify"

    payload = {
        "hash": hash_value,
        "creator": creator,
        "teammate": teammate
    }

    try:
        res = requests.post(url, json=payload)
        return res.json()
    except:
        return {"error": "Blockchain server not running"}
    
# Health route
@app.route("/")
def home():
    return {"msg": "Flask backend running"}


# Create activity + upload certificate
@app.route("/create", methods=["POST"])
def create():

    file = request.files["certificate"]

    creator = request.form["creator_wallet"]
    teammate = request.form["teammate_wallet"]
    event = request.form["event"]

    hash_value = generate_hash(file)

    activity = {
        "id": len(read_db()) + 1,
        "creator_wallet": creator,
        "teammate_wallet": teammate,
        "event": event,
        "hash": hash_value,
        "txid": None,
        "status": "pending"
    }

    data = read_db()
    data.append(activity)
    write_db(data)

    return jsonify(activity)

@app.route("/verify/<int:id>", methods=["POST"])
def verify(id):

    data = read_db()

    for activity in data:

        if activity["id"] == id:

            result = send_to_blockchain(
                activity["hash"],
                activity["creator_wallet"],
                activity["teammate_wallet"]
            )

            # Store txid
            activity["txid"] = result.get("txid")
            activity["status"] = "verified"

    write_db(data)

    return {"msg": "Verification complete"}

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/form")
def form_page():
    return render_template("forms.html")


@app.route("/achievements")
def achievements():
    return render_template("achievements.html")