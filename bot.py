import logging
import asyncio
import requests
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration - REPLACE WITH YOUR ACTUAL VALUES
BOT_TOKEN = "8269947031:AAFiiLpB7mJyz7K4m_ez_qHlYiTjmsKyBE"  # Get from @BotFather
ADMIN_ID = "8367788232"    # Your Telegram user ID (get from @userinfobot)

# Image URLs for illustrations (replace with your own image URLs)
WELCOME_IMAGE = "https://example.com/welcome.jpg"  # Replace with actual image URL
TEAM_IMAGE = "https://example.com/team.jpg"        # Replace with actual image URL
EARNING_IMAGE = "https://example.com/earning.jpg"  # Replace with actual image URL

# Store user states
user_states = {}

def download_image(url, filename):
    """Download an image from URL and save it locally"""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception as e:
        logger.error(f"Error downloading image: {e}")
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when the command /start is issued."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    # Send initial welcome message with image
    welcome_message = (
        "🤝 Hi, thank you for subscribing to my channel. In this chat I will tell you a little bit about myself.\n\n"
        "CHECK my channel and if you will ready to work, message me \"READY\" 💸\n\n"
        "I'm waiting for your message and we'll get started 🚀"
    )
    
    # Try to send image with caption, fallback to text only if image fails
    try:
        # Download and send image
        if download_image(WELCOME_IMAGE, "welcome.jpg"):
            with open("welcome.jpg", "rb") as photo:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=InputFile(photo),
                    caption=welcome_message,
                    parse_mode=ParseMode.MARKDOWN
                )
        else:
            await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"Error sending welcome image: {e}")
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
    
    # Set user state to waiting for READY
    user_states[user_id] = "waiting_ready"
    
    # Simulate typing for 15 seconds
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    await asyncio.sleep(15)
    
    # Send the first message after delay
    if user_id in user_states and user_states[user_id] == "waiting_ready":
        await send_victorex_intro(update, context)

async def send_victorex_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send Victorex introduction messages with delays."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    messages = [
        "Hello 🤝 My name is Victorex. I'm a developer 💻 and started earning online few months ago 💵. Now I am recruiting people for my team so that we can earn together 🤲",
        "I earn $3000 thousand USD monthly and also share algorithms with my clients who give me 10% of their earnings 🙏",
        "You will work on your personal account ✍️, only you will have access to your account and your money, for security purposes and I will give you the winning algorithm and bot. I give all my students a profit guarantee because I trust my work 💪",
        "And I'll give you a personal manager who will do everything with you step by step 👍",
        "Are you ready to join my team and start earning with the bot?"
    ]
    
    # Send team image with first message
    try:
        if download_image(TEAM_IMAGE, "team.jpg"):
            with open("team.jpg", "rb") as photo:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=InputFile(photo),
                    caption=messages[0],
                    parse_mode=ParseMode.MARKDOWN
                )
        else:
            await update.message.reply_text(messages[0], parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"Error sending team image: {e}")
        await update.message.reply_text(messages[0], parse_mode=ParseMode.MARKDOWN)
    
    await asyncio.sleep(3)  # Wait after image
    
    # Send remaining messages
    for msg in messages[1:]:
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        await asyncio.sleep(2)  # Simulate typing
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(3)  # Wait between messages
    
    # Update user state to waiting for yes
    user_states[user_id] = "waiting_yes"

