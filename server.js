global.fetch = require('node-fetch');
const express = require('express');
const crypto = require('crypto');
const { storeHash } = require('./algorand');

const app = express();
app.use(express.json());

// test route
app.get('/', (req, res) => {
    res.send("SkillChain Backend Running");
});

// issue certificate
// issue certificate (store fingerprint on blockchain)
app.post('/issue', async (req, res) => {
    try {

        const { hash } = req.body;

        if (!hash) {
            return res.status(400).json({ error: "No hash provided" });
        }

        console.log("Received certificate hash from Flask:", hash);

        // store SAME hash on blockchain
        const txId = await storeHash(hash);

        console.log("Transaction ID:", txId);

        res.json({
            certificateHash: hash,
            transactionID: txId
        });

    } catch (error) {
        console.error("BLOCKCHAIN ERROR BELOW ↓↓↓↓↓");
        console.error(error);

        res.status(500).json({
            error: error.message
        });
    }
});


app.listen(3000, () => console.log("Server started on port 3000"));