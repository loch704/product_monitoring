import requests

BOT_TOKEN = "你的Bot Token"
CHAT_ID = "你的Chat ID"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": "🚀 Telegram Bot Test Success!"
}

requests.post(url, data=payload)
``
