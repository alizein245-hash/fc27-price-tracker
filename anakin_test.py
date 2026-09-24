
import os
import requests
import json

API_KEY = os.environ["ANAKIN_API_KEY"]

url = "https://anakin.io/v1/wire/task"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
}

payload = {
    "action_id": "act_futbin_com_market_player_listing",
    "params": {}
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=60,
)

print("HTTP:", response.status_code)
print("Content-Type:", response.headers.get("content-type"))
print()
print(response.text[:20000])
