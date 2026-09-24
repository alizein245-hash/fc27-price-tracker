import requests
import json
import sys


URL = "https://www.futbin.com/27/playerPrices"

PLAYER_IDS = [
    21977,
    466,
    21976,
    20,
]


print("=" * 70)
print("FC 27 FUTBIN BATCH PRICE TEST")
print("=" * 70)

rids = ",".join(str(x) for x in PLAYER_IDS)

params = {
    "player": "",
    "rids": rids,
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.futbin.com/",
}

print()
print("Spieler:", len(PLAYER_IDS))
print("RIDs:", rids)
print()
print("URL:")
print(URL)

try:
    response = requests.get(
        URL,
        params=params,
        headers=headers,
        timeout=30,
    )

    print()
    print("HTTP Status:", response.status_code)
    print("Final URL:", response.url)

    print()
    print("ANTWORT:")
    print("-" * 70)
    print(response.text[:10000])
    print("-" * 70)

    if response.status_code != 200:
        print()
        print(">>> BATCH REQUEST NICHT ERFOLGREICH")
        sys.exit(1)

    data = response.json()

    print()
    print("JSON ERFOLGREICH GELESEN")
    print()

    names = {
        21977: "Bradley Barcola",
        466: "Paulo Dybala",
        21976: "Emiliano Martinez",
        20: "Temwa Chawinga",
    }

    successful = 0

    print("=" * 70)
    print("PLAYSTATION PREISE")
    print("=" * 70)

    for player_id in PLAYER_IDS:

        player = data.get(str(player_id))

        print()
        print("Spieler:", names.get(player_id, str(player_id)))
        print("ID:", player_id)

        if not player:
            print("Preis: NICHT GEFUNDEN")
            continue

        prices = player.get("prices", {})
        ps = prices.get("ps", {})

        price = ps.get("LCPrice")

        print("Preis:", price)

        if price is not None:
            successful += 1

    print()
    print("=" * 70)
    print(f"ERGEBNIS: {successful}/{len(PLAYER_IDS)}")
    print("=" * 70)

    if successful == len(PLAYER_IDS):
        print()
        print(">>> BATCH SNAPSHOT FUNKTIONIERT <<<")
        sys.exit(0)

    sys.exit(1)

except Exception as error:
    print()
    print("FEHLER:")
    print(type(error).__name__, error)
    sys.exit(1)
