from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from bs4 import BeautifulSoup

load_dotenv()
tavily = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))

# tools for fetch the latitude and longitude of the input city
@tool
def _fetch_geocoding(city : str) -> list:
    """fetch the latitude and longitude and return latitude and longitude."""

    url = "https://geocoding-api.open-meteo.com/v1/search" #url of the api to fetch the latitude and longitude

    param = {
        "name" : city,
        "count" : 1
    }

    response = requests.get(url, params=param)
    data = response.json()

    result = data["results"][0]

    return {
        "latitude": result["latitude"],  #latitude of the city 
        "longitude": result["longitude"] #longitude of the city 
    }

# tools for fetch the weather details for the given latitude and longitude
@tool
def _fetch_weather(latitude: float, longitude: float):
    """fetch the weather details using latitude and longitude and return the details."""

    url = "https://api.open-meteo.com/v1/forecast" #url of the api to fetch the weather details

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    }

    response = requests.get(url, params=params)

    return response.json()

@tool
def _fetch_web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""

    result = tavily.search(query=query, max_results=5)

    out = []

    for r in result["result"]:
          out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
          
    return "\n-----\n".join(out)

@tool
def web_scraping_urls(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""

    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"