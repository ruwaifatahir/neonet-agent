from dotenv import load_dotenv
import os
from datetime import datetime
from agents import (
    Agent,
    Runner,
    function_tool,
    enable_verbose_stdout_logging,
    SQLiteSession,
)
from neonet_agent.tools import (
    get_top_gainers,
    get_unique_buyers_count,
    get_trade_volume,
)
from pydantic import BaseModel, Field

load_dotenv()
# enable_verbose_stdout_logging()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set")

session = SQLiteSession("conversation_123", "conversation_history.db")


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
    current_time = datetime.now().strftime("%I:%M %p")

    # Tweet Generator Agent - Specialized for creating engaging tweets
    tweet_generator_agent = Agent(
        name="Tweet Generator Agent",
        instructions="""
        You are a specialized tweet generator for SUI momentum trading analysis.
        
        You will receive analysis data from the momentum agent and create an engaging tweet.
        
        IMPORTANT: You should ONLY receive coins that meet strict HIGH-CONVICTION criteria:
        - 20+ unique buyers AND $5000+ volume
        - If you somehow receive a coin with less than 20 buyers OR less than $5000 volume, REFUSE to create a tweet
        
        TWEET STYLE AND STRUCTURE:
        - Use lowercase throughout (no caps except for coin symbols)
        - Casual, insider tone like you're sharing alpha
        - Start with the main narrative/thesis
        - Include specific dollar amounts and percentages
        - Use bullet points (•) for multiple data points when relevant
        - End with a memorable/philosophical line
        - No hashtags or emojis
        - Maximum 280 characters
        
        AVAILABLE DATA ONLY (don't make up other info):
        - Price change percentage (from top gainers data)
        - Number of unique buyers (from API)
        - Trading volume in USD (from API)
        - Timeframe (1 hour)
        
        DO NOT MENTION (we don't have this data):
        - Liquidity levels
        - Support/resistance levels  
        - Market cap
        - Technical indicators
        - Chart patterns
        
        EXAMPLE STRUCTURES:
        "$SYMBOL up X% with Y buyers and $Z volume in 1h
        
        • Y unique buyers moved $Z through the market
        • price momentum building while volume confirms interest
        • sui ecosystem plays hitting different
        
        sometimes the best plays happen when nobody's watching"
        
        OR:
        
        "$SYMBOL climbing X% while most sleep on sui ecosystem
        
        Y unique buyers pushed $Z volume past expectations. remember when small caps were just 'lottery tickets'?
        
        smart money doesn't announce entries, they build them"
        
        CRITICAL: Only create tweets for coins with 20+ buyers AND $5000+ volume
        
        After creating the tweet, call log_tweet() to log it.
        """,
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
        tools=[get_top_gainers, get_unique_buyers_count, get_trade_volume],
        handoffs=[tweet_generator_agent],
    )

    result = Runner.run_sync(
        momentum_agent,
        f"It's {current_time}. Find and analyze a high-conviction SUI momentum play. If you find one, hand it off to the tweet generator.",
        session=session,
        max_turns=50,
    )

    print(f"\nFinal Result: {result.final_output}")


if __name__ == "__main__":
    main()
