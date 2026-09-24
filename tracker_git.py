
import os
import requests

PLAYERS = {
    21977: "Bradley Barcola",
    466: "Paulo Dybala",
    21976: "Emiliano Martinez",
    20: "Temwa Chawinga",
}

BASE_URL = "https://www.futbin.org/futbin/api/27/fetchPriceInformation"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json,text/plain,*/*",
}

for player_id, player_name in PLAYERS.items():
    print(f"\nTeste {player_name} ({player_id})")

    params = {
        "playerresource": player_id,
        "platform": "PS",
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            headers=headers,
            timeout=20,
        )

        print("HTTP:", response.status_code)
        print("URL:", response.url)
        print("Content-Type:", response.headers.get("content-type"))

        print("Antwort:")
        print(response.text[:2000])

        if response.status_code == 200:
            try:
                data = response.json()

                print("JSON:", data)

                price = data.get("LCPrice")

                if price is not None:
                    print(f"FUTBIN PREIS: {price:,}")
                else:
                    print("LCPrice nicht gefunden.")

            except Exception as e:
                print("JSON konnte nicht gelesen werden:", e)

    except Exception as e:
        print("REQUEST FEHLER:", repr(e))
