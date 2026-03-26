import os
from datetime import datetime
from dotenv import load_dotenv

from langchain_openrouter import ChatOpenRouter
from langchain.agents import create_agent
from langchain.tools import tool


load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "hello world"


@tool
def simple_calculator(expression: str) -> str:
    """Perform basic mathematical calculations. Input should be a math expression like '25 * 4'."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_weather_info(city: str) -> str:
    """Get weather information for a city. Input should be a city name."""
    mock_weather = {
        "New York": "Clear, 72°F",
        "London": "Rainy, 55°F",
        "Tokyo": "Sunny, 68°F",
    }
    return mock_weather.get(city, f"Weather data for {city} not available")


@tool
def get_current_time() -> str:
    """Get the current date and time. Takes no input."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def initialize_agent():
    """
    Initialize a LangChain agent using OpenRouter with Anthropic models.
    
    Models available through OpenRouter (cheap options):
    - anthropic/claude-3-haiku: Very fast, cheapest Anthropic model
    - anthropic/claude-3.5-haiku: Better than Haiku, still very cheap
    - anthropic/claude-3.5-sonnet: Balanced cost and performance
    - anthropic/claude-3-opus: Most capable, higher cost
    
    Returns:
        Compiled LangGraph agent ready to run
    """

    llm = ChatOpenRouter(
        model="anthropic/claude-3.5-haiku",
        temperature=0.2,
        api_key=OPENROUTER_API_KEY,
    )

    tools = [simple_calculator, get_weather_info, get_current_time]

    agent = create_agent(
        llm,
        tools,
        system_prompt="You are a helpful AI assistant that uses tools to answer questions and complete tasks. Be concise and helpful in your responses.",
    )

    return agent


def run_agent(query: str, agent):
    """
    Run the agent with a user query.
    
    Args:
        query: The user's question or task
        agent: The compiled LangGraph agent
    
    Returns:
        The agent's response
    """
    response = agent.invoke({"messages": [("user", query)]})

    messages = response.get("messages", [])
    if messages:
        last_message = messages[-1]
        if hasattr(last_message, "content"):
            return last_message.content
        else:
            return str(last_message)
    
    return "No response generated"


if __name__ == "__main__":
    print("Initializing LangChain agent with OpenRouter and Claude 3.5 Haiku...\n")
    agent = initialize_agent()

    queries = [
        "What is 25 * 4?",
        "Tell me a fun fact about AI",
        "What's the current time?",
    ]

    for query in queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        result = run_agent(query, agent)
        print(f"\nFinal Response: {result}\n")
