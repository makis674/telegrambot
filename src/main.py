import os
import requests
from flask import Flask, request
import json

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.route('/')
def home():
    return 'Bot is running!'

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print(json.dumps(data, indent=4))  # Βοηθά να δεις το chat_id και το μήνυμα στα logs

    message = data.get('message', {})
    text = message.get('text')
    caption = message.get('caption')

    # Επιλογή μεταξύ text ή caption (εικόνας/βίντεο)
    content = text or caption

    if content:
        payload = {
            'content': content
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print(f'Discord response: {response.status_code}')
    else:
        print('No content to send.')

    return 'OK'


