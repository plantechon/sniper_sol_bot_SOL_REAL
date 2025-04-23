
import requests
import os

def is_liquidity_locked(token):
    pool_address = token.get("lpAddress")
    api_key = os.getenv("HELIUS_API_KEY")
    url = f"https://api.helius.xyz/v0/addresses/{pool_address}/tokens?api-key={api_key}"
    res = requests.get(url)
    return "locked" in res.text.lower()
