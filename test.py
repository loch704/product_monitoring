import requests

BOT_TOKEN = "8872232866:AAFrLRFygu-w7f2lrPCPeeZtZoAX-2VavuE"
CHAT_ID = "354370983"

r = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": "🧪 Product Monitor Test"
    },
    timeout=20
)

print(r.status_code)
print(r.text)
