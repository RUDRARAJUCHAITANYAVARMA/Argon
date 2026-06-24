import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def initialize_article_db(db_name="news.db"):

    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                content TEXT NOT NULL
            )
        """
        )

        connection.commit()
        connection.close()
        logger.info(f"Successfully initiallized database '{db_name}'")

    except Exception as e:
        logger.exception(f"Failed to initialize database '{db_name}' : {e}")
        raise
