
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(topic, page_size=10):
    if not API_KEY:
        raise ValueError("NEWS_API_KEY is missing from .env")

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()

    if data.get("status") != "ok":
        raise RuntimeError(data.get("message", "NewsAPI request failed"))

    return data.get("articles", [])
