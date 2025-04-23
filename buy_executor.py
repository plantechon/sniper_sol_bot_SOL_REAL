
import requests
import base64
from solders.transaction import Transaction
from solders.keypair import Keypair
from solana.rpc.api import Client
import os
import json
import ast

def get_sol_price():
    res = requests.get("https://public-api.birdeye.so/public/price?address=So11111111111111111111111111111111111111112",
                       headers={"X-API-KEY": os.getenv("HELIUS_API_KEY")})
    return float(res.json()["data"]["value"])

def buy_token(token):
    keypair = Keypair.from_bytes(bytes(ast.literal_eval(os.getenv("SOLANA_PRIVATE_KEY"))))
    rpc = Client(os.getenv("RPC_URL"))
    sol_price = get_sol_price()
    usd_to_sol = 20 / sol_price
    amount_lamports = int(usd_to_sol * 1e9)

    payload = {
        "inputMint": "So11111111111111111111111111111111111111112",
        "outputMint": token["mint"],
        "amount": amount_lamports,
        "slippageBps": 500,
        "userPublicKey": str(keypair.pubkey())
    }
    res = requests.post("https://quote-api.jup.ag/v6/swap", json=payload)
    swap_tx = base64.b64decode(res.json()["swapTransaction"])

    tx = Transaction.from_bytes(swap_tx)
    tx.sign([keypair])
    txid = rpc.send_transaction(tx, keypair)["result"]
    return txid, round(usd_to_sol, 4)
