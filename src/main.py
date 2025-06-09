import os
import requests
from flask import Flask, request

app = Flask(__name__)

# 🔐 Περιβάλλον (Render → Environment)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_KENTRIKO = os.environ.get("WEBHOOK_KENTRIKO")

@app.route("/", methods=["POST"])
def handle_webhook():
    data = request.get_json()
    print("📥 Λήφθηκε:", data)

    if not data or "message" not in data:
        return "no message", 200

    msg = data["message"]
    text = msg.get("text") or msg.get("caption") or ""

    if not text.strip():
        return "empty", 200

    # 🚀 Αποστολή στο Discord
    payload = {"content": text}
    resp = requests.post(WEBHOOK_KENTRIKO, json=payload)

    print("➡️ Απεστάλη στο Discord:", resp.status_code)
    return "ok", 200

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))




