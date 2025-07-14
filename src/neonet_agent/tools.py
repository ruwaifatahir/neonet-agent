from agents import function_tool
from neonet_agent.config import exa

@function_tool
def web_search_tool(query: str):
    """Searches the web using Exa and returns the contents of the search results.

    :param query: The search query.
    :return: The contents of the search results.
    """
    return exa.search_and_contents(
        query,
        text=True,
        type="keyword",
        category="news",
        num_results=3
    )