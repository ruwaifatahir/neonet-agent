from agents import function_tool
from neonet_agent.config import exa
import requests
import os
import time
from neonet_agent.lib.constants import stable_coins
from neonet_agent.lib.utils import extract_symbol


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
def get_most_liquid_pools(limit: int = 20):
    """Get the most liquid pools on SUI blockchain

    :param limit: Number of most liquid pools to return (default 20)
    :return: JSON response containing most liquid pools data.
    """
    url = f"{insidex_api_url}/pools/top-liquidity?limit={limit}&platforms=cetus,turbo"
    headers = {"x-api-key": api_key if api_key else ""}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Filter out pools where both coins are stable coins
        if isinstance(data, list):
            filtered_pools = []
            for pool in data:
                coin_a_address = pool.get("coinA", "")
                coin_b_address = pool.get("coinB", "")

                # Extract symbols from addresses
                coin_a_symbol = extract_symbol(coin_a_address)
                coin_b_symbol = extract_symbol(coin_b_address)

                # Check if both coins are stable coins
                is_coin_a_stable = coin_a_symbol in stable_coins
                is_coin_b_stable = coin_b_symbol in stable_coins

                if not (is_coin_a_stable and is_coin_b_stable):
                    filtered_pools.append(pool)

            return filtered_pools

        return data
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
def get_trade_volume(coin_address: str):
    """Get the trading volume for a specific coin in a given timeframe

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

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@function_tool
def get_top_trade_count():
    """Get top coins by trade count on SUI blockchain

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

@function_tool
def get_top_holder_quality_score():
    """Get top coins by holder quality score from the Insidex API.

    :return: JSON response containing top holder quality score data.
    """
    url = f"{insidex_api_url}/coins/top-holder-quality-score"
    headers = {"x-api-key": api_key if api_key else ""}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if isinstance(data, list):
            filtered_coins = []
            for coin_data in data:
                coin_address = coin_data.get("coin", "")
                coin_symbol = extract_symbol(coin_address)

                if coin_symbol not in stable_coins:
                    filtered_coins.append(coin_data)
            return filtered_coins

        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@function_tool
def complete_portfolio(wallet_address: str):
    """
    Fetches the complete spot portfolio for a given wallet address from the Insidex API.

    :param wallet_address: The wallet address to fetch the portfolio for.
    :return: JSON response containing the spot portfolio data, excluding icon URLs.
    """
    url = f"{insidex_api_url}/spot-portfolio/{wallet_address}"
    headers = {"x-api-key": api_key if api_key else ""}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # If response is a dict and has a "balances" key with list
        if isinstance(data, dict) and "balances" in data:
            for item in data["balances"]:
                coin_metadata = item.get("coinMetadata", {})
                coin_metadata.pop("icon_url", None)
                coin_metadata.pop("iconUrl", None)

        return data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@function_tool
def get_past_trades(wallet_address: str, limit: int = 1, skip: int = 0):
    """Fetches past trades for a given wallet address from the Insidex API.

    :param wallet_address: The wallet address to fetch past trades for.
    :param limit: The maximum number of trades to return.
    :param skip: The number of trades to skip.
    :return: JSON response containing past trades data.
    """
    url = f"{insidex_api_url}/spot-portfolio/{wallet_address}/past-trades"
    headers = {"x-api-key": api_key if api_key else ""}
    params = {"limit": limit, "skip": skip}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@function_tool
def get_spot_trade_stats(wallet_address: str):
    """Fetches spot trade statistics for a given wallet address from the Insidex API.

    :param wallet_address: The wallet address to fetch trade statistics for.
    :return: JSON response containing spot trade statistics.
    """
    url = f"{insidex_api_url}/spot-portfolio/{wallet_address}/spot-trade-stats"
    headers = {"x-api-key": api_key if api_key else ""}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if isinstance(data, dict) and "coins" in data and isinstance(data["coins"], list):
            for coin_data in data["coins"]:
                if "coinMetadata" in coin_data:
                    if "iconUrl" in coin_data["coinMetadata"]:
                        del coin_data["coinMetadata"]["iconUrl"]
                    if "icon_url" in coin_data["coinMetadata"]:
                        del coin_data["coinMetadata"]["icon_url"]
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@function_tool
def get_most_profitable_traders(coin_address: str, limit: int = 2, skip: int = 0):
    """Fetches the most profitable traders for a given coin address from the Insidex API.

    :param coin_address: The address of the coin to analyze.
    :param limit: The maximum number of traders to return.
    :param skip: The number of traders to skip.
    :return: JSON response containing most profitable traders data.
    """
    url = f"{insidex_api_url}/spot-trades/{coin_address}/most-profitable-traders"
    headers = {"x-api-key": api_key if api_key else ""}
    params = {"limit": limit, "skip": skip}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}