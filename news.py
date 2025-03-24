import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("RAPID_API_KEY")

# API Endpoint and Headers
URL = "https://real-time-news-data.p.rapidapi.com/search"
HEADERS = {
    "x-rapidapi-key": f"{API_KEY}",
    "x-rapidapi-host": "real-time-news-data.p.rapidapi.com"
}

def fetch_news(company, limit=20, country="US", lang="en", time_published="anytime"):
    query_params = {
        "query": company,
        "limit": str(limit),
        "time_published": time_published,
        "country": country,
        "lang": lang
    }
    try:
        response = requests.get(URL, headers=HEADERS, params=query_params)
        response.raise_for_status()  # Raises an error for HTTP errors (e.g., 400, 500)

        data = response.json()

        if "data" not in data:
            print("Error: Unexpected API response format")
            return []

        articles = []
        for item in data["data"]:
            articles.append({
                "title": item.get("title", "No Title"),
                "snippet": item.get("snippet", "No Snippet"),
                "link": item.get("link", "#")
            })
        return articles

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching news: {e}")
        return []

