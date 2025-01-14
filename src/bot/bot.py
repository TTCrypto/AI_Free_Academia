from telegram.ext import Application
from src.bot.handlers import setup_handlers
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="logs/bot.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    """Main entry point for the bot."""
    try:
        application = Application.builder().token(BOT_TOKEN).build()

        # Set up handlers
        setup_handlers(application)

        # Start polling or webhook based on environment
        if os.getenv("ENV") == "production":
            logging.info("Starting bot in webhook mode...")
            application.run_webhook(
                listen="0.0.0.0",
                port=int(os.getenv("PORT", 8443)),
                url_path=BOT_TOKEN,
                webhook_url=f"https://{os.getenv('RENDER_APP_URL')}/{BOT_TOKEN}"
            )
        else:
            logging.info("Starting bot in polling mode...")
            application.run_polling()
    except Exception as e:
        logging.error(f"Bot failed to start: {e}")

if __name__ == "__main__":
    main()
