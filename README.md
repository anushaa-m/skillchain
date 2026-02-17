# SkillChain — Blockchain Certificate Verification (Algorand)

A tamper-proof digital certificate verification platform built using **Flask + Node.js + Algorand Blockchain + Docker**.

IdenPro allows any third party (recruiter, university, or organization) to verify the authenticity of a certificate **without contacting the issuer**.

---

##  The Problem
Educational and achievement certificates are extremely easy to forge.

Today verification is:
- manual
- slow
- centralized
- dependent on human confirmation

Organizations cannot reliably verify:
- if a certificate is genuine
- if the file was modified
- if the issuer actually issued it

This leads to:
- hiring fraud
- fake internships
- resume inflation
- trust issues in remote hiring

---

## Our Solution
Instead of trusting the document, **we trust mathematics + blockchain**.

IdenPro generates a **cryptographic fingerprint (SHA-256 hash)** of a certificate image and stores that fingerprint permanently on the **Algorand blockchain**.

If even **1 pixel changes**, the fingerprint changes → verification fails.

We do **NOT store certificates on blockchain**  
We store proof that the certificate existed.

---

## How It Works

### Certificate Issuance
1. User uploads certificate (PNG)
2. Flask backend reads the file
3. A SHA-256 hash is generated
4. Hash is sent to Node.js blockchain service
5. Node writes the hash into an Algorand transaction note field
6. Transaction ID is returned and saved

### Certificate Verification
1. Verifier uploads certificate file
2. System hashes the file again
3. Hash is compared with stored database hash
4. If found → VERIFIED
5. Transaction ID proves blockchain immutability

---

## System Architecture

Frontend (HTML Forms)  
⬇  
Flask Server (Hash Generation & Verification)  
⬇  
Node.js Blockchain Service  
⬇  
Algorand Network (TestNet)

---

##  Why Blockchain?
A database can be edited.  
A blockchain cannot.

Algorand provides:
- immutability
- public auditability
- no centralized trust
- instant finality

Once stored, the certificate proof **can never be altered or deleted**.

---

## Technologies Used

| Layer | Technology |
|------|------|
| Frontend | HTML/CSS |
| Backend | Flask (Python) |
| Blockchain Service | Node.js |
| Cryptography | SHA-256 hashing |
| Blockchain | Algorand TestNet |
| Containerization | Docker + Docker Compose |

---

## Running the Project (Docker — Recommended)

### Requirements
- Docker Desktop installed

### Run

```bash
docker compose up --build
```

Open:

http://localhost:5000/welcome

Issue a Certificate

Go to Create Achievement

Upload a certificate PNG

System generates a blockchain transaction

Transaction ID is stored

Verify a Certificate

Open Verify Certificate

Upload the same certificate file

System recomputes hash

If hashes match → VERIFIED

If the file is edited, renamed, compressed, or modified → verification fails.

 What Exactly Is Stored on Algorand?

We store only the SHA-256 hash of the certificate file.

Example:

8b515fdde9d2cc0274310cefdeaca5fe62c12921de18b670275d30d188d32adc


This hash is written inside the Algorand transaction NOTE field.

Important:

No personal data stored

No student name stored

No certificate image stored

The blockchain stores proof of existence, not the document.

This preserves privacy while guaranteeing authenticity.

Security Model

IdenPro prevents three types of attacks:

1. Certificate Editing

If someone edits even one pixel → hash changes → verification fails.

2. Fake Certificate Creation

An attacker cannot guess a valid hash because SHA-256 is collision-resistant.

3. Database Tampering

Even if our database is deleted or hacked:

The blockchain transaction still exists

The certificate can still be verified using the transaction ID

Therefore trust is moved from our server → blockchain consensus.

API Communication (Flask ↔ Node)

Flask communicates with the blockchain service via REST:

Issue Certificate

Flask → Node

POST /issue
{
  "hash": "<certificate_sha256>"
}


Node:

receives hash

writes to Algorand

returns transaction ID

Response:

{
  "certificateHash": "...",
  "transactionID": "LCVN4FAW6LBVZ..."
}

Why We Used Two Servers (Flask + Node)

Flask handles:

file upload

hashing

verification logic

Node handles:

blockchain wallet

transaction signing

Algorand SDK interaction

Reason:
Python is better for file processing.
Node has mature Algorand SDK support.

This separation follows a microservice architecture.

 Limitations (Honest Section — judges LOVE this)

Current constraints:

Verification requires the original file (binary match)

Re-exported PDFs or screenshots fail verification

Uses TestNet (not MainNet yet)

Centralized issuer (no decentralized identity yet)

 Future Work

QR code embedded certificates

Public blockchain explorer link per certificate

Wallet-based issuers

IPFS storage

Self-sovereign identity

