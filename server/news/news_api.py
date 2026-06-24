import requests
import os
from dotenv import load_dotenv

load_dotenv()

news_api_key = os.getenv("NEWS_API_KEY")

response = requests.get(
    f"https://newsapi.org/v2/everything?q=*&from=2026-06-22&sortBy=publishedAt&apiKey={news_api_key}"
)
