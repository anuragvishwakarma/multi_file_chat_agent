import os
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.initialize import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool

from dotenv import load_dotenv

load_dotenv()


def create_agent_with_multiple_dfs(dfs: dict):
    # Convert dfs dict to tools for each DataFrame
    tools = []
    for name, df in dfs.items():
        agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0, model="gpt-4"),
            df,
            verbose=True,
            allow_dangerous_code=True,
        )
        tools.append(Tool(name=name, func=agent.run, description=f"Tool for {name} sheet"))

    # Memory for conversation
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    agent_executor = initialize_agent(
        tools,
        ChatOpenAI(temperature=0, model="gpt-4"),
        agent="chat-conversational-react-description",
        memory=memory,
        verbose=True,
        allow_dangerous_code =True,
        handle_parsing_errors=True
    )
    return agent_executor

def run_query(agent, query: str):
    try:
        result = agent.invoke(query)
        return result
    except Exception as e:
        return f"Error: {e}"
