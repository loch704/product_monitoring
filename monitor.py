import requests

url = "https://lastchancetoy.com/products.json"

data = requests.get(url).json()

KEYWORDS = [
    "arranged wigs",
]

for product in data["products"]:

    title = product["title"]

    if any(k in title.lower() for k in KEYWORDS):
        message = f"""
		🚨 New Product Found
        {title}https://lastchancetoy.com/products/{product['handle']}
        """
        requests.post(
			f"https://api.telegram.org/bot8872232866:AAFrLRFygu-w7f2lrPCPeeZtZoAX-2VavuE/sendMessage",
			data={
				"chat_id": 354370983,
				"text": message
    }
)

#for product in data["products"]:
#    print(product["title"])
