const algosdk = require('algosdk');

// connect to Algorand testnet
const algodClient = new algosdk.Algodv2(
    '',
    'https://testnet-api.algonode.cloud',
    ''
);

// IMPORTANT: paste your 25-word mnemonic here
require('dotenv').config();
const mnemonic = process.env.MNEMONIC;


const account = algosdk.mnemonicToSecretKey(mnemonic);

async function storeHash(hash) {

    // get network parameters
    const params = await algodClient.getTransactionParams().do();

    // encode hash into transaction note
    const note = new TextEncoder().encode(hash);

    // create 0 Algo transaction to yourself
    const txn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
        from: account.addr,
        to: account.addr,
        amount: 0,
        note: note,
        suggestedParams: params
    });

    // sign transaction
    const signedTxn = txn.signTxn(account.sk);

    // send to blockchain
    const tx = await algodClient.sendRawTransaction(signedTxn).do();

    return tx.txId;
}

module.exports = storeHash;
