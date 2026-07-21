import requests

BOT_TOKEN = "8872232866:AAFrLRFygu-w7f2lrPCPeeZtZoAX-2VavuE"
CHAT_ID = "354370983"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": "🚀 Telegram Bot Test Success!"
}

response = requests.post(url, data=payload)

print(response.status_code)
print(response.text)
