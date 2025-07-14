from dotenv import load_dotenv
import os
from datetime import datetime
from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging
from neonet_agent.tools import web_search_tool
from pydantic import BaseModel, Field, field_validator

api_key = os.getenv("OPENAI_API_KEY")
load_dotenv()


if not api_key:
    raise ValueError("OPENAI_API_KEY is not set")

# enable_verbose_stdout_logging()


class TweetOutput(BaseModel):
    tweet: str = Field(..., description="The generated tweet content")
    character_count: int = Field(..., description="Number of characters in the tweet")
    
    @field_validator('tweet')
    @classmethod
    def validate_tweet_length(cls, v):
        if len(v) > 280:
            raise ValueError(f'Tweet must be 280 characters or less. Current length: {len(v)}')
        if len(v) < 10:
            raise ValueError(f'Tweet must be at least 10 characters. Current length: {len(v)}')
        return v


def main() -> None:
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    tweet_generator_agent = Agent(
        name="Tweet Generator",
        instructions="""
        You are a Tweet Generator. Generate engaging tweets that summarize information.
        
        CRITICAL REQUIREMENTS:
        1. The tweet content must be EXACTLY 220 characters or less
        2. Count ONLY the tweet text - do NOT include the character count in the tweet content
        3. Do not add "(Character count: X)" or similar text to the tweet itself
        4. Do NOT include hashtags or emojis - plain text only
        5. Make tweets engaging, clear, and concise using only words
        6. Do not include links unless explicitly requested
        
        OUTPUT FORMAT:
        - tweet: [your tweet content here - max 220 chars, plain text only]
        - character_count: [actual character count]
        
        EXAMPLE:
        tweet: "SUI blockchain gained 12 percent today reaching 3.90 dollars with record TVL of 2.20 billion showing strong market confidence"
        character_count: 127
        """,
        model="gpt-4o-mini",
        output_type=TweetOutput,
    )

    web_search_agent = Agent(
        name="Web Search Agent",
        instructions=f"""
        You are a Web Search Agent. Today's date is {current_date}. 
        
        YOUR ONLY JOB: Search for information, summarize, and handoff.
        
        CRITICAL RULES:
        1. You do NOT generate tweets - NEVER create tweets
        2. You do NOT create final content  
        3. You do NOT include emojis or hashtags in your summary
        4. You ONLY search, summarize, and handoff
        
        MANDATORY PROCESS:
        1. Search for the requested information using your tool
        2. Summarize key findings in 2-3 clear sentences
        3. IMMEDIATELY call transfer_to_tweet_generator function - DO NOT SKIP THIS STEP
        
        You MUST handoff to Tweet Generator after every search. This is not optional.
        
        For date ranges: Only use when users ask for recent/current news or specific time periods.
        For example, if today is 2025-01-14, use start_published_date='2025-01-14T00:00:00.000Z' and end_published_date='2025-01-14T23:59:59.999Z' for today's news.
        """,
        model="gpt-4o-mini",
        tools=[web_search_tool],
        handoffs=[tweet_generator_agent],
    )

    manager_agent = Agent(
        name="Manager Agent",
        instructions="""
        You are a Manager Agent. Analyze user requests and decide the appropriate workflow.
        
        DECISION LOGIC:
        - If user asks for current news, recent information, or "today's" content → handoff to Web Search Agent
        - If user has existing content and just wants a tweet → handoff to Tweet Generator
        - If user asks for both search and tweet → handoff to Web Search Agent (it will chain to Tweet Generator)
        
        Always choose the most appropriate agent based on the user's request.
        """,
        model="gpt-4o-mini",
        handoffs=[web_search_agent, tweet_generator_agent],
    )

    result = Runner.run_sync(manager_agent, "Find SUI blockchain news today and create a tweet")
    print(result.final_output)


if __name__ == "__main__":
    main()
