
import requests
import os

def get_new_tokens():
    api_key = os.getenv("HELIUS_API_KEY")
    res = requests.get("https://public-api.birdeye.so/public/pairs", headers={"X-API-KEY": api_key})
    data = res.json()["data"]
    return [
        {
            "symbol": p["baseToken"]["symbol"],
            "mint": p["baseToken"]["address"],
            "lpAddress": p.get("lpAddress", ""),
            "liquidity_locked": True
        }
        for p in data[:5]
    ]
