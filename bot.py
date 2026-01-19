import telebot
import requests
import time
import threading
import random
import os
from flask import Flask

# --- FLASK SETUP (For Render Port Exposure) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is Running!", 200

def run_flask():
    # Render uses port 10000 by default
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- TELEGRAM BOT CONFIG ---
API_TOKEN = '8474261468:AAF3TZemleBwXKv27mFdMY0w4T57kZh_nLk'
VERCEL_API_URL = "https://api-api-nine.vercel.app/get-key?key=CHIRAGx9"
bot = telebot.TeleBot(API_TOKEN)

subscribers = set()

# --- BACKGROUND MONITOR ---
def api_monitor():
    print("🚂 Background Engine Started... 💀")
    while True:
        if subscribers:
            try:
                response = requests.get(VERCEL_API_URL, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        intel = data["intel"]
                        msg = (
                            f"⚡️ *PREMIUM API DETECTED* ⚡️\n"
                            f"━━━━━━━━━━━━━━━━━━━━\n"
                            f"📡 *Service:* `{intel['service']}`\n"
                            f"🔑 *API Key:* `{intel['api_key']}`\n"
                            f"✅ *Status:* Online & Active\n"
                            f"━━━━━━━━━━━━━━━━━━━━\n"
                            f"📅 *First Found:* `{intel['dates']['first_found']}`\n"
                            f"🔍 *Displays:* `{intel['metrics']['times_displayed']}`\n"
                            f"📂 *Path:* `{intel['source_leak']['file_path']}`\n"
                            f"🔗 *Source:* [View Repository]({intel['source_leak']['repo_url']})\n"
                            f"━━━━━━━━━━━━━━━━━━━━\n"
                            f"👤 *Developer:* @dex4dev | *Owner:* CHIRAGX9\n\n"
                            f"⚠️ /UNSUBSCRIBE to stop alerts."
                        )
                        for user_id in list(subscribers):
                            try:
                                bot.send_message(user_id, msg, parse_mode="Markdown", disable_web_page_preview=True)
                            except: pass
            except Exception as e:
                print(f"Fetch Error: {e}")

        wait_time = random.randint(20, 300)
        time.sleep(wait_time)

# --- COMMANDS ---
@bot.message_handler(commands=['start', 'subscribe', 'SUBSCRIBE'])
def start_command(message):
    subscribers.add(message.chat.id)
    bot.reply_to(message, "🤖 *PROFESSIONAL API INTELLIGENCE* 🤖\n\nSUBSCRIBED! YOU WILL RECEIVE EVERY WORKING API.\n\n👉 /UNSUBSCRIBE TO STOP.", parse_mode="Markdown")

@bot.message_handler(commands=['unsubscribe', 'UNSUBSCRIBE'])
def stop_command(message):
    if message.chat.id in subscribers:
        subscribers.remove(message.chat.id)
    bot.reply_to(message, "Service stopped. Message /SUBSCRIBE to start again.")

# --- EXECUTION ---
if __name__ == "__main__":
    # 1. Start Port Exposure
    threading.Thread(target=run_flask, daemon=True).start()
    # 2. Start API Monitor
    threading.Thread(target=api_monitor, daemon=True).start()
    # 3. Start Bot Polling
    print("🔥 Bot and Port 10000 are Live... 💀")
    bot.infinity_polling()
