import requests
import os
import time

BOT_TOKEN = os.environ.get("8051404880:AAGBmdENZAxJf8bVHQmT5mgLGHR0qEXjhYA")
CHAT_ID = os.environ.get("925595845")

alerted_flights = set()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        resp = requests.post(url, data=data)
        resp.raise_for_status()
    except Exception as e:
        print("Telegram gönderim hatası:", e)

def check_adsbexchange():
    url = "https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("ADS-B Exchange API hatası:", e)
        return

    aircraft_list = data.get("acList", [])

    for aircraft in aircraft_list:
        callsign = aircraft.get("Call", "")
        squawk = aircraft.get("Sqk", "")
        hex_id = aircraft.get("Icao", "")

        if callsign.startswith("THY") and squawk == "7700":
            if hex_id not in alerted_flights:
                message = f"⚠️ THY Emergency detected!\nCallsign: {callsign}\nSquawk: {squawk}\nICAO: {hex_id}"
                print(message)
                send_telegram(message)
                alerted_flights.add(hex_id)

if __name__ == "__main__":
    send_telegram("✅ ADS-B Exchange bot başladı, test mesajı!")
    while True:
        check_adsbexchange()
        time.sleep(60)
