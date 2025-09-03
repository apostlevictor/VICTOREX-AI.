import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Configuration (Replace with your actual tokens/IDs)
TELEGRAM_BOT_TOKEN = "8269947031:AAFX3qv2HOwXI0sCTdb3vF6LdrDw_SkONhA"
OPENAI_API_KEY = "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"
OWNER_ID = 8367788232  # Integer value of your Telegram User ID

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom keyboard for quick responses
keyboard = [["💰 Services", "📊 Channel Info"], ["🛒 Buy/Sell Crypto", "🎁 Gift Cards"]]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = f"""
Hello {user.first_name}! I'm Victorex Trader 🕴️
Providing reliable crypto & gift card services with Christian values 🙏

*Services Offered:*
• Crypto Trading & Exchange
• Gift Card Trading
• Forex & Binary Signals
• Meme Coin Trading

Tap '📊 Channel Info' to join my official channel!
    """
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.effective_user.id

    # Pre-defined responses
    if user_message == "💰 Services":
        response = """
*My Services:*
• Crypto Buy/Sell (BTC, USDT, ETH)
• Gift Card Exchange (Amazon, iTunes, Steam)
• Forex/Binary Signals
• Meme Coin Trading

*Contact me for rates!*
        """
    elif user_message == "📊 Channel Info":
        response = "Join my Telegram channel for daily signals & updates:\nhttps://t.me/VictorexTrader"
    elif user_message == "🛒 Buy/Sell Crypto":
        response = "I offer competitive rates for:\n• BTC\n• USDT\n• ETH\n• Other altcoins\n\n*Message me directly for current rates!*"
    elif user_message == "🎁 Gift Cards":
        response = "I buy/sell:\n• Amazon Cards\n• iTunes Cards\n• Google Play Cards\n• Steam Cards\n\n*Contact me with card details!*"
    else:
        # Generate AI response for other queries
        try:
            ai_response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are Victorex Trader, a Christian crypto/gift card trader from Winners Chapel. Keep responses professional and spiritual. Always promote https://t.me/VictorexTrader. Redirect complex queries to the owner."},
                    {"role": "user", "content": user_message}
                ]
            )
            response = ai_response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI Error: {e}")
            response = "⚠️ Please try again later."

        # Forward complex queries to owner
        if "cannot" in response.lower() or "owner" in response.lower():
            await context.bot.send_message(chat_id=OWNER_ID, text=f"Forwarded from {user_id}:\n\n{user_message}")
            response = "I've forwarded your query to the owner for assistance 🙏"

    await update.message.reply_text(response, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    # Create Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
