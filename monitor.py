import requests

url = "https://lastchancetoy.com/products.json"

data = requests.get(url).json()

for product in data["products"]:
    print(product["title"])
