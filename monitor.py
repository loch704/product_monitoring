import requests
import os
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

print(f"[{datetime.now()}] Monitor Started")

BOT_TOKEN = "8872232866:AAFrLRFygu-w7f2lrPCPeeZtZoAX-2VavuE"
CHAT_ID = "354370983"

KEYWORDS = [
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

    base_url = "https://www.toysrus.com.hk"

    search_url = (
        "https://www.toysrus.com.hk/on/demandware.store/"
        "Sites-ToysRUs_HK-Site/zh_HK/Search-UpdateGrid"
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    start = 0
    size = 48
    total_found = 0

    while True:

        params = {
            "cgid": "preorder_hk",
            "start": start,
            "sz": size
        }

        response = requests.get(
            search_url,
            params=params,
            headers=headers,
            timeout=20
        )

        print(f"[{datetime.now()}] ToysRUs start={start}, status={response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        product_tiles = soup.select("div.product-tile")

        print(f"[{datetime.now()}] ToysRUs products found on page: {len(product_tiles)}")

        if not product_tiles:
            break

        for tile in product_tiles:

            metadata_raw = tile.get("data-metadata")

            if not metadata_raw:
                continue

            try:
                metadata = json.loads(metadata_raw)
            except Exception as e:
                print(f"[{datetime.now()}] ToysRUs metadata parse error: {e}")
                continue

            product_id_raw = metadata.get("sku") or metadata.get("id")
            title = metadata.get("name_local") or metadata.get("name") or ""
            brand = metadata.get("brand") or ""
            price = metadata.get("price") or ""

            if not product_id_raw or not title:
                continue

            searchable_text = f"{title} {brand}".lower()

            if not any(k.lower() in searchable_text for k in KEYWORDS):
                continue

            # Check sold out / unavailable text inside product tile
            tile_text = tile.get_text(" ", strip=True)

            if "暫時缺貨" in tile_text or "售罄" in tile_text or "out of stock" in tile_text.lower():
                print(f"[{datetime.now()}] Skip ToysRUs out of stock: {title}")
                continue

            product_link_tag = tile.select_one("a[data-gtm-product-link]")

            if product_link_tag and product_link_tag.get("href"):
                product_link = urljoin(base_url, product_link_tag.get("href"))
            else:
                product_link = "https://www.toysrus.com.hk/zh-hk/whats-on/new-arrivals/pre-order/"

            unique_id = f"toysrus|{product_id_raw}"

            if unique_id in known_products:
                print(f"[{datetime.now()}] Skip known ToysRUs: {title}")
                continue

            message = f"""
🚨 New Product Found

Source: ToysRUs HK

{title}

Price: ${price}

{product_link}
"""

            send_telegram(message)

            known_products.add(unique_id)
            total_found += 1

            print(f"[{datetime.now()}] Notify ToysRUs: {title}")

        # If page has fewer than size, no more pages
        if len(product_tiles) < size:
            break

        start += size

    print(f"[{datetime.now()}] ToysRUs new matched products: {total_found}")

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
