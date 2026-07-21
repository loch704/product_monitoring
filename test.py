import requests
import json

url = "https://backend.hobbylandeshop.com/api/products"

payload = {
    "page": 1,
    "category": ["nproduct_booking"],
    "stockStatus": "in_stock"
}

headers = {
    "Origin": "https://www.hobbylandeshop.com",
    "Referer": "https://www.hobbylandeshop.com/",
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

response = requests.post(
    url,
    json=payload,
    headers=headers
)

print(response.status_code)
print(response.text[:5000])
