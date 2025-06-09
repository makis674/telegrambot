import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import subprocess

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_KENTRIKO = os.getenv("WEBHOOK_KENTRIKO")
WEBHOOK_EPIVIOSI = os.getenv("WEBHOOK_EPIVIOSI")
WEBHOOK_EFEDREIA = os.getenv("WEBHOOK_EFEDREIA")
WEBHOOK_YGEIA = os.getenv("WEBHOOK_YGEIA")
WEBHOOK_GEOPOLITIKA = os.getenv("WEBHOOK_GEOPOLITIKA")

KEYWORDS = {
    "EPIVIOSI": WEBHOOK_EPIVIOSI,
    "EFEDREIA": WEBHOOK_EFEDREIA,
    "YGEIA": WEBHOOK_YGEIA,
    "GEOPOLITIKA": WEBHOOK_GEOPOLITIKA,
}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    text = update.message.text or update.message.caption or ""
    if not text:
        return
    urls = [word for word in text.split() if "youtube.com" in word or "youtu.be" in word]
    if urls:
        url = urls[0]
        try:
            title = subprocess.check_output(["yt-dlp", "--skip-download", "--print", "%(title)s", url], text=True).strip()
        except:
            title = ""
        full_text = f"{title} {text}".upper()
    else:
        full_text = text.upper()

    target_webhook = WEBHOOK_KENTRIKO
    for keyword, webhook in KEYWORDS.items():
        if keyword in full_text:
            target_webhook = webhook
            break

    requests.post(target_webhook, json={"content": text})

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    print("Bot started...")
    app.run_polling()
