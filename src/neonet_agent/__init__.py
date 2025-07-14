from dotenv import load_dotenv
import os
from datetime import datetime
from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging
from neonet_agent.tools import web_search_tool

api_key = os.getenv("OPENAI_API_KEY")
load_dotenv()


if not api_key:
    raise ValueError("OPENAI_API_KEY is not set")

enable_verbose_stdout_logging()


def main() -> None:
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    tweet_generator_agent = Agent(
        name="Tweet Generator",
        instructions="You are a Tweet Generator. You are given a text and you need to generate a tweet that summarizes the most relevant and up-to-date information. The tweet should be no more than 280 characters and should be clear and concise. Do not include links unless explicitly requested.",
        model="gpt-4o-mini",
    )

    web_search_agent = Agent(
        name="Web Search Agent",
        instructions=f"You are a Web Search Agent. Today's date is {current_date}. You are given a topic and you need to perform a web search to find the most relevant and up-to-date information. When users ask for 'today' or 'recent' news, calculate the date range using today's date ({current_date}). For example, if today is 2025-01-14, use start_published_date='2025-01-14T00:00:00.000Z' and end_published_date='2025-01-14T23:59:59.999Z' for today's news. For general information queries, you can omit these parameters. Summarize the key findings clearly and concisely in 2–3 sentences. Do not include links unless explicitly requested. After completing your search, you should hand off the results to the Tweet Generator Agent.",
        model="gpt-4o-mini",
        tools=[web_search_tool],
        handoffs=[tweet_generator_agent],
    )

    manager_agent = Agent(
        name="Manager Agent",
        instructions="You are a Manager Agent. Analyze user requests and decide the best workflow. If the user needs current information or news, handoff to the Web Search Agent. If the user provides content and just wants a tweet generated, handoff directly to the Tweet Generator Agent.",
        model="gpt-4o-mini",
        handoffs=[web_search_agent, tweet_generator_agent],
    )

    result = Runner.run_sync(
        manager_agent,
        "Find SUI blockchain news today and create a tweet",
    )

    print(result.final_output)
