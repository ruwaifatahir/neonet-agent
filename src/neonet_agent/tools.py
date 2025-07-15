from agents import function_tool
from neonet_agent.config import exa
import requests
import os
import time


insidex_api_url = "https://api-ex.insidex.trade"
api_key = os.getenv(
    "INSIDEX_API_KEY"
)  # Assuming API key is stored in environment variable


@function_tool
def web_search_tool(
    query: str, start_published_date: str = None, end_published_date: str = None
):
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
        end_published_date=end_published_date,
    )


@function_tool
def price_and_mcap(coin_address: str):
    """Fetches the price and market cap for a specific coin from the Insidex API.

    :param coin_address: The address of the coin (e.g., "0x2cd6f14a4b64c3a0fa9c644e8ed88d9c91d789a071886d67d24e6b435147063d::pugwif::PUGWIF").
    :return: JSON response containing coin price and market cap data.
    """
    url = f"{insidex_api_url}/coins/{coin_address}/price-and-mc"
    headers = {"x-api-key": api_key if api_key else ""}
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
    headers = {"x-api-key": api_key if api_key else ""}
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
    headers = {"x-api-key": api_key if api_key else ""}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        for coin in data:
            if "coinMetadata" in coin:
                if "iconUrl" in coin["coinMetadata"]:
                    del coin["coinMetadata"]["iconUrl"]
                if "icon_url" in coin["coinMetadata"]:
                    del coin["coinMetadata"]["icon_url"]
        return data[:5]
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_latest_created_coins():
    """Fetches the latest created coins data from the Insidex API.

    :return: JSON response containing latest created coins data.
    """
    url = f"{insidex_api_url}/coins/latest-created"
    headers = {"x-api-key": api_key if api_key else ""}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_top_gainers():
    """Get top gaining coins by price performance on SUI blockchain
    :return: JSON response containing top gaining coins with price data
    """
    url = f"{insidex_api_url}/coins/top-gainers"
    headers = {"x-api-key": api_key if api_key else ""}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        for coin in data:
            if "coinMetadata" in coin:
                if "iconUrl" in coin["coinMetadata"]:
                    del coin["coinMetadata"]["iconUrl"]
                if "icon_url" in coin["coinMetadata"]:
                    del coin["coinMetadata"]["icon_url"]
        return data[:5]
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_unique_buyers_count(coin_address: str, timeframe: str = "1h"):
    """Get the count of unique buyers for a specific coin in a given timeframe

    :param coin_address: The full address of the coin to analyze
    :param timeframe: Time period to analyze (1h, 4h, 24h, etc.)
    :return: JSON response containing unique buyers count
    """

    # Convert timeframe to milliseconds
    timeframe_ms = {
        "1h": 60 * 60 * 1000,
        "4h": 4 * 60 * 60 * 1000,
        "24h": 24 * 60 * 60 * 1000,
    }

    end_time = int(time.time() * 1000)  # Current time in milliseconds
    start_time = end_time - timeframe_ms.get(timeframe, 60 * 60 * 1000)  # Default to 1h

    url = f"{insidex_api_url}/spot-trades/{coin_address}/unique-buyer-count"
    headers = {"x-api-key": api_key if api_key else ""}
    params = {"startTime": start_time, "endTime": end_time}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_trade_volume(coin_address: str, timeframe: str = "1h"):
    """Get the trading volume for a specific coin in a given timeframe

    :param coin_address: The full address of the coin to analyze
    :param timeframe: Time period to analyze (1h, 4h, 24h, etc.)
    :return: JSON response containing trading volume data
    """

    # Convert timeframe to milliseconds
    timeframe_ms = {
        "1h": 60 * 60 * 1000,
        "4h": 4 * 60 * 60 * 1000,
        "24h": 24 * 60 * 60 * 1000,
    }

    end_time = int(time.time() * 1000)  # Current time in milliseconds
    start_time = end_time - timeframe_ms.get(timeframe, 60 * 60 * 1000)  # Default to 1h

    url = f"{insidex_api_url}/spot-trades/{coin_address}/trade-volume"
    headers = {"x-api-key": api_key if api_key else ""}
    params = {"startTime": start_time, "endTime": end_time}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@function_tool
def get_top_trade_count():
    """Get top coins by trade count on SUI blockchain

    :param timeframe: Time period for trade count calculation (4h, 1h, 24h, etc.)
    :param limit: Number of top trade count coins to return (default 5)
    :return: JSON response containing top trade count coins with data
    """
    url = f"{insidex_api_url}/coins/top-trade-count"
    headers = {"x-api-key": api_key if api_key else ""}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}