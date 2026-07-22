import requests
import os
from datetime import datetime

print(f"[{datetime.now()}] Monitor Started")

BOT_TOKEN = "YOUR_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

KEYWORDS = [
    "arranged wigs",
    "beyblade",
    "beybladex",
    "beyblade x",
    "ux-21",
    "ux21"
]

def send_telegram(message):

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

def monitor_lastchance(known_products):

    print(f"[{datetime.now()}] Checking LastChanceToy")
    
    data = requests.get(
        "https://lastchancetoy.com/products.json?limit=250"
    ).json()

    print(f"[{datetime.now()}] Total Products: {len(data['products'])}")

    for product in data["products"][:10]:
        print(product["title"])
    
    for product in data["products"]:

        title = product["title"]

        if not any(
            k.lower() in title.lower()
            for k in KEYWORDS
        ):
            continue

        product_id = f"lastchance|{product['id']}"

        if product_id in known_products:
            continue

        message = f"""
🚨 New Product Found

Source: LastChanceToy

{title}

https://lastchancetoy.com/products/{product['handle']}
"""

        send_telegram(message)

        known_products.add(product_id)

        print(
            f"[{datetime.now()}] Notify: {title}"
        )

def main():

    known_products = set()

    if os.path.exists("notified_products.txt"):
        with open(
            "notified_products.txt",
            "r",
            encoding="utf-8"
        ) as f:

            known_products = {
                line.strip()
                for line in f
            }

    monitor_lastchance(known_products)
    #monitor_hobbyland(known_products)

    with open(
        "notified_products.txt",
        "w",
        encoding="utf-8"
    ) as f:

        for item in sorted(known_products):
            f.write(item + "\n")

if __name__ == "__main__":
    main()

'''
URL = "https://lastchancetoy.com/products.json"

KEYWORDS = [
    "arranged wigs",
    "beyblade",
    "beybladex",
    "beyblade x",
    "ux-21",
    "ux21"
]

# 讀取已通知產品
known_products = set()

if os.path.exists("notified_products.txt"):
    with open("notified_products.txt", "r", encoding="utf-8") as f:
        known_products = {line.strip() for line in f}

print(f"[{datetime.now()}] Checking LastChanceToy")

data = requests.get(URL).json()

new_products = []

for product in data["products"]:

    title = product["title"]

    if any(k.lower() in title.lower() for k in KEYWORDS):

        # 加 Source Prefix
        product_id = f"lastchance|{product['id']}"

        if product_id not in known_products:

            message = f"""
🚨 New Product Found

Source: LastChanceToy

{title}

https://lastchancetoy.com/products/{product['handle']}
"""

            response = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={
                    "chat_id": CHAT_ID,
                    "text": message
                }
            )

            print(
                f"[{datetime.now()}] Notify: {title}"
            )

            print(
                f"[{datetime.now()}] Telegram Status: {response.status_code}"
            )

            new_products.append(product_id)

if new_products:

    with open("notified_products.txt", "a", encoding="utf-8") as f:
        for item in new_products:
            f.write(item + "\n")

print(f"[{datetime.now()}] Monitor Finished")
'''
