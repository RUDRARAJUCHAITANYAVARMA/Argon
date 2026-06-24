def clean_news_data(news):
    """
    Helps in cleaning the news data

    Args:
        news (list): List of news articles

    Returns:
        list: List of cleaned news articles
    """

    news_data = []

    for article in news:
        news_data.append(
            {
                "title": article.get("title"),
                "description": article.get("description"),
                "content": article.get("content"),
            }
        )

    return news_data
