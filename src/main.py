@app.route("/", methods=["POST"])
def handle_webhook():
    data = request.get_json()
    print("📨 RAW incoming data:", data)

    if not data or "message" not in data:
        return "No message", 200

    msg = data["message"]
    text = msg.get("text") or msg.get("caption") or ""

    print("📝 Extracted text:", text)

    if not text:
        print("⚠️ No text/caption found in message")
        return "empty", 200

    urls = [word for word in text.split() if "youtube.com" in word or "youtu.be" in word]

    if urls:
        url = urls[0]
        try:
            title = subprocess.check_output(
                ["yt-dlp", "--skip-download", "--print", "%(title)s", url],
                text=True
            ).strip()
            full_text = f"{title}\n{text}".upper()
        except:
            full_text = text.upper()
    else:
        full_text = text.upper()

    target_webhook = WEBHOOK_KENTRIKO
    for keyword, webhook in keywords.items():
        if keyword in full_text:
            target_webhook = webhook
            break

    print("📤 Sending to Discord webhook:", target_webhook)
    print("📦 Payload:", full_text)

    requests.post(target_webhook, json={"content": full_text})
    return "ok", 200







