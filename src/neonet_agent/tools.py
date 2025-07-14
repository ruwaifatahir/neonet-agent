from agents import function_tool
from neonet_agent.config import exa
import requests
import os


insidex_api_url="https://api-ex.insidex.trade"
api_key = os.getenv("INSIDEX_API_KEY") # Assuming API key is stored in environment variable


@function_tool
def web_search_tool(query: str, start_published_date: str = None, end_published_date: str = None):
    """Searches the web using Exa and returns the contents of the search results.

    :param query: The search query.
    :param start_published_date: The start date for published content in ISO 8601 format (e.g., "2025-01-01T00:00:00.000Z").
    :param end_published_date: The end date for published content in ISO 8601 format (e.g., "2025-01-31T23:59:59.999Z").
    :return: The contents of the search results.
    """
    return exa.search_and_contents(
        query,
        text=True,
        type="keyword",
        category="news",
        num_results=3,
        start_published_date=start_published_date,
        end_published_date=end_published_date
    )



@function_tool
def price_and_mcap(coin_address: str):
    """Fetches the price and market cap for a specific coin from the Insidex API.

    :param coin_address: The address of the coin (e.g., "0x2cd6f14a4b64c3a0fa9c644e8ed88d9c91d789a071886d67d24e6b435147063d::pugwif::PUGWIF").
    :return: JSON response containing coin price and market cap data.
    """
    url = f"{insidex_api_url}/coins/{coin_address}/price-and-mc"
    headers = {
        'x-api-key': api_key if api_key else ''
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_coin_safety_check(coin_address: str):
    """Fetches the safety check and market data for a specific coin from the Insidex API.

    :param coin_address: The address of the coin (e.g., "0x2cd6f14a4b64c3a0fa9c644e8ed88d9c91d789a071886d67d24e6b435147063d::pugwif::PUGWIF").
    :return: JSON response containing coin safety check data.
    """
    url = f"{insidex_api_url}/coins/{coin_address}/safety-check"
    headers = {
        'x-api-key': api_key if api_key else ''
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_trending_coins():
    """Fetches the trending coins data from the Insidex API.

    :return: JSON response containing trending coins data.
    """
    url = f"{insidex_api_url}/coins/trending"
    headers = {
        'x-api-key': api_key if api_key else ''
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@function_tool
def get_latest_created_coins():
    """Fetches the latest created coins data from the Insidex API.

    :return: JSON response containing latest created coins data.
    """
    url = f"{insidex_api_url}/coins/latest-created"
    headers = {
        'x-api-key': api_key if api_key else ''
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}