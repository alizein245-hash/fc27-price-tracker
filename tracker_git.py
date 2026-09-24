import json
import os
import re
import urllib.request
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright


# ============================================================
# SPIELER
# ============================================================

PLAYERS = [
    {
        "name": "Bradley Barcola",
        "url": "https://www.futbin.com/27/player/21977/bradley-barcola",
    },
    {
        "name": "Paulo Dybala",
        "url": "https://www.futbin.com/27/player/466/paulo-dybala",
    },
    {
        "name": "Emiliano Martinez",
        "url": "https://www.futbin.com/27/player/21976/emiliano-martinez",
    },
    {
        "name": "Temwa Chawinga",
        "url": "https://www.futbin.com/27/player/20/temwa-chawinga",
    },
]


# ============================================================
# GOOGLE SHEETS WEBHOOK
# ============================================================

GOOGLE_WEBHOOK = os.environ.get("GOOGLE_WEBHOOK")

if not GOOGLE_WEBHOOK:
    raise RuntimeError(
        "GOOGLE_WEBHOOK wurde nicht gefunden. "
        "Bitte das GitHub Secret prüfen."
    )


# ============================================================
# PREIS AUS FUTBIN-SEITENTEXT ERMITTELN
# ============================================================

def extract_price(text):
    """
    Sucht plausible FUTBIN-Preise im sichtbaren Seitentext.
    """

    candidates = []

    patterns = [
        r"\b\d{1,3}(?:[.,]\d{3})+\b",
        r"\b\d{4,7}\b",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)

        for raw in matches:
            cleaned = raw.replace(".", "").replace(",", "")

            try:
                value = int(cleaned)
            except ValueError:
                continue

            # FUT-Preis sinnvoll begrenzen
            if 200 <= value <= 15_000_000:
                candidates.append(value)

    if not candidates:
        return None

    # Doppelte Werte entfernen
    candidates = sorted(set(candidates))

    print("Gefundene plausible Zahlen:", candidates[:30])

    # Vorläufig kleinsten plausiblen Wert verwenden
    return candidates[0]


# ============================================================
# EINEN SPIELER ABFRAGEN
# ============================================================

def get_player_price(page, player):

    print()
    print("=" * 60)
    print(f"Spieler: {player['name']}")
    print(f"URL: {player['url']}")
    print("=" * 60)

    page.goto(
        player["url"],
        wait_until="domcontentloaded",
        timeout=60_000,
    )

    # Warten, damit dynamische Inhalte geladen werden
    page.wait_for_timeout(7_000)

    # Etwas scrollen
    page.mouse.wheel(0, 1200)
    page.wait_for_timeout(2_000)

    text = page.locator("body").inner_text()

    print(f"Seitentext: {len(text)} Zeichen")

    # Cloudflare / Browser-Challenge erkennen
    challenge_words = [
        "Just a moment",
        "Checking your browser",
        "Verify you are human",
        "Performing security verification",
    ]

    for word in challenge_words:
        if word.lower() in text.lower():
            raise RuntimeError(
                f"FUTBIN-Browser-Challenge erkannt: {word}"
            )

    price = extract_price(text)

    if price is None:
        print("KEIN PREIS GEFUNDEN.")

        print()
        print("---- SEITENTEXT AUSZUG ----")
        print(text[:5000])
        print("---- ENDE AUSZUG ----")

        return None

    print(f"ERKANNTER PREIS: {price:,}")

    return price


# ============================================================
# DATEN AN GOOGLE SHEETS SENDEN
# ============================================================

def send_to_google(prices):

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prices": prices,
    }

    print()
    print("=" * 60)
    print("Sende Daten an Google Sheets")
    print("=" * 60)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        GOOGLE_WEBHOOK,
        data=data,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:

        response_text = response.read().decode("utf-8")

        print()
        print("Google Sheets Antwort:")
        print(response_text)

        if response.status != 200:
            raise RuntimeError(
                f"Google Webhook HTTP-Fehler: {response.status}"
            )


# ============================================================
# HAUPTPROGRAMM
# ============================================================

def main():

    results = []

    print("=" * 60)
    print("FC 27 FUTBIN PRICE TRACKER")
    print("=" * 60)

    print(f"Spieler insgesamt: {len(PLAYERS)}")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
        )

        for player in PLAYERS:

            context = browser.new_context(
                viewport={
                    "width": 1365,
                    "height": 900,
                },
                locale="en-US",
                user_agent=(
                    "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/140.0.0.0 Safari/537.36"
                ),
            )

            page = context.new_page()

            try:

                price = get_player_price(
                    page,
                    player,
                )

                if price is not None:

                    results.append(
                        {
                            "name": player["name"],
                            "price": price,
                        }
                    )

            except Exception as error:

                print()
                print(
                    f"FEHLER bei {player['name']}: "
                    f"{type(error).__name__}: {error}"
                )

            finally:

                context.close()

        browser.close()

    print()
    print("=" * 60)
    print(
        f"ERGEBNIS: {len(results)}/{len(PLAYERS)} Spieler erfolgreich"
    )
    print("=" * 60)

    if not results:

        raise RuntimeError(
            "Kein einziger Spielerpreis konnte ermittelt werden."
        )

    send_to_google(results)

    print()
    print("Tracker erfolgreich beendet.")


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()
