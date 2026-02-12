from flask import Flask, request, jsonify, render_template
import json
import os
import requests
from hash_utils import generate_hash

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "database.json")


def read_db():
    if not os.path.exists(DB):
        return {"users": [], "achievements": []}

    with open(DB, "r") as f:
        return json.load(f)


def write_db(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=4)


def send_to_blockchain(hash_value, event):
    url = "http://localhost:3000/issue"

    payload = {
        "hash": hash_value,
        "event": event
    }

    try:
        res = requests.post(url, json=payload)
        return res.json()
    except Exception:
        return {"error": "Blockchain server not running"}


@app.route("/")
def home():
    return {"msg": "Flask backend running"}


@app.route("/create_user", methods=["POST"])
def create_user():
    db = read_db()

    user = {
        "id": len(db["users"]) + 1,
        "name": request.form["name"],
        "email": request.form["email"],
        "number": request.form["number"],
        "branch": request.form["branch"],
        "year": request.form["year"]
    }

    db["users"].append(user)
    write_db(db)

    return jsonify(user)


@app.route("/create_achievement", methods=["POST"])
def create_achievement():
    db = read_db()

    file = request.files["certificate"]
    event = request.form["event"]

    hash_value = generate_hash(file)

    achievement = {
        "id": len(db["achievements"]) + 1,
        "event": event,
        "hash": hash_value,
        "txid": None,
        "status": "pending"
    }

    db["achievements"].append(achievement)
    write_db(db)

    return jsonify(achievement)


@app.route("/verify/<int:id>", methods=["POST"])
def verify(id):
    db = read_db()

    for achievement in db["achievements"]:
        if achievement["id"] == id:

            result = send_to_blockchain(
                achievement["hash"],
                achievement["event"]
            )

            achievement["txid"] = result.get("txid")
            achievement["status"] = "verified"

    write_db(db)

    return {"msg": "Verification complete"}


@app.route("/form")
def form_page():
    return render_template("form.html")


@app.route("/achievements")
def achievements_page():
    return render_template("achievements.html")


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


if __name__ == "__main__":
    app.run(debug=True)