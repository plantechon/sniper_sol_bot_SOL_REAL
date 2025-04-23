
import time
from liquidity_checker import is_liquidity_locked
from buy_executor import buy_token
from sell_executor import monitor_and_sell
from telegram_notify import notify
from utils import get_new_tokens

while True:
    try:
        tokens = get_new_tokens()
        for token in tokens:
            if is_liquidity_locked(token):
                tx_hash, entry_price = buy_token(token)
                notify(f"✅ COMPRA: {token['symbol']} | Preço: {entry_price} | TX: {tx_hash}")
                monitor_and_sell(token, entry_price)
            else:
                notify(f"❌ Ignorado: {token['symbol']} (liquidez desbloqueada)")
        time.sleep(10)
    except Exception as e:
        notify(f"⚠️ ERRO: {str(e)}")
        time.sleep(30)
