import requests
import os
from datetime import datetime

print(f"[{datetime.now()}] Monitor Started")

BOT_TOKEN = "8872232866:AAFrLRFygu-w7f2lrPCPeeZtZoAX-2VavuE"
CHAT_ID = "354370983"

KEYWORDS = [
    "arranged wigs",
    "beyblade",
    "beybladex",
    "beyblade x",
    "ux-21",
    "ux21",
    "bx-49",
    "bx49"
]

def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )
    return response

def monitor_lastchance(known_products):

    print(f"[{datetime.now()}] Checking LastChanceToy")
    
    data = requests.get(
        "https://lastchancetoy.com/products.json?limit=250"
    ).json()

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

def monitor_hobbyland(known_products):

    print(f"[{datetime.now()}] Checking Hobbyland")

    payload = {
        "page": 1,
        "category": ["nproduct_booking"],
        "stockStatus": "in_stock"
    }

    headers = {
        "Origin": "https://www.hobbylandeshop.com",
        "Referer": "https://www.hobbylandeshop.com/",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(
        "https://backend.hobbylandeshop.com/api/products",
        json=payload,
        headers=headers
    )

    data = response.json()

    for product in data["data"]["list"]:

        title = product["title"]

        if not any(
            k.lower() in title.lower()
            for k in KEYWORDS
        ):
            continue

        product_id = f"hobbyland|{product['sku']}"

        if product_id in known_products:
            continue

        message = f"""
🚨 New Product Found

Source: Hobbyland

{title}

https://www.hobbylandeshop.com{product['link']}
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
    monitor_hobbyland(known_products)

    with open(
        "notified_products.txt",
        "w",
        encoding="utf-8"
    ) as f:

        for item in sorted(known_products):
            f.write(item + "\n")

if __name__ == "__main__":
    main()
