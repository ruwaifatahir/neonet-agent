from dotenv import load_dotenv
import os
from datetime import datetime
from agents import (
    Agent,
    Runner,
    enable_verbose_stdout_logging,
)
from neonet_agent.tools import (
    get_top_gainers,
    get_unique_buyers_count,
    get_trade_volume,
    get_most_liquid_pools,
    get_top_trade_count,
    get_trending_coins,
)


from neonet_agent.agents.news_room.editor import editor

from pydantic import BaseModel, Field

load_dotenv()
enable_verbose_stdout_logging()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set")


def main() -> None:

    simple_agent = Agent(
        name="Simple Agent",
        instructions="""
        Your are a simple agent and you have a tool for top gainer of coins
        """,
        model="gpt-4o-mini",
        tools=[get_trending_coins, get_top_gainers],
    )

    result = Runner.run_sync(
        simple_agent,
        "Bring me the top holder quality score",
        max_turns=50,
    )

    print(f"\nFinal Result: {result.final_output}")


if __name__ == "__main__":
    main()
