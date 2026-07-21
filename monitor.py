import requests
import os

BOT_TOKEN = "8872232866:AAFrLRFygu-w7f2lrPCPeeZtZoAX-2VavuE"
CHAT_ID = "354370983"

URL = "https://lastchancetoy.com/products.json"

KEYWORDS = [
    "arranged wigs",
]

# 讀取已通知產品
known_products = set()

if os.path.exists("notified_products.txt"):
    with open("notified_products.txt", "r", encoding="utf-8") as f:
        known_products = {line.strip() for line in f}

data = requests.get(URL).json()

new_products = []

for product in data["products"]:

    title = product["title"]

    if any(k.lower() in title.lower() for k in KEYWORDS):

        product_id = str(product["id"])

        # 未通知過
        if product_id not in known_products:

            message = f"""
🚨 New Product Found

{title}

https://lastchancetoy.com/products/{product['handle']}
"""

            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={
                    "chat_id": CHAT_ID,
                    "text": message
                }
            )

            print(f"Notify: {title}")

            new_products.append(product_id)
