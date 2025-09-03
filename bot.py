import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Configuration (Replace with your actual tokens/IDs)
TELEGRAM_BOT_TOKEN = "8269947031:AAFX3qv2HOwXI0sCTdb3vF6LdrDw_SkONhA"
OPENAI_API_KEY = "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"  # Free tier API key
OWNER_ID = 8367788232  # Integer value of your Telegram User ID

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom keyboard for quick responses
keyboard = [["💰 Services", "📊 Channel Info"], ["🛒 Buy/Sell Crypto", "🎁 Gift Cards"], ["❓ How It Works"]]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Pre-defined responses to avoid always needing API calls
predefined_responses = {
    "💰 services": """
*My Services:*
• Crypto Buy/Sell (BTC, USDT, ETH)
• Gift Card Exchange (Amazon, iTunes, Steam)
• Forex/Binary Signals
• Meme Coin Trading

*Contact me for rates!(+2347062791952)* 🙏
    """,
    "📊 channel info": "Join my Telegram channel for daily signals & updates:\nhttps://t.me/VictorexTrader\n\nWe trade FOREX market, binary options, meme coins, and exchange cards/crypto with Christian values!",
    "🛒 buy/sell crypto": """
I offer competitive rates for:
• BTC • USDT • ETH • Other altcoins

*Process:*
1. Tell me what you want to buy/sell
2. I'll provide current rates
3. We complete the transaction securely

*Message me directly with your needs!(+2347062791952)* 📲
    """,
    "🎁 gift cards": """
I buy and sell various gift cards:
• Amazon • iTunes • Google Play • Steam

*Process:*
1. Share card details (type, amount, currency)
2. I'll provide exchange rate
3. Secure transaction

*Contact me with card details!(+2347062791952)* 🎯
    """,
    "❓ how it works": """
*How My Services Work:*

1. *Signals & Trading:* Join my channel https://t.me/VictorexTrader for daily signals

2. *Crypto Exchange:* 
   - Tell me what you want to buy/sell
   - I provide current rates
   - We complete secure transaction

3. *Gift Cards:*
   - Share card details
   - I provide exchange rate
   - Secure transaction

All services conducted with Christian values and integrity! 🙏

*Message me for specific inquiries!(+2347062791952)*
    """
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = f"""
Peace be with you {user.first_name}! I'm Victorex Trader 🕴️
Providing reliable crypto & gift card services with Christian values from Winners Chapel 🙏

*Services Offered:*
• Crypto Trading & Exchange
• Gift Card Trading
• Forex & Binary Signals
• Meme Coin Trading

Tap '📊 Channel Info' to join my official channel where we share daily signals!
    """
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    user_id = update.effective_user.id

    # Check for predefined responses first
    if user_message in predefined_responses:
        response = predefined_responses[user_message]
    else:
        # For other messages, try to use OpenAI with free tier considerations
        try:
            # Simple prompt for free tier compatibility
            prompt = f"""
            You are Victorex Trader, a Christian crypto/gift card trader from Winners Chapel Nigeria.
            You're discussing services like buying/selling crypto and gift cards.
            Always promote your Telegram channel: https://t.me/VictorexTrader
            Keep responses short, professional, and include Christian values.
            
            User message: {user_message}
            
            Response:
            """
            
            # Use a simpler API call for free tier
            ai_response = openai.Completion.create(
                engine="text-davinci-003",  # More likely to work with free tier
                prompt=prompt,
                max_tokens=150,
                temperature=0.7
            )
            response = ai_response.choices[0].text.strip()
            
            # If response is empty or error, use fallback
            if not response or "error" in response.lower():
                response = "I appreciate your message. Please contact me directly for specific inquiries about crypto, gift cards, or trading signals. You can also join my channel: https://t.me/VictorexTrader 🙏"
                
        except Exception as e:
            logger.error(f"OpenAI Error: {e}")
            # Fallback response that doesn't rely on OpenAI
            response = "Thanks for your message! For specific inquiries about crypto trading, gift cards, or our signals service, please message me directly or join our channel at https://t.me/VictorexTrader 🙏"
            
            # Forward complex queries to owner
            if len(user_message) > 20:  # Only forward substantial messages
                try:
                    await context.bot.send_message(
                        chat_id=OWNER_ID, 
                        text=f"Query from user {user_id}:\n\n{user_message}"
                    )
                except:
                    pass

    await update.message.reply_text(response, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    # Create Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
