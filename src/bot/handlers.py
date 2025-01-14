from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from src.bot.utils import add_user, check_subscription, send_pdf
from src.bot.analytics import track_subscription, track_download
from src.bot.config import CHANNEL_USERNAME
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    """Send a welcome message and 'Get' button."""
    user = update.effective_user
    add_user(user.id, user.username)
    await update.message.reply_text(
        "Welcome to AI Free Academia! 🚀\n\nGet the top 10 free neural networks and instructions on how to work with them. Click the button below to start!",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Get", callback_data="get")]])
    )

async def button_handler(update: Update, context: CallbackContext):
    """Handle button clicks."""
    query = update.callback_query
    await query.answer()

    if query.data == "get":
        if not CHANNEL_USERNAME:
            await query.message.reply_text("Error: Channel username is not configured.")
            return

        subscribe_url = f"https://t.me/{CHANNEL_USERNAME}"
        keyboard = [
            [InlineKeyboardButton("Subscribe", url=subscribe_url)],
            [InlineKeyboardButton("I Subscribed", callback_data="subscribed")]
        ]
        await query.edit_message_text(
            text="Subscribe to the AI Free Academia channel and get your free gift 🎁.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "subscribed":
        if await check_subscription(context.bot, query.from_user.id):
            track_subscription(query.from_user.id)
            await query.edit_message_text("Thank you for subscribing! 🎉 Here's your free gift ✨.")
            await send_pdf(query.from_user.id, context)
            track_download(query.from_user.id)
        else:
            await query.edit_message_text(
                "It seems like you haven't subscribed yet. Please subscribe and try again. 🙏",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Subscribe", url=f"https://t.me/{CHANNEL_USERNAME}")],
                    [InlineKeyboardButton("I Subscribed", callback_data="subscribed")]
                ])
            )

def setup_handlers(application):
    """Set up the handlers for the bot."""
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
