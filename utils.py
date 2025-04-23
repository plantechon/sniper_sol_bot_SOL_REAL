
import requests
import os
from telegram_notify import notify

def get_new_tokens():
    api_key = os.getenv("HELIUS_API_KEY")
    res = requests.get("https://public-api.birdeye.so/public/pairs", headers={"X-API-KEY": api_key})
    res_json = res.json()
    if "data" not in res_json:
        notify(f"❌ ERRO: resposta inesperada da API Birdeye: {res_json}")
        return []
    data = res_json["data"]
    return [
        {
            "symbol": p["baseToken"]["symbol"],
            "mint": p["baseToken"]["address"],
            "lpAddress": p.get("lpAddress", ""),
            "liquidity_locked": True
        }
        for p in data[:5]
    ]
