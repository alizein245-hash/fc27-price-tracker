
import os
import time
import json
import requests

# ============================================================
# ANAKIN / FUTBIN TEST
# FC 27 - PlayStation
# Bradley Barcola
# ============================================================

API_KEY = os.environ["ANAKIN_API_KEY"]

BASE_URL = "https://anakin.io"

ACTION_ID = "act_futbin_com_player_detail"

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

# ------------------------------------------------------------
# 1. FUTBIN-Abfrage über Anakin starten
# ------------------------------------------------------------

payload = {
    "action_id": ACTION_ID,
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

# ------------------------------------------------------------
# 2. Job pollen
# ------------------------------------------------------------

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

print()

# ------------------------------------------------------------
# 3. Ergebnis ausgeben
# ------------------------------------------------------------

print("=" * 70)
print("ERGEBNIS")
print("=" * 70)
print()

if final_result is None:
    print("TIMEOUT")
    print(
        "Nach",
        MAX_ATTEMPTS * WAIT_SECONDS,
        "Sekunden wurde kein Ergebnis geliefert."
    )
    raise SystemExit(1)

print(
    json.dumps(
        final_result,
        indent=2,
        ensure_ascii=False
    )
)

print()

# ------------------------------------------------------------
# 4. Ergebnis bewerten
# ------------------------------------------------------------

status = final_result.get("status")

if status == "completed":

    print("=" * 70)
    print("FUTBIN-ZUGRIFF ERFOLGREICH")
    print("=" * 70)

    credits = final_result.get("credits_used")

    if credits is not None:
        print("Credits verwendet:", credits)

    print()
    print("Die komplette FUTBIN-Antwort steht oben.")
    print()
    print(
        "Bitte diese Ausgabe hier im Chat posten, "
        "damit wir den PS-Preis identifizieren können."
    )

elif status == "failed":

    print("=" * 70)
    print("FUTBIN-ZUGRIFF FEHLGESCHLAGEN")
    print("=" * 70)

    error = final_result.get("error")

    print()
    print("Fehler:")
    print(json.dumps(error, indent=2, ensure_ascii=False))

    print()
    print(
        "Bitte diese Ausgabe hier im Chat posten."
    )

else:

    print("=" * 70)
    print("UNBEKANNTER STATUS")
    print("=" * 70)

    print("Status:", status)
```

### 2. GitHub-Workflow

Lege zusätzlich unter

`.github/workflows/`

eine neue Datei an, zum Beispiel:

`anakin-player-test.yml`

mit:

```yaml
name: Anakin FUTBIN Player Test

on:
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest

    permissions:
      contents: read

    steps:

      - name: Repository auschecken
        uses: actions/checkout@v4

      - name: Python einrichten
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Requests installieren
        run: |
          python -m pip install --upgrade pip
          python -m pip install re
