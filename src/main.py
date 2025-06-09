import os
import requests
from flask import Flask, request
import subprocess

app = Flask(__name__)

# Load tokens and webhook URLs
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_KENTRIKO = os.environ.get("WEBHOOK_KENTRIKO")
WEBHOOK_EPISTIMI = os.environ.get("WEBHOOK_EPISTIMI")
WEBHOOK_EFIMERIDA = os.environ.get("WEBHOOK_EFIMERIDA")
WEBHOOK_YGEIA = os.environ.get("WEBHOOK_YGEIA")
WEBHOOK_GEOPOLITIKA = os.environ.get("WEBHOOK_GEOPOLITIKA")

KEYWORDS = {
    "ΕΠΙΣΤΗΜΗ": WEBHOOK_EPISTIMI,
    "ΕΦΗΜΕΡΙΔΑ": WEBHOOK_EFIMERIDA,
    "ΥΓΕΙΑ": WEBHOOK_YGEIA,
    "ΓΕΩΠΟΛΙΤΙΚΑ": WEBHOOK_GEOPOLITIKA,
}

@app.route("/", methods=["POST"])
def handle_webhook():
    data = request.get_json()

    if not data or "message" not in data:
        return "no message", 200

    msg = data["message"]
    text = msg.get("text") or msg.get("caption") or ""
    if not text:
        return "empty", 200

    urls = [word for word in text.split() if "youtube.com" in word or "youtu.be" in word]
    if urls:
        url = urls[0]
        try:
            title = subprocess.check_output(
                ["yt-dlp", "--skip-download", "--print", "%(title)s", url],
                text=True
            ).strip()
        except:
            title = ""
        full_text = f"({title}) {text}".upper()
    else:
        full_text = text.upper()

    target_webhook = WEBHOOK_KENTRIKO
    for keyword, webhook in KEYWORDS.items():
        if keyword in full_text:
            target_webhook = webhook
            break

    requests.post(target_webhook, json={"content": full_text})
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

