const algosdk = require('algosdk');

const account = algosdk.generateAccount();

console.log("YOUR ADDRESS:\n");
console.log(account.addr.toString());

console.log("\nYOUR 25 WORD MNEMONIC:\n");
console.log(algosdk.secretKeyToMnemonic(account.sk));
