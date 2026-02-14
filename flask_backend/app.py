from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import os
import requests
from hash_utils import generate_hash

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "database.json")


def read_db():
    if not os.path.exists(DB):
        data = {"users": [], "achievements": []}
        with open(DB, "w") as f:
            json.dump(data, f, indent=4)
        return data

    # file exists but might be empty/corrupt
    try:
        with open(DB, "r") as f:
            return json.load(f)
    except:
        data = {"users": [], "achievements": []}
        with open(DB, "w") as f:
            json.dump(data, f, indent=4)
        return data





def write_db(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=4)


def send_to_blockchain(hash_value, creator, teammate, event):

    url = "http://127.0.0.1:3000/issue"

    payload = {
        "name": creator,
        "skill": event,
        "issuer": teammate
    }

    try:
        print("Sending to blockchain:", payload)

        res = requests.post(url, json=payload, timeout=30)

        print("NODE RESPONSE:", res.text)

        return res.json()

    except requests.exceptions.ConnectionError:
        print("Node server is not running!")
        return {"transactionID": None}

    except Exception as e:
        print("BLOCKCHAIN ERROR:", e)
        return {"transactionID": None}



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

    # 🔥 SEND TO BLOCKCHAIN IMMEDIATELY
    result = send_to_blockchain(
        hash_value,
        "Student",
        "SkillChain",
        event
    )

    # 🔥 STORE TXID
    db = read_db()
    db["achievements"][-1]["txid"] = result.get("transactionID")
    db["achievements"][-1]["status"] = "verified"
    write_db(db)

    return redirect(url_for("achievements_page"))



@app.route("/verify/<int:id>", methods=["POST"])
def verify(id):
    db = read_db()

    for achievement in db["achievements"]:
        if achievement["id"] == id:

            result=send_to_blockchain(
                achievement["hash"],
                "Student",
                "SkillChain",
                achievement["event"]
                
            )
            

            achievement["txid"] = result.get("transactionID")
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