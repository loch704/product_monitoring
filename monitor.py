import requests

url = "https://lastchancetoy.com/products.json"

data = requests.get(url).json()

KEYWORDS = [
    "arranged wigs",
]

for product in data["products"]:

    title = product["title"]

    if any(k in title.lower() for k in KEYWORDS):
        print(title)

#for product in data["products"]:
#    print(product["title"])
