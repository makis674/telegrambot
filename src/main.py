import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Ρύθμιση σταθερών
BOT_TOKEN = "7514517889:AAHjBmv5LYplbLe182Quz8T1BKiWWwGdblc"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1380237398268579870/fRHBfkGPSZWu7aqNVzeYkH7W6kab5ZDvPYaYLsl-YwaGUyidf8CgOBep8piDjnLWfGzs"
RENDER_URL = "https://telegrambot-1003.onrender.com/"  # ⚠️ Προσαρμοσμένο για εσένα

@app.route('/')
def home():
    return 'OK', 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📥 Νέο μήνυμα:", data)

    try:
        message = data.get("message") or data.get("edited_message")
        if not message:
            return 'No message', 200

        text = message.get("text") or message.get("caption")
        if not text:
            print("⚠️ Χωρίς text ή caption")
            return 'No content to send', 200

        payload = {
            "content": text
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print(f"✅ Εστάλη στο Discord: {response.status_code}")
    except Exception as e:
        print("❌ Σφάλμα:", e)

    return 'OK', 200

def set_webhook():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    response = requests.post(url, json={"url": RENDER_URL})
    print(f"🌐 Webhook set: {response.status_code} {response.text}")

if __name__ == '__main__':
    set_webhook()
    app.run(host='0.0.0.0', port=10000)


