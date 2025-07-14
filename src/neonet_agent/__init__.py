from dotenv import load_dotenv
import os
from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging
from neonet_agent.tools import web_search_tool

api_key = os.getenv("OPENAI_API_KEY")
load_dotenv()



if not api_key:
    raise ValueError("OPENAI_API_KEY is not set")

enable_verbose_stdout_logging()


def main() -> None:
    tweet_generator_agent = Agent(
        name="Tweet Generator",
        instructions="You are a Tweet Generator. You are given a text and you need to generate a tweet that summarizes the most relevant and up-to-date information. The tweet should be no more than 280 characters and should be clear and concise. Do not include links unless explicitly requested.",
        model="gpt-4o-mini",
    )

    web_search_agent = Agent(
        name="Web Search Agent",
        instructions="You are a Web Search Agent. You are given a topic and you need to perform a web search to find the most relevant and up-to-date information. Summarize the key findings clearly and concisely in 2–3 sentences. Do not include links unless explicitly requested. After completing your search, you should hand off the results to the Tweet Generator Agent.",
        model="gpt-4o-mini",
        tools=[web_search_tool],
        handoffs=[tweet_generator_agent]
    )



    result = Runner.run_sync(
        web_search_agent,
        "SUI blockchain news",
    
    )

    print(result.final_output)
