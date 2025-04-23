
import requests
import os

def notify(message, parse_mode=None):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
    }
    if parse_mode:
        data["parse_mode"] = parse_mode
    try:
        requests.post(url, json=data)
    except Exception as e:
        print(f"Erro Telegram: {e}")
