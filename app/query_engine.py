import os
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from dotenv import load_dotenv

load_dotenv()


def create_agent_with_multiple_dfs(dfs: dict):
    # Combine all dataframes into one agent
    agent = create_pandas_dataframe_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        df=list(dfs.values()),
        verbose=True,
        allow_dangerous_code=True
    )
    return agent

def run_query(agent, query: str):
    try:
        result = agent.invoke(query)
        return result
    except Exception as e:
        return f"Error: {e}"
