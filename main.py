import requests
import time

BOT_TOKEN = "8051404880:AAGBmdENZAxJf8bVHQmT5mgLGHR0qEXjhYA"
CHAT_ID = "925595845"

SQUAWK_CODES = ["7700", "7500", "7600", "1200", "2000"]

HEADERS = {
    "x-rapidapi-host": "adsbexchange-com1.p.rapidapi.com",
    "x-rapidapi-key": "83acefe879mshcb54cb1e7e3e581p15e468jsna77c1d6260ab"
}

alerted_flights = set()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        resp = requests.post(url, data=data)
        resp.raise_for_status()
    except Exception as e:
        print("Telegram gönderim hatası:", e)

def check_squawk(squawk):
    url = f"https://adsbexchange-com1.p.rapidapi.com/v2/sqk/{squawk}/"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Squawk {squawk} API hatası:", e)
        return

    aircraft = data.get("acList", [])
    for plane in aircraft:
        icao = plane.get("Icao")
        callsign = plane.get("Call")
        if icao not in alerted_flights:
            message = f"Squawk {squawk} aktif!\nCallsign: {callsign}\nICAO: {icao}"
            print(message)
            send_telegram(message)
            alerted_flights.add(icao)

if __name__ == "__main__":
    send_telegram("✅ Squawk bot başladı!")
    while True:
        for code in SQUAWK_CODES:
            check_squawk(code)
        time.sleep(60)
