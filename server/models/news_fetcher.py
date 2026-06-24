import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def fectch_top_news_articals(db_name="news.db"):
    """
    Retrieves all the titles from the database and send it to llm with its id and ask the llm for top 10 titles which will top 10 news globally


    Returns:
        list: List of top 10 news articles
    """

    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT id, title FROM articles")
        articles = cursor.fetchall()

        for article_id, title in articles:
            print(f"{article_id}: {title}")

    except Exception as e:
        logger.exception(f"Failed to fetch news from database : {e}")
        raise
