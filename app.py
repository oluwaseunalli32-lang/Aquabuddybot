import os
import threading
import logging
import telebot
from flask import Flask

# Configure standard logging to show up instantly in Gunicorn/Render
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/')
def home():
    return "AquaBuddyBot is up and running!", 200

BOT_TOKEN = os.environ.get('BOT_TOKEN')
logging.info(f"Checking BOT_TOKEN presence: {bool(BOT_TOKEN)}")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    logging.info("RECEIVED: /start command in Telegram!")
    welcome_text = (
        "🤖 **Welcome to AquaBuddy!** 🌊\n\n"
        "I'm your personal hydration cheerleader.\n\n"
        "👉 Type /water to log a glass right now."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['water'])
def log_water(message):
    logging.info("RECEIVED: /water command!")
    bot.reply_to(message, "💧 *Gulp gulp...* log recorded!", parse_mode='Markdown')

def run_bot():
    logging.info("Starting Telegram Bot infinity polling...")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        logging.error(f"Bot polling ran into an error: {e}")

if __name__ == "__main__":
    # Start the background thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
