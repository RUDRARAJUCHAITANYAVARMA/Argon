import os
import sqlite3
import logging
import json
from dotenv import load_dotenv
from models.prompts import TOP_10_NEWS_RETRIEVAL_PROMPT, ARTICLE_SUMMARIZATION_PROMPT
from groq import Groq

load_dotenv()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("LLM_API_KEY"))

from helpers.news_processor import clean_json_string


def retrieve_news_from_db(db_name="news.db"):
    """
    Retrieves all the titles from the database and send it to llm with its id and ask the llm for top 10 titles which will top 10 news globally


    Returns:
        dict: Dictionary of news articles
    """

    news = []

    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT id, title FROM articles")
        articles = cursor.fetchall()

        for title in articles:
            news.append(title)

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

    chunks = []
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            chunks.append(content)
    return "".join(chunks)


def fetch_articles_from_db(top_10_news, db_name="news.db"):
    """
    This function is used to fetch the top 10 news articles from the database and return them in a JSON format

    Args:
        top_10_news (dict): Dictionary of top 10 news articles
        db_name (str, optional): Name of the database. Defaults to "news.db".

    Returns:
        dict: Dictionary of top 10 news articles
    """

    logger.info("Fetching top 10 news articles from the database")

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    articles = []

    for item in top_10_news:
        cursor.execute(
            """
            SELECT id, title, description, content
            FROM articles
            WHERE title = ?
            """,
            (item["title"],),
        )

        row = cursor.fetchone()

        if row:
            articles.append(
                {
                    "rank": item["rank"],
                    "reason": item["reason"],
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "content": row[3],
                }
            )

    conn.close()
    return articles


def artical_rephraser(artical):
    """
    This function is used to rephrase the article

    Args:
        artical (dict): Dictionary of the article

    Returns:
        dict: Dictionary of the rephrased article
    """

    logger.info("Rephrasing the article")

    rephrased_articals = {}

    for artical in artical:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": ARTICLE_SUMMARIZATION_PROMPT.replace(
                        "{{ARTICAL}}", str(artical)
                    ),
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        content = clean_json_string(completion.choices[0].message.content)
        rephrased_artical = json.loads(content, strict=False)

        if rephrased_artical["title"] not in rephrased_articals:
            rephrased_articals[rephrased_artical["title"]] = rephrased_artical

    return rephrased_articals


def fectch_top_news_articals(db_name="news.db"):
    """
    This function is used to fetch the top 10 news articles from the database and return them in a JSON format

    Returns:
        dict: Dictionary of top 10 news articles
    """

    logger.info("Fetching top 10 news articles from the database")

    news = retrieve_news_from_db()
    top_10_news_raw = retrieve_top_10_news_using_llm(news)
    top_10_news = json.loads(clean_json_string(top_10_news_raw), strict=False)
    final_articals = fetch_articles_from_db(top_10_news, db_name)
    rephrased_articals = artical_rephraser(final_articals)

    return rephrased_articals
