import os
import sys
import json
import requests


PARSE_API_KEY = os.environ.get("PARSE_API_KEY")

API_URL = (
    "https://api.parse.bot/"
    "scraper/21963078-8a17-40ff-a896-9b0b0ec3e828/"
    "get_fc27_market_snapshot"
)


PLAYERS = [
    ("Bradley Barcola", 21977),
    ("Paulo Dybala", 466),
    ("Emiliano Martinez", 21976),
    ("Temwa Chawinga", 20),
]


print("=" * 70)
print("FC 27 PARSE FUTBIN API TEST")
print("=" * 70)

if not PARSE_API_KEY:
    print()
    print("FEHLER: PARSE_API_KEY wurde nicht gefunden.")
    print("Bitte prüfen, ob das GitHub Secret korrekt angelegt wurde.")
    sys.exit(1)


player_ids = ",".join(str(player_id) for _, player_id in PLAYERS)

params = {
    "year": "27",
    "platform": "ps",
    "player_ids": player_ids,
}

headers = {
    "X-API-Key": PARSE_API_KEY,
    "Accept": "application/json",
}


print()
print("Spieler insgesamt:", len(PLAYERS))
print("Player IDs:", player_ids)
print("Jahr: 27")
print("Plattform: PlayStation")
print()
print("Kein Chrome.")
print("Kein Playwright.")
print("Kein Google Sheet.")
print("Nur Parse API.")
print()
print("API-Aufruf:")
print(API_URL)
print()
print("=" * 70)


try:
    response = requests.get(
        API_URL,
        params=params,
        headers=headers,
        timeout=60,
    )

    print("HTTP Status:", response.status_code)
    print("Final URL:", response.url)
    print()

    print("ROHE ANTWORT:")
    print("-" * 70)
    print(response.text[:10000])
    print("-" * 70)

    if response.status_code != 200:
        print()
        print("FEHLER: Parse API hat keinen HTTP-200-Status geliefert.")
        sys.exit(1)

    try:
        data = response.json()
    except Exception as error:
        print()
        print("FEHLER: Antwort ist kein gültiges JSON.")
        print(error)
        sys.exit(1)

    print()
    print("JSON:")
    print("-" * 70)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("-" * 70)

    # Parse kann die eigentlichen Daten in "data" zurückgeben.
    payload = data.get("data", data)

    players = payload.get("players", [])

    print()
    print("=" * 70)
    print("AUSGELESENE PREISE")
    print("=" * 70)

    if not players:
        print("Keine Spieler im Ergebnis gefunden.")
        sys.exit(1)

    names_by_id = {
        player_id: name
        for name, player_id in PLAYERS
    }

    successful = 0

    for player in players:
        player_id = player.get("player_id")
        price = player.get("price")

        name = names_by_id.get(
            player_id,
            f"Unbekannter Spieler ({player_id})"
        )

        print()
        print(f"Spieler: {name}")
        print(f"ID:      {player_id}")
        print(f"Preis:   {price}")

        if price is not None:
            print("STATUS:  PREIS GEFUNDEN")
            successful += 1
        else:
            print("STATUS:  KEIN PREIS")

    print()
    print("=" * 70)
    print(f"ERGEBNIS: {successful}/{len(PLAYERS)} Preise gefunden")
    print("=" * 70)

    if successful == len(PLAYERS):
        print()
        print(">>> PARSE TEST ERFOLGREICH <<<")
        sys.exit(0)

    print()
    print(">>> PARSE ERREICHT, ABER NICHT ALLE PREISE GEFUNDEN <<<")
    sys.exit(1)


except requests.RequestException as error:
    print()
    print("REQUEST FEHLER:")
    print(type(error).__name__, error)
    sys.exit(1)

except Exception as error:
    print()
    print("UNBEKANNTER FEHLER:")
    print(type(error).__name__, error)
    sys.exit(1)
