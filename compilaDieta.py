import json
import sys
import requests
from requests_oauthlib import OAuth1
from datetime import date, timedelta

CONSUMER_KEY = "3df3703445594d26a5059eabe2fab6f2"
CONSUMER_SECRET = "7e25fc5768e5498ab613455470ccffa1"

TOKEN_FILE = r"D:\Il mio Drive\Il mio Drive\2 Areas\Automation\fatsecret-meal-planner\fatsecret_token.json"

MENU = {
    0: [("36088308", "lunch"),   # Pr. Lav (Lun, Gio)
        ("44876698", "dinner")], # Cena WO (Lun)

    1: [("36088362", "lunch"),   # Pr. Hamburger (Mar)
        ("36088760", "dinner")], # Cena calcetto (Mar)

    2: [("36088605", "lunch"),   # Pr. Fagioli (Mer)
        ("46007550", "dinner")], # Cena (Mer)

    3: [("36088308", "lunch"),   # Pr. Lav (Lun, Gio)
        ("36088980", "dinner")], # Cena WO (Gio)

    4: [("44888708", "lunch"),   # Pr. Yogurt/Pollo (Ven)
        ("44887245", "dinner")], # Cena Salmone (Ven)

    5: [("44888758", "lunch"),   # Pr. Yogurt/Lenticchie (Sab)
        ("37019234", "dinner")], # Cena Pizza (sab&dom)

    6: [("37022485", "lunch"),   # Pranzo della Domenica (Dom)
        ("37019234", "dinner"),  # Cena Pizza (sab&dom)
        ("36888847", "other")],  # Panino con nutella (Dom)
}

def days_since_epoch(d):
    return (d - date(1970, 1, 1)).days

def monday_has_entries(auth, monday):
    """Controlla se il lunedì indicato ha già pasti inseriti su FatSecret."""
    date_int = days_since_epoch(monday)
    response = requests.get(
        "https://platform.fatsecret.com/rest/server.api",
        params={
            "method": "food_entries.get",
            "date": date_int,
            "format": "json"
        },
        auth=auth
    )
    result = response.json()
    # Se c'è almeno una voce, il giorno è già compilato
    food_entries = result.get("food_entries", {})
    return bool(food_entries.get("food_entry"))

# ── Presentazione ─────────────────────────────────────────────────────────────
print("=" * 55)
print("         COMPILA DIETA - FatSecret Meal Planner")
print("=" * 55)
print()
print("Questo script inserisce automaticamente i pasti della")
print("prossima settimana (lun-dom) su FatSecret, copiando i")
print("saved meal predefiniti per ogni giorno.")
print()

# ── Setup auth e calcolo settimana ────────────────────────────────────────────
with open(TOKEN_FILE) as f:
    token_data = json.load(f)

auth = OAuth1(
    CONSUMER_KEY, CONSUMER_SECRET,
    token_data["token"], token_data["secret"]
)

# Calcola il lunedì della prossima settimana
# Funziona qualsiasi giorno tu lo lanci: compila sempre lun-dom della settimana successiva
today = date.today()
days_to_monday = (7 - today.weekday()) % 7 or 7
next_monday = today + timedelta(days=days_to_monday)
week_end = next_monday + timedelta(days=6)

print(f"Settimana da compilare: {next_monday.strftime('%d/%m/%Y')} - {week_end.strftime('%d/%m/%Y')}")
print()

# ── Controllo preventivo: lunedì già compilato? ───────────────────────────────
print("Controllo pasti già presenti su FatSecret...", end=" ", flush=True)
if monday_has_entries(auth, next_monday):
    print("ATTENZIONE!\n")
    print(f"Il lunedì {next_monday.strftime('%d/%m/%Y')} ha già dei pasti inseriti.")
    print("La settimana risulta già compilata. Operazione annullata.")
    print()
    input("Premi INVIO per chiudere...")
    sys.exit(0)
print("OK, settimana libera.\n")

# ── Conferma utente ───────────────────────────────────────────────────────────
risposta = input("Vuoi procedere con la compilazione? (s/n): ").strip().lower()
if risposta != "s":
    print("\nOperazione annullata dall'utente.")
    input("Premi INVIO per chiudere...")
    sys.exit(0)

print(f"\nCompilo la settimana dal {next_monday} al {week_end}\n")

for day_offset, meals in MENU.items():
    target_date = next_monday + timedelta(days=day_offset)
    date_int = days_since_epoch(target_date)

    for meal_id, meal_type in meals:
        response = requests.get(
            "https://platform.fatsecret.com/rest/server.api",
            params={
                "method": "food_entries.copy_saved_meal",
                "saved_meal_id": meal_id,
                "meal": meal_type,
                "date": date_int,
                "format": "json"
            },
            auth=auth
        )
        result = response.json()
        if "error" in result:
            print(f"ERRORE {target_date} {meal_type}: {result['error']['message']}")
        else:
            print(f"OK {target_date} {meal_type} (meal_id: {meal_id})")

input("\nPremi INVIO per chiudere...")
