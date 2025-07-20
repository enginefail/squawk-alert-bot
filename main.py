import requests
import time
import os

BOT_TOKEN = os.environ.get("8051404880:AAGBmdENZAxJf8bVHQmT5mgLGHR0qEXjhYA")
CHAT_ID = os.environ.get("925595845")

ALERT_SQUAWKS = ['7500', '7600', '7700']
TARGET_AIRLINE = "THY"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_squawk():
    try:
        print("Squawk kontrol ediliyor...")
        response = requests.get("https://opensky-network.org/api/states/all", timeout=10)
        data = response.json()

        for flight in data.get("states", []):
            callsign = flight[1].strip() if flight[1] else ""
            squawk = flight[14] if len(flight) > 14 else None

            if TARGET_AIRLINE in callsign and squawk in ALERT_SQUAWKS:
                msg = f"🚨 Acil Durum Squawk!\n📡 Flight: {callsign}\n🔢 Squawk: {squawk}"
                send_telegram_alert(msg)
                print("Gönderildi:", msg)
    except Exception as e:
        print("Hata:", e)

# Script başlarken test mesajı gönder
send_telegram_alert("Test mesajı: Bot başarıyla çalışıyor!")


while True:
    check_squawk()
    time.sleep(60)
