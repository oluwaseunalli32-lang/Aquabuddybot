import os
import threading
import telebot
from flask import Flask

# 1. Initialize Flask app for Render's health check
app = Flask(__name__)

@app.route('/')
def home():
    return "AquaBuddyBot is up and running!", 200

# 2. Initialize Telegram Bot
# We pull the token from environment variables for security
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# 3. Bot Command Handlers
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 **Welcome to AquaBuddy!** 🌊\n\n"
        "I'm your personal hydration cheerleader. I'm here to make sure "
        "you don't turn into a raisin today!\n\n"
        "👉 Use /remind to set up your schedule (Coming soon!).\n"
        "👉 Type /water to log a glass right now."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['water'])
def log_water(message):
    bot.reply_to(message, "💧 *Gulp gulp...* log recorded! Keep it up, hero! 🏆", parse_mode='Markdown')

# 4. Function to run the bot poll in a separate thread
def run_bot():
    print("Starting Telegram Bot polling...")
    bot.infinity_polling()

if __name__ == "__main__":
    # Start the Telegram bot thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Start the Flask web server on the port Render gives us
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
  
