from IPython.core import logger
from datetime import timedelta
from datetime import datetime
from server.news.news_api import get_top_headlines


def pipeline():

    logger.info("Starting the pipeline")

    date = datetime.now() - timedelta(days=1)

    try:
        logger.info(f"Fetching news for date : {date}")
        news = get_top_headlines(date)
        logger.info(f"fetched {len(news)} news")

    except Exception as e:
        logger.exception("Pipeline Failed with Exception : {e}")
        raise
