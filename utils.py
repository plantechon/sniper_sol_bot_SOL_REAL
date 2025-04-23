
import requests
import os
from telegram_notify import notify

def get_new_tokens():
    api_key = os.getenv("HELIUS_API_KEY")
    headers = {"X-API-KEY": api_key}
    try:
        res = requests.get("https://public-api.birdeye.so/public/pairs", headers=headers)
        res_json = res.json()
        if not res_json.get("success") or "data" not in res_json:
            notify(f"⚠️ API fallback: resposta inesperada Birdeye - {res_json}")
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
    except Exception as e:
        notify(f"❌ ERRO crítico Birdeye: {str(e)}")
        return []
