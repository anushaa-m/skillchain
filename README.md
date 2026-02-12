# SkillChain — Blockchain Certificate Verification System

## ⚠️ IMPORTANT FOR JUDGES / REVIEWERS

**Please evaluate the project using the `integration-safe-backup` branch.**

The `main` branch contains experimental frontend commits and is not the stable build.

The fully working integrated system (Flask + Node + Algorand blockchain pipeline) is present in:

➡ **integration-safe-backup**

This branch contains the stable implementation.

---

## 🧠 Problem

Educational certificates and achievements are easy to fake because verification today is manual, slow, and centralized.

Recruiters and organizations cannot easily confirm:

* whether a certificate is genuine
* whether it has been tampered with
* whether the issuer actually issued it

This leads to:

* hiring fraud
* resume inflation
* trust issues in hackathons and remote hiring

---

## 💡 Our Solution — SkillChain

SkillChain stores a **cryptographic fingerprint (hash)** of a certificate on the **Algorand blockchain**.

Instead of trusting a PDF or image, the verifier trusts the blockchain.

If the certificate is modified even by 1 pixel → the hash changes → verification fails.

We do NOT store certificates on the blockchain.
We store proof that the certificate existed.

This makes certificates:

* tamper-proof
* verifiable
* permanent
* publicly auditable

---

## 🏗️ System Architecture

User Uploads Certificate (PNG)
↓
Flask Backend
↓ (SHA-256 hashing)
Certificate Hash
↓
Node.js Blockchain Service
↓
Algorand TestNet Transaction (note field)
↓
Transaction ID stored
↓
Anyone can verify using blockchain explorer

---

## 🔗 What is stored on blockchain?

Stored:

* SHA-256 hash of the certificate

Not stored:

* the image
* personal data
* private information

So the system remains privacy-safe.

---

## 🛠️ Tech Stack

Frontend — HTML + Flask templates
Backend API — Python Flask
Hashing — Python SHA-256
Blockchain Service — Node.js (algosdk)
Blockchain — Algorand TestNet
Database — JSON database

---

## ⚙️ Workflow

### Step 1 — Upload

User uploads a certificate (PNG).

### Step 2 — Hashing

Flask converts the file into SHA-256 hash.

Example:
certificate.png → SHA256 → ea3c34d6df10db535ddfeb5a3417be6fadbcc553574684a4c829c1e9d6555bef

### Step 3 — Blockchain Storage

The hash is written into the Algorand transaction NOTE field.

### Step 4 — Verification

Verifier checks:

* transaction exists
* hash matches certificate

If match → certificate is genuine.

---

## ▶️ How to Run

### Start Blockchain Server

From project root:

node server.js

Expected:
REAL WALLET ADDRESS: XXXXX
Server started on port 3000

---

### Start Flask Backend

cd flask_backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python app.py

Backend runs at:
http://127.0.0.1:5000

---

### Test Verification

curl -X POST http://127.0.0.1:5000/verify/1

If successful → blockchain transaction is created.

---

## 🔐 Why Blockchain?

Traditional database:

* editable
* requires trust in admin

Blockchain:

* immutable
* public
* tamper-proof
* independently verifiable

We replace institutional trust with cryptographic proof.

---

## 🚀 Current Status

✔ Certificate hashing
✔ Blockchain transaction creation
✔ Transaction ID generation
✔ Flask → Node → Algorand pipeline working

---

## 📌 Future Improvements

* QR code verification
* Issuer authentication
* Recruiter verification portal
* NFT-based certificates
* IPFS storage

---

## 👥 Team
Team Lead: Anusha Malhotra(blockchain & backend integration)
Saloni Tiwari(backend)
Rachana Wagh( frontend and documentation)
Anushree Chatur(frontend)


---

## 🧾 Final Note

This project demonstrates a real blockchain verification pipeline:

Certificate → Hash → Blockchain Transaction → Public Verification

The blockchain transaction itself becomes the permanent proof of authenticity.

## 🔎 Live Blockchain Proof (Working Transaction)

The system successfully wrote a certificate hash to the Algorand TestNet.

**Transaction ID:**

GLHJHLWTVTRXGMFIMW7NQS357KH2CET6JWFQPYNBMXW7SGUUDLLA

What this proves:

* Backend hashing works
* Node blockchain service works
* Algorand transaction submission works
* Verification pipeline works

To verify:

1. Open Algorand TestNet Explorer (Lora Explorer)
2. Search the above Transaction ID
3. Open the transaction
4. Check the NOTE field (Base64)

The NOTE field contains the certificate hash written by SkillChain.

This transaction acts as permanent public proof that the certificate existed at the time of issuance.
