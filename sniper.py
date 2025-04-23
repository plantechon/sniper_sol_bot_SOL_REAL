
import time
from liquidity_checker import is_liquidity_locked
from buy_executor import buy_token, get_sol_price
from sell_executor import monitor_and_sell
from telegram_notify import notify
from utils import get_new_tokens
import os
from solders.keypair import Keypair
from solana.rpc.api import Client
import ast

operando = False

def check_wallet_balance():
    keypair = Keypair.from_bytes(bytes(ast.literal_eval(os.getenv("SOLANA_PRIVATE_KEY"))))
    rpc = Client(os.getenv("RPC_URL"))
    balance = rpc.get_balance(keypair.pubkey())["result"]["value"] / 1e9
    if balance < 0.03:
        notify(f"⚠️ Saldo insuficiente na carteira do bot: apenas {balance:.4f} SOL", parse_mode="Markdown")
        return False
    return True

while True:
    try:
        if operando or not check_wallet_balance():
            time.sleep(30)
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
                msg = (
                    f"✅ ENTRADA: {token['symbol']}\n"
                    f"`{entry_price:.6f} SOL` (~${entry_price * sol_price:.2f})\n"
                    f"[Ver transação](https://solscan.io/tx/{tx_hash})"
                )
                notify(msg, parse_mode="Markdown")
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
