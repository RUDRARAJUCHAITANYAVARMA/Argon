import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def store_news_in_db(news_data, db_name="news.db"):
    """
    Stores the cleaned news data in the database

    Args:
        news_data (list): List of cleaned news articles
        db_name (str): Name of the database
    """
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        for article in news_data:
            cursor.execute(
                """
                INSERT INTO articles (title, description, content) VALUES (?, ?, ?)
                """,
                (article["title"], article["description"], article["content"]),
            )
        connection.commit()
        connection.close()

    except Exception as e:
        logger.exception(f"Failed to store news in database : {e}")
        raise
