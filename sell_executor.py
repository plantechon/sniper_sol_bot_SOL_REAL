
import time
from telegram_notify import notify
import os
import requests

def get_price(mint):
    api_key = os.getenv("HELIUS_API_KEY")
    url = f"https://public-api.birdeye.so/public/price?address={mint}"
    headers = {"X-API-KEY": api_key}
    res = requests.get(url, headers=headers)
    return float(res.json()["data"]["value"])

def monitor_and_sell(token, entry_price):
    tp = entry_price * (1 + int(os.getenv("TP_PERCENT", 300)) / 100)
    sl = entry_price * (1 - int(os.getenv("SL_PERCENT", 50)) / 100)
    for _ in range(30):
        price = get_price(token["mint"])
        if price >= tp:
            notify(f"🚀 VENDA TP: {token['symbol']} | Preço: {price:.4f}")
            return
        if price <= sl:
            notify(f"🔻 VENDA SL: {token['symbol']} | Preço: {price:.4f}")
            return
        time.sleep(10)
