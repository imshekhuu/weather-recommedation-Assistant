from tools.tools import (
    _fetch_weather,
    _fetch_geocoding,
    _fetch_web_search, 
    web_scraping_urls
)

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()

llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0)


def _build_weather():
    return create_agent(
        model = llm,
        tools = [_fetch_weather]
    )

def _build_geocoding():
    return create_agent(
        model = llm,
        tools = [_fetch_geocoding]
    )

def _web_search():
    return create_agent(
        model = llm,
        tools = [_fetch_web_search]
    )


def _web_sraping():
    return create_agent(
        model = llm,
        tools = [web_scraping_urls]
    )


