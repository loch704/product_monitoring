import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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

'''
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
'''

def monitor_toysrus(known_products):

    print(f"[{datetime.now()}] Checking ToysRUs HK")

    url = "https://www.toysrus.com.hk/zh-hk/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    print(f"[{datetime.now()}] ToysRUs Status: {response.status_code}")

    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all("a")

    found_count = 0

    for a in links:

        title = a.get_text(" ", strip=True)
        href = a.get("href")

        if not title:
            continue

        if not href:
            continue

        # keyword filtering
        if not any(
            k.lower() in title.lower()
            for k in KEYWORDS
        ):
            continue

        full_link = urljoin(
            "https://www.toysrus.com.hk",
            href
        )

        # source-specific dedup
        product_id = f"toysrus|{full_link}"

        if product_id in known_products:
            print(f"[{datetime.now()}] Skip known ToysRUs: {title}")
            continue

        # basic stock text check
        lower_text = title.lower()

        if "暫時缺貨" in title or "out of stock" in lower_text:
            print(f"[{datetime.now()}] Skip out of stock ToysRUs: {title}")
            continue

        message = f"""
🚨 New Product Found

Source: ToysRUs HK

{title}

{full_link}
"""

        send_telegram(message)

        known_products.add(product_id)

        found_count += 1

        print(f"[{datetime.now()}] Notify ToysRUs: {title}")

    print(f"[{datetime.now()}] ToysRUs matched new products: {found_count}")
    print(f"[{datetime.now()}] Candidate ToysRUs: {title}")
    print(full_link)

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

    #monitor_lastchance(known_products)
    #monitor_hobbyland(known_products)
    monitor_toysrus(known_products)

    with open(
        "notified_products.txt",
        "w",
        encoding="utf-8"
    ) as f:

        for item in sorted(known_products):
            f.write(item + "\n")

if __name__ == "__main__":
    main()
