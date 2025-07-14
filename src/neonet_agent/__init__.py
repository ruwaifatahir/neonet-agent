from dotenv import load_dotenv
import os
from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set")

enable_verbose_stdout_logging()


def main() -> None:
    agent = Agent(
        name="Neonet Agent",
        instructions="You are a Neonet agent. You are given a topic and you need to generate a tweet about it. The tweet should be 280 characters or less. Do not add hashtags or emojis.",
        model="gpt-4o-mini",
        tools=[],
    )

    result = Runner.run_sync(
        agent,
        "Generate a tweet as a parody of Morty. Use the get_bias_of_morty tool to get the bias of Morty.",
    )

    print(result.final_output)
