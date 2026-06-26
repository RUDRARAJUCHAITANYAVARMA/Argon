import os
import sqlite3
import logging
from dotenv import load_dotenv
from models.prompts import TOP_10_NEWS_RETRIEVAL_PROMPT
from groq import Groq

load_dotenv()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("LLM_API_KEY"))


def retrieve_news_from_db(db_name="news.db"):
    """
    Retrieves all the titles from the database and send it to llm with its id and ask the llm for top 10 titles which will top 10 news globally


    Returns:
        dict: Dictionary of news articles
    """

    news = {}

    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT id, title FROM articles")
        articles = cursor.fetchall()

        for article_id, title in articles:
            news[article_id] = title

        return news

    except Exception as e:
        logger.exception(f"Failed to fetch news from database : {e}")
        raise


def retrieve_top_10_news_using_llm(news):
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": TOP_10_NEWS_RETRIEVAL_PROMPT.replace(
                    "{{NEWS_LIST}}", str(news)
                ),
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")


def fectch_top_news_articals(db_name="news.db"):

    news = retrieve_news_from_db()
    retrieve_top_10_news_using_llm(news)
