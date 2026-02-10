require('dotenv').config();
const algosdk = require('algosdk');

// connect to Algorand TestNet (backup public node)
const algodClient = new algosdk.Algodv2(
    '',
    'https://testnet-api.algonode.network',
    ''
);

// load wallet from mnemonic
const mnemonic = process.env.MNEMONIC;

if (!mnemonic) {
    throw new Error("Mnemonic not found in .env file");
}

const account = algosdk.mnemonicToSecretKey(mnemonic);
// convert public key to readable Algorand address
const senderAddress = account.addr.toString();

console.log("REAL WALLET ADDRESS:", senderAddress);

// function to store certificate hash on blockchain
async function storeHash(hash) {
    // get blockchain params
    const suggestedParams = await algodClient.getTransactionParams().do();
    suggestedParams.fee = 1000;
    suggestedParams.flatFee = true;

    // NOTE FIELD (THIS IS WHERE WE STORE THE HASH)
    const note = new TextEncoder().encode(hash);

    // IMPORTANT: sending 0 ALGO to self, only storing note
    const txn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
        sender: senderAddress,
        receiver: senderAddress,
        amount: 0,
        note: note,
        suggestedParams: suggestedParams
    });

    // sign transaction
    const signedTxn = txn.signTxn(account.sk);

    // send to blockchain
    const response = await algodClient.sendRawTransaction(signedTxn).do();
    const txId = response.txid;

    // wait for confirmation
    console.log("Transaction submitted to network. TXID:", txId);
    return txId;
}

module.exports = { storeHash };
