import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def clean_news_data(news):
    """
    Helps in cleaning the news data

    Args:
        news (list): List of news articles

    Returns:
        list: List of cleaned news articles
    """

    news_data = []
    try:
        for article in news:
            news_data.append(
                {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "content": article.get("content"),
                }
            )
    except Exception as e:
        logger.exception(f"Failed to store news in database : {e}")
        raise

    return news_data
