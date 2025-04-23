
import time
from telegram_notify import notify
import os
import requests
from buy_executor import get_sol_price

def get_price(mint):
    api_key = os.getenv("HELIUS_API_KEY")
    url = f"https://public-api.birdeye.so/public/price?address={mint}"
    headers = {"X-API-KEY": api_key}
    res = requests.get(url, headers=headers)
    return float(res.json()["data"]["value"])

def monitor_and_sell(token, entry_price):
    sol_price = get_sol_price()
    tp = entry_price * (1 + int(os.getenv("TP_PERCENT", 300)) / 100)
    sl = entry_price * (1 - int(os.getenv("SL_PERCENT", 50)) / 100)
    
    for _ in range(30):
        price = get_price(token["mint"])
        if price >= tp:
            lucro_pct = ((price - entry_price) / entry_price) * 100
            notify(
                f"💰 *SAÍDA COM LUCRO*
"
                f"Token: [`{token['symbol']}`](https://solscan.io/token/{token['mint']})
"
                f"Entrada: `{entry_price:.6f} SOL` (~${entry_price * sol_price:.2f})
"
                f"Saída: `{price:.6f} SOL` (~${price * sol_price:.2f})
"
                f"Lucro: *+{lucro_pct:.2f}%*",
                parse_mode="Markdown"
            )
            return
        if price <= sl:
            perda_pct = ((entry_price - price) / entry_price) * 100
            notify(
                f"🔻 *SAÍDA COM PREJUÍZO*
"
                f"Token: [`{token['symbol']}`](https://solscan.io/token/{token['mint']})
"
                f"Entrada: `{entry_price:.6f} SOL` (~${entry_price * sol_price:.2f})
"
                f"Saída: `{price:.6f} SOL` (~${price * sol_price:.2f})
"
                f"Perda: *-{perda_pct:.2f}%*",
                parse_mode="Markdown"
            )
            return
        time.sleep(10)
