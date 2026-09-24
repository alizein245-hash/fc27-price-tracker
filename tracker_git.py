import os
import sys
import json
import time
import requests


PLAYERS = [
    {
        "name": "Bradley Barcola",
        "resource_id": 21977,
    },
    {
        "name": "Paulo Dybala",
        "resource_id": 466,
    },
    {
        "name": "Emiliano Martinez",
        "resource_id": 21976,
    },
    {
        "name": "Temwa Chawinga",
        "resource_id": 20,
    },
]

BASE_URL = "https://www.futbin.org/futbin/api/27/fetchPriceInformation"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.futbin.com/",
}


def get_price(player):
    name = player["name"]
    resource_id = player["resource_id"]

    params = {
        "playerresource": resource_id,
        "platform": "PS",
    }

    print()
    print("=" * 60)
    print(f"Spieler: {name}")
    print(f"Resource ID: {resource_id}")
    print(f"URL: {BASE_URL}")
    print(f"Parameter: {params}")
    print("-" * 60)

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            headers=HEADERS,
            timeout=20,
        )

        print(f"HTTP Status: {response.status_code}")
        print(f"Final URL: {response.url}")

        print()
        print("Antwort:")
        print(response.text[:5000])

        if response.status_code != 200:
            print()
            print(f"FEHLER: HTTP {response.status_code}")
            return None

        try:
            data = response.json()
        except Exception as error:
            print(f"FEHLER: Antwort ist kein JSON: {error}")
            return None

        print()
        print("JSON:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        price = data.get("LCPrice")

        print()
        print(f"LCPrice: {price}")

        if price is None:
            print("KEIN LCPrice in der Antwort gefunden.")
            return None

        try:
            price = int(price)
        except (ValueError, TypeError):
            print(f"LCPrice konnte nicht in Zahl umgewandelt werden: {price}")
            return None

        if price <= 0:
            print(f"Preis ist nicht positiv: {price}")
            return None

        print(f"SUCCESS: {name} = {price:,} Coins")

        return {
            "name": name,
            "resource_id": resource_id,
            "price": price,
        }

    except requests.exceptions.Timeout:
        print("FEHLER: Timeout beim Request.")
        return None

    except requests.exceptions.RequestException as error:
        print(f"FEHLER beim HTTP-Request: {error}")
        return None

    except Exception as error:
        print(f"UNBEKANNTER FEHLER: {type(error).__name__}: {error}")
        return None


def main():
    print()
    print("=" * 60)
    print("FC 27 FUTBIN DIRECT API TEST")
    print("=" * 60)
    print()
    print("Kein Chrome.")
    print("Kein Playwright.")
    print("Kein Google Sheet.")
    print("Nur direkter HTTP-Test gegen futbin.org.")
    print()
    print(f"Spieler insgesamt: {len(PLAYERS)}")

    results = []

    for player in PLAYERS:
        result = get_price(player)

        if result:
            results.append(result)

        # Kleine Pause zwischen den Requests
        time.sleep(1)

    print()
    print("=" * 60)
    print("ERGEBNIS")
    print("=" * 60)

    print(f"Erfolgreich: {len(results)}/{len(PLAYERS)}")
    print()

    if results:
        for result in results:
            print(
                f"{result['name']}: "
                f"{result['price']:,} Coins "
                f"(ID {result['resource_id']})"
            )

    print()
    print("=" * 60)

    if len(results) == len(PLAYERS):
        print("🎉 ALLE SPIELER ERFOLGREICH!")
        print()
        print("Der direkte FUTBIN-Endpoint funktioniert.")
        print("Als nächsten Schritt können wir den Tracker")
        print("ohne Chrome aufbauen.")
        print("=" * 60)

        sys.exit(0)

    elif len(results) > 0:
        print("TEILWEISE ERFOLGREICH.")
        print()
        print("Mindestens ein Spieler konnte abgefragt werden.")
        print("Die Antwort müssen wir genauer untersuchen.")
        print("=" * 60)

        sys.exit(1)

    else:
        print("KEIN SPIELER ERFOLGREICH.")
        print()
        print("Der direkte Endpoint funktioniert aus GitHub Actions")
        print("entweder nicht oder benötigt zusätzliche Parameter.")
        print("=" * 60)

        sys.exit(1)


if __name__ == "__main__":
    main()
