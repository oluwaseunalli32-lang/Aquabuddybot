import os
import threading
import telebot
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "AquaBuddyBot is up and running!", 200

BOT_TOKEN = os.environ.get('BOT_TOKEN')
print(f"DEBUG: Found BOT_TOKEN: {bool(BOT_TOKEN)}") # This will print True or False in your logs

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print("DEBUG: Received /start command!") # This will tell us if Telegram reached Render
    welcome_text = (
        "🤖 **Welcome to AquaBuddy!** 🌊\n\n"
        "I'm your personal hydration cheerleader.\n\n"
        "👉 Type /water to log a glass right now."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['water'])
def log_water(message):
    print("DEBUG: Received /water command!")
    bot.reply_to(message, "💧 *Gulp gulp...* log recorded!", parse_mode='Markdown')

def run_bot():
    print("DEBUG: Thread started. Starting infinity_polling now...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"DEBUG: Bot polling crashed with error: {e}")

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
