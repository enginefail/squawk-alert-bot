import requests

BOT_TOKEN = "8051404880:AAGBmdENZAxJf8bVHQmT5mgLGHR0qEXjhYA"
CHAT_ID = "925595845"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    print(response.status_code, response.text)

send_telegram("Merhaba, bu bir test mesajıdır!")
