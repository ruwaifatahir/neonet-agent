from dotenv import load_dotenv
import os
from datetime import datetime
from agents import (
    Agent,
    Runner,
    function_tool,
    enable_verbose_stdout_logging,
)
from neonet_agent.tools import (
    get_top_gainers,
    get_unique_buyers_count,
    get_trade_volume,
    get_most_liquid_pools,
)


from neonet_agent.agents.news_room.editor import editor

from pydantic import BaseModel, Field

load_dotenv()
enable_verbose_stdout_logging()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set")


class MomentumAnalysis(BaseModel):
    coin_symbol: str = Field(..., description="The symbol of the analyzed coin")
    analysis: str = Field(..., description="The momentum analysis findings")
    should_post: bool = Field(
        ..., description="Whether this coin meets high-conviction criteria"
    )


@function_tool
def log_tweet(content: str):
    """Log a tweet instead of posting it

    :param content: The tweet content to log
    :return: Confirmation message
    """
    print(f"\n--- TWEET LOG ---")
    print(f"Content: {content}")
    print(f"Character count: {len(content)}")
    print(f"--- END TWEET LOG ---\n")
    return {"status": "logged", "content": content, "character_count": len(content)}


def main() -> None:

    simple_agent = Agent(
        name="Simple Agent",
        instructions="""
        You are a simple agent. You are given a task and you need to complete it.
        """,
        tools=[get_most_liquid_pools],
        model="gpt-4o-mini",
    )

    result = Runner.run_sync(
        simple_agent,
        f"Bring me top 20 liquid pools.",
        max_turns=50,
    )

    print(f"\nFinal Result: {result.final_output}")


if __name__ == "__main__":
    main()
