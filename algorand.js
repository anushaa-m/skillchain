const algosdk = require("algosdk");
require("dotenv").config();


const algodClient = new algosdk.Algodv2(
  "",
  "https://testnet-api.algonode.cloud",
  ""
);


const mnemonic = process.env.MNEMONIC;

if (!mnemonic) {
  throw new Error("MNEMONIC missing in .env file");
}

const account = algosdk.mnemonicToSecretKey(mnemonic);


async function storeHash(hashData) {

  try {

    const params =
      await algodClient.getTransactionParams().do();


    const note = new TextEncoder().encode(hashData);

    const txn =
      algosdk.makePaymentTxnWithSuggestedParamsFromObject({
        from: account.addr,
        to: account.addr,
        amount: 0,
        note: note,
        suggestedParams: params
      });


    const signedTxn =
      txn.signTxn(account.sk);


    const tx =
      await algodClient
        .sendRawTransaction(signedTxn)
        .do();


    const txId = tx.txId;

    const explorerLink =
      `https://testnet.explorer.perawallet.app/tx/${txId}`;


    console.log("Transaction ID:", txId);
    console.log("Explorer:", explorerLink);


    return {
      txId,
      explorerLink
    };

  } catch (error) {

    console.error("Blockchain Error:", error);

    throw error;
  }
}

module.exports = storeHash;