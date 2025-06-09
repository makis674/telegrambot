from flask import Flask, request
import os
import requests
import subprocess

app = Flask(__name__)

WEBHOOK_KENTRIKO = os.environ.get("WEBHOOK_KENTRIKO")
WEBHOOK_YOUTUBE = os.environ.get("WEBHOOK_YOUTUBE")
WEBHOOK_PORN = os.environ.get("WEBHOOK_PORN")

keywords = {
    "PORN": WEBHOOK_PORN,
    "YOUTUBE": WEBHOOK_YOUTUBE,
}

@app.route("/", methods=["POST"])
def handle_webhook():
    data = request.get_json()
    print("📥 Raw incoming data:", data)

    if not data or "message" not in data:
        return "No message", 200

    msg = data["message"]
    text = msg.get("text") or msg.get("caption") or ""

    print("📝 Extracted text:", text)

    if not text:
        print("⚠️ No text/caption found in message")
        return "empty", 200

    urls = [word for word in text.split() if "youtube.com" in word or "youtu.be" in word]
    print("🔗 Detected URLs:", urls)

    return "ok", 200
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

