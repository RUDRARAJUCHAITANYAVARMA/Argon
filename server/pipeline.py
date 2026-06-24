import logging
from datetime import timedelta
from datetime import datetime
from news.news_api import get_top_headlines
from helpers.news_processor import clean_news_data
from database.store_database import store_news_in_db
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

        # Stage 3 - Cleaning the raw data
        logger.info("Clenaing the raw data")
        cleaned_news = clean_news_data(news)
        logger.info("Successfully cleaned the raw data")

        # Stage 4 - Storing the data in the database
        logger.info("Storing the data in the database")
        store_news_in_db(cleaned_news)
        logger.info("Successfully stored the data in the database")

    except Exception as e:
        logger.exception("Pipeline Failed with Exception : {e}")
        raise


pipeline()
