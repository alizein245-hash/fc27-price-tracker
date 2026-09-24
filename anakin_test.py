
import os
import time
import requests
import json

API_KEY = os.environ["ANAKIN_API_KEY"]

BASE_URL = "https://api.anakin.io"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
}

# 1. FUTBIN Market Player Listing starten
response = requests.post(
    f"{BASE_URL}/v1/wire/task",
    headers=headers,
    json={
        "action_id": "act_futbin_com_market_player_listing",
        "params": {}
    },
    timeout=60,
)

print("START HTTP:", response.status_code)
print(response.text)

response.raise_for_status()

job = response.json()
job_id = job["job_id"]

print()
print("JOB ID:", job_id)
print("Warte auf Ergebnis...")

# 2. Job abfragen
for attempt in range(30):

    time.sleep(3)

    result_response = requests.get(
        f"{BASE_URL}/v1/wire/jobs/{job_id}",
        headers=headers,
        timeout=60,
    )

    print(
        f"Abfrage {attempt + 1}: "
        f"HTTP {result_response.status_code}"
    )

    result_response.raise_for_status()

    result = result_response.json()

    print("Status:", result.get("status"))

    if result.get("status") == "completed":
        print()
        print("===== FERTIG =====")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        break

    if result.get("status") == "failed":
        print()
        print("===== FEHLER =====")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        break

else:
    print("Timeout: Nach 90 Sekunden noch kein Ergebnis.")
