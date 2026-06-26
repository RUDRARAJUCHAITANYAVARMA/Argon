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


def fetch_article_titles(db_name="news.db"):
    """
    Retrieve the ID and title of every article stored in the database.

    These titles are later sent to the LLM to identify the most important
    global news stories.

    Args:
        db_name (str): SQLite database file.

    Returns:
        list[tuple[int, str]]:
            List of (article_id, title).
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


def rank_top_news_articles(news):
    """
    Use the LLM to identify the ten most important global news stories.

    The LLM ranks the supplied article titles based on global significance,
    uniqueness, and overall newsworthiness.

    Args:
        article_titles (list):
            List of article IDs and titles.

    Returns:
        str:
            Raw JSON response produced by the LLM.
    """

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


def fetch_article_details(top_10_news, db_name="news.db"):
    """
    Retrieve the complete article information for the selected top news.

    Matches the LLM-selected titles with records stored in the database and
    enriches them with their description and full content.

    Args:
        top_news (list):
            Ranked articles returned by the LLM.

        db_name (str):
            SQLite database file.

    Returns:
        list[dict]:
            List of complete article objects.
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


def summarize_articles(artical):
    """
    Generate concise, rewritten versions of each selected article.

    Each article is passed to the LLM, which produces a short,
    content-dense summary suitable for a news digest.

    Args:
        articles (list):
            Complete article objects.

    Returns:
        dict:
            Dictionary of summarized articles keyed by title.
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


def get_top_news_digest(db_name="news.db"):
    """
    Execute the complete news processing pipeline.

    The pipeline performs the following steps:
        1. Retrieve article titles from the database.
        2. Rank the most important stories using the LLM.
        3. Fetch complete article details.
        4. Summarize each article into a concise news digest.

    Args:
        db_name (str):
            SQLite database file.

    Returns:
        dict:
            Final summarized news digest.
    """

    logger.info("=" * 60)
    logger.info("Starting LLM News Pipeline")
    logger.info("=" * 60)

    # Stage 1: Load article titles
    logger.info("[Stage 1] Loading article titles from the database...")
    article_titles = fetch_article_titles(db_name)
    logger.info("[Stage 1] Loaded %d article titles.", len(article_titles))

    # Stage 2: Select top news
    logger.info("[Stage 2] Selecting the top 10 news stories using the LLM...")
    top_news_raw = rank_top_news_articles(article_titles)
    top_news = json.loads(clean_json_string(top_news_raw), strict=False)
    logger.info("[Stage 2] Successfully selected %d news stories.", len(top_news))

    # Stage 3: Load complete articles
    logger.info("[Stage 3] Fetching complete article details...")
    selected_articles = fetch_article_details(top_news, db_name)
    logger.info("[Stage 3] Retrieved %d complete articles.", len(selected_articles))

    # Stage 4: Generate summaries
    logger.info("[Stage 4] Generating concise article summaries...")
    summarized_articles = summarize_articles(selected_articles)
    logger.info("[Stage 4] Generated %d summarized articles.", len(summarized_articles))

    logger.info("=" * 60)
    logger.info("LLM News Pipeline completed successfully.")
    logger.info("=" * 60)

    return summarized_articles
