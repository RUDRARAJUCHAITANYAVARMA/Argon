import logging
from datetime import timedelta
from datetime import datetime
from news.news_api import get_top_headlines
from database.database_creation import initialize_article_db

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def pipeline():

    logger.info("Starting the pipeline")

    date = datetime.now() - timedelta(days=2)

    try:

        # Stage 1 - Retrieving the news
        logger.info(f"Fetching news for date : {date}")
        news = get_top_headlines(date)
        logger.info(f"Successfully fetched {len(news)} news")

        # Stage 2 - Initializing the database
        logger.info("Initializing the database")
        initialize_article_db()
        logger.info("Successfully initialized the database")

    except Exception as e:
        logger.exception("Pipeline Failed with Exception : {e}")
        raise


pipeline()
