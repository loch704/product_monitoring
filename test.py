import requests
from bs4 import BeautifulSoup

url = "https://www.hobbylandeshop.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(url, headers=headers).text

print(html[:1000])
