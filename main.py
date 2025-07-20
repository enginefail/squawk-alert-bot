import requests
import time

BOT_TOKEN = "8051404880:AAGBmdENZAxJf8bVHQmT5mgLGHR0qEXjhYA"  # buraya gerçek token
CHAT_ID = "925595845"       # buraya gerçek chat ID

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
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("ADS-B Exchange API hatası:", e)
        print("Yanıt metni:", response.text)
        return

    aircraft_list = data.get("acList", [])
    print(f"Toplam uçak sayısı: {len(aircraft_list)}")

    for aircraft in aircraft_list:
        callsign = aircraft.get("Call", "")
        squawk = aircraft.get("Sqk", "")
        destination = aircraft.get("Dst", "")
        hex_id = aircraft.get("Icao", "")

        # Tüm uçak bilgilerini konsola yazalım
        print(f"Callsign: {callsign}, Squawk: {squawk}, Destination: {destination}, ICAO: {hex_id}")

        if callsign.startswith("THY") and squawk == "7700":
            message = f"⚠️ THY Emergency detected!\nCallsign: {callsign}\nSquawk: {squawk}\nICAO: {hex_id}"
            print(message)
            send_telegram(message)

        if destination == "IST":
            message = f"✈️ İstanbul'a iniş yapan uçuş:\nCallsign: {callsign}\nICAO: {hex_id}\nSquawk: {squawk}"
            print(message)
            send_telegram(message)
