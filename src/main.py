import os
import requests
from flask import Flask, request
import subprocess

app = Flask(__name__)

# Load tokens and webhook URLs
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_KENTRIKO = os.environ.get("WEBHOOK_KENTRIKO")
WEBHOOK_PISTINE = os.environ.get("WEBHOOK_PISTINE")
WEBHOOK_FITERNIDA = os.environ.get("WEBHOOK_FITERNIDA")
WEBHOOK_XEPLA = os.environ.get("WEBHOOK_XEPLA")
WEBHOOK_GEOPOLITIKA = os.environ.get("WEBHOOK_GEOPOLITIKA")

# Keywords
keywords = {
    "ΚΕΝΤΡΙΚΟ": WEBHOOK_KENTRIKO,
    "ΠΙΣΤΙΝΕΣ": WEBHOOK_PISTINE,
    "FITERNIDA": WEBHOOK_FITERNIDA,
    "ΧΕΠΛΑ": WEBHOOK_XEPLA,
    "ΓΕΩΠΟΛΙΤΙΚΑ": WEBHOOK_GEOPOLITIKA
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
        full_text = f"«{title}» {text}".upper()
    else:
        full_text = text.upper()

    target_webhook = WEBHOOK_KENTRIKO
    for keyword, webhook in keywords.items():
        if keyword in full_text:
            target_webhook = webhook
            break

    requests.post(target_webhook, json={"content": full_text})
    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)





