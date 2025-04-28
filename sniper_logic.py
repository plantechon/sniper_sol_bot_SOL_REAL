import asyncio
from solana_utils import check_new_pools, execute_trade, get_price_change, sell_token
from telegram_alert import send_alert

LIQUIDITY_THRESHOLD = 1000
TP_MULTIPLIER = 3.0
SL_MULTIPLIER = 0.5

em_operacao = False
known_pools = set()

async def monitor_pools():
    global em_operacao
    print("Bot iniciado. Monitorando pools da Raydium...")

    while True:
        try:
            if not em_operacao:
                pool = check_new_pools(min_liquidity=LIQUIDITY_THRESHOLD, known=known_pools)
                if pool:
                    em_operacao = True
                    await send_alert(f"Novo pool detectado: {pool['symbol']}")
                    entry_price, tx = execute_trade(pool)
                    await send_alert(f"Compra REAL executada! TX: {tx} | Entrada estimada: {entry_price}")

                    while True:
                        await asyncio.sleep(10)
                        price_change = get_price_change(pool['symbol'], entry_price)

                        if price_change >= TP_MULTIPLIER:
                            await send_alert(f"TP atingido (+{price_change:.2f}x)! Enviando venda...")
                            sell_tx = sell_token(pool)
                            await send_alert(f"Venda executada (TP). TX: {sell_tx}")
                            break
                        elif price_change <= SL_MULTIPLIER:
                            await send_alert(f"SL atingido ({price_change:.2f}x)! Enviando venda...")
                            sell_tx = sell_token(pool)
                            await send_alert(f"Venda executada (SL). TX: {sell_tx}")
                            break

                    em_operacao = False
        except Exception as e:
            await send_alert(f"Erro: {str(e)}")
            em_operacao = False
        await asyncio.sleep(5)
