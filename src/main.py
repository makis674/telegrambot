import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import subprocess

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_ΚΕΝΤΡΙΚΟ = os.getenv("WEBHOOK_ΚΕΝΤΡΙΚΟ")
WEBHOOK_ΕΠΙΒΙΩΣΗ = os.getenv("WEBHOOK_ΕΠΙΒΙΩΣΗ")
WEBHOOK_ΕΦΕΔΡΕΙΑ = os.getenv("WEBHOOK_ΕΦΕΔΡΕΙΑ")
WEBHOOK_ΥΓΕΙΑ = os.getenv("WEBHOOK_ΥΓΕΙΑ")
WEBHOOK_ΓΕΩΠΟΛΙΤΙΚΑ = os.getenv("WEBHOOK_ΓΕΩΠΟΛΙΤΙΚΑ")

def get_topic_webhook(text):
    clean_text = text.lower()
    
    if any(word in clean_text for word in [
        "efedr", "ethelon", "ekpaideus", "ekpaideutik", "taktik", "strat", "stratiotis",
        "vasiki ekpaideusi", "ekpaideusi", "ekpaideysh",
        "εφεδρ", "εθελον", "εκπαιδευσ", "εκπαιδευτικ", "τακτικ", "στρατ", "στρατιώτ", "βασική εκπαίδευση"
    ]):
        return WEBHOOK_ΕΦΕΔΡΕΙΑ

    elif any(word in clean_text for word in [
        "geopolitik", "tourk", "polemos", "nato", "amyn", "synora", "metopo", "kypros",
        "rosia", "oukrania", "israil",
        "γεωπολιτικ", "τούρκ", "πόλεμος", "νΑΤΟ", "άμυν", "σύνορα", "μέτωπο", "κύπρο",
        "ρωσία", "ουκρανία", "ισραήλ"
    ]):
        return WEBHOOK_ΓΕΩΠΟΛΙΤΙΚΑ

    elif any(word in clean_text for word in [
        "ygeia", "farmak", "protes voitheies", "iatr", "epidimia", "loimoxi", "iatriki", "covid", "pandimia",
        "υγει", "φαρμακ", "πρώτες βοήθειες", "ιατρ", "επιδημία", "λοίμωξη", "ιατρική", "πανδημία"
    ]):
        return WEBHOOK_ΥΓΕΙΑ

    elif any(word in clean_text for word in [
        "epiviosi", "epibiwsi", "pyxida", "ektakto", "katarrefsi", "astikos polemos", "crisis", "survival",
        "επιβίωση", "πυξίδα", "έκτακτο", "κατάρρευση", "αστικός πόλεμος", "κρίση"
    ]):
        return WEBHOOK_ΕΠΙΒΙΩΣΗ

    return WEBHOOK_ΚΕΝΤΡΙΚΟ

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
        full_text = f"{title} {text}".lower()
    else:
        full_text = text.lower()

    target_webhook = get_topic_webhook(full_text)
    requests.post(target_webhook, json={"content": text})

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    print("🤖 Bot ξεκίνησε...")
    app.run_polling()
