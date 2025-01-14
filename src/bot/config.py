from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
PDF_FILE_PATH = os.getenv("PDF_FILE_PATH", "data/pdfs/neural_networks_guide.pdf")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in the environment.")

