import os
import time
import json
import requests

API_KEY = os.environ["ANAKIN_API_KEY"]

BASE_URL = "https://anakin.io"

PLAYER = {
    "name": "Bradley Barcola",
    "game_year": "27",
    "player_id": "21977",
    "player_slug": "bradley-barcola",
}

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
}

payload = {
    "action_id": "act_futbin_com_player_detail",
    "params": {
        "game_year": PLAYER["game_year"],
        "player_id": PLAYER["player_id"],
        "player_slug": PLAYER["player_slug"],
    },
}

print("=" * 70)
print("ANAKIN / FUTBIN TEST")
print("=" * 70)
print()
print("Spieler:", PLAYER["name"])
print("FC Jahr:", PLAYER["game_year"])
print("FUTBIN ID:", PLAYER["player_id"])
print("Slug:", PLAYER["player_slug"])
print()

print("Starte Anfrage...")

response = requests.post(
    f"{BASE_URL}/v1/wire/task",
    headers=HEADERS,
    json=payload,
    timeout=60,
)

print("HTTP:", response.status_code)
print("Antwort:")
print(response.text)
print()

response.raise_for_status()

start_result = response.json()

if "job_id" not in start_result:
    print("Kein job_id erhalten.")
    print(json.dumps(start_result, indent=2, ensure_ascii=False))
    raise SystemExit(1)

job_id = start_result["job_id"]

print("JOB ID:", job_id)
print()
print("Warte auf FUTBIN-Ergebnis...")
print()

MAX_ATTEMPTS = 30
WAIT_SECONDS = 3

final_result = None

for attempt in range(1, MAX_ATTEMPTS + 1):

    time.sleep(WAIT_SECONDS)

    job_response = requests.get(
        f"{BASE_URL}/v1/wire/jobs/{job_id}",
        headers=HEADERS,
        timeout=60,
    )

    print(
        f"Abfrage {attempt}/{MAX_ATTEMPTS} "
        f"- HTTP {job_response.status_code}"
    )

    job_response.raise_for_status()

    result = job_response.json()

    status = result.get("status")

    print("Status:", status)

    if status == "completed":
        final_result = result
        break

    if status == "failed":
        final_result = result
        break

if final_result is None:
    print()
    print("=" * 70)
    print("TIMEOUT")
    print("=" * 70)
    print()
    print("Nach 90 Sekunden wurde kein Ergebnis geliefert.")
    raise SystemExit(1)

print()
print("=" * 70)
print("ERGEBNIS")
print("=" * 70)
print()

print(
    json.dumps(
        final_result,
        indent=2,
        ensure_ascii=False
    )
)

print()

status = final_result.get("status")

if status == "completed":

    print("=" * 70)
    print("FUTBIN-ZUGRIFF ERFOLGREICH")
    print("=" * 70)

    credits = final_result.get("credits_used")

    if credits is not None:
        print("Credits verwendet:", credits)

elif status == "failed":

    print("=" * 70)
    print("FUTBIN-ZUGRIFF FEHLGESCHLAGEN")
    print("=" * 70)

    error = final_result.get("error")

    print(
        json.dumps(
            error,
            indent=2,
            ensure_ascii=False
        )
    )

else:

    print("=" * 70)
    print("UNBEKANNTER STATUS")
    print("=" * 70)

    print("Status:", status)
