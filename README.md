# SkillChain — Blockchain Certificate Verification System

> ⚠️ IMPORTANT FOR JUDGES
> The stable working version of this project is **NOT in the `main` branch**.
> Please switch to the branch:

## 👉 `integration-safe-backup`

All integrated functionality (Flask + Blockchain) is located there.

Direct link:
https://github.com/anushaa-m/skillchain/tree/integration-safe-backup

---

## Problem Statement

Many student clubs, hackathons, and small organizations issue certificates that are easy to forge because verification depends on manual checking.

SkillChain solves this by storing a **cryptographic fingerprint (hash) of the certificate on the Algorand blockchain**.
Anyone can verify authenticity without contacting the issuer.

---

## What the System Does

Workflow:

1. User uploads certificate (PNG)
2. Flask backend generates SHA-256 hash
3. Hash is saved in local database
4. Verification endpoint sends hash to Node backend
5. Node backend writes hash onto Algorand TestNet
6. Transaction ID acts as a permanent public proof

The blockchain never stores the actual certificate — only its hash.

This ensures:

* privacy
* immutability
* tamper detection

---

## Architecture

HTML Form → Flask API → Local Database → Node Server → Algorand Blockchain

**Tech Stack**

* Python Flask (API + hashing)
* Node.js (Algorand SDK transaction writer)
* Algorand TestNet
* SHA-256 cryptographic hashing

---

## How Verification Works

If someone edits even **one pixel** of a certificate:

the hash changes → blockchain mismatch → certificate is fake.

This provides trustless verification.

---

## Running the Project (3 minutes)

### 1️⃣ Start Blockchain Server

```bash
cd skillchain-main
npm install
node server.js
```

You should see:

```
REAL WALLET ADDRESS: XXXXX
Server started on port 3000
```

---

### 2️⃣ Start Flask Backend

Open a new terminal:

```bash
cd skillchain-main/flask_backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Runs on:

```
http://127.0.0.1:5000
```

---

### 3️⃣ Trigger Blockchain Verification

In another terminal:

```bash
curl -X POST http://127.0.0.1:5000/verify/1
```

This writes the certificate hash to Algorand.

---

## What to Look For

When verification runs:

Node terminal prints:

```
Transaction submitted to network. TXID: XXXXX
```

This TXID is the public proof of certificate authenticity.

---

## Key Innovation

Instead of storing certificates (large files) on chain, SkillChain stores **cryptographic evidence**.

This:

* drastically reduces cost
* increases speed
* preserves privacy
* enables public verification

---

## Future Scope

* QR code verification
* Public verification portal
* Multi-issuer dashboards
* Integration with universities

---

## Note

The `main` branch contains intermediate commits during team development and may not run correctly.
The fully integrated implementation is available in **integration-safe-backup**.
