import requests

url = "https://www.hobbylandeshop.com/"

html = requests.get(
    "https://www.hobbylandeshop.com/"
).text

print(html)
