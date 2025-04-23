
import time
from liquidity_checker import is_liquidity_locked
from buy_executor import buy_token, get_sol_price
from sell_executor import monitor_and_sell
from telegram_notify import notify
from utils import get_new_tokens

operando = False

while True:
    try:
        if operando:
            time.sleep(5)
            continue

        tokens = get_new_tokens()
        if not tokens:
            notify("⚠️ Nenhum token retornado — aguardando 60s para nova tentativa.")
            time.sleep(60)
            continue

        for token in tokens:
            if is_liquidity_locked(token):
                operando = True
                tx_hash, entry_price = buy_token(token)
                sol_price = get_sol_price()
                notify(f"✅ ENTRADA: {token['symbol']}
{entry_price:.6f} SOL (~${entry_price * sol_price:.2f}) | TX: {tx_hash}")
                monitor_and_sell(token, entry_price)
                operando = False
                break
            else:
                notify(f"❌ Ignorado: {token['symbol']} (liquidez desbloqueada)")
        time.sleep(10)
    except Exception as e:
        notify(f"⚠️ ERRO inesperado: {str(e)}")
        operando = False
        time.sleep(60)
