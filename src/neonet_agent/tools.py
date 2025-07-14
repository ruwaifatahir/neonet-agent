from agents import function_tool
from neonet_agent.config import exa

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