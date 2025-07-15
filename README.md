1. post to twitter
2. reply to mentions
3. interact with target user's tweet
4. all info about SUI eco system
5. web search 
6. crypto panic
7. personality
8. biases



Manager:                                                

get trending coins 

plan searches for trending coins

get news about each coin

extract relevant data that can go viral

store in db

generate tweet

post tweet


get mentions

identify request

decide if should reply or not

tweet generation

post tweet


get tweets from target users

decide if should reply or not



# Install openai-agents

export GIT_CONFIG_GLOBAL=/c/git-config

uv pip install "git+https://github.com/openai/openai-agents-python@main"


graph TD
    A[Scheduler<br>(e.g., every 30 mins)] --> B(<b>Orchestrator Agent</b><br>Editor-in-Chief);

    subgraph "Analyst Agent Teams (The Reporters)"
        C(<b>Momentum Analyst</b><br>Finds high-conviction pumps)
        D(<b>Trader Analyst</b><br>Tracks smart money)
        E(<b>DeFi Analyst</b><br>Monitors pool health)
        F(<b>Anomaly Analyst</b><br>Spots market divergences)
        G(<b>Capital Flow Analyst</b><br>Predicts rotations)
    end
    
    B --> C;
    B --> D;
    B --> E;
    B --> F;
    B --> G;

    C --> H(<b>Tweet Composer</b><br>The "Writer");
    D --> H;
    E --> H;
    F --> H;
    G --> H;

    H --> I[Post Tweet];