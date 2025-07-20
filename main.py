import os
import time
import requests

BOT_TOKEN = os.environ.get("8051404880:AAGBmdENZAxJf8bVHQmT5mgLGHR0qEXjhYA")
CHAT_ID = os.environ.get("925595845")
OPENSKY_USER = os.environ.get("enginefail")
OPENSKY_PASS = os.environ.get("Haci123..")

alerted_aircraft = {}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except Exception as e:
        print("Telegram gönderim hatası:", e)

def fetch_opensky_data():
    try:
        response = requests.get(
            "https://opensky-network.org/api/states/all",
            auth=(OPENSKY_USER, OPENSKY_PASS),
            timeout=10
        )
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            print("Geçersiz JSON. Yanıt:", response.text)
            return None
    except Exception as e:
        print("OpenSky bağlantı hatası:", e)
        return None

def monitor_squawk():
    print("Takip başlatıldı...\n")
    while True:
        data = fetch_opensky_data()
        if not data or "states" not in data or data["states"] is None:
            print("Veri alınamadı veya boş. Bekleniyor...")
            time.sleep(30)
            continue

        for aircraft in data["states"]:
            icao24 = aircraft[0]
            callsign = aircraft[1] or "N/A"
            squawk = aircraft[14]

            if squawk and squawk != alerted_aircraft.get(icao24):
                message = f"📡 Squawk değişimi tespit edildi:\✈️ ICAO: {icao24}\n📞 CallSign: {callsign.strip()}\n🔢 Squawk: {squawk}"
                print(message)
                send_telegram_message(message)
                alerted_aircraft[icao24] = squawk

        time.sleep(30)

if __name__ == "__main__":
    monitor_squawk()