async def send_final_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send final details after user says yes."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    messages = [
        "Your job is simply just use SOFTWARE and SIGNALS 🔝",
        "Daily PROFIT is 600-900 USD 💵 minimum. 😮",
        "My percentage is 10% ONLY AFTER you withdraw money. 💯",
        "➡️ I provide only guarantee winning signals",
        "➡️ There is NO risk and your money be SAFE",
        "➡️ Your balance must be top up",
        "Are you ready now fully to work with me?"
    ]
    
    # Send earning image with first message
    try:
        if download_image(EARNING_IMAGE, "earning.jpg"):
            with open("earning.jpg", "rb") as photo:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=InputFile(photo),
                    caption=messages[0],
                    parse_mode=ParseMode.MARKDOWN
                )
        else:
            await update.message.reply_text(messages[0], parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"Error sending earning image: {e}")
        await update.message.reply_text(messages[0], parse_mode=ParseMode.MARKDOWN)
    
    await asyncio.sleep(3)  # Wait after image
    
    # Send remaining messages
    for msg in messages[1:]:
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        await asyncio.sleep(2)  # Simulate typing
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(3)  # Wait between messages
    
    # Update user state to completed
    user_states[user_id] = "completed"
    
    # Notify that owner will take over
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    await asyncio.sleep(2)
    await update.message.reply_text("Great! I'll now connect you with victorex assistant for the next steps. Please wait for her message.", parse_mode=ParseMode.MARKDOWN)
    
    # Notify admin about new user
    try:
        user = update.effective_user
        user_info = (
            f"👤 New user completed the onboarding process:\n\n"
            f"Name: {user.first_name} {user.last_name or ''}\n"
            f"Username: @{user.username or 'Not provided'}\n"
            f"User ID: {user.id}\n\n"
            f"Please contact them for next steps."
        )
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=user_info,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Error notifying admin: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages based on their current state."""
    user_id = update.effective_user.id
    message_text = update.message.text.strip().lower()
    
    if user_id not in user_states:
        await update.message.reply_text("Please start with /start first.", parse_mode=ParseMode.MARKDOWN)
        return
    
    if user_states[user_id] == "waiting_ready" and "ready" in message_text:
        await send_victorex_intro(update, context)
    elif user_states[user_id] == "waiting_yes" and ("yes" in message_text or "ready" in message_text or "yeah" in message_text):
        await send_final_details(update, context)
    elif user_states[user_id] == "completed":
        # Forward messages to admin after completion
        await forward_to_admin(update, context)
    else:
        # Handle other messages appropriately
        if user_states[user_id] == "waiting_ready":
            await update.message.reply_text("Please type 'READY' when you're ready to proceed. 😊", parse_mode=ParseMode.MARKDOWN)
        elif user_states[user_id] == "waiting_yes":
            await update.message.reply_text("Please answer with 'YES' if you're ready to join the team. 👍", parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text("Please wait for the owner to contact you. They'll be with you shortly. ⏳", parse_mode=ParseMode.MARKDOWN)

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forward user messages to admin after the automated conversation."""
    user = update.effective_user
    message = update.message
    
    # Prepare message with user info
    user_info = (
        f"👤 Message from: {user.first_name} {user.last_name or ''}\n"
        f"Username: @{user.username or 'no_username'}\n"
        f"User ID: `{user.id}`"
    )
    
    try:
        if message.text:
            full_message = f"{user_info}\n\n💬 {message.text}"
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=full_message,
                parse_mode=ParseMode.MARKDOWN
            )
            # Confirm to user
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            await asyncio.sleep(1)
            await update.message.reply_text("✅ Message delivered to (Charlotte Victorex assistant)she will respond shortly .", parse_mode=ParseMode.MARKDOWN)
            
        elif message.photo:
            # Forward photo to admin
            caption = f"{user_info}\n\n📸 Photo"
            if message.caption:
                caption += f"\nCaption: {message.caption}"
                
            await context.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=message.photo[-1].file_id,
                caption=caption,
                parse_mode=ParseMode.MARKDOWN
            )
            await update.message.reply_text("✅ Photo delivered to (Charlotte Victorex assistant). 📸", parse_mode=ParseMode.MARKDOWN)
            
        elif message.video:
            # Forward video to admin
            caption = f"{user_info}\n\n🎥 Video"
            if message.caption:
                caption += f"\nCaption: {message.caption}"
                
            await context.bot.send_video(
                chat_id=ADMIN_ID,
                video=message.video.file_id,
                caption=caption,
                parse_mode=ParseMode.MARKDOWN
            )
            await update.message.reply_text("✅ Video delivered to (Charlotte Victorex assistant). 🎥", parse_mode=ParseMode.MARKDOWN)
            
        elif message.document:
            # Forward document to admin
            caption = f"{user_info}\n\n📄 Document"
            if message.caption:
                caption += f"\nCaption: {message.caption}"
                
            await context.bot.send_document(
                chat_id=ADMIN_ID,
                document=message.document.file_id,
                caption=caption,
                parse_mode=ParseMode.MARKDOWN
            )
            await update.message.reply_text("✅ Document delivered to (Charlotte Victorex assistant). 📄", parse_mode=ParseMode.MARKDOWN)
            
    except Exception as e:
        logger.error(f"Error forwarding message to admin: {e}")
        await update.message.reply_text("❌ Could not deliver your message. Please try again later.", parse_mode=ParseMode.MARKDOWN)

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Allow admin to reply to users directly."""
    if str(update.effective_user.id) != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.", parse_mode=ParseMode.MARKDOWN)
        return
    
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /reply <user_id> <message>\n\nExample: /reply 12345678 Hello there!",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    try:
        user_id = int(context.args[0])
        message_text = " ".join(context.args[1:])
        
        # Send message to user
        await context.bot.send_message(
            chat_id=user_id,
            text=f"📩 Message from Charlotte Victorex assistant:\n\n{message_text}",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Confirm to admin
        await update.message.reply_text("✅ Message sent to user.", parse_mode=ParseMode.MARKDOWN)
        
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID. Please provide a numeric user ID.", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"Error sending message to user: {e}")
        await update.message.reply_text("❌ Failed to send message. User might have blocked the bot.", parse_mode=ParseMode.MARKDOWN)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by Updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reply", admin_reply))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Handle media messages
    application.add_handler(MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.ATTACHMENT,
        forward_to_admin
    ))
    
    # Handle errors
    application.add_error_handler(error_handler)

    # Start the Bot
    print("🤖 Victorex Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
