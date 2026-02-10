const express = require('express');
const crypto = require('crypto');
const storeHash = require('./algorand');

const app = express();
app.use(express.json());

// test route
app.get('/', (req, res) => {
    res.send("SkillChain Backend Running");
});

// issue certificate
app.post('/issue', async (req, res) => {

    try {
        const { name, skill, issuer } = req.body;

        // combine certificate data
        const data = name + skill + issuer;

        // create fingerprint
        const hash = crypto.createHash('sha256')
            .update(data)
            .digest('hex');

        // send to blockchain
        const txId = await storeHash(hash);

        res.json({
            certificateHash: hash,
            transactionID: txId
        });

    } catch (error) {
        console.error(error);
        res.status(500).send("Error issuing certificate");
    }
});

app.listen(3000, () => console.log("Server started on port 3000"));

app.post("/verify", async (req, res) => {

  const { hash, creator, teammate } = req.body;

  try {

    // Combine verification data
    const verificationData = `${creator}:${teammate}:${hash}`;

    // Hash again for tamper-proof storage
    const verificationHash = crypto
      .createHash("sha256")
      .update(verificationData)
      .digest("hex");

    // Store on Algorand
    const txid = await storeHash(verificationHash);

    res.json({ txid });

  } catch (err) {

    console.error(err);
    res.status(500).json({ error: "Transaction failed" });

  }
});