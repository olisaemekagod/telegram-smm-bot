import requests
from telegram.ext import Updater, CommandHandler
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("API_KEY")
PANEL_URL = 'https://smm8.com/api/v2'

def start(update, context):
    update.message.reply_text("Welcome to BoostBot! Type /services to see what I offer.")

def services(update, context):
    payload = {'key': API_KEY, 'action': 'services'}
    try:
        response = requests.post(PANEL_URL, data=payload)
        services = response.json()

        msg = "Available Services:\n"
        for s in services[:10]:
            msg += f"ID: {s['service']} | {s['name']} (${s['rate']}/1k)\n"
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Failed to fetch services.")

def order(update, context):
    try:
        _, service_id, link, quantity = update.message.text.split()
        payload = {
            'key': API_KEY,
            'action': 'add',
            'service': service_id,
            'link': link,
            'quantity': quantity
        }
        r = requests.post(PANEL_URL, data=payload)
        res = r.json()
        if 'order' in res:
            update.message.reply_text(f"✅ Order placed! Order ID: {res['order']}")
        else:
            update.message.reply_text(f"❌ Error: {res}")
    except:
        update.message.reply_text("❗ Usage: /order service_id link quantity")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('services', services))
    dp.add_handler(CommandHandler('order', order))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
