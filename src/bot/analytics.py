import logging
import sqlite3

logger = logging.getLogger(__name__)

def track_subscription(user_id):
    """Track when a user subscribes."""
    logger.info(f"User {user_id} subscribed.")
    with sqlite3.connect("data/db/bot_database.db") as conn:
        conn.execute('INSERT INTO subscriptions (user_id, subscribed_at) VALUES (?, datetime("now"))', (user_id,))
        conn.commit()

def track_download(user_id):
    """Track when a user downloads the guide."""
    logger.info(f"User {user_id} downloaded the guide.")
    with sqlite3.connect("data/db/bot_database.db") as conn:
        conn.execute('INSERT INTO downloads (user_id, downloaded_at) VALUES (?, datetime("now"))', (user_id,))
        conn.commit()

