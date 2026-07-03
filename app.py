import os
import threading
import logging
import telebot
from flask import Flask

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@app.route('/')
def home():
    return "AquaBuddyBot is alive and running smoothly!", 200

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    logging.info("👉 SUCCESS: /start command received in Telegram!")
    welcome_text = (
        "🤖 **Welcome to AquaBuddy!** 🌊\n\n"
        "I'm your personal hydration cheerleader.\n\n"
        "👉 Type /water to log a glass right now."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['water'])
def log_water(message):
    logging.info("👉 SUCCESS: /water command received!")
    bot.reply_to(message, "💧 *Gulp gulp...* log recorded!", parse_mode='Markdown')

def run_bot():
    logging.info("🤖 Starting Telegram Bot polling thread...")
    try:
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    except Exception as e:
        logging.error(f"❌ Bot polling error: {e}")

# This ensures the thread starts cleanly as soon as Gunicorn spins up the app context
def start_background_worker():
    logging.info("⚙️ Initializing background worker...")
    if not os.environ.get('WERKZEUG_RUN_MAIN'): # Prevents double-running in dev environments
        worker_thread = threading.Thread(target=run_bot)
        worker_thread.daemon = True
        worker_thread.start()

start_background_worker()

