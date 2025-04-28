import asyncio
from sniper_logic import monitor_pools
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot de monitoramento ativo!'

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(monitor_pools())
    app.run(host='0.0.0.0', port=10000)
