import os
import sqlite3
import logging
from telegram import Bot
from pathlib import Path
from src.bot.config import PDF_FILE_PATH

logger = logging.getLogger(__name__)

DB_PATH = Path("data/db/bot_database.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            language TEXT,
            points INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, username, language="en"):
    """Add a new user to the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, username, language, points) VALUES (?, ?, ?, 0)', (user_id, username, language))
    conn.commit()
    conn.close()

async def check_subscription(bot: Bot, user_id: int) -> bool:
    """Check if the user is subscribed to the Telegram channel."""
    try:
        member = await bot.get_chat_member(os.getenv("CHANNEL_USERNAME"), user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Error checking subscription for user {user_id}: {e}")
        return False

async def send_pdf(chat_id, context):
    """Send the PDF file to the user."""
    try:
        with open(PDF_FILE_PATH, "rb") as pdf:
            await context.bot.send_document(
                chat_id=chat_id,
                document=pdf,
                caption="Here's your free gift! 🎁 Stay tuned for more updates in the AI Free Academia channel!"
            )
    except FileNotFoundError:
        await context.bot.send_message(chat_id=chat_id, text="Sorry, the PDF file is currently unavailable.")
    except Exception as e:
        logger.error(f"Error sending PDF: {e}")
        await context.bot.send_message(chat_id=chat_id, text="An error occurred while sending the file.")
