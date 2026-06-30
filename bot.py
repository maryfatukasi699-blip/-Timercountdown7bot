import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token from environment variable
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm Timer Countdown Bot. ⏰\n"
        "I can help you with countdowns and timers!\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Get help\n"
        "/about - About this bot\n"
        "/timer [seconds] - Set a timer (e.g., /timer 10)"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /help is issued."""
    await update.message.reply_text(
        "⏰ Timer Countdown Bot Help\n"
        "Commands available:\n"
        "/start - Start the bot\n"
        "/help - Get help\n"
        "/about - About this bot\n"
        "/timer [seconds] - Set a countdown timer\n\n"
        "Example: /timer 60 (sets a 60-second timer)\n"
        "Send me any message and I'll echo it back!"
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /about is issued."""
    await update.message.reply_text(
        "⏰ Timer Countdown Bot v1.0\n"
        "Built with python-telegram-bot\n"
        "Deployed on Railway 🚀"
    )

async def timer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /timer command."""
    try:
        if context.args:
            seconds = int(context.args[0])
            if seconds <= 0:
                await update.message.reply_text("❌ Please enter a positive number!")
                return
            if seconds > 3600:
                await update.message.reply_text("❌ Timer cannot exceed 1 hour (3600 seconds)!")
                return
            
            await update.message.reply_text(f"⏰ Timer set for {seconds} seconds! Starting now...")
            
            await asyncio.sleep(seconds)
            
            await update.message.reply_text(f"⏰ DING DING DING! {seconds} seconds are up! 🔔")
        else:
            await update.message.reply_text("❌ Please specify time in seconds!\nExample: /timer 10")
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number!\nExample: /timer 30")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    user_message = update.message.text
    await update.message.reply_text(
        f"📝 You said: {user_message}\n\n"
        "I'm your Timer Countdown Bot! ⏰\n"
        "Send /help to see available commands."
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands."""
    await update.message.reply_text(
        "❌ Sorry, I don't understand that command.\n"
        "Use /help to see available commands."
    )

def main():
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("timer", timer_command))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("Timer Countdown Bot started! Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == "__main__":
    main()
