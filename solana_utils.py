import requests
import os
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.publickey import PublicKey

def check_new_pools(min_liquidity, known):
    try:
        response = requests.get("https://api.raydium.io/pairs")
        data = response.json()

        for pool in data:
            liquidity = float(pool.get('liquidity', 0))
            pool_id = pool.get('id')

            if liquidity >= min_liquidity and pool_id not in known:
                known.add(pool_id)
                return {
                    "symbol": pool.get('name'),
                    "address": pool_id,
                    "tokenA": pool.get('baseMint'),
                    "tokenB": pool.get('quoteMint')
                }
    except Exception as e:
        print("Erro ao buscar pools:", e)
    return None

def get_sol_price_usd():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd")
        return response.json()["solana"]["usd"]
    except:
        return 150

def execute_trade(pool):
    sol_price = get_sol_price_usd()
    sol_to_send = round(20 / sol_price, 5)

    client = Client("https://api.mainnet-beta.solana.com")
    private_key_str = os.getenv("PRIVATE_KEY")
    secret_key = [int(x) for x in private_key_str.strip("[]").split(",")]
    keypair = Keypair.from_secret_key(bytes(secret_key))

    receiver = PublicKey(pool["address"][:44])
    tx = Transaction()
    tx.add(
        transfer(
            TransferParams(
                from_pubkey=keypair.public_key,
                to_pubkey=receiver,
                lamports=int(sol_to_send * 1e9)
            )
        )
    )

    result = client.send_transaction(tx, keypair)
    return sol_to_send, result["result"]

def get_price_change(symbol, entry_price):
    import random
    return round(random.uniform(0.3, 3.5), 2)

def sell_token(pool):
    return "TX_SELL_REAL"