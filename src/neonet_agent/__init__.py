from dotenv import load_dotenv
import os
from datetime import datetime
from agents import (
    Agent,
    Runner,
    function_tool,
    enable_verbose_stdout_logging,
    # SQLiteSession,
)
from neonet_agent.tools import (
    get_top_gainers,
    get_unique_buyers_count,
    get_trade_volume,
    get_most_liquid_pools,
    get_top_trade_count,
    get_trending_coins
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
        tools=[log_tweet],
    )

    # Momentum Analysis Agent - Specialized for finding high-conviction plays
    momentum_agent = Agent(
        name="SUI Momentum Agent",
        instructions=f"""
        You are a specialized SUI momentum trading analyst. Current time: {current_time}
        
        YOUR ONLY JOB: Find high-conviction momentum plays and hand off the data.
        
        ANALYSIS PROCESS:
        1. Call get_top_gainers() to find the best performing coins (get top 5)
        2. FILTER OUT major coins: Skip any BTC, ETH, or other major cryptocurrencies - focus only on SUI ecosystem tokens
        3. ITERATE through each remaining coin in the results list, starting with the top performer:
           - For each coin, use the 'coin' field (the full coin address)
           - Call get_unique_buyers_count() with the coin address and timeframe="1h"
           - Call get_trade_volume() with the coin address and timeframe="1h"
           - STRICT CRITERIA CHECK - A coin is HIGH-CONVICTION ONLY if BOTH conditions are met:
             * CONDITION 1: buyers >= 20 (twenty or more unique buyers)
             * CONDITION 2: volume >= 5000 (five thousand dollars or more in volume)
           - If EITHER condition fails, IMMEDIATELY REJECT the coin and move to next coin
           - If BOTH conditions pass: HANDOFF TO TWEET GENERATOR with this data format:
             "Found high-conviction play: [SYMBOL] - Price: [change]%, Buyers: [count], Volume: $[amount], Analysis: [brief insight]"
           - NEVER post about coins with less than 20 buyers OR less than $5000 volume
         4. If NO coins meet BOTH criteria: conclude "No high-conviction opportunities found at {current_time}"
         
         CRITICAL: Your job ends when you find one good coin and hand it off, or when you've checked all coins.
         You do NOT create tweets - that's the tweet generator's job.
         """,
        model="gpt-4o-mini",
        tools=[get_top_gainers],
        # handoffs=[tweet_generator_agent],
    )

    simple_agent = Agent(
        name="Simple Agent",
        instructions="""
        Your are a simple agent and you have a tool for top gainer of coins
        """,
        model="gpt-4o-mini",
        tools=[get_trending_coins,get_top_gainers],
    )


    result = Runner.run_sync(
        simple_agent,
        "Bring me the trending coins",
        # session=session,
        max_turns=50,
    )

    print(f"\nFinal Result: {result.final_output}")


if __name__ == "__main__":
    main()
