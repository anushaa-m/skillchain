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


def send_to_blockchain(hash_value):

    url = "http://127.0.0.1:3000/issue"

    payload = {
        "hash": hash_value
    }

    try:
        print("Sending to blockchain:", payload)

        res = requests.post(url, json=payload, timeout=30)
        
        print("STATUS:", res.status_code)
        print("NODE RESPONSE:", res.text)
        
        data= res.json()
        
        print("PARSED JSON:", data)
        
        return data

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

    # create record FIRST
    achievement = {
        "id": len(db["achievements"]) + 1,
        "event": event,
        "hash": hash_value,
        "txid": None,
        "status": "pending"
    }

    db["achievements"].append(achievement)
    write_db(db)

    # SEND TO BLOCKCHAIN
    result = send_to_blockchain(hash_value)

    # RELOAD DB FROM FILE (CRITICAL)
    db = read_db()

    # update the ACTUAL stored record
    for a in db["achievements"]:
        if a["hash"] == hash_value:
            a["txid"] = result.get("transactionID")
            a["status"] = "verified"

    write_db(db)

    return redirect(url_for("achievements_page"))


@app.route("/verify", methods=["GET", "POST"])
def verify_page():

    # when user opens the page
    if request.method == "GET":
        return render_template("verify.html")

    # when user uploads certificate
    file = request.files.get("certificate")
    if not file or file.filename == "":
        return "<h2 style='color:red;text-align:center;'>No file uploaded</h2>"

    uploaded_hash = generate_hash(file)
    print("UPLOADED HASH:", uploaded_hash)

    db = read_db()

    for achievement in db["achievements"]:
        if achievement["hash"] == uploaded_hash:
            return f"""
            <div style="text-align:center;margin-top:80px;font-family:sans-serif;">
            <h1 style="color:#00ff88;">✓ CERTIFICATE VERIFIED</h1>
            <p>This certificate exists on SkillChain blockchain.</p>
            <p><b>Transaction ID:</b></p>
            <p style="word-wrap:break-word;width:70%;margin:auto;">{achievement['txid']}</p>
            </div>
            """


    return """
    <h2 style='color:red;text-align:center;margin-top:40px;'>
    NOT VERIFIED  <br>
    Certificate does not exist on SkillChain
    </h2>
    """



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