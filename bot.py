from flask import Flask, request
import requests
from telegram import Bot

# 🔑 TOKENS
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
PAYSTACK_SECRET = "YOUR_PAYSTACK_SECRET_KEY"

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

# 👑 VIP storage (simple version)
vip_users = set()

# 💰 Telegram message function
def send_message(chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)

# 🚀 TELEGRAM WEBHOOK (optional extension)
@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]

        if data["message"].get("text") == "/start":
            send_message(chat_id,
                "👋 Welcome to Auto Market Bot\n\n"
                "💰 VIP Access: ₦2,000/month\n"
                "Click pay link to activate VIP."
            )

    return "ok"


# 💳 PAYSTACK WEBHOOK (AUTO PAYMENT CONFIRMATION)
@app.route('/paystack-webhook', methods=['POST'])
def paystack_webhook():
    event = request.get_json()

    if event["event"] == "charge.success":
        email = event["data"]["customer"]["email"]

        # You can map email → telegram user (important upgrade later)
        # For now we simulate VIP activation

        print("Payment successful for:", email)

        # Example: auto activate VIP (demo logic)
        # In real system, you link email to telegram ID
        vip_users.add(email)

    return "ok"


# 📊 CHECK VIP STATUS
def is_vip(user):
    return user in vip_users


# 🚀 RUN SERVER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(port="0.0.0.0", port=port)